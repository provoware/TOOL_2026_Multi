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

from app.todo_store import add_task, complete_task, task_groups
from app.module_widgets import t
from app.ui_standards import SPACING, apply_global_style


class TodoWindow(QWidget):
    def __init__(self, project_root: Path, zoom_percent: int = 100,
                 on_changed: Callable[[], None] | None = None,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self.zoom_percent = zoom_percent
        self.on_changed = on_changed
        self.error_logger = getattr(parent, "logger", None)
        self.setWindowTitle("Aufgaben · Todo-Liste")
        self.resize(900, 650)
        self.setMinimumSize(760, 520)
        self._build()
        self.set_zoom(zoom_percent)
        self.refresh()
        self.title_entry.setFocus()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACING["m"], SPACING["m"], SPACING["m"], SPACING["m"])
        outer.setSpacing(SPACING["s"])

        title = QLabel("Aufgaben (Todo-Liste)")
        title.setObjectName("sectionTitle")
        outer.addWidget(title)
        hint = QLabel("1. Aufgabe eingeben  →  2. optional Termin einschalten  →  3. Aufgabe anlegen. Erledigte Aufgaben bleiben im Archiv erhalten.")
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        outer.addWidget(hint)

        form_frame = QFrame()
        form_frame.setObjectName("innerCard")
        form = QFormLayout(form_frame)
        self.title_entry = QLineEdit()
        self.title_entry.setPlaceholderText("Was ist zu erledigen?")
        form.addRow("Aufgabe", self.title_entry)
        self.note_entry = QTextEdit()
        self.note_entry.setPlaceholderText("Zusätzliche Notiz (optional) …")
        self.note_entry.setFixedHeight(75)
        form.addRow("Notiz", self.note_entry)

        due_row = QHBoxLayout()
        self.use_due = QCheckBox("Termin hinzufügen")
        due_row.addWidget(self.use_due)
        self.due_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.due_edit.setCalendarPopup(True)
        self.due_edit.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.due_edit.setEnabled(False)
        self.use_due.toggled.connect(self.due_edit.setEnabled)
        due_row.addWidget(self.due_edit, 1)
        form.addRow("Fällig am", due_row)

        add_row = QHBoxLayout()
        add_row.addStretch(1)
        add_button = QPushButton("Aufgabe anlegen")
        add_button.setObjectName("primaryButton")
        add_button.clicked.connect(self.add_current_task)
        add_row.addWidget(add_button)
        form.addRow("", add_row)
        outer.addWidget(form_frame)

        outer.addWidget(self._build_task_tabs(), 1)

        buttons = QHBoxLayout()
        self.status_label = QLabel("Bereit · Aufgabe eingeben oder eine aktive Aufgabe auswählen.")
        self.status_label.setObjectName("muted")
        buttons.addWidget(self.status_label, 1)
        refresh = QPushButton("Liste aktualisieren")
        refresh.clicked.connect(self.refresh)
        buttons.addWidget(refresh)
        done = QPushButton("Als erledigt markieren → Archiv")
        done.setToolTip("Die Aufgabe wird nicht gelöscht, sondern vollständig ins Archiv verschoben.")
        self.done_button = done
        self.tabs.currentChanged.connect(self._update_done_button)
        done.clicked.connect(self.complete_selected)
        buttons.addWidget(done)
        outer.addLayout(buttons)

        self.title_entry.returnPressed.connect(self.add_current_task)

    def _build_task_tabs(self):
        self.tabs = QTabWidget()
        self.active_table = self._make_table(["Aufgabe", "Termin", "Notiz"])
        self.archive_table = self._make_table(["Aufgabe", "Termin", "Erledigt", "Notiz"])
        self.tabs.addTab(self.active_table, "Aktiv")
        self.tabs.addTab(self.archive_table, "Archiv")
        self.development_panel = QWidget(self.tabs)
        self.development_panel.hide()
        legacy_box = QVBoxLayout(self.development_panel)
        legacy_hint = QLabel(t('todo_legacy_hint',
            'Früher automatisch eingetragene Entwicklungsaufgaben. Sie bleiben unverändert erhalten '
            'und zählen nicht zu deinen persönlichen Aufgaben. Bei Bedarf eine persönliche Kopie anlegen.'))
        legacy_hint.setWordWrap(True)
        legacy_box.addWidget(legacy_hint)
        self.development_table = self._make_table([
            t('todo_legacy_task', 'Entwicklungsaufgabe'), t('todo_legacy_status', 'Stand'),
            t('todo_legacy_due', 'Termin'), t('todo_legacy_note', 'Notiz')])
        self.development_table.setAccessibleName(t('todo_legacy_accessible', 'Erhaltene Entwicklungsaufgaben aus älteren Versionen'))
        legacy_box.addWidget(self.development_table, 1)
        self.copy_legacy_button = QPushButton(t('todo_copy_personal', 'Als persönliche Aufgabe kopieren'))
        self.copy_legacy_button.clicked.connect(self.copy_legacy_task)
        legacy_box.addWidget(self.copy_legacy_button)
        return self.tabs

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
            QMessageBox.critical(
                self, "Aufgabe nicht gespeichert",
                f"Es wurde keine unvollständige Aufgabe angelegt.\n\nGrund: {error}",
            )
            return
        self.title_entry.clear()
        self.note_entry.clear()
        self.use_due.setChecked(False)
        self.refresh()
        self.status_label.setText("Aufgabe gespeichert · sie steht jetzt unter „Aktiv“.")
        if self.on_changed:
            self.on_changed()
        self.title_entry.setFocus()

    def _fill_active(self, tasks) -> None:
        self.active_table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            values = [str(task["title"]), self._format_due(task["due"]), str(task["note"])]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column == 0:
                    item.setData(Qt.UserRole, str(task["id"]))
                self.active_table.setItem(row, column, item)
        self.tabs.setTabText(0, f"Aktiv ({len(tasks)})")

    def _fill_archive(self, tasks) -> None:
        self.archive_table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            values = [
                str(task["title"]), self._format_due(task["due"]),
                self._format_completed(task["completed_at"]), str(task["note"]),
            ]
            for column, value in enumerate(values):
                self.archive_table.setItem(row, column, QTableWidgetItem(value))
        self.tabs.setTabText(1, f"Archiv ({len(tasks)})")

    def _fill_development(self, tasks) -> None:
        index = self.tabs.indexOf(self.development_panel)
        if tasks and index < 0:
            index = self.tabs.addTab(self.development_panel, '')
        elif not tasks and index >= 0:
            self.tabs.removeTab(index)
        if tasks:
            self.tabs.setTabText(index, t('todo_legacy_tab', 'Entwicklungsplanung (Altbestand)') + f' ({len(tasks)})')
        self.development_table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            status = t('todo_legacy_done', 'Erledigt') if task['completed_at'] else t('todo_legacy_active', 'Offen')
            values = [str(task['title']), status, self._format_due(task['due']), str(task['note'])]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column == 0:
                    item.setData(Qt.UserRole, task)
                self.development_table.setItem(row, column, item)
        self.development_table.resizeColumnsToContents()
        self._update_done_button()

    def _update_done_button(self, _index=None) -> None:
        self.done_button.setEnabled(self.tabs.currentWidget() is self.active_table)

    def _report_copy_error(self, error):
        record = getattr(self.error_logger, 'record', None)
        if callable(record):
            try:
                record(severity='ERROR', area='AUFGABEN_KOPIE',
                       summary=t('todo_copy_failed', 'Persönliche Kopie nicht gespeichert'),
                       cause=str(error),
                       protection=t('todo_copy_protection', 'Der gespeicherte Aufgabenbestand wurde nicht verworfen.'),
                       next_step=t('todo_copy_next', 'Schreibrechte und freien Speicher prüfen. Details stehen unter F1 in der Fehlerhilfe.'),
                       exception=error)
            except Exception:
                pass  # Ein Diagnosefehler darf keinen weiteren Speicherversuch auslösen.
        QMessageBox.critical(self, t('todo_copy_failed', 'Persönliche Kopie nicht gespeichert'),
                             t('todo_copy_error', 'Der Altbestand bleibt erhalten.\n\nGrund: {error}').format(error=error))

    def copy_legacy_task(self) -> None:
        if self.tabs.currentWidget() is not self.development_panel:
            return
        row = self.development_table.currentRow()
        item = self.development_table.item(row, 0) if row >= 0 else None
        if item is None:
            QMessageBox.information(self, t('todo_select_legacy_title', 'Entwicklungsaufgabe auswählen'),
                                    t('todo_select_legacy', 'Bitte zuerst eine Entwicklungsaufgabe markieren.'))
            return
        task = item.data(Qt.UserRole)
        dialog = QMessageBox(self)
        dialog.setWindowTitle(t('todo_copy_title', 'Persönliche Kopie anlegen?'))
        dialog.setTextFormat(Qt.PlainText)
        dialog.setText(t('todo_copy_confirm',
            'Diesen Eintrag als neue persönliche Aufgabe anlegen?\n\n{title}\n\n'
            'Die Kopie erscheint unter Aktiv. Der Altbestand bleibt erhalten. Wiederholtes Kopieren erzeugt weitere Aufgaben.').format(title=task['title']))
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.button(QMessageBox.Yes).setText(t('todo_copy_apply', 'Persönliche Kopie anlegen'))
        dialog.button(QMessageBox.No).setText(t('todo_copy_cancel', 'Abbrechen'))
        dialog.setDefaultButton(QMessageBox.No)
        if dialog.exec() != QMessageBox.Yes:
            return
        try:
            copied = add_task(self.project_root, task['title'], task['note'], task['due'])
        except Exception as error:
            self._report_copy_error(error)
            return
        self.refresh()
        self.tabs.setCurrentWidget(self.active_table)
        for row in range(self.active_table.rowCount()):
            if self.active_table.item(row, 0).data(Qt.UserRole) == copied['id']:
                self.active_table.selectRow(row)
                break
        self.status_label.setText(t('todo_copy_saved', 'Persönliche Kopie unter „Aktiv“ angelegt.'))
        if self.on_changed:
            self.on_changed()

    def refresh(self) -> None:
        try:
            groups = task_groups(self.project_root)
            self._fill_active(groups["active"])
            self._fill_archive(groups["archive"])
            self._fill_development(groups["development"])
        except Exception as error:
            QMessageBox.critical(
                self, "Aufgaben nicht lesbar",
                f"Es wurden keine Daten verändert.\n\nGrund: {error}",
            )
            return
        self.active_table.resizeColumnsToContents()
        self.archive_table.resizeColumnsToContents()

    def complete_selected(self) -> None:
        if self.tabs.currentWidget() is not self.active_table:
            return
        row = self.active_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Keine Aufgabe ausgewählt", "Bitte zuerst unter „Aktiv“ eine Aufgabe markieren.")
            return
        item = self.active_table.item(row, 0)
        task_id = item.data(Qt.UserRole) if item else None
        if not task_id:
            QMessageBox.critical(self, "Aufgabe nicht gefunden", "Die ausgewählte Aufgabe kann nicht eindeutig zugeordnet werden. Es wurde nichts verändert.")
            return
        try:
            complete_task(self.project_root, str(task_id))
        except Exception as error:
            QMessageBox.critical(
                self, "Aufgabe nicht verschoben",
                f"Die Aufgabe bleibt unter „Aktiv“.\n\nGrund: {error}",
            )
            return
        self.refresh()
        self.status_label.setText("Aufgabe erledigt · vollständig ins Archiv verschoben, nicht gelöscht.")
        if self.on_changed:
            self.on_changed()

    def set_zoom(self, percent: int) -> None:
        self.zoom_percent = percent
        apply_global_style(self, percent)
