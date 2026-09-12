"""Zentrale PySide6-Standards für modernes, kontrastreiches, responsives und barrierearmes UI."""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFrame, QHeaderView, QLabel, QLineEdit,
    QListWidget, QPlainTextEdit, QPushButton, QSizePolicy, QSplitter, QTableWidget,
    QTextEdit, QToolButton, QTreeWidget, QWidget,
)

from app.presentation_policy import HIGH_ZOOM_MIN_PERCENT, WIDE_MIN_WIDTH_PX, normalize_zoom

DEFAULT_THEME = "Amber"
THEMES: dict[str, dict[str, str]] = {
    "Amber": {
        "background": "#061019", "surface": "#0A1927", "surface_alt": "#102438",
        "surface_soft": "#0C1C2B", "sidebar": "#071522", "text": "#F6F8FB",
        "muted": "#B7C4D2", "accent": "#FFB11B", "accent_hover": "#FFC44D",
        "accent_soft": "#35280F", "cyan": "#34D9FF", "green": "#48E69B",
        "yellow": "#FFD66B", "red": "#FF7180", "red_soft": "#35171E",
        "blocked": "#93A8BA", "border": "#52718C", "border_soft": "#38546B",
        "hover": "#19354B", "active_nav": "#18344A", "header_section": "#173149",
        "inverse_text": "#07111A", "input_bg": "#263C50", "input_border": "#66839A", "placeholder": "#C7D4DF",
    },
    "Türkis": {
        "background": "#051419", "surface": "#0A2026", "surface_alt": "#103038",
        "surface_soft": "#0B252B", "sidebar": "#061A20", "text": "#F4FEFF",
        "muted": "#B6DDE2", "accent": "#40F2E2", "accent_hover": "#83FFF4",
        "accent_soft": "#143B3A", "cyan": "#5DE8FF", "green": "#61F2A6",
        "yellow": "#FFE06A", "red": "#FF7A8A", "red_soft": "#3A1B22",
        "blocked": "#9BC2C7", "border": "#3F7C86", "border_soft": "#2F5E66",
        "hover": "#143B43", "active_nav": "#143A42", "header_section": "#153D45",
        "inverse_text": "#041012", "input_bg": "#244A50", "input_border": "#4E8188", "placeholder": "#C8E5E8",
    },
    "Lila": {
        "background": "#120B1B", "surface": "#1B1028", "surface_alt": "#2B1840",
        "surface_soft": "#211330", "sidebar": "#160D22", "text": "#FFF7FF",
        "muted": "#D7C2E5", "accent": "#DFA0FF", "accent_hover": "#F0C4FF",
        "accent_soft": "#432653", "cyan": "#69E6FF", "green": "#62E6A7",
        "yellow": "#FFD86A", "red": "#FF7C92", "red_soft": "#431C2B",
        "blocked": "#C0A6D0", "border": "#80609B", "border_soft": "#5B4070",
        "hover": "#3B2251", "active_nav": "#38204D", "header_section": "#3D2353",
        "inverse_text": "#13081A", "input_bg": "#4A3558", "input_border": "#8A6A9F", "placeholder": "#E0D2E8",
    },
    "Kontrast": {
        "background": "#000000", "surface": "#0A0A0A", "surface_alt": "#161616",
        "surface_soft": "#0F0F0F", "sidebar": "#050505", "text": "#FFFFFF",
        "muted": "#E6E6E6", "accent": "#FFD800", "accent_hover": "#FFF176",
        "accent_soft": "#3A3200", "cyan": "#00E5FF", "green": "#00E676",
        "yellow": "#FFEA00", "red": "#FF5252", "red_soft": "#3A0000",
        "blocked": "#C7C7C7", "border": "#FFFFFF", "border_soft": "#BDBDBD",
        "hover": "#242424", "active_nav": "#1B1B1B", "header_section": "#202020",
        "inverse_text": "#000000", "input_bg": "#222222", "input_border": "#BDBDBD", "placeholder": "#E0E0E0",
    },
}
THEME_NAMES = tuple(THEMES)
COLORS = dict(THEMES[DEFAULT_THEME])  # Rückwärtskompatible Standardpalette.

SPACING = {"xs": 5, "s": 8, "m": 12, "l": 16, "xl": 22}
FONTS = {"body_size": 10, "small_size": 9, "section_size": 12, "title_size": 16, "hero_size": 19}
UI_FONT_FAMILY = "Sans Serif"

SEVERITY_STATUS = {
    "INFO": ("●", COLORS["green"]), "HINWEIS": ("●", COLORS["green"]),
    "WARNUNG": ("●", COLORS["yellow"]), "FEHLER": ("●", COLORS["red"]),
    "KRITISCH": ("●", COLORS["red"]), "SCHWER": ("●", COLORS["red"]),
    "ABSTURZ": ("●", COLORS["red"]),
}


def theme_colors(theme_name: str | None = None) -> dict[str, str]:
    return THEMES.get(theme_name or DEFAULT_THEME, THEMES[DEFAULT_THEME])


def _application_theme_name() -> str:
    app = QApplication.instance()
    if app is not None:
        value = app.property("provowareTheme")
        if isinstance(value, str) and value in THEMES:
            return value
    return DEFAULT_THEME


def scaled(value: int, zoom_percent: int) -> int:
    """Skaliert Schriftwerte vollständig mit dem gewählten Zoom."""
    return max(1, round(value * zoom_percent / 100))


def geometry_scaled(value: int, zoom_percent: int) -> int:
    """Skaliert Geometrie bewusst flacher als Schrift.

    200 % Schriftzoom darf nicht gleichzeitig alle Abstände, Radien und
    Mindesthöhen verdoppeln. Die Geometrie wächst deshalb maximal um 25 %.
    """
    zoom = normalize_zoom(zoom_percent)
    factor = 1.0 + ((zoom - 100) / 100.0) * 0.25
    return max(1, round(value * factor))


def _zoom_percent(window: QWidget) -> int:
    return normalize_zoom(getattr(window, "zoom_percent", 100))


def app_stylesheet(zoom_percent: int = 100, theme_name: str = DEFAULT_THEME) -> str:
    colors = theme_colors(theme_name)
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
    focus_width = 3 if theme_name == "Kontrast" else 2
    return f"""
    QWidget {{
        background:{colors['background']}; color:{colors['text']};
        font-family:"{UI_FONT_FAMILY}"; font-size:{body}pt;
    }}
    QWidget#dashboardShell {{ background:{colors['background']}; }}
    QFrame#header, QFrame#toolbar, QFrame#statusBar {{
        background:{colors['surface_soft']}; border:1px solid {colors['border_soft']};
        border-radius:{radius}px;
    }}
    QFrame#sidebar {{
        background:{colors['sidebar']}; border:1px solid {colors['border_soft']};
        border-radius:{radius}px;
    }}
    QFrame#card {{
        background:{colors['surface']}; border:1px solid {colors['border']};
        border-radius:{radius}px;
    }}
    QFrame#innerCard {{
        background:{colors['surface_alt']}; border:1px solid {colors['border_soft']};
        border-radius:{radius}px;
    }}
    QLabel {{ background:transparent; border:none; }}
    QLabel#appTitle {{ font-size:{hero}pt; font-weight:700; letter-spacing:0.2px; }}
    QLabel#subtitle, QLabel#muted, QLabel#cardHint {{ color:{colors['muted']}; font-size:{small}pt; }}
    QLabel#sectionTitle {{ font-size:{title}pt; font-weight:700; }}
    QLabel#cardTitle {{ font-size:{section}pt; font-weight:700; }}
    QLabel#accent {{ color:{colors['accent']}; font-weight:700; }}
    QLabel#statusGood {{ color:{colors['green']}; font-weight:700; }}

    QPushButton, QToolButton {{
        background:{colors['surface_alt']}; color:{colors['text']};
        border:1px solid {colors['border']}; border-radius:{radius}px;
        padding:{pad_v}px {pad_h}px; min-height:{control_height}px; text-align:center;
    }}
    QPushButton:hover, QToolButton:hover {{
        border-color:{colors['accent_hover']}; background:{colors['hover']};
    }}
    QPushButton:pressed, QToolButton:pressed {{
        background:{colors['accent_soft']}; border-color:{colors['accent']};
    }}
    QPushButton#primaryButton {{
        border:1px solid {colors['accent']}; background:{colors['accent_soft']};
        font-weight:700;
    }}
    QPushButton#primaryButton:hover {{ background:{colors['accent']}; color:{colors['inverse_text']}; }}
    QPushButton#dangerButton {{ border:1px solid {colors['red']}; background:{colors['red_soft']}; }}
    QPushButton#dangerButton:hover {{ background:{colors['red']}; color:{colors['inverse_text']}; }}
    QPushButton[planned="true"] {{
        color:{colors['muted']}; border:1px dashed {colors['blocked']};
        background:{colors['surface_soft']};
    }}
    QPushButton[planned="true"]:hover {{ color:{colors['text']}; border-color:{colors['yellow']}; }}
    QPushButton#navButton {{
        text-align:left; border:none; background:transparent;
        padding:{nav_pad_v}px {nav_pad_h}px;
        min-height:{geometry_scaled(22, zoom_percent)}px;
    }}
    QPushButton#navButton:hover {{ background:{colors['surface_alt']}; }}
    QPushButton#activeNav {{
        text-align:left; background:{colors['active_nav']}; color:{colors['text']}; font-weight:700;
        border:1px solid {colors['border']}; border-left:3px solid {colors['accent']};
        border-radius:{geometry_scaled(6, zoom_percent)}px;
        padding:{nav_pad_v}px {nav_pad_h}px;
        min-height:{geometry_scaled(22, zoom_percent)}px;
    }}
    QPushButton#tileButton {{ min-height:{geometry_scaled(54, zoom_percent)}px; font-weight:600; }}
    QPushButton#tileButton[ready="true"] {{
        background:{colors['header_section']}; border-bottom:2px solid {colors['accent']};
    }}
    QPushButton#recentSongButton {{ text-align:left; }}
    QPushButton#closeWindowButton {{
        border:1px solid {colors['border']}; background:{colors['surface_soft']}; font-weight:700;
    }}
    QPushButton#closeWindowButton:hover {{ border-color:{colors['accent']}; background:{colors['hover']}; }}
    QPushButton#featureButton {{ min-height:{geometry_scaled(82, zoom_percent)}px; font-weight:600; }}

    QLineEdit, QTextEdit, QPlainTextEdit {{
        background:{colors['input_bg']}; color:{colors['text']};
        border:1px solid {colors['input_border']}; border-radius:{radius}px;
        padding:{geometry_scaled(5, zoom_percent)}px;
        placeholder-text-color:{colors['placeholder']};
        selection-background-color:{colors['accent_soft']}; selection-color:{colors['text']};
    }}
    QListWidget, QTreeWidget, QTableWidget {{
        background:{colors['surface']}; color:{colors['text']};
        border:1px solid {colors['border']}; border-radius:{radius}px;
        padding:{geometry_scaled(5, zoom_percent)}px;
        selection-background-color:{colors['accent_soft']}; selection-color:{colors['text']};
    }}
    QLineEdit {{ min-height:{control_height}px; }}
    QComboBox {{
        background:{colors['input_bg']}; color:{colors['text']};
        border:1px solid {colors['input_border']}; border-radius:{radius}px;
        padding:{geometry_scaled(3, zoom_percent)}px {geometry_scaled(6, zoom_percent)}px;
        min-height:{control_height}px;
        selection-background-color:{colors['accent_soft']}; selection-color:{colors['text']};
    }}
    QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border:{focus_width}px solid {colors['accent']};
    }}
    QLineEdit[fieldState="error"], QComboBox[fieldState="error"], QTextEdit[fieldState="error"], QPlainTextEdit[fieldState="error"] {{
        border:{focus_width}px solid {colors['red']};
    }}
    QLineEdit[fieldState="valid"], QComboBox[fieldState="valid"], QTextEdit[fieldState="valid"], QPlainTextEdit[fieldState="valid"] {{
        border:{focus_width}px solid {colors['green']};
    }}
    QListWidget:focus, QTreeWidget:focus, QTableWidget:focus, QPushButton:focus, QToolButton:focus {{
        border:{focus_width}px solid {colors['cyan']};
    }}
    QComboBox::drop-down {{ border:none; width:{geometry_scaled(24, zoom_percent)}px; }}
    QHeaderView::section {{
        background:{colors['header_section']}; color:{colors['text']}; border:none;
        border-right:1px solid {colors['border_soft']}; border-bottom:1px solid {colors['border']};
        padding:{geometry_scaled(6, zoom_percent)}px; font-weight:700;
    }}
    QTreeWidget, QTableWidget {{ alternate-background-color:{colors['surface_soft']}; outline:0; }}
    QTreeWidget::item, QTableWidget::item {{ padding:{geometry_scaled(2, zoom_percent)}px; }}
    QTreeWidget::item:selected, QTableWidget::item:selected {{
        background:{colors['accent_soft']}; color:{colors['text']};
    }}
    QTabWidget::pane {{ border:1px solid {colors['border_soft']}; border-radius:{radius}px; }}
    QTabBar::tab {{
        background:{colors['surface_soft']}; color:{colors['muted']};
        border:1px solid {colors['border_soft']};
        padding:{geometry_scaled(6, zoom_percent)}px {geometry_scaled(11, zoom_percent)}px;
    }}
    QTabBar::tab:selected {{ color:{colors['text']}; border-bottom:2px solid {colors['accent']}; background:{colors['surface_alt']}; }}
    QCheckBox {{ spacing:{geometry_scaled(6, zoom_percent)}px; }}
    QSplitter::handle {{ background:{colors['border_soft']}; width:{geometry_scaled(5, zoom_percent)}px; }}
    QSplitter::handle:hover {{ background:{colors['accent']}; }}
    QMenu {{ background:{colors['surface']}; color:{colors['text']}; border:1px solid {colors['border']}; }}
    QMenu::item {{ padding:{geometry_scaled(6, zoom_percent)}px {geometry_scaled(12, zoom_percent)}px; }}
    QMenu::item:selected {{ background:{colors['accent_soft']}; }}
    QToolTip {{ background:{colors['surface_alt']}; color:{colors['text']}; border:1px solid {colors['accent']}; padding:5px; }}
    QScrollBar:vertical {{ background:{colors['surface_soft']}; width:{geometry_scaled(10, zoom_percent)}px; margin:0; }}
    QScrollBar::handle:vertical {{ background:{colors['border']}; min-height:{geometry_scaled(28, zoom_percent)}px; border-radius:{geometry_scaled(5, zoom_percent)}px; }}
    QScrollBar::handle:vertical:hover {{ background:{colors['accent']}; }}
    QScrollBar:add-line:vertical, QScrollBar:sub-line:vertical {{ height:0; }}
    QScrollBar:horizontal {{ background:{colors['surface_soft']}; height:{geometry_scaled(10, zoom_percent)}px; margin:0; }}
    QScrollBar::handle:horizontal {{ background:{colors['border']}; min-width:{geometry_scaled(28, zoom_percent)}px; border-radius:{geometry_scaled(5, zoom_percent)}px; }}
    QScrollBar::handle:horizontal:hover {{ background:{colors['accent']}; }}
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
    """Schaltet das Dashboard bei 175/200 % auf eine verlustarme Hochzoomansicht."""
    if window.__class__.__name__ != "Dashboard":
        return

    nav_collapsed = bool(getattr(window, "nav_collapsed", False))
    for button in window.findChildren(QPushButton):
        if button.objectName() == "navButton" and button.property("planned") is True:
            button.setMaximumHeight(0 if high_zoom else 16777215)
            button.setVisible(not high_zoom and not nav_collapsed)
        elif button.objectName() == "tileButton" and button.property("planned") is True:
            button.setVisible(not high_zoom)

    for card in window.findChildren(QFrame):
        if card.objectName() != "card":
            continue
        title = _card_title(card)
        if title.startswith("▣  Funktionen") or title.startswith("▤  Dateien & Werkzeuge"):
            card.setVisible(not high_zoom)

    # Header: bei 200 % keine abgeschnittene Produktbezeichnung und keine
    # redundante Unterzeile, die Platz von Suche und Beenden nimmt.
    title = getattr(window, "app_title_label", None)
    if isinstance(title, QLabel):
        title.setText("Provoware Dashboard 2026" if high_zoom else "Provoware-Datenbank-Dashboard 2026")
    subtitle = getattr(window, "header_subtitle", None)
    if isinstance(subtitle, QLabel):
        subtitle.setVisible(not high_zoom)
    search_icon = getattr(window, "header_search_icon", None)
    if isinstance(search_icon, QLabel):
        search_icon.setVisible(not high_zoom)
    quit_button = getattr(window, "quit_button", None)
    if isinstance(quit_button, QPushButton):
        quit_button.setText("Beenden" if high_zoom else "Programm beenden")

    quick_label = getattr(window, "quick_info_label", None)
    if isinstance(quick_label, QLabel):
        quick_label.setText("Notiz:" if high_zoom else "Projekt-Notiz:")
    quick_save = getattr(window, "quick_save_button", None)
    if isinstance(quick_save, QPushButton):
        quick_save.setText("Speichern" if high_zoom else "Notiz speichern")

    # Breite Einzelbuttons für letzte Songs werden im Hochzoom durch ein einziges
    # Auswahlfeld ersetzt. Dadurch bleiben alle fünf Einträge erreichbar, ohne
    # dass lange Songtitel andere Bedienelemente verdecken.
    for recent in getattr(window, "_recent_widgets", ()):  # type: ignore[attr-defined]
        if isinstance(recent, QWidget):
            recent.setVisible(not high_zoom)
    recent_label = getattr(window, "recent_label", None)
    if isinstance(recent_label, QLabel):
        recent_label.setText("Letzte Songs" if high_zoom else "Zuletzt bearbeitete Songs")
    recent_combo = getattr(window, "recent_combo", None)
    if isinstance(recent_combo, QComboBox):
        recent_combo.setVisible(high_zoom)
    recent_open = getattr(window, "recent_open_button", None)
    if isinstance(recent_open, QPushButton):
        recent_open.setVisible(high_zoom)

    for label in window.findChildren(QLabel):
        text = label.text()
        if text.startswith("Tipp: Für Genres, Stimmung, Stil oder Stimme"):
            label.setVisible(not high_zoom)
        elif text == "GitHub-Repositories und Prompts: In Planung":
            label.setVisible(not high_zoom)
        elif text == "Profil:":
            label.setVisible(not high_zoom)
        elif text.startswith("Wähle einen fertigen Bereich."):
            label.setText(
                "Wähle einen fertigen Bereich." if high_zoom
                else "Wähle einen fertigen Bereich.\nGeplante Funktionen sind deutlich mit „In Planung“ markiert."
            )

    legend = getattr(window, "status_legend", None)
    if isinstance(legend, QLabel):
        legend.setVisible(not high_zoom)
    theme_label = getattr(window, "theme_label", None)
    if isinstance(theme_label, QLabel):
        theme_label.setText("Theme:" if high_zoom else "Farben:")


def _apply_responsive_layout(window: QWidget) -> None:
    if window.property("provowareResponsiveBusy"):
        return
    window.setProperty("provowareResponsiveBusy", True)
    try:
        width = max(window.width(), window.minimumWidth())
        height = max(window.height(), window.minimumHeight())
        zoom = _zoom_percent(window)
        compact = width < 1100
        wide = width >= WIDE_MIN_WIDTH_PX
        high_zoom = zoom >= HIGH_ZOOM_MIN_PERCENT
        module_compact = width < 1180 or height < 760 or zoom >= 150
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

        compact_handler = getattr(window, "set_compact_mode", None)
        if callable(compact_handler) and window.__class__.__name__ in {"SongEditor", "SongLibrary"}:
            compact_handler(module_compact)

        for card in window.findChildren(QFrame):
            if card.objectName() in {"card", "innerCard"}:
                card.setMinimumWidth(0)
                card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        sidebar = getattr(window, "sidebar", None)
        if isinstance(sidebar, QWidget) and not getattr(window, "nav_collapsed", False):
            base = 198 if compact else (258 if wide else 226)
            if high_zoom:
                # Kurze Hochzoom-Labels erlauben eine schmalere Navigation und
                # geben dem eigentlichen Arbeitsbereich wieder mehr Platz.
                base = 224
            _set_width(sidebar, round(base * width_factor))

        search = getattr(window, "search_entry", None)
        if isinstance(search, QWidget):
            if window.__class__.__name__ == "Dashboard":
                base = 190 if compact else (320 if wide else 250)
                if high_zoom:
                    base = 205
                _set_width(search, round(base * width_factor))
            elif window.__class__.__name__ == "SongLibrary":
                search.setMinimumWidth(round(220 * width_factor))
                search.setMaximumWidth(16777215)
                if hasattr(search, "setPlaceholderText"):
                    search.setPlaceholderText("Songtitel, Genre, Stimmung, Stil, Stimme oder Tag eingeben …")

        theme_combo = getattr(window, "theme_combo", None)
        if isinstance(theme_combo, QComboBox):
            _set_width(theme_combo, round((90 if high_zoom else 132) * width_factor))

        profile_combo = getattr(window, "db_profile_combo", None)
        if isinstance(profile_combo, QWidget):
            minimum = round((100 if high_zoom else (110 if compact else 135)) * width_factor)
            maximum = round((135 if high_zoom else (190 if wide else 160)) * width_factor)
            profile_combo.setMinimumWidth(minimum)
            profile_combo.setMaximumWidth(maximum)

        for label in window.findChildren(QLabel):
            if label.text() in {"Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten"}:
                if high_zoom:
                    # Keine starre Mini-Breite bei doppelter Schriftgröße: die
                    # längste Beschriftung muss vollständig lesbar bleiben.
                    base = max(128, label.fontMetrics().horizontalAdvance(label.text()) + 18)
                    _set_width(label, base)
                else:
                    base = 94 if compact else (128 if wide else 108)
                    _set_width(label, round(base * width_factor))

        for button in window.findChildren(QPushButton):
            if button.text() in {"Profile & Werte bearbeiten", "Profile bearbeiten", "Profile"}:
                if high_zoom:
                    button.setText("Profile")
                else:
                    button.setText("Profile & Werte bearbeiten" if wide else "Profile bearbeiten")

        if window.__class__.__name__ == "CalendarWindow":
            today_button = window.findChild(QPushButton, "calendarTodayButton")
            refresh_button = window.findChild(QPushButton, "calendarRefreshButton")
            close_button = window.findChild(QPushButton, "closeWindowButton")
            if today_button is not None:
                today_button.setText("Heute" if high_zoom else "Heute anzeigen")
            if refresh_button is not None:
                refresh_button.setText("Aktualisieren" if high_zoom else "Ansicht aktualisieren")
            if close_button is not None:
                close_button.setText("Schließen" if high_zoom else "Kalender schließen")

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
                    QHeaderView.Stretch, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents,
                    QHeaderView.ResizeToContents, QHeaderView.ResizeToContents, QHeaderView.Stretch,
                    QHeaderView.ResizeToContents, QHeaderView.ResizeToContents,
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


def _clean_accessible_text(text: str) -> str:
    compact = " ".join((text or "").replace("\n", " ").split())
    return compact.lstrip("♫▣▤▥?⌕≡◈✎◫▦⚕✓●①②③ ·") or compact


def _apply_accessibility(widget: QWidget) -> None:
    """Ergänzt robuste Tastatur- und Screenreader-Grundwerte ohne Fachlogik."""
    interactive_types = (
        QPushButton, QToolButton, QLineEdit, QTextEdit, QPlainTextEdit,
        QComboBox, QCheckBox, QListWidget, QTreeWidget, QTableWidget,
    )
    for control_type in interactive_types:
        for control in widget.findChildren(control_type):
            control.setFocusPolicy(Qt.StrongFocus)
            if control.accessibleDescription() == "" and control.toolTip():
                control.setAccessibleDescription(control.toolTip())
            if control.accessibleName():
                continue
            name = ""
            if isinstance(control, (QPushButton, QToolButton, QCheckBox)):
                name = _clean_accessible_text(control.text())
            elif isinstance(control, QLineEdit):
                name = _clean_accessible_text(control.placeholderText())
            elif isinstance(control, (QTextEdit, QPlainTextEdit)):
                name = _clean_accessible_text(control.placeholderText())
            elif isinstance(control, QComboBox):
                name = _clean_accessible_text(control.objectName().replace("_", " ")) if control.objectName() else "Auswahlfeld"
            elif isinstance(control, (QTreeWidget, QTableWidget)):
                name = _clean_accessible_text(control.objectName().replace("_", " ")) if control.objectName() else "Tabelle"
            elif isinstance(control, QListWidget):
                name = _clean_accessible_text(control.objectName().replace("_", " ")) if control.objectName() else "Liste"
            if name:
                control.setAccessibleName(name)


def _refresh_accent_labels(widget: QWidget, theme_name: str) -> None:
    colors = theme_colors(theme_name)
    for label in widget.findChildren(QLabel):
        if label.objectName() == "accent" and label.styleSheet():
            style = label.styleSheet()
            if "font-size: 23pt" in style:
                label.setStyleSheet(f"font-size: 23pt; color: {colors['accent']}; font-weight: 700;")


def _apply_theme_to_widget(widget: QWidget, zoom_percent: int, theme_name: str) -> None:
    widget.theme_name = theme_name  # type: ignore[attr-defined]
    widget.setStyleSheet(app_stylesheet(zoom_percent, theme_name))
    font = QFont(UI_FONT_FAMILY)
    font.setPointSize(scaled(FONTS["body_size"], zoom_percent))
    widget.setFont(font)
    _refresh_accent_labels(widget, theme_name)
    _apply_accessibility(widget)
    _install_responsive_layout(widget)


def set_application_theme(theme_name: str) -> None:
    """Wechselt das Theme für alle geöffneten Provoware-Fenster derselben Sitzung."""
    if theme_name not in THEMES:
        return
    app = QApplication.instance()
    if app is None:
        return
    app.setProperty("provowareTheme", theme_name)
    for top in app.topLevelWidgets():
        if not isinstance(top, QWidget):
            continue
        _apply_theme_to_widget(top, _zoom_percent(top), theme_name)
        combo = getattr(top, "theme_combo", None)
        if isinstance(combo, QComboBox) and combo.currentText() != theme_name:
            combo.blockSignals(True)
            combo.setCurrentText(theme_name)
            combo.blockSignals(False)


def _install_theme_selector(widget: QWidget) -> None:
    """Fügt dem Dashboard einen kompakten, tastaturbedienbaren Theme-Schalter hinzu."""
    if widget.__class__.__name__ != "Dashboard" or hasattr(widget, "theme_combo"):
        return
    status = None
    for frame in widget.findChildren(QFrame):
        if frame.objectName() == "statusBar":
            status = frame
            break
    if status is None or status.layout() is None:
        return

    layout = status.layout()
    legend = None
    for label in status.findChildren(QLabel):
        if label.text().startswith("Gestrichelt"):
            legend = label
            break
    widget.status_legend = legend  # type: ignore[attr-defined]

    label = QLabel("Farben:")
    label.setObjectName("muted")
    widget.theme_label = label  # type: ignore[attr-defined]
    combo = QComboBox()
    combo.setObjectName("theme_selector")
    combo.addItems(THEME_NAMES)
    combo.setCurrentText(_application_theme_name())
    combo.setToolTip("Farbtheme für alle geöffneten Provoware-Fenster. Die Auswahl gilt für diese Sitzung.")
    combo.setAccessibleName("Farbtheme auswählen")
    combo.setAccessibleDescription("Wähle Amber, Türkis, Lila oder Kontrast. Die Auswahl verändert keine Nutzerdaten.")
    combo.currentTextChanged.connect(set_application_theme)
    widget.theme_combo = combo  # type: ignore[attr-defined]

    if legend is not None:
        index = layout.indexOf(legend)
        layout.insertWidget(index, label)
        layout.insertWidget(index + 1, combo)
    else:
        layout.addWidget(label)
        layout.addWidget(combo)


def apply_global_style(widget: QWidget, zoom_percent: int = 100, theme_name: str | None = None) -> None:
    selected = theme_name or getattr(widget, "theme_name", None) or _application_theme_name()
    if selected not in THEMES:
        selected = DEFAULT_THEME
    app = QApplication.instance()
    if app is not None and app.property("provowareTheme") is None:
        app.setProperty("provowareTheme", selected)
    _apply_theme_to_widget(widget, zoom_percent, selected)
    _install_theme_selector(widget)
    _apply_accessibility(widget)
    _apply_responsive_layout(widget)


def configure_application(app: QApplication, zoom_percent: int = 100, theme_name: str = DEFAULT_THEME) -> None:
    app.setStyle("Fusion")
    app.setProperty("provowareTheme", theme_name if theme_name in THEMES else DEFAULT_THEME)
    font = QFont(UI_FONT_FAMILY)
    font.setPointSize(scaled(FONTS["body_size"], zoom_percent))
    app.setFont(font)
    app.setStyleSheet(app_stylesheet(zoom_percent, _application_theme_name()))


def severity_display(severity: str, theme_name: str | None = None) -> tuple[str, str]:
    colors = theme_colors(theme_name or _application_theme_name())
    key = severity.upper()
    color_key = "green" if key in {"INFO", "HINWEIS"} else "yellow" if key == "WARNUNG" else "red" if key in {"FEHLER", "KRITISCH", "SCHWER", "ABSTURZ"} else "blocked"
    return "●", colors[color_key]
