"""Einheitliche, signalgeschützte Charakterauswahl in Schreibfenstern."""

from pathlib import Path

from PySide6.QtCore import QSignalBlocker
from PySide6.QtWidgets import QComboBox

from app.character_store import character_options


def refresh_character_combo(combo: QComboBox, project_root: Path) -> None:
    """Aktualisiert Figuren und erhält eine weiterhin vorhandene Auswahl."""
    selected = combo.currentData()
    with QSignalBlocker(combo):
        combo.clear()
        combo.addItem("Charakter auswählen …", "")
        try:
            options = character_options(project_root)
        except Exception:
            options = []
        for option in options:
            combo.addItem(option.label, option.character_id)
        if selected:
            index = combo.findData(selected)
            if index >= 0:
                combo.setCurrentIndex(index)
