"""Atomarer Todo-Bestand mit aktivem Bereich und Archiv."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

SCHEMA_VERSION = 1


def store_path(root: Path) -> Path:
    return root / "daten" / "todo" / "todo.json"


def empty_state() -> dict[str, object]:
    return {"schema_version": SCHEMA_VERSION, "active": [], "archive": []}


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _clean_text(value: object, *, required: bool = False, field: str = "Text") -> str:
    cleaned = " ".join(str(value or "").strip().split())
    if required and not cleaned:
        raise ValueError(f"{field} darf nicht leer sein.")
    return cleaned


def _validate_due(value: object) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    try:
        datetime.fromisoformat(text)
    except ValueError as error:
        raise ValueError("Termin hat kein gültiges Datum/Zeit-Format.") from error
    return text


def _validate_task(raw: object, *, archived: bool) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("Todo-Eintrag ist beschädigt.")
    task_id = _clean_text(raw.get("id"), required=True, field="Todo-ID")
    title = _clean_text(raw.get("title"), required=True, field="Titel")
    note = str(raw.get("note") or "").strip()
    created_at = _clean_text(raw.get("created_at"), required=True, field="Erstellzeit")
    try:
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("Erstellzeit eines Todos ist beschädigt.") from error
    completed_at = raw.get("completed_at")
    if archived:
        completed_at = _clean_text(completed_at, required=True, field="Abschlusszeit")
        try:
            datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("Abschlusszeit eines Todos ist beschädigt.") from error
    else:
        completed_at = None
    return {
        "id": task_id,
        "title": title,
        "note": note,
        "due": _validate_due(raw.get("due")),
        "created_at": created_at,
        "completed_at": completed_at,
    }


def validate_state(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("Todo-Datei muss ein JSON-Objekt enthalten.")
    schema = raw.get("schema_version", SCHEMA_VERSION)
    if schema != SCHEMA_VERSION:
        raise ValueError(f"Unbekannte Todo-Datenversion: {schema}")
    active_raw = raw.get("active", [])
    archive_raw = raw.get("archive", [])
    if not isinstance(active_raw, list) or not isinstance(archive_raw, list):
        raise ValueError("Todo-Datei enthält ungültige Listen.")
    active = [_validate_task(item, archived=False) for item in active_raw]
    archive = [_validate_task(item, archived=True) for item in archive_raw]
    ids = [str(item["id"]) for item in [*active, *archive]]
    if len(ids) != len(set(ids)):
        raise ValueError("Todo-Datei enthält doppelte IDs.")
    return {"schema_version": SCHEMA_VERSION, "active": active, "archive": archive}


def load_state(root: Path) -> dict[str, object]:
    target = store_path(root)
    if not target.exists():
        return empty_state()
    return validate_state(json.loads(target.read_text(encoding="utf-8")))


def save_state(root: Path, state: dict[str, object]) -> Path:
    clean = validate_state(state)
    target = store_path(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(clean, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink(missing_ok=True)
    return target


def add_task(root: Path, title: str, note: str = "", due: str | None = None) -> dict[str, object]:
    state = load_state(root)
    task = {
        "id": uuid4().hex,
        "title": _clean_text(title, required=True, field="Titel"),
        "note": str(note or "").strip(),
        "due": _validate_due(due),
        "created_at": _now_utc(),
        "completed_at": None,
    }
    active = list(state["active"])
    active.append(task)
    state["active"] = active
    save_state(root, state)
    return deepcopy(task)


def complete_task(root: Path, task_id: str) -> dict[str, object]:
    state = load_state(root)
    active = list(state["active"])
    archive = list(state["archive"])
    for index, task in enumerate(active):
        if task["id"] == task_id:
            moved = dict(task)
            moved["completed_at"] = _now_utc()
            del active[index]
            archive.append(moved)
            state["active"] = active
            state["archive"] = archive
            save_state(root, state)
            return deepcopy(moved)
    raise ValueError("Aufgabe wurde nicht in den aktiven Todos gefunden.")


def active_tasks(root: Path) -> list[dict[str, object]]:
    tasks = list(load_state(root)["active"])
    return sorted(tasks, key=lambda item: (item["due"] is None, str(item["due"] or ""), str(item["title"]).casefold()))


def archived_tasks(root: Path) -> list[dict[str, object]]:
    tasks = list(load_state(root)["archive"])
    return sorted(tasks, key=lambda item: str(item["completed_at"] or ""), reverse=True)
