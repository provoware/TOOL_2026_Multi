"""PySide6-Songtexteditor mit Bereichen, Vorschau, Metadaten, Autosave und Export."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCloseEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QMenu, QMessageBox, QPushButton, QSplitter,
    QTextEdit, QToolButton, QVBoxLayout, QWidget,
)

from app.song_document import SECTION_TYPES, SONG_STATUSES, SongDocument, SongSection, export_song, save_song
from app.ui_standards import SPACING, apply_global_style

AUTOSAVE_MS = 5 * 60 * 1000


class SongEditor(QWidget):
    """Einheitlicher Qt-Editor; Fachlogik und Speicherformat bleiben unverändert."""

    def __init__(self, project_root: Path, zoom_percent: int = 100,
                 on_closed: Callable[["SongEditor"], None] | None = None,
                 document: SongDocument | None = None,
                 on_saved: Callable[[Path], None] | None = None,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.Window)
        self.project_root = project_root
        self.document = document or SongDocument(title="Unbenannter Song", sections=[SongSection("Strophe")])
        if not self.document.sections:
            self.document.sections.append(SongSection("Strophe"))
        self.on_closed = on_closed
        self.on_saved = on_saved
        self.zoom_percent = zoom_percent
        self._closed = False
        self._closing_after_save = False
        self._active_index: int | None = None
        self._loading_section = False

        self.setWindowTitle(f"Songtexteditor – {self.document.title or 'Unbenannt'}")
        self.resize(1180, 810)
        self.setMinimumSize(940, 650)
        self._build()
        self._load_document_into_widgets()
        self._load_section(0)
        self._update_preview()
        apply_global_style(self, zoom_percent)

        self.autosave_timer = QTimer(self)
        self.autosave_timer.setInterval(AUTOSAVE_MS)
        self.autosave_timer.timeout.connect(self._autosave)
        self.autosave_timer.start()
        QShortcut(QKeySequence("Ctrl+S"), self, activated=lambda: self.save())
        QShortcut(QKeySequence("Escape"), self, activated=self.close_safely)
        self.title_entry.setFocus()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACING["l"], SPACING["l"], SPACING["l"], SPACING["l"])
        outer.setSpacing(SPACING["m"])

        header = QHBoxLayout()
        title = QLabel("Songtexteditor")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch(1)
        self.export_button = QToolButton()
        self.export_button.setText("Export")
        self.export_button.setPopupMode(QToolButton.InstantPopup)
        export_menu = QMenu(self.export_button)
        export_menu.addAction("TXT mit Metadaten", lambda: self.export("txt"))
        export_menu.addAction("Markdown", lambda: self.export("md"))
        export_menu.addAction("JSON", lambda: self.export("json"))
        export_menu.addSeparator()
        export_menu.addAction("Nur Songtext (TXT)", lambda: self.export("txt", lyrics_only=True))
        self.export_button.setMenu(export_menu)
        header.addWidget(self.export_button)
        save_button = QPushButton("Speichern")
        save_button.clicked.connect(lambda: self.save())
        header.addWidget(save_button)
        outer.addLayout(header)

        meta_frame = QFrame()
        meta_frame.setObjectName("card")
        meta_layout = QGridLayout(meta_frame)
        meta_layout.setContentsMargins(10, 8, 10, 8)
        meta_layout.setHorizontalSpacing(10)
        meta_layout.setVerticalSpacing(5)
        self.meta_entries: list[QLineEdit] = []
        field_names = ("Titel", "Genre", "Stimmung", "Stil", "Stimme", "Besonderheiten", "Tags (Komma getrennt)")
        self._meta_by_name: dict[str, QLineEdit] = {}
        for index, label_text in enumerate(field_names):
            row, col = divmod(index, 3)
            label = QLabel(label_text)
            label.setObjectName("muted")
            entry = QLineEdit()
            entry.editingFinished.connect(self._save_from_focus)
            entry.textChanged.connect(self._update_preview)
            meta_layout.addWidget(label, row * 2, col)
            meta_layout.addWidget(entry, row * 2 + 1, col)
            self.meta_entries.append(entry)
            self._meta_by_name[label_text] = entry
        self.title_entry = self._meta_by_name["Titel"]
        self.genre_entry = self._meta_by_name["Genre"]
        self.mood_entry = self._meta_by_name["Stimmung"]
        self.style_entry = self._meta_by_name["Stil"]
        self.voice_entry = self._meta_by_name["Stimme"]
        self.special_entry = self._meta_by_name["Besonderheiten"]
        self.tags_entry = self._meta_by_name["Tags (Komma getrennt)"]

        status_row = QHBoxLayout()
        status_row.addWidget(QLabel("Bearbeitungsstatus:"))
        self.status_song = QComboBox()
        self.status_song.addItems(SONG_STATUSES)
        self.status_song.currentTextChanged.connect(lambda _value: self.save(reason="Status gespeichert"))
        status_row.addWidget(self.status_song)
        self.favorite_check = QCheckBox("★ Favorit")
        self.favorite_check.toggled.connect(lambda _value: self.save(reason="Favorit gespeichert"))
        status_row.addWidget(self.favorite_check)
        status_row.addStretch(1)
        meta_layout.addLayout(status_row, 5, 1, 1, 2)
        for col in range(3):
            meta_layout.setColumnStretch(col, 1)
        outer.addWidget(meta_frame)

        splitter = QSplitter(Qt.Horizontal)
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        section_bar = QHBoxLayout()
        section_bar.addWidget(QLabel("Bereich:"))
        self.section_type = QComboBox()
        self.section_type.addItems(SECTION_TYPES)
        self.section_type.setCurrentText("Strophe")
        section_bar.addWidget(self.section_type)
        add_button = QPushButton("Bereich hinzufügen")
        add_button.clicked.connect(self.add_section)
        section_bar.addWidget(add_button)
        remove_button = QPushButton("Bereich entfernen")
        remove_button.clicked.connect(self.remove_section)
        section_bar.addWidget(remove_button)
        section_bar.addStretch(1)
        left_layout.addLayout(section_bar)

        content_row = QHBoxLayout()
        self.section_list = QListWidget()
        self.section_list.setFixedWidth(190)
        self.section_list.currentRowChanged.connect(self._section_changed)
        content_row.addWidget(self.section_list)
        self.section_text = QTextEdit()
        self.section_text.textChanged.connect(self._section_text_changed)
        self.section_text.installEventFilter(self)
        content_row.addWidget(self.section_text, 1)
        left_layout.addLayout(content_row, 1)
        splitter.addWidget(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        preview_title = QLabel("Vorschau")
        preview_title.setObjectName("sectionTitle")
        right_layout.addWidget(preview_title)
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        right_layout.addWidget(self.preview, 1)
        right_layout.addWidget(QLabel("Sonstiges (optional):"))
        self.other_text = QTextEdit()
        self.other_text.setMaximumHeight(120)
        self.other_text.textChanged.connect(self._update_preview)
        self.other_text.installEventFilter(self)
        right_layout.addWidget(self.other_text)
        splitter.addWidget(right)
        splitter.setSizes([700, 470])
        outer.addWidget(splitter, 1)

        self.status_label = QLabel("Bereit · Autosave alle 5 Minuten")
        self.status_label.setObjectName("muted")
        outer.addWidget(self.status_label)

    def eventFilter(self, watched, event):
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.FocusOut and watched in {self.section_text, self.other_text}:
            QTimer.singleShot(0, lambda: self.save(reason="Feld gespeichert"))
        return super().eventFilter(watched, event)

    def _load_document_into_widgets(self) -> None:
        widgets = (
            (self.title_entry, self.document.title), (self.genre_entry, self.document.genre),
            (self.mood_entry, self.document.mood), (self.style_entry, self.document.style),
            (self.voice_entry, self.document.voice), (self.special_entry, self.document.special),
            (self.tags_entry, ", ".join(self.document.tags)),
        )
        for widget, value in widgets:
            widget.blockSignals(True)
            widget.setText(value)
            widget.blockSignals(False)
        self.status_song.blockSignals(True)
        self.status_song.setCurrentText(self.document.status if self.document.status in SONG_STATUSES else "Idee")
        self.status_song.blockSignals(False)
        self.favorite_check.blockSignals(True)
        self.favorite_check.setChecked(self.document.favorite)
        self.favorite_check.blockSignals(False)
        self.other_text.blockSignals(True)
        self.other_text.setPlainText(self.document.other)
        self.other_text.blockSignals(False)
        self._refresh_section_list()

    def _refresh_section_list(self) -> None:
        self.section_list.blockSignals(True)
        self.section_list.clear()
        counters: dict[str, int] = {}
        for section in self.document.sections:
            counters[section.kind] = counters.get(section.kind, 0) + 1
            number = f" {counters[section.kind]}" if counters[section.kind] > 1 or section.kind == "Strophe" else ""
            self.section_list.addItem(f"{section.kind}{number}")
        self.section_list.blockSignals(False)

    def _current_index(self) -> int | None:
        index = self.section_list.currentRow()
        return index if index >= 0 else None

    def _store_current_section(self) -> None:
        index = self._active_index
        if index is not None and 0 <= index < len(self.document.sections):
            self.document.sections[index].text = self.section_text.toPlainText()

    def _load_section(self, index: int) -> None:
        if not self.document.sections:
            self._active_index = None
            self.section_text.clear()
            return
        index = max(0, min(index, len(self.document.sections) - 1))
        self._loading_section = True
        try:
            self.section_list.blockSignals(True)
            self.section_list.setCurrentRow(index)
            self.section_list.blockSignals(False)
            self.section_text.blockSignals(True)
            self.section_text.setPlainText(self.document.sections[index].text)
            self.section_text.blockSignals(False)
            self._active_index = index
        finally:
            self._loading_section = False

    def _section_changed(self, index: int) -> None:
        if self._loading_section or index < 0 or index == self._active_index:
            return
        self._store_current_section()
        self._load_section(index)
        self._update_preview()

    def _section_text_changed(self) -> None:
        if self._loading_section:
            return
        self._store_current_section()
        self._update_preview()

    def add_section(self) -> None:
        self._store_current_section()
        self.document.sections.append(SongSection(self.section_type.currentText() or "Strophe"))
        self._refresh_section_list()
        self._load_section(len(self.document.sections) - 1)
        self._update_preview()
        self.section_text.setFocus()

    def remove_section(self) -> None:
        index = self._active_index
        if index is None:
            return
        self._store_current_section()
        del self.document.sections[index]
        if not self.document.sections:
            self.document.sections.append(SongSection("Strophe"))
        self._refresh_section_list()
        self._load_section(min(index, len(self.document.sections) - 1))
        self._update_preview()

    def _sync_document(self) -> None:
        self._store_current_section()
        self.document.title = self.title_entry.text().strip() or "Unbenannter Song"
        self.document.genre = self.genre_entry.text().strip()
        self.document.mood = self.mood_entry.text().strip()
        self.document.style = self.style_entry.text().strip()
        self.document.voice = self.voice_entry.text().strip()
        self.document.special = self.special_entry.text().strip()
        self.document.tags = [part.strip() for part in self.tags_entry.text().split(",") if part.strip()]
        self.document.status = self.status_song.currentText() if self.status_song.currentText() in SONG_STATUSES else "Idee"
        self.document.favorite = self.favorite_check.isChecked()
        self.document.other = self.other_text.toPlainText()
        self.setWindowTitle(f"Songtexteditor – {self.document.title}")

    def _update_preview(self, *_args: object) -> None:
        if not hasattr(self, "preview"):
            return
        self._sync_document()
        self.preview.setPlainText(self.document.render())

    def _save_from_focus(self) -> None:
        self.save(reason="Feld gespeichert")

    def save(self, *, reason: str = "gespeichert") -> Path | None:
        if self._closed:
            return None
        try:
            self._sync_document()
            target = save_song(self.project_root, self.document)
            self.status_label.setText(f"● {reason}: {target.name}")
            if self.on_saved is not None:
                self.on_saved(target)
            return target
        except Exception as error:
            self.status_label.setText(f"Speichern fehlgeschlagen: {type(error).__name__}")
            QMessageBox.critical(self, "Songtext nicht gespeichert", str(error))
            return None

    def export(self, export_format: str, *, lyrics_only: bool = False) -> Path | None:
        try:
            self._sync_document()
            target = export_song(self.project_root, self.document, export_format, lyrics_only=lyrics_only)
            self.status_label.setText(f"Export erstellt: {target.name}")
            return target
        except Exception as error:
            self.status_label.setText(f"Export fehlgeschlagen: {type(error).__name__}")
            QMessageBox.critical(self, "Export fehlgeschlagen", str(error))
            return None

    def _autosave(self) -> None:
        if not self._closed:
            self.save(reason="Autosave")

    def close_safely(self) -> None:
        if self._closed:
            return
        if self.save(reason="beim Schließen gespeichert") is None:
            return
        self._closing_after_save = True
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._closed:
            event.accept()
            return
        if not self._closing_after_save and self.save(reason="beim Schließen gespeichert") is None:
            event.ignore()
            return
        self._closed = True
        self.autosave_timer.stop()
        if self.on_closed is not None:
            self.on_closed(self)
        event.accept()
