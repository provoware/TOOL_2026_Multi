"""PySide6-Kalender mit Tages-, Wochen-, Monats- und Jahresansicht."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QDate, QDateTime, Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QCalendarWidget, QComboBox, QDateTimeEdit, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSplitter,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
)

from app.calendar_store import (
    REMINDER_OPTIONS, add_event, day_range, events_between, month_range, week_range,
    year_range,
)
from app.ui_standards import SPACING, apply_global_style

REMINDER_LABELS = {
    None: "Keine Erinnerung",
    0: "Zum Terminbeginn",
    5: "5 Minuten vorher",
    15: "15 Minuten vorher",
    30: "30 Minuten vorher",
    60: "1 Stunde vorher",
    1440: "1 Tag vorher",
}


class CalendarWindow(QWidget):
    def __init__(self, project_root: Path, zoom_percent: int = 100,
                 on_changed: Callable[[], None] | None = None,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self.zoom_percent = zoom_percent
        self.on_changed = on_changed
        self.setWindowTitle("Kalender & Termine")
        self.resize(1100, 720)
        self.setMinimumSize(860, 580)
        self._build()
        self.set_zoom(zoom_percent)
        self.refresh()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACING["m"], SPACING["m"], SPACING["m"], SPACING["m"])
        outer.setSpacing(SPACING["s"])

        heading = QHBoxLayout()
        title = QLabel("Kalender & Termine")
        title.setObjectName("sectionTitle")
        heading.addWidget(title)
        heading.addStretch(1)
        today = QPushButton("Heute anzeigen")
        today.setObjectName("calendarTodayButton")
        today.clicked.connect(self._select_today)
        heading.addWidget(today)
        refresh_button = QPushButton("Ansicht aktualisieren")
        refresh_button.setObjectName("calendarRefreshButton")
        refresh_button.clicked.connect(self.refresh)
        heading.addWidget(refresh_button)
        self.close_button = QPushButton("Kalender schließen")
        self.close_button.setObjectName("closeWindowButton")
        self.close_button.setToolTip("Schließt nur das Kalenderfenster. Das Dashboard bleibt geöffnet.")
        self.close_button.setAccessibleName("Kalenderfenster schließen")
        self.close_button.clicked.connect(self.close)
        heading.addWidget(self.close_button)
        outer.addLayout(heading)

        hint = QLabel(
            "Links Datum auswählen oder neuen Termin anlegen. Rechts zwischen Tag, Woche, Monat und Jahr wechseln. "
            "Erinnerungen funktionieren, solange das Hauptprogramm geöffnet ist."
        )
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        outer.addWidget(hint)

        splitter = QSplitter(Qt.Horizontal)
        left = QFrame()
        left.setObjectName("innerCard")
        left_layout = QVBoxLayout(left)
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.refresh)
        left_layout.addWidget(self.calendar)
        left_layout.addWidget(self._build_event_form())
        splitter.addWidget(left)

        right = QFrame()
        right.setObjectName("innerCard")
        right_layout = QVBoxLayout(right)
        self.range_label = QLabel("")
        self.range_label.setObjectName("cardTitle")
        right_layout.addWidget(self.range_label)
        self.tabs = QTabWidget()
        self.day_table = self._make_table(["Zeit", "Titel", "Notiz", "Erinnerung"])
        self.week_table = self._make_table(["Tag", "Zeit", "Titel", "Notiz"])
        self.month_table = self._make_table(["Datum", "Zeit", "Titel", "Notiz"])
        self.year_table = self._make_table(["Monat", "Datum", "Zeit", "Titel"])
        self.tabs.addTab(self.day_table, "Tag")
        self.tabs.addTab(self.week_table, "Woche")
        self.tabs.addTab(self.month_table, "Monat")
        self.tabs.addTab(self.year_table, "Jahr")
        self.tabs.currentChanged.connect(lambda _index: self._update_range_label())
        right_layout.addWidget(self.tabs, 1)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        outer.addWidget(splitter, 1)

        self.status_label = QLabel("Bereit · Datum wählen oder links einen Termin anlegen.")
        self.status_label.setObjectName("muted")
        outer.addWidget(self.status_label)

    def _build_event_form(self) -> QFrame:
        frame = QFrame()
        form = QFormLayout(frame)
        form.setContentsMargins(0, SPACING["s"], 0, 0)

        form_title = QLabel("Neuen Termin anlegen")
        form_title.setObjectName("cardTitle")
        form.addRow(form_title)

        self.title_entry = QLineEdit()
        self.title_entry.setPlaceholderText("Worum geht es?")
        form.addRow("Titel", self.title_entry)

        self.note_entry = QTextEdit()
        self.note_entry.setPlaceholderText("Zusätzliche Notiz (optional) …")
        self.note_entry.setFixedHeight(65)
        form.addRow("Notiz", self.note_entry)

        now = QDateTime.currentDateTime()
        rounded = QDateTime(now.date(), now.time())
        self.start_edit = QDateTimeEdit(rounded)
        self.start_edit.setCalendarPopup(True)
        self.start_edit.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.end_edit = QDateTimeEdit(rounded.addSecs(3600))
        self.end_edit.setCalendarPopup(True)
        self.end_edit.setDisplayFormat("dd.MM.yyyy HH:mm")
        form.addRow("Beginn", self.start_edit)
        form.addRow("Ende", self.end_edit)

        self.reminder_combo = QComboBox()
        for minutes in REMINDER_OPTIONS:
            self.reminder_combo.addItem(REMINDER_LABELS[minutes], minutes)
        self.reminder_combo.setCurrentIndex(0)
        self.reminder_combo.setToolTip("Erinnerungen erscheinen nur, solange das Hauptprogramm läuft.")
        form.addRow("Erinnerung", self.reminder_combo)

        add_button = QPushButton("Termin anlegen")
        add_button.setObjectName("primaryButton")
        add_button.clicked.connect(self.add_current_event)
        form.addRow("", add_button)
        self.title_entry.returnPressed.connect(self.add_current_event)
        return frame

    @staticmethod
    def _make_table(headers: list[str]) -> QTableWidget:
        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setStretchLastSection(True)
        return table

    def _select_today(self) -> None:
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)
        self.calendar.showSelectedDate()
        self.refresh()
        self.status_label.setText("Heute ausgewählt.")

    def selected_date(self) -> date:
        selected = self.calendar.selectedDate()
        return date(selected.year(), selected.month(), selected.day())

    @staticmethod
    def _event_datetimes(event: dict[str, object]) -> tuple[datetime, datetime]:
        return datetime.fromisoformat(str(event["start"])), datetime.fromisoformat(str(event["end"]))

    @staticmethod
    def _time_span(event: dict[str, object]) -> str:
        start, end = CalendarWindow._event_datetimes(event)
        if start.date() == end.date():
            return f"{start:%H:%M}–{end:%H:%M}"
        return f"{start:%d.%m. %H:%M} – {end:%d.%m. %H:%M}"

    @staticmethod
    def _reminder_text(event: dict[str, object]) -> str:
        return REMINDER_LABELS.get(event.get("reminder_minutes"), "—")

    @staticmethod
    def _fill_table(table: QTableWidget, rows: list[list[str]]) -> None:
        table.setRowCount(len(rows))
        for row_index, values in enumerate(rows):
            for column, value in enumerate(values):
                table.setItem(row_index, column, QTableWidgetItem(value))
        table.resizeColumnsToContents()

    def add_current_event(self) -> None:
        start = self.start_edit.dateTime().toPython().replace(second=0, microsecond=0)
        end = self.end_edit.dateTime().toPython().replace(second=0, microsecond=0)
        reminder = self.reminder_combo.currentData()
        try:
            add_event(
                self.project_root, self.title_entry.text(),
                start.isoformat(timespec="minutes"), end.isoformat(timespec="minutes"),
                self.note_entry.toPlainText(), reminder,
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Termin nicht gespeichert",
                f"Es wurde kein unvollständiger Termin angelegt.\n\nGrund: {error}",
            )
            return
        self.calendar.setSelectedDate(QDate(start.year, start.month, start.day))
        self.title_entry.clear()
        self.note_entry.clear()
        self.refresh()
        self.status_label.setText("Termin gespeichert · er erscheint jetzt in den passenden Ansichten.")
        if self.on_changed:
            self.on_changed()
        self.title_entry.setFocus()

    def refresh(self) -> None:
        selected = self.selected_date()
        try:
            day_start, day_end = day_range(selected)
            week_start, week_end = week_range(selected)
            month_start, month_end = month_range(selected)
            year_start, year_end = year_range(selected)
            day_events = events_between(self.project_root, day_start, day_end)
            week_events = events_between(self.project_root, week_start, week_end)
            month_events = events_between(self.project_root, month_start, month_end)
            year_events = events_between(self.project_root, year_start, year_end)
        except Exception as error:
            QMessageBox.critical(
                self,
                "Kalender nicht lesbar",
                f"Es wurden keine Kalenderdaten verändert.\n\nGrund: {error}",
            )
            return

        self._fill_table(self.day_table, [
            [self._time_span(event), str(event["title"]), str(event["note"]), self._reminder_text(event)]
            for event in day_events
        ])
        self._fill_table(self.week_table, [
            [self._event_datetimes(event)[0].strftime("%a %d.%m."), self._time_span(event), str(event["title"]), str(event["note"])]
            for event in week_events
        ])
        self._fill_table(self.month_table, [
            [self._event_datetimes(event)[0].strftime("%d.%m.%Y"), self._time_span(event), str(event["title"]), str(event["note"])]
            for event in month_events
        ])
        self._fill_table(self.year_table, [
            [self._event_datetimes(event)[0].strftime("%B"), self._event_datetimes(event)[0].strftime("%d.%m.%Y"), self._time_span(event), str(event["title"])]
            for event in year_events
        ])
        self.tabs.setTabText(0, f"Tag ({len(day_events)})")
        self.tabs.setTabText(1, f"Woche ({len(week_events)})")
        self.tabs.setTabText(2, f"Monat ({len(month_events)})")
        self.tabs.setTabText(3, f"Jahr ({len(year_events)})")
        self._update_range_label()

    def _update_range_label(self) -> None:
        selected = self.selected_date()
        index = self.tabs.currentIndex()
        if index == 0:
            text = selected.strftime("Tag · %d.%m.%Y")
        elif index == 1:
            start, end = week_range(selected)
            text = f"Woche · {start:%d.%m.%Y} – {(end - timedelta(days=1)):%d.%m.%Y}"
        elif index == 2:
            text = selected.strftime("Monat · %m/%Y")
        else:
            text = selected.strftime("Jahr · %Y")
        self.range_label.setText(text)

    def set_zoom(self, percent: int) -> None:
        self.zoom_percent = percent
        apply_global_style(self, percent)
