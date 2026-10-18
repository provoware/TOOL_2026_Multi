"""Gemeinsame Listen-/Formularbedienung für Ideen und Kontometadaten."""
import json
from uuid import uuid4
from PySide6.QtCore import Qt, QSignalBlocker, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import (
    QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextEdit, QWidget,
)
from app.module_widgets import ModuleWindow, button, scroll_panel, t


class RecordList(QListWidget):
    def startDrag(self, _actions):
        item = self.currentItem()
        if item is None or not item.data(Qt.UserRole + 1):
            return
        mime = QMimeData()
        mime.setText(item.data(Qt.UserRole + 1))
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.exec(Qt.CopyAction)


class RecordWindow(ModuleWindow):
    def __init__(self, root, store, title, fields, zoom_percent=100, parent=None):
        self.store, self.module, self.collection = store, store.MODULE, store.COLLECTION
        self.validate = store.validate
        self.current_id, self.fields = None, {}
        self.records, self._selected = [], -1
        super().__init__(root, title, zoom_percent, parent)
        split = QSplitter()
        self.outer.addWidget(split, 1)
        left = QWidget()
        from PySide6.QtWidgets import QVBoxLayout
        box = QVBoxLayout(left)
        self.search = QLineEdit()
        self.search.setPlaceholderText(t('record_search', 'Einträge durchsuchen …'))
        self.search.textChanged.connect(self.render)
        box.addWidget(self.search)
        self.group_filter = QComboBox()
        self.group_filter.setAccessibleName(t('record_group_filter', 'Gruppe filtern'))
        self.group_filter.currentTextChanged.connect(self.render)
        box.addWidget(self.group_filter)
        self.listing = RecordList()
        self.listing.setAccessibleName(t('record_list', 'Gespeicherte Einträge'))
        self.listing.currentRowChanged.connect(self.choose)
        box.addWidget(self.listing)
        button(box, t('record_new', 'Neuen Eintrag anlegen'), self.new_record)
        split.addWidget(left)
        scroll, self.form_box = scroll_panel()
        split.addWidget(scroll)
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.WrapAllRows)
        self.form_box.addLayout(form)
        for key, label, multiline in fields:
            editor = self.make_editor(key, multiline)
            if isinstance(editor, QTextEdit):
                editor.setAcceptRichText(False)
                editor.setMaximumHeight(180)
            editor.setAccessibleName(label)
            self.fields[key] = editor
            label_widget = QLabel(label)
            label_widget.setWordWrap(True)
            form.addRow(label_widget, editor)
        self.group_filter.setVisible('group' in self.fields)
        button(self.form_box, t('record_save', 'Eintrag speichern'), self.save)

    def make_editor(self, key, multiline):
        return QTextEdit() if multiline else QLineEdit()

    def finish_record(self):
        self.refresh()
        self.finish()

    def text(self, key):
        field = self.fields[key]
        return field.toPlainText() if isinstance(field, QTextEdit) else field.text()

    def snapshot(self):
        return self.current_id, tuple((key, self.text(key)) for key in self.fields)

    def _reset_form(self):
        self.current_id = None
        for field in self.fields.values():
            field.clear()
        self.remember()

    def discard_draft(self):
        self._reset_form()

    def new_record(self):
        if ModuleWindow.confirm_leave(self):
            self._reset_form()

    def load_state(self):
        return self.store.load(self.root)

    def import_copies(self, raw):
        return self.store.import_copies(self.root, raw)

    def refresh(self):
        try:
            self.records = self.load_state()[self.collection]
            if 'group' in self.fields:
                old = self.group_filter.currentText()
                with QSignalBlocker(self.group_filter):
                    self.group_filter.clear()
                    self.group_filter.addItem(t('record_all_groups', 'Alle Gruppen'))
                    self.group_filter.addItems(sorted({r['group'] for r in self.records if r['group']}))
                    index = self.group_filter.findText(old)
                    self.group_filter.setCurrentIndex(max(0, index))
            self.render()
        except (OSError, ValueError) as error:
            self.error(t('record_load_error', 'Einträge nicht lesbar'), error)

    def render(self):
        query = self.search.text().casefold()
        group = self.group_filter.currentText() if self.group_filter.currentIndex() > 0 else ''
        with QSignalBlocker(self.listing):
            self.listing.clear()
            for record in self.records:
                if query not in json.dumps(record, ensure_ascii=False).casefold() or group and record.get('group') != group:
                    continue
                item = QListWidgetItem(self.record_label(record))
                item.setData(Qt.UserRole, record['id'])
                item.setData(Qt.UserRole + 1, record.get('content', ''))
                self.listing.addItem(item)
            self._selected = -1

    def record_label(self, record):
        return record.get('title') or record.get('name') or record.get('url')

    def choose(self, row):
        item = self.listing.item(row)
        if item is None:
            return
        if not ModuleWindow.confirm_leave(self):
            with QSignalBlocker(self.listing):
                self.listing.setCurrentRow(self._selected)
            return
        record = next(r for r in self.records if r['id'] == item.data(Qt.UserRole))
        self.current_id, self._selected = record['id'], row
        for key, field in self.fields.items():
            value = record[key]
            if isinstance(value, list):
                value = ', '.join(value)
            elif isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False, indent=2)
            if isinstance(field, QTextEdit):
                field.setPlainText(value)
            else:
                field.setText(value)
        self.remember()

    def form_record(self):
        return {'id': self.current_id or uuid4().hex, **{key: self.text(key) for key in self.fields}}

    def save(self):
        try:
            record = self.store.put(self.root, self.form_record())
            self.current_id = record['id']
            self.remember()
            self.refresh()
            self.status.setText(t('record_saved', 'Eintrag gespeichert.'))
            return True
        except (OSError, ValueError) as error:
            self.error(t('record_save_error', 'Eintrag nicht gespeichert'), error)
            return False
