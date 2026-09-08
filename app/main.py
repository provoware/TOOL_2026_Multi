"""Sicherer Programmeinstieg."""

from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk

from app.event_log import EventLogger, emergency_message
from app.texts import TextRegistry
from app.ui import Dashboard, install_exception_handler


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    version = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))["tool"]["version"]
    logger = EventLogger(ROOT, version)
    try:
        root = tk.Tk()
        dashboard = Dashboard(root, TextRegistry(ROOT / "texte" / "registry.json"), logger)
        install_exception_handler(root, logger, dashboard.refresh)
        logger.record(severity="INFO", area="START", summary="Das Programm wurde sicher gestartet.",
                      cause="Normaler Programmstart", protection="Es waren keine Schutzmaßnahmen nötig.",
                      next_step="Sie können das Werkzeug jetzt verwenden.")
        dashboard.refresh()
        root.mainloop()
        return 0
    except Exception as error:
        try:
            logger.record(severity="KRITISCH", area="START", summary="Das Programm konnte nicht gestartet werden.",
                          cause=str(error) or "Unbekannter Startfehler",
                          protection="Der Start wurde beendet; vorhandene Daten wurden nicht verändert.",
                          next_step="Prüfen Sie den Bericht im Ordner berichte und starten Sie danach erneut.", exception=error)
        except Exception:
            print(emergency_message(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
