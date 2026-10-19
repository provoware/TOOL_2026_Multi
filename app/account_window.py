"""Konten wiederfinden: Metadaten ausdrücklich ohne Passwortspeicherung."""
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QLabel, QMessageBox
from app import account_store as store
from app.record_window import RecordWindow
from app.custom_fields import CustomFieldsEditor
from app.module_widgets import t, button


class AccountWindow(RecordWindow):
    def __init__(self, root, zoom_percent=100, parent=None):
        fields = [('url', t('account_url', 'Webadresse (http/https) *'), False),
                  ('name', t('account_name', 'Profilname (optional)'), False),
                  ('email', t('account_email', 'Verwendete E-Mail-Adresse'), False),
                  ('hint', t('account_hint', 'Merkhilfe – niemals das Passwort'), False),
                  ('group', t('account_group', 'Gruppe'), False),
                  ('notes', t('account_notes', 'Sonstige Angaben ohne Geheimnisse'), True),
                  ('custom', t('account_custom', 'Eigene Zusatzfelder'), True)]
        super().__init__(root, store, t('accounts', 'Profil- & Accountmanager'), fields, zoom_percent, parent)
        warning = QLabel(t('account_privacy', 'Kein Passworttresor: Diese lokalen Metadaten sind unverschlüsselt. Keine Passwörter, Tokens oder Wiederherstellungscodes eingeben. Für Geheimnisse einen Passwortmanager verwenden.'))
        warning.setWordWrap(True)
        self.form_box.insertWidget(0, warning)
        button(self.form_box, t('account_open', 'Webadresse im Browser öffnen'), self.open_url)
        self.finish_record()

    def make_editor(self, key, multiline):
        return CustomFieldsEditor() if key == 'custom' else super().make_editor(key, multiline)

    def form_record(self):
        raw = super().form_record()
        raw['custom'] = self.fields['custom'].values()
        return raw

    def open_url(self):
        try:
            url = store.validate_url(self.text('url').strip())
            if not QDesktopServices.openUrl(QUrl(url)):
                raise ValueError(t('account_browser_error', 'Der Browser konnte die Adresse nicht öffnen.'))
        except ValueError as error:
            self.error(t('account_open_error', 'Webadresse nicht geöffnet'), error)

    def export_data(self):
        if QMessageBox.question(self, t('account_export_title', 'Kontometadaten exportieren'),
                                t('account_export_privacy', 'Der Export enthält Webadressen, E-Mails, Merkhilfen und Notizen unverschlüsselt. Nur an einem geschützten Ort speichern. Fortfahren?'),
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            super().export_data()
