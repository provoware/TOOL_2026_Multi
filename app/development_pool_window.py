"""Verwaltung lokaler Entwicklungsprojekte, Kopien und ZIP-Archive."""
from __future__ import annotations

from uuid import uuid4

from PySide6.QtCore import Qt, QSignalBlocker
from PySide6.QtWidgets import (
    QFileDialog, QComboBox, QFormLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMessageBox, QTextEdit, QSplitter, QVBoxLayout, QWidget,
)
from app import development_pool as store
from app.module_widgets import ModuleWindow, button, scroll_panel


class DevelopmentPoolWindow(ModuleWindow):
    def __init__(self, root, zoom_percent=100, parent=None):
        self.module, self.collection = store.MODULE, store.COLLECTION
        self.validate = store.validate
        self.current_id = None
        self.projects = []
        super().__init__(root, "Entwicklungspool · lokale Projekte", zoom_percent, parent)
        splitter = QSplitter()
        self.outer.addWidget(splitter, 1)
        left = QWidget()
        leftbox = QVBoxLayout(left)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Projektnamen und Beschreibungen suchen")
        self.search.textChanged.connect(self.render)
        leftbox.addWidget(self.search)
        self.filter = QComboBox()
        self.filter.addItems(["Alle", *store.STATES])
        self.filter.currentTextChanged.connect(self.render)
        leftbox.addWidget(self.filter)
        self.listing = QListWidget()
        self.listing.setAccessibleName("Gespeicherte Entwicklungsprojekte")
        self.listing.currentRowChanged.connect(self.choose)
        leftbox.addWidget(self.listing)
        button(leftbox, "Neues Projekt", self.new)
        splitter.addWidget(left)
        right, box = scroll_panel()
        splitter.addWidget(right)
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.WrapAllRows)
        box.addLayout(form)
        self.name = QLineEdit()
        self.name.setAccessibleName("Projektname")
        self.description = QTextEdit()
        self.description.setAcceptRichText(False)
        self.description.setMaximumHeight(150)
        self.description.setAccessibleName("Projektbeschreibung")
        self.project_status = QComboBox()
        self.project_status.addItems(store.STATES)
        form.addRow("Projektname", self.name)
        form.addRow("Beschreibung", self.description)
        form.addRow("Bearbeitungsstand", self.project_status)
        button(box, "Projekt speichern", self.save)
        button(box, "Arbeitsordner als sichere Kopie sichern", self.copy_current)
        button(box, "Arbeitsordner als ZIP exportieren", self.archive_current)
        box.addWidget(QLabel("Es werden nie Projekte automatisch gelöscht oder Dateien umbenannt."))
        self.files = QListWidget()
        self.files.setAccessibleName("Dateien des gewählten lokalen Projektordners")
        box.addWidget(self.files)
        self.refresh()
        self.finish()

    def snapshot(self):
        return (self.current_id, self.name.text(), self.description.toPlainText(),
                self.project_status.currentText())

    def load_state(self):
        return store.load(self.root)

    def import_copies(self, raw):
        # Sichere JSON-Metadaten sind nicht dasselbe wie ganze Arbeitsordner.
        # Ein separater Verzeichnisimport wird in der nächsten Iteration ergänzt.
        raise ValueError("Arbeitsordner können nur als vollständige ZIP-Kopie gesichert werden.")

    def import_data(self):
        QMessageBox.information(self, "Arbeitsordner geschützt",
                                "Ein automatischer Projektimport ist noch nicht freigegeben. "
                                "Nutze Export als ZIP oder sichere Arbeitskopien.")

    def refresh(self):
        try:
            self.projects = self.load_state()[self.collection]
            self.render()
            self.refresh_files()
        except (OSError, ValueError) as error:
            self.error("Projektpool nicht lesbar", error)

    def render(self):
        query = self.search.text().casefold()
        state = self.filter.currentText()
        with QSignalBlocker(self.listing):
            self.listing.clear()
            for row in self.projects:
                if (query not in (row["name"] + " " + row["description"]).casefold()
                        or state not in ("Alle", row["status"])):
                    continue
                item = QListWidgetItem(row["name"] + " · " + row["status"])
                item.setData(Qt.UserRole, row["id"])
                self.listing.addItem(item)

    def choose(self, index):
        item = self.listing.item(index)
        if item is None:
            return
        ident = item.data(Qt.UserRole)
        if not self.confirm_leave():
            return
        row = next((p for p in self.projects if p["id"] == ident), None)
        if row is None:
            return
        self.current_id = ident
        self.name.setText(row["name"])
        self.description.setPlainText(row["description"])
        self.project_status.setCurrentText(row["status"])
        self.refresh_files()
        self.remember()

    def refresh_files(self):
        self.files.clear()
        if self.current_id is None:
            return
        try:
            self.files.addItems(store.list_files(self.root, self.current_id))
        except (OSError, ValueError) as error:
            self.status.setText("Arbeitsordner nicht lesbar: " + str(error))

    def discard_draft(self):
        self.current_id = None
        self.name.clear()
        self.description.clear()
        self.project_status.setCurrentText("offen")
        self.files.clear()
        self.remember()

    def new(self):
        if self.confirm_leave():
            self.discard_draft()

    def save(self):
        try:
            ident = self.current_id or uuid4().hex
            row = store.put(self.root, {
                "id": ident, "name": self.name.text().strip(),
                "description": self.description.toPlainText(),
                "status": self.project_status.currentText(),
            })
            self.current_id = row["id"]
            self.refresh()
            self.remember()
            self.status.setText("Projekt und Arbeitsverzeichnis gespeichert.")
            return True
        except (OSError, ValueError) as error:
            self.error("Projekt nicht gespeichert", error)
            return False

    def copy_current(self):
        if self.current_id is None or not self.confirm_leave():
            return
        try:
            folder = store.copy_workspace(self.root, self.current_id)
            self.status.setText("Separate Arbeitskopie: " + str(folder))
        except (OSError, ValueError) as error:
            self.error("Arbeitskopie fehlgeschlagen", error)

    def archive_current(self):
        if self.current_id is None or not self.confirm_leave():
            return
        filename, _ = QFileDialog.getSaveFileName(
            self, "Neues ZIP-Archiv speichern", "projekt.zip", "ZIP (*.zip)")
        if not filename:
            return
        try:
            result = store.archive_workspace(self.root, self.current_id, filename)
            self.status.setText("Archiv vollständig geprüft: " + str(result))
        except (OSError, ValueError) as error:
            self.error("Archivierung fehlgeschlagen", error)
