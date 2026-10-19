"""Grafischer Entwurfseditor für deklarative (nicht ausführbare) Zusatzmodule."""
from __future__ import annotations

from uuid import uuid4
from PySide6.QtCore import Qt, QSignalBlocker
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMessageBox, QTextEdit, QSplitter, QVBoxLayout, QWidget,
)
from app import module_blueprints as store
from app.module_records_dialog import ModuleRecordsDialog
from app.module_widgets import ModuleWindow, button, scroll_panel


class BlueprintWindow(ModuleWindow):
    def __init__(self, root, zoom_percent=100, parent=None):
        self.module, self.collection = store.MODULE, store.COLLECTION
        self.validate = store.validate
        self.current_id = None
        self.entries = []
        super().__init__(root, "Modulbaukasten · Entwürfe", zoom_percent, parent)
        splitter = QSplitter()
        self.outer.addWidget(splitter, 1)
        left = QWidget()
        left_box = QVBoxLayout(left)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Entwürfe suchen")
        self.search.textChanged.connect(self.render)
        left_box.addWidget(self.search)
        self.listing = QListWidget()
        self.listing.setAccessibleName("Gespeicherte Modulentwürfe")
        self.listing.currentRowChanged.connect(self.select)
        left_box.addWidget(self.listing)
        button(left_box, "Neuer Modulentwurf", self.new)
        button(left_box, "Entwurf löschen", self.delete)
        splitter.addWidget(left)
        right, box = scroll_panel()
        splitter.addWidget(right)
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.WrapAllRows)
        box.addLayout(form)
        self.title = QLineEdit()
        self.title.setAccessibleName("Name des Moduls")
        self.description = QTextEdit()
        self.description.setMaximumHeight(100)
        self.description.setAcceptRichText(False)
        self.description.setAccessibleName("Modulbeschreibung")
        self.field_text = QLineEdit("Titel, Inhalt")
        self.field_text.setPlaceholderText("Titel, Inhalt, Datum")
        self.field_text.setAccessibleName("Feldbezeichnungen mit Komma trennen")
        form.addRow("Modulname", self.title)
        form.addRow("Beschreibung", self.description)
        form.addRow("Eingabefelder (mit Komma getrennt)", self.field_text)
        box.addWidget(QLabel("Die Vorschau enthält nur harmlose Eingabefelder; niemals Python- oder Shell-Code."))
        self.checks = {}
        for key, label in (("edit", "Bearbeiten"), ("search", "Suche"),
                           ("import", "Import"), ("export", "Export")):
            check = QCheckBox(label)
            check.setAccessibleName("Fähigkeit " + label)
            self.checks[key] = check
            box.addWidget(check)
        button(box, "Entwurf speichern", self.save)
        button(box, "Vorschau erzeugen", self.preview)
        button(box, "Datensätze des Moduls öffnen", self.open_records)
        self.preview_frame = QWidget()
        self.preview_layout = QFormLayout(self.preview_frame)
        box.addWidget(self.preview_frame)
        self._baseline = None
        self.refresh()
        self.finish()

    def snapshot(self):
        return (self.current_id, self.title.text(), self.description.toPlainText(),
                self.field_text.text(), tuple(key for key, box in self.checks.items() if box.isChecked()))

    def load_state(self):
        return store.load(self.root)

    def import_copies(self, raw):
        return store.import_copies(self.root, raw)

    def refresh(self):
        try:
            self.entries = self.load_state()[self.collection]
            self.render()
        except (OSError, ValueError) as error:
            self.error("Modulentwürfe nicht lesbar", error)

    def render(self):
        query = self.search.text().casefold()
        with QSignalBlocker(self.listing):
            self.listing.clear()
            for x in self.entries:
                if query in (x["title"] + " " + x["description"]).casefold():
                    item = QListWidgetItem(x["title"])
                    item.setData(Qt.UserRole, x["id"])
                    self.listing.addItem(item)

    def select(self, n):
        item = self.listing.item(n)
        if item is None:
            return
        ident = item.data(Qt.UserRole)
        if not self.confirm_leave():
            return
        record = next((x for x in self.entries if x["id"] == ident), None)
        if record is None:
            return
        self.current_id = ident
        self.title.setText(record["title"])
        self.description.setPlainText(record["description"])
        self.field_text.setText(", ".join(field["label"] for field in record["fields"]))
        for key, field in self.checks.items():
            field.setChecked(key in record["capabilities"])
        self.remember()

    def new(self):
        if self.confirm_leave():
            self.discard_draft()

    def discard_draft(self):
        self.current_id = None
        self.title.clear()
        self.description.clear()
        self.field_text.setText("Titel, Inhalt")
        for box in self.checks.values():
            box.setChecked(False)
        self.remember()

    def form_record(self):
        labels = [x.strip() for x in self.field_text.text().split(",")]
        if not all(labels):
            raise ValueError("Bitte alle Feldnamen ausfüllen.")
        return {"id": self.current_id or uuid4().hex,
                "title": self.title.text().strip(), "description": self.description.toPlainText(),
                "fields": [{"id": f"field_{i}", "label": label, "type": "text"}
                           for i, label in enumerate(labels, start=1)],
                "capabilities": ["view"] + [key for key, check in self.checks.items()
                                           if check.isChecked()]}

    def save(self):
        try:
            record = store.put(self.root, self.form_record())
            self.current_id = record["id"]
            self.refresh()
            self.remember()
            self.status.setText("Modulentwurf sicher gespeichert. Kein fremder Code ausgeführt.")
            return True
        except (OSError, ValueError) as error:
            self.error("Modulentwurf nicht gespeichert", error)
            return False

    def preview(self):
        try:
            definition = store.preview_definition(self.form_record())
        except ValueError as error:
            self.error("Vorschau nicht möglich", error)
            return
        while self.preview_layout.count():
            row = self.preview_layout.takeAt(0)
            if row.widget() is not None:
                row.widget().deleteLater()
        for field in definition["fields"]:
            editor = QLineEdit()
            editor.setReadOnly(True)
            editor.setPlaceholderText("Vorschau: " + field["label"])
            self.preview_layout.addRow(field["label"], editor)
        self.status.setText("Vorschau erstellt – nur Darstellung, keine Programmausführung.")

    def open_records(self):
        if not self.confirm_leave():
            return
        if self.current_id is None:
            self.status.setText("Bitte zuerst einen Modulentwurf speichern.")
            return
        try:
            dialog = ModuleRecordsDialog(self.root, self.current_id, self)
            dialog.exec()
        except (OSError, ValueError) as error:
            self.error("Moduldaten nicht geöffnet", error)

    def delete(self):
        if self.current_id is None:
            return
        if QMessageBox.question(self, "Modulentwurf löschen",
                                "Diesen Entwurf wirklich löschen? Andere Module bleiben unverändert.",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return
        try:
            store.remove(self.root, self.current_id)
            self.discard_draft()
            self.refresh()
        except (OSError, ValueError) as error:
            self.error("Entwurf konnte nicht gelöscht werden", error)
