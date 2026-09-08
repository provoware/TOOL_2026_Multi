"""PySide6-Multimodul-Dashboard nach dem Provoware-Referenzentwurf."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtGui import QCloseEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QSizePolicy, QVBoxLayout, QWidget,
)

from app.event_log import EventLogger
from app.quick_note import append_developer_info
from app.recovery_center import RecoveryCenter
from app.recovery_ui import ZOOM_LEVELS
from app.song_document import list_songs, load_song
from app.song_editor import SongEditor
from app.song_library import SongLibrary
from app.texts import TextRegistry
from app.ui_standards import COLORS, SPACING, apply_global_style


class Dashboard(QWidget):
    """Referenznahes Hauptfenster mit linker Navigation, Kachelleiste und 2×2-Arbeitsfläche."""

    closed_cleanly = Signal()

    def __init__(self, texts: TextRegistry, logger: EventLogger,
                 project_root: Path | None = None) -> None:
        super().__init__()
        self.texts, self.logger = texts, logger
        self.project_root = project_root or Path.cwd()
        self.zoom_percent = 100
        self._song_editors: list[SongEditor] = []
        self._song_library: SongLibrary | None = None
        self._recovery_center: RecoveryCenter | None = None
        self.nav_collapsed = False
        self._nav_entries: list[QWidget] = []
        self._closing_after_save = False
        self._event_filter_installed = False

        self.setObjectName("dashboardShell")
        self.setWindowTitle("Provoware-Datenbank-Dashboard 2026")
        self.resize(1280, 790)
        self.setMinimumSize(1020, 650)
        self._build()
        self._bind_shortcuts()
        apply_global_style(self, self.zoom_percent)
        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)
            self._event_filter_installed = True
        self.refresh()
        self.search_entry.setFocus()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACING["s"], SPACING["s"], SPACING["s"], SPACING["s"])
        outer.setSpacing(SPACING["s"])
        outer.addWidget(self._build_header())
        outer.addLayout(self._build_tile_strip())

        body = QHBoxLayout()
        body.setSpacing(SPACING["s"])
        self.sidebar = self._build_sidebar()
        body.addWidget(self.sidebar)

        main = QVBoxLayout()
        main.setSpacing(SPACING["s"])
        main.addWidget(self._build_quick_info())
        main.addWidget(self._build_recent_strip())
        main.addLayout(self._build_dashboard_grid(), 1)
        body.addLayout(main, 1)
        outer.addLayout(body, 1)
        outer.addWidget(self._build_statusbar())

    def _build_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("header")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(12, 7, 10, 7)
        layout.setSpacing(8)

        logo = QLabel("▦")
        logo.setObjectName("accent")
        logo.setStyleSheet(f"font-size: 23pt; color: {COLORS['accent']}; font-weight: 700;")
        layout.addWidget(logo)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        title = QLabel("Provoware-Datenbank-Dashboard 2026")
        title.setObjectName("appTitle")
        subtitle = QLabel("Linux · PySide6 · Erweiterbares Multimodul-Dashboard")
        subtitle.setObjectName("subtitle")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        layout.addLayout(title_box)
        layout.addStretch(1)

        search_icon = QLabel("⌕")
        search_icon.setObjectName("accent")
        layout.addWidget(search_icon)
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Suchen …")
        self.search_entry.setFixedWidth(245)
        self.search_entry.returnPressed.connect(self._header_search)
        layout.addWidget(self.search_entry)
        logout = QPushButton("Logout")
        logout.clicked.connect(self.logout)
        layout.addWidget(logout)
        return header

    def _build_tile_strip(self) -> QHBoxLayout:
        strip = QHBoxLayout()
        strip.setSpacing(SPACING["xs"])
        tiles = (
            ("♫\nSongtexte", self.open_song_library),
            ("▣\nHörspiele", lambda: self._planned("Hörspiele")),
            ("▤\nBlogartikel", lambda: self._planned("Blogartikel")),
            ("▥\nGenres", lambda: self._planned("Genres-Datenbank")),
            ("?\nPrompts", lambda: self._planned("Prompts")),
            ("⌕\nSuche", lambda: self._planned("Dateisuche")),
            ("≡\nDuplikate", lambda: self._planned("Duplikatprüfer")),
        )
        for text, command in tiles:
            button = QPushButton(text)
            button.setObjectName("tileButton")
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.clicked.connect(command)
            strip.addWidget(button)
        return strip

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(214)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(1)

        top = QHBoxLayout()
        menu_button = QPushButton("☰")
        menu_button.setObjectName("navButton")
        menu_button.setFixedWidth(42)
        menu_button.clicked.connect(self.toggle_sidebar)
        top.addWidget(menu_button)
        nav_title = QLabel("Navigation")
        nav_title.setObjectName("muted")
        top.addWidget(nav_title)
        top.addStretch(1)
        layout.addLayout(top)

        self._add_nav(layout, "▦  Übersicht", lambda: None, active=True)
        self._add_nav(layout, "◈  Modulauswahl", lambda: self._planned("Modulauswahl"))
        self._add_heading(layout, "Workflow Schreiben")
        self._add_nav(layout, "  ♫  Songtexte", self.open_song_library)
        self._add_nav(layout, "  ▣  Hörspiele", lambda: self._planned("Hörspiele"))
        self._add_nav(layout, "  ▤  Blogartikel", lambda: self._planned("Blogartikel"))
        self._add_heading(layout, "DB-Eingaben")
        for label in ("Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten", "GitHub-Repositories", "Prompts"):
            self._add_nav(layout, f"  ·  {label}", lambda _checked=False, item=label: self._planned(item))
        self._add_heading(layout, "Funktionen")
        self._add_nav(layout, "  ◉  Genreszufallsgenerator", lambda: self._planned("Genreszufallsgenerator"))
        self._add_nav(layout, "  ✎  Reimfinder", lambda: self._planned("Reimfinder"))
        self._add_heading(layout, "Systemanwendungen")
        self._add_nav(layout, "  ⌕  Datenbank-Suche", lambda: self._planned("Datenbank-Suche"))
        self._add_nav(layout, "  ▤  Inhaltssuche Textdateien", lambda: self._planned("Inhaltssuche Textdateien"))
        self._add_nav(layout, "  ≡  Trefferliste", lambda: self._planned("Trefferliste"))
        self._add_nav(layout, "  ◫  Duplikatprüfer", lambda: self._planned("Duplikatprüfer"))
        self._add_heading(layout, "Werkzeug")
        self.recovery_nav_button = self._add_nav(layout, "  ⚕  Recovery", self.open_recovery)
        layout.addStretch(1)
        return sidebar

    def _add_heading(self, layout: QVBoxLayout, text: str) -> None:
        label = QLabel(f"⌄  {text}")
        label.setObjectName("muted")
        label.setContentsMargins(8, 6, 2, 2)
        layout.addWidget(label)
        self._nav_entries.append(label)

    def _add_nav(self, layout: QVBoxLayout, text: str, command: Callable[[], None],
                 active: bool = False) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("activeNav" if active else "navButton")
        button.clicked.connect(command)
        layout.addWidget(button)
        self._nav_entries.append(button)
        return button

    def toggle_sidebar(self) -> None:
        self.nav_collapsed = not self.nav_collapsed
        self.sidebar.setFixedWidth(56 if self.nav_collapsed else 214)
        for widget in self._nav_entries:
            widget.setVisible(not self.nav_collapsed)

    def _build_quick_info(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("toolbar")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 5, 8, 5)
        layout.addWidget(QLabel("Entwicklerinfo:"))
        self.quick_entry = QLineEdit()
        self.quick_entry.setPlaceholderText("Kurze Information an Entwicklerinformation.txt anhängen …")
        self.quick_entry.returnPressed.connect(self.save_quick_info)
        layout.addWidget(self.quick_entry, 1)
        save = QPushButton("Speichern")
        save.clicked.connect(self.save_quick_info)
        layout.addWidget(save)
        return frame

    def _build_recent_strip(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("toolbar")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 5, 8, 5)
        label = QLabel("Zuletzt bearbeitet")
        label.setObjectName("muted")
        layout.addWidget(label)
        self.recent_layout = QHBoxLayout()
        self.recent_layout.setSpacing(4)
        layout.addLayout(self.recent_layout, 1)
        all_songs = QPushButton("Alle Songs")
        all_songs.clicked.connect(self.open_song_library)
        layout.addWidget(all_songs)
        return frame

    def _card(self, title: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 9)
        layout.setSpacing(6)
        heading = QLabel(title)
        heading.setObjectName("cardTitle")
        layout.addWidget(heading)
        return card, layout

    def _build_dashboard_grid(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setHorizontalSpacing(SPACING["s"])
        grid.setVerticalSpacing(SPACING["s"])
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)

        workflow, w = self._card("🚀  Workflow Übersicht")
        claim = QLabel("Kreative Ideen.\nStrukturierte Workflows.\nStarke Ergebnisse.")
        claim.setAlignment(Qt.AlignCenter)
        w.addWidget(claim)
        for step in ("①  Idee erfassen", "②  DB-Eingaben ergänzen", "③  Funktionen nutzen", "④  Ergebnisse speichern"):
            hint = QLabel(step)
            hint.setObjectName("cardHint")
            w.addWidget(hint)
        w.addStretch(1)
        grid.addWidget(workflow, 0, 0)

        db, d = self._card("▦  DB-Eingaben")
        self.db_boxes: dict[str, QComboBox] = {}
        for label in ("Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten", "GitHub-Repositories", "Prompts"):
            row = QHBoxLayout()
            name = QLabel(label)
            name.setObjectName("cardHint")
            name.setFixedWidth(145)
            row.addWidget(name)
            combo = QComboBox()
            combo.addItem("Bitte auswählen …")
            row.addWidget(combo, 1)
            d.addLayout(row)
            self.db_boxes[label] = combo
        d.addStretch(1)
        grid.addWidget(db, 0, 1)

        functions, f = self._card("▣  Funktionen")
        function_row = QHBoxLayout()
        for text, command in (
            ("◈\nGenreszufallsgenerator\nZufällige Genres entdecken", lambda: self._planned("Genreszufallsgenerator")),
            ("✎\nReimfinder\nPassende Reime finden", lambda: self._planned("Reimfinder")),
        ):
            button = QPushButton(text)
            button.setObjectName("featureButton")
            button.clicked.connect(command)
            function_row.addWidget(button)
        f.addLayout(function_row)
        grid.addWidget(functions, 1, 0)

        system, s = self._card("▤  Systemanwendungen")
        for icon, title, subtitle in (
            ("⌕", "Datenbank-Suche", "Nach Dateien im System suchen"),
            ("▤", "Inhaltssuche Textdateien", "Inhalte in Textdateien durchsuchen"),
            ("≡", "Trefferliste", "Suchergebnisse anzeigen"),
            ("◫", "Duplikatprüfer", "Doppelte Dateien finden"),
        ):
            row = QHBoxLayout()
            icon_label = QLabel(icon)
            icon_label.setObjectName("accent")
            icon_label.setFixedWidth(28)
            row.addWidget(icon_label)
            text_box = QVBoxLayout()
            text_box.setSpacing(0)
            text_box.addWidget(QLabel(title))
            sub = QLabel(subtitle)
            sub.setObjectName("cardHint")
            text_box.addWidget(sub)
            row.addLayout(text_box, 1)
            s.addLayout(row)
        s.addStretch(1)
        grid.addWidget(system, 1, 1)
        return grid

    def _build_statusbar(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("statusBar")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 4, 10, 4)
        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("statusGood")
        layout.addWidget(self.status_dot)
        self.quick_status = QLabel("Bereit.")
        self.quick_status.setObjectName("muted")
        layout.addWidget(self.quick_status)
        layout.addStretch(1)
        smaller = QPushButton("A−")
        smaller.setToolTip("Schrift und Oberfläche verkleinern (Strg + Mausrad nach unten)")
        smaller.clicked.connect(lambda: self._step_zoom(-1))
        layout.addWidget(smaller)
        self.zoom_label = QLabel("100 %")
        self.zoom_label.setObjectName("muted")
        self.zoom_label.setMinimumWidth(52)
        self.zoom_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.zoom_label)
        larger = QPushButton("A+")
        larger.setToolTip("Schrift und Oberfläche vergrößern (Strg + Mausrad nach oben)")
        larger.clicked.connect(lambda: self._step_zoom(1))
        layout.addWidget(larger)
        tech = QLabel("Linux · PySide6 · Dark Orange Industrial")
        tech.setObjectName("muted")
        layout.addWidget(tech)
        return frame

    def _bind_shortcuts(self) -> None:
        QShortcut(QKeySequence("F5"), self, activated=self.refresh)
        QShortcut(QKeySequence("Ctrl++"), self, activated=lambda: self._step_zoom(1))
        QShortcut(QKeySequence("Ctrl+-"), self, activated=lambda: self._step_zoom(-1))
        QShortcut(QKeySequence("Ctrl+0"), self, activated=lambda: self.set_zoom(100))
        QShortcut(QKeySequence("Ctrl+R"), self, activated=self.open_recovery)

    def _is_managed_widget(self, watched: object) -> bool:
        if not isinstance(watched, QWidget):
            return False
        window = watched.window()
        managed = [self, *self._song_editors]
        if self._song_library is not None:
            managed.append(self._song_library)
        if self._recovery_center is not None:
            managed.append(self._recovery_center)
        return window in managed

    def eventFilter(self, watched: object, event: QEvent) -> bool:
        if (event.type() == QEvent.Type.Wheel
                and (event.modifiers() & Qt.KeyboardModifier.ControlModifier)
                and self._is_managed_widget(watched)):
            delta = event.angleDelta().y()
            if delta:
                self._step_zoom(1 if delta > 0 else -1)
                event.accept()
                return True
        return super().eventFilter(watched, event)

    def _planned(self, name: str) -> None:
        QMessageBox.information(self, "Geplanter Bereich", f"{name} ist im Dashboard vorgesehen, aber noch nicht als Fachfunktion freigegeben.")

    def _header_search(self) -> None:
        self.open_song_library(initial_search=self.search_entry.text().strip())

    def save_quick_info(self) -> None:
        try:
            target = append_developer_info(self.project_root, self.quick_entry.text())
        except ValueError:
            self.quick_status.setText("Bitte zuerst eine kurze Information eingeben.")
            return
        except Exception as error:
            self.quick_status.setText(f"Speichern fehlgeschlagen: {type(error).__name__}")
            return
        self.quick_entry.clear()
        self.quick_status.setText(f"An {target.name} angehängt.")
        self.quick_entry.setFocus()

    def refresh_recent_songs(self) -> None:
        while self.recent_layout.count():
            item = self.recent_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        paths = list_songs(self.project_root)[:5]
        if not paths:
            empty = QLabel("Noch keine Songs gespeichert.")
            empty.setObjectName("muted")
            self.recent_layout.addWidget(empty)
            return
        for path in paths:
            try:
                document = load_song(path)
            except (OSError, UnicodeError, ValueError):
                continue
            subtitle = document.genre or "ohne Genre"
            button = QPushButton(f"{document.title}\n{subtitle}")
            button.setToolTip(f"{document.title} öffnen")
            button.clicked.connect(lambda _checked=False, selected=path: self.open_song_path(selected))
            self.recent_layout.addWidget(button, 1)

    def open_song_editor(self) -> None:
        editor = SongEditor(self.project_root, zoom_percent=self.zoom_percent,
                            on_closed=self._song_editor_closed, on_saved=self._song_saved, parent=self)
        self._song_editors.append(editor)
        editor.show()

    def open_song_path(self, path: Path) -> None:
        try:
            document = load_song(path)
        except Exception as error:
            QMessageBox.critical(self, "Song konnte nicht geöffnet werden", str(error))
            return
        editor = SongEditor(self.project_root, zoom_percent=self.zoom_percent,
                            on_closed=self._song_editor_closed, document=document,
                            on_saved=self._song_saved, parent=self)
        self._song_editors.append(editor)
        editor.show()

    def open_song_library(self, initial_search: str = "") -> None:
        if self._song_library is not None and self._song_library.isVisible():
            if initial_search:
                self._song_library.set_search(initial_search)
            self._song_library.raise_()
            self._song_library.activateWindow()
            self._song_library.refresh()
            return
        self._song_library = SongLibrary(self.project_root, self.zoom_percent, self.open_song_path, parent=self)
        if initial_search:
            self._song_library.set_search(initial_search)
        self._song_library.show()

    def open_recovery(self) -> None:
        if self._recovery_center is not None and self._recovery_center.isVisible():
            self._recovery_center.raise_()
            self._recovery_center.activateWindow()
            self._recovery_center.refresh()
            return
        self._recovery_center = RecoveryCenter(self.texts, self.logger, self.zoom_percent, parent=self)
        self._recovery_center.show()

    def _song_saved(self, _path: Path) -> None:
        self.refresh_recent_songs()
        if self._song_library is not None:
            self._song_library.refresh()

    def _song_editor_closed(self, editor: SongEditor) -> None:
        if editor in self._song_editors:
            self._song_editors.remove(editor)
        self.refresh_recent_songs()

    def save_open_song_editors(self) -> bool:
        success = True
        for editor in list(self._song_editors):
            if editor.save(reason="Sitzung gespeichert") is None:
                success = False
        return success

    def logout(self) -> None:
        if not self.save_open_song_editors():
            QMessageBox.critical(self, "Logout gestoppt", "Mindestens ein Songtext konnte nicht gespeichert werden. Die Sitzung bleibt geöffnet.")
            return
        self._closing_after_save = True
        for editor in list(self._song_editors):
            editor.close_safely()
        self.close()

    def _remove_event_filter(self) -> None:
        if not self._event_filter_installed:
            return
        app = QApplication.instance()
        if app is not None:
            app.removeEventFilter(self)
        self._event_filter_installed = False

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._closing_after_save:
            self._remove_event_filter()
            self.closed_cleanly.emit()
            event.accept()
            return
        if not self.save_open_song_editors():
            QMessageBox.critical(self, "Schließen gestoppt", "Mindestens ein Songtext konnte nicht gespeichert werden.")
            event.ignore()
            return
        self._closing_after_save = True
        for editor in list(self._song_editors):
            editor.close_safely()
        self._remove_event_filter()
        self.closed_cleanly.emit()
        event.accept()

    def refresh(self) -> None:
        self.refresh_recent_songs()
        self.quick_status.setText("Bereit.")
        if self._recovery_center is not None and self._recovery_center.isVisible():
            self._recovery_center.refresh()

    def _step_zoom(self, direction: int) -> None:
        current = ZOOM_LEVELS.index(self.zoom_percent)
        target = max(0, min(len(ZOOM_LEVELS) - 1, current + direction))
        self.set_zoom(ZOOM_LEVELS[target])

    def set_zoom(self, percent: int) -> None:
        if percent not in ZOOM_LEVELS:
            return
        self.zoom_percent = percent
        apply_global_style(self, percent)
        self.zoom_label.setText(f"{percent} %")
        for editor in list(self._song_editors):
            editor.zoom_percent = percent
            apply_global_style(editor, percent)
        if self._song_library is not None:
            self._song_library.set_zoom(percent)
        if self._recovery_center is not None:
            self._recovery_center.set_zoom(percent)


def install_exception_handler(app, logger: EventLogger, refresh: Callable[[], None], parent: QWidget) -> None:
    """Qt-kompatibler zentraler Ausnahmehandler; wird von main über sys.excepthook verdrahtet."""
    import sys

    def report(kind: type[BaseException], error: BaseException, trace: object) -> None:
        try:
            event = logger.record(
                severity="FEHLER", area="OBERFLAECHE",
                summary="Eine Aktion wurde sicher abgebrochen.", cause=str(error) or "Unbekannter Programmfehler",
                protection="Die betroffene Aktion wurde beendet; andere Bereiche bleiben verfügbar.",
                next_step="Öffnen Sie Recovery und folgen Sie dem dort genannten Schritt.", exception=error,
            )
            refresh()
            QMessageBox.critical(parent, "Aktion sicher beendet", f"{event['summary']}\n\n{event['next_step']}\n\nKennung: {event['event_id']}")
        except Exception as logging_error:
            QMessageBox.critical(parent, "Sicherer Abbruch", f"Die Aktion wurde beendet. Das Protokoll konnte nicht geschrieben werden: {logging_error}")
        finally:
            sys.__excepthook__(kind, error, trace)
    sys.excepthook = report