"""Gemeinsame Bedienung, Datenaustausch und Fehlerrückmeldung neuer Module."""
from __future__ import annotations

import json
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QBoxLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton,
    QScrollArea, QVBoxLayout, QWidget,
)
from app import module_archive as archive
from app.texts import TextRegistry
from app.ui_standards import SPACING, apply_global_style

_REGISTRY = None


def t(key, fallback):
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = TextRegistry(Path(__file__).resolve().parent.parent / 'texte/registry.json')
    return _REGISTRY.get('modules.' + key, fallback)



def ask_unsaved(parent, *, closing=False):
    """Aktionswörter und sichere Vorauswahl statt mehrdeutiger Ja/Nein-Antworten."""
    dialog = QMessageBox(parent)
    dialog.setIcon(QMessageBox.Question)
    dialog.setWindowTitle(t('unsaved', 'Ungespeicherte Änderungen'))
    dialog.setText(t('leave_explicit', 'Deine Änderungen sind noch nicht gespeichert. Was möchtest du tun?'))
    dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    dialog.button(QMessageBox.Yes).setText(t('leave_save_close' if closing else 'leave_save_switch',
        'Speichern und schließen' if closing else 'Speichern und wechseln'))
    dialog.button(QMessageBox.No).setText(t('leave_discard_close' if closing else 'leave_discard_switch',
        'Verwerfen und schließen' if closing else 'Verwerfen und wechseln'))
    dialog.button(QMessageBox.Cancel).setText(t('leave_keep', 'Weiterarbeiten'))
    dialog.setDefaultButton(QMessageBox.Cancel)
    dialog.setEscapeButton(QMessageBox.Cancel)
    dialog.setTextFormat(Qt.PlainText)
    return dialog.exec()


def button(layout, label, action):
    widget = QPushButton(label)
    widget.setAccessibleName(label)
    widget.setFocusPolicy(Qt.StrongFocus)
    widget.clicked.connect(lambda _checked=False: action())
    layout.addWidget(widget)
    return widget


def scroll_panel():
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    host = QWidget()
    box = QVBoxLayout(host)
    box.setSpacing(SPACING['s'])
    scroll.setWidget(host)
    return scroll, box


class ModuleWindow(QWidget):
    """Gleicher Grundaufbau und Schutz ungespeicherter Arbeit in beiden Modulen."""

    def __init__(self, root, title, zoom_percent=100, parent=None):
        super().__init__(parent, Qt.Window)
        self.root, self.zoom_percent = Path(root), zoom_percent
        self.setWindowTitle(title)
        self.resize(1120, 760)
        self.setMinimumSize(640, 480)
        self.outer = QVBoxLayout(self)
        self.outer.setContentsMargins(*([SPACING['s']] * 4))
        self.header = QBoxLayout(QBoxLayout.LeftToRight)
        self.heading = QLabel(title)
        self.heading.setObjectName('sectionTitle')
        self.heading.setWordWrap(True)
        self.header.addWidget(self.heading, 1)
        self.header_actions = QWidget()
        actions = QHBoxLayout(self.header_actions)
        actions.setContentsMargins(0, 0, 0, 0)
        button(actions, t('import', 'Importieren'), self.import_data)
        button(actions, t('export', 'Exportieren'), self.export_data)
        button(actions, t('close', 'Schließen'), self.close)
        self.header.addWidget(self.header_actions)
        self.outer.addLayout(self.header)
        self.status = QLabel(t('ready', 'Bereit.'))
        self.status.setWordWrap(True)
        self.status.setTextFormat(Qt.PlainText)
        self._baseline = None
        QShortcut(QKeySequence('Ctrl+S'), self, activated=self.save)
        QShortcut(QKeySequence('F5'), self, activated=self.refresh)

    def finish(self):
        self.outer.addWidget(self.status)
        self.set_zoom(self.zoom_percent)
        self.remember()

    def set_zoom(self, percent):
        self.zoom_percent = percent
        apply_global_style(self, percent)
        self._header_layout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._header_layout()

    def _header_layout(self):
        needed = self.heading.fontMetrics().horizontalAdvance(self.windowTitle()) + self.header_actions.sizeHint().width() + 48
        self.header.setDirection(QBoxLayout.TopToBottom if self.width() < needed else QBoxLayout.LeftToRight)

    def remember(self):
        self._baseline = self.snapshot()

    def confirm_leave(self, *, closing=False):
        if self._baseline is None or self.snapshot() == self._baseline:
            return True
        answer = ask_unsaved(self, closing=closing)
        return answer == QMessageBox.No or answer == QMessageBox.Yes and bool(self.save())

    def closeEvent(self, event):
        if self.confirm_leave(closing=True):
            if self.snapshot() != self._baseline:
                self.discard_draft()
            event.accept()
        else:
            event.ignore()

    def error(self, action, error):
        message = t('error', 'Die Aktion konnte nicht abgeschlossen werden. Der gespeicherte Bestand bleibt geschützt. Bitte Eingaben und Dateirechte prüfen.')
        logger = getattr(self.parent(), 'logger', None)
        event_id = ''
        if logger is not None:
            try:
                event = logger.record(severity='ERROR', area=self.module, summary=action,
                                      cause=type(error).__name__, protection=message,
                                      next_step='Eingaben und Dateirechte prüfen; danach erneut versuchen.')
                event_id = '\nKennung: ' + event['event_id']
            except OSError:
                event_id = '\nProtokoll konnte nicht geschrieben werden.'
        self.status.setText(action + ' · ' + str(error))
        QMessageBox.warning(self, action, message + '\n\n' + str(error) + event_id)

    def export_data(self):
        target, _ = QFileDialog.getSaveFileName(self, t('export', 'Exportieren'), self.module + '.json', 'JSON (*.json)')
        if not target:
            return
        try:
            # Ein Export bildet immer den sichtbaren, ausdrücklich gespeicherten Stand ab.
            if not self.confirm_leave():
                return
            archive.export_archive(Path(target), self.module, self.load_state(), self.validate, root=self.root)
            self.status.setText(t('exported', 'Gespeicherter Modulbestand exportiert.'))
        except Exception as error:
            self.error(t('export_failed', 'Export fehlgeschlagen'), error)

    def import_data(self):
        source, _ = QFileDialog.getOpenFileName(self, t('import', 'Importieren'), '', 'JSON (*.json)')
        if not source:
            return
        try:
            data = archive.read_archive(Path(source), self.module, self.validate)
            count = len(data[self.collection])
            message = t('import_preview', '{count} Einträge geprüft. Als neue Kopien ergänzen? Vorhandene Einträge bleiben erhalten.').format(count=count)
            if QMessageBox.question(self, t('preview', 'Importvorschau'), message,
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
                return
            self.import_copies(data)
            self.refresh()
            self.status.setText(t('imported', '{count} Einträge als neue Kopien ergänzt.').format(count=count))
        except Exception as error:
            self.error(t('import_failed', 'Import fehlgeschlagen'), error)

    def paste_field(self, field):
        value = QApplication.clipboard().text()
        if hasattr(field, 'setPlainText'):
            field.insertPlainText(value)
        else:
            field.insert(value.replace('\n', ' '))
        field.setFocus()
        self.status.setText(t('pasted', 'Text aus der Zwischenablage eingefügt.'))
