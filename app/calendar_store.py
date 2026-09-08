"""Atomarer Kalenderbestand und berechenbare Termin-/Erinnerungslogik."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from app.atomic_io import atomic_write_json

SCHEMA_VERSION = 1
REMINDER_OPTIONS = (None, 0, 5, 15, 30, 60, 1440)


def store_path(root: Path) -> Path:
    return root / "daten" / "kalender" / "termine.json"


def empty_state() -> dict[str, object]:
    return {"schema_version": SCHEMA_VERSION, "events": []}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _clean_text(value: object, *, required: bool = False, field: str = "Text") -> str:
    cleaned = " ".join(str(value or "").strip().split())
    if required and not cleaned:
        raise ValueError(f"{field} darf nicht leer sein.")
    return cleaned


def _local_datetime(value: object, *, field: str) -> datetime:
    text = str(value or "").strip()
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as error:
        raise ValueError(f"{field} hat kein gültiges Datum/Zeit-Format.") from error
    if parsed.tzinfo is not None:
        raise ValueError(f"{field} muss lokale Datum/Zeit ohne Zeitzone enthalten.")
    return parsed.replace(second=0, microsecond=0)


def _validate_timestamp(value: object, *, field: str, optional: bool = False) -> str | None:
    if optional and value in (None, ""):
        return None
    text = _clean_text(value, required=True, field=field)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{field} ist beschädigt.") from error
    return text


def _validate_reminder(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("Erinnerungsabstand ist ungültig.")
    try:
        minutes = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError("Erinnerungsabstand ist ungültig.") from error
    if minutes not in {item for item in REMINDER_OPTIONS if item is not None}:
        raise ValueError("Erinnerungsabstand wird nicht unterstützt.")
    return minutes


def _validate_event(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("Kalendereintrag ist beschädigt.")
    event_id = _clean_text(raw.get("id"), required=True, field="Termin-ID")
    title = _clean_text(raw.get("title"), required=True, field="Titel")
    note = str(raw.get("note") or "").strip()
    start = _local_datetime(raw.get("start"), field="Start")
    end = _local_datetime(raw.get("end"), field="Ende")
    if end <= start:
        raise ValueError("Das Ende muss nach dem Start liegen.")
    reminder = _validate_reminder(raw.get("reminder_minutes"))
    created_at = _validate_timestamp(raw.get("created_at"), field="Erstellzeit")
    reminded_at = _validate_timestamp(raw.get("reminded_at"), field="Erinnerungszeit", optional=True)
    return {
        "id": event_id,
        "title": title,
        "note": note,
        "start": start.isoformat(timespec="minutes"),
        "end": end.isoformat(timespec="minutes"),
        "reminder_minutes": reminder,
        "created_at": created_at,
        "reminded_at": reminded_at,
    }


def validate_state(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("Kalenderdatei muss ein JSON-Objekt enthalten.")
    schema = raw.get("schema_version", SCHEMA_VERSION)
    if schema != SCHEMA_VERSION:
        raise ValueError(f"Unbekannte Kalender-Datenversion: {schema}")
    raw_events = raw.get("events", [])
    if not isinstance(raw_events, list):
        raise ValueError("Kalenderdatei enthält keine gültige Terminliste.")
    events = [_validate_event(item) for item in raw_events]
    ids = [str(event["id"]) for event in events]
    if len(ids) != len(set(ids)):
        raise ValueError("Kalenderdatei enthält doppelte Termin-IDs.")
    return {"schema_version": SCHEMA_VERSION, "events": events}


def load_state(root: Path) -> dict[str, object]:
    target = store_path(root)
    if not target.exists():
        return empty_state()
    return validate_state(json.loads(target.read_text(encoding="utf-8")))


def save_state(root: Path, state: dict[str, object]) -> Path:
    clean = validate_state(state)
    return atomic_write_json(store_path(root), clean)


def add_event(root: Path, title: str, start: str, end: str, note: str = "",
              reminder_minutes: int | None = None) -> dict[str, object]:
    start_dt = _local_datetime(start, field="Start")
    end_dt = _local_datetime(end, field="Ende")
    if end_dt <= start_dt:
        raise ValueError("Das Ende muss nach dem Start liegen.")
    event = {
        "id": uuid4().hex,
        "title": _clean_text(title, required=True, field="Titel"),
        "note": str(note or "").strip(),
        "start": start_dt.isoformat(timespec="minutes"),
        "end": end_dt.isoformat(timespec="minutes"),
        "reminder_minutes": _validate_reminder(reminder_minutes),
        "created_at": _utc_now(),
        "reminded_at": None,
    }
    state = load_state(root)
    events = list(state["events"])
    events.append(event)
    state["events"] = events
    save_state(root, state)
    return deepcopy(event)


def all_events(root: Path) -> list[dict[str, object]]:
    events = list(load_state(root)["events"])
    return sorted(events, key=lambda event: (str(event["start"]), str(event["title"]).casefold()))


def events_between(root: Path, range_start: datetime, range_end: datetime) -> list[dict[str, object]]:
    if range_start.tzinfo is not None or range_end.tzinfo is not None:
        raise ValueError("Ansichtsbereiche müssen lokale Datum/Zeit ohne Zeitzone verwenden.")
    if range_end <= range_start:
        raise ValueError("Ansichtsende muss nach dem Anfang liegen.")
    result = []
    for event in all_events(root):
        start = datetime.fromisoformat(str(event["start"]))
        end = datetime.fromisoformat(str(event["end"]))
        if start < range_end and end > range_start:
            result.append(event)
    return result


def day_range(selected: date) -> tuple[datetime, datetime]:
    start = datetime.combine(selected, time.min)
    return start, start + timedelta(days=1)


def week_range(selected: date) -> tuple[datetime, datetime]:
    monday = selected - timedelta(days=selected.weekday())
    start = datetime.combine(monday, time.min)
    return start, start + timedelta(days=7)


def month_range(selected: date) -> tuple[datetime, datetime]:
    start = datetime(selected.year, selected.month, 1)
    if selected.month == 12:
        end = datetime(selected.year + 1, 1, 1)
    else:
        end = datetime(selected.year, selected.month + 1, 1)
    return start, end


def year_range(selected: date) -> tuple[datetime, datetime]:
    return datetime(selected.year, 1, 1), datetime(selected.year + 1, 1, 1)


def due_reminders(root: Path, now: datetime | None = None) -> list[dict[str, object]]:
    now = now or datetime.now()
    if now.tzinfo is not None:
        raise ValueError("Erinnerungsprüfung erwartet lokale Datum/Zeit ohne Zeitzone.")
    due: list[dict[str, object]] = []
    for event in all_events(root):
        reminder = event["reminder_minutes"]
        if reminder is None or event["reminded_at"]:
            continue
        start = datetime.fromisoformat(str(event["start"]))
        end = datetime.fromisoformat(str(event["end"]))
        reminder_at = start - timedelta(minutes=int(reminder))
        if reminder_at <= now <= end:
            due.append(event)
    return due


def mark_reminded(root: Path, event_id: str, at: str | None = None) -> None:
    state = load_state(root)
    events = list(state["events"])
    for event in events:
        if event["id"] == event_id:
            if event["reminded_at"]:
                return
            event["reminded_at"] = at or _utc_now()
            state["events"] = events
            save_state(root, state)
            return
    raise ValueError("Termin für Erinnerungsmarkierung wurde nicht gefunden.")
