"""Zentrale PySide6-Standards für modernes, kontrastreiches und zoom-sicheres UI."""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import (
    QApplication, QFrame, QGridLayout, QHeaderView, QLabel, QLayout, QListWidget,
    QPushButton, QScrollArea, QSizePolicy, QSplitter, QTreeWidget, QVBoxLayout,
    QWidget,
)

COLORS = {
    "background": "#061019",
    "surface": "#0A1927",
    "surface_alt": "#102438",
    "surface_soft": "#0C1C2B",
    "sidebar": "#071522",
    "text": "#F6F8FB",
    "muted": "#B7C4D2",
    "accent": "#FFB11B",
    "accent_hover": "#FFC44D",
    "accent_soft": "#35280F",
    "cyan": "#34D9FF",
    "green": "#48E69B",
    "yellow": "#FFD66B",
    "red": "#FF7180",
    "red_soft": "#35171E",
    "blocked": "#7D91A5",
    "border": "#2D4963",
    "border_soft": "#20384E",
}

SPACING = {"xs": 5, "s": 8, "m": 12, "l": 16, "xl": 22}
FONTS = {"body_size": 10, "small_size": 9, "section_size": 12, "title_size": 16, "hero_size": 19}
UI_FONT_FAMILY = "Sans Serif"

SEVERITY_STATUS = {
    "INFO": ("●", COLORS["green"]), "HINWEIS": ("●", COLORS["green"]),
    "WARNUNG": ("●", COLORS["yellow"]), "FEHLER": ("●", COLORS["red"]),
    "KRITISCH": ("●", COLORS["red"]), "SCHWER": ("●", COLORS["red"]),
    "ABSTURZ": ("●", COLORS["red"]),
}


def scaled(value: int, zoom_percent: int) -> int:
    """Skaliert echte Schriftgrößen weiterhin vollständig mit dem Nutzer-Zoom."""
    return max(1, round(value * zoom_percent / 100))


def _metric_zoom_percent(zoom_percent: int) -> int:
    """Abstände wachsen bewusst langsamer als Schrift, damit 200 % nicht alles verdrängt."""
    return max(100, min(145, round(100 + (zoom_percent - 100) * 0.45)))


def _heading_zoom_percent(zoom_percent: int) -> int:
    """Große Überschriften bleiben deutlich, wachsen aber nicht doppelt so stark wie Fließtext."""
    return max(100, min(165, round(100 + (zoom_percent - 100) * 0.65)))


def _metric_scaled(value: int, zoom_percent: int) -> int:
    return scaled(value, _metric_zoom_percent(zoom_percent))


def _heading_scaled(value: int, zoom_percent: int) -> int:
    return scaled(value, _heading_zoom_percent(zoom_percent))


def _window_zoom(window: QWidget) -> int:
    try:
        zoom = int(getattr(window, "zoom_percent", 100))
    except (TypeError, ValueError):
        zoom = 100
    return max(100, min(200, zoom))


def _effective_width(window: QWidget) -> float:
    """Physische Breite auf 100-%-Arbeitsbreite zurückrechnen."""
    zoom = _window_zoom(window)
    return max(1.0, window.width() * 100.0 / zoom)


def app_stylesheet(zoom_percent: int = 100) -> str:
    body = scaled(FONTS["body_size"], zoom_percent)
    small = scaled(FONTS["small_size"], zoom_percent)
    section = _heading_scaled(FONTS["section_size"], zoom_percent)
    title = _heading_scaled(FONTS["title_size"], zoom_percent)
    hero = _heading_scaled(FONTS["hero_size"], zoom_percent)
    radius = _metric_scaled(9, zoom_percent)
    pad_v = _metric_scaled(7, zoom_percent)
    pad_h = _metric_scaled(11, zoom_percent)
    control_height = _metric_scaled(27, zoom_percent)
    return f"""
    QWidget {{
        background:{COLORS['background']}; color:{COLORS['text']};
        font-family:"{UI_FONT_FAMILY}"; font-size:{body}pt;
    }}
    QWidget#dashboardShell {{ background:{COLORS['background']}; }}
    QFrame#header, QFrame#toolbar, QFrame#statusBar {{
        background:{COLORS['surface_soft']}; border:1px solid {COLORS['border_soft']};
        border-radius:{radius}px;
    }}
    QFrame#sidebar {{
        background:{COLORS['sidebar']}; border:1px solid {COLORS['border_soft']};
        border-radius:{radius}px;
    }}
    QFrame#card {{
        background:{COLORS['surface']}; border:1px solid {COLORS['border']};
        border-radius:{radius}px;
    }}
    QFrame#innerCard {{
        background:{COLORS['surface_alt']}; border:1px solid {COLORS['border_soft']};
        border-radius:{radius}px;
    }}
    QLabel {{ background:transparent; border:none; }}
    QLabel#appTitle {{ font-size:{hero}pt; font-weight:700; letter-spacing:0.2px; }}
    QLabel#subtitle, QLabel#muted, QLabel#cardHint {{ color:{COLORS['muted']}; font-size:{small}pt; }}
    QLabel#sectionTitle {{ font-size:{title}pt; font-weight:700; }}
    QLabel#cardTitle {{ font-size:{section}pt; font-weight:700; }}
    QLabel#accent {{ color:{COLORS['accent']}; font-weight:700; }}
    QLabel#statusGood {{ color:{COLORS['green']}; font-weight:700; }}

    QPushButton, QToolButton {{
        background:{COLORS['surface_alt']}; color:{COLORS['text']};
        border:1px solid {COLORS['border']}; border-radius:{radius}px;
        padding:{pad_v}px {pad_h}px; min-height:{control_height}px; text-align:center;
    }}
    QPushButton:hover, QToolButton:hover {{
        border-color:{COLORS['accent_hover']}; background:#162D42;
    }}
    QPushButton:pressed, QToolButton:pressed {{
        background:{COLORS['accent_soft']}; border-color:{COLORS['accent']};
    }}
    QPushButton#primaryButton {{
        border:1px solid {COLORS['accent']}; background:{COLORS['accent_soft']};
        font-weight:700;
    }}
    QPushButton#primaryButton:hover {{ background:{COLORS['accent']}; color:#07111A; }}
    QPushButton#dangerButton {{ border:1px solid {COLORS['red']}; background:{COLORS['red_soft']}; }}
    QPushButton#dangerButton:hover {{ background:{COLORS['red']}; color:#07111A; }}
    QPushButton[planned="true"] {{
        color:{COLORS['muted']}; border:1px dashed {COLORS['blocked']};
        background:{COLORS['surface_soft']};
    }}
    QPushButton[planned="true"]:hover {{ color:{COLORS['text']}; border-color:{COLORS['yellow']}; }}
    QPushButton#navButton {{
        text-align:left; border:none; background:transparent;
        padding:{_metric_scaled(6, zoom_percent)}px {_metric_scaled(9, zoom_percent)}px;
        min-height:{_metric_scaled(24, zoom_percent)}px;
    }}
    QPushButton#navButton:hover {{ background:{COLORS['surface_alt']}; }}
    QPushButton#activeNav {{
        text-align:left; background:#142B3E; color:{COLORS['text']}; font-weight:700;
        border:1px solid {COLORS['border']}; border-left:3px solid {COLORS['accent']};
        border-radius:{_metric_scaled(6, zoom_percent)}px;
        padding:{_metric_scaled(6, zoom_percent)}px {_metric_scaled(8, zoom_percent)}px;
    }}
    QPushButton#tileButton {{ min-height:{_metric_scaled(54, zoom_percent)}px; font-weight:600; }}
    QPushButton#featureButton {{ min-height:{_metric_scaled(82, zoom_percent)}px; font-weight:600; }}

    QLineEdit, QTextEdit, QPlainTextEdit, QListWidget, QTreeWidget, QTableWidget {{
        background:{COLORS['surface']}; color:{COLORS['text']};
        border:1px solid {COLORS['border']}; border-radius:{radius}px;
        padding:{_metric_scaled(6, zoom_percent)}px;
        selection-background-color:{COLORS['accent_soft']}; selection-color:{COLORS['text']};
    }}
    QLineEdit {{ min-height:{control_height}px; }}
    QComboBox {{
        background:{COLORS['surface']}; color:{COLORS['text']};
        border:1px solid {COLORS['border']}; border-radius:{radius}px;
        padding:{_metric_scaled(4, zoom_percent)}px {_metric_scaled(7, zoom_percent)}px;
        min-height:{control_height}px;
        selection-background-color:{COLORS['accent_soft']}; selection-color:{COLORS['text']};
    }}
    QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus,
    QListWidget:focus, QTreeWidget:focus, QTableWidget:focus, QPushButton:focus, QToolButton:focus {{
        border:2px solid {COLORS['cyan']};
    }}
    QComboBox::drop-down {{ border:none; width:{_metric_scaled(24, zoom_percent)}px; }}
    QHeaderView::section {{
        background:#12283C; color:{COLORS['text']}; border:none;
        border-right:1px solid {COLORS['border_soft']}; border-bottom:1px solid {COLORS['border']};
        padding:{_metric_scaled(7, zoom_percent)}px; font-weight:700;
    }}
    QTreeWidget, QTableWidget {{ alternate-background-color:{COLORS['surface_soft']}; outline:0; }}
    QTreeWidget::item, QTableWidget::item {{ padding:{_metric_scaled(3, zoom_percent)}px; }}
    QTreeWidget::item:selected, QTableWidget::item:selected {{
        background:{COLORS['accent_soft']}; color:{COLORS['text']};
    }}
    QTabWidget::pane {{ border:1px solid {COLORS['border_soft']}; border-radius:{radius}px; }}
    QTabBar::tab {{
        background:{COLORS['surface_soft']}; color:{COLORS['muted']};
        border:1px solid {COLORS['border_soft']};
        padding:{_metric_scaled(7, zoom_percent)}px {_metric_scaled(12, zoom_percent)}px;
    }}
    QTabBar::tab:selected {{ color:{COLORS['text']}; border-bottom:2px solid {COLORS['accent']}; background:{COLORS['surface_alt']}; }}
    QCheckBox {{ spacing:{_metric_scaled(7, zoom_percent)}px; }}
    QSplitter::handle {{ background:{COLORS['border_soft']}; width:{_metric_scaled(5, zoom_percent)}px; }}
    QSplitter::handle:hover {{ background:{COLORS['accent']}; }}
    QMenu {{ background:{COLORS['surface']}; color:{COLORS['text']}; border:1px solid {COLORS['border']}; }}
    QMenu::item {{ padding:{_metric_scaled(7, zoom_percent)}px {_metric_scaled(14, zoom_percent)}px; }}
    QMenu::item:selected {{ background:{COLORS['accent_soft']}; }}
    QToolTip {{ background:{COLORS['surface_alt']}; color:{COLORS['text']}; border:1px solid {COLORS['accent']}; padding:5px; }}
    QScrollArea {{ border:none; background:transparent; }}
    QScrollArea > QWidget > QWidget {{ background:transparent; }}
    QScrollBar:vertical {{ background:{COLORS['surface_soft']}; width:{_metric_scaled(10, zoom_percent)}px; margin:0; }}
    QScrollBar::handle:vertical {{ background:{COLORS['border']}; min-height:{_metric_scaled(28, zoom_percent)}px; border-radius:{_metric_scaled(5, zoom_percent)}px; }}
    QScrollBar::handle:vertical:hover {{ background:{COLORS['accent']}; }}
    QScrollBar:add-line:vertical, QScrollBar:sub-line:vertical {{ height:0; }}
    QScrollBar:horizontal {{ background:{COLORS['surface_soft']}; height:{_metric_scaled(10, zoom_percent)}px; margin:0; }}
    QScrollBar::handle:horizontal {{ background:{COLORS['border']}; min-width:{_metric_scaled(28, zoom_percent)}px; border-radius:{_metric_scaled(5, zoom_percent)}px; }}
    QScrollBar::handle:horizontal:hover {{ background:{COLORS['accent']}; }}
    QScrollBar:add-line:horizontal, QScrollBar:sub-line:horizontal {{ width:0; }}
    """


def _set_width(widget: QWidget, value: int) -> None:
    value = max(1, value)
    widget.setMinimumWidth(value)
    widget.setMaximumWidth(value)


def _metric_width_factor(window: QWidget) -> float:
    return _metric_zoom_percent(_window_zoom(window)) / 100.0


def _find_dashboard_grid(layout: QLayout) -> tuple[QVBoxLayout, int, QGridLayout] | None:
    """Findet die bestehende 2×2-Kartenfläche ohne Annahme fester Top-Level-Indizes."""
    for index in range(layout.count()):
        item = layout.itemAt(index)
        child = item.layout()
        if isinstance(child, QGridLayout):
            cards = [
                child.itemAt(pos).widget() for pos in range(child.count())
                if child.itemAt(pos).widget() is not None
                and child.itemAt(pos).widget().objectName() == "card"
            ]
            if len(cards) == 4 and isinstance(layout, QVBoxLayout):
                return layout, index, child
        if child is not None:
            found = _find_dashboard_grid(child)
            if found is not None:
                return found
    return None


def _ensure_dashboard_scroll_safety(window: QWidget) -> None:
    """Rüstet nur das Dashboard einmalig mit sicheren Scrollcontainern nach."""
    if window.__class__.__name__ != "Dashboard":
        return

    sidebar = getattr(window, "sidebar", None)
    if isinstance(sidebar, QWidget) and not hasattr(window, "_provoware_nav_scroll"):
        side_layout = sidebar.layout()
        if isinstance(side_layout, QVBoxLayout) and side_layout.count() > 1:
            nav_content = QWidget(sidebar)
            nav_content.setObjectName("sidebarScrollContent")
            nav_layout = QVBoxLayout(nav_content)
            nav_layout.setContentsMargins(0, 0, 0, 0)
            nav_layout.setSpacing(1)
            nav_layout.setSizeConstraint(QLayout.SetMinimumSize)
            while side_layout.count() > 1:
                item = side_layout.takeAt(1)
                widget = item.widget()
                nested = item.layout()
                spacer = item.spacerItem()
                if widget is not None:
                    nav_layout.addWidget(widget)
                elif nested is not None:
                    nav_layout.addLayout(nested)
                elif spacer is not None:
                    nav_layout.addItem(spacer)
            nav_scroll = QScrollArea(sidebar)
            nav_scroll.setObjectName("sidebarScroll")
            nav_scroll.setWidgetResizable(True)
            nav_scroll.setFrameShape(QFrame.NoFrame)
            nav_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            nav_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            nav_scroll.setWidget(nav_content)
            side_layout.addWidget(nav_scroll, 1)
            window._provoware_nav_scroll = nav_scroll  # type: ignore[attr-defined]
            window._provoware_nav_content = nav_content  # type: ignore[attr-defined]
            window._provoware_nav_layout = nav_layout  # type: ignore[attr-defined]

    if hasattr(window, "_provoware_dashboard_scroll"):
        return
    root_layout = window.layout()
    if root_layout is None:
        return
    found = _find_dashboard_grid(root_layout)
    if found is None:
        return
    parent_layout, index, old_grid = found
    cards: list[tuple[int, int, QWidget]] = []
    for item_index in range(old_grid.count()):
        row, column, _row_span, _column_span = old_grid.getItemPosition(item_index)
        widget = old_grid.itemAt(item_index).widget()
        if widget is not None and widget.objectName() == "card":
            cards.append((row, column, widget))
    if len(cards) != 4:
        return
    cards.sort(key=lambda entry: (entry[0], entry[1]))
    parent_layout.takeAt(index)
    for _row, _column, card in cards:
        old_grid.removeWidget(card)

    host = QWidget(window)
    host.setObjectName("dashboardCardsHost")
    grid = QGridLayout(host)
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setHorizontalSpacing(SPACING["s"])
    grid.setVerticalSpacing(SPACING["s"])
    grid.setSizeConstraint(QLayout.SetMinimumSize)
    for row, column, card in cards:
        grid.addWidget(card, row, column)

    scroll = QScrollArea(window)
    scroll.setObjectName("dashboardCardsScroll")
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    scroll.setWidget(host)
    parent_layout.insertWidget(index, scroll, 1)

    window._provoware_dashboard_scroll = scroll  # type: ignore[attr-defined]
    window._provoware_dashboard_host = host  # type: ignore[attr-defined]
    window._provoware_dashboard_grid = grid  # type: ignore[attr-defined]
    window._provoware_dashboard_cards = [entry[2] for entry in cards]  # type: ignore[attr-defined]


def _fit_sidebar(window: QWidget, width: int, zoom: int, compact: bool, wide: bool) -> None:
    sidebar = getattr(window, "sidebar", None)
    if not isinstance(sidebar, QWidget):
        return
    nav_scroll = getattr(window, "_provoware_nav_scroll", None)
    collapsed = bool(getattr(window, "nav_collapsed", False))
    if isinstance(nav_scroll, QScrollArea):
        nav_scroll.setVisible(not collapsed)
    menu_buttons = [button for button in sidebar.findChildren(QPushButton) if button.text() == "☰"]
    if menu_buttons:
        menu_buttons[0].setFixedWidth(_metric_scaled(42, zoom))
    if collapsed:
        _set_width(sidebar, _metric_scaled(56, zoom))
        return

    factor = _metric_width_factor(window)
    base = 198 if compact else (258 if wide else 226)
    target = round(base * factor)
    if zoom >= 150:
        font = QFont(UI_FONT_FAMILY)
        font.setPointSize(scaled(FONTS["body_size"], zoom))
        metrics = QFontMetrics(font)
        entries = getattr(window, "_nav_entries", [])
        longest = 0
        for entry in entries:
            if isinstance(entry, QPushButton):
                longest = max(longest, metrics.horizontalAdvance(entry.text().replace("\n", " ")))
        target = max(target, longest + _metric_scaled(30, zoom))
        target = min(target, max(_metric_scaled(210, zoom), round(width * 0.38)))
    _set_width(sidebar, target)

    nav_content = getattr(window, "_provoware_nav_content", None)
    nav_layout = getattr(window, "_provoware_nav_layout", None)
    if isinstance(nav_content, QWidget) and isinstance(nav_layout, QVBoxLayout):
        nav_layout.activate()
        nav_content.setMinimumHeight(nav_layout.minimumSize().height())


def _fit_dashboard_labels(window: QWidget, zoom: int, compact: bool, wide: bool) -> None:
    factor = _metric_width_factor(window)
    font = QFont(UI_FONT_FAMILY)
    font.setPointSize(scaled(FONTS["small_size"], zoom))
    metrics = QFontMetrics(font)
    category_names = {"Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten"}
    for label in window.findChildren(QLabel):
        if label.text() in category_names:
            base = 94 if compact else (128 if wide else 108)
            target = round(base * factor)
            if zoom >= 150:
                target = max(target, metrics.horizontalAdvance(label.text()) + _metric_scaled(16, zoom))
            _set_width(label, target)
        if label.objectName() == "appTitle":
            label.setWordWrap(True)
            label.setMinimumWidth(0)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        if label.objectName() == "subtitle" and label.text().startswith("Deine Zentrale"):
            label.setVisible(not (zoom >= 175 and window.width() < 1250))


def _reflow_dashboard_cards(window: QWidget, logical_width: float, zoom: int) -> None:
    grid = getattr(window, "_provoware_dashboard_grid", None)
    cards = getattr(window, "_provoware_dashboard_cards", None)
    host = getattr(window, "_provoware_dashboard_host", None)
    if not isinstance(grid, QGridLayout) or not isinstance(cards, list) or len(cards) != 4:
        return
    single_column = logical_width < 960
    for card in cards:
        if isinstance(card, QWidget):
            grid.removeWidget(card)
    if single_column:
        for row, card in enumerate(cards):
            grid.addWidget(card, row, 0)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 0)
        for row in range(4):
            grid.setRowStretch(row, 0)
    else:
        positions = ((0, 0), (0, 1), (1, 0), (1, 1))
        for card, (row, column) in zip(cards, positions):
            grid.addWidget(card, row, column)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 0)
        grid.setRowStretch(3, 0)
    grid.setHorizontalSpacing(_metric_scaled(SPACING["s"], zoom))
    grid.setVerticalSpacing(_metric_scaled(SPACING["s"], zoom))
    grid.activate()
    if isinstance(host, QWidget):
        host.setMinimumHeight(grid.minimumSize().height() if single_column else 0)


def _fit_section_list(window: QWidget, width: int, zoom: int, compact: bool, wide: bool) -> None:
    section_list = getattr(window, "section_list", None)
    if not isinstance(section_list, QListWidget):
        return
    factor = _metric_width_factor(window)
    base = 165 if compact else (235 if wide else 200)
    target = round(base * factor)
    if zoom >= 150 and section_list.count():
        font = QFont(UI_FONT_FAMILY)
        font.setPointSize(scaled(FONTS["body_size"], zoom))
        metrics = QFontMetrics(font)
        longest = max(metrics.horizontalAdvance(section_list.item(index).text()) for index in range(section_list.count()))
        target = max(target, longest + _metric_scaled(24, zoom))
        target = min(target, max(round(width * 0.42), _metric_scaled(180, zoom)))
    _set_width(section_list, target)
    section_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)


def _apply_responsive_layout(window: QWidget) -> None:
    if window.property("provowareResponsiveBusy"):
        return
    window.setProperty("provowareResponsiveBusy", True)
    try:
        _ensure_dashboard_scroll_safety(window)
        width = max(window.width(), window.minimumWidth())
        zoom = _window_zoom(window)
        logical_width = max(1.0, width * 100.0 / zoom)
        compact = logical_width < 1100
        wide = logical_width >= 1450
        factor = _metric_width_factor(window)
        margin = round((7 if compact else (13 if wide else 10)) * factor)
        gap = round((6 if compact else (10 if wide else 8)) * factor)
        root_layout = window.layout()
        if root_layout is not None:
            root_layout.setContentsMargins(margin, margin, margin, margin)
            root_layout.setSpacing(gap)

        for card in window.findChildren(QFrame):
            if card.objectName() in {"card", "innerCard"}:
                card.setMinimumWidth(0)

        if window.__class__.__name__ == "Dashboard":
            _fit_sidebar(window, width, zoom, compact, wide)
            _fit_dashboard_labels(window, zoom, compact, wide)
            _reflow_dashboard_cards(window, logical_width, zoom)

        search = getattr(window, "search_entry", None)
        if isinstance(search, QWidget):
            if window.__class__.__name__ == "Dashboard":
                base = 190 if compact else (320 if wide else 250)
                target = round(base * factor)
                target = min(target, max(_metric_scaled(180, zoom), round(width * 0.28)))
                _set_width(search, target)
            elif window.__class__.__name__ == "SongLibrary":
                search.setMinimumWidth(round(220 * factor))
                search.setMaximumWidth(16777215)
                if hasattr(search, "setPlaceholderText"):
                    search.setPlaceholderText("Songtitel, Genre, Stimmung, Stil, Stimme oder Tag eingeben …")

        profile_combo = getattr(window, "db_profile_combo", None)
        if isinstance(profile_combo, QWidget):
            minimum = round((110 if compact else 135) * factor)
            maximum = round((190 if wide else 160) * factor)
            profile_combo.setMinimumWidth(minimum)
            profile_combo.setMaximumWidth(maximum)

        for button in window.findChildren(QPushButton):
            if button.text() in {"Profile & Werte bearbeiten", "Profile bearbeiten"}:
                button.setText("Profile & Werte bearbeiten" if wide and zoom <= 150 else "Profile bearbeiten")

        _fit_section_list(window, width, zoom, compact, wide)

        for splitter in window.findChildren(QSplitter):
            splitter.setChildrenCollapsible(False)
            splitter.setHandleWidth(_metric_scaled(5, zoom))
            if window.__class__.__name__ == "SongEditor" and splitter.orientation() == Qt.Horizontal:
                available = max(_metric_scaled(700, zoom), width - _metric_scaled(40, zoom))
                left = round(available * (0.57 if wide else 0.60))
                splitter.setSizes([left, max(1, available - left)])
                splitter.setStretchFactor(0, 3)
                splitter.setStretchFactor(1, 2)

        if window.__class__.__name__ == "SongLibrary":
            table = getattr(window, "table", None)
            if isinstance(table, QTreeWidget) and table.columnCount() >= 8:
                header = table.header()
                header.setMinimumSectionSize(round(42 * factor))
                header.setStretchLastSection(False)
                modes = (
                    QHeaderView.Stretch,
                    QHeaderView.ResizeToContents,
                    QHeaderView.ResizeToContents,
                    QHeaderView.ResizeToContents,
                    QHeaderView.ResizeToContents,
                    QHeaderView.Stretch,
                    QHeaderView.ResizeToContents,
                    QHeaderView.ResizeToContents,
                )
                for index, mode in enumerate(modes):
                    header.setSectionResizeMode(index, mode)
    finally:
        window.setProperty("provowareResponsiveBusy", False)


class _ResponsiveFilter(QObject):
    def __init__(self, owner: QWidget) -> None:
        super().__init__(owner)
        self.owner = owner

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        del watched
        if event.type() in {QEvent.Type.Show, QEvent.Type.Resize}:
            _apply_responsive_layout(self.owner)
        return False


def refresh_responsive_layout(widget: QWidget) -> None:
    """Wendet die aktuelle Breiten-/Zoomverteilung erneut an."""
    _apply_responsive_layout(widget)


def _install_responsive_layout(widget: QWidget) -> None:
    _ensure_dashboard_scroll_safety(widget)
    responsive_filter = getattr(widget, "_provoware_responsive_filter", None)
    if responsive_filter is None:
        responsive_filter = _ResponsiveFilter(widget)
        widget._provoware_responsive_filter = responsive_filter  # type: ignore[attr-defined]
        widget.installEventFilter(responsive_filter)
        sidebar = getattr(widget, "sidebar", None)
        if isinstance(sidebar, QWidget):
            sidebar.installEventFilter(responsive_filter)
    _apply_responsive_layout(widget)


def apply_global_style(widget: QWidget, zoom_percent: int = 100) -> None:
    widget.setStyleSheet(app_stylesheet(zoom_percent))
    font = QFont(UI_FONT_FAMILY)
    font.setPointSize(scaled(FONTS["body_size"], zoom_percent))
    widget.setFont(font)
    _install_responsive_layout(widget)


def configure_application(app: QApplication, zoom_percent: int = 100) -> None:
    app.setStyle("Fusion")
    font = QFont(UI_FONT_FAMILY)
    font.setPointSize(scaled(FONTS["body_size"], zoom_percent))
    app.setFont(font)
    app.setStyleSheet(app_stylesheet(zoom_percent))


def severity_display(severity: str) -> tuple[str, str]:
    return SEVERITY_STATUS.get(severity.upper(), ("●", COLORS["blocked"]))
