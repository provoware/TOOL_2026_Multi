"""Deterministische Präsentationsregeln für Dashboard, Laptopmodus und Navigation.

Dieses Modul enthält bewusst keine Qt-Logik. Die Entscheidung, ob eine Ansicht
als Laptop-, Groß- oder Hochzoomzustand gilt, ist dadurch unabhängig von der
Ereignisreihenfolge der Oberfläche und separat testbar.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


MIN_ZOOM_PERCENT = 100
MAX_ZOOM_PERCENT = 200
LAPTOP_ZOOM_MIN_PERCENT = 125
HIGH_ZOOM_MIN_PERCENT = 175
WIDE_MIN_WIDTH_PX = 1450
LAPTOP_HEIGHT_LIMIT_PX = 820
LAPTOP_EFFECTIVE_HEIGHT_LIMIT_PX = 700


class WindowMetrics(Protocol):
    """Kleinster benötigter Vertrag für eine Fensterklassifikation."""

    zoom_percent: int

    def width(self) -> int: ...
    def height(self) -> int: ...
    def minimumWidth(self) -> int: ...
    def minimumHeight(self) -> int: ...


@dataclass(frozen=True, slots=True)
class PresentationState:
    """Unveränderlicher, aus Messwerten abgeleiteter Darstellungszustand."""

    width_px: int
    height_px: int
    zoom_percent: int
    wide: bool
    high_zoom: bool
    laptop_compact: bool

    @property
    def restricted_navigation(self) -> bool:
        """Geplante Zusatznavigation wird bei knapper Fläche nicht angeboten."""
        return self.high_zoom or self.laptop_compact


def normalize_zoom(value: object) -> int:
    """Normalisiert beliebige Zoomwerte auf den unterstützten Bereich."""
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = MIN_ZOOM_PERCENT
    return max(MIN_ZOOM_PERCENT, min(MAX_ZOOM_PERCENT, parsed))


def classify_presentation(
    *,
    width_px: int,
    height_px: int,
    minimum_width_px: int = 0,
    minimum_height_px: int = 0,
    zoom_percent: object = MIN_ZOOM_PERCENT,
    dashboard: bool = True,
) -> PresentationState:
    """Leitet den Darstellungsmodus ausschließlich aus stabilen Messwerten ab."""
    width = max(int(width_px), int(minimum_width_px), 0)
    height = max(int(height_px), int(minimum_height_px), 0)
    zoom = normalize_zoom(zoom_percent)
    wide = width >= WIDE_MIN_WIDTH_PX
    high_zoom = zoom >= HIGH_ZOOM_MIN_PERCENT

    laptop_compact = False
    if dashboard and not wide and LAPTOP_ZOOM_MIN_PERCENT <= zoom < HIGH_ZOOM_MIN_PERCENT:
        effective_height = height * 100 / zoom if zoom else float(height)
        laptop_compact = (
            height < LAPTOP_HEIGHT_LIMIT_PX
            or effective_height < LAPTOP_EFFECTIVE_HEIGHT_LIMIT_PX
        )

    return PresentationState(
        width_px=width,
        height_px=height,
        zoom_percent=zoom,
        wide=wide,
        high_zoom=high_zoom,
        laptop_compact=laptop_compact,
    )


def presentation_state(window: WindowMetrics) -> PresentationState:
    """Adapter von einem Qt-artigen Fenster auf die reine Präsentationspolicy."""
    return classify_presentation(
        width_px=window.width(),
        height_px=window.height(),
        minimum_width_px=window.minimumWidth(),
        minimum_height_px=window.minimumHeight(),
        zoom_percent=getattr(window, "zoom_percent", MIN_ZOOM_PERCENT),
        dashboard=window.__class__.__name__ == "Dashboard",
    )
