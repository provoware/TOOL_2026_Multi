"""Eigenständiger allgemeiner Texteditor mit Titel-Dateiname und Abschlussnotizen."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMessageBox, QPushButton, QSplitter, QTextEdit, QVBoxLayout, QWidget,
)

from app.character_store import character_marker, character_options
from app.text_editor_store import TextDocument, list_text_documents, load_text_document, save_text_document
from app.ui_standards import SPACING, apply_global_style

AUTOSAVE_MS = 5 * 60 * 1000


class TextEditorWindow(QWidget):
    """Farbig unterstützte, allgemeine Schreibfläche mit sicherer lokaler Speicherung."""

    def __init__(self, project_root: Path, zoom_percent: int = 100,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.Window)
        self.project_root = project_root
        self.zoom_percent = zoom_percent
        self.document = TextDocument()
        self.current_path: Path | None = None
        self.setWindowTitle("Texteditor")
        self.resize(1120, 760)
        self.setMinimumSize(820, 560)
        self._build()
        apply_global_style(self, zoom_percent)
        self.refresh()
        self.new_document()
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self.save)
        QShortcut(QKeySequence("Escape"), self, activated=self.close)
        self.autosave_timer = QTimer(self)
        self.autosave_timer.setInterval(AUTOSAVE_MS)
        self.autosave_timer.timeout.connect(self._autosave)
        self.autosave_timer.start()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACING["m"], SPACING["m"], SPACING["m"], SPACING["m"])
        outer.setSpacing(SPACING["s"])

        header = QHBoxLayout()
        title = QLabel("Texteditor")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch(1)
        new_button = QPushButton("Neuer Text")
        new_button.clicked.connect(self.new_document)
        header.addWidget(new_button)
        self.save_button = QPushButton("Jetzt speichern")
        self.save_button.setObjectName("primaryButton")
        self.save_button.clicked.connect(self.save)
        header.addWidget(self.save_button)
        close_button = QPushButton("Editor schließen")
        close_button.clicked.connect(self.close)
        header.addWidget(close_button)
        outer.addLayout(header)

        hint = QLabel(
            "Der Titel bestimmt automatisch den Dateinamen. Text und Abschlussnotizen werden strukturiert und atomar gespeichert. Strg+S speichert sofort."
        )
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        outer.addWidget(hint)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        left = QFrame()
        left.setObjectName("innerCard")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(SPACING["s"], SPACING["s"], SPACING["s"], SPACING["s"])
        left_layout.setSpacing(SPACING["s"])
        left_layout.addWidget(QLabel("Gespeicherte Texte"))
        self.file_list = QListWidget()
        self.file_list.setObjectName("editor_document_list")
        self.file_list.currentItemChanged.connect(self._load_selected)
        left_layout.addWidget(self.file_list, 1)
        refresh_button = QPushButton("Liste aktualisieren")
        refresh_button.clicked.connect(self.refresh)
        left_layout.addWidget(refresh_button)
        splitter.addWidget(left)

        work = QFrame()
        work.setObjectName("card")
        work_layout = QVBoxLayout(work)
        work_layout.setContentsMargins(SPACING["m"], SPACING["m"], SPACING["m"], SPACING["m"])
        work_layout.setSpacing(SPACING["s"])

        title_row = QHBoxLayout()
        title_row.addWidget(QLabel("Titel / Dateiname:"))
        self.title_entry = QLineEdit()
        self.title_entry.setPlaceholderText("Titel des Textes")
        self.title_entry.textChanged.connect(self._update_window_title)
        title_row.addWidget(self.title_entry, 1)
        work_layout.addLayout(title_row)

        character_row = QHBoxLayout()
        character_row.addWidget(QLabel("Charakterfibel:"))
        self.character_combo = QComboBox()
        self.character_combo.setObjectName("editor_character_selector")
        self.character_combo.setToolTip("Charaktere stammen direkt aus der zentralen Charakterfibel.")
        character_row.addWidget(self.character_combo, 1)
        insert_character = QPushButton("Charakter in Text einfügen")
        insert_character.clicked.connect(self.insert_character_reference)
        character_row.addWidget(insert_character)
        work_layout.addLayout(character_row)

        text_label = QLabel("Text")
        text_label.setObjectName("cardTitle")
        work_layout.addWidget(text_label)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Hier schreiben …")
        work_layout.addWidget(self.text_edit, 1)

        notes_label = QLabel("Abschließende Notizen")
        notes_label.setObjectName("cardTitle")
        work_layout.addWidget(notes_label)
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Notizen, offene Punkte, nächste Bearbeitungsschritte …")
        self.notes_edit.setMaximumHeight(150)
        work_layout.addWidget(self.notes_edit)
        splitter.addWidget(work)
        splitter.setSizes([280, 820])
        outer.addWidget(splitter, 1)

        self.status_label = QLabel("Bereit · Titel eingeben und schreiben.")
        self.status_label.setObjectName("muted")
        outer.addWidget(self.status_label)

    def set_zoom(self, percent: int) -> None:
        self.zoom_percent = percent
        apply_global_style(self, percent)

    def _update_window_title(self, *_args: object) -> None:
        title = self.title_entry.text().strip() if hasattr(self, "title_entry") else ""
        self.setWindowTitle(f"Texteditor – {title}" if title else "Texteditor")

    def refresh_characters(self) -> None:
        selected = self.character_combo.currentData()
        self.character_combo.blockSignals(True)
        self.character_combo.clear()
        self.character_combo.addItem("Charakter auswählen …", "")
        try:
            options = character_options(self.project_root)
        except Exception:
            options = []
        for option in options:
            self.character_combo.addItem(option.label, option.character_id)
        if selected:
            index = self.character_combo.findData(selected)
            if index >= 0:
                self.character_combo.setCurrentIndex(index)
        self.character_combo.blockSignals(False)

    def refresh(self) -> None:
        selected_path = str(self.current_path) if self.current_path else ""
        self.file_list.blockSignals(True)
        self.file_list.clear()
        try:
            paths = list_text_documents(self.project_root)
        except Exception as error:
            self.file_list.blockSignals(False)
            self.status_label.setText(f"Textliste nicht lesbar · nichts verändert. Grund: {error}")
            return
        selected_row = -1
        for row, path in enumerate(paths):
            try:
                document = load_text_document(path)
                label = document.title
            except Exception:
                label = f"⚠ {path.stem}"
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, str(path))
            self.file_list.addItem(item)
            if str(path) == selected_path:
                selected_row = row
        self.file_list.blockSignals(False)
        if selected_row >= 0:
            self.file_list.setCurrentRow(selected_row)
        self.refresh_characters()

    def new_document(self) -> None:
        self.current_path = None
        self.document = TextDocument()
        self.file_list.clearSelection()
        self.title_entry.setText("")
        self.text_edit.clear()
        self.notes_edit.clear()
        self.status_label.setText("Neuer Text · der Titel wird beim Speichern zum Dateinamen.")
        self.title_entry.setFocus()

    def _load_selected(self, current: QListWidgetItem | None, _previous: QListWidgetItem | None) -> None:
        if current is None:
            return
        path = Path(str(current.data(Qt.UserRole)))
        try:
            document = load_text_document(path)
        except Exception as error:
            QMessageBox.critical(self, "Text nicht lesbar", f"Es wurde nichts verändert.\n\nGrund: {error}")
            return
        self.current_path = path
        self.document = document
        self.title_entry.setText(document.title)
        self.text_edit.setPlainText(document.text)
        self.notes_edit.setPlainText(document.notes)
        self.status_label.setText(f"„{document.title}“ geladen.")

    def insert_character_reference(self) -> None:
        character_id = str(self.character_combo.currentData() or "")
        if not character_id:
            QMessageBox.information(self, "Kein Charakter ausgewählt", "Bitte zuerst einen Charakter aus der Charakterfibel auswählen.")
            return
        try:
            marker = character_marker(self.project_root, character_id)
        except ValueError as error:
            self.refresh_characters()
            QMessageBox.information(self, "Charakter nicht mehr verfügbar", str(error))
            return
        if character_id not in self.document.character_ids:
            self.document.character_ids.append(character_id)
        cursor = self.text_edit.textCursor()
        cursor.insertText(marker)
        self.text_edit.setTextCursor(cursor)
        self.status_label.setText(f"Charakterreferenz „{marker}“ eingefügt.")

    def save(self) -> Path | None:
        title = self.title_entry.text().strip()
        if not title:
            QMessageBox.information(self, "Titel fehlt", "Bitte zuerst einen Titel eingeben. Er wird als Dateiname verwendet.")
            self.title_entry.setFocus()
            return None
        self.document.title = title
        self.document.text = self.text_edit.toPlainText()
        self.document.notes = self.notes_edit.toPlainText()
        try:
            target = save_text_document(self.project_root, self.document, self.current_path)
        except Exception as error:
            QMessageBox.critical(self, "Text nicht gespeichert", f"Der bisherige gespeicherte Stand bleibt erhalten.\n\nGrund: {error}")
            return None
        self.current_path = target
        self.refresh()
        self.status_label.setText(f"● Gespeichert: {target.name}")
        return target

    def _autosave(self) -> None:
        if self.title_entry.text().strip():
            self.save()
