"""Sichere, portable Fenstergeometrie für eigenständige Provoware-Module."""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget

from app.atomic_io import atomic_write_json

STATE_FILE = Path("daten/ui/fenster.json")
SCREEN_MARGIN = 16
MIN_VISIBLE_WIDTH = 180
MIN_VISIBLE_HEIGHT = 120


def _state_path(project_root: Path) -> Path:
    return Path(project_root) / STATE_FILE


def _load_states(project_root: Path) -> dict[str, dict[str, object]]:
    target = _state_path(project_root)
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    result: dict[str, dict[str, object]] = {}
    for key, value in payload.items():
        if isinstance(key, str) and isinstance(value, dict):
            result[key] = value
    return result


def _available_rectangles() -> tuple[QRect, ...]:
    app = QApplication.instance()
    if app is None:
        return ()
    rectangles = tuple(screen.availableGeometry() for screen in app.screens())
    if rectangles:
        return rectangles
    primary = app.primaryScreen()
    return (primary.availableGeometry(),) if primary is not None else ()


def _fallback_available(widget: QWidget) -> QRect:
    screen = widget.screen()
    if screen is not None:
        return screen.availableGeometry()
    rectangles = _available_rectangles()
    return rectangles[0] if rectangles else QRect(0, 0, 1280, 720)


def _intersection_score(rect: QRect, available: QRect) -> int:
    intersection = rect.intersected(available)
    return max(0, intersection.width()) * max(0, intersection.height())


def _best_screen(rect: QRect, widget: QWidget) -> QRect:
    screens = _available_rectangles()
    if not screens:
        return _fallback_available(widget)
    return max(screens, key=lambda available: _intersection_score(rect, available))


def _is_usefully_visible(rect: QRect, available: QRect) -> bool:
    intersection = rect.intersected(available)
    return intersection.width() >= MIN_VISIBLE_WIDTH and intersection.height() >= MIN_VISIBLE_HEIGHT


def fit_rect_to_available(rect: QRect, available: QRect, minimum: QSize,
                          margin: int = SCREEN_MARGIN) -> QRect:
    """Begrenzt eine Geometrie auf die sichtbare Arbeitsfläche, ohne sie zu verstecken."""
    safe = available.adjusted(margin, margin, -margin, -margin)
    if safe.width() <= 0 or safe.height() <= 0:
        safe = QRect(available)

    min_width = min(max(1, minimum.width()), max(1, safe.width()))
    min_height = min(max(1, minimum.height()), max(1, safe.height()))
    width = min(max(rect.width(), min_width), max(1, safe.width()))
    height = min(max(rect.height(), min_height), max(1, safe.height()))

    max_x = safe.right() - width + 1
    max_y = safe.bottom() - height + 1
    x = min(max(rect.x(), safe.left()), max_x)
    y = min(max(rect.y(), safe.top()), max_y)
    return QRect(x, y, width, height)


def _centered_rect(available: QRect, preferred: QSize, minimum: QSize) -> QRect:
    width = min(max(preferred.width(), minimum.width()), max(1, available.width() - 2 * SCREEN_MARGIN))
    height = min(max(preferred.height(), minimum.height()), max(1, available.height() - 2 * SCREEN_MARGIN))
    x = available.x() + max(0, (available.width() - width) // 2)
    y = available.y() + max(0, (available.height() - height) // 2)
    return fit_rect_to_available(QRect(x, y, width, height), available, minimum)


def restore_window_state(widget: QWidget, project_root: Path, key: str, *,
                         preferred: QSize, minimum: QSize) -> None:
    """Stellt eine gespeicherte Position nur wieder her, wenn sie noch sichtbar ist."""
    states = _load_states(project_root)
    state = states.get(key, {})
    available = _fallback_available(widget)
    rect: QRect | None = None

    try:
        candidate = QRect(
            int(state["x"]), int(state["y"]),
            int(state["width"]), int(state["height"]),
        )
    except (KeyError, TypeError, ValueError):
        candidate = QRect()

    if candidate.isValid() and candidate.width() > 0 and candidate.height() > 0:
        best = _best_screen(candidate, widget)
        if _is_usefully_visible(candidate, best):
            available = best
            rect = fit_rect_to_available(candidate, available, minimum)

    if rect is None:
        rect = _centered_rect(available, preferred, minimum)

    bounded_minimum = QSize(
        min(minimum.width(), max(1, available.width() - 2 * SCREEN_MARGIN)),
        min(minimum.height(), max(1, available.height() - 2 * SCREEN_MARGIN)),
    )
    widget.setMinimumSize(bounded_minimum)
    widget.setGeometry(rect)
    if bool(state.get("maximized", False)):
        widget.setWindowState(widget.windowState() | Qt.WindowMaximized)


def ensure_window_visible(widget: QWidget, minimum: QSize) -> None:
    """Holt ein bereits existierendes Fenster nach Monitor-/Skalierungswechsel zurück."""
    if widget.isMaximized():
        return
    current = widget.geometry()
    available = _best_screen(current, widget)
    if not _is_usefully_visible(current, available):
        current = _centered_rect(available, current.size(), minimum)
    widget.setGeometry(fit_rect_to_available(current, available, minimum))


def save_window_state(widget: QWidget, project_root: Path, key: str) -> bool:
    """Speichert nur Geometrie; ein Fehler darf Schließen oder Nutzerdaten nie blockieren."""
    try:
        states = _load_states(project_root)
        rect = widget.normalGeometry() if widget.isMaximized() else widget.geometry()
        states[key] = {
            "x": int(rect.x()),
            "y": int(rect.y()),
            "width": int(rect.width()),
            "height": int(rect.height()),
            "maximized": bool(widget.isMaximized()),
        }
        atomic_write_json(_state_path(project_root), states)
        return True
    except (OSError, UnicodeError, TypeError, ValueError):
        return False
