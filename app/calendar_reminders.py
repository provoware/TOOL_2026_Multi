"""Gebundene Kalender-Erinnerungsprüfung während das Dashboard läuft."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QObject, QTimer

from app.calendar_store import due_reminders, mark_reminded


class CalendarReminderController(QObject):
    """Prüft höchstens alle 30 Sekunden und markiert erst nach angezeigter Erinnerung."""

    def __init__(self, project_root: Path, on_due: Callable[[dict[str, object]], None],
                 on_error: Callable[[Exception], None] | None = None,
                 parent: QObject | None = None, interval_ms: int = 30_000) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self.on_due = on_due
        self.on_error = on_error
        self._checking = False
        self.timer = QTimer(self)
        self.timer.setInterval(interval_ms)
        self.timer.timeout.connect(self.check_now)
        self.timer.start()

    def check_now(self, now: datetime | None = None) -> None:
        if self._checking:
            return
        self._checking = True
        try:
            for event in due_reminders(self.project_root, now):
                self.on_due(event)
                mark_reminded(self.project_root, str(event["id"]))
        except Exception as error:
            if self.on_error is not None:
                self.on_error(error)
        finally:
            self._checking = False

    def stop(self) -> None:
        self.timer.stop()
