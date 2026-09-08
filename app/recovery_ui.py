"""Wiederverwendbare Filter-, Detail- und Zoomlogik für die Recovery-Oberfläche."""

from __future__ import annotations

from typing import Any, Iterable

ZOOM_LEVELS = (100, 125, 150, 175, 200)


def filter_events(events: Iterable[dict[str, Any]], severity: str = "ALLE", area: str = "ALLE") -> list[dict[str, Any]]:
    severity_key = severity.strip().upper() or "ALLE"
    area_key = area.strip().upper() or "ALLE"
    result: list[dict[str, Any]] = []
    for event in events:
        event_severity = str(event.get("severity", "")).upper()
        event_area = str(event.get("area", "")).upper()
        if severity_key != "ALLE" and event_severity != severity_key:
            continue
        if area_key != "ALLE" and event_area != area_key:
            continue
        result.append(event)
    return result


def available_areas(events: Iterable[dict[str, Any]]) -> list[str]:
    return ["ALLE", *sorted({str(event.get("area", "")).upper() for event in events if event.get("area")})]


def zoom_font_size(base_size: int, percent: int) -> int:
    if percent not in ZOOM_LEVELS:
        raise ValueError("Ungültige Zoomstufe")
    return max(8, round(base_size * percent / 100))


def repetition_summary(event: dict[str, Any]) -> tuple[int, str]:
    regression = event.get("regression") or {}
    count = int(regression.get("count") or 1)
    first_seen = str(regression.get("first_seen") or event.get("time") or "Unbekannt")
    return count, first_seen


def technical_details(event: dict[str, Any]) -> str:
    regression = event.get("regression") or {}
    lines = [
        f"Kennung: {event.get('event_id') or 'Keine Angabe'}",
        f"Technischer Grund: {event.get('technical_cause') or 'Keine Angabe'}",
        f"Ausnahmetyp: {event.get('exception_type') or 'Keiner'}",
        f"Signatur: {regression.get('signature') or 'Keine'}",
        f"Spur: {event.get('trace') or 'Keine'}",
    ]
    return "\n".join(lines)
