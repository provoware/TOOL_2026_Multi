"""Schreibfreie Abhängigkeitsvorschau vor ausdrücklich bestätigtem Löschen."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QDialog, QHBoxLayout, QPlainTextEdit, QPushButton,
    QScrollArea, QVBoxLayout, QWidget,
)
from app.event_log import EventLogger
from app.profile_deletion import DeleteError, delete_profile, preview_profile_delete, t
from app.profile_transaction import ProfileRecoveryError
from app.ui_standards import apply_global_style


class ProfileDeleteDialog(QDialog):
    def __init__(self, root, name, *, logger=None, zoom_percent=100, parent=None):
        super().__init__(parent)
        self.root, self.name = root, name
        self.zoom_percent = zoom_percent
        self.logger = logger if logger is not None else EventLogger(root, 'unbekannt')
        self.plan = self.deleted_name = self.last_event_id = None
        self.setWindowTitle(t('title', 'Profil sicher löschen'))
        self.resize(600, 460)
        self.setMinimumSize(420, 340)
        outer = QVBoxLayout(self)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        body = QWidget()
        content = QVBoxLayout(body)
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setMinimumHeight(120)
        self.preview.setAccessibleName(t('preview_label', 'Löschvorschau mit Profilinhalt und Abhängigkeiten'))
        content.addWidget(self.preview, 1)
        self.confirm = QCheckBox(t('confirm', 'Löschen bestätigen'))
        self.confirm.setAccessibleName(t('confirm_accessible', 'Das geprüfte Profil mit allen enthaltenen Feldern endgültig löschen'))
        self.confirm.setToolTip(t('irreversible', 'Im Programm gibt es nach erfolgreichem Löschen keine Rückgängig-Funktion.'))
        self.confirm.toggled.connect(self._enable_action)
        content.addWidget(self.confirm)
        self.scroll.setWidget(body)
        outer.addWidget(self.scroll, 1)
        actions = QHBoxLayout()
        self.check_button = QPushButton(t('check', 'Prüfen'))
        self.delete_button = QPushButton(t('action', 'Profil löschen'))
        self.delete_button.setObjectName('dangerButton')
        self.cancel_button = QPushButton(t('cancel', 'Abbrechen'))
        for button in (self.check_button, self.delete_button):
            actions.addWidget(button)
        outer.addLayout(actions)
        outer.addWidget(self.cancel_button)
        for button in (self.check_button, self.delete_button, self.cancel_button):
            button.setAutoDefault(False)
            button.setAccessibleName(button.text())
        self.check_button.clicked.connect(self.check)
        self.delete_button.clicked.connect(self.apply)
        self.cancel_button.clicked.connect(self.reject)
        self._invalidate()
        apply_global_style(self, zoom_percent)
        self.cancel_button.setFocus()

    def _enable_action(self, *_args):
        self.delete_button.setEnabled(bool(self.plan and self.plan.allowed and self.confirm.isChecked()))

    def _invalidate(self):
        self.plan = None
        self.confirm.setChecked(False)
        self.confirm.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.preview.setPlainText(t('start', 'Profil: {name}\nZuerst prüfen. Es wurde noch nichts gelöscht.').format(name=self.name))

    def check(self):
        self._invalidate()
        try:
            plan = preview_profile_delete(self.root, self.name)
        except DeleteError as error:
            self.preview.setPlainText(str(error))
            return False
        except Exception as error:
            self._failure(error)
            return False
        self.plan = plan
        lines = [t('target', 'Zu löschendes Profil: {name}').format(name=plan.name)]
        lines += [f'{category}: {count}' for category, count in plan.categories]
        lines.append(t('extra', 'Zusätzliche Felder (ebenfalls betroffen): {fields}').format(fields=', '.join(plan.extra_fields) or t('none', 'keine')))
        lines.append(t('counts', 'Verbleibende Profile: {remaining}\nFavoritenzuordnungen: {favorites}\nVerlaufseinträge: {history}').format(
            remaining=plan.remaining_profiles, favorites=plan.favorite_links, history=plan.history_links))
        if plan.favorite_links or plan.history_links:
            lines.append(t('references', 'Favoriten oder Verlauf verwenden dieses Profil. Löschen ist zum Schutz der Bezüge gesperrt.'))
        if plan.remaining_profiles < 1:
            lines.append(t('last', 'Das letzte Profil bleibt erhalten. Bitte zuerst ein anderes Profil anlegen.'))
        if plan.allowed:
            lines.append(t('ready', 'Keine Bezüge gefunden. Das Profil wird mit allen enthaltenen Feldern entfernt. Favoriten und Verlauf bleiben unverändert.'))
            lines.append(t('irreversible', 'Im Programm gibt es nach erfolgreichem Löschen keine Rückgängig-Funktion.'))
        self.preview.setPlainText('\n\n'.join(lines))
        self.confirm.setEnabled(plan.allowed)
        return plan.allowed

    def apply(self):
        if self.plan is None or not self.confirm.isChecked() or not self.plan.allowed:
            return False
        try:
            deleted = delete_profile(self.root, self.plan)
        except DeleteError as error:
            self._invalidate()
            self.preview.setPlainText(str(error))
            return False
        except Exception as error:
            self._failure(error)
            return False
        self.deleted_name = deleted
        self.accept()
        return True

    def _failure(self, error):
        self.last_event_id = None
        self._invalidate()
        pending = isinstance(error, ProfileRecoveryError)
        message = (t('pending', 'Die Profiländerung ist unvollständig. Profilzugriffe sind gesperrt. Bitte neu starten; Journal nicht löschen. Grund: {error}')
                   if pending else t('failure', 'Profil nicht gelöscht. Der bisherige Bestand bleibt erhalten. Grund: {error}')).format(error=error)
        try:
            event = self.logger.record(
                severity='FEHLER', area='PROFIL_LOESCHEN',
                summary=t('log_summary', 'Ein Profil konnte nicht sicher gelöscht werden.'), cause=str(error),
                protection=(t('pending_protection', 'Profilzugriffe bis zur Wiederherstellung gesperrt; Journal erhalten.') if pending else t('protected', 'Löschen abgebrochen; bisheriger Bestand erhalten.')),
                next_step=t('next', 'Öffne Hilfe & Fehlerhilfe mit der Ereigniskennung und prüfe Dateien oder Schreibrechte.'), exception=error,
            )
            self.last_event_id = event['event_id']
            message += '\n' + t('event', 'Fehler: {event_id}. Details in Hilfe & Fehlerhilfe.').format(event_id=self.last_event_id)
        except Exception:
            message += '\n' + t('log_failed', 'Auch das Fehlerprotokoll konnte nicht vollständig geschrieben werden. Prüfe Speicherort und Schreibrechte.')
        self.preview.setPlainText(message)
