"""PySide6-Todo-Modul mit Terminierung, Abhaken und getrenntem Archiv."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QDateTime, Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QCheckBox, QDateTimeEdit, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QPushButton, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
)

from app.todo_store import active_tasks, add_task, archived_tasks, complete_task
from app.ui_standards import SPACING, apply_global_style


class TodoWindow(QWidget):
    def __init__(self, project_root: Path, zoom_percent: int = 100,
                 on_changed: Callable[[], None] | None = None,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self.zoom_percent = zoom_percent
        self.on_changed = on_changed
        self.setWindowTitle("Todo-Liste")
        self.resize(900, 650)
        self.setMinimumSize(760, 520)
        self._build()
        self.set_zoom(zoom_percent)
        self.refresh()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACING["m"], SPACING["m"], SPACING["m"], SPACING["m"])
        outer.setSpacing(SPACING["s"])

        title = QLabel("Todo-Liste")
        title.setObjectName("sectionTitle")
        outer.addWidget(title)
        hint = QLabel("Neue Aufgabe anlegen, optional terminieren und nach Erledigung sicher ins Archiv verschieben.")
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        outer.addWidget(hint)

        form_frame = QFrame()
        form_frame.setObjectName("innerCard")
        form = QFormLayout(form_frame)
        self.title_entry = QLineEdit()
        self.title_entry.setPlaceholderText("Was ist zu erledigen?")
        form.addRow("Titel", self.title_entry)
        self.note_entry = QTextEdit()
        self.note_entry.setPlaceholderText("Optionale Notiz …")
        self.note_entry.setFixedHeight(75)
        form.addRow("Notiz", self.note_entry)

        due_row = QHBoxLayout()
        self.use_due = QCheckBox("Termin verwenden")
        due_row.addWidget(self.use_due)
        self.due_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.due_edit.setCalendarPopup(True)
        self.due_edit.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.due_edit.setEnabled(False)
        self.use_due.toggled.connect(self.due_edit.setEnabled)
        due_row.addWidget(self.due_edit, 1)
        form.addRow("Termin", due_row)

        add_row = QHBoxLayout()
        add_row.addStretch(1)
        add_button = QPushButton("Aufgabe anlegen")
        add_button.clicked.connect(self.add_current_task)
        add_row.addWidget(add_button)
        form.addRow("", add_row)
        outer.addWidget(form_frame)

        self.tabs = QTabWidget()
        self.active_table = self._make_table(["Titel", "Termin", "Notiz"])
        self.archive_table = self._make_table(["Titel", "Termin", "Erledigt", "Notiz"])
        self.tabs.addTab(self.active_table, "Aktiv")
        self.tabs.addTab(self.archive_table, "Archiv")
        outer.addWidget(self.tabs, 1)

        buttons = QHBoxLayout()
        self.status_label = QLabel("Bereit.")
        self.status_label.setObjectName("muted")
        buttons.addWidget(self.status_label, 1)
        refresh = QPushButton("Aktualisieren")
        refresh.clicked.connect(self.refresh)
        buttons.addWidget(refresh)
        done = QPushButton("Ausgewählte Aufgabe abhaken")
        done.clicked.connect(self.complete_selected)
        buttons.addWidget(done)
        outer.addLayout(buttons)

        self.title_entry.returnPressed.connect(self.add_current_task)

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

    @staticmethod
    def _format_due(value: object) -> str:
        if not value:
            return "—"
        try:
            return datetime.fromisoformat(str(value)).strftime("%d.%m.%Y %H:%M")
        except ValueError:
            return str(value)

    @staticmethod
    def _format_completed(value: object) -> str:
        if not value:
            return "—"
        try:
            return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone().strftime("%d.%m.%Y %H:%M")
        except ValueError:
            return str(value)

    def add_current_task(self) -> None:
        due = None
        if self.use_due.isChecked():
            due = self.due_edit.dateTime().toPython().replace(second=0, microsecond=0).isoformat(timespec="minutes")
        try:
            add_task(self.project_root, self.title_entry.text(), self.note_entry.toPlainText(), due)
        except Exception as error:
            QMessageBox.critical(self, "Aufgabe nicht gespeichert", str(error))
            return
        self.title_entry.clear()
        self.note_entry.clear()
        self.use_due.setChecked(False)
        self.status_label.setText("Aufgabe gespeichert.")
        self.refresh()
        if self.on_changed:
            self.on_changed()
        self.title_entry.setFocus()

    def _fill_active(self) -> None:
        tasks = active_tasks(self.project_root)
        self.active_table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            values = [str(task["title"]), self._format_due(task["due"]), str(task["note"])]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column == 0:
                    item.setData(Qt.UserRole, str(task["id"]))
                self.active_table.setItem(row, column, item)
        self.tabs.setTabText(0, f"Aktiv ({len(tasks)})")

    def _fill_archive(self) -> None:
        tasks = archived_tasks(self.project_root)
        self.archive_table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            values = [
                str(task["title"]), self._format_due(task["due"]),
                self._format_completed(task["completed_at"]), str(task["note"]),
            ]
            for column, value in enumerate(values):
                self.archive_table.setItem(row, column, QTableWidgetItem(value))
        self.tabs.setTabText(1, f"Archiv ({len(tasks)})")

    def refresh(self) -> None:
        try:
            self._fill_active()
            self._fill_archive()
        except Exception as error:
            QMessageBox.critical(self, "Todo-Daten nicht lesbar", str(error))
            return
        self.active_table.resizeColumnsToContents()
        self.archive_table.resizeColumnsToContents()

    def complete_selected(self) -> None:
        row = self.active_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Keine Aufgabe gewählt", "Bitte zuerst eine aktive Aufgabe auswählen.")
            return
        item = self.active_table.item(row, 0)
        task_id = item.data(Qt.UserRole) if item else None
        if not task_id:
            QMessageBox.critical(self, "Aufgabe nicht gefunden", "Die ausgewählte Aufgabe besitzt keine gültige Kennung.")
            return
        try:
            complete_task(self.project_root, str(task_id))
        except Exception as error:
            QMessageBox.critical(self, "Abhaken fehlgeschlagen", str(error))
            return
        self.status_label.setText("Aufgabe erledigt und ins Archiv verschoben.")
        self.refresh()
        if self.on_changed:
            self.on_changed()

    def set_zoom(self, percent: int) -> None:
        self.zoom_percent = percent
        apply_global_style(self, percent)
