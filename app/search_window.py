"""Abbrechbare Dateinamen-/Textsuche mit rein lesender Trefferanzeige."""
import os
from pathlib import Path
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView, QCheckBox, QHBoxLayout, QLabel, QLineEdit,
    QFileDialog, QMessageBox, QProgressBar, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
)
from app.data_search import DataSearch
from app.module_widgets import t
from app.ui_standards import apply_global_style
from app.window_state import ensure_window_visible


class SearchWindow(QWidget):
    def __init__(self, root, zoom_percent=100, parent=None):
        super().__init__(parent, Qt.Window)
        self.root, self.zoom_percent = Path(root), zoom_percent
        self.session = self.iterator = None
        self.setWindowTitle(t('search_title', 'Dateien & Texte suchen'))
        self.resize(960, 680)
        self.setMinimumSize(600, 430)
        box = QVBoxLayout(self)
        hint = QLabel(t('search_hint', 'Wähle einen lokalen Ordner. Suche einschließlich Unterordnern; versteckte Einträge und Verknüpfungen bleiben außen vor. Dateien werden nur gelesen.'))
        hint.setWordWrap(True)
        box.addWidget(hint)
        self.default_path = (self.root / 'daten').absolute()
        self.approved_path = None
        path_row = QHBoxLayout()
        path_label = QLabel(t('search_folder', 'Suchordner:'))
        self.path_entry = QLineEdit(str(self.default_path))
        self.path_entry.setAccessibleName(t('search_folder', 'Suchordner:'))
        path_label.setBuddy(self.path_entry)
        self.path_entry.textChanged.connect(self._forget_approval)
        self.folder_button = QPushButton(t('search_choose_folder', 'Ordner auswählen …'))
        self.folder_button.clicked.connect(self.choose_folder)
        path_row.addWidget(path_label)
        path_row.addWidget(self.path_entry, 1)
        path_row.addWidget(self.folder_button)
        box.addLayout(path_row)
        self.query = QLineEdit()
        self.query.setMaxLength(200)
        self.query.setPlaceholderText(t('search_query', 'Suchtext eingeben …'))
        self.query.setAccessibleName(t('search_query', 'Suchtext eingeben …'))
        self.query.returnPressed.connect(self.start)
        box.addWidget(self.query)
        options = QHBoxLayout()
        self.names = QCheckBox(t('search_names', 'Dateinamen'))
        self.contents = QCheckBox(t('search_contents', 'Textinhalte'))
        for option in (self.names, self.contents):
            option.setChecked(True)
            options.addWidget(option)
        self.start_button = QPushButton(t('search_start', 'Suchen'))
        self.start_button.clicked.connect(self.start)
        options.addWidget(self.start_button)
        self.stop_button = QPushButton(t('search_stop', 'Abbrechen'))
        self.stop_button.clicked.connect(self.cancel)
        options.addWidget(self.stop_button)
        box.addLayout(options)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        box.addWidget(self.progress)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels([t('search_file', 'Datei'), t('search_line', 'Zeile'), t('search_excerpt', 'Textausschnitt')])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAccessibleName(t('search_results', 'Gefundene Dateien und Textstellen'))
        self.table.itemSelectionChanged.connect(self.preview_selection)
        box.addWidget(self.table, 2)
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setAccessibleName(t('search_preview', 'Ausgewählte Fundstelle'))
        box.addWidget(self.preview, 1)
        self.status = QLabel(t('search_ready', 'Suchtext eingeben und Suchen wählen.'))
        self.status.setWordWrap(True)
        self.status.setTextFormat(Qt.PlainText)
        box.addWidget(self.status)
        self.timer = QTimer(self)
        self.timer.setInterval(0)
        self.timer.timeout.connect(self._advance)
        QShortcut(QKeySequence('Escape'), self, activated=self.cancel)
        self.set_zoom(zoom_percent)
        self._busy(False)

    def _busy(self, busy):
        self.start_button.setEnabled(not busy)
        self.stop_button.setEnabled(busy)
        self.progress.setVisible(busy)
        for field in (self.query, self.names, self.contents, self.path_entry, self.folder_button):
            field.setEnabled(not busy)

    def _forget_approval(self):
        self.approved_path = None

    def choose_folder(self):
        selected = QFileDialog.getExistingDirectory(
            self, t('search_choose_folder', 'Ordner auswählen …'), self.path_entry.text())
        if selected:
            self.path_entry.setText(selected)

    def _ask_access(self, title, message):
        dialog = QMessageBox(QMessageBox.Question, title, message,
                             QMessageBox.Yes | QMessageBox.No, self)
        dialog.setTextFormat(Qt.PlainText)
        dialog.setDefaultButton(QMessageBox.No)
        return dialog.exec()

    def _authorize_path(self, folder):
        if folder == self.default_path or folder == self.approved_path:
            return True
        message = t('search_consent',
            'Diesen Ordner und seine Unterordner nach Dateinamen und Textinhalten durchsuchen?\n\n'
            '{path}\n\nDateien werden nur gelesen. Die Freigabe gilt für diesen Suchordner, '
            'solange er in diesem Fenster unverändert bleibt. Betriebssystemrechte werden dadurch nicht geändert.')
        answer = self._ask_access(t('search_access_title', 'Ordnerzugriff bestätigen'),
                                  message.format(path=str(folder)))
        if answer != QMessageBox.Yes:
            self.status.setText(t('search_consent_declined', 'Ordnerzugriff nicht bestätigt. Bisherige Treffer bleiben erhalten.'))
            return False
        self.approved_path = folder
        return True

    def start(self):
        self.cancel()
        try:
            raw_path = self.path_entry.text().strip()
            if not raw_path:
                raise ValueError(t('search_folder_required', 'Bitte einen Suchordner auswählen oder einen absoluten Pfad eingeben.'))
            folder = Path(raw_path).expanduser()
            if not folder.is_absolute():
                raise ValueError(t('search_folder_required', 'Bitte einen Suchordner auswählen oder einen absoluten Pfad eingeben.'))
            folder = Path(os.path.abspath(folder))
            session = DataSearch(self.root, self.query.text(), names=self.names.isChecked(),
                                 contents=self.contents.isChecked(), search_path=folder)
            if not self._authorize_path(folder):
                return
            self.session = session
        except ValueError as error:
            self.status.setText(str(error))
            return
        self.table.setRowCount(0)
        self.preview.clear()
        self.iterator = iter(self.session.batches())
        self._busy(True)
        self.status.setText(t('search_running', 'Suche läuft … Abbrechen ist jederzeit möglich.'))
        self.timer.start()

    def _advance(self):
        try:
            for hit in next(self.iterator):
                row = self.table.rowCount()
                self.table.insertRow(row)
                for column, value in enumerate((hit['path'], hit['line'] or '', hit['excerpt'])):
                    self.table.setItem(row, column, QTableWidgetItem(str(value)))
        except StopIteration:
            self._finish(self.session.result.reason)
        except PermissionError:
            self.session.record_denied(self.session.data)
            self._finish('permission')
        except (OSError, ValueError):
            self._finish('error')

    def _finish(self, reason):
        self.timer.stop()
        if self.iterator is not None:
            self.iterator.close()
            self.iterator = None
        self._busy(False)
        count = len(self.session.result.hits) if self.session else 0
        skipped = self.session.result.skipped if self.session else 0
        label = t('search_state_' + reason, reason)
        denied = self.session.result.denied if self.session else 0
        self.status.setText(t('search_summary', '{state} · {count} Treffer · {skipped} Dateien/Ordner ausgelassen.').format(state=label, count=count, skipped=skipped)
            + t('search_root_summary', '\nSuchordner: {path} · Fehlende Leseberechtigungen: {denied}').format(
                path=str(self.session.data), denied=denied))
        self.table.setColumnWidth(0, 280)
        self.table.setColumnWidth(1, 70)
        if denied and reason != 'cancelled':
            self._request_folder_access()

    def _request_folder_access(self):
        self.approved_path = None
        message = t('search_permission_request',
            'Einige Bereiche sind nicht lesbar:\n{paths}\n\n'
            'Möchtest du die Betriebssystem-Ordnerauswahl zur Freigabe oder Auswahl eines anderen Ordners öffnen? '
            'Linux-Dateirechte müssen gegebenenfalls von einer berechtigten Person geändert werden. '
            'Provoware erhält durch diese Bestätigung keine Administratorrechte. '
            'Bisherige Treffer bleiben erhalten; eine neue Suche musst du ausdrücklich starten.')
        answer = self._ask_access(t('search_permission_title', 'Leseberechtigung erforderlich'),
                                 message.format(paths='\n'.join(self.session.result.denied_paths)))
        if answer == QMessageBox.Yes:
            self.choose_folder()

    def cancel(self):
        if self.iterator is not None:
            self._finish('cancelled')

    def preview_selection(self):
        row = self.table.currentRow()
        if row >= 0 and self.table.item(row, 0) is not None:
            self.preview.setPlainText('\n'.join(self.table.item(row, column).text() for column in range(3)))

    def refresh(self):
        # Treffer bleiben erhalten; ein Dashboard-Refresh löst keinen neuen Scan aus.
        pass

    def set_zoom(self, percent):
        self.zoom_percent = percent
        apply_global_style(self, percent)
        self.ensure_on_screen()

    def ensure_on_screen(self):
        ensure_window_visible(self, QSize(600, 430))

    def closeEvent(self, event):
        self.cancel()
        super().closeEvent(event)
