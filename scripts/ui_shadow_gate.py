#!/usr/bin/env python3
"""Nicht blockierender UI-Qualitätsgate für Provoware.

Der Prozess liefert maschinenlesbare Evidenz, Screenshots nur bei Auffälligkeiten
und einen klaren Exitcode. In Iteration 39 läuft er in GitHub Actions mit
``continue-on-error`` und kann daher noch keinen Release blockieren.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import traceback
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QPoint, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QListWidget,
    QPlainTextEdit,
    QPushButton,
    QTableWidget,
    QTextEdit,
    QToolButton,
    QTreeWidget,
    QWidget,
)

from app.song_editor import SongEditor
from app.song_library import SongLibrary
from app.ui import Dashboard
from app.ui_quality_contracts import (
    BASE_GRID_PX,
    FINE_GRID_PX,
    MIN_CONTROL_HEIGHT_PX,
    RECOMMENDED_CONTROL_HEIGHT_PX,
    RectSpec,
    ViewportSpec,
    contrast_ratio,
    critical_matrix,
    deterministic_window_state_cases,
    evaluate_rect_contract,
    grid_compliance,
    release_matrix,
    validate_matrix,
)
from app.ui_standards import apply_global_style, theme_colors
from app.window_state import fit_rect_to_available


class FakeTexts:
    def get(self, _key: str, default: str = "") -> str:
        return default


class FakeLogger:
    def recent(self, _limit: int = 100) -> list[object]:
        return []

    @staticmethod
    def human_report(event: object) -> str:
        return str(event)


INTERACTIVE_TYPES = (
    QPushButton,
    QToolButton,
    QLineEdit,
    QTextEdit,
    QPlainTextEdit,
    QComboBox,
    QCheckBox,
    QListWidget,
    QTreeWidget,
    QTableWidget,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(text: str) -> str:
    text = text.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9._-]+", "-", text).strip("-") or "ui"


def _rect_of(control: QWidget, window: QWidget) -> QRect:
    top_left = control.mapTo(window, QPoint(0, 0))
    return QRect(top_left, control.size())


def _visible_controls(window: QWidget) -> list[QWidget]:
    controls: list[QWidget] = []
    for kind in INTERACTIVE_TYPES:
        for control in window.findChildren(kind):
            if not control.isVisibleTo(window):
                continue
            if control.width() <= 0 or control.height() <= 0:
                continue
            controls.append(control)
    return list(dict.fromkeys(controls))


def _finding(severity: str, code: str, message: str, *, window: str, case: str, rect: QRect | None = None, control: QWidget | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "severity": severity,
        "code": code,
        "message": message,
        "window": window,
        "case": case,
    }
    if rect is not None:
        result["rect"] = {"x": rect.x(), "y": rect.y(), "width": rect.width(), "height": rect.height()}
    if control is not None:
        result["control_type"] = control.__class__.__name__
        result["object_name"] = control.objectName()
        if isinstance(control, (QPushButton, QToolButton, QCheckBox)):
            result["text"] = control.text()
        elif isinstance(control, QLineEdit):
            result["text"] = control.placeholderText()
    return result


def _scan_window(window: QWidget, spec: ViewportSpec) -> tuple[list[dict[str, object]], dict[str, object]]:
    case = spec.key
    name = window.__class__.__name__
    findings: list[dict[str, object]] = []
    controls = _visible_controls(window)
    window_bounds = QRect(0, 0, window.width(), window.height())
    grid_values: list[int] = []

    if window.width() > spec.width or window.height() > spec.height:
        findings.append(_finding(
            "error", "UI-WINDOW-OVERSIZE",
            f"{name} überschreitet die simulierte Arbeitsfläche {spec.width}×{spec.height}.",
            window=name, case=case, rect=window.geometry(),
        ))

    for control in controls:
        rect = _rect_of(control, window)
        grid_values.extend((rect.x(), rect.y(), rect.width(), rect.height()))
        intersection = rect.intersected(window_bounds)
        if intersection.isEmpty():
            findings.append(_finding(
                "error", "UI-CONTROL-OFFSCREEN",
                "Ein sichtbares Bedienelement liegt vollständig außerhalb des Fensters.",
                window=name, case=case, rect=rect, control=control,
            ))
        elif intersection.width() < rect.width() or intersection.height() < rect.height():
            findings.append(_finding(
                "warning", "UI-CONTROL-CLIPPED",
                "Ein sichtbares Bedienelement wird am Fensterrand teilweise abgeschnitten.",
                window=name, case=case, rect=rect, control=control,
            ))

        if isinstance(control, (QPushButton, QToolButton, QLineEdit, QComboBox, QCheckBox)):
            if control.height() < MIN_CONTROL_HEIGHT_PX:
                findings.append(_finding(
                    "error", "UI-CONTROL-HEIGHT-HARD",
                    f"Bedienelement ist niedriger als {MIN_CONTROL_HEIGHT_PX}px.",
                    window=name, case=case, rect=rect, control=control,
                ))
            elif control.height() < RECOMMENDED_CONTROL_HEIGHT_PX:
                findings.append(_finding(
                    "info", "UI-CONTROL-HEIGHT-TARGET",
                    f"Bedienelement liegt unter dem Zielwert {RECOMMENDED_CONTROL_HEIGHT_PX}px.",
                    window=name, case=case, rect=rect, control=control,
                ))

        if not control.accessibleName().strip():
            findings.append(_finding(
                "warning", "UI-ACCESSIBLE-NAME",
                "Sichtbares interaktives Element hat keinen Screenreader-Namen.",
                window=name, case=case, rect=rect, control=control,
            ))

        if isinstance(control, (QPushButton, QToolButton)):
            text = " ".join(control.text().replace("&&", "&").split())
            if text and "\n" not in control.text():
                needed = control.fontMetrics().horizontalAdvance(text) + 20
                if needed > max(1, control.width()):
                    findings.append(_finding(
                        "warning", "UI-BUTTON-TEXT-CLIPPED",
                        "Buttontext benötigt voraussichtlich mehr Breite als verfügbar.",
                        window=name, case=case, rect=rect, control=control,
                    ))

    # Überlappungen nur zwischen echten Geschwistern prüfen. Das vermeidet
    # Fehlalarme durch Scroll-Viewports und intern zusammengesetzte Qt-Controls.
    by_parent: dict[int, list[QWidget]] = {}
    for control in controls:
        parent = control.parentWidget()
        if parent is not None:
            by_parent.setdefault(id(parent), []).append(control)
    for siblings in by_parent.values():
        for index, first in enumerate(siblings):
            first_rect = first.geometry()
            for second in siblings[index + 1:]:
                second_rect = second.geometry()
                overlap = first_rect.intersected(second_rect)
                if overlap.width() > 2 and overlap.height() > 2:
                    findings.append(_finding(
                        "error", "UI-SIBLING-OVERLAP",
                        f"Zwei interaktive Geschwisterelemente überlappen sich ({first.__class__.__name__}/{second.__class__.__name__}).",
                        window=name, case=case, rect=_rect_of(first, window), control=first,
                    ))

    compliance = grid_compliance(grid_values)
    if compliance < 0.70:
        findings.append(_finding(
            "info", "UI-GRID-COMPLIANCE",
            f"Nur {compliance:.0%} der gemessenen Geometriewerte liegen auf dem {FINE_GRID_PX}px-Feinraster (±1px).",
            window=name, case=case,
        ))

    metrics = {
        "window": name,
        "case": case,
        "width": window.width(),
        "height": window.height(),
        "visible_controls": len(controls),
        "grid_compliance": round(compliance, 4),
    }
    return findings, metrics


def _save_debug_image(window: QWidget, findings: list[dict[str, object]], destination: Path) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    pixmap = window.grab()
    if pixmap.isNull():
        return False
    painter = QPainter(pixmap)
    try:
        grid_pen = QPen(QColor(255, 255, 255, 42))
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)
        for x in range(0, pixmap.width(), BASE_GRID_PX):
            painter.drawLine(x, 0, x, pixmap.height())
        for y in range(0, pixmap.height(), BASE_GRID_PX):
            painter.drawLine(0, y, pixmap.width(), y)
        issue_pen = QPen(QColor(255, 70, 85, 220))
        issue_pen.setWidth(3)
        painter.setPen(issue_pen)
        for finding in findings:
            rect = finding.get("rect")
            if isinstance(rect, dict):
                painter.drawRect(
                    int(rect.get("x", 0)), int(rect.get("y", 0)),
                    max(1, int(rect.get("width", 1))), max(1, int(rect.get("height", 1))),
                )
    finally:
        painter.end()
    return pixmap.save(str(destination), "PNG")


def _apply_case(window: QWidget, spec: ViewportSpec) -> None:
    setattr(window, "zoom_percent", spec.zoom)
    set_zoom = getattr(window, "set_zoom", None)
    if callable(set_zoom):
        set_zoom(spec.zoom)
    apply_global_style(window, spec.zoom, spec.theme)
    target_width = max(window.minimumWidth(), spec.width - 32)
    target_height = max(window.minimumHeight(), spec.height - 72)
    window.resize(target_width, target_height)
    window.show()
    QApplication.processEvents()


def _close_window(window: QWidget) -> None:
    if isinstance(window, (SongEditor, Dashboard)):
        setattr(window, "_closing_after_save", True)
    window.close()
    QApplication.processEvents()


def _core_factories(root: Path, zoom: int) -> tuple[Callable[[], QWidget], ...]:
    return (
        lambda: Dashboard(FakeTexts(), FakeLogger(), root),
        lambda: SongLibrary(root, zoom, lambda _path: None),
        lambda: SongEditor(root, zoom_percent=zoom),
    )


def _contrast_findings() -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for theme in ("Amber", "Türkis", "Lila", "Kontrast"):
        colors = theme_colors(theme)
        pairs = (
            ("text/background", colors["text"], colors["background"]),
            ("muted/background", colors["muted"], colors["background"]),
            ("placeholder/input_bg", colors["placeholder"], colors["input_bg"]),
            ("accent/background", colors["accent"], colors["background"]),
        )
        for label, foreground, background in pairs:
            ratio = contrast_ratio(foreground, background)
            if ratio < 4.5:
                findings.append({
                    "severity": "error",
                    "code": "UI-CONTRAST-CORE",
                    "message": f"{theme} {label} erreicht nur {ratio:.2f}:1 statt 4.5:1.",
                    "window": "Theme",
                    "case": theme,
                    "ratio": round(ratio, 3),
                })
    return findings


def _window_state_fuzz(matrix: tuple[ViewportSpec, ...]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    # Drei repräsentative Flächen reichen für den geometrischen Fuzzer; die
    # vollständige UI-Matrix wird separat geprüft.
    unique_sizes: list[tuple[int, int]] = []
    for spec in matrix:
        size = (spec.width, spec.height)
        if size not in unique_sizes:
            unique_sizes.append(size)
    for width, height in unique_sizes:
        available = QRect(0, 0, width, height - 40)
        available_spec = RectSpec(0, 0, width, height - 40)
        for index, case in enumerate(deterministic_window_state_cases(), start=1):
            for name, minimum in (("SongEditor", QSize(760, 560)), ("SongLibrary", QSize(760, 520))):
                result = fit_rect_to_available(
                    QRect(case.x, case.y, case.width, case.height), available, minimum,
                )
                result_spec = RectSpec(result.x(), result.y(), result.width(), result.height())
                contract = evaluate_rect_contract(
                    result_spec,
                    available_spec,
                    minimum_width=minimum.width(),
                    minimum_height=minimum.height(),
                )
                for item in contract:
                    findings.append({
                        "severity": item.severity,
                        "code": item.code,
                        "message": item.message,
                        "window": name,
                        "case": f"fuzz-{width}x{height}-{index}",
                        "source_rect": asdict(case),
                        "result_rect": asdict(result_spec),
                    })
    return findings


def _write_summary(path: Path, payload: dict[str, object]) -> None:
    summary = payload["summary"]
    lines = [
        "# Provoware UI-Shadow-Gate",
        "",
        f"- Profil: **{payload['profile']}**",
        f"- Commit: `{payload['git_sha']}`",
        f"- Matrixfälle: **{summary['matrix_cases']}**",
        f"- geprüfte Fensterinstanzen: **{summary['window_instances']}**",
        f"- Fehler: **{summary['errors']}**",
        f"- Warnungen: **{summary['warnings']}**",
        f"- Hinweise: **{summary['info']}**",
        f"- Status: **{summary['status']}**",
        "",
        "Shadow-Modus: Auffälligkeiten werden dokumentiert, blockieren Iteration 39 aber noch nicht den Release.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(profile: str, output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = _utc_now()
    matrix = critical_matrix() if profile == "pr" else release_matrix()
    matrix_errors = validate_matrix(matrix)
    if matrix_errors:
        raise RuntimeError("; ".join(matrix_errors))

    app = QApplication.instance() or QApplication([])
    findings: list[dict[str, object]] = []
    metrics: list[dict[str, object]] = []
    window_instances = 0
    findings.extend(_contrast_findings())
    findings.extend(_window_state_fuzz(matrix))

    with tempfile.TemporaryDirectory(prefix="provoware-ui-shadow-") as tmp:
        root = Path(tmp)
        for spec in matrix:
            for factory in _core_factories(root, spec.zoom):
                window = factory()
                try:
                    _apply_case(window, spec)
                    current, current_metrics = _scan_window(window, spec)
                    findings.extend(current)
                    metrics.append(current_metrics)
                    window_instances += 1
                    if any(item["severity"] in {"error", "warning"} for item in current):
                        image = output_dir / "screenshots" / f"{spec.key}_{_slug(window.__class__.__name__)}.png"
                        _save_debug_image(window, current, image)
                finally:
                    _close_window(window)

    counts = {
        severity: sum(1 for item in findings if item.get("severity") == severity)
        for severity in ("error", "warning", "info")
    }
    status = "red" if counts["error"] else "yellow" if counts["warning"] else "green"
    payload: dict[str, object] = {
        "schema_version": 1,
        "mode": "shadow",
        "profile": profile,
        "git_sha": os.environ.get("GITHUB_SHA", "local"),
        "run_number": os.environ.get("GITHUB_RUN_NUMBER", "local"),
        "started_utc": started,
        "finished_utc": _utc_now(),
        "contracts": {
            "base_grid_px": BASE_GRID_PX,
            "fine_grid_px": FINE_GRID_PX,
            "minimum_control_height_px": MIN_CONTROL_HEIGHT_PX,
            "recommended_control_height_px": RECOMMENDED_CONTROL_HEIGHT_PX,
        },
        "summary": {
            "status": status,
            "matrix_cases": len(matrix),
            "window_instances": window_instances,
            "errors": counts["error"],
            "warnings": counts["warning"],
            "info": counts["info"],
            "blocking": False,
            "promotion_candidate": counts["error"] == 0 and counts["warning"] == 0,
        },
        "matrix": [asdict(case) | {"key": case.key} for case in matrix],
        "metrics": metrics,
        "findings": findings,
    }
    evidence = output_dir / "ui_shadow_evidence.json"
    evidence.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    markdown = output_dir / "ui_shadow_summary.md"
    _write_summary(markdown, payload)

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as handle:
            handle.write(markdown.read_text(encoding="utf-8"))

    print(json.dumps(payload["summary"], ensure_ascii=False, sort_keys=True))
    return 1 if counts["error"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Provoware UI-Qualitätsgate im Shadow-Modus")
    parser.add_argument("--profile", choices=("pr", "release"), default="pr")
    parser.add_argument("--output-dir", type=Path, default=Path("berichte/ui-shadow"))
    args = parser.parse_args()
    try:
        return run(args.profile, args.output_dir)
    except Exception as exc:  # Infrastrukturfehler müssen ebenfalls Evidenz erzeugen.
        args.output_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 1,
            "mode": "shadow",
            "profile": args.profile,
            "git_sha": os.environ.get("GITHUB_SHA", "local"),
            "started_utc": _utc_now(),
            "finished_utc": _utc_now(),
            "summary": {
                "status": "infrastructure-error",
                "errors": 0,
                "warnings": 0,
                "info": 0,
                "infrastructure_errors": 1,
                "blocking": False,
                "promotion_candidate": False,
            },
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
        (args.output_dir / "ui_shadow_evidence.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"UI-Shadow-Gate Infrastrukturfehler: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
