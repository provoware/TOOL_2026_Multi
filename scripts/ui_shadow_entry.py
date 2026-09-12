#!/usr/bin/env python3
"""Robuster Einstieg und Evidenz-Wächter für den UI-Shadow-Gate.

Dieses Skript bleibt absichtlich stdlib-only. Es stellt zuerst den Projektpfad
sicher, startet danach den eigentlichen PySide6-Gate und kann dessen Evidenz
unabhängig von Qt hart validieren. Dadurch werden Import-/Bootstrapfehler nicht
mehr als scheinbar erfolgreiche Shadow-Läufe gewertet.
"""

from __future__ import annotations

import argparse
import json
import os
import runpy
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = PROJECT_ROOT / "scripts" / "ui_shadow_gate.py"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _context_from_argv(argv: Sequence[str]) -> tuple[str, Path]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--profile", choices=("pr", "release"), default="pr")
    parser.add_argument("--output-dir", type=Path, default=Path("berichte/ui-shadow"))
    args, _unknown = parser.parse_known_args(list(argv))
    return args.profile, args.output_dir


def _append_step_summary(markdown: Path) -> None:
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if not step_summary or not markdown.exists():
        return
    with open(step_summary, "a", encoding="utf-8") as handle:
        handle.write(markdown.read_text(encoding="utf-8"))


def write_infrastructure_evidence(
    output_dir: Path,
    *,
    profile: str,
    stage: str,
    exc: BaseException,
) -> Path:
    """Schreibt selbst bei frühem Import-/Bootstrapfehler verwertbare Evidenz."""
    output_dir.mkdir(parents=True, exist_ok=True)
    now = _utc_now()
    payload = {
        "schema_version": 1,
        "mode": "shadow",
        "profile": profile,
        "git_sha": os.environ.get("GITHUB_SHA", "local"),
        "run_number": os.environ.get("GITHUB_RUN_NUMBER", "local"),
        "started_utc": now,
        "finished_utc": now,
        "summary": {
            "status": "infrastructure-error",
            "matrix_cases": 0,
            "window_instances": 0,
            "errors": 0,
            "warnings": 0,
            "info": 0,
            "infrastructure_errors": 1,
            "blocking": False,
            "promotion_candidate": False,
        },
        "infrastructure": {
            "stage": stage,
            "exception_type": exc.__class__.__name__,
            "message": str(exc),
            "python": sys.version,
            "executable": sys.executable,
            "cwd": str(Path.cwd()),
            "project_root": str(PROJECT_ROOT),
            "target": str(TARGET),
            "traceback": "".join(traceback.format_exception(exc)),
        },
        "matrix": [],
        "metrics": [],
        "findings": [],
    }
    evidence = output_dir / "ui_shadow_evidence.json"
    evidence.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = output_dir / "ui_shadow_summary.md"
    summary.write_text(
        "# Provoware UI-Shadow-Gate\n\n"
        f"- Profil: **{profile}**\n"
        "- Status: **infrastructure-error**\n"
        f"- Phase: **{stage}**\n"
        f"- Fehlerart: **{exc.__class__.__name__}**\n"
        f"- Meldung: `{str(exc)}`\n\n"
        "Der Shadow-Lauf ist technisch ungültig und darf nicht als Kalibrierungslauf zählen.\n",
        encoding="utf-8",
    )
    _append_step_summary(summary)
    return evidence


def validate_evidence(path: Path) -> tuple[bool, tuple[str, ...]]:
    """Prüft nur die Funktionsfähigkeit des Prüfsystems, nicht dessen UI-Befunde."""
    problems: list[str] = []
    if not path.is_file():
        return False, (f"Evidenzdatei fehlt: {path}",)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, (f"Evidenz ist kein gültiges JSON: {exc}",)

    if not isinstance(payload, dict):
        return False, ("Evidenzwurzel ist kein Objekt.",)
    if payload.get("schema_version") != 1:
        problems.append("schema_version muss 1 sein.")
    if payload.get("mode") != "shadow":
        problems.append("mode muss 'shadow' sein.")

    profile = payload.get("profile")
    if profile not in {"pr", "release"}:
        problems.append("profile muss 'pr' oder 'release' sein.")

    summary = payload.get("summary")
    if not isinstance(summary, dict):
        problems.append("summary fehlt oder ist ungültig.")
        return False, tuple(problems)

    status = summary.get("status")
    infrastructure_errors = summary.get("infrastructure_errors", 0)
    if status == "infrastructure-error" or infrastructure_errors:
        problems.append("Shadow-Prüfsystem meldet einen Infrastrukturfehler.")

    expected_cases = 8 if profile == "pr" else 60 if profile == "release" else None
    matrix_cases = summary.get("matrix_cases")
    window_instances = summary.get("window_instances")
    if expected_cases is not None and matrix_cases != expected_cases:
        problems.append(f"matrix_cases muss für {profile} exakt {expected_cases} sein.")
    if not isinstance(window_instances, int) or window_instances <= 0:
        problems.append("window_instances muss größer als 0 sein.")
    elif isinstance(matrix_cases, int) and window_instances < matrix_cases * 3:
        problems.append("Es wurden weniger als drei Kernfenster pro Matrixfall geprüft.")

    if not payload.get("finished_utc"):
        problems.append("finished_utc fehlt.")
    metrics = payload.get("metrics")
    findings = payload.get("findings")
    if not isinstance(metrics, list):
        problems.append("metrics muss eine Liste sein.")
    elif isinstance(window_instances, int) and len(metrics) < window_instances:
        problems.append("metrics enthält weniger Einträge als geprüfte Fensterinstanzen.")
    if not isinstance(findings, list):
        problems.append("findings muss eine Liste sein.")

    return not problems, tuple(problems)


def _bind_execution_globals(namespace: dict[str, object], name: str, replacements: dict[str, object]) -> None:
    """Bindet Ersatzobjekte an den echten Global-Namespace einer geladenen Funktion.

    ``runpy.run_path`` kann einen Ergebnis-Namespace liefern, der nicht mit dem
    ``__globals__``-Mapping bereits erzeugter Funktionen identisch ist. Nur den
    Ergebnis-Namespace zu ändern reicht dann nicht. Diese Funktion macht die
    Bindung explizit und prüfbar, damit der CI-Lauf exakt dieselbe Dashboard-
    Präsentationsschicht nutzt wie der Produktstart.
    """
    target = namespace.get(name)
    globals_map = getattr(target, "__globals__", None)
    if not callable(target) or not isinstance(globals_map, dict):
        raise RuntimeError(f"Shadow-Gate-Funktion {name!r} besitzt keinen bindbaren Global-Namespace.")
    globals_map.update(replacements)
    namespace.update(replacements)


def _load_shadow_runtime() -> dict[str, object]:
    """Lädt den Gate-Code ohne ihn sofort zu starten und gleicht ihn an Produktion an."""
    if not TARGET.is_file():
        raise FileNotFoundError(f"Shadow-Gate-Ziel fehlt: {TARGET}")

    namespace = runpy.run_path(str(TARGET), run_name="provoware_ui_shadow_gate_runtime")
    original_core = namespace.get("_core_factories")
    dashboard_type = namespace.get("Dashboard")
    fake_texts = namespace.get("FakeTexts")
    fake_logger = namespace.get("FakeLogger")
    if not callable(original_core) or not callable(dashboard_type) or not callable(fake_texts) or not callable(fake_logger):
        raise RuntimeError("Shadow-Gate stellt den erwarteten Dashboard-Vertrag nicht bereit.")

    from app.main import configure_dashboard_presentation

    def production_dashboard(root: Path):
        dashboard = dashboard_type(fake_texts(), fake_logger(), root)
        return configure_dashboard_presentation(dashboard)

    def production_core_factories(root: Path, zoom: int):
        factories = tuple(original_core(root, zoom))
        if len(factories) != 3:
            raise RuntimeError("Shadow-Gate muss exakt drei Kernfenster-Fabriken bereitstellen.")
        return (lambda: production_dashboard(root), *factories[1:])

    # Wichtig: Nicht nur die von runpy zurückgegebene Dictionary-Kopie ändern.
    # ``run()`` löst ``_core_factories`` über sein eigenes __globals__ auf.
    # Genau diese Verbindung war im ersten realen Kalibrierungslauf ungetestet.
    _bind_execution_globals(
        namespace,
        "run",
        {
            "_core_factories": production_core_factories,
            "_provoware_production_dashboard_factory": production_dashboard,
        },
    )
    namespace["_provoware_production_dashboard_factory"] = production_dashboard
    namespace["_provoware_production_core_factories"] = production_core_factories
    return namespace


def _run_target(argv: Sequence[str]) -> int:
    old_argv = sys.argv[:]
    try:
        sys.argv = [str(TARGET), *argv]
        namespace = _load_shadow_runtime()
        target_main = namespace.get("main")
        if not callable(target_main):
            raise RuntimeError("Shadow-Gate besitzt keinen aufrufbaren Programmeinstieg.")
        try:
            code = target_main()
        except SystemExit as exc:
            code = exc.code
            if code is None:
                return 0
            if isinstance(code, int):
                return code
            print(code, file=sys.stderr)
            return 1
        return int(code or 0)
    finally:
        sys.argv = old_argv


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if "--bootstrap-check" in argv:
        try:
            __import__("app")
        except Exception as exc:
            print(f"Bootstrap fehlgeschlagen: {exc}", file=sys.stderr)
            return 2
        print(f"BOOTSTRAP_OK {PROJECT_ROOT}")
        return 0

    if "--validate-evidence" in argv:
        parser = argparse.ArgumentParser(description="UI-Shadow-Evidenz hart validieren")
        parser.add_argument("--validate-evidence", type=Path, required=True)
        args = parser.parse_args(argv)
        ok, problems = validate_evidence(args.validate_evidence)
        if ok:
            payload = json.loads(args.validate_evidence.read_text(encoding="utf-8"))
            summary = payload["summary"]
            print(
                "UI_SHADOW_EVIDENCE_OK "
                f"status={summary.get('status')} "
                f"matrix_cases={summary.get('matrix_cases')} "
                f"window_instances={summary.get('window_instances')}"
            )
            return 0
        for problem in problems:
            print(f"UI_SHADOW_EVIDENCE_INVALID: {problem}", file=sys.stderr)
        return 2

    profile, output_dir = _context_from_argv(argv)
    try:
        return _run_target(argv)
    except BaseException as exc:
        write_infrastructure_evidence(
            output_dir,
            profile=profile,
            stage="launcher-or-import",
            exc=exc,
        )
        print(f"UI-Shadow-Gate Infrastrukturfehler: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
