"""Offline-Wiki mit Sammlungen, Suche, Textversionen und geprüften Artikelverweisen."""
from __future__ import annotations

from uuid import uuid4

from PySide6.QtCore import Qt, QSignalBlocker
from PySide6.QtWidgets import (
    QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMessageBox, QSplitter, QTextEdit, QVBoxLayout, QWidget,
)

from app import wiki_store as store
from app.module_widgets import ModuleWindow, button, scroll_panel


class WikiWindow(ModuleWindow):
    def __init__(self, root, zoom_percent=100, parent=None):
        self.module, self.collection, self.validate = store.MODULE, store.COLLECTION, store.validate
        self.current_id = None
        self.articles = []
        self.current_revisions = []
        super().__init__(root, "Wiki · lokale Wissenssammlungen", zoom_percent, parent)
        splitter = QSplitter()
        self.outer.addWidget(splitter, 1)
        left = QWidget()
        left_box = QVBoxLayout(left)
        self.bases = QComboBox()
        self.bases.setAccessibleName("Wissenssammlung")
        self.bases.currentTextChanged.connect(self.render)
        left_box.addWidget(self.bases)
        row = QHBoxLayout()
        self.new_base = QLineEdit()
        self.new_base.setPlaceholderText("Neue Sammlung")
        self.new_base.setAccessibleName("Name einer neuen Wissenssammlung")
        row.addWidget(self.new_base)
        button(row, "Anlegen", self.add_base)
        left_box.addLayout(row)
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Artikel durchsuchen")
        self.search_entry.textChanged.connect(self.render)
        left_box.addWidget(self.search_entry)
        self.listing = QListWidget()
        self.listing.setAccessibleName("Wissensartikel")
        self.listing.currentRowChanged.connect(self.select_article)
        left_box.addWidget(self.listing)
        button(left_box, "Neuer Artikel", self.new_article)
        button(left_box, "Artikel löschen", self.remove_article)
        splitter.addWidget(left)
        scroll, self.form_box = scroll_panel()
        splitter.addWidget(scroll)
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.WrapAllRows)
        self.form_box.addLayout(form)
        self.title_field = QLineEdit()
        self.title_field.setAccessibleName("Artikeltitel")
        form.addRow("Titel", self.title_field)
        self.content_field = QTextEdit()
        self.content_field.setAcceptRichText(False)
        self.content_field.setAccessibleName("Artikeltext")
        form.addRow("Text", self.content_field)
        self.tags_field = QLineEdit()
        self.tags_field.setAccessibleName("Schlagworte mit Komma trennen")
        form.addRow("Schlagworte", self.tags_field)
        self.links = QListWidget()
        self.links.setAccessibleName("Verknüpfte Wiki-Artikel auswählen")
        self.links.setMaximumHeight(170)
        form.addRow("Verknüpfungen (Häkchen)", self.links)
        self.form_box.addWidget(QLabel("Verknüpfungen bleiben lokal. Löschen verknüpfter Artikel wird verhindert."))
        button(self.form_box, "Artikel speichern", self.save)
        button(self.form_box, "Letzte Textfassung als Entwurf öffnen", self.restore_draft)
        self.refresh()
        self.finish()

    def snapshot(self):
        return (self.current_id, self.bases.currentText(), self.title_field.text(),
                self.content_field.toPlainText(), self.tags_field.text(),
                tuple(sorted(self._checked_links())))

    def _checked_links(self):
        return [self.links.item(i).data(Qt.UserRole) for i in range(self.links.count())
                if self.links.item(i).checkState() == Qt.Checked]

    def _populate_links(self, active=None):
        active = set(active or ())
        with QSignalBlocker(self.links):
            self.links.clear()
            for item in self.articles:
                if item["id"] == self.current_id:
                    continue
                entry = QListWidgetItem(f'{item["base"]} · {item["title"]}')
                entry.setData(Qt.UserRole, item["id"])
                entry.setFlags(entry.flags() | Qt.ItemIsUserCheckable)
                entry.setCheckState(Qt.Checked if item["id"] in active else Qt.Unchecked)
                self.links.addItem(entry)

    def load_state(self):
        return store.load(self.root)

    def import_copies(self, raw):
        return store.import_copies(self.root, raw)

    def refresh(self):
        try:
            state = self.load_state()
            self.articles = state["articles"]
            previous = self.bases.currentText()
            with QSignalBlocker(self.bases):
                self.bases.clear()
                self.bases.addItems(state["bases"])
                if previous in state["bases"]:
                    self.bases.setCurrentText(previous)
            self.render()
            current = next((item for item in self.articles if item["id"] == self.current_id), None)
            self._populate_links(current["links"] if current is not None else ())
            if current is not None:
                self.remember()
        except (OSError, ValueError) as error:
            self.error("Wiki konnte nicht geladen werden", error)

    def render(self):
        query = self.search_entry.text().casefold().strip()
        base = self.bases.currentText()
        with QSignalBlocker(self.listing):
            self.listing.clear()
            for article in self.articles:
                if article["base"] != base:
                    continue
                if query not in " ".join((article["title"], article["content"], " ".join(article["tags"]))).casefold():
                    continue
                item = QListWidgetItem(article["title"])
                item.setData(Qt.UserRole, article["id"])
                self.listing.addItem(item)

    def select_article(self, index):
        item = self.listing.item(index)
        if item is None:
            return
        selected_id = item.data(Qt.UserRole)
        if not self.confirm_leave():
            with QSignalBlocker(self.listing):
                self.listing.setCurrentRow(-1)
            return
        # Bestätigung mit "Speichern" kann die Liste neu laden und das alte
        # Qt-Item zerstören; die Kennung muss deshalb vorab gesichert sein.
        match = next((a for a in self.articles if a["id"] == selected_id), None)
        if match is None:
            return
        self.current_id = match["id"]
        self.current_revisions = match["revisions"]
        self.title_field.setText(match["title"])
        self.content_field.setPlainText(match["content"])
        self.tags_field.setText(", ".join(match["tags"]))
        self._populate_links(match["links"])
        self.remember()

    def discard_draft(self):
        self.current_id = None
        self.current_revisions = []
        self.title_field.clear()
        self.content_field.clear()
        self.tags_field.clear()
        self._populate_links()
        self.remember()

    def new_article(self):
        if self.confirm_leave():
            self.discard_draft()

    def add_base(self):
        if not self.confirm_leave():
            return
        try:
            value = store.add_base(self.root, self.new_base.text())
            self.refresh()
            self.bases.setCurrentText(value)
            self.new_base.clear()
            self.discard_draft()
        except (ValueError, OSError) as error:
            self.error("Wissenssammlung nicht angelegt", error)

    def form_record(self):
        tags = list(dict.fromkeys(x.strip() for x in self.tags_field.text().split(",") if x.strip()))
        return {"id": self.current_id or uuid4().hex,
                "base": self.bases.currentText(), "title": self.title_field.text().strip(),
                "content": self.content_field.toPlainText(), "tags": tags,
                "links": self._checked_links(), "revisions": list(self.current_revisions)}

    def save(self):
        try:
            article = store.put(self.root, self.form_record())
            self.current_id = article["id"]
            self.current_revisions = article["revisions"]
            self.remember()
            self.refresh()
            self.status.setText("Wissensartikel sicher gespeichert.")
            return True
        except (ValueError, OSError) as error:
            self.error("Wissensartikel nicht gespeichert", error)
            return False

    def remove_article(self):
        if self.current_id is None:
            return
        if QMessageBox.question(
            self, "Wissensartikel entfernen", "Artikel wirklich löschen?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        ) != QMessageBox.Yes:
            return
        try:
            store.remove(self.root, self.current_id)
            self.discard_draft()
            self.refresh()
        except (ValueError, OSError) as error:
            self.error("Artikel wurde nicht entfernt", error)

    def restore_draft(self):
        if not self.current_revisions:
            self.status.setText("Keine ältere Fassung vorhanden.")
            return
        if QMessageBox.question(
            self, "Frühere Fassung", "Die vorherige Textfassung als ungespeicherten Entwurf öffnen?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        ) == QMessageBox.Yes:
            self.content_field.setPlainText(self.current_revisions[-1]["content"])
            self.status.setText("Ältere Fassung als Entwurf geladen. Zum Übernehmen speichern.")
