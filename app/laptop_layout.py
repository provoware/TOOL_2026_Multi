"""Gezielte Dashboard-Anpassung für kleine Laptop-Bildschirme.

Die große Ansicht bleibt unangetastet. Der Modus wird nur bei knapper Fläche
und 125/150 % Zoom aktiv und blendet ausschließlich redundante Planungsinfos aus.
"""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, QTimer
from PySide6.QtWidgets import QComboBox, QFrame, QLabel, QPushButton, QWidget


def _zoom_percent(window: QWidget) -> int:
    try:
        return max(100, min(200, int(getattr(window, "zoom_percent", 100))))
    except (TypeError, ValueError):
        return 100


def _is_laptop_compact(window: QWidget) -> bool:
    if window.__class__.__name__ != "Dashboard":
        return False
    width = max(window.width(), window.minimumWidth())
    height = max(window.height(), window.minimumHeight())
    zoom = _zoom_percent(window)
    if width >= 1450 or not 125 <= zoom < 175:
        return False
    effective_height = height * 100 / zoom
    return height < 820 or effective_height < 700


def _card_title(card: QFrame) -> str:
    for label in card.findChildren(QLabel):
        if label.objectName() == "cardTitle":
            return label.text()
    return ""


def apply_laptop_layout(window: QWidget) -> None:
    """Verdichtet nur die kleine Dashboard-Ansicht und stellt sie reversibel wieder her."""
    compact = _is_laptop_compact(window)
    was_compact = bool(window.property("provowareLaptopCompact"))

    # Ist der Laptop-Modus weder aktiv noch zu restaurieren, darf diese Schicht
    # nichts anfassen. So bleiben normale Großansicht und 175/200-%-Hochzoom
    # vollständig unter Kontrolle der bereits geprüften zentralen UI-Standards.
    if not compact and not was_compact:
        return

    nav_collapsed = bool(getattr(window, "nav_collapsed", False))

    for button in window.findChildren(QPushButton):
        if button.objectName() == "navButton" and button.property("planned") is True:
            if compact:
                button.setMaximumHeight(0)
                button.setVisible(False)
            else:
                button.setMaximumHeight(16777215)
                button.setVisible(not nav_collapsed)
        if button.text() in {"Profile & Werte bearbeiten", "Profile bearbeiten", "Profile"}:
            button.setText("Profile" if compact else (
                "Profile & Werte bearbeiten" if window.width() >= 1450 else "Profile bearbeiten"
            ))

    for label in window.findChildren(QLabel):
        text = label.text()
        if text in {"⌄  Funktionen", "⌄  Dateien & Werkzeuge"}:
            label.setVisible(not compact and not nav_collapsed)
        elif text.startswith("Tipp: Für Genres, Stimmung, Stil oder Stimme"):
            label.setVisible(not compact)
        elif text == "GitHub-Repositories und Prompts: In Planung":
            label.setVisible(not compact)
        elif text == "Profil:":
            label.setVisible(not compact)
        elif text.startswith("Wähle einen fertigen Bereich."):
            label.setText(
                "Wähle einen fertigen Bereich." if compact
                else "Wähle einen fertigen Bereich.\nGeplante Funktionen sind deutlich mit „In Planung“ markiert."
            )
        elif text in {"Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten"}:
            if compact:
                label.setFixedWidth(88)
            else:
                label.setMinimumWidth(0)
                label.setMaximumWidth(16777215)

    profile_combo = getattr(window, "db_profile_combo", None)
    if isinstance(profile_combo, QComboBox):
        if compact:
            profile_combo.setMinimumWidth(92)
            profile_combo.setMaximumWidth(120)
        else:
            profile_combo.setMinimumWidth(0)
            profile_combo.setMaximumWidth(16777215)

    for card in window.findChildren(QFrame):
        if card.objectName() != "card":
            continue
        title = _card_title(card)
        if title.startswith("▣  Funktionen") or title.startswith("▤  Dateien & Werkzeuge"):
            card.setVisible(not compact)

    legend = getattr(window, "status_legend", None)
    if isinstance(legend, QLabel):
        legend.setVisible(not compact)

    window.setProperty("provowareLaptopCompact", compact)

    if was_compact and not compact:
        # Danach darf der zentrale Responsive-Standard die gute große Ansicht
        # wieder exakt nach seinen bestehenden Regeln verteilen.
        from app.ui_standards import refresh_responsive_layout
        refresh_responsive_layout(window)


class _LaptopLayoutFilter(QObject):
    def __init__(self, root: QWidget) -> None:
        super().__init__(root)
        self.root = root
        self._queued = False

    def _schedule(self) -> None:
        if self._queued:
            return
        self._queued = True

        def run() -> None:
            self._queued = False
            apply_laptop_layout(self.root)

        QTimer.singleShot(0, run)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() in {QEvent.Type.Show, QEvent.Type.Resize, QEvent.Type.LayoutRequest}:
            self._schedule()
        return False


def install_laptop_layout(window: QWidget) -> None:
    """Installiert die kleine Laptop-Anpassung genau einmal am Dashboard."""
    if getattr(window, "_provoware_laptop_layout_filter", None) is not None:
        apply_laptop_layout(window)
        return
    event_filter = _LaptopLayoutFilter(window)
    window._provoware_laptop_layout_filter = event_filter  # type: ignore[attr-defined]
    window.installEventFilter(event_filter)
    sidebar = getattr(window, "sidebar", None)
    if isinstance(sidebar, QWidget):
        sidebar.installEventFilter(event_filter)
    apply_laptop_layout(window)
