"""Sicherer Programmeinstieg mit prüfbarem Headless-Modus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.event_log import EventLogger, emergency_message
from app.texts import TextRegistry

ROOT = Path(__file__).resolve().parent.parent


def headless_check() -> int:
    """Prüft den echten Startunterbau ohne Fenster und ohne dauerhafte Laufzeitdaten."""
    try:
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        version = manifest["tool"]["version"]
        registry = TextRegistry(ROOT / "texte" / "registry.json")
        registry.get("app.name", "TOOL_2026_Multi")
        if not version or not (ROOT / manifest["runtime"]["entrypoint"]).is_file():
            raise ValueError("Manifest enthält keinen gültigen Programmeinstieg.")
        return 0
    except Exception as error:
        print(f"HEADLESS-START-FEHLER: {type(error).__name__}: {error}")
        return 1


def main() -> int:
    version = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))["tool"]["version"]
    logger = EventLogger(ROOT, version)
    try:
        import tkinter as tk
        from app.ui import Dashboard, install_exception_handler
        root = tk.Tk()
        dashboard = Dashboard(root, TextRegistry(ROOT / "texte" / "registry.json"), logger, ROOT)
        install_exception_handler(root, logger, dashboard.refresh)
        logger.record(severity="INFO", area="START", summary="Das Programm wurde sicher gestartet.",
                      cause="Normaler Programmstart", protection="Es waren keine Schutzmaßnahmen nötig.",
                      next_step="Sie können das Werkzeug jetzt verwenden.")
        dashboard.refresh()
        root.mainloop()
        logger.record(severity="INFO", area="ENDE", summary="Das Programm wurde kontrolliert beendet.",
                      cause="Normales Schließen der Anwendung",
                      protection="Alle laufenden Oberflächenaktionen waren beendet.",
                      next_step="Keine weitere Aktion nötig.")
        return 0
    except Exception as error:
        try:
            logger.record(severity="KRITISCH", area="START", summary="Das Programm konnte nicht gestartet oder sauber beendet werden.",
                          cause=str(error) or "Unbekannter Start- oder Laufzeitfehler",
                          protection="Der betroffene Ablauf wurde beendet; vorhandene Daten wurden nicht verändert.",
                          next_step="Prüfen Sie den Bericht im Ordner berichte und starten Sie danach erneut.", exception=error)
        except Exception:
            print(emergency_message(error))
        return 1


def cli() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--headless-check", action="store_true")
    args, _unknown = parser.parse_known_args()
    return headless_check() if args.headless_check else main()


if __name__ == "__main__":
    raise SystemExit(cli())
