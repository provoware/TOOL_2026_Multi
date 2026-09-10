"""Sichere, explizite Prüfung der benötigten Provoware-Arbeitsordner."""

from __future__ import annotations

import tempfile
from collections.abc import Callable
from pathlib import Path

REQUIRED_SUBDIRS = ("daten", "logs", "berichte", "backups")


def required_paths(root: Path) -> tuple[Path, ...]:
    return (root, *(root / name for name in REQUIRED_SUBDIRS))


def missing_paths(root: Path) -> tuple[Path, ...]:
    return tuple(path for path in required_paths(root) if not path.exists())


def _verify_directory(path: Path) -> None:
    if not path.is_dir():
        raise NotADirectoryError(f"Kein Ordner: {path}")
    try:
        with tempfile.NamedTemporaryFile(prefix=".provoware-schreibtest-", dir=path, delete=True):
            pass
    except OSError as error:
        raise PermissionError(f"Ordner ist nicht beschreibbar: {path}") from error


def ensure_runtime_folders(root: Path, ask_create: Callable[[tuple[Path, ...]], bool]) -> bool:
    """Prüft/erstellt fehlende Ordner nur nach ausdrücklicher Zustimmung.

    Bereits vorhandene Ordner werden nicht verändert. Bei Ablehnung bleibt das
    Dateisystem unverändert. Nach einer Erstellung wird jeder benötigte Ordner
    mit einem sofort wieder entfernten Temp-Schreibtest validiert.
    """
    missing = missing_paths(root)
    if missing:
        if not ask_create(missing):
            return False
        root.mkdir(parents=True, exist_ok=True)
        for name in REQUIRED_SUBDIRS:
            (root / name).mkdir(parents=True, exist_ok=True)
    for path in required_paths(root):
        _verify_directory(path)
    return True


def ensure_runtime_folders_gui(root: Path) -> bool:
    """Qt-Dialog für die Startvalidierung; importiert Qt erst bei GUI-Nutzung."""
    missing = missing_paths(root)

    def ask(paths: tuple[Path, ...]) -> bool:
        from PySide6.QtWidgets import QMessageBox

        shown = "\n".join(f"• {path}" for path in paths)
        answer = QMessageBox.question(
            None,
            "Provoware-Ordner vorbereiten?",
            "Für einen sicheren Start fehlen benötigte Arbeitsordner.\n\n"
            f"Diese Ordner sollen angelegt werden:\n{shown}\n\n"
            "Vorhandene Dateien werden dabei nicht überschrieben. Soll Provoware die fehlenden Ordner jetzt erstellen?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return answer == QMessageBox.Yes

    if not missing:
        try:
            return ensure_runtime_folders(root, lambda _paths: True)
        except OSError:
            return False
    try:
        return ensure_runtime_folders(root, ask)
    except OSError as error:
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.critical(
            None,
            "Provoware-Ordner nicht bereit",
            "Der benötigte Arbeitsordner konnte nicht sicher vorbereitet werden.\n\n"
            f"Grund: {error}\n\nDas Programm startet nicht weiter, damit keine unvollständige Ordnerstruktur entsteht.",
        )
        return False
