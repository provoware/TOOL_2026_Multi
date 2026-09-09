"""Globale PySide6-Oberflächenstandards nach dem Dashboard-Referenzentwurf."""

from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget

COLORS = {
    "background": "#06111D",
    "surface": "#0B1A28",
    "surface_alt": "#102538",
    "surface_soft": "#0C1D2B",
    "sidebar": "#071522",
    "text": "#F4F8FC",
    "muted": "#9DB0C4",
    "accent": "#FF9800",
    "accent_hover": "#FFAE2B",
    "accent_soft": "#39270E",
    "cyan": "#18D9FF",
    "green": "#3DE783",
    "yellow": "#FFD166",
    "red": "#FF6475",
    "blocked": "#6F8398",
    "border": "#27425A",
}

SPACING = {"xs": 4, "s": 7, "m": 10, "l": 15, "xl": 20}
FONTS = {"body_size": 10, "small_size": 8, "section_size": 11, "title_size": 15, "hero_size": 18}

SEVERITY_STATUS = {
    "INFO": ("●", COLORS["green"]), "HINWEIS": ("●", COLORS["green"]),
    "WARNUNG": ("●", COLORS["yellow"]), "FEHLER": ("●", COLORS["red"]),
    "KRITISCH": ("●", COLORS["red"]), "SCHWER": ("●", COLORS["red"]),
    "ABSTURZ": ("●", COLORS["red"]),
}


def scaled(value: int, zoom_percent: int) -> int:
    return max(1, round(value * zoom_percent / 100))


def app_stylesheet(zoom_percent: int = 100) -> str:
    body = scaled(FONTS["body_size"], zoom_percent)
    small = scaled(FONTS["small_size"], zoom_percent)
    section = scaled(FONTS["section_size"], zoom_percent)
    title = scaled(FONTS["title_size"], zoom_percent)
    hero = scaled(FONTS["hero_size"], zoom_percent)
    radius = scaled(5, zoom_percent)
    pad = scaled(7, zoom_percent)
    return f"""
    QWidget {{ background:{COLORS['background']}; color:{COLORS['text']}; font-size:{body}pt; }}
    QWidget#dashboardShell {{ background:{COLORS['background']}; }}
    QFrame#header, QFrame#toolbar, QFrame#statusBar {{ background:{COLORS['surface_soft']}; border:1px solid {COLORS['border']}; border-radius:{radius}px; }}
    QFrame#sidebar {{ background:{COLORS['sidebar']}; border:1px solid {COLORS['border']}; border-radius:{radius}px; }}
    QFrame#card {{ background:{COLORS['surface']}; border:1px solid {COLORS['accent']}; border-radius:{radius}px; }}
    QFrame#innerCard {{ background:{COLORS['surface_alt']}; border:1px solid {COLORS['border']}; border-radius:{radius}px; }}
    QLabel {{ background:transparent; border:none; }}
    QLabel#appTitle {{ font-size:{hero}pt; font-weight:700; }}
    QLabel#subtitle, QLabel#muted, QLabel#cardHint {{ color:{COLORS['muted']}; font-size:{small}pt; }}
    QLabel#sectionTitle {{ font-size:{title}pt; font-weight:700; }}
    QLabel#cardTitle {{ font-size:{section}pt; font-weight:700; }}
    QLabel#accent {{ color:{COLORS['accent']}; font-weight:700; }}
    QLabel#statusGood {{ color:{COLORS['green']}; font-weight:700; }}
    QPushButton {{ background:{COLORS['surface_alt']}; border:1px solid {COLORS['border']}; border-radius:{radius}px; padding:{pad}px {scaled(10, zoom_percent)}px; text-align:center; }}
    QPushButton:hover {{ border-color:{COLORS['accent']}; background:{COLORS['accent_soft']}; }}
    QPushButton:pressed {{ background:{COLORS['accent']}; color:#07111A; }}
    QPushButton#primaryButton {{ border:2px solid {COLORS['accent']}; background:{COLORS['accent_soft']}; font-weight:700; }}
    QPushButton#dangerButton {{ border:1px solid {COLORS['red']}; }}
    QPushButton[planned="true"] {{ color:{COLORS['muted']}; border:1px dashed {COLORS['blocked']}; background:{COLORS['surface_soft']}; }}
    QPushButton[planned="true"]:hover {{ color:{COLORS['text']}; border-color:{COLORS['yellow']}; }}
    QPushButton#navButton {{ text-align:left; border:none; background:transparent; padding:{scaled(5, zoom_percent)}px {scaled(8, zoom_percent)}px; }}
    QPushButton#navButton:hover {{ background:{COLORS['surface_alt']}; }}
    QPushButton#activeNav {{ text-align:left; border:none; background:{COLORS['accent']}; color:#07111A; font-weight:700; }}
    QPushButton#tileButton {{ min-height:{scaled(48, zoom_percent)}px; font-weight:600; }}
    QPushButton#featureButton {{ min-height:{scaled(78, zoom_percent)}px; font-weight:600; }}
    QLineEdit, QTextEdit, QPlainTextEdit, QListWidget, QTreeWidget, QTableWidget {{ background:{COLORS['surface']}; color:{COLORS['text']}; border:1px solid {COLORS['border']}; border-radius:{radius}px; padding:{scaled(4, zoom_percent)}px; selection-background-color:{COLORS['accent_soft']}; selection-color:{COLORS['text']}; }}
    QComboBox {{ background:{COLORS['surface']}; color:{COLORS['text']}; border:1px solid {COLORS['border']}; border-radius:{radius}px; padding:{scaled(2, zoom_percent)}px {scaled(4, zoom_percent)}px; max-height:{scaled(24, zoom_percent)}px; selection-background-color:{COLORS['accent_soft']}; }}
    QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus, QListWidget:focus, QTreeWidget:focus, QTableWidget:focus, QPushButton:focus {{ border:2px solid {COLORS['accent']}; }}
    QComboBox::drop-down {{ border:none; width:{scaled(20, zoom_percent)}px; }}
    QHeaderView::section {{ background:{COLORS['surface_alt']}; color:{COLORS['text']}; border:none; border-right:1px solid {COLORS['border']}; padding:{scaled(6, zoom_percent)}px; font-weight:700; }}
    QTreeWidget, QTableWidget {{ alternate-background-color:{COLORS['surface_soft']}; }}
    QCheckBox {{ spacing:{scaled(6, zoom_percent)}px; }}
    QSplitter::handle {{ background:{COLORS['border']}; width:1px; }}
    QMenu {{ background:{COLORS['surface']}; color:{COLORS['text']}; border:1px solid {COLORS['border']}; }}
    QMenu::item:selected {{ background:{COLORS['accent_soft']}; }}
    QToolTip {{ background:{COLORS['surface_alt']}; color:{COLORS['text']}; border:1px solid {COLORS['accent']}; }}
    """


def apply_global_style(widget: QWidget, zoom_percent: int = 100) -> None:
    widget.setStyleSheet(app_stylesheet(zoom_percent))
    font = QFont(widget.font())
    font.setPointSize(scaled(FONTS["body_size"], zoom_percent))
    widget.setFont(font)


def configure_application(app: QApplication, zoom_percent: int = 100) -> None:
    app.setStyle("Fusion")
    app.setStyleSheet(app_stylesheet(zoom_percent))


def severity_display(severity: str) -> tuple[str, str]:
    return SEVERITY_STATUS.get(severity.upper(), ("●", COLORS["blocked"]))
