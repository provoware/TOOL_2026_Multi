"""Maschinenlesbarer Barrierefreiheits- und Datensicherheits-Prüfkatalog.

Das Vorhandensein eines Tests ist KEIN Nachweis seines erfolgreichen CI-Laufs.
Ein echter Bildschirmleser- oder Sichttest bleibt als offen ausgewiesen.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.accessibility_contracts import accessibility_matrix

EVIDENCE = {
    "tastatur": ("P2", ["tests/test_keyboard_journeys_gui.py",
                       "tests/test_keyboard_workflow_gui.py"]),
    "fokus": ("P2", ["tests/test_accessibility_eight_windows_gui.py",
                    "tests/test_keyboard_workflow_gui.py"]),
    "beschriftung": ("P2", ["tests/test_accessibility_eight_windows_gui.py",
                          "tests/test_calendar_keyboard_save_failures_gui.py"]),
    "kontrast": ("P3", ["tests/test_accessibility_eight_windows_gui.py"]),
    "zoom": ("P3", ["tests/test_accessibility_eight_windows_gui.py"]),
    "bildschirmleser_praxis": ("P2", []),
    "speichern_abbrechen_wiederherstellen": (
        "P1", ["tests/test_restore.py", "tests/test_storage_error_protection_gui.py",
               "tests/test_keyboard_workflow_gui.py"]),
}


def build_report(root: Path = ROOT) -> dict:
    entries = []
    for case in accessibility_matrix():
        priority, sources = EVIDENCE[case.dimension]
        existing = [source for source in sources if (root / source).is_file()]
        if case.dimension == "bildschirmleser_praxis":
            status = "praxispruefung_offen"
        elif existing:
            status = "automatische_teilabdeckung"
        else:
            status = "ohne_automatischen_nachweis"
        entries.append({
            "modul": case.module, "kriterium": case.dimension,
            "prioritaet": priority, "status": status,
            "vorhandene_testdateien": existing,
        })
    return {
        "schema": 1,
        "zeitpunkt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "gesamtfaelle": len(entries),
        "hinweis": "Dateiexistenz und Testzuordnung sind keine Testergebnisse. "
                   "Automatische Teilabdeckung ersetzt keine echte Sicht-/Screenreader-Abnahme.",
        "prueffalle": entries,
        "offen": [entry for entry in entries if entry["status"] != "automatische_teilabdeckung"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Barrierefreiheitsbefunde als JSON erfassen")
    parser.add_argument("--output", type=Path, help="Optional JSON-Bericht speichern")
    args = parser.parse_args()
    text = json.dumps(build_report(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
