"""PySide6-Songbibliothek mit Suche, Filtern, Gruppierung und sicherem Restore."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QMessageBox, QPushButton, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget,
)

from app.song_document import (
    SONG_STATUSES, SongDocument, list_songs, list_versions, load_song, restore_version,
)
from app.ui_standards import SPACING, apply_global_style

FILTER_ALL = "Alle"
SORT_OPTIONS = ("Zuletzt bearbeitet", "Titel", "Genre", "Tags", "Status")
GROUP_OPTIONS = ("Keine", "Genre", "Tags", "Status")


@dataclass(frozen=True)
class SongRow:
    path: Path
    document: SongDocument
    modified: float
    versions: int


def _norm(value: str) -> str:
    return value.strip().casefold()


def song_matches(row: SongRow, search: str = "", *, genre: str = FILTER_ALL,
                 mood: str = FILTER_ALL, style: str = FILTER_ALL,
                 voice: str = FILTER_ALL, tag: str = FILTER_ALL,
                 status: str = FILTER_ALL, favorites_only: bool = False) -> bool:
    document = row.document
    needle = _norm(search)
    searchable = " ".join((
        document.title, document.genre, document.mood, document.style,
        document.voice, " ".join(document.tags),
    )).casefold()
    if needle and needle not in searchable:
        return False
    fields = (
        (genre, document.genre), (mood, document.mood), (style, document.style),
        (voice, document.voice), (status, document.status),
    )
    if any(selected != FILTER_ALL and _norm(selected) != _norm(actual)
           for selected, actual in fields):
        return False
    if tag != FILTER_ALL and _norm(tag) not in {_norm(value) for value in document.tags}:
        return False
    return not favorites_only or document.favorite


def sort_rows(rows: list[SongRow], sort_by: str) -> list[SongRow]:
    if sort_by == "Titel":
        key, reverse = lambda row: _norm(row.document.title), False
    elif sort_by == "Genre":
        key, reverse = lambda row: (_norm(row.document.genre), _norm(row.document.title)), False
    elif sort_by == "Tags":
        key, reverse = lambda row: (_norm(", ".join(row.document.tags)), _norm(row.document.title)), False
    elif sort_by == "Status":
        order = {status: index for index, status in enumerate(SONG_STATUSES)}
        key, reverse = lambda row: (order.get(row.document.status, 99), _norm(row.document.title)), False
    else:
        key, reverse = lambda row: row.modified, True
    return sorted(rows, key=key, reverse=reverse)


def row_group(row: SongRow, group_by: str) -> str:
    if group_by == "Genre":
        return row.document.genre.strip() or "Ohne Genre"
    if group_by == "Tags":
        return ", ".join(row.document.tags) or "Ohne Tags"
    if group_by == "Status":
        return row.document.status or "Idee"
    return ""


class SongLibrary(QWidget):
    def __init__(self, project_root: Path, zoom_percent: int,
                 open_song: Callable[[Path], None], parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.Window)
        self.project_root = project_root
        self.open_song_callback = open_song
        self.new_song_callback = getattr(parent, "open_song_editor", None)
        self.zoom_percent = zoom_percent
        self._rows: list[SongRow] = []
        self._path_by_item: dict[int, Path] = {}
        self.setWindowTitle("Songbibliothek")
        self.resize(1180, 720)
        self.setMinimumSize(920, 580)
        self._build()
        apply_global_style(self, zoom_percent)
        self.refresh()
        self.search_entry.setFocus()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACING["l"], SPACING["l"], SPACING["l"], SPACING["l"])
        outer.setSpacing(SPACING["s"])

        header = QHBoxLayout()
        title = QLabel("Songbibliothek")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch(1)
        if callable(self.new_song_callback):
            new_button = QPushButton("＋ Neuen Song schreiben")
            new_button.setObjectName("primaryButton")
            new_button.setToolTip("Öffnet einen leeren Songtexteditor. Bestehende Songs bleiben unverändert.")
            new_button.clicked.connect(self.new_song_callback)
            header.addWidget(new_button)
        refresh_button = QPushButton("Liste aktualisieren")
        refresh_button.clicked.connect(self.refresh)
        header.addWidget(refresh_button)
        outer.addLayout(header)

        hint = QLabel("Song suchen, Filter setzen und anschließend einen Song markieren. Doppelklick öffnet ihn direkt.")
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        outer.addWidget(hint)

        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Song suchen:"))
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Titel, Genre, Stimmung, Stil, Stimme oder Tag eingeben …")
        self.search_entry.textChanged.connect(self.apply_view)
        search_row.addWidget(self.search_entry, 1)
        outer.addLayout(search_row)

        filters = QGridLayout()
        self.filter_boxes: dict[str, QComboBox] = {}
        for index, label in enumerate(("Genre", "Stimmung", "Stil", "Stimme", "Tags", "Status")):
            filters.addWidget(QLabel(label), 0, index)
            box = QComboBox()
            box.addItem(FILTER_ALL)
            box.currentTextChanged.connect(self.apply_view)
            filters.addWidget(box, 1, index)
            self.filter_boxes[label] = box
        self.favorite_check = QCheckBox("★ Nur Favoriten")
        self.favorite_check.toggled.connect(self.apply_view)
        filters.addWidget(self.favorite_check, 2, 0, 1, 2)
        reset = QPushButton("Suche und Filter zurücksetzen")
        reset.clicked.connect(self.reset_filters)
        filters.addWidget(reset, 2, 4, 1, 2)
        outer.addLayout(filters)

        view_row = QHBoxLayout()
        view_row.addWidget(QLabel("Sortieren nach:"))
        self.sort_box = QComboBox()
        self.sort_box.addItems(SORT_OPTIONS)
        self.sort_box.currentTextChanged.connect(self.apply_view)
        view_row.addWidget(self.sort_box)
        view_row.addWidget(QLabel("Gruppieren nach:"))
        self.group_box = QComboBox()
        self.group_box.addItems(GROUP_OPTIONS)
        self.group_box.currentTextChanged.connect(self.apply_view)
        view_row.addWidget(self.group_box)
        view_row.addStretch(1)
        outer.addLayout(view_row)

        self.table = QTreeWidget()
        self.table.setHeaderLabels((
            "Gruppe / Titel", "★", "Genre", "Stimmung", "Stand", "Tags",
            "Zuletzt bearbeitet", "Versionen",
        ))
        self.table.setAlternatingRowColors(True)
        self.table.itemDoubleClicked.connect(lambda *_args: self.open_selected())
        outer.addWidget(self.table, 1)

        actions = QHBoxLayout()
        open_button = QPushButton("Ausgewählten Song öffnen")
        open_button.setObjectName("primaryButton")
        open_button.clicked.connect(self.open_selected)
        actions.addWidget(open_button)
        version_button = QPushButton("Ältere Version ansehen / wiederherstellen")
        version_button.clicked.connect(self.show_versions)
        actions.addWidget(version_button)
        actions.addStretch(1)
        self.status_label = QLabel("")
        self.status_label.setObjectName("muted")
        actions.addWidget(self.status_label)
        outer.addLayout(actions)

    @staticmethod
    def _values(rows: list[SongRow], attr: str) -> tuple[str, ...]:
        found: set[str] = set()
        for row in rows:
            value = getattr(row.document, attr)
            if isinstance(value, list):
                found.update(item.strip() for item in value if item.strip())
            elif str(value).strip():
                found.add(str(value).strip())
        return (FILTER_ALL, *sorted(found, key=str.casefold))

    @staticmethod
    def _set_values(box: QComboBox, values: tuple[str, ...]) -> None:
        current = box.currentText()
        box.blockSignals(True)
        box.clear()
        box.addItems(values)
        box.setCurrentText(current if current in values else FILTER_ALL)
        box.blockSignals(False)

    def _update_filter_values(self) -> None:
        for label, attr in {
            "Genre": "genre", "Stimmung": "mood", "Stil": "style",
            "Stimme": "voice", "Tags": "tags",
        }.items():
            self._set_values(self.filter_boxes[label], self._values(self._rows, attr))
        self._set_values(self.filter_boxes["Status"], (FILTER_ALL, *SONG_STATUSES))

    def refresh(self) -> None:
        rows: list[SongRow] = []
        skipped = 0
        for path in list_songs(self.project_root):
            try:
                document = load_song(path)
                rows.append(SongRow(
                    path, document, path.stat().st_mtime,
                    len(list_versions(self.project_root, document.title)),
                ))
            except (OSError, UnicodeError, ValueError):
                skipped += 1
        self._rows = rows
        self._update_filter_values()
        self.apply_view()
        if skipped:
            self.status_label.setText(f"{skipped} nicht lesbare Songdatei(en) wurden sicher übersprungen.")

    def apply_view(self, *_args: object) -> None:
        self.table.clear()
        self._path_by_item.clear()
        filters = self.filter_boxes
        rows = [
            row for row in self._rows
            if song_matches(
                row, self.search_entry.text(),
                genre=filters["Genre"].currentText(),
                mood=filters["Stimmung"].currentText(),
                style=filters["Stil"].currentText(),
                voice=filters["Stimme"].currentText(),
                tag=filters["Tags"].currentText(),
                status=filters["Status"].currentText(),
                favorites_only=self.favorite_check.isChecked(),
            )
        ]
        rows = sort_rows(rows, self.sort_box.currentText())
        groups: dict[str, QTreeWidgetItem] = {}
        group_by = self.group_box.currentText()
        for row in rows:
            parent = self.table.invisibleRootItem()
            if group_by != "Keine":
                group = row_group(row, group_by)
                if group not in groups:
                    groups[group] = QTreeWidgetItem([group])
                    self.table.addTopLevelItem(groups[group])
                    groups[group].setExpanded(True)
                parent = groups[group]
            document = row.document
            item = QTreeWidgetItem((
                document.title,
                "★" if document.favorite else "",
                document.genre,
                document.mood,
                document.status,
                ", ".join(document.tags),
                datetime.fromtimestamp(row.modified).strftime("%d.%m.%Y %H:%M"),
                str(row.versions),
            ))
            if parent is self.table.invisibleRootItem():
                self.table.addTopLevelItem(item)
            else:
                parent.addChild(item)
            self._path_by_item[id(item)] = row.path
        self.table.resizeColumnToContents(0)
        if not self._rows:
            self.status_label.setText("Noch keine Songs vorhanden · oben mit „Neuen Song schreiben“ starten.")
        elif not rows:
            self.status_label.setText(f"Keine Treffer · {len(self._rows)} Song(s) insgesamt. Suche oder Filter zurücksetzen.")
        else:
            self.status_label.setText(f"{len(rows)} angezeigt · {len(self._rows)} Song(s) insgesamt")

    def reset_filters(self) -> None:
        self.search_entry.clear()
        for box in self.filter_boxes.values():
            box.setCurrentText(FILTER_ALL)
        self.favorite_check.setChecked(False)
        self.apply_view()
        self.search_entry.setFocus()

    def set_search(self, text: str) -> None:
        self.search_entry.setText(text)
        self.search_entry.setFocus()

    def selected_path(self) -> Path | None:
        item = self.table.currentItem()
        return self._path_by_item.get(id(item)) if item else None

    def open_selected(self) -> None:
        path = self.selected_path()
        if path is None:
            QMessageBox.information(self, "Kein Song ausgewählt", "Bitte zuerst einen Song in der Liste markieren.")
            return
        self.open_song_callback(path)

    def show_versions(self) -> None:
        path = self.selected_path()
        if path is None:
            QMessageBox.information(self, "Kein Song ausgewählt", "Bitte zuerst einen Song in der Liste markieren.")
            return
        try:
            document = load_song(path)
            versions = list_versions(self.project_root, document.title)
        except Exception as error:
            QMessageBox.critical(self, "Versionen nicht lesbar", f"Der Song wurde nicht verändert.\n\nGrund: {error}")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Ältere Versionen – {document.title}")
        dialog.resize(820, 600)
        layout = QVBoxLayout(dialog)
        title = QLabel(f"Ältere Versionen · {document.title}")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)
        hint = QLabel(
            "1. Version links auswählen  →  2. Vorschau prüfen  →  3. erst dann wiederherstellen. "
            "Der aktuelle Stand wird vorher automatisch gesichert."
        )
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        listing = QListWidget()
        for version in versions:
            listing.addItem(version.stem)
        layout.addWidget(listing)
        preview = QTextEdit()
        preview.setReadOnly(True)
        layout.addWidget(preview, 1)
        result = QLabel()
        result.setObjectName("muted")
        layout.addWidget(result)

        def chosen() -> Path | None:
            index = listing.currentRow()
            return versions[index] if 0 <= index < len(versions) else None

        def load_preview() -> None:
            version = chosen()
            preview.setPlainText(
                version.read_text(encoding="utf-8")
                if version else "Noch keine älteren Versionen vorhanden."
            )

        listing.currentRowChanged.connect(lambda *_args: load_preview())
        action_row = QHBoxLayout()
        restore = QPushButton("Diese Version wiederherstellen")
        restore.setObjectName("primaryButton")
        restore.setEnabled(bool(versions))

        def do_restore() -> None:
            version = chosen()
            if version is None:
                QMessageBox.information(dialog, "Keine Version ausgewählt", "Bitte zuerst links eine Version markieren.")
                return
            answer = QMessageBox.question(
                dialog,
                "Version wirklich wiederherstellen?",
                "Der aktuelle Songstand wird zuerst automatisch gesichert. Danach wird die gewählte ältere Version eingesetzt.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                return
            try:
                _target, backup = restore_version(self.project_root, path, version)
            except Exception as error:
                QMessageBox.critical(dialog, "Nicht wiederhergestellt", f"Der aktuelle Song bleibt erhalten.\n\nGrund: {error}")
                return
            if backup is None:
                result.setText("Diese Version entspricht bereits dem aktuellen Song.")
            else:
                result.setText("Wiederhergestellt · der vorherige Stand wurde automatisch als neue Version gesichert.")
            self.refresh()

        restore.clicked.connect(do_restore)
        action_row.addWidget(restore)
        action_row.addStretch(1)
        close = QPushButton("Schließen")
        close.clicked.connect(dialog.accept)
        action_row.addWidget(close)
        layout.addLayout(action_row)
        if versions:
            listing.setCurrentRow(0)
        else:
            load_preview()
        apply_global_style(dialog, self.zoom_percent)
        dialog.exec()

    def set_zoom(self, percent: int) -> None:
        self.zoom_percent = percent
        apply_global_style(self, percent)
