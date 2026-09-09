"""Zentrale PySide6-Standards für modernes, kontrastreiches und responsives UI."""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QFrame, QHeaderView, QLabel, QListWidget, QPushButton,
    QSizePolicy, QSplitter, QTreeWidget, QWidget,
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
    """Skaliert Schriftwerte vollständig mit dem gewählten Zoom."""
    return max(1, round(value * zoom_percent / 100))


def geometry_scaled(value: int, zoom_percent: int) -> int:
    """Skaliert Geometrie bewusst flacher als Schrift.

    200 % Schriftzoom darf nicht gleichzeitig alle Abstände, Radien und
    Mindesthöhen verdoppeln. Die Geometrie wächst deshalb maximal um 25 %.
    """
    zoom = max(100, min(200, int(zoom_percent)))
    factor = 1.0 + ((zoom - 100) / 100.0) * 0.25
    return max(1, round(value * factor))


def _zoom_percent(window: QWidget) -> int:
    try:
        return max(100, min(200, int(getattr(window, "zoom_percent", 100))))
    except (TypeError, ValueError):
        return 100


def app_stylesheet(zoom_percent: int = 100) -> str:
    body = scaled(FONTS["body_size"], zoom_percent)
    small = scaled(FONTS["small_size"], zoom_percent)
    section = scaled(FONTS["section_size"], zoom_percent)
    title = scaled(FONTS["title_size"], zoom_percent)
    hero = scaled(FONTS["hero_size"], zoom_percent)
    radius = geometry_scaled(9, zoom_percent)
    pad_v = geometry_scaled(6, zoom_percent)
    pad_h = geometry_scaled(10, zoom_percent)
    control_height = geometry_scaled(27, zoom_percent)
    nav_pad_v = geometry_scaled(3, zoom_percent)
    nav_pad_h = geometry_scaled(8, zoom_percent)
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
        padding:{nav_pad_v}px {nav_pad_h}px;
        min-height:{geometry_scaled(22, zoom_percent)}px;
    }}
    QPushButton#navButton:hover {{ background:{COLORS['surface_alt']}; }}
    QPushButton#activeNav {{
        text-align:left; background:#142B3E; color:{COLORS['text']}; font-weight:700;
        border:1px solid {COLORS['border']}; border-left:3px solid {COLORS['accent']};
        border-radius:{geometry_scaled(6, zoom_percent)}px;
        padding:{nav_pad_v}px {nav_pad_h}px;
        min-height:{geometry_scaled(22, zoom_percent)}px;
    }}
    QPushButton#tileButton {{ min-height:{geometry_scaled(54, zoom_percent)}px; font-weight:600; }}
    QPushButton#featureButton {{ min-height:{geometry_scaled(82, zoom_percent)}px; font-weight:600; }}

    QLineEdit, QTextEdit, QPlainTextEdit, QListWidget, QTreeWidget, QTableWidget {{
        background:{COLORS['surface']}; color:{COLORS['text']};
        border:1px solid {COLORS['border']}; border-radius:{radius}px;
        padding:{geometry_scaled(5, zoom_percent)}px;
        selection-background-color:{COLORS['accent_soft']}; selection-color:{COLORS['text']};
    }}
    QLineEdit {{ min-height:{control_height}px; }}
    QComboBox {{
        background:{COLORS['surface']}; color:{COLORS['text']};
        border:1px solid {COLORS['border']}; border-radius:{radius}px;
        padding:{geometry_scaled(3, zoom_percent)}px {geometry_scaled(6, zoom_percent)}px;
        min-height:{control_height}px;
        selection-background-color:{COLORS['accent_soft']}; selection-color:{COLORS['text']};
    }}
    QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus,
    QListWidget:focus, QTreeWidget:focus, QTableWidget:focus, QPushButton:focus, QToolButton:focus {{
        border:2px solid {COLORS['cyan']};
    }}
    QComboBox::drop-down {{ border:none; width:{geometry_scaled(24, zoom_percent)}px; }}
    QHeaderView::section {{
        background:#12283C; color:{COLORS['text']}; border:none;
        border-right:1px solid {COLORS['border_soft']}; border-bottom:1px solid {COLORS['border']};
        padding:{geometry_scaled(6, zoom_percent)}px; font-weight:700;
    }}
    QTreeWidget, QTableWidget {{ alternate-background-color:{COLORS['surface_soft']}; outline:0; }}
    QTreeWidget::item, QTableWidget::item {{ padding:{geometry_scaled(2, zoom_percent)}px; }}
    QTreeWidget::item:selected, QTableWidget::item:selected {{
        background:{COLORS['accent_soft']}; color:{COLORS['text']};
    }}
    QTabWidget::pane {{ border:1px solid {COLORS['border_soft']}; border-radius:{radius}px; }}
    QTabBar::tab {{
        background:{COLORS['surface_soft']}; color:{COLORS['muted']};
        border:1px solid {COLORS['border_soft']};
        padding:{geometry_scaled(6, zoom_percent)}px {geometry_scaled(11, zoom_percent)}px;
    }}
    QTabBar::tab:selected {{ color:{COLORS['text']}; border-bottom:2px solid {COLORS['accent']}; background:{COLORS['surface_alt']}; }}
    QCheckBox {{ spacing:{geometry_scaled(6, zoom_percent)}px; }}
    QSplitter::handle {{ background:{COLORS['border_soft']}; width:{geometry_scaled(5, zoom_percent)}px; }}
    QSplitter::handle:hover {{ background:{COLORS['accent']}; }}
    QMenu {{ background:{COLORS['surface']}; color:{COLORS['text']}; border:1px solid {COLORS['border']}; }}
    QMenu::item {{ padding:{geometry_scaled(6, zoom_percent)}px {geometry_scaled(12, zoom_percent)}px; }}
    QMenu::item:selected {{ background:{COLORS['accent_soft']}; }}
    QToolTip {{ background:{COLORS['surface_alt']}; color:{COLORS['text']}; border:1px solid {COLORS['accent']}; padding:5px; }}
    QScrollBar:vertical {{ background:{COLORS['surface_soft']}; width:{geometry_scaled(10, zoom_percent)}px; margin:0; }}
    QScrollBar::handle:vertical {{ background:{COLORS['border']}; min-height:{geometry_scaled(28, zoom_percent)}px; border-radius:{geometry_scaled(5, zoom_percent)}px; }}
    QScrollBar::handle:vertical:hover {{ background:{COLORS['accent']}; }}
    QScrollBar:add-line:vertical, QScrollBar:sub-line:vertical {{ height:0; }}
    QScrollBar:horizontal {{ background:{COLORS['surface_soft']}; height:{geometry_scaled(10, zoom_percent)}px; margin:0; }}
    QScrollBar::handle:horizontal {{ background:{COLORS['border']}; min-width:{geometry_scaled(28, zoom_percent)}px; border-radius:{geometry_scaled(5, zoom_percent)}px; }}
    QScrollBar::handle:horizontal:hover {{ background:{COLORS['accent']}; }}
    QScrollBar:add-line:horizontal, QScrollBar:sub-line:horizontal {{ width:0; }}
    """


def _set_width(widget: QWidget, value: int) -> None:
    widget.setMinimumWidth(value)
    widget.setMaximumWidth(value)


def _zoom_width_factor(window: QWidget) -> float:
    zoom = _zoom_percent(window)
    return 1.0 + ((zoom - 100) / 100.0) * 0.10


def _card_title(card: QFrame) -> str:
    for label in card.findChildren(QLabel):
        if label.objectName() == "cardTitle":
            return label.text()
    return ""


def _apply_dashboard_high_zoom(window: QWidget, high_zoom: bool) -> None:
    """Reduziert bei 175/200 % ausschließlich redundante Planungsübersichten.

    Die geplanten Module bleiben oben als Kacheln sichtbar. In der langen linken
    Navigation und im unteren 2x2-Bereich würden dieselben Einträge bei Hochzoom
    sonst nur Platz verbrauchen und Überlagerungen provozieren.
    """
    if window.__class__.__name__ != "Dashboard":
        return

    nav_collapsed = bool(getattr(window, "nav_collapsed", False))
    for button in window.findChildren(QPushButton):
        if button.objectName() == "navButton" and button.property("planned") is True:
            button.setMaximumHeight(0 if high_zoom else 16777215)
            button.setVisible(not high_zoom and not nav_collapsed)

    for card in window.findChildren(QFrame):
        if card.objectName() != "card":
            continue
        title = _card_title(card)
        if title.startswith("▣  Funktionen") or title.startswith("▤  Dateien & Werkzeuge"):
            card.setVisible(not high_zoom)


def _apply_responsive_layout(window: QWidget) -> None:
    if window.property("provowareResponsiveBusy"):
        return
    window.setProperty("provowareResponsiveBusy", True)
    try:
        width = max(window.width(), window.minimumWidth())
        zoom = _zoom_percent(window)
        compact = width < 1100
        wide = width >= 1450
        high_zoom = zoom >= 175
        width_factor = _zoom_width_factor(window)
        margin = 7 if compact else (13 if wide else 10)
        gap = 6 if compact else (10 if wide else 8)
        if high_zoom:
            margin = min(margin, 8)
            gap = min(gap, 6)

        root_layout = window.layout()
        if root_layout is not None:
            root_layout.setContentsMargins(margin, margin, margin, margin)
            root_layout.setSpacing(gap)

        _apply_dashboard_high_zoom(window, high_zoom)

        for card in window.findChildren(QFrame):
            if card.objectName() in {"card", "innerCard"}:
                card.setMinimumWidth(0)
                card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        sidebar = getattr(window, "sidebar", None)
        if isinstance(sidebar, QWidget) and not getattr(window, "nav_collapsed", False):
            base = 198 if compact else (258 if wide else 226)
            if high_zoom:
                base = max(base, 238 if compact else 260)
            _set_width(sidebar, round(base * width_factor))

        search = getattr(window, "search_entry", None)
        if isinstance(search, QWidget):
            if window.__class__.__name__ == "Dashboard":
                base = 190 if compact else (320 if wide else 250)
                if high_zoom:
                    base = min(base, 250)
                _set_width(search, round(base * width_factor))
            elif window.__class__.__name__ == "SongLibrary":
                search.setMinimumWidth(round(220 * width_factor))
                search.setMaximumWidth(16777215)
                if hasattr(search, "setPlaceholderText"):
                    search.setPlaceholderText("Songtitel, Genre, Stimmung, Stil, Stimme oder Tag eingeben …")

        profile_combo = getattr(window, "db_profile_combo", None)
        if isinstance(profile_combo, QWidget):
            minimum = round((100 if high_zoom else (110 if compact else 135)) * width_factor)
            maximum = round((135 if high_zoom else (190 if wide else 160)) * width_factor)
            profile_combo.setMinimumWidth(minimum)
            profile_combo.setMaximumWidth(maximum)

        for label in window.findChildren(QLabel):
            if label.text() in {"Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten"}:
                base = 82 if high_zoom else (94 if compact else (128 if wide else 108))
                _set_width(label, round(base * width_factor))

        for button in window.findChildren(QPushButton):
            if button.text() in {"Profile & Werte bearbeiten", "Profile bearbeiten", "Profile"}:
                if high_zoom:
                    button.setText("Profile")
                else:
                    button.setText("Profile & Werte bearbeiten" if wide else "Profile bearbeiten")

        section_list = getattr(window, "section_list", None)
        if isinstance(section_list, QListWidget):
            base = 150 if high_zoom else (165 if compact else (235 if wide else 200))
            _set_width(section_list, round(base * width_factor))
            section_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        for splitter in window.findChildren(QSplitter):
            splitter.setChildrenCollapsible(False)
            splitter.setHandleWidth(geometry_scaled(5, zoom))
            if window.__class__.__name__ == "SongEditor" and splitter.orientation() == Qt.Horizontal:
                available = max(700, width - 40)
                left_ratio = 0.64 if high_zoom else (0.57 if wide else 0.60)
                left = round(available * left_ratio)
                splitter.setSizes([left, available - left])
                splitter.setStretchFactor(0, 3)
                splitter.setStretchFactor(1, 2)

        if window.__class__.__name__ == "SongLibrary":
            table = getattr(window, "table", None)
            if isinstance(table, QTreeWidget) and table.columnCount() >= 8:
                header = table.header()
                header.setMinimumSectionSize(round(42 * width_factor))
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
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QWidget) and event.type() in {QEvent.Type.Show, QEvent.Type.Resize}:
            _apply_responsive_layout(watched)
        return False


def refresh_responsive_layout(widget: QWidget) -> None:
    """Wendet die aktuelle Breiten-/Zoomverteilung erneut an."""
    _apply_responsive_layout(widget)


def _install_responsive_layout(widget: QWidget) -> None:
    responsive_filter = getattr(widget, "_provoware_responsive_filter", None)
    if responsive_filter is None:
        responsive_filter = _ResponsiveFilter(widget)
        widget._provoware_responsive_filter = responsive_filter  # type: ignore[attr-defined]
        widget.installEventFilter(responsive_filter)
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
