"""Maschinenlesbare UI-Verträge für die automatische Provoware-Oberflächenabnahme.

Das Modul ist bewusst Qt-unabhängig. Dadurch können Raster-, Geometrie-,
Kontrast- und Gate-Regeln auch dann geprüft werden, wenn keine grafische
Sitzung verfügbar ist. Die eigentliche QWidget-Prüfung lebt im separaten
Shadow-Gate unter ``scripts/ui_shadow_gate.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import isfinite
from typing import Iterable, Mapping, Sequence

BASE_GRID_PX = 8
FINE_GRID_PX = 4
GRID_TOLERANCE_PX = 1
WORKAREA_MARGIN_PX = 16
MIN_VISIBLE_WIDTH_PX = 180
MIN_VISIBLE_HEIGHT_PX = 120
MIN_CONTROL_HEIGHT_PX = 27
RECOMMENDED_CONTROL_HEIGHT_PX = 32
MIN_NORMAL_CONTRAST = 4.5
MIN_LARGE_TEXT_CONTRAST = 3.0

SUPPORTED_THEMES = ("Amber", "Türkis", "Lila", "Kontrast")
SUPPORTED_ZOOMS = (100, 125, 150, 175, 200)
SUPPORTED_VIEWPORTS = ((1366, 768), (1600, 900), (1920, 1080))


@dataclass(frozen=True, slots=True)
class ViewportSpec:
    width: int
    height: int
    zoom: int
    theme: str

    @property
    def key(self) -> str:
        safe_theme = self.theme.lower().replace("ü", "ue").replace("ä", "ae").replace("ö", "oe")
        return f"{self.width}x{self.height}_z{self.zoom}_{safe_theme}"


@dataclass(frozen=True, slots=True)
class RectSpec:
    x: int
    y: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height


@dataclass(frozen=True, slots=True)
class ContractFinding:
    severity: str
    code: str
    message: str
    context: Mapping[str, object] | None = None


@dataclass(frozen=True, slots=True)
class PromotionDecision:
    ready: bool
    reasons: tuple[str, ...]


def critical_matrix() -> tuple[ViewportSpec, ...]:
    """Kleine, absichtlich harte Matrix für normale Pull-Request-Läufe."""
    return (
        ViewportSpec(1366, 768, 100, "Amber"),
        ViewportSpec(1366, 768, 150, "Amber"),
        ViewportSpec(1366, 768, 175, "Türkis"),
        ViewportSpec(1366, 768, 200, "Kontrast"),
        ViewportSpec(1600, 900, 125, "Türkis"),
        ViewportSpec(1600, 900, 175, "Lila"),
        ViewportSpec(1920, 1080, 100, "Amber"),
        ViewportSpec(1920, 1080, 200, "Kontrast"),
    )


def release_matrix() -> tuple[ViewportSpec, ...]:
    """Vollständige Release-Matrix: 3 Größen × 5 Zoomstufen × 4 Themes = 60."""
    return tuple(
        ViewportSpec(width, height, zoom, theme)
        for (width, height), zoom, theme in product(SUPPORTED_VIEWPORTS, SUPPORTED_ZOOMS, SUPPORTED_THEMES)
    )


def validate_matrix(matrix: Sequence[ViewportSpec]) -> tuple[str, ...]:
    errors: list[str] = []
    seen: set[str] = set()
    for case in matrix:
        if case.key in seen:
            errors.append(f"Doppelter Matrixfall: {case.key}")
        seen.add(case.key)
        if case.width < 800 or case.height < 600:
            errors.append(f"Unrealistisch kleine Testfläche: {case.key}")
        if case.zoom not in SUPPORTED_ZOOMS:
            errors.append(f"Nicht freigegebener Zoom: {case.key}")
        if case.theme not in SUPPORTED_THEMES:
            errors.append(f"Nicht freigegebenes Theme: {case.key}")
    return tuple(errors)


def _hex_rgb(value: str) -> tuple[float, float, float]:
    text = value.strip()
    if len(text) != 7 or not text.startswith("#"):
        raise ValueError(f"Ungültige Hex-Farbe: {value!r}")
    try:
        return tuple(int(text[index:index + 2], 16) / 255.0 for index in (1, 3, 5))  # type: ignore[return-value]
    except ValueError as exc:
        raise ValueError(f"Ungültige Hex-Farbe: {value!r}") from exc


def _relative_luminance(value: str) -> float:
    channels: list[float] = []
    for channel in _hex_rgb(value):
        channels.append(channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(first: str, second: str) -> float:
    high, low = sorted((_relative_luminance(first), _relative_luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def grid_distance(value: int, grid: int = FINE_GRID_PX) -> int:
    """Kleinster Pixelabstand eines Werts zum gewählten Raster."""
    if grid <= 0:
        raise ValueError("Raster muss größer als 0 sein")
    remainder = abs(value) % grid
    return min(remainder, grid - remainder)


def grid_compliance(values: Iterable[int], grid: int = FINE_GRID_PX, tolerance: int = GRID_TOLERANCE_PX) -> float:
    values = tuple(values)
    if not values:
        return 1.0
    matches = sum(grid_distance(value, grid) <= tolerance for value in values)
    return matches / len(values)


def intersection_area(first: RectSpec, second: RectSpec) -> int:
    width = max(0, min(first.right, second.right) - max(first.x, second.x))
    height = max(0, min(first.bottom, second.bottom) - max(first.y, second.y))
    return width * height


def rect_is_inside(rect: RectSpec, available: RectSpec, margin: int = 0) -> bool:
    return (
        rect.width >= 0
        and rect.height >= 0
        and rect.x >= available.x + margin
        and rect.y >= available.y + margin
        and rect.right <= available.right - margin
        and rect.bottom <= available.bottom - margin
    )


def evaluate_rect_contract(
    rect: RectSpec,
    available: RectSpec,
    *,
    minimum_width: int,
    minimum_height: int,
    margin: int = WORKAREA_MARGIN_PX,
) -> tuple[ContractFinding, ...]:
    findings: list[ContractFinding] = []
    if rect.width < minimum_width or rect.height < minimum_height:
        findings.append(ContractFinding(
            "error",
            "UI-GEOMETRY-MINIMUM",
            "Fenster unterschreitet seine sichere Mindestgröße.",
            {"rect": rect, "minimum": (minimum_width, minimum_height)},
        ))
    if not rect_is_inside(rect, available, margin):
        findings.append(ContractFinding(
            "error",
            "UI-GEOMETRY-WORKAREA",
            "Fenster liegt nicht vollständig innerhalb der verfügbaren Arbeitsfläche.",
            {"rect": rect, "available": available, "margin": margin},
        ))
    return tuple(findings)


def deterministic_window_state_cases() -> tuple[RectSpec, ...]:
    """Deterministische Problemfälle für Monitorwechsel, Skalierung und beschädigte Zustände."""
    return (
        RectSpec(-2400, -900, 1600, 1000),
        RectSpec(-1800, 40, 1180, 720),
        RectSpec(2500, 120, 1180, 720),
        RectSpec(40, 1900, 1180, 720),
        RectSpec(-20, -20, 900, 600),
        RectSpec(0, 0, 3000, 2000),
        RectSpec(10, 10, 760, 560),
        RectSpec(300, 180, 900, 600),
        RectSpec(1200, 600, 900, 600),
        RectSpec(-1, 220, 1366, 728),
        RectSpec(4000, -2000, 760, 560),
        RectSpec(-4000, 2000, 1180, 720),
    )


def promotion_decision(history: Sequence[Mapping[str, object]], minimum_runs: int = 3) -> PromotionDecision:
    """Entscheidet reproduzierbar, ob der Shadow-Gate zum Pflicht-Gate reif ist.

    Erwartete Run-Felder: ``errors``, ``infrastructure_errors``,
    ``false_positives`` und ``injected_detection_rate``.
    """
    reasons: list[str] = []
    if len(history) < minimum_runs:
        reasons.append(f"Erst {len(history)} von {minimum_runs} benötigten stabilen Läufen vorhanden.")
    for index, run in enumerate(history, start=1):
        errors = int(run.get("errors", 0) or 0)
        infra = int(run.get("infrastructure_errors", 0) or 0)
        false_positives = int(run.get("false_positives", 0) or 0)
        rate = float(run.get("injected_detection_rate", 0.0) or 0.0)
        if not isfinite(rate):
            rate = 0.0
        if errors:
            reasons.append(f"Lauf {index}: {errors} ungeklärte Qualitätsfehler.")
        if infra:
            reasons.append(f"Lauf {index}: {infra} Infrastrukturfehler.")
        if false_positives:
            reasons.append(f"Lauf {index}: {false_positives} bestätigte Fehlalarme.")
        if rate < 1.0:
            reasons.append(f"Lauf {index}: absichtlich eingebaute Fehler nur zu {rate:.0%} erkannt.")
    return PromotionDecision(not reasons, tuple(reasons))
