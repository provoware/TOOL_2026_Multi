"""Konservativer, automatisch prüfbarer Barrierefreiheits-Vertrag.

Automatische Prüfungen ersetzen weder Screenreader- noch reale Tastaturabnahme.
Die Prüfmatrix enthält ausdrücklich auch die manuell zu prüfenden Aspekte.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.ui_quality_contracts import (
    MIN_LARGE_TEXT_CONTRAST, MIN_NORMAL_CONTRAST,
    SUPPORTED_THEMES, SUPPORTED_ZOOMS, contrast_ratio,
)

MODULES = (
    "Dashboard", "SongEditor", "TextEditorWindow", "SongLibrary",
    "CalendarWindow", "TodoWindow", "CharacterWindow", "ProfileEditor",
)
DIMENSIONS = (
    "tastatur", "fokus", "beschriftung", "kontrast", "zoom",
    "bildschirmleser_praxis", "speichern_abbrechen_wiederherstellen",
)
PRACTICAL_CHECKS = frozenset(("bildschirmleser_praxis",))


@dataclass(frozen=True)
class AccessibilityCase:
    module: str
    dimension: str
    automatic: bool


def accessibility_matrix() -> tuple[AccessibilityCase, ...]:
    return tuple(
        AccessibilityCase(module, dimension, dimension not in PRACTICAL_CHECKS)
        for module in MODULES for dimension in DIMENSIONS
    )


def contrast_ok(foreground: str, background: str, *, large: bool = False) -> bool:
    target = MIN_LARGE_TEXT_CONTRAST if large else MIN_NORMAL_CONTRAST
    return contrast_ratio(foreground, background) >= target


def validate_accessibility_matrix() -> tuple[str, ...]:
    cases = accessibility_matrix()
    issues = []
    if len(cases) != len(MODULES) * len(DIMENSIONS):
        issues.append("Prüfmatrix ist unvollständig.")
    if len({(c.module, c.dimension) for c in cases}) != len(cases):
        issues.append("Prüfmatrix enthält doppelte Kombinationen.")
    if not set(SUPPORTED_ZOOMS).issuperset({100, 200}):
        issues.append("Zoom 100 und 200 Prozent fehlen.")
    if not set(SUPPORTED_THEMES).issuperset({"Amber", "Kontrast"}):
        issues.append("Basis- oder Kontrast-Theme fehlt.")
    if any(c.automatic for c in cases if c.dimension in PRACTICAL_CHECKS):
        issues.append("Praxisprüfung wird fälschlich als automatisch bezeichnet.")
    return tuple(issues)
