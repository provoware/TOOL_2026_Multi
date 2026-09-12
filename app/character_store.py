"""Atomarer Datenbestand für wiederverwendbare, konsistente Charakterprofile."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.atomic_io import atomic_write_json

SCHEMA_VERSION = 1
TEXT_FIELDS = (
    "name", "role", "age", "appearance", "personality", "motivation",
    "background", "relationships", "speech", "strengths", "weaknesses", "notes",
)


@dataclass(frozen=True)
class CharacterOption:
    """UI-unabhängige Auswahlrepräsentation für alle Schreibmodule."""

    character_id: str
    name: str
    role: str
    label: str
    reference: str


def store_path(root: Path) -> Path:
    return root / "daten" / "charaktere" / "charaktere.json"


def empty_state() -> dict[str, object]:
    return {"schema_version": SCHEMA_VERSION, "characters": []}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _clean_line(value: object, *, required: bool = False, field: str = "Wert") -> str:
    cleaned = " ".join(str(value or "").strip().split())
    if required and not cleaned:
        raise ValueError(f"{field} darf nicht leer sein.")
    if "\0" in cleaned:
        raise ValueError(f"{field} enthält unzulässige Zeichen.")
    return cleaned


def _clean_multiline(value: object) -> str:
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if "\0" in text:
        raise ValueError("Text enthält unzulässige Zeichen.")
    return text


def _clean_tags(value: object) -> list[str]:
    raw = value if isinstance(value, list) else str(value or "").split(",")
    result: list[str] = []
    seen: set[str] = set()
    for item in raw:
        cleaned = _clean_line(item)
        if not cleaned:
            continue
        key = cleaned.casefold()
        if key in seen:
            continue
        seen.add(key)
        result.append(cleaned)
    return result


def _validate_character(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("Charaktereintrag ist beschädigt.")
    character_id = _clean_line(raw.get("id"), required=True, field="Charakter-ID")
    created_at = _clean_line(raw.get("created_at"), required=True, field="Erstellzeit")
    updated_at = _clean_line(raw.get("updated_at"), required=True, field="Änderungszeit")
    for label, timestamp in (("Erstellzeit", created_at), ("Änderungszeit", updated_at)):
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError(f"{label} ist beschädigt.") from error
    result: dict[str, object] = {
        "id": character_id,
        "created_at": created_at,
        "updated_at": updated_at,
        "tags": _clean_tags(raw.get("tags", [])),
    }
    for field in TEXT_FIELDS:
        if field in {"name", "role", "age"}:
            result[field] = _clean_line(raw.get(field), required=field == "name", field="Name" if field == "name" else field)
        else:
            result[field] = _clean_multiline(raw.get(field))
    return result


def validate_state(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("Charakterdatei muss ein JSON-Objekt enthalten.")
    if raw.get("schema_version", SCHEMA_VERSION) != SCHEMA_VERSION:
        raise ValueError("Unbekannte Charakter-Datenversion.")
    characters_raw = raw.get("characters", [])
    if not isinstance(characters_raw, list):
        raise ValueError("Charakterdatei enthält keine gültige Liste.")
    characters = [_validate_character(item) for item in characters_raw]
    ids = [str(item["id"]) for item in characters]
    if len(ids) != len(set(ids)):
        raise ValueError("Charakterdatei enthält doppelte IDs.")
    return {"schema_version": SCHEMA_VERSION, "characters": characters}


def load_state(root: Path) -> dict[str, object]:
    target = store_path(root)
    if not target.exists():
        return empty_state()
    return validate_state(json.loads(target.read_text(encoding="utf-8")))


def save_state(root: Path, state: dict[str, object]) -> Path:
    return atomic_write_json(store_path(root), validate_state(state))


def list_characters(root: Path, search: str = "") -> list[dict[str, object]]:
    characters = [deepcopy(item) for item in load_state(root)["characters"]]
    needle = " ".join(search.casefold().split())
    if needle:
        characters = [
            item for item in characters
            if needle in " ".join(
                str(item.get(key, "")) for key in ("name", "role", "personality", "tags")
            ).casefold()
        ]
    return sorted(characters, key=lambda item: str(item["name"]).casefold())


def character_options(root: Path) -> list[CharacterOption]:
    """Liefert dieselbe stabile Charakterauswahl für jedes Schreibmodul."""
    options: list[CharacterOption] = []
    for character in list_characters(root):
        name = str(character["name"])
        role = str(character.get("role") or "").strip()
        options.append(CharacterOption(
            character_id=str(character["id"]),
            name=name,
            role=role,
            label=f"{name} — {role}" if role else name,
            reference=f"{name} ({role})" if role else name,
        ))
    return options


def get_character(root: Path, character_id: str) -> dict[str, object] | None:
    for item in load_state(root)["characters"]:
        if item["id"] == character_id:
            return deepcopy(item)
    return None


def upsert_character(root: Path, values: dict[str, object], character_id: str | None = None) -> dict[str, object]:
    state = load_state(root)
    characters = list(state["characters"])
    now = _now()
    existing: dict[str, object] | None = None
    existing_index: int | None = None
    if character_id:
        for index, item in enumerate(characters):
            if item["id"] == character_id:
                existing = dict(item)
                existing_index = index
                break
        if existing is None:
            raise ValueError("Der gewählte Charakter wurde nicht gefunden.")
    candidate: dict[str, object] = {
        "id": character_id or uuid4().hex,
        "created_at": existing["created_at"] if existing else now,
        "updated_at": now,
        "tags": values.get("tags", []),
    }
    for field in TEXT_FIELDS:
        candidate[field] = values.get(field, "")
    clean = _validate_character(candidate)
    if existing_index is None:
        characters.append(clean)
    else:
        characters[existing_index] = clean
    state["characters"] = characters
    save_state(root, state)
    return deepcopy(clean)


def character_reference(root: Path, character_id: str) -> str:
    character = get_character(root, character_id)
    if character is None:
        raise ValueError("Charakter wurde nicht gefunden.")
    role = str(character.get("role") or "").strip()
    return f"{character['name']} ({role})" if role else str(character["name"])


def character_marker(root: Path, character_id: str) -> str:
    """Erzeugt einen sichtbaren Marker, der nicht mit Songbereichsklammern kollidiert."""
    return f"«Charakter: {character_reference(root, character_id)}»"
