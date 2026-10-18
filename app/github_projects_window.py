"""Übersichtliche Offline-Verwaltung offener und fertiger GitHub-Projekte."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QSignalBlocker
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QPushButton,
    QSplitter, QTextEdit, QVBoxLayout, QWidget,
)

from app.github_projects import (
    delete_project, export_projects, import_projects, load_projects, upsert_project,
)
from app.ui_standards import apply_global_style


class GitHubProjectsWindow(QWidget):
    """Projektregister, kein GitHub-Synchronisations- oder Statistikmodul."""

    def __init__(self, root: Path, zoom_percent: int = 100, parent: QWidget | None = None):
        super().__init__(parent, Qt.Window)
        self.root, self.zoom_percent = root, zoom_percent
        self._current_id: str | None = None
        self._baseline = None
        self.setWindowTitle("GitHub-Projekte · Übersicht und Notizen")
        self.resize(1080, 740)
        self.setMinimumSize(780, 550)
        self._build()
        self.set_zoom(zoom_percent)
        self.refresh()

    @staticmethod
    def _button(layout, text, handler):
        button = QPushButton(text)
        button.clicked.connect(handler)
        layout.addWidget(button)
        return button

    def _build(self):
        outer = QVBoxLayout(self)
        heading = QLabel("GitHub-Projekte · offene und abgeschlossene Arbeiten")
        heading.setObjectName("sectionTitle")
        outer.addWidget(heading)
        info = QLabel("Lokale Übersicht: Hier werden keine GitHub-Daten automatisch heruntergeladen.")
        info.setWordWrap(True)
        outer.addWidget(info)
        splitter = QSplitter(Qt.Horizontal)
        left = QFrame()
        left.setObjectName("innerCard")
        l = QVBoxLayout(left)
        l.addWidget(QLabel("Gespeicherte Projekte"))
        self.search = QLineEdit()
        self.search.setPlaceholderText("Projektname oder Repository suchen …")
        self.search.textChanged.connect(self._refresh_list)
        l.addWidget(self.search)
        self.filter_status = QComboBox()
        self.filter_status.addItems(("Alle Projekte", "Offen", "Fertig"))
        self.filter_status.currentIndexChanged.connect(self._refresh_list)
        l.addWidget(self.filter_status)
        self.list = QListWidget()
        self.list.setAccessibleName("Projektliste – offen und abgeschlossen")
        self.list.currentItemChanged.connect(self._selected)
        l.addWidget(self.list, 1)
        self.count = QLabel("0 Projekte")
        l.addWidget(self.count)
        splitter.addWidget(left)

        right = QFrame()
        right.setObjectName("innerCard")
        r = QVBoxLayout(right)
        r.addWidget(QLabel("Projektdaten · Eingabe und Bearbeitung"))
        form = QFormLayout()
        self.project = QLineEdit()
        self.project.setPlaceholderText("Projektbezeichnung, z. B. VideoBatchTool")
        self.project.setAccessibleName("Projektname")
        form.addRow("Projektname:", self.project)
        self.repo = QLineEdit()
        self.repo.setPlaceholderText("Eigentümer/Repository, z. B. provoware/Projekt")
        self.repo.setAccessibleName("GitHub Repository Name mit Eigentümer")
        form.addRow("GitHub-Name:", self.repo)
        self.url = QLineEdit()
        self.url.setPlaceholderText("https://github.com/Eigentümer/Repository")
        self.url.setAccessibleName("GitHub Repository URL")
        form.addRow("GitHub-URL:", self.url)
        self.status_combo = QComboBox()
        self.status_combo.addItems(("Offen", "Fertig"))
        form.addRow("Projektstand:", self.status_combo)
        r.addLayout(form)
        self.notes = QTextEdit()
        self.notes.setAccessibleName("Freie Projektnotizen")
        self.notes.setPlaceholderText("Stand, nächste Schritte, Besonderheiten, hilfreiche Informationen …")
        r.addWidget(QLabel("Notizen (frei erweiterbar):"))
        r.addWidget(self.notes, 1)
        r.addWidget(QLabel("Optionale Aufgaben · Häkchen bedeutet erledigt"))
        self.todo_list = QListWidget()
        self.todo_list.setAccessibleName("Projektaufgaben, einzeln abhaken")
        r.addWidget(self.todo_list, 1)
        row = QHBoxLayout()
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Neue Aufgabe …")
        self.todo_input.returnPressed.connect(self.add_todo)
        row.addWidget(self.todo_input, 1)
        self._button(row, "Aufgabe hinzufügen", self.add_todo)
        self._button(row, "Aufgabe entfernen", self.remove_todo)
        r.addLayout(row)
        actions = QHBoxLayout()
        self._button(actions, "Neu", self.new_project)
        self._button(actions, "Speichern", self.save_current)
        self._button(actions, "Projekt entfernen", self.delete_current)
        r.addLayout(actions)
        copy = QHBoxLayout()
        self._button(copy, "Projektname kopieren", lambda: self._copy(self.project.text()))
        self._button(copy, "GitHub-Name kopieren", lambda: self._copy(self.repo.text()))
        self._button(copy, "URL kopieren", lambda: self._copy(self.url.text()))
        r.addLayout(copy)
        exchange = QHBoxLayout()
        self._button(exchange, "JSON exportieren", self.export_data)
        self._button(exchange, "JSON importieren", self.import_data)
        r.addLayout(exchange)
        splitter.addWidget(right)
        splitter.setSizes((320, 750))
        outer.addWidget(splitter, 1)
        self.message = QLabel("Bereit. Projekte bleiben ausschließlich auf diesem Rechner.")
        self.message.setWordWrap(True)
        outer.addWidget(self.message)

    def set_zoom(self, percent: int):
        self.zoom_percent = percent
        apply_global_style(self, percent)

    def _error(self, title, error):
        self.message.setText(f"{title}: {error}. Die bisherigen Daten bleiben erhalten.")
        QMessageBox.warning(self, title, f"Es wurde nichts verändert.\n\nGrund: {error}")

    def _fields(self):
        return (self.project.text(), self.repo.text(), self.url.text(),
                self.notes.toPlainText(), self.status_combo.currentIndex(),
                tuple((self.todo_list.item(i).text(),
                       self.todo_list.item(i).checkState() == Qt.Checked)
                      for i in range(self.todo_list.count())))

    def _may_discard(self):
        if self._baseline is None or self._fields() == self._baseline:
            return True
        return QMessageBox.question(
            self, "Ungespeicherte Änderungen",
            "Änderungen sind noch nicht gespeichert. Eingaben wirklich verwerfen?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        ) == QMessageBox.Yes

    def _fill(self, entry=None):
        entry = entry or {}
        self._current_id = entry.get("id")
        self.project.setText(entry.get("project", ""))
        self.repo.setText(entry.get("repo", ""))
        self.url.setText(entry.get("url", ""))
        self.notes.setPlainText(entry.get("notes", ""))
        self.status_combo.setCurrentIndex(1 if entry.get("status") == "fertig" else 0)
        self.todo_list.clear()
        for todo in entry.get("todos", []):
            self._append_todo(todo["text"], todo["done"])
        self._baseline = self._fields()

    def _append_todo(self, text, done=False):
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        item.setCheckState(Qt.Checked if done else Qt.Unchecked)
        self.todo_list.addItem(item)

    def add_todo(self):
        text = self.todo_input.text().strip()
        if not text:
            self.message.setText("Bitte einen Aufgabentext eingeben.")
            return
        if any(self.todo_list.item(i).text().casefold() == text.casefold()
               for i in range(self.todo_list.count())):
            self.message.setText("Diese Aufgabe steht bereits in der Liste.")
            return
        self._append_todo(text)
        self.todo_input.clear()

    def remove_todo(self):
        row = self.todo_list.currentRow()
        if row >= 0:
            self.todo_list.takeItem(row)

    def _refresh_list(self):
        try:
            entries = load_projects(self.root)
        except Exception as exc:
            self._error("Projektliste nicht lesbar", exc)
            return
        ident = self._current_id
        with QSignalBlocker(self.list):
            self.list.clear()
            state = self.filter_status.currentIndex()
            needle = self.search.text().casefold()
            filtered = sorted(entries, key=lambda p: (
                p["status"] == "fertig", p["project"].casefold()))
            for entry in filtered:
                if state == 1 and entry["status"] != "offen":
                    continue
                if state == 2 and entry["status"] != "fertig":
                    continue
                if needle not in (entry["project"] + " " + entry["repo"]).casefold():
                    continue
                label = ("✓ Fertig · " if entry["status"] == "fertig" else "○ Offen · ")
                item = QListWidgetItem(label + entry["project"] + " | " + entry["repo"])
                item.setData(Qt.UserRole, entry["id"])
                self.list.addItem(item)
                if ident == entry["id"]:
                    self.list.setCurrentItem(item)
        self.count.setText(
            f"{len(entries)} Projekte insgesamt · "
            f"{sum(p['status'] == 'offen' for p in entries)} offen · "
            f"{sum(p['status'] == 'fertig' for p in entries)} fertig"
        )

    def refresh(self):
        self._refresh_list()

    def _selected(self, current, previous):
        if current is None:
            return
        if not self._may_discard():
            with QSignalBlocker(self.list):
                self.list.setCurrentItem(previous)
            return
        ident = current.data(Qt.UserRole)
        try:
            record = next(p for p in load_projects(self.root) if p["id"] == ident)
        except Exception as exc:
            self._error("Projekt konnte nicht geöffnet werden", exc)
            return
        self._fill(record)

    def new_project(self):
        if not self._may_discard():
            return
        with QSignalBlocker(self.list):
            self.list.setCurrentRow(-1)
        self._fill()
        self.message.setText("Neues Projekt: Namen, GitHub-Daten und Status eingeben.")

    def save_current(self):
        todos = [{"text": self.todo_list.item(i).text(),
                  "done": self.todo_list.item(i).checkState() == Qt.Checked}
                 for i in range(self.todo_list.count())]
        try:
            saved = upsert_project(
                self.root, ident=self._current_id,
                project=self.project.text(), repo=self.repo.text(), url=self.url.text(),
                notes=self.notes.toPlainText(),
                status=("fertig" if self.status_combo.currentIndex() else "offen"),
                todos=todos)
        except Exception as exc:
            self._error("Projekt nicht gespeichert", exc)
            return
        self._fill(saved)
        self._refresh_list()
        self.message.setText(f"Projekt „{saved['project']}“ sicher gespeichert.")

    def delete_current(self):
        if not self._current_id:
            self.message.setText("Bitte zuerst ein gespeichertes Projekt auswählen.")
            return
        if QMessageBox.question(
            self, "Projekt entfernen", "Dieses Projekt aus der lokalen Übersicht entfernen?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        ) != QMessageBox.Yes:
            return
        try:
            delete_project(self.root, self._current_id)
        except Exception as exc:
            self._error("Entfernen fehlgeschlagen", exc)
            return
        self._fill()
        self._refresh_list()

    def _copy(self, text):
        if not text.strip():
            self.message.setText("Hier ist noch kein Wert zum Kopieren eingetragen.")
            return
        QApplication.clipboard().setText(text.strip())
        self.message.setText("Wert in die Zwischenablage kopiert.")

    def export_data(self):
        target, _ = QFileDialog.getSaveFileName(self, "Projekte exportieren",
                                                "github-projekte.json", "JSON-Dateien (*.json)")
        if not target:
            return
        try:
            export_projects(self.root, Path(target))
        except Exception as exc:
            self._error("Export fehlgeschlagen", exc)
            return
        self.message.setText("Projektliste als JSON exportiert.")

    def import_data(self):
        if not self._may_discard():
            return
        source, _ = QFileDialog.getOpenFileName(self, "Projekte importieren", "",
                                                "JSON-Dateien (*.json)")
        if not source:
            return
        try:
            count = import_projects(self.root, Path(source))
        except Exception as exc:
            self._error("Import fehlgeschlagen", exc)
            return
        self._fill()
        self._refresh_list()
        self.message.setText(f"{count} neue Projekte importiert; bestehende unverändert.")

    def closeEvent(self, event):
        if not self._may_discard():
            event.ignore()
            return
        event.accept()
