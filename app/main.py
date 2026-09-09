"""Sicherer PySide6-Programmeinstieg mit prüfbarem Headless-Modus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.event_log import EventLogger, emergency_message
from app.process_guard import CONTROLLED_ALREADY_RUNNING_EXIT, acquire_instance_guard
from app.texts import TextRegistry

ROOT = Path(__file__).resolve().parent.parent


def headless_check() -> int:
    try:
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        version = manifest["tool"]["version"]
        TextRegistry(ROOT / "texte" / "registry.json").get("app.name", "TOOL_2026_Multi")
        if not version or not (ROOT / manifest["runtime"]["entrypoint"]).is_file():
            raise ValueError("Manifest enthält keinen gültigen Programmeinstieg.")
        return 0
    except Exception as error:
        print(f"HEADLESS-START-FEHLER: {type(error).__name__}: {error}")
        return 1


def main() -> int:
    version = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))["tool"]["version"]
    guard = None
    logger = None
    try:
        from PySide6.QtWidgets import QApplication
        from app.ui import Dashboard, install_exception_handler
        from app.ui_standards import configure_application

        app = QApplication.instance() or QApplication([])
        app.setApplicationName("Provoware-Datenbank-Dashboard 2026")
        configure_application(app)

        guard = acquire_instance_guard(ROOT)
        if guard is None:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(
                None,
                "Provoware ist schon geöffnet",
                "Dieses Projekt ist bereits in einem Provoware-Fenster geöffnet.\n\n"
                "Zum Schutz deiner Daten wird kein zweites Fenster gestartet. Das bereits geöffnete Fenster läuft normal weiter.",
            )
            return CONTROLLED_ALREADY_RUNNING_EXIT

        logger = EventLogger(ROOT, version)
        dashboard = Dashboard(TextRegistry(ROOT / "texte" / "registry.json"), logger, ROOT)
        install_exception_handler(app, logger, dashboard.refresh, dashboard)
        logger.record(
            severity="INFO", area="START", summary="Das Programm wurde sicher gestartet.",
            cause="Normaler Programmstart", protection="Der Schutz vor einem versehentlichen Doppelstart ist aktiv.",
            next_step="Starte im Dashboard mit Songtexte, Todo-Liste oder Kalender.",
        )
        dashboard.show()
        dashboard.refresh()
        code = app.exec()
        logger.record(
            severity="INFO", area="ENDE", summary="Das Programm wurde kontrolliert beendet.",
            cause="Normales Schließen der Anwendung",
            protection="Offene Songtexte wurden vor dem Beenden gespeichert.",
            next_step="Keine weitere Aktion nötig.",
        )
        return int(code)
    except Exception as error:
        if logger is not None:
            try:
                logger.record(
                    severity="KRITISCH", area="START",
                    summary="Das Programm konnte nicht vollständig gestartet oder beendet werden.",
                    cause=str(error) or "Unbekannter Start- oder Laufzeitfehler",
                    protection="Der betroffene Ablauf wurde beendet; vorhandene Daten wurden nicht absichtlich verändert.",
                    next_step="Öffne nach dem nächsten Start die Fehlerhilfe (Recovery). Falls das nicht möglich ist, prüfe den Ordner berichte.",
                    exception=error,
                )
            except Exception:
                print(emergency_message(error))
        else:
            print(emergency_message(error))
        return 1
    finally:
        if guard is not None:
            guard.release()


def cli() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--headless-check", action="store_true")
    args, _ = parser.parse_known_args()
    return headless_check() if args.headless_check else main()


if __name__ == "__main__":
    raise SystemExit(cli())
