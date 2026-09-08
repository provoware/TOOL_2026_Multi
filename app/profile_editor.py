"""PySide6-Editor für profilbasierte Genres, Stimmungen, Stil, Stimme und Besonderheiten."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QMessageBox, QPushButton, QVBoxLayout, QWidget,
)

from app.profile_store import CATEGORIES, add_profile, add_value, load_profiles, remove_value
from app.ui_standards import apply_global_style


class ProfileEditor(QDialog):
    """Verwaltet DB-Werte profilweise; Änderungen werden sofort atomar gespeichert."""

    def __init__(self, project_root: Path, zoom_percent: int = 100,
                 initial_category: str | None = None,
                 on_changed: Callable[[], None] | None = None,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self.zoom_percent = zoom_percent
        self.on_changed = on_changed
        self.setWindowTitle("DB-Eingaben · Profile")
        self.resize(760, 560)
        self.setMinimumSize(620, 460)
        self._build()
        apply_global_style(self, zoom_percent)
        self.refresh()
        if initial_category in CATEGORIES:
            self.category_combo.setCurrentText(initial_category)
        self._refresh_values()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        title = QLabel("DB-Eingaben mit Profilen")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)
        help_text = QLabel(
            "Jedes Profil besitzt eigene Genres, Stimmungen, Stil-, Stimmen- und Besonderheiten-Werte. "
            "Änderungen gelten nur für das ausgewählte Profil."
        )
        help_text.setWordWrap(True)
        layout.addWidget(help_text)

        form = QFormLayout()
        self.profile_combo = QComboBox()
        self.profile_combo.currentTextChanged.connect(self._refresh_values)
        form.addRow("Profil:", self.profile_combo)
        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        self.category_combo.currentTextChanged.connect(self._refresh_values)
        form.addRow("Bereich:", self.category_combo)
        layout.addLayout(form)

        new_profile_row = QHBoxLayout()
        self.profile_name_entry = QLineEdit()
        self.profile_name_entry.setPlaceholderText("Neues Profil, z. B. Ambient")
        new_profile_row.addWidget(self.profile_name_entry, 1)
        profile_button = QPushButton("Profil anlegen")
        profile_button.clicked.connect(self.create_profile)
        new_profile_row.addWidget(profile_button)
        layout.addLayout(new_profile_row)

        self.values_list = QListWidget()
        layout.addWidget(self.values_list, 1)

        value_row = QHBoxLayout()
        self.value_entry = QLineEdit()
        self.value_entry.setPlaceholderText("Neuen Wert eingeben …")
        self.value_entry.returnPressed.connect(self.create_value)
        value_row.addWidget(self.value_entry, 1)
        add_button = QPushButton("Wert hinzufügen")
        add_button.clicked.connect(self.create_value)
        value_row.addWidget(add_button)
        remove_button = QPushButton("Ausgewählten Wert entfernen")
        remove_button.clicked.connect(self.delete_selected_value)
        value_row.addWidget(remove_button)
        layout.addLayout(value_row)

        self.status_label = QLabel("Bereit.")
        self.status_label.setObjectName("muted")
        layout.addWidget(self.status_label)

        close_button = QPushButton("Schließen")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, 0, Qt.AlignRight)

    def set_zoom(self, percent: int) -> None:
        self.zoom_percent = percent
        apply_global_style(self, percent)

    def refresh(self) -> None:
        selected = self.profile_combo.currentText()
        try:
            profiles = load_profiles(self.project_root)
        except Exception as error:
            QMessageBox.critical(self, "Profildaten nicht lesbar", str(error))
            return
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        self.profile_combo.addItems(sorted(profiles, key=str.casefold))
        if selected in profiles:
            self.profile_combo.setCurrentText(selected)
        elif self.profile_combo.count():
            self.profile_combo.setCurrentIndex(0)
        self.profile_combo.blockSignals(False)
        self._refresh_values()

    def _refresh_values(self, *_args: object) -> None:
        self.values_list.clear()
        profile = self.profile_combo.currentText()
        category = self.category_combo.currentText()
        if not profile or category not in CATEGORIES:
            return
        try:
            values = load_profiles(self.project_root).get(profile, {}).get(category, [])
        except Exception as error:
            self.status_label.setText(f"Lesen fehlgeschlagen: {type(error).__name__}")
            return
        self.values_list.addItems(values)
        self.status_label.setText(f"{len(values)} Werte · {profile} · {category}")

    def _changed(self) -> None:
        self.refresh()
        if self.on_changed is not None:
            self.on_changed()

    def create_profile(self) -> None:
        try:
            name = add_profile(self.project_root, self.profile_name_entry.text())
        except Exception as error:
            QMessageBox.warning(self, "Profil nicht angelegt", str(error))
            return
        self.profile_name_entry.clear()
        self._changed()
        self.profile_combo.setCurrentText(name)
        self.status_label.setText(f"Profil {name} angelegt.")

    def create_value(self) -> None:
        profile = self.profile_combo.currentText()
        category = self.category_combo.currentText()
        try:
            value = add_value(self.project_root, profile, category, self.value_entry.text())
        except Exception as error:
            QMessageBox.warning(self, "Wert nicht gespeichert", str(error))
            return
        self.value_entry.clear()
        self._changed()
        self.status_label.setText(f"{value} gespeichert.")

    def delete_selected_value(self) -> None:
        item = self.values_list.currentItem()
        if item is None:
            QMessageBox.information(self, "Nichts ausgewählt", "Bitte zuerst einen Wert markieren.")
            return
        profile = self.profile_combo.currentText()
        category = self.category_combo.currentText()
        value = item.text()
        answer = QMessageBox.question(
            self, "Wert entfernen?",
            f"Soll „{value}“ aus {profile} / {category} entfernt werden?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        try:
            remove_value(self.project_root, profile, category, value)
        except Exception as error:
            QMessageBox.critical(self, "Wert nicht entfernt", str(error))
            return
        self._changed()
        self.status_label.setText(f"{value} entfernt.")
