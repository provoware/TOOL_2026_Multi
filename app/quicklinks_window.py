"""Übersichtliche Schnellstarter-Verwaltung mit bewusstem Browseraufruf."""
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox
from app import quicklinks_store as store
from app.account_store import validate_url
from app.module_widgets import t, button, ModuleWindow
from app.record_window import RecordWindow


class QuicklinksWindow(RecordWindow):
    def __init__(self, root, zoom_percent=100, parent=None):
        fields = [
            ('name', t('quicklinks_name', 'Name des Schnellstarters'), False),
            ('url', t('quicklinks_url', 'Webadresse (https:// oder http://)'), False),
            ('group', t('quicklinks_group', 'Gruppe, optional'), False),
            ('icon', t('quicklinks_icon', 'Kurzer Symboltext, optional'), False),
        ]
        super().__init__(root, store, t('quicklinks', 'Link-Schnellstarter'), fields, zoom_percent, parent)
        button(self.form_box, t('quicklinks_open', 'Ausgewählte Webseite öffnen'), self.open_selected)
        button(self.form_box, t('quicklinks_delete', 'Ausgewählten Eintrag löschen'), self.delete_selected)
        self.finish_record()

    def record_label(self, record):
        prefix = (record['icon'] + '  ') if record['icon'] else ''
        return prefix + record['name'] + (' · ' + record['group'] if record['group'] else '')

    def open_selected(self):
        try:
            url = validate_url(self.fields['url'].text().strip())
            if not QDesktopServices.openUrl(QUrl(url)):
                raise ValueError('Der Standardbrowser konnte die Adresse nicht öffnen.')
            self.status.setText(t('quicklinks_opened', 'Adresse an den Standardbrowser übergeben.'))
        except ValueError as error:
            self.error(t('quicklinks_open_error', 'Webseite konnte nicht geöffnet werden'), error)

    def delete_selected(self):
        if self.current_id is None:
            self.status.setText(t('quicklinks_select', 'Bitte zuerst einen gespeicherten Eintrag auswählen.'))
            return
        if not ModuleWindow.confirm_leave(self):
            return
        if QMessageBox.question(
            self, t('quicklinks_delete_title', 'Schnellstarter entfernen?'),
            t('quicklinks_delete_confirm', 'Nur diesen gespeicherten Link löschen? Andere Einträge bleiben erhalten.'),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        ) != QMessageBox.Yes:
            return
        try:
            store.remove(self.root, self.current_id)
            self._reset_form()
            self.refresh()
            self.status.setText(t('quicklinks_deleted', 'Schnellstarter entfernt.'))
        except (ValueError, OSError) as error:
            self.error(t('quicklinks_delete_error', 'Löschen fehlgeschlagen'), error)
