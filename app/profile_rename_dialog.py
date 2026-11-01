"""Prüfbarer Umbenennungsdialog mit ausdrücklicher Freigabe für Namensbezüge."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QDialog, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QScrollArea, QVBoxLayout, QWidget,
)
from app.event_log import EventLogger
from app.profile_transaction import ProfileRecoveryError
from app.profile_management import RenameError, preview_profile_rename, rename_profile, t
from app.ui_standards import apply_global_style


class ProfileRenameDialog(QDialog):
    def __init__(self, root, old_name, *, logger=None, zoom_percent=100, parent=None):
        super().__init__(parent)
        self.root, self.old_name = root, old_name
        self.zoom_percent = zoom_percent
        self.logger = logger if logger is not None else EventLogger(root, 'unbekannt')
        self.plan = self.signature = self.renamed_to = self.last_event_id = None
        self.setWindowTitle(t('title', 'Profil sicher umbenennen'))
        self.resize(600, 460)
        self.setMinimumSize(420, 340)
        self._build()
        apply_global_style(self, zoom_percent)

    def _build(self):
        outer = QVBoxLayout(self)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        body = QWidget()
        layout = QVBoxLayout(body)
        target = QLabel(t('target', 'Ausgewähltes Profil: {name}').format(name=self.old_name))
        target.setTextFormat(Qt.PlainText)
        target.setWordWrap(True)
        layout.addWidget(target)
        label = QLabel(t('new_label', 'Neuer Profilname:'))
        self.name_entry = QLineEdit()
        self.name_entry.setAccessibleName(label.text())
        label.setBuddy(self.name_entry)
        layout.addWidget(label)
        layout.addWidget(self.name_entry)
        self.transfer_links = QCheckBox(t('transfer_label', 'Bezüge übertragen'))
        self.transfer_links.setAccessibleName(t('transfer_accessible', 'Favoriten und Verlauf mit umbenennen'))
        self.transfer_links.setToolTip(t('transfer_help', 'Nach der Prüfung die Bezüge zum alten Namen gemeinsam übertragen. Abweichende Namen und belegte Zielnamen bleiben gesperrt.'))
        self.transfer_links.toggled.connect(self._invalidate)
        layout.addWidget(self.transfer_links)
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setMinimumHeight(120)
        self.preview.setAccessibleName(t('preview_label', 'Vorschau und Verknüpfungen der Umbenennung'))
        layout.addWidget(self.preview, 1)
        self.scroll.setWidget(body)
        outer.addWidget(self.scroll, 1)
        actions = QHBoxLayout()
        self.check_button = QPushButton(t('check', 'Prüfen'))
        self.rename_button = QPushButton(t('action', 'Umbenennen'))
        self.rename_button.setObjectName('primaryButton')
        self.rename_button.setEnabled(False)
        self.cancel_button = QPushButton(t('cancel', 'Abbrechen'))
        actions.addWidget(self.check_button)
        actions.addWidget(self.rename_button)
        outer.addLayout(actions)
        outer.addWidget(self.cancel_button)
        for button in (self.check_button, self.rename_button, self.cancel_button):
            button.setAutoDefault(False)
            button.setAccessibleName(button.text())
        self.name_entry.textChanged.connect(self._invalidate)
        self.name_entry.returnPressed.connect(self.check)
        self.check_button.clicked.connect(self.check)
        self.rename_button.clicked.connect(self.apply)
        self.cancel_button.clicked.connect(self.reject)
        self._invalidate()

    def _invalidate(self, *_args):
        self.plan = self.signature = None
        self.rename_button.setEnabled(False)
        message = t('first', 'Neuen Namen eingeben und zuerst prüfen. Es wird noch nichts geändert.')
        if self.last_event_id:
            message += '\n' + t('event', 'Letzter Fehler: {event_id}. Details in Hilfe & Fehlerhilfe.').format(event_id=self.last_event_id)
        self.preview.setPlainText(message)

    def check(self):
        self._invalidate()
        try:
            plan = preview_profile_rename(self.root, self.old_name, self.name_entry.text(), transfer_links=self.transfer_links.isChecked())
        except RenameError as error:
            self.preview.setPlainText(str(error))
            return False
        except Exception as error:
            self._failure(error)
            return False
        self.plan, self.signature = plan, self.name_entry.text()
        message = t('summary', '{old} → {new}\nBekannte Werte: {values}\nFavoritenzuordnungen: {favorites}\nVerlaufseinträge: {history}').format(
            old=plan.old_name, new=plan.new_name, values=plan.value_count,
            favorites=plan.favorite_links, history=plan.history_links)
        if plan.transfer_links and plan.allowed and (plan.favorite_links or plan.history_links):
            message += '\n\n' + t('transfer_ready', 'Die angezeigten Bezüge zum alten Namen werden gemeinsam mit dem Profilnamen übertragen. Favoritenwerte und bisherige Ergebnisse bleiben erhalten.')
        elif plan.unsafe_links:
            message += '\n\n' + t('unsafe_links', 'Bezüge zu einer abweichenden Schreibweise oder zum Zielnamen sind mehrdeutig. Die Umbenennung bleibt gesperrt; es wird nichts zusammengeführt.')
        else:
            message += '\n\n' + (t('ready', 'Keine Namensbezüge gefunden. Nur der Profilname wird geändert; vorhandene Datenfelder bleiben erhalten.')
                                if plan.allowed else t('blocked', 'Favoriten oder Verlauf verwenden den alten oder neuen Namen. Die Umbenennung ist zum Schutz dieser Verknüpfungen gesperrt.'))
        self.preview.setPlainText(message)
        self.rename_button.setEnabled(plan.allowed)
        return plan.allowed

    def apply(self):
        if self.plan is None or self.signature != self.name_entry.text():
            self._invalidate()
            return False
        try:
            new_name = rename_profile(self.root, self.plan)
        except RenameError as error:
            self._invalidate()
            self.preview.setPlainText(str(error))
            return False
        except Exception as error:
            self._failure(error)
            return False
        self.renamed_to = new_name
        self.accept()
        return True

    def _failure(self, error):
        self.last_event_id = None
        self._invalidate()
        message = (t('pending_failure', 'Die Profiländerung ist unvollständig. Weitere Profilzugriffe sind gesperrt. Bitte neu starten; Wiederherstellungsjournal erhalten. Grund: {error}') if isinstance(error, ProfileRecoveryError) else t('failure', 'Nicht umbenannt. Name und Bestand bleiben erhalten. Grund: {error}')).format(error=error)
        try:
            event = self.logger.record(
                severity='FEHLER', area='PROFIL_UMBENENNEN',
                summary=t('log_summary', 'Ein Profil konnte nicht sicher umbenannt werden.'),
                cause=str(error), protection=(t('pending_protection', 'Profilzugriffe bis zur Wiederherstellung gesperrt; Journal erhalten.') if isinstance(error, ProfileRecoveryError) else t('protected', 'Kein Profilname geändert; Vorschlag und ursprünglicher Bestand bleiben erhalten.')),
                next_step=t('next', 'Öffne Hilfe & Fehlerhilfe mit der Ereigniskennung und prüfe Dateien oder Schreibrechte.'),
                exception=error,
            )
            self.last_event_id = event['event_id']
            message += '\n' + t('event', 'Letzter Fehler: {event_id}. Details in Hilfe & Fehlerhilfe.').format(event_id=self.last_event_id)
        except Exception:
            message += '\n' + t('log_failed', 'Auch das Fehlerprotokoll konnte nicht vollständig geschrieben werden. Prüfe Speicherort und Schreibrechte.')
        self.preview.setPlainText(message)
