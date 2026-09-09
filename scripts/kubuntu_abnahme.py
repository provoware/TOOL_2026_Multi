#!/usr/bin/env python3
"""Laienfreundliche reale Kubuntu-26.04-/Wayland-Endabnahme.

Die automatischen Prüfungen verändern keine Nutzerdaten. Der Signaltest läuft
vollständig in einem temporären Verzeichnis. Sichtbare GUI-Merkmale werden nur
nach ausdrücklicher Bestätigung des Nutzers als bestanden dokumentiert.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import signal
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_RELEASE = "26.04"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.atomic_io import atomic_write_text


@dataclass(frozen=True)
class CheckResult:
    key: str
    label: str
    status: str
    detail: str


def read_os_release(path: Path = Path("/etc/os-release")) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key] = value.strip().strip('"').strip("'")
    except OSError:
        pass
    return values


def environment_checks(
    env: dict[str, str] | None = None,
    os_release: dict[str, str] | None = None,
) -> list[CheckResult]:
    values = dict(os.environ if env is None else env)
    release_values = read_os_release() if os_release is None else dict(os_release)
    session = values.get("XDG_SESSION_TYPE", "").strip().lower()
    desktop = " ".join((values.get("XDG_CURRENT_DESKTOP", ""), values.get("DESKTOP_SESSION", ""))).lower()
    wayland_display = values.get("WAYLAND_DISPLAY", "").strip()
    qpa = values.get("QT_QPA_PLATFORM", "").strip().lower()
    version_id = release_values.get("VERSION_ID", "").strip()
    distro_ids = " ".join((release_values.get("ID", ""), release_values.get("ID_LIKE", ""))).lower()
    ubuntu_base = "ubuntu" in distro_ids
    release_ok = ubuntu_base and (version_id == TARGET_RELEASE or version_id.startswith(f"{TARGET_RELEASE}."))
    qpa_ok = not qpa or qpa.startswith("wayland")
    return [
        CheckResult("linux", "Linux-System", "OK" if sys.platform.startswith("linux") else "BLOCKIERT", platform.platform()),
        CheckResult(
            "release",
            "Kubuntu-/Ubuntu-Basis 26.04",
            "OK" if release_ok else "BLOCKIERT",
            f"VERSION_ID={version_id or 'unbekannt'}, ID/ID_LIKE={distro_ids or 'unbekannt'}",
        ),
        CheckResult(
            "wayland",
            "Plasma-Wayland-Sitzung",
            "OK" if session == "wayland" and wayland_display else "BLOCKIERT",
            f"Sitzung={session or 'unbekannt'}, WAYLAND_DISPLAY={wayland_display or 'fehlt'}",
        ),
        CheckResult(
            "kde",
            "KDE/Plasma-Oberfläche",
            "OK" if ("kde" in desktop or "plasma" in desktop) else "BLOCKIERT",
            desktop or "Desktop nicht erkannt",
        ),
        CheckResult(
            "qpa_env",
            "Qt-Plattformvorgabe",
            "OK" if qpa_ok else "BLOCKIERT",
            f"QT_QPA_PLATFORM={qpa or 'nicht erzwungen'}",
        ),
    ]


def qt_platform_probe(root: Path = ROOT, env: dict[str, str] | None = None) -> CheckResult:
    """Prüft in einem Kindprozess, ob Qt tatsächlich nativ über Wayland startet."""
    probe_env = os.environ.copy()
    if env is not None:
        probe_env.update(env)
    command = [
        sys.executable,
        "-c",
        (
            "from PySide6.QtWidgets import QApplication; "
            "app=QApplication([]); "
            "print(app.platformName()); "
            "app.quit()"
        ),
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            env=probe_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return CheckResult("qt_wayland", "Qt läuft nativ über Wayland", "FEHLER", f"Qt-Probe fehlgeschlagen: {exc}")
    platform_name = completed.stdout.strip().splitlines()[-1].strip().lower() if completed.stdout.strip() else ""
    ok = completed.returncode == 0 and platform_name.startswith("wayland")
    detail = f"Qt-Plattform={platform_name or 'unbekannt'}, Rückgabecode={completed.returncode}"
    if not ok and completed.stderr.strip():
        detail += f"; Hinweis={completed.stderr.strip().splitlines()[-1][:180]}"
    return CheckResult("qt_wayland", "Qt läuft nativ über Wayland", "OK" if ok else "BLOCKIERT", detail)


def signal_probe(root: Path = ROOT) -> CheckResult:
    """Prüft den echten Prozesswächter mit SIGTERM ausschließlich in Tempdaten."""
    with tempfile.TemporaryDirectory(prefix="provoware_signalprobe_") as temp:
        probe_root = Path(temp)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(root)
        command = [
            sys.executable,
            str(root / "scripts" / "process_watch.py"),
            "--root", str(probe_root), "--",
            sys.executable, "-c",
            "import os,signal; os.kill(os.getpid(), signal.SIGTERM)",
        ]
        completed = subprocess.run(command, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, timeout=20, check=False)
        reports = list((probe_root / "berichte").glob("WAECHTER-ABSTURZ-*.txt"))
        logs = probe_root / "logs" / "ereignisse.jsonl"
        expected_codes = {-signal.SIGTERM, 256 - signal.SIGTERM}
        if completed.returncode in expected_codes and len(reports) == 1 and logs.is_file():
            text = reports[0].read_text(encoding="utf-8")
            if "SIGTERM" in text and "keine Nutzerdaten verändert" in text:
                return CheckResult("signal", "Echter Signal-/Wächtertest", "OK",
                                   "SIGTERM erkannt; Bericht und JSONL-Ereignis nur im Tempordner erzeugt.")
        return CheckResult("signal", "Echter Signal-/Wächtertest", "FEHLER",
                           f"Rückgabecode={completed.returncode}; Berichte={len(reports)}")


def checks_are_green(results: list[CheckResult]) -> bool:
    return bool(results) and all(item.status == "OK" for item in results)


def write_report(root: Path, results: list[CheckResult], visual: dict[str, bool] | None = None) -> tuple[Path, Path]:
    visual = dict(visual or {})
    now = datetime.now(timezone.utc).astimezone()
    report_dir = root / "berichte"
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%Y%m%d_%H%M%S")
    json_path = report_dir / f"KUBUNTU_2604_WAYLAND_ABNAHME_{stamp}.json"
    txt_path = report_dir / f"KUBUNTU_2604_WAYLAND_ABNAHME_{stamp}.txt"
    automatic_ok = checks_are_green(results)
    visual_ok = bool(visual) and all(visual.values())
    overall = "OK" if automatic_ok and visual_ok else "NICHT_VOLLSTAENDIG"
    payload = {
        "schema_version": 2,
        "time": now.isoformat(timespec="seconds"),
        "tool": "TOOL_2026_Multi",
        "target": "Kubuntu 26.04 LTS / KDE Plasma Wayland reale Endabnahme",
        "status": overall,
        "automatic_checks": [asdict(item) for item in results],
        "visual_confirmations": visual,
        "safety": "Signaltest ausschließlich in Tempdaten; keine Song-/Nutzerdaten verändert.",
    }
    atomic_write_text(json_path, json.dumps(payload, ensure_ascii=False, indent=2))
    lines = [
        "PROVOWARE · KUBUNTU 26.04 / WAYLAND-ENDABNAHME",
        "=" * 62,
        f"Zeit: {payload['time']}",
        f"Status: {overall}",
        "",
        "AUTOMATISCHE PRÜFUNGEN",
    ]
    lines.extend(f"[{item.status}] {item.label}: {item.detail}" for item in results)
    lines += ["", "SICHTBARE BESTÄTIGUNGEN"]
    if visual:
        lines.extend(f"[{'OK' if value else 'OFFEN'}] {key}" for key, value in visual.items())
    else:
        lines.append("[OFFEN] Noch keine sichtbare Bestätigung erfasst.")
    lines += ["", "DATENSCHUTZ / SICHERHEIT", payload["safety"], ""]
    atomic_write_text(txt_path, "\n".join(lines))
    return txt_path, json_path


def automatic_run(root: Path = ROOT) -> tuple[list[CheckResult], tuple[Path, Path]]:
    results = environment_checks()
    results.append(qt_platform_probe(root))
    results.append(signal_probe(root))
    return results, write_report(root, results)


def gui(root: Path = ROOT) -> int:
    from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout, QLabel, QMessageBox,
                                   QPushButton, QTextEdit, QVBoxLayout)
    from app.ui_standards import apply_global_style

    app = QApplication.instance() or QApplication(sys.argv)
    dialog = QDialog()
    dialog.setWindowTitle("Provoware · Kubuntu 26.04 / Wayland-Endabnahme")
    dialog.resize(860, 700)
    apply_global_style(dialog)
    layout = QVBoxLayout(dialog)
    title = QLabel("Kubuntu 26.04 · Wayland-Endabnahme")
    title.setObjectName("sectionTitle")
    layout.addWidget(title)
    info = QLabel(
        "Automatische Prüfung von Kubuntu/Ubuntu 26.04, Plasma, Wayland und dem tatsächlich verwendeten Qt-Backend. "
        "Danach bestätigst du die sichtbare Darstellung. Keine Songdaten werden verändert."
    )
    info.setWordWrap(True)
    layout.addWidget(info)

    results = environment_checks()
    results.append(CheckResult(
        "qt_wayland",
        "Qt läuft nativ über Wayland",
        "OK" if app.platformName().lower().startswith("wayland") else "BLOCKIERT",
        f"Qt-Plattform={app.platformName()}",
    ))
    results.append(signal_probe(root))
    automatic = QTextEdit()
    automatic.setReadOnly(True)
    automatic.setMaximumHeight(220)
    automatic.setPlainText("\n".join(f"{item.status}: {item.label} – {item.detail}" for item in results))
    layout.addWidget(automatic)

    open_button = QPushButton("Dashboard für Sichtprüfung öffnen")
    layout.addWidget(open_button)
    child: list[subprocess.Popen[str]] = []

    def open_dashboard() -> None:
        if child and child[0].poll() is None:
            return
        child[:] = [subprocess.Popen([sys.executable, "-m", "app.main"], cwd=root, text=True)]

    open_button.clicked.connect(open_dashboard)
    checks = {
        "1366×768 bei 125/150 %: Menü, Karten und Eingaben ohne Überlagerungen": QCheckBox(),
        "175/200 %: Hauptbedienung bleibt erreichbar und Texte bleiben lesbar": QCheckBox(),
        "Tastaturfokus, Theme Kontrast und Menü-Schalter sind klar erkennbar": QCheckBox(),
        "Fenster, Menüs und Eingabefokus reagieren unter Wayland ohne sichtbare Darstellungsfehler": QCheckBox(),
    }
    for label, box in checks.items():
        row = QHBoxLayout()
        row.addWidget(box)
        text = QLabel(label)
        text.setWordWrap(True)
        row.addWidget(text, 1)
        layout.addLayout(row)

    finish = QPushButton("Abnahmebericht speichern")
    finish.setEnabled(False)
    layout.addWidget(finish)
    status = QLabel("Alle sichtbaren Punkte und alle automatischen Prüfungen müssen grün sein.")
    status.setWordWrap(True)
    layout.addWidget(status)

    def update_finish() -> None:
        finish.setEnabled(checks_are_green(results) and all(box.isChecked() for box in checks.values()))

    for box in checks.values():
        box.stateChanged.connect(update_finish)
    update_finish()

    def save() -> None:
        visual = {label: box.isChecked() for label, box in checks.items()}
        txt, json_file = write_report(root, results, visual)
        if checks_are_green(results) and all(visual.values()):
            QMessageBox.information(dialog, "Abnahme gespeichert", f"🟢 Abnahme vollständig.\n\n{txt}\n{json_file}")
            dialog.accept()
        else:
            QMessageBox.warning(dialog, "Abnahme nicht vollständig", f"Bericht gespeichert, aber mindestens eine Prüfung ist offen oder fehlgeschlagen.\n\n{txt}")

    finish.clicked.connect(save)
    result = dialog.exec()
    if child and child[0].poll() is None:
        child[0].terminate()
        try:
            child[0].wait(timeout=5)
        except subprocess.TimeoutExpired:
            child[0].kill()
    return 0 if result in {QDialog.Accepted, QDialog.Rejected} else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true", help="Nur automatische Prüfungen und Bericht ohne Fenster.")
    args = parser.parse_args()
    if args.auto:
        results, paths = automatic_run(ROOT)
        for item in results:
            print(f"{item.status}: {item.label} – {item.detail}")
        print(f"Bericht: {paths[0]}")
        return 0 if checks_are_green(results) else 1
    return gui(ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
