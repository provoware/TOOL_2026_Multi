"""Bewusste Profileingabe mit schreibfreier Vorschau im bestehenden Store."""
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPlainTextEdit,
    QPushButton, QVBoxLayout, QWidget, QLayout,
)

from app.module_widgets import ask_unsaved
from app.event_log import EventLogger
from app.profile_store import CATEGORIES, add_values, input_text, preview_values, split_input_values


def t(key, fallback):
    return input_text('quick.' + key, fallback)


class ProfileQuickEntry(QWidget):
    saved = Signal(str, str, list)
    back_requested = Signal()
    editing_requested = Signal()
    reveal_requested = Signal(QWidget)

    def __init__(self, root: Path, parent=None, *, logger=None):
        super().__init__(parent)
        self.root = root
        self.logger = logger if logger is not None else EventLogger(root, 'unbekannt')
        self.last_event_id = None
        self.profile = ''
        self._signature = None
        self._preview = None
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.back_button = QPushButton(t('back', 'Zurück zur Auswahl'))
        self.back_button.clicked.connect(self.back_requested.emit)
        layout.addWidget(self.back_button)
        self.target_label = QLabel()
        self.target_label.setTextFormat(Qt.PlainText)
        self.target_label.setWordWrap(True)
        layout.addWidget(self.target_label)
        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        self.category_combo.setAccessibleName(t('category', 'Bereich wählen:'))
        category_label = QLabel(t('category', 'Bereich wählen:'))
        category_label.setWordWrap(True)
        category_label.setBuddy(self.category_combo)
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)
        self.value_entry = QLineEdit()
        self.value_entry.setAccessibleName(t('values', 'Neue Werte, mit Komma getrennt'))
        self.value_entry.setPlaceholderText(t('placeholder', 'Zum Beispiel: ruhig, warm …'))
        self.value_entry.setToolTip(input_text('help', 'Mit Komma trennen; Begriffe mit Komma in Anführungszeichen setzen.'))
        value_label = QLabel(t('values', 'Neue Werte, mit Komma getrennt'))
        value_label.setWordWrap(True)
        value_label.setBuddy(self.value_entry)
        layout.addWidget(value_label)
        layout.addWidget(self.value_entry)
        self.preview_text = QPlainTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setAccessibleName(t('preview', 'Vorschau: neu, vorhanden und wiederholt'))
        self.preview_text.setFixedHeight(96)
        layout.addWidget(self.preview_text)
        actions = QHBoxLayout()
        self.check_button = QPushButton(t('check', 'Prüfen'))
        self.check_button.clicked.connect(self.check_values)
        self.save_button = QPushButton(t('save', 'Speichern'))
        self.save_button.setObjectName('primaryButton')
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_values)
        actions.addWidget(self.check_button)
        actions.addWidget(self.save_button)
        layout.addLayout(actions)
        self.status_label = QLabel(t('start', 'Eingeben, prüfen und bewusst speichern.'))
        self.status_label.setTextFormat(Qt.PlainText)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        layout.addStretch(1)
        for button in (self.back_button, self.check_button, self.save_button):
            button.setAccessibleName(button.text())
        self.value_entry.textChanged.connect(self._invalidate)
        self.category_combo.currentTextChanged.connect(self._invalidate)
        self.value_entry.returnPressed.connect(self.check_values)
        escape = QShortcut(QKeySequence('Escape'), self)
        escape.setContext(Qt.WidgetWithChildrenShortcut)
        escape.activated.connect(self.back_requested.emit)

    def set_profile(self, profile):
        if profile != self.profile:
            self.profile = profile
            self.target_label.setText(t('target', 'Profil: {profile}').format(profile=profile))
            self._invalidate()

    def _current(self):
        return (self.profile, self.category_combo.currentText(), self.value_entry.text())

    def _invalidate(self, *_args):
        self._signature = self._preview = None
        self.preview_text.clear()
        self.save_button.setEnabled(False)
        self.status_label.setText(t('changed', 'Vor dem Speichern erneut prüfen.'))
        if self.last_event_id:
            self.status_label.setText(self.status_label.text() + ' ' + t(
                'event_ref', 'Letzter Fehler: {event_id}. Details in Hilfe & Fehlerhilfe.').format(event_id=self.last_event_id))

    def check_values(self):
        self._invalidate()
        # Erwartete Eingabefehler getrennt vom unerwarteten Datei-Lesefehler
        # behandeln; beide Prüfungen nutzen denselben vorhandenen Parser.
        try:
            split_input_values(self.value_entry.text())
        except ValueError as error:
            self._feedback(t('invalid', 'Nicht gespeichert. Eingabe erhalten. Grund: {error}').format(error=error))
            return False
        try:
            preview = preview_values(self.root, *self._current())
        except Exception as error:
            self._operation_failed(error)
            return False
        self._show_preview(preview)
        self.status_label.setText(t('checked', 'Geprüft. Speichern übernimmt die neuen Werte.'))
        self.reveal_requested.emit(self.preview_text)
        return True

    def _feedback(self, text):
        self.status_label.setText(text)
        self.reveal_requested.emit(self.status_label)

    def _operation_failed(self, error):
        self.last_event_id = None
        self._invalidate()
        message = t('invalid', 'Nicht gespeichert. Eingabe erhalten. Grund: {error}').format(error=error)
        try:
            event = self.logger.record(
                severity='FEHLER', area='PROFIL_EINGABE',
                summary=t('log_summary', 'Profilwerte konnten nicht gelesen oder gespeichert werden.'),
                cause=str(error),
                protection=t('log_protection', 'Eingabe erhalten; diese Aktion hat den Profilbestand nicht verändert.'),
                next_step=t('log_next', 'Öffne Hilfe & Fehlerhilfe mit der Ereigniskennung. Prüfe Speicherrechte oder eine geprüfte Sicherung.'),
                exception=error,
            )
            self.last_event_id = event['event_id']
            message += ' ' + t('event_ref', 'Letzter Fehler: {event_id}. Details in Hilfe & Fehlerhilfe.').format(
                event_id=self.last_event_id)
        except Exception:
            # Ein zusätzlich unbeschreibbares Log darf den Eingabeentwurf
            # oder die ursprüngliche Fehlererklärung nicht verdecken.
            message += ' ' + t('log_failed', 'Auch das Fehlerprotokoll konnte nicht vollständig geschrieben werden. Keine vollständige Ereignisaufzeichnung bestätigt. Prüfe Speicherort und Schreibrechte.')
        self._feedback(message)

    def _show_preview(self, preview):
        self._signature, self._preview = self._current(), preview
        names = (('new', t('new', 'Neu')), ('present', t('present', 'Vorhanden')),
                 ('repeated', t('repeated', 'Wiederholt')))
        self.preview_text.setPlainText('\n'.join(
            f'{label} ({len(preview[key])}): ' + ', '.join(f'„{value}“' for value in preview[key])
            for key, label in names))
        self.save_button.setEnabled(True)

    def save_values(self):
        if self._signature != self._current():
            self._invalidate()
            return False
        profile, category, text = self._current()
        try:
            current = preview_values(self.root, profile, category, text)
            if current != self._preview:
                self._show_preview(current)
                self._feedback(t('store_changed', 'Bestand geändert. Vorschau erneuert; bitte erneut Speichern wählen.'))
                return False
            added = add_values(self.root, profile, category, text)
        except Exception as error:
            self._operation_failed(error)
            return False
        skipped = sum(len(values) for values in current.values()) - len(added)
        self.last_event_id = None
        self.value_entry.clear()
        self._invalidate()
        self._feedback(input_text('saved_counts', '{saved} gespeichert · {skipped} übersprungen · 0 fehlerhaft').format(
            saved=len(added), skipped=skipped))
        self.saved.emit(profile, category, added)
        return True

    def confirm_leave(self, *, closing=False):
        if not self.value_entry.text():
            return True
        self.editing_requested.emit()
        answer = ask_unsaved(self, closing=closing)
        if answer == QMessageBox.No:
            return True
        if answer == QMessageBox.Yes:
            return self.save_values()
        return False
