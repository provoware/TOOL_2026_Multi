"""Laienfreundliche, reversible Aufbereitung der Dashboard-Navigation.

Die fachlichen Menüaktionen bleiben in ``app.ui.Dashboard`` definiert. Dieses
Modul ordnet dieselben vorhandenen Bedienelemente nur neu an: fertige Wege
stehen dauerhaft oben, geplante Bereiche werden bedarfsgesteuert gruppiert.
"""

from __future__ import annotations

from collections.abc import Iterable

from PySide6.QtCore import QEvent, QObject, Qt, QTimer
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.presentation_policy import presentation_state


PLANNED_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("creative", ("Hörspiele", "Blogartikel", "Prompts", "Genre-Zufall", "Reimfinder")),
    ("files", ("Dateisuche", "Textinhalt suchen", "Trefferliste", "Duplikatprüfer")),
    ("projects", ("GitHub-Repositories",)),
)
PLANNED_COUNT = sum(len(items) for _key, items in PLANNED_GROUPS)


def _text(widget: QWidget) -> str:
    value = widget.text() if hasattr(widget, "text") else ""
    return " ".join(str(value).replace("&&", "&").split())


def _find_button(widgets: Iterable[QWidget], needle: str) -> QPushButton:
    for widget in widgets:
        if isinstance(widget, QPushButton) and needle in _text(widget):
            return widget
    raise RuntimeError(f"Navigationseintrag fehlt: {needle}")


def _section_label(parent: QWidget, text: str, *, subheading: bool = False) -> QLabel:
    label = QLabel(text, parent)
    label.setObjectName("muted")
    label.setStyleSheet("font-weight: 600;" if subheading else "font-weight: 700;")
    label.setContentsMargins(7, 5 if subheading else 8, 2, 2)
    return label


class NavigationUxController(QObject):
    """Ordnet bestehende Sidebar-Aktionen ohne Änderung ihrer Fachlogik neu."""

    def __init__(self, dashboard: QWidget) -> None:
        super().__init__(dashboard)
        self.dashboard = dashboard
        self.sidebar = getattr(dashboard, "sidebar", None)
        if not isinstance(self.sidebar, QFrame) or not isinstance(self.sidebar.layout(), QVBoxLayout):
            raise RuntimeError("Dashboard-Sidebar konnte nicht sicher erkannt werden.")
        self.layout: QVBoxLayout = self.sidebar.layout()
        self.planned_expanded = False
        self._queued = False
        self._rebuild()
        dashboard.installEventFilter(self)
        self.sidebar.installEventFilter(self)
        self.sync_visibility()

    def _t(self, key: str, fallback: str) -> str:
        registry = getattr(self.dashboard, "texts", None)
        getter = getattr(registry, "get", None)
        return getter(key, fallback) if callable(getter) else fallback

    def _take_existing(self) -> tuple[QHBoxLayout, list[QWidget]]:
        top_layout: QHBoxLayout | None = None
        widgets: list[QWidget] = []
        while self.layout.count():
            item = self.layout.takeAt(0)
            child_layout = item.layout()
            child_widget = item.widget()
            if top_layout is None and isinstance(child_layout, QHBoxLayout):
                top_layout = child_layout
            elif child_widget is not None:
                widgets.append(child_widget)
                child_widget.hide()
        if top_layout is None:
            raise RuntimeError("Menükopf konnte nicht sicher erkannt werden.")
        return top_layout, widgets

    def _menu_header(self, top_layout: QHBoxLayout) -> None:
        menu_button: QPushButton | None = None
        title: QLabel | None = None
        for index in range(top_layout.count()):
            widget = top_layout.itemAt(index).widget()
            if isinstance(widget, QPushButton) and widget.text() == "☰":
                menu_button = widget
            elif isinstance(widget, QLabel):
                title = widget
        if menu_button is None or title is None:
            raise RuntimeError("Menükopf ist unvollständig.")

        toggle_text = self._t("navigation.toggle", "Menü ein- oder ausklappen")
        menu_button.setToolTip(toggle_text)
        menu_button.setAccessibleName(toggle_text)
        try:
            menu_button.clicked.disconnect()
        except (RuntimeError, TypeError):
            pass
        menu_button.clicked.connect(self.toggle_sidebar)

        title.setText(self._t("navigation.title", "Menü"))
        title.setObjectName("muted")
        title.setStyleSheet("font-weight: 700;")
        self.menu_button = menu_button
        self.menu_title = title

    @staticmethod
    def _set_ready_button(button: QPushButton, text: str) -> QPushButton:
        button.setText(text)
        button.setProperty("ready", True)
        button.setAccessibleName((" ".join(text.split()[1:]) if "  " in text else text).replace("&&", "&"))
        button.setStyleSheet("font-weight: 600;")
        button.show()
        return button

    @staticmethod
    def _set_planned_button(button: QPushButton, text: str) -> QPushButton:
        button.setText(text)
        button.setObjectName("navButton")
        button.setProperty("planned", True)
        button.setAccessibleName(text)
        button.setToolTip(f"{text} ist vorbereitet, aber noch nicht fertig nutzbar.")
        button.setAccessibleDescription(
            f"{text} ist noch nicht fertig. Ein Klick verändert keine Nutzerdaten."
        )
        button.hide()
        return button

    def _rebuild(self) -> None:
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(2)
        top_layout, widgets = self._take_existing()
        self._menu_header(top_layout)

        overview = _find_button(widgets, "Übersicht")
        song = _find_button(widgets, "Songtexte")
        text_editor = _find_button(widgets, "Texteditor")
        characters = _find_button(widgets, "Charakterfibel")
        genres = _find_button(widgets, "Genres")
        todo = _find_button(widgets, "Todo-Liste")
        calendar = _find_button(widgets, "Kalender")
        recovery = _find_button(widgets, "Hilfe & Fehlerhilfe")

        overview.setText("⌂  Übersicht")
        overview.setAccessibleName("Übersicht")
        overview.show()
        self.overview_button = overview
        self.ready_buttons = [
            self._set_ready_button(song, "♫  Songtexte"),
            self._set_ready_button(text_editor, "✎  Texteditor"),
            self._set_ready_button(characters, "♙  Charakterfibel"),
            self._set_ready_button(
                genres, f"▦  {self._t('navigation.ready.profile', 'Genres & Vorgaben')}"
            ),
            self._set_ready_button(todo, "✓  Todo-Liste"),
            self._set_ready_button(calendar, "▦  Kalender"),
            self._set_ready_button(recovery, "ⓘ  Hilfe && Fehlerhilfe"),
        ]

        # Der frühere Sammelpunkt "Alle Bereiche" führte ebenfalls nur zu einer
        # Planungsinfo. Er wird nicht gelöscht, sondern aus dem sichtbaren Menü
        # genommen, damit keine zweite bedeutungslose Sackgasse entsteht.
        all_areas = _find_button(widgets, "Alle Bereiche")
        all_areas.setProperty("planned", False)
        all_areas.setObjectName("retiredNav")
        all_areas.hide()

        planned_by_name: dict[str, QPushButton] = {}
        for _group_key, names in PLANNED_GROUPS:
            for name in names:
                planned_by_name[name] = self._set_planned_button(_find_button(widgets, name), name)
        self.planned_buttons = list(planned_by_name.values())

        used_ids = {id(overview), id(all_areas), *(id(button) for button in self.ready_buttons),
                    *(id(button) for button in self.planned_buttons)}
        for widget in widgets:
            if id(widget) not in used_ids:
                widget.hide()

        self.ready_heading = _section_label(
            self.sidebar, self._t("navigation.ready", "Direkt nutzbar")
        )
        self.planned_heading = _section_label(
            self.sidebar, self._t("navigation.planned", "Noch nicht fertig")
        )
        hint_template = self._t(
            "navigation.planned.hint",
            "{count} vorbereitete Bereiche – nur bei Bedarf anzeigen.",
        )
        self.planned_hint = QLabel(hint_template.format(count=PLANNED_COUNT), self.sidebar)
        self.planned_hint.setObjectName("muted")
        self.planned_hint.setWordWrap(True)
        self.planned_hint.setContentsMargins(7, 0, 4, 3)

        self.planned_toggle = QPushButton(self._planned_toggle_text(), self.sidebar)
        self.planned_toggle.setObjectName("plannedGroupButton")
        self.planned_toggle.setProperty("planned", True)
        self.planned_toggle.setStyleSheet("text-align: left; font-weight: 700;")
        self.planned_toggle.setFocusPolicy(Qt.StrongFocus)
        self.planned_toggle.setToolTip(
            self._t(
                "navigation.planned.tooltip",
                "Blendet vorbereitete, aber noch nicht nutzbare Bereiche ein oder aus.",
            )
        )
        self.planned_toggle.setAccessibleName("Geplante Bereiche anzeigen oder ausblenden")
        self.planned_toggle.setAccessibleDescription(
            "Die Bereiche sind noch nicht fertig. Das Ein- und Ausblenden verändert keine Nutzerdaten."
        )
        self.planned_toggle.clicked.connect(self.toggle_planned)

        self.planned_container = QFrame(self.sidebar)
        planned_layout = QVBoxLayout(self.planned_container)
        planned_layout.setContentsMargins(4, 4, 2, 4)
        planned_layout.setSpacing(1)
        group_text = {
            "creative": self._t("navigation.planned.group.creative", "Kreativ & Inhalte"),
            "files": self._t("navigation.planned.group.files", "Dateien & Werkzeuge"),
            "projects": self._t("navigation.planned.group.projects", "Projekte"),
        }
        for group_key, names in PLANNED_GROUPS:
            planned_layout.addWidget(
                _section_label(self.planned_container, group_text[group_key], subheading=True)
            )
            for name in names:
                planned_layout.addWidget(planned_by_name[name])
        self.planned_container.hide()

        self.layout.addLayout(top_layout)
        self.layout.addWidget(overview)
        self.layout.addWidget(self.ready_heading)
        for button in self.ready_buttons:
            self.layout.addWidget(button)
        self.layout.addWidget(self.planned_heading)
        self.layout.addWidget(self.planned_hint)
        self.layout.addWidget(self.planned_toggle)
        self.layout.addWidget(self.planned_container)
        self.layout.addStretch(1)

        self.core_entries: list[QWidget] = [
            overview, self.ready_heading, *self.ready_buttons,
            self.planned_heading, self.planned_hint, self.planned_toggle,
        ]
        self.dashboard._nav_entries = self.core_entries  # type: ignore[attr-defined]
        self.dashboard.song_nav_button = song  # type: ignore[attr-defined]
        self.dashboard.text_editor_nav_button = text_editor  # type: ignore[attr-defined]
        self.dashboard.character_nav_button = characters  # type: ignore[attr-defined]
        self.dashboard.profile_nav_button = genres  # type: ignore[attr-defined]
        self.dashboard.todo_nav_button = todo  # type: ignore[attr-defined]
        self.dashboard.calendar_nav_button = calendar  # type: ignore[attr-defined]
        self.dashboard.recovery_nav_button = recovery  # type: ignore[attr-defined]
        self.dashboard.nav_title = self.menu_title  # type: ignore[attr-defined]
        self.dashboard.planned_menu_toggle = self.planned_toggle  # type: ignore[attr-defined]
        self.dashboard.planned_menu_hint = self.planned_hint  # type: ignore[attr-defined]
        self.dashboard.planned_menu_container = self.planned_container  # type: ignore[attr-defined]
        self.dashboard.planned_menu_expanded = False  # type: ignore[attr-defined]
        self.dashboard.toggle_sidebar = self.toggle_sidebar  # type: ignore[method-assign]

    def _planned_toggle_text(self) -> str:
        if self.planned_expanded:
            return f"▾  Bereiche ausblenden ({PLANNED_COUNT})"
        return f"▸  Geplante Bereiche ({PLANNED_COUNT})"

    def _restricted(self) -> bool:
        return presentation_state(self.dashboard).restricted_navigation

    def _sync_ready_labels(self, compact_labels: bool) -> None:
        """Verwendet bei knapper Fläche kurze sichtbare Labels ohne Informationsverlust."""
        labels = (
            "♫  Songtexte",
            "✎  Editor" if compact_labels else "✎  Texteditor",
            "♙  Charaktere" if compact_labels else "♙  Charakterfibel",
            "▦  Vorgaben" if compact_labels else f"▦  {self._t('navigation.ready.profile', 'Genres & Vorgaben')}",
            "✓  Todo-Liste",
            "▦  Kalender",
            "ⓘ  Hilfe" if compact_labels else "ⓘ  Hilfe && Fehlerhilfe",
        )
        for button, text in zip(self.ready_buttons, labels, strict=True):
            button.setText(text)

    @staticmethod
    def _set_vertical_presence(widget: QWidget, visible: bool) -> None:
        """Entfernt versteckte Bereiche auch sicher aus der Höhenverteilung."""
        widget.setMaximumHeight(16777215 if visible else 0)
        widget.setVisible(visible)

    def sync_visibility(self) -> None:
        collapsed = bool(getattr(self.dashboard, "nav_collapsed", False))
        sidebar_open = not collapsed
        state = presentation_state(self.dashboard)
        restricted = state.restricted_navigation
        self._sync_ready_labels(state.high_zoom or state.laptop_compact)
        self.layout.setContentsMargins(
            4 if state.high_zoom else 8,
            4 if state.high_zoom else 8,
            4 if state.high_zoom else 8,
            4 if state.high_zoom else 8,
        )
        self.layout.setSpacing(4 if state.high_zoom else 2)

        self.menu_title.setVisible(sidebar_open)
        for button in self.ready_buttons:
            button.setVisible(sidebar_open)
        self._set_vertical_presence(self.overview_button, sidebar_open and not state.high_zoom)
        self._set_vertical_presence(self.ready_heading, sidebar_open and not state.high_zoom)
        self._set_vertical_presence(self.planned_heading, sidebar_open and not restricted)
        self._set_vertical_presence(self.planned_hint, sidebar_open and not restricted)
        self._set_vertical_presence(self.planned_toggle, sidebar_open and not restricted)

        show_planned = sidebar_open and not restricted and self.planned_expanded
        self._set_vertical_presence(self.planned_container, show_planned)
        for button in self.planned_buttons:
            button.setMaximumHeight(16777215)
            button.setVisible(show_planned)

    def toggle_planned(self) -> None:
        if self._restricted():
            return
        self.planned_expanded = not self.planned_expanded
        self.dashboard.planned_menu_expanded = self.planned_expanded  # type: ignore[attr-defined]
        self.planned_toggle.setText(self._planned_toggle_text())
        self.sync_visibility()

    def toggle_sidebar(self) -> None:
        collapsed = not bool(getattr(self.dashboard, "nav_collapsed", False))
        self.dashboard.nav_collapsed = collapsed  # type: ignore[attr-defined]
        if collapsed:
            self.sidebar.setFixedWidth(56)
            self.sync_visibility()
            return

        self.sidebar.setMinimumWidth(0)
        self.sidebar.setMaximumWidth(16777215)
        self.sync_visibility()
        from app.ui_standards import refresh_responsive_layout
        refresh_responsive_layout(self.dashboard)

    def _schedule_sync(self) -> None:
        if self._queued:
            return
        self._queued = True

        def after_other_layout_filters() -> None:
            QTimer.singleShot(0, self._finish_sync)

        QTimer.singleShot(0, after_other_layout_filters)

    def _finish_sync(self) -> None:
        self._queued = False
        self.sync_visibility()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() in {
            QEvent.Type.Show, QEvent.Type.Resize, QEvent.Type.LayoutRequest,
            QEvent.Type.StyleChange, QEvent.Type.FontChange, QEvent.Type.DynamicPropertyChange,
        }:
            self._schedule_sync()
        return False


def install_navigation_ux(dashboard: QWidget) -> NavigationUxController:
    """Installiert die Menüaufbereitung genau einmal und gibt den Controller zurück."""
    existing = getattr(dashboard, "_provoware_navigation_ux", None)
    if isinstance(existing, NavigationUxController):
        existing.sync_visibility()
        return existing
    controller = NavigationUxController(dashboard)
    dashboard._provoware_navigation_ux = controller  # type: ignore[attr-defined]
    return controller
