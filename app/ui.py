"""PySide6-Multimodul-Dashboard mit klarer Laienführung."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtGui import QCloseEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QSizePolicy, QSplitter, QVBoxLayout, QWidget, QMenu, QToolButton,
    QScrollArea, QStackedWidget, QLayout,
)

from app.calendar_reminders import CalendarReminderController
from app.calendar_window import CalendarWindow
from app.character_window import CharacterWindow
from app.book_window import BookWindow
from app.snippet_window import SnippetWindow
from app.search_window import SearchWindow
from app.idea_window import IdeaWindow
from app.account_window import AccountWindow
from app.quicklinks_window import QuicklinksWindow
from app.wiki_window import WikiWindow
from app.module_controls_window import ModuleControlsWindow
from app.module_blueprints_window import BlueprintWindow
from app.development_pool_window import DevelopmentPoolWindow
from app.audio_player_window import AudioPlayerWindow
from app.image_preview_window import ImagePreviewWindow
from app.slideshow_window import SlideshowWindow
from app import module_contracts
from app.quicklinks_rail import QuicklinksRail
from app.module_widgets import t as module_text
from app.event_log import EventLogger
from app.profile_editor import ProfileEditor
from app.profile_quick_entry import ProfileQuickEntry, t as quick_text
from app.genre_random_window import GenreRandomWindow
from app.github_projects_window import GitHubProjectsWindow
from app.profile_store import CATEGORIES, profile_names, read_profile
from app.quick_note import append_developer_info, legacy_notes_pending, preserve_legacy_notes
from app.recovery_center import RecoveryCenter
from app.recovery_ui import ZOOM_LEVELS
from app.song_document import list_songs, load_song
from app.song_editor import SongEditor
from app.song_library import SongLibrary
from app.texts import TextRegistry
from app.todo_window import TodoWindow
from app.text_editor_window import TextEditorWindow
from app.ui_standards import COLORS, SPACING, apply_global_style
from app.window_lifecycle import (
    _ManagedWindowRegistration, _activate_window, _open_managed_window,
    _prepare_module_window, _show_module_window,
)


class _DashboardCardDivider(QFrame):
    """Schmale, per Maus und Pfeiltasten bedienbare Raster-Trennlinie."""

    def __init__(self, dashboard: "Dashboard", axis: str, name: str) -> None:
        super().__init__()
        self.dashboard = dashboard
        self.axis = axis
        self._dragging = False
        self.setObjectName(name)
        self.setAccessibleName(
            "Dashboard-Karten links und rechts verstellen"
            if axis == "column" else "Dashboard-Karten oben und unten verstellen"
        )
        self.setToolTip("Mit der Maus ziehen oder mit den Pfeiltasten verstellen.")
        self.setFocusPolicy(Qt.StrongFocus)
        if axis == "column":
            self.setFixedWidth(10)
            self.setCursor(Qt.SplitHCursor)
        else:
            self.setFixedHeight(10)
            self.setCursor(Qt.SplitVCursor)

    def _move_at(self, global_position) -> None:
        parent = self.parentWidget()
        if parent is not None:
            point = parent.mapFromGlobal(global_position)
            self.dashboard._adjust_dashboard_card_divider(
                self.axis, point.x() if self.axis == "column" else point.y()
            )

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self.setFocus()
            self._move_at(event.globalPosition().toPoint())
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._dragging and event.buttons() & Qt.LeftButton:
            self._move_at(event.globalPosition().toPoint())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton and self._dragging:
            self._dragging = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def keyPressEvent(self, event) -> None:
        directions = (
            (Qt.Key_Left, Qt.Key_Right) if self.axis == "column"
            else (Qt.Key_Up, Qt.Key_Down)
        )
        if event.key() in directions:
            first = self.dashboard.dashboard_grid.cellRect(0, 0)
            position = first.right() if self.axis == "column" else first.bottom()
            offset = -30 if event.key() == directions[0] else 30
            self.dashboard._adjust_dashboard_card_divider(self.axis, position + offset)
            event.accept()
        else:
            super().keyPressEvent(event)


class Dashboard(QWidget):
    """Hauptfenster mit klarer Trennung zwischen fertigen und geplanten Bereichen."""

    closed_cleanly = Signal()

    def __init__(self, texts: TextRegistry, logger: EventLogger,
                 project_root: Path | None = None) -> None:
        super().__init__()
        self.texts, self.logger = texts, logger
        self.project_root = project_root or Path.cwd()
        self.zoom_percent = 100
        self._song_editors: list[SongEditor] = []
        self._song_library: SongLibrary | None = None
        self._song_library_hidden_for_editor_session = False
        self._recovery_center: RecoveryCenter | None = None
        self._profile_editor: ProfileEditor | None = None
        self._genre_random_window: GenreRandomWindow | None = None
        self._github_projects_window: GitHubProjectsWindow | None = None
        self._todo_window: TodoWindow | None = None
        self._calendar_window: CalendarWindow | None = None
        self._character_window: CharacterWindow | None = None
        self._text_editor_window: TextEditorWindow | None = None
        self._book_window: BookWindow | None = None
        self._snippet_window: SnippetWindow | None = None
        self._search_window: SearchWindow | None = None
        self._idea_window: IdeaWindow | None = None
        self._account_window: AccountWindow | None = None
        self._quicklinks_window: QuicklinksWindow | None = None
        self._wiki_window: WikiWindow | None = None
        self._module_controls_window: ModuleControlsWindow | None = None
        self._blueprint_window: BlueprintWindow | None = None
        self._development_pool_window: DevelopmentPoolWindow | None = None
        self._audio_window: AudioPlayerWindow | None = None
        self._pictures_window: ImagePreviewWindow | None = None
        self._slideshow_window: SlideshowWindow | None = None
        self.nav_collapsed = False
        self._sidebar_manual_width: int | None = None
        self._nav_entries: list[QWidget] = []
        self._closing_after_save = False
        self._event_filter_installed = False

        self.setObjectName("dashboardShell")
        title = self.texts.get("app.window_title", "Provoware-Datenbank-Dashboard 2026")
        version = getattr(logger, "version", "")
        self.setWindowTitle(f"{title} · {version}" if isinstance(version, str) and version else title)
        self.resize(1280, 790)
        self.setMinimumSize(1020, 650)
        self._build()
        self._bind_shortcuts()
        apply_global_style(self, self.zoom_percent)
        self._calendar_reminders = CalendarReminderController(
            self.project_root, self._show_calendar_reminder,
            self._calendar_reminder_error, parent=self,
        )
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
        self.dashboard_splitter = QSplitter(Qt.Horizontal)
        self.dashboard_splitter.setObjectName("dashboardAreaSplitter")
        self.dashboard_splitter.setAccessibleName("Verstellbare Navigation und Arbeitsfläche")
        self.dashboard_splitter.setHandleWidth(10)
        self.dashboard_splitter.setChildrenCollapsible(False)
        self.dashboard_splitter.addWidget(self.sidebar)

        main = QVBoxLayout()
        main.setSpacing(SPACING["s"])
        main.addWidget(self._build_quick_info())
        main.addWidget(self._build_recent_strip())
        main.addLayout(self._build_dashboard_grid(), 1)
        main_widget = QWidget()
        main_widget.setLayout(main)
        self.dashboard_splitter.addWidget(main_widget)
        self.dashboard_splitter.setStretchFactor(1, 1)
        self.dashboard_splitter.handle(1).setToolTip(
            "Mit der Maus verschieben: Navigation breiter oder schmaler machen."
        )
        self.dashboard_splitter.splitterMoved.connect(self._remember_sidebar_width)
        body.addWidget(self.dashboard_splitter, 1)
        self.quicklinks_rail = QuicklinksRail(self.project_root, self.open_quicklinks, self)
        body.addWidget(self.quicklinks_rail)
        self.quicklinks_rail.hide()  # Schmale Geräte behalten den vollen Hauptbereich.
        outer.addLayout(body, 1)
        outer.addWidget(self._build_statusbar())

    def _build_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("header")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(12, 7, 10, 7)
        layout.setSpacing(8)

        logo = QToolButton()
        logo.setText("▦")
        logo.setAccessibleName(module_text("more_modules", "Weitere Module öffnen"))
        logo.setToolTip(module_text("more_modules", "Weitere Module öffnen"))
        logo.setPopupMode(QToolButton.InstantPopup)
        logo.setStyleSheet(f"font-size: 18pt; color: {COLORS['accent']};")
        self.module_menu = QMenu(logo)
        self._optional_actions = {
            "ideas": self.module_menu.addAction(module_text("ideas", "Textfragmente & Ideenarchiv"), self.open_ideas),
            "accounts": self.module_menu.addAction(module_text("accounts", "Profil- & Accountmanager"), self.open_accounts),
            "quicklinks": self.module_menu.addAction(module_text("quicklinks", "Link-Schnellstarter"), self.open_quicklinks),
            "wiki": self.module_menu.addAction(module_text("wiki", "Wiki · Wissenssammlungen"), self.open_wiki),
            "audio": self.module_menu.addAction("Audioplayer", self.open_audio_player),
            "pictures": self.module_menu.addAction("Bildvorschau", self.open_picture_preview),
            "slideshow": self.module_menu.addAction("Video & Slideshow", self.open_slideshow),
        }
        self.module_menu.addSeparator()
        self.module_menu.addAction("Module verwalten", self.open_module_controls)
        self.module_menu.addAction("Modulbaukasten · Entwürfe", self.open_module_blueprints)
        self.module_menu.addAction("Entwicklungspool · Projekte", self.open_development_pool)
        # Bereichsverteilung anpassen, ohne die bestehenden Karten umzubauen.
        self.area_size_menu = self.module_menu.addMenu("Dashboard-Bereichsgrößen")
        for label, left, right in (
            ("Gleich breit", 1, 1),
            ("Links etwas breiter", 3, 2),
            ("Rechts etwas breiter", 2, 3),
        ):
            action = self.area_size_menu.addAction(label)
            action.triggered.connect(
                lambda _checked=False, ratio=(left, right): self.set_dashboard_column_ratio(*ratio)
            )
        self.module_menu.addAction("Navigationsbreite zurücksetzen", self.reset_sidebar_width)
        logo.setMenu(self.module_menu)
        layout.addWidget(logo)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        title = QLabel("Provoware-Datenbank-Dashboard 2026")
        title.setObjectName("appTitle")
        self.app_title_label = title
        subtitle = QLabel("Deine Zentrale für Songs, Planung und Projektvorgaben")
        subtitle.setObjectName("subtitle")
        self.header_subtitle = subtitle
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        layout.addLayout(title_box)
        layout.addStretch(1)

        search_icon = QLabel("⌕")
        search_icon.setObjectName("accent")
        self.header_search_icon = search_icon
        layout.addWidget(search_icon)
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText(module_text("search_query", "Suchtext eingeben …"))
        self.search_entry.setToolTip(module_text("search_title", "Dateien & Texte suchen"))
        self.search_entry.setFixedWidth(245)
        self.search_entry.returnPressed.connect(self._header_search)
        layout.addWidget(self.search_entry)
        self.quit_button = QPushButton("Programm beenden")
        self.quit_button.setObjectName("dangerButton")
        self.quit_button.setToolTip("Speichert zuerst offene Songtexte und beendet danach das Programm.")
        self.quit_button.clicked.connect(self.logout)
        layout.addWidget(self.quit_button)
        return header

    @staticmethod
    def _mark_planned(button: QPushButton, name: str) -> None:
        button.setProperty("planned", True)
        button.setToolTip(f"{name} ist sichtbar vorbereitet, aber noch nicht fertig nutzbar.")

    def _build_tile_strip(self) -> QHBoxLayout:
        strip = QHBoxLayout()
        strip.setSpacing(SPACING["xs"])
        tiles = (
            ("♫\nSongtexte", self.open_song_library, False, "Songtexte"),
            ("♙\nCharakterfibel", self.open_character_fibel, False, "Charakterfibel"),
            ("✎\nTexteditor", self.open_text_editor, False, "Texteditor"),
            ("▥\nGenres", lambda: self.open_profile_editor("Genres"), False, "Genres"),
            (module_text("snippet_tile", "▣\nTextbuttons"), self.open_snippets, False, "Textbuttons"),
            (module_text("search_tile", "⌕\nDateisuche"), self.open_search, False, "Dateisuche"),
            (module_text("book_tile", "▤\nBücher"), self.open_books, False, "Buchwerkstatt"),
        )
        for text, command, planned, name in tiles:
            button = QPushButton(text)
            button.setObjectName("tileButton")
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setProperty("ready", not planned)
            if planned:
                self._mark_planned(button, name)
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
        menu_button.setToolTip("Navigation ein- oder ausklappen")
        menu_button.setFixedWidth(42)
        menu_button.clicked.connect(self.toggle_sidebar)
        top.addWidget(menu_button)
        nav_title = QLabel("Navigation")
        nav_title.setObjectName("muted")
        top.addWidget(nav_title)
        top.addStretch(1)
        layout.addLayout(top)

        self._add_nav(layout, "▦  Übersicht", lambda: None, active=True)
        self._add_nav(layout, "◈  Alle Bereiche · geplant", lambda: self._planned("Alle Bereiche"), planned=True)
        self._add_heading(layout, "Schreiben")
        self._add_nav(layout, "  ♫  Songtexte", self.open_song_library)
        self._add_nav(layout, "  ✎  Texteditor", self.open_text_editor)
        self._add_nav(layout, "  ♙  Charakterfibel", self.open_character_fibel)
        self._add_nav(layout, module_text("snippets", "Textbaustein-Buttons"), self.open_snippets)
        self._add_nav(layout, module_text("books", "Buchwerkstatt"), self.open_books)
        self._add_nav(layout, "  ▣  Hörspiele · geplant", lambda: self._planned("Hörspiele"), planned=True)
        self._add_nav(layout, "  ▤  Blogartikel · geplant", lambda: self._planned("Blogartikel"), planned=True)
        self._add_heading(layout, "Daten & Vorgaben")
        for label in CATEGORIES:
            self._add_nav(layout, f"  ·  {label}", lambda _checked=False, item=label: self.open_profile_editor(item))
        self._add_nav(layout, "  ·  GitHub-Projekte", self.open_github_projects)
        self._add_nav(layout, "  ·  Prompts · geplant", lambda: self._planned("Prompts"), planned=True)
        self._add_heading(layout, "Funktionen")
        self._add_nav(layout, "  ◉  Genre-Zufall", self.open_genre_random)
        self._add_nav(layout, "  ✎  Reimfinder · geplant", lambda: self._planned("Reimfinder"), planned=True)
        self._add_heading(layout, "Dateien & Werkzeuge")
        self._add_nav(layout, "  ◫  Duplikatprüfer · geplant", lambda: self._planned("Duplikatprüfer"), planned=True)
        self._add_heading(layout, "Planung")
        self.todo_nav_button = self._add_nav(layout, "  ✓  Todo-Liste", self.open_todo)
        self.calendar_nav_button = self._add_nav(layout, "  ▦  Kalender", self.open_calendar)
        self._add_heading(layout, "Hilfe")
        self.recovery_nav_button = self._add_nav(layout, "  ⓘ  Hilfe && Fehlerhilfe", self.open_recovery)
        layout.addStretch(1)
        return sidebar

    def _add_heading(self, layout: QVBoxLayout, text: str) -> None:
        label = QLabel(f"⌄  {text}")
        label.setObjectName("muted")
        label.setContentsMargins(8, 6, 2, 2)
        layout.addWidget(label)
        self._nav_entries.append(label)

    def _add_nav(self, layout: QVBoxLayout, text: str, command: Callable[[], None],
                 active: bool = False, planned: bool = False) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("activeNav" if active else "navButton")
        if planned:
            self._mark_planned(button, text.replace("· geplant", "").strip())
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
        self.quick_info_label = QLabel("Projekt-Notiz:")
        layout.addWidget(self.quick_info_label)
        self.quick_entry = QLineEdit()
        self.quick_entry.setPlaceholderText("Kurze Notiz für dieses Projekt …")
        self.quick_entry.setToolTip("Die Notiz wird fortlaufend gespeichert. Vorhandene Notizen bleiben erhalten.")
        self.quick_entry.returnPressed.connect(self.save_quick_info)
        layout.addWidget(self.quick_entry, 1)
        save = QPushButton("Notiz speichern")
        self.quick_save_button = save
        save.clicked.connect(self.save_quick_info)
        layout.addWidget(save)
        return frame

    def _build_recent_strip(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("toolbar")
        self.recent_frame = frame
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 5, 8, 5)
        label = QLabel("Zuletzt bearbeitete Songs")
        label.setObjectName("muted")
        self.recent_label = label
        layout.addWidget(label)
        self.recent_layout = QHBoxLayout()
        self.recent_layout.setSpacing(4)
        layout.addLayout(self.recent_layout, 1)

        # Bei 175/200 % ersetzt eine platzsparende Auswahl die breite Buttonreihe.
        # Die normalen Schnellbuttons bleiben darunter erhalten und werden nur
        # darstellungsabhängig ein-/ausgeblendet.
        self.recent_combo = QComboBox()
        self.recent_combo.setObjectName("recent_song_selector")
        self.recent_combo.setAccessibleName("Zuletzt bearbeitete Songs")
        self.recent_combo.setToolTip("Wähle einen zuletzt bearbeiteten Song aus.")
        self.recent_combo.hide()
        layout.addWidget(self.recent_combo, 1)
        self.recent_open_button = QPushButton("Song öffnen")
        self.recent_open_button.setToolTip("Öffnet den ausgewählten zuletzt bearbeiteten Song in einem eigenen Fenster.")
        self.recent_open_button.clicked.connect(self._open_recent_selected)
        self.recent_open_button.hide()
        layout.addWidget(self.recent_open_button)

        self.recent_all_button = QPushButton("Alle Songs")
        self.recent_all_button.clicked.connect(self.open_song_library)
        layout.addWidget(self.recent_all_button)
        self._recent_widgets: list[QWidget] = []
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

    def _remember_sidebar_width(self, _position: int, _handle: int) -> None:
        """Nur bewusstes Verschieben merkt sich die Navigation innerhalb der Sitzung."""
        if not self.nav_collapsed:
            self._sidebar_manual_width = self.sidebar.width()

    def reset_sidebar_width(self) -> None:
        """Stellt die Bildschirm- und Schriftgrößen-abhängige Standardbreite wieder her."""
        self._sidebar_manual_width = None
        from app.ui_standards import refresh_responsive_layout
        refresh_responsive_layout(self)

    def set_dashboard_column_ratio(self, left: int, right: int) -> None:
        """Verteilt den Platz der vorhandenen Karten ohne deren Inhalt zu ändern."""
        if (left, right) not in {(1, 1), (3, 2), (2, 3)}:
            return
        self.dashboard_grid.setColumnStretch(0, left)
        self.dashboard_grid.setColumnStretch(2, right)
        self.dashboard_grid.invalidate()

    def _adjust_dashboard_card_divider(self, axis: str, position: int) -> None:
        """Verstellt Rasteranteile, ohne bestehende Karten oder Inhalte zu ersetzen."""
        grid = self.dashboard_grid
        first = grid.cellRect(0, 0)
        if axis == "column":
            second = grid.cellRect(0, 2)
            total = first.width() + second.width()
            minimum = min(310, max(1, (total - 1) // 2))
            left = max(minimum, min(total - minimum, position - first.left()))
            grid.setColumnStretch(0, max(1, left))
            grid.setColumnStretch(2, max(1, total - left))
        elif axis == "row" and self.dashboard_row_handle.isVisible():
            second = grid.cellRect(2, 0)
            total = first.height() + second.height()
            minimum = min(185, max(1, (total - 1) // 2))
            top = max(minimum, min(total - minimum, position - first.top()))
            self._dashboard_card_row_weights = (max(1, top), max(1, total - top))
            grid.setRowStretch(0, self._dashboard_card_row_weights[0])
            grid.setRowStretch(2, self._dashboard_card_row_weights[1])
        grid.invalidate()

    def _build_start_card(self) -> QFrame:
        card, layout = self._card(module_text('start_title', 'Was möchtest du tun?'))
        self.start_card = card
        self.start_actions = {}
        actions = QGridLayout()
        actions.setSpacing(6)
        actions.setColumnStretch(0, 1)
        actions.setColumnStretch(1, 1)
        for index, (key, label, command, tooltip) in enumerate((
            ('song', 'Song schreiben', self.open_song_editor, 'Öffnet einen neuen Song. Vorhandene Songeditoren bleiben erhalten.'),
            ('text', 'Text schreiben', self.start_writing_text, 'Beginne einen Text oder schreibe in deinem offenen Entwurf weiter.'),
            ('todo', 'Aufgabe planen', self.start_task, 'Öffnet die Aufgabenliste und setzt den Fokus in die Eingabe.'),
            ('calendar', 'Termin anlegen', self.start_event, 'Öffnet den Kalender. Eine begonnene Termineingabe bleibt erhalten.'),
        )):
            action = QPushButton(module_text('start_' + key, label))
            action.setObjectName('start_' + key)
            action.setAccessibleName(module_text('start_' + key, label))
            action.setToolTip(module_text('start_' + key + '_tooltip', tooltip))
            action.clicked.connect(command)
            self.start_actions[key] = action
            actions.addWidget(action, index // 2, index % 2)
        layout.addLayout(actions)
        layout.addStretch(1)
        return card

    def start_writing_text(self) -> None:
        current = self._text_editor_window
        if current is not None and current.isVisible():
            # Ein Refresh könnte die gespeicherte Auswahl neu laden und den Entwurf stören.
            _activate_window(current)
        else:
            self.open_text_editor()
        editor = self._text_editor_window
        if editor.title_entry.text().strip():
            editor.text_edit.setFocus()
        else:
            editor.title_entry.setFocus()

    def start_task(self) -> None:
        self.open_todo()
        self._todo_window.title_entry.setFocus()

    def start_event(self) -> None:
        self.open_calendar()
        self._calendar_window.title_entry.setFocus()

    def _build_dashboard_grid(self) -> QGridLayout:
        grid = QGridLayout()
        self.dashboard_grid = grid
        # Original-Raster bewahren: keine Qt-Splitter-Mindestgrößenkaskade.
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(2, 1)
        self._dashboard_card_row_weights = (1, 1)

        grid.addWidget(self._build_start_card(), 0, 0)
        self.dashboard_column_handle_top = _DashboardCardDivider(
            self, "column", "dashboardCardColumnTop"
        )
        self.dashboard_column_handle_bottom = _DashboardCardDivider(
            self, "column", "dashboardCardColumnBottom"
        )
        self.dashboard_row_handle = _DashboardCardDivider(
            self, "row", "dashboardCardRow"
        )
        grid.addWidget(self.dashboard_column_handle_top, 0, 1)
        grid.addWidget(self.dashboard_column_handle_bottom, 2, 1)
        grid.addWidget(self.dashboard_row_handle, 1, 0, 1, 3)

        db, d = self._card("▦  Daten & Vorgaben")
        d.setSpacing(5)
        heading = d.takeAt(0).widget()
        profile_row = QHBoxLayout()
        if heading is not None:
            heading.setText("▦  Vorgaben")
            profile_row.addWidget(heading)
        profile_row.addStretch(1)
        profile_label = QLabel("Profil:")
        profile_label.setObjectName("cardHint")
        profile_row.addWidget(profile_label)
        self.db_profile_combo = QComboBox()
        self.db_profile_combo.setMinimumWidth(150)
        self.db_profile_combo.setToolTip("Ein Profil bündelt passende Genres, Stimmungen, Stil, Stimme und Besonderheiten.")
        self.db_profile_combo.currentTextChanged.connect(self._load_profile_values)
        profile_row.addWidget(self.db_profile_combo)
        edit_profiles = QPushButton("Profile & Werte bearbeiten")
        edit_profiles.setObjectName("profileEditButton")
        edit_profiles.setAccessibleName("Profile & Werte bearbeiten")
        edit_profiles.clicked.connect(self.open_profile_editor)
        edit_profiles.setToolTip("Profile und gespeicherte Werte bearbeiten")
        # Keine zusätzliche Zeile: In kleinen Karten würde sie die nachfolgenden
        # Kombinationsfelder verdrängen. Die kurze Beschriftung passt daneben.
        profile_row.addWidget(edit_profiles)
        d.insertLayout(0, profile_row)

        self.db_pages = QStackedWidget()
        self.db_selection_page = QWidget()
        selection = QVBoxLayout(self.db_selection_page)
        selection.setContentsMargins(0, 0, 0, 0)
        selection.setSpacing(5)
        selection.setSizeConstraint(QLayout.SetMinimumSize)
        self.db_boxes: dict[str, QComboBox] = {}
        for label in CATEGORIES:
            row = QHBoxLayout()
            name = QLabel(label)
            name.setObjectName("cardHint")
            name.setFixedWidth(145)
            row.addWidget(name)
            combo = QComboBox()
            combo.addItem("Bitte auswählen …")
            row.addWidget(combo, 1)
            selection.addLayout(row)
            self.db_boxes[label] = combo
        project_open = QPushButton("◈  GitHub-Projekte öffnen")
        self.github_project_open_button = project_open
        project_open.setAccessibleName("GitHub-Projekte öffnen")
        project_open.setToolTip("Lokale Übersicht der offenen und fertigen Projekte öffnen")
        project_open.clicked.connect(self.open_github_projects)
        actions = QHBoxLayout()
        actions.addWidget(project_open)
        self.db_quick_button = QPushButton(quick_text('open', 'Werte ergänzen'))
        self.db_quick_button.clicked.connect(self.open_profile_quick_entry)
        actions.addWidget(self.db_quick_button)
        actions.addStretch(1)
        selection.addLayout(actions)
        selection.addStretch(1)
        self.db_selection_scroll = QScrollArea()
        self.db_selection_scroll.setWidgetResizable(True)
        self.db_selection_scroll.setWidget(self.db_selection_page)
        self.db_pages.addWidget(self.db_selection_scroll)
        self.profile_quick_entry = ProfileQuickEntry(self.project_root, logger=self.logger)
        self.db_quick_scroll = QScrollArea()
        self.db_quick_scroll.setWidgetResizable(True)
        self.db_quick_scroll.setWidget(self.profile_quick_entry)
        self.db_pages.addWidget(self.db_quick_scroll)
        self.profile_quick_entry.back_requested.connect(self.close_profile_quick_entry)
        self.profile_quick_entry.editing_requested.connect(self.open_profile_quick_entry)
        self.profile_quick_entry.reveal_requested.connect(self._reveal_profile_control)
        self.profile_quick_entry.saved.connect(self._profile_values_added)
        d.addWidget(self.db_pages, 1)
        grid.addWidget(db, 0, 2)

        functions, f = self._card("▣  Funktionen · In Planung")
        function_row = QHBoxLayout()
        for text, name in (
            ("◈\nGenre-Zufall", "Genre-Zufall"),
            ("✎\nReimfinder\nIn Planung", "Reimfinder"),
        ):
            button = QPushButton(text)
            button.setObjectName("featureButton")
            if name == "Genre-Zufall":
                button.clicked.connect(self.open_genre_random)
            else:
                self._mark_planned(button, name)
                button.clicked.connect(lambda _checked=False, selected=name: self._planned(selected))
            function_row.addWidget(button)
        f.addLayout(function_row)
        grid.addWidget(functions, 2, 0)

        system, s = self._card(module_text("search_tools", "▤  Dateien & Werkzeuge"))
        for title, subtitle in (
            ("⌕  Dateisuche", "Dateien nach Namen finden"),
            ("▤  Textinhalt suchen", "Wörter in Textdateien finden"),
            ("≡  Trefferliste", "Gefundene Dateien gesammelt anzeigen"),
            ("◫  Duplikatprüfer", "Doppelte Dateien finden"),
        ):
            planned = "Duplikatprüfer" in title
            button = QPushButton(f"{title} · In Planung" if planned else title)
            button.setToolTip(subtitle)
            if planned:
                self._mark_planned(button, title)
                button.clicked.connect(lambda _checked=False, selected=title: self._planned(selected))
            else:
                button.clicked.connect(self.open_search)
            s.addWidget(button)
        s.addStretch(1)
        grid.addWidget(system, 2, 2)
        return grid

    def _build_statusbar(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("statusBar")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 4, 10, 4)
        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("statusGood")
        layout.addWidget(self.status_dot)
        self.quick_status = QLabel(module_text("start_ready", "Bereit · Wähle eine Tätigkeit."))
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
        legend = QLabel("Gestrichelt = noch nicht fertig")
        legend.setObjectName("muted")
        layout.addWidget(legend)
        return frame

    def _bind_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+Alt+A"), self, activated=self.open_accounts)
        QShortcut(QKeySequence("Ctrl+Alt+I"), self, activated=self.open_ideas)
        QShortcut(QKeySequence("Ctrl+Alt+L"), self, activated=self.open_quicklinks)
        QShortcut(QKeySequence("Ctrl+Alt+W"), self, activated=self.open_wiki)
        QShortcut(QKeySequence("Ctrl+Alt+M"), self, activated=self.open_module_controls)
        QShortcut(QKeySequence("Ctrl+Alt+E"), self, activated=self.open_module_blueprints)
        QShortcut(QKeySequence("Ctrl+Alt+P"), self, activated=self.open_development_pool)
        QShortcut(QKeySequence("Ctrl+Alt+U"), self, activated=self.open_audio_player)
        QShortcut(QKeySequence("Ctrl+Alt+O"), self, activated=self.open_picture_preview)
        QShortcut(QKeySequence("Ctrl+Alt+V"), self, activated=self.open_slideshow)
        QShortcut(QKeySequence("Ctrl+Shift+F"), self, activated=self.open_search)
        QShortcut(QKeySequence("Ctrl+Alt+T"), self, activated=self.open_snippets)
        QShortcut(QKeySequence("Ctrl+Alt+B"), self, activated=self.open_books)
        QShortcut(QKeySequence("Ctrl+Shift+G"), self, activated=self.open_github_projects)
        QShortcut(QKeySequence("F5"), self, activated=self.refresh)
        QShortcut(QKeySequence("Ctrl++"), self, activated=lambda: self._step_zoom(1))
        QShortcut(QKeySequence("Ctrl+-"), self, activated=lambda: self._step_zoom(-1))
        QShortcut(QKeySequence("Ctrl+0"), self, activated=lambda: self.set_zoom(100))
        QShortcut(QKeySequence("Ctrl+R"), self, activated=self.open_recovery)
        QShortcut(QKeySequence("F1"), self, activated=self.open_recovery)

    @staticmethod
    def _set_song_editor_zoom(editor: SongEditor, percent: int) -> None:
        """Wendet den bestehenden Songeditor-Zoom über denselben Registry-Vertrag an."""
        editor.zoom_percent = percent
        apply_global_style(editor, percent)

    def _managed_window_registry(self) -> tuple[_ManagedWindowRegistration, ...]:
        """Liefert alle aktuell vom Dashboard verwalteten Fenster aus einer Quelle.

        Neben der Fensterreferenz enthält der Eintrag nur die gemeinsamen Aktionen,
        die für genau dieses Fenster gelten. Dadurch bleiben Sonderfälle explizit,
        während Fenstererkennung, Zoom und Dashboard-Refresh dieselbe Registry nutzen.
        """
        registrations: list[_ManagedWindowRegistration] = [
            _ManagedWindowRegistration(self),
        ]
        for editor in tuple(self._song_editors):
            registrations.append(
                _ManagedWindowRegistration(
                    editor,
                    apply_zoom=lambda percent, editor=editor: self._set_song_editor_zoom(editor, percent),
                )
            )

        optional_windows = (
            (self._song_library, False),
            (self._recovery_center, True),
            (self._profile_editor, False),
            (self._genre_random_window, False),
            (self._github_projects_window, False),
            (self._todo_window, True),
            (self._calendar_window, True),
            (self._character_window, False),
            (self._text_editor_window, False),
            (self._book_window, False),
            (self._snippet_window, False),
            (self._search_window, False),
            (self._idea_window, False),
            (self._account_window, False),
            (self._quicklinks_window, False),
            (self._wiki_window, False),
            (self._module_controls_window, False),
            (self._blueprint_window, False),
            (self._development_pool_window, False),
            (self._audio_window, False),
            (self._pictures_window, False),
            (self._slideshow_window, False),
        )
        for window, refresh_with_dashboard in optional_windows:
            if window is None:
                continue
            registrations.append(
                _ManagedWindowRegistration(
                    window,
                    apply_zoom=window.set_zoom,
                    refresh_when_visible=window.refresh if refresh_with_dashboard else None,
                )
            )
        return tuple(registrations)

    def _is_managed_widget(self, watched: object) -> bool:
        if not isinstance(watched, QWidget):
            return False
        window = watched.window()
        return any(window is registration.window for registration in self._managed_window_registry())

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
        QMessageBox.information(
            self,
            "Noch nicht verfügbar",
            f"{name} ist bereits eingeplant, aber noch nicht fertig nutzbar.\n\n"
            "Hier wird nichts gespeichert oder verändert. Nutze bis dahin einen Bereich ohne „In Planung“.",
        )

    def _header_search(self) -> None:
        self.open_search()
        if self.search_entry.text().strip():
            self._search_window.cancel()
            self._search_window.query.setText(self.search_entry.text().strip())
            self._search_window.start()

    def _offer_legacy_notes(self) -> bool | None:
        if getattr(self, '_legacy_notes_declined', False):
            return False
        if not legacy_notes_pending(self.project_root):
            return True
        dialog = QMessageBox(self)
        dialog.setWindowTitle(module_text('notes_legacy_title', 'Alte Projekt-Notizen übernehmen?'))
        dialog.setTextFormat(Qt.PlainText)
        dialog.setText(module_text('notes_legacy_question',
            'Alte Notizen liegen noch außerhalb der persönlichen Datensicherung. '
            'Eine unveränderte Kopie in den Datenordner übernehmen? '
            'Die ursprüngliche Datei bleibt erhalten. Bei Nein werden nur neue Notizen dort gespeichert; '
            'alte Notizen sind dann weiterhin nicht im persönlichen Daten-ZIP enthalten.'))
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        dialog.setDefaultButton(QMessageBox.Cancel)
        answer = dialog.exec()
        if answer == QMessageBox.Cancel:
            return None
        if answer == QMessageBox.No:
            self._legacy_notes_declined = True
            return False
        preserve_legacy_notes(self.project_root, approved=True)
        return True

    def _record_note_failure(self, error: Exception) -> None:
        record = getattr(self.logger, 'record', None)
        if not callable(record):
            return
        try:
            record(severity='ERROR', area='PROJEKT_NOTIZ',
                   summary=module_text('notes_failed', 'Notiz nicht gespeichert. Eingabe bleibt erhalten.'),
                   cause=str(error),
                   protection=module_text('notes_error_protection',
                       'Aktuelle Eingabe und ursprüngliche Altdatei wurden nicht verworfen.'),
                   next_step=module_text('notes_error_next',
                       'Unter F1 die Fehlermeldung prüfen: Schreibrechte, freien Speicher, Notizgröße und mögliche Dateikonflikte kontrollieren.'),
                   exception=error)
        except Exception:
            # Eine defekte Diagnoseablage darf die noch offene Eingabe nicht gefährden.
            return

    def save_quick_info(self) -> None:
        if not self.quick_entry.text().strip():
            self.quick_status.setText(module_text('notes_empty', 'Bitte zuerst eine kurze Projekt-Notiz eingeben.'))
            return
        try:
            legacy_included = self._offer_legacy_notes()
            if legacy_included is None:
                return
            append_developer_info(self.project_root, self.quick_entry.text())
        except Exception as error:
            self.quick_status.setText(module_text('notes_failed',
                'Notiz nicht gespeichert. Eingabe bleibt erhalten.'))
            self._record_note_failure(error)
            return
        self.quick_entry.clear()
        message = module_text('notes_saved', 'Projekt-Notiz im Datenordner gespeichert.')
        if not legacy_included:
            message = module_text('notes_legacy_excluded', 'Neue Notiz gespeichert; alte Notizen sind noch nicht im Daten-ZIP.')
        self.quick_status.setText(message)
        self.quick_entry.setFocus()

    def refresh_recent_songs(self) -> None:
        while self.recent_layout.count():
            item = self.recent_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._recent_widgets = []
        self.recent_combo.clear()
        paths = list_songs(self.project_root)[:5]
        if not paths:
            empty = QLabel("Noch keine Songs gespeichert · mit „Songtexte“ starten.")
            empty.setObjectName("muted")
            self.recent_layout.addWidget(empty)
            self._recent_widgets.append(empty)
            self.recent_combo.addItem("Noch keine Songs gespeichert")
            self.recent_combo.setEnabled(False)
            self.recent_open_button.setEnabled(False)
            from app.ui_standards import refresh_responsive_layout
            refresh_responsive_layout(self)
            return

        self.recent_combo.setEnabled(True)
        self.recent_open_button.setEnabled(True)
        for path in paths:
            try:
                document = load_song(path)
            except (OSError, UnicodeError, ValueError):
                continue
            subtitle = document.genre or "ohne Genre"
            button = QPushButton(f"{document.title}\n{subtitle}")
            button.setObjectName("recentSongButton")
            button.setToolTip(f"{document.title} öffnen")
            button.clicked.connect(lambda _checked=False, selected=path: self.open_song_path(selected))
            self.recent_layout.addWidget(button, 1)
            self._recent_widgets.append(button)
            self.recent_combo.addItem(f"{document.title} — {subtitle}", str(path))

        if self.recent_combo.count() == 0:
            self.recent_combo.addItem("Keine lesbaren Songs gefunden")
            self.recent_combo.setEnabled(False)
            self.recent_open_button.setEnabled(False)
        from app.ui_standards import refresh_responsive_layout
        refresh_responsive_layout(self)

    def _open_recent_selected(self) -> None:
        selected = self.recent_combo.currentData()
        if selected:
            self.open_song_path(Path(str(selected)))

    def refresh_db_profiles(self, preferred_profile: str | None = None) -> None:
        current = preferred_profile if preferred_profile is not None else self.db_profile_combo.currentText()
        try:
            profiles = profile_names(self.project_root)
        except Exception:
            self.quick_status.setText("Profile konnten nicht geladen werden. Öffne Hilfe & Fehlerhilfe, wenn das Problem bleibt.")
            return
        self.db_profile_combo.blockSignals(True)
        self.db_profile_combo.clear()
        self.db_profile_combo.addItems(profiles)
        if current in profiles:
            self.db_profile_combo.setCurrentText(current)
        elif "HardTechno" in profiles:
            self.db_profile_combo.setCurrentText("HardTechno")
        self.db_profile_combo.blockSignals(False)
        self._load_profile_values()

    def _load_profile_values(self, *_args: object) -> None:
        profile = self.db_profile_combo.currentText()
        self.profile_quick_entry.set_profile(profile)
        if not profile:
            return
        try:
            data = read_profile(self.project_root, profile)
        except Exception:
            self.quick_status.setText("Profilwerte konnten nicht geladen werden. Öffne bei Bedarf Hilfe & Fehlerhilfe.")
            return
        for category in CATEGORIES:
            combo = self.db_boxes[category]
            selected = combo.currentText()
            combo.clear()
            combo.addItem("Bitte auswählen …")
            combo.addItems(data.get(category, []))
            if selected and selected != "Bitte auswählen …" and combo.findText(selected) >= 0:
                combo.setCurrentText(selected)

    def open_profile_quick_entry(self) -> None:
        self.profile_quick_entry.set_profile(self.db_profile_combo.currentText())
        self.db_pages.setCurrentWidget(self.db_quick_scroll)
        self.profile_quick_entry.value_entry.setFocus()

    def close_profile_quick_entry(self) -> None:
        self.db_pages.setCurrentWidget(self.db_selection_scroll)
        self.db_quick_button.setFocus()

    def _reveal_profile_control(self, control) -> None:
        self.profile_quick_entry.layout().activate()
        # Bei mehrzeiligen Meldungen werden die Scrollgrenzen erst nach dem
        # Layout-Ereignis aktualisiert. Der Kontext stoppt den Callback beim
        # Zerstören des Dashboards; ein gelöschtes Ziel wird nicht verwendet.
        def reveal():
            from shiboken6 import isValid
            if isValid(control):
                self.db_quick_scroll.verticalScrollBar().setValue(control.y())
        QTimer.singleShot(0, self, reveal)

    def _profile_values_added(self, profile, category, added) -> None:
        self.refresh_db_profiles()
        if added and self.db_profile_combo.currentText() == profile:
            self.db_boxes[category].setCurrentText(added[-1])
        for window in (self._profile_editor, self._genre_random_window):
            if window is not None and window.isVisible():
                window.refresh()

    def open_profile_editor(self, initial_category: str | None = None) -> None:
        def prepare_visible(window: ProfileEditor) -> None:
            if initial_category in CATEGORIES:
                window.category_combo.setCurrentText(initial_category)

        self._profile_editor = _open_managed_window(
            self._profile_editor,
            lambda: ProfileEditor(
                self.project_root, self.zoom_percent, initial_category,
                on_changed=self.refresh_db_profiles, parent=self, logger=self.logger,
                on_renamed=self._profile_renamed, on_deleted=self._profile_deleted,
            ),
            prepare_visible=prepare_visible,
        )

    def _profile_renamed(self, old_name, new_name) -> None:
        selected = self.db_profile_combo.currentText()
        self.refresh_db_profiles(new_name if selected == old_name else None)
        window = self._genre_random_window
        if window is not None and window.isVisible():
            selected = window.profile_combo.currentText()
            window.refresh()
            if selected == old_name:
                window.profile_combo.setCurrentText(new_name)

    def _profile_deleted(self, _name) -> None:
        self.refresh_db_profiles()
        window = self._genre_random_window
        if window is not None and window.isVisible():
            window.refresh()

    def open_github_projects(self) -> None:
        self._github_projects_window = _open_managed_window(
            self._github_projects_window,
            lambda: GitHubProjectsWindow(self.project_root, self.zoom_percent, parent=self),
        )

    def open_genre_random(self) -> None:
        self._genre_random_window = _open_managed_window(
            self._genre_random_window,
            lambda: GenreRandomWindow(self.project_root, self.zoom_percent, parent=self),
        )

    def open_character_fibel(self) -> None:
        self._character_window = _open_managed_window(
            self._character_window,
            lambda: CharacterWindow(self.project_root, self.zoom_percent, parent=self),
        )

    def open_text_editor(self) -> None:
        self._text_editor_window = _open_managed_window(
            self._text_editor_window,
            lambda: TextEditorWindow(self.project_root, self.zoom_percent, parent=self),
            refresh_after_show=True,
        )

    def open_snippets(self) -> None:
        self._snippet_window = _open_managed_window(
            self._snippet_window,
            lambda: SnippetWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def open_accounts(self) -> None:
        if not self._optional_allowed("accounts"):
            return
        self._account_window = _open_managed_window(
            self._account_window,
            lambda: AccountWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def open_quicklinks(self) -> None:
        if not self._optional_allowed("quicklinks"):
            return
        self._quicklinks_window = _open_managed_window(
            self._quicklinks_window,
            lambda: QuicklinksWindow(self.project_root, self.zoom_percent, parent=self,
                                     on_changed=self.quicklinks_rail.refresh),
            reuse_hidden=True,
        )
        self.quicklinks_rail.refresh()

    def open_wiki(self) -> None:
        if not self._optional_allowed("wiki"):
            return
        self._wiki_window = _open_managed_window(
            self._wiki_window,
            lambda: WikiWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def _optional_allowed(self, ident: str) -> bool:
        try:
            enabled = module_contracts.is_module_enabled(self.project_root, ident)
        except (OSError, ValueError) as error:
            self.quick_status.setText("Modulregister nicht lesbar: " + str(error))
            return False
        if not enabled:
            self.quick_status.setText("Modul deaktiviert. Im Modulmenü unter „Module verwalten“ einschalten.")
        return enabled

    def _may_disable_module(self, ident: str) -> bool:
        windows = {
            "ideas": self._idea_window, "accounts": self._account_window,
            "quicklinks": self._quicklinks_window, "wiki": self._wiki_window,
            "audio": self._audio_window, "pictures": self._pictures_window,
            "slideshow": self._slideshow_window,
        }
        window = windows.get(ident)
        return window is None or not window.isVisible()

    def _sync_optional_actions(self) -> None:
        for ident, action in self._optional_actions.items():
            try:
                action.setEnabled(module_contracts.is_module_enabled(self.project_root, ident))
            except (OSError, ValueError):
                action.setEnabled(False)
        if hasattr(self, "quicklinks_rail"):
            self._update_quicklinks_visibility()

    def open_audio_player(self) -> None:
        if not self._optional_allowed('audio'):
            return
        self._audio_window = _open_managed_window(
            self._audio_window,
            lambda: AudioPlayerWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def open_picture_preview(self) -> None:
        if not self._optional_allowed('pictures'):
            return
        self._pictures_window = _open_managed_window(
            self._pictures_window,
            lambda: ImagePreviewWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def open_slideshow(self) -> None:
        if not self._optional_allowed('slideshow'):
            return
        self._slideshow_window = _open_managed_window(
            self._slideshow_window,
            lambda: SlideshowWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def open_development_pool(self) -> None:
        self._development_pool_window = _open_managed_window(
            self._development_pool_window,
            lambda: DevelopmentPoolWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def open_module_blueprints(self) -> None:
        self._blueprint_window = _open_managed_window(
            self._blueprint_window,
            lambda: BlueprintWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def open_module_controls(self) -> None:
        self._module_controls_window = _open_managed_window(
            self._module_controls_window,
            lambda: ModuleControlsWindow(
                self.project_root, self.zoom_percent,
                can_disable=self._may_disable_module,
                on_saved=self._sync_optional_actions, parent=self,
            ),
            reuse_hidden=True,
        )

    def open_ideas(self) -> None:
        if not self._optional_allowed("ideas"):
            return
        self._idea_window = _open_managed_window(
            self._idea_window,
            lambda: IdeaWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def open_search(self) -> None:
        self._search_window = _open_managed_window(
            self._search_window,
            lambda: SearchWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def open_books(self) -> None:
        self._book_window = _open_managed_window(
            self._book_window,
            lambda: BookWindow(self.project_root, self.zoom_percent, parent=self),
            reuse_hidden=True,
        )

    def _confirm_creative_modules(self) -> bool:
        return all(window.confirm_leave(closing=True) for window in
                   (self._book_window, self._snippet_window, self._idea_window,
                    self._account_window, self._quicklinks_window, self._wiki_window,
                    self._module_controls_window, self._blueprint_window,
                    self._development_pool_window, self._audio_window,
                    self._pictures_window, self._slideshow_window,
                    getattr(self, 'profile_quick_entry', None)) if window is not None)

    def open_todo(self) -> None:
        self._todo_window = _open_managed_window(
            self._todo_window,
            lambda: TodoWindow(self.project_root, self.zoom_percent, parent=self),
        )

    def open_calendar(self) -> None:
        self._calendar_window = _open_managed_window(
            self._calendar_window,
            lambda: CalendarWindow(
                self.project_root, self.zoom_percent,
                on_changed=self._calendar_changed, parent=self,
            ),
            reuse_hidden=True,
            refresh_after_show=True,
        )

    def _calendar_changed(self) -> None:
        if self._calendar_window is not None:
            self._calendar_window.refresh()
        self._calendar_reminders.check_now()

    def _show_calendar_reminder(self, event: dict[str, object]) -> None:
        start = datetime.fromisoformat(str(event["start"])).strftime("%d.%m.%Y %H:%M")
        note = str(event.get("note") or "").strip()
        message = f"{event['title']}\nBeginn: {start}"
        if note:
            message += f"\n\n{note}"
        QMessageBox.information(self, "Terminerinnerung", message)

    def _calendar_reminder_error(self, error: Exception) -> None:
        del error
        self.quick_status.setText("Kalender-Erinnerungen konnten nicht geprüft werden. Öffne bei Bedarf Hilfe & Fehlerhilfe.")

    def _begin_song_editor_session(self) -> None:
        """Verhindert den Bibliothek-Editor-Stapel und merkt den sicheren Rückweg."""
        if self._song_library is not None and self._song_library.isVisible():
            self._song_library.hide()
            self._song_library_hidden_for_editor_session = True

    def _show_song_editor(self, editor: SongEditor) -> None:
        """Registriert und aktiviert einen Songeditor über einen gemeinsamen Ablauf."""
        self._song_editors.append(editor)
        _show_module_window(editor)
        _activate_window(editor)

    def open_song_editor(self) -> None:
        self._begin_song_editor_session()
        editor = SongEditor(self.project_root, zoom_percent=self.zoom_percent,
                            on_closed=self._song_editor_closed, on_saved=self._song_saved, parent=self)
        self._show_song_editor(editor)

    def open_song_path(self, path: Path) -> None:
        try:
            document = load_song(path)
        except Exception as error:
            QMessageBox.critical(
                self, "Song konnte nicht geöffnet werden",
                f"Der Song wurde nicht verändert.\n\nGrund: {error}",
            )
            return
        self._begin_song_editor_session()
        editor = SongEditor(self.project_root, zoom_percent=self.zoom_percent,
                            on_closed=self._song_editor_closed, document=document,
                            on_saved=self._song_saved, parent=self)
        self._show_song_editor(editor)

    def open_song_library(self, initial_search: str = "") -> None:
        visible_editors = [editor for editor in self._song_editors if editor.isVisible()]
        if visible_editors:
            editor = visible_editors[-1]
            _activate_window(editor)
            self.quick_status.setText("Ein Songtexteditor ist geöffnet. Schließe ihn zuerst; danach erscheint die Songbibliothek wieder.")
            return

        def apply_search(window: SongLibrary) -> None:
            if initial_search:
                window.set_search(initial_search)

        self._song_library = _open_managed_window(
            self._song_library,
            lambda: SongLibrary(
                self.project_root, self.zoom_percent, self.open_song_path, parent=self,
            ),
            prepare_visible=apply_search,
            prepare_before_show=apply_search,
        )

    def open_recovery(self) -> None:
        self._recovery_center = _open_managed_window(
            self._recovery_center,
            lambda: RecoveryCenter(self.texts, self.logger, self.zoom_percent, parent=self),
        )

    def _song_saved(self, _path: Path) -> None:
        self.refresh_recent_songs()
        if self._song_library is not None:
            self._song_library.refresh()

    def _song_editor_closed(self, editor: SongEditor) -> None:
        if editor in self._song_editors:
            self._song_editors.remove(editor)
        self.refresh_recent_songs()
        if (not self._song_editors and self._song_library_hidden_for_editor_session
                and not self._closing_after_save):
            self._song_library_hidden_for_editor_session = False
            if self._song_library is not None:
                self._song_library.refresh()
                _show_module_window(self._song_library)
                _activate_window(self._song_library)

    def save_open_song_editors(self) -> bool:
        success = True
        for editor in list(self._song_editors):
            if editor.save(reason="Sitzung gespeichert") is None:
                success = False
        return success

    def logout(self) -> None:
        if not self._confirm_creative_modules():
            return
        if not self.save_open_song_editors():
            QMessageBox.critical(
                self, "Beenden gestoppt",
                "Mindestens ein Songtext konnte nicht gespeichert werden. Das Programm bleibt geöffnet, damit nichts verloren geht.",
            )
            return
        self._closing_after_save = True
        for editor in list(self._song_editors):
            editor.close_safely()
        self.close()

    def _remove_event_filter(self) -> None:
        if hasattr(self, "_calendar_reminders"):
            self._calendar_reminders.stop()
        if not self._event_filter_installed:
            return
        app = QApplication.instance()
        if app is not None:
            app.removeEventFilter(self)
        self._event_filter_installed = False

    def closeEvent(self, event: QCloseEvent) -> None:
        if not self._closing_after_save and not self._confirm_creative_modules():
            event.ignore()
            return
        if self._closing_after_save:
            self._remove_event_filter()
            self.closed_cleanly.emit()
            event.accept()
            return
        if not self.save_open_song_editors():
            QMessageBox.critical(
                self, "Schließen gestoppt",
                "Mindestens ein Songtext konnte nicht gespeichert werden. Das Fenster bleibt geöffnet, damit nichts verloren geht.",
            )
            event.ignore()
            return
        self._closing_after_save = True
        for editor in list(self._song_editors):
            editor.close_safely()
        self._remove_event_filter()
        self.closed_cleanly.emit()
        event.accept()

    def refresh(self) -> None:
        self.quicklinks_rail.refresh()
        self._sync_optional_actions()
        self.refresh_recent_songs()
        self.refresh_db_profiles()
        self.quick_status.setText(module_text("start_ready", "Bereit · Wähle eine Tätigkeit."))
        for registration in self._managed_window_registry():
            if (registration.refresh_when_visible is not None
                    and registration.window.isVisible()):
                registration.refresh_when_visible()

    def _step_zoom(self, direction: int) -> None:
        current = ZOOM_LEVELS.index(self.zoom_percent)
        target = max(0, min(len(ZOOM_LEVELS) - 1, current + direction))
        self.set_zoom(ZOOM_LEVELS[target])

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, 'quicklinks_rail'):
            self._update_quicklinks_visibility()

    def _update_quicklinks_visibility(self) -> None:
        # Nicht mit Profilfeldern oder Hochzoom um wertvolle Breite konkurrieren.
        self.quicklinks_rail.setVisible(self.width() >= 1500 and self.zoom_percent <= 125
                                        and self._optional_allowed("quicklinks"))

    def set_zoom(self, percent: int) -> None:
        if percent not in ZOOM_LEVELS:
            return
        self.zoom_percent = percent
        apply_global_style(self, percent)
        # Der zusätzliche Zugang darf bei Hochzoom keine Profilfelder verdrängen.
        # Menü und Tastenkürzel bleiben als unabhängige Zugänge erhalten.
        self.github_project_open_button.setVisible(percent < 175)
        self.zoom_label.setText(f"{percent} %")
        self._update_quicklinks_visibility()
        for registration in self._managed_window_registry():
            if registration.apply_zoom is not None:
                registration.apply_zoom(percent)


def install_exception_handler(app, logger: EventLogger, refresh: Callable[[], None], parent: QWidget) -> None:
    """Qt-kompatibler zentraler Ausnahmehandler; wird von main über sys.excepthook verdrahtet."""
    import sys

    def report(kind: type[BaseException], error: BaseException, trace: object) -> None:
        try:
            event = logger.record(
                severity="FEHLER", area="OBERFLAECHE",
                summary="Eine Aktion wurde sicher abgebrochen.", cause=str(error) or "Unbekannter Programmfehler",
                protection="Die betroffene Aktion wurde beendet; andere Bereiche bleiben verfügbar.",
                next_step="Öffnen Sie Hilfe & Fehlerhilfe und folgen Sie dem dort genannten Schritt.", exception=error,
            )
            refresh()
            QMessageBox.critical(parent, "Aktion sicher beendet", f"{event['summary']}\n\n{event['next_step']}\n\nKennung: {event['event_id']}")
        except Exception as logging_error:
            QMessageBox.critical(parent, "Sicherer Abbruch", f"Die Aktion wurde beendet. Das Protokoll konnte nicht geschrieben werden: {logging_error}")
        finally:
            sys.__excepthook__(kind, error, trace)
    sys.excepthook = report
