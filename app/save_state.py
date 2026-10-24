"""Gemeinsame, vom Aktionshinweis unabhängige Speicheranzeige der Schreibfenster."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from app.module_widgets import t


class SaveState(QLabel):
    """Erfolg gehört zu einem konkreten Snapshot, niemals nur zum letzten Klick."""

    def __init__(self, snapshot, title, policy, *, title_required=True):
        super().__init__()
        self.snapshot, self.title, self.policy = snapshot, title, policy
        self.title_required = title_required
        self.saved_snapshot = None
        self.failed_snapshot = None
        self.target = ''
        self.setObjectName('saveState')
        self.setAccessibleName(t('save_state_name', 'Speicherzustand'))
        self.setWordWrap(True)
        self.setTextFormat(Qt.PlainText)
        self.update_state()

    def update_state(self, *_args):
        current = self.snapshot()
        if self.failed_snapshot is not None and current == self.failed_snapshot:
            state = 'failed'
            text = t('save_state_failed', 'Nicht gespeichert · Eingaben bleiben im Fenster. Bitte erneut speichern.')
        elif self.saved_snapshot is not None and current == self.saved_snapshot:
            state = 'saved'
            text = t('save_state_saved', 'Gespeichert · aktueller Stand auf dem Datenträger.')
        elif self.title_required and not self.title().strip():
            state = 'untitled'
            text = t('save_state_untitled', 'Nicht gespeichert · zuerst Titel eingeben. Ohne Titel keine automatische Speicherung.')
        else:
            state = 'changed'
            text = t('save_state_changed', 'Nicht gespeichert · Änderungen nur im Fenster. {policy}').format(policy=self.policy)
        self.setProperty('saveState', state)
        self.setText(text)
        self.setToolTip(self.target if state == 'saved' else text)

    def mark_saved(self, target):
        self.saved_snapshot = self.snapshot()
        self.failed_snapshot = None
        self.target = str(target)
        self.update_state()

    def mark_new(self):
        self.saved_snapshot = self.failed_snapshot = None
        self.target = ''
        self.update_state()

    def mark_failed(self):
        self.failed_snapshot = self.snapshot()
        self.update_state()
