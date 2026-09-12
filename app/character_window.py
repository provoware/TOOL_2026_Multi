"""Eigenständiges PySide6-Modul zum Erstellen und Pflegen konsistenter Charaktere."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMessageBox, QPushButton, QScrollArea, QSplitter, QTextEdit, QVBoxLayout, QWidget,
)

from app.character_store import get_character, list_characters, upsert_character
from app.ui_standards import SPACING, apply_global_style


class CharacterWindow(QWidget):
    """Charakterfibel mit suchbarer Liste und strukturiertem Detailformular."""

    MULTILINE_FIELDS = (
        ("appearance", "Aussehen", "Äußeres, Kleidung, besondere Merkmale …"),
        ("personality", "Persönlichkeit", "Eigenschaften, Widersprüche, Gewohnheiten …"),
        ("motivation", "Ziele & Motivation", "Was treibt die Figur an? Was will sie erreichen?"),
        ("background", "Hintergrund", "Biografie, Herkunft, prägende Ereignisse …"),
        ("relationships", "Beziehungen", "Familie, Freunde, Konflikte, Abhängigkeiten …"),
        ("speech", "Sprache & Stimme", "Wortwahl, Tonfall, typische Sätze, Akzent …"),
        ("strengths", "Stärken", "Fähigkeiten, Ressourcen, positive Eigenschaften …"),
        ("weaknesses", "Schwächen", "Ängste, Grenzen, Fehler, innere Konflikte …"),
        ("notes", "Notizen", "Offene Punkte, Entwicklung, Kontinuitätshinweise …"),
    )

    def __init__(self, project_root: Path, zoom_percent: int = 100,
                 on_changed: Callable[[], None] | None = None,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.Window)
        self.project_root = project_root
        self.zoom_percent = zoom_percent
        self.on_changed = on_changed
        self.current_id: str | None = None
        self.setWindowTitle("Charakterfibel")
        self.resize(1080, 760)
        self.setMinimumSize(820, 560)
        self._build()
        apply_global_style(self, zoom_percent)
        self.refresh()
        self.name_entry.setFocus()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACING["m"], SPACING["m"], SPACING["m"], SPACING["m"])
        outer.setSpacing(SPACING["s"])

        header = QHBoxLayout()
        title = QLabel("Charakterfibel")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch(1)
        new_button = QPushButton("Neuen Charakter anlegen")
        new_button.setObjectName("primaryButton")
        new_button.clicked.connect(self.new_character)
        header.addWidget(new_button)
        close_button = QPushButton("Charakterfibel schließen")
        close_button.clicked.connect(self.close)
        header.addWidget(close_button)
        outer.addLayout(header)

        hint = QLabel(
            "Lege Figuren einmal strukturiert an. Andere Module können diese Charakterdaten über die zentrale Charakterdatenbank wiederverwenden."
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
        left_layout.addWidget(QLabel("Charaktere finden"))
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Name, Rolle, Eigenschaft oder Tag …")
        self.search_entry.textChanged.connect(self.refresh)
        left_layout.addWidget(self.search_entry)
        self.character_list = QListWidget()
        self.character_list.setObjectName("character_list")
        self.character_list.currentItemChanged.connect(self._selection_changed)
        left_layout.addWidget(self.character_list, 1)
        splitter.addWidget(left)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        form_host = QFrame()
        form_host.setObjectName("card")
        form_layout = QVBoxLayout(form_host)
        form_layout.setContentsMargins(SPACING["m"], SPACING["m"], SPACING["m"], SPACING["m"])
        form_layout.setSpacing(SPACING["s"])

        section = QLabel("Charakterdetails")
        section.setObjectName("cardTitle")
        form_layout.addWidget(section)
        basic = QFormLayout()
        basic.setSpacing(SPACING["s"])
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Name des Charakters")
        basic.addRow("Name *", self.name_entry)
        self.role_entry = QLineEdit()
        self.role_entry.setPlaceholderText("z. B. Hauptfigur, Gegenspieler, Mentor …")
        basic.addRow("Rolle", self.role_entry)
        self.age_entry = QLineEdit()
        self.age_entry.setPlaceholderText("Alter oder Altersbeschreibung")
        basic.addRow("Alter", self.age_entry)
        self.tags_entry = QLineEdit()
        self.tags_entry.setPlaceholderText("Tags mit Komma trennen")
        basic.addRow("Tags", self.tags_entry)
        form_layout.addLayout(basic)

        self.text_fields: dict[str, QTextEdit] = {}
        for key, label, placeholder in self.MULTILINE_FIELDS:
            field_label = QLabel(label)
            field_label.setObjectName("muted")
            form_layout.addWidget(field_label)
            editor = QTextEdit()
            editor.setPlaceholderText(placeholder)
            editor.setMinimumHeight(78 if key != "notes" else 96)
            self.text_fields[key] = editor
            form_layout.addWidget(editor)

        actions = QHBoxLayout()
        actions.addStretch(1)
        self.save_button = QPushButton("Charakter speichern")
        self.save_button.setObjectName("primaryButton")
        self.save_button.clicked.connect(self.save_character)
        actions.addWidget(self.save_button)
        form_layout.addLayout(actions)
        scroll.setWidget(form_host)
        splitter.addWidget(scroll)
        splitter.setSizes([300, 760])
        outer.addWidget(splitter, 1)

        self.status_label = QLabel("Bereit · neuen Charakter anlegen oder links auswählen.")
        self.status_label.setObjectName("muted")
        outer.addWidget(self.status_label)

    def set_zoom(self, percent: int) -> None:
        self.zoom_percent = percent
        apply_global_style(self, percent)

    def refresh(self, *_args: object) -> None:
        selected_id = self.current_id
        try:
            characters = list_characters(self.project_root, self.search_entry.text())
        except Exception as error:
            self.status_label.setText(f"Charaktere konnten nicht gelesen werden · nichts verändert. Grund: {error}")
            return
        self.character_list.blockSignals(True)
        self.character_list.clear()
        selected_row = -1
        for row, character in enumerate(characters):
            role = str(character.get("role") or "").strip()
            text = f"{character['name']}\n{role}" if role else str(character["name"])
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, str(character["id"]))
            self.character_list.addItem(item)
            if character["id"] == selected_id:
                selected_row = row
        self.character_list.blockSignals(False)
        if selected_row >= 0:
            self.character_list.setCurrentRow(selected_row)
        self.status_label.setText(f"{len(characters)} Charakter(e) angezeigt.")

    def _selection_changed(self, current: QListWidgetItem | None, _previous: QListWidgetItem | None) -> None:
        if current is None:
            return
        character_id = str(current.data(Qt.UserRole) or "")
        try:
            character = get_character(self.project_root, character_id)
        except Exception as error:
            QMessageBox.critical(self, "Charakter nicht lesbar", f"Es wurde nichts verändert.\n\nGrund: {error}")
            return
        if character is None:
            return
        self.current_id = character_id
        self.name_entry.setText(str(character["name"]))
        self.role_entry.setText(str(character.get("role") or ""))
        self.age_entry.setText(str(character.get("age") or ""))
        self.tags_entry.setText(", ".join(str(tag) for tag in character.get("tags", [])))
        for key, editor in self.text_fields.items():
            editor.setPlainText(str(character.get(key) or ""))
        self.status_label.setText(f"„{character['name']}“ geladen.")

    def new_character(self) -> None:
        self.current_id = None
        self.character_list.clearSelection()
        self.name_entry.clear()
        self.role_entry.clear()
        self.age_entry.clear()
        self.tags_entry.clear()
        for editor in self.text_fields.values():
            editor.clear()
        self.status_label.setText("Neuer Charakter · Name eintragen und Details ergänzen.")
        self.name_entry.setFocus()

    def save_character(self) -> None:
        values: dict[str, object] = {
            "name": self.name_entry.text(),
            "role": self.role_entry.text(),
            "age": self.age_entry.text(),
            "tags": self.tags_entry.text(),
        }
        values.update({key: editor.toPlainText() for key, editor in self.text_fields.items()})
        try:
            saved = upsert_character(self.project_root, values, self.current_id)
        except Exception as error:
            QMessageBox.warning(self, "Charakter nicht gespeichert", f"Der bisherige Datenbestand bleibt erhalten.\n\nGrund: {error}")
            return
        self.current_id = str(saved["id"])
        self.refresh()
        self.status_label.setText(f"● „{saved['name']}“ sicher gespeichert.")
        if self.on_changed is not None:
            self.on_changed()
