"""PySide6-Songtexteditor mit Bereichen, Vorschau, Metadaten, Autosave und Export."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QCloseEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QMenu, QMessageBox, QPushButton, QSplitter,
    QTextEdit, QToolButton, QVBoxLayout, QWidget,
)

from app.character_store import character_marker, character_options
from app.song_document import SECTION_TYPES, SONG_STATUSES, SongDocument, SongSection, export_song, normalize_section_name, save_song
from app.ui_standards import SPACING, apply_global_style
from app.window_state import ensure_window_visible, restore_window_state, save_window_state

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
        self._compact_mode: bool | None = None
        self._build()
        self._load_document_into_widgets()
        self.refresh_characters()
        self._load_section(0)
        self._update_preview()
        apply_global_style(self, zoom_percent)
        restore_window_state(
            self, self.project_root, "song_editor",
            preferred=QSize(1180, 810), minimum=QSize(760, 560),
        )

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
        title = QLabel("Songtext schreiben")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch(1)
        self.export_button = QToolButton()
        self.export_button.setText("Exportieren")
        self.export_button.setToolTip("Eine zusätzliche Datei erzeugen. Der aktuelle Song wird dabei nicht verändert.")
        self.export_button.setPopupMode(QToolButton.InstantPopup)
        export_menu = QMenu(self.export_button)
        export_menu.addAction("TXT mit Angaben", lambda: self.export("txt"))
        export_menu.addAction("Markdown", lambda: self.export("md"))
        export_menu.addAction("JSON", lambda: self.export("json"))
        export_menu.addSeparator()
        export_menu.addAction("Nur Songtext als TXT", lambda: self.export("txt", lyrics_only=True))
        self.export_button.setMenu(export_menu)
        header.addWidget(self.export_button)
        save_button = QPushButton("Jetzt speichern")
        save_button.setToolTip("Zusätzlich zum automatischen Speichern sofort speichern.")
        save_button.clicked.connect(lambda: self.save())
        header.addWidget(save_button)
        outer.addLayout(header)

        guide = QLabel("1. Titel eintragen  →  2. Bereich wählen oder hinzufügen  →  3. Text schreiben. Charaktere können optional direkt aus der Charakterfibel eingefügt werden.")
        guide.setObjectName("muted")
        guide.setWordWrap(True)
        outer.addWidget(guide)

        meta_frame = QFrame()
        meta_frame.setObjectName("card")
        meta_layout = QGridLayout(meta_frame)
        meta_layout.setContentsMargins(10, 8, 10, 8)
        meta_layout.setHorizontalSpacing(10)
        meta_layout.setVerticalSpacing(5)
        self.meta_entries: list[QLineEdit] = []
        self._meta_by_name: dict[str, QLineEdit] = {}

        def add_meta_field(layout: QGridLayout, label_text: str, row: int, col: int, *, span: int = 1) -> QLineEdit:
            label = QLabel(label_text)
            label.setObjectName("muted")
            entry = QLineEdit()
            entry.setAccessibleName(label_text)
            label.setBuddy(entry)
            entry.editingFinished.connect(self._save_from_focus)
            entry.textChanged.connect(self._update_preview)
            layout.addWidget(label, row, col, 1, span)
            layout.addWidget(entry, row + 1, col, 1, span)
            self.meta_entries.append(entry)
            self._meta_by_name[label_text] = entry
            return entry

        self.title_entry = add_meta_field(meta_layout, "Titel", 0, 0)
        self.genre_entry = add_meta_field(meta_layout, "Genre", 0, 1)
        self.mood_entry = add_meta_field(meta_layout, "Stimmung", 0, 2)

        status_row = QHBoxLayout()
        status_row.addWidget(QLabel("Bearbeitungsstand:"))
        self.status_song = QComboBox()
        self.status_song.addItems(SONG_STATUSES)
        self.status_song.currentTextChanged.connect(lambda _value: self.save(reason="Bearbeitungsstand gespeichert"))
        status_row.addWidget(self.status_song)
        self.favorite_check = QCheckBox("★ Favorit")
        self.favorite_check.toggled.connect(lambda _value: self.save(reason="Favorit gespeichert"))
        status_row.addWidget(self.favorite_check)
        status_row.addStretch(1)
        self.details_toggle = QToolButton()
        self.details_toggle.setCheckable(True)
        self.details_toggle.setChecked(True)
        self.details_toggle.setToolTip("Optionale Angaben wie Stil, Stimme, Besonderheiten und Tags ein- oder ausblenden.")
        self.details_toggle.toggled.connect(self._toggle_details)
        status_row.addWidget(self.details_toggle)
        meta_layout.addLayout(status_row, 2, 0, 1, 3)
        for col in range(3):
            meta_layout.setColumnStretch(col, 1)
        outer.addWidget(meta_frame)

        self.details_frame = QFrame()
        self.details_frame.setObjectName("innerCard")
        details_layout = QGridLayout(self.details_frame)
        details_layout.setContentsMargins(10, 7, 10, 7)
        details_layout.setHorizontalSpacing(10)
        details_layout.setVerticalSpacing(5)
        self.style_entry = add_meta_field(details_layout, "Stil", 0, 0)
        self.voice_entry = add_meta_field(details_layout, "Stimme", 0, 1)
        self.special_entry = add_meta_field(details_layout, "Besonderheiten", 0, 2)
        self.tags_entry = add_meta_field(details_layout, "Tags (mit Komma trennen)", 2, 0, span=3)
        for col in range(3):
            details_layout.setColumnStretch(col, 1)
        outer.addWidget(self.details_frame)
        self._toggle_details(True)

        character_frame = QFrame()
        character_frame.setObjectName("innerCard")
        character_layout = QHBoxLayout(character_frame)
        character_layout.setContentsMargins(10, 6, 10, 6)
        character_layout.addWidget(QLabel("Charakterfibel:"))
        self.character_combo = QComboBox()
        self.character_combo.setObjectName("song_character_selector")
        self.character_combo.setToolTip("Charaktere stammen direkt aus der zentralen Charakterfibel.")
        character_layout.addWidget(self.character_combo, 1)
        insert_character = QPushButton("In Songbereich einfügen")
        insert_character.setToolTip("Fügt die ausgewählte Figur an der aktuellen Schreibposition ein und speichert den Song anschließend.")
        insert_character.clicked.connect(self.insert_character_reference)
        character_layout.addWidget(insert_character)
        outer.addWidget(character_frame)

        splitter = QSplitter(Qt.Horizontal)
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        section_bar = QHBoxLayout()
        section_bar.addWidget(QLabel("Songbereich:"))
        self.section_type = QComboBox()
        self.section_type.addItems(SECTION_TYPES)
        self.section_type.setEditable(True)
        self.section_type.setInsertPolicy(QComboBox.NoInsert)
        self.section_type.setToolTip("Standardbereich wählen oder einen eigenen Bereichsnamen eintippen.")
        if self.section_type.lineEdit() is not None:
            self.section_type.lineEdit().setPlaceholderText("Standard wählen oder eigenen Namen eingeben")
        self.section_type.setCurrentText("Strophe")
        section_bar.addWidget(self.section_type)
        self.add_section_button = QPushButton("Bereich hinzufügen")
        self.add_section_button.setAccessibleName("Bereich hinzufügen")
        self.add_section_button.setToolTip("Fügt einen neuen Songbereich hinzu.")
        self.add_section_button.clicked.connect(self.add_section)
        section_bar.addWidget(self.add_section_button)
        self.remove_section_button = QPushButton("Bereich entfernen")
        self.remove_section_button.setAccessibleName("Bereich entfernen")
        self.remove_section_button.setToolTip("Fragt vor dem Entfernen noch einmal nach.")
        self.remove_section_button.clicked.connect(self.remove_section)
        section_bar.addWidget(self.remove_section_button)
        section_bar.addStretch(1)
        left_layout.addLayout(section_bar)
        self._sync_section_action_labels()

        content_row = QHBoxLayout()
        self.section_list = QListWidget()
        self.section_list.setFixedWidth(190)
        self.section_list.currentRowChanged.connect(self._section_changed)
        content_row.addWidget(self.section_list)
        self.section_text = QTextEdit()
        self.section_text.setPlaceholderText("Hier den Text für den ausgewählten Songbereich schreiben …")
        self.section_text.textChanged.connect(self._section_text_changed)
        self.section_text.installEventFilter(self)
        content_row.addWidget(self.section_text, 1)
        left_layout.addLayout(content_row, 1)
        splitter.addWidget(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        preview_title = QLabel("Gesamtvorschau")
        preview_title.setObjectName("sectionTitle")
        right_layout.addWidget(preview_title)
        self.preview = QTextEdit()
        self.preview.setAccessibleName("Gesamtvorschau")
        self.preview.setReadOnly(True)
        right_layout.addWidget(self.preview, 1)
        right_layout.addWidget(QLabel("Zusätzliche Notizen zum Song (optional):"))
        self.other_text = QTextEdit()
        self.other_text.setMaximumHeight(120)
        self.other_text.setPlaceholderText("Ideen, Hinweise oder offene Punkte …")
        self.other_text.textChanged.connect(self._update_preview)
        self.other_text.installEventFilter(self)
        right_layout.addWidget(self.other_text)
        splitter.addWidget(right)
        splitter.setSizes([700, 470])
        outer.addWidget(splitter, 1)

        self.status_label = QLabel("Bereit · Änderungen werden automatisch gespeichert.")
        self.status_label.setObjectName("muted")
        outer.addWidget(self.status_label)

    def ensure_on_screen(self) -> None:
        ensure_window_visible(self, QSize(760, 560))

    def _toggle_details(self, checked: bool) -> None:
        if hasattr(self, "details_frame"):
            self.details_frame.setVisible(bool(checked))
        if hasattr(self, "details_toggle"):
            self.details_toggle.setText("▾ Weitere Angaben" if checked else "▸ Weitere Angaben")

    def _sync_section_action_labels(self) -> None:
        """Hält Aktionsnamen vollständig, verkürzt aber die sichtbaren Hochzoomtexte."""
        high_zoom = self.zoom_percent >= 175
        self.add_section_button.setText("＋ Bereich" if high_zoom else "Bereich hinzufügen")
        self.remove_section_button.setText("− Bereich" if high_zoom else "Bereich entfernen")

    def set_compact_mode(self, compact: bool) -> None:
        """Verdichtet optionale Metadaten nur beim Wechsel in/aus dem Kompaktmodus."""
        compact = bool(compact)
        self._sync_section_action_labels()
        if self._compact_mode == compact:
            return
        self._compact_mode = compact
        self.details_toggle.blockSignals(True)
        self.details_toggle.setChecked(not compact)
        self.details_toggle.blockSignals(False)
        self._toggle_details(not compact)
        self.other_text.setMaximumHeight(88 if compact else 120)

    def eventFilter(self, watched, event):
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.FocusOut and watched in {self.section_text, self.other_text}:
            QTimer.singleShot(0, lambda: self.save(reason="Änderung gespeichert"))
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

    def refresh_characters(self) -> None:
        """Verwendet dieselbe zentrale Auswahl wie andere Schreibmodule."""
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

    def insert_character_reference(self) -> None:
        """Fügt eine lesbare Referenz in den aktuellen Bereich ein; das Songformat bleibt unverändert."""
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
        cursor = self.section_text.textCursor()
        cursor.insertText(marker)
        self.section_text.setTextCursor(cursor)
        self._store_current_section()
        self._update_preview()
        self.save(reason="Charakterreferenz eingefügt")

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
        try:
            kind = normalize_section_name(self.section_type.currentText() or "Strophe")
        except ValueError as error:
            QMessageBox.information(self, "Bereich nicht angelegt", str(error))
            return
        self.document.sections.append(SongSection(kind))
        if self.section_type.findText(kind) < 0:
            self.section_type.addItem(kind)
        self.section_type.setCurrentText(kind)
        self._refresh_section_list()
        self._load_section(len(self.document.sections) - 1)
        self._update_preview()
        self.status_label.setText("Neuer Songbereich angelegt · Text kann jetzt eingegeben werden.")
        self.section_text.setFocus()

    def remove_section(self) -> None:
        index = self._active_index
        if index is None:
            QMessageBox.information(self, "Kein Bereich ausgewählt", "Bitte zuerst links einen Songbereich auswählen.")
            return
        self._store_current_section()
        section = self.document.sections[index]
        answer = QMessageBox.question(
            self,
            "Songbereich entfernen?",
            f"Soll „{section.kind}“ wirklich aus diesem Song entfernt werden?\n\n"
            "Die Änderung wird erst mit dem nächsten Speichern dauerhaft übernommen.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        del self.document.sections[index]
        if not self.document.sections:
            self.document.sections.append(SongSection("Strophe"))
        self._refresh_section_list()
        self._load_section(min(index, len(self.document.sections) - 1))
        self._update_preview()
        self.status_label.setText("Songbereich entfernt · Änderung noch nicht dauerhaft gespeichert.")

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
        self.save(reason="Änderung gespeichert")

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
            self.status_label.setText("Speichern fehlgeschlagen · der bisherige Stand bleibt geschützt.")
            QMessageBox.critical(
                self,
                "Songtext nicht gespeichert",
                f"Der bisherige gespeicherte Stand bleibt erhalten.\n\nGrund: {error}",
            )
            return None

    def export(self, export_format: str, *, lyrics_only: bool = False) -> Path | None:
        try:
            self._sync_document()
            target = export_song(self.project_root, self.document, export_format, lyrics_only=lyrics_only)
            self.status_label.setText(f"Export gespeichert: {target.name}")
            return target
        except Exception as error:
            self.status_label.setText("Export fehlgeschlagen · der Song wurde nicht verändert.")
            QMessageBox.critical(
                self,
                "Export fehlgeschlagen",
                f"Der Song wurde nicht verändert.\n\nGrund: {error}",
            )
            return None

    def _autosave(self) -> None:
        if not self._closed:
            self.save(reason="automatisch gespeichert")

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
        save_window_state(self, self.project_root, "song_editor")
        self._closed = True
        self.autosave_timer.stop()
        if self.on_closed is not None:
            self.on_closed(self)
        event.accept()
