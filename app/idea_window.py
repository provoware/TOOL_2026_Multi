"""Ideen sammeln und per Kopie zu neuen Texten zusammenstellen."""
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QMessageBox, QTextEdit
from app import idea_store as store
from app.record_window import RecordWindow
from app.module_widgets import t, button
from app.text_editor_store import TextDocument, save_text_document


class IdeaWindow(RecordWindow):
    def __init__(self, root, zoom_percent=100, parent=None):
        fields = [('title', t('idea_title', 'Ideentitel'), False),
                  ('content', t('idea_content', 'Textfragment'), True),
                  ('tags', t('idea_tags', 'Schlagworte, mit Komma getrennt'), False),
                  ('origin', t('idea_origin', 'Herkunft oder Quelle'), False)]
        super().__init__(root, store, t('ideas', 'Textfragmente & Ideenarchiv'), fields, zoom_percent, parent)
        self.listing.setDragEnabled(True)
        self.composition_title = QLineEdit()
        self.composition_title.setPlaceholderText(t('idea_composition_title', 'Titel des neuen Textes'))
        self.composition_title.setAccessibleName(t('idea_composition_title', 'Titel des neuen Textes'))
        self.composition = QTextEdit()
        self.composition.setAcceptRichText(False)
        self.composition.setAcceptDrops(True)
        self.composition.setAccessibleName(t('idea_composition', 'Komposition: Fragmente hierher ziehen oder kopieren'))
        self.form_box.addWidget(self.composition_title)
        self.form_box.addWidget(self.composition)
        button(self.form_box, t('idea_append', 'Ausgewähltes Fragment als Kopie anfügen'), self.append_selected)
        button(self.form_box, t('idea_compose_save', 'Komposition als neuen Text speichern'), self.save_composition)
        self._composition_saved = ('', '')
        self.finish_record()

    def form_record(self):
        raw = super().form_record()
        raw['tags'] = list(dict.fromkeys(tag.strip() for tag in raw['tags'].split(',') if tag.strip()))
        return raw

    def append_selected(self):
        item = self.listing.currentItem()
        if item is not None:
            from PySide6.QtCore import Qt
            text = item.data(Qt.UserRole + 1)
            self.composition.insertPlainText(('\n' if self.composition.toPlainText() else '') + text)

    def save_composition(self):
        title, text = self.composition_title.text().strip(), self.composition.toPlainText()
        if title and (self.composition_title.text(), text) == self._composition_saved:
            return True
        try:
            if not title or not text.strip():
                raise ValueError(t('idea_composition_required', 'Bitte Titel und Kompositionstext ausfüllen.'))
            path = save_text_document(self.root, TextDocument(title=title, text=text))
            self._composition_saved = (self.composition_title.text(), text)
            self.status.setText(t('idea_composed', 'Neuer Text gespeichert; alle ursprünglichen Ideen bleiben erhalten.') + ' ' + path.name)
            return True
        except (OSError, ValueError) as error:
            self.error(t('idea_compose_error', 'Komposition nicht gespeichert'), error)
            return False

    def confirm_leave(self):
        if not super().confirm_leave():
            return False
        if (self.composition_title.text(), self.composition.toPlainText()) == self._composition_saved:
            return True
        answer = QMessageBox.question(self, t('unsaved', 'Ungespeicherte Änderungen'),
                                      t('idea_compose_leave', 'Komposition speichern? Ja = speichern, Nein = verwerfen, Abbrechen = bleiben.'),
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if answer == QMessageBox.No:
            self.composition.clear()
            self.composition_title.clear()
            self._composition_saved = ('', '')
            return True
        return answer == QMessageBox.Yes and self.save_composition()

    def discard_draft(self):
        super().discard_draft()
        self.composition.clear()
        self.composition_title.clear()
        self._composition_saved = ('', '')
