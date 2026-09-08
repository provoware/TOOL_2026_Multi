#!/usr/bin/env python3
"""Laienfreundliche reale Kubuntu/X11-Endabnahme für TOOL_2026_Multi.

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


@dataclass(frozen=True)
class CheckResult:
    key: str
    label: str
    status: str
    detail: str


def environment_checks(env: dict[str, str] | None = None) -> list[CheckResult]:
    values = dict(os.environ if env is None else env)
    session = values.get("XDG_SESSION_TYPE", "").strip().lower()
    desktop = " ".join((values.get("XDG_CURRENT_DESKTOP", ""), values.get("DESKTOP_SESSION", ""))).lower()
    display = values.get("DISPLAY", "").strip()
    return [
        CheckResult("linux", "Linux-System", "OK" if sys.platform.startswith("linux") else "BLOCKIERT", platform.platform()),
        CheckResult("x11", "X11-Sitzung", "OK" if session == "x11" and display else "BLOCKIERT",
                    f"Sitzung={session or 'unbekannt'}, DISPLAY={display or 'fehlt'}"),
        CheckResult("kde", "KDE/Kubuntu-Oberfläche", "OK" if ("kde" in desktop or "plasma" in desktop) else "HINWEIS",
                    desktop or "Desktop nicht erkannt"),
    ]


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
        if completed.returncode == -signal.SIGTERM and len(reports) == 1 and logs.is_file():
            text = reports[0].read_text(encoding="utf-8")
            if "SIGTERM" in text and "keine Nutzerdaten verändert" in text:
                return CheckResult("signal", "Echter Signal-/Wächtertest", "OK",
                                   "SIGTERM erkannt; Bericht und JSONL-Ereignis nur im Tempordner erzeugt.")
        return CheckResult("signal", "Echter Signal-/Wächtertest", "FEHLER",
                           f"Rückgabecode={completed.returncode}; Berichte={len(reports)}")


def write_report(root: Path, results: list[CheckResult], visual: dict[str, bool] | None = None) -> tuple[Path, Path]:
    visual = dict(visual or {})
    now = datetime.now(timezone.utc).astimezone()
    report_dir = root / "berichte"
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%Y%m%d_%H%M%S")
    json_path = report_dir / f"KUBUNTU_X11_ABNAHME_{stamp}.json"
    txt_path = report_dir / f"KUBUNTU_X11_ABNAHME_{stamp}.txt"
    automatic_ok = all(item.status in {"OK", "HINWEIS"} for item in results)
    visual_ok = bool(visual) and all(visual.values())
    overall = "OK" if automatic_ok and visual_ok else "NICHT_VOLLSTAENDIG"
    payload = {
        "schema_version": 1,
        "time": now.isoformat(timespec="seconds"),
        "tool": "TOOL_2026_Multi",
        "target": "Kubuntu/KDE X11 reale Endabnahme",
        "status": overall,
        "automatic_checks": [asdict(item) for item in results],
        "visual_confirmations": visual,
        "safety": "Signaltest ausschließlich in Tempdaten; keine Song-/Nutzerdaten verändert.",
    }
    temporary = json_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, json_path)
    lines = [
        "PROVOWARE · KUBUNTU/X11-ENDABNAHME",
        "=" * 54,
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
    txt_path.write_text("\n".join(lines), encoding="utf-8")
    return txt_path, json_path


def automatic_run(root: Path = ROOT) -> tuple[list[CheckResult], tuple[Path, Path]]:
    results = environment_checks()
    results.append(signal_probe(root))
    return results, write_report(root, results)


def gui(root: Path = ROOT) -> int:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout, QLabel, QMessageBox,
                                   QPushButton, QTextEdit, QVBoxLayout)
    from app.ui_standards import apply_global_style

    app = QApplication.instance() or QApplication(sys.argv)
    dialog = QDialog()
    dialog.setWindowTitle("Provoware · Kubuntu/X11-Endabnahme")
    dialog.resize(820, 660)
    apply_global_style(dialog)
    layout = QVBoxLayout(dialog)
    title = QLabel("Kubuntu/X11-Endabnahme")
    title.setObjectName("sectionTitle")
    layout.addWidget(title)
    info = QLabel("Automatische System- und Signalprüfung plus drei sichtbare Bestätigungen. Keine Songdaten werden verändert.")
    info.setWordWrap(True)
    layout.addWidget(info)

    results = environment_checks()
    results.append(signal_probe(root))
    automatic = QTextEdit()
    automatic.setReadOnly(True)
    automatic.setMaximumHeight(180)
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
        "Referenzlayout sichtbar: Dark Orange, linke Navigation, 7 Schnellkacheln, 2×2 Hauptkarten": QCheckBox(),
        "Tastaturfokus sichtbar und logisch per Tab erreichbar": QCheckBox(),
        "Zoom 100/125/150/175/200 % bleibt lesbar und ohne abgeschnittene Hauptbedienung": QCheckBox(),
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
    status = QLabel("Alle drei sichtbaren Punkte müssen bestätigt werden.")
    status.setWordWrap(True)
    layout.addWidget(status)

    def update_finish() -> None:
        finish.setEnabled(all(box.isChecked() for box in checks.values()))

    for box in checks.values():
        box.stateChanged.connect(update_finish)

    def save() -> None:
        visual = {label: box.isChecked() for label, box in checks.items()}
        txt, json_file = write_report(root, results, visual)
        automatic_ok = all(item.status in {"OK", "HINWEIS"} for item in results)
        if automatic_ok and all(visual.values()):
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
        return 0 if all(item.status in {"OK", "HINWEIS", "BLOCKIERT"} for item in results) else 1
    return gui(ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
