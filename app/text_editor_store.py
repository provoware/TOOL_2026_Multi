"""Atomar gespeicherte allgemeine Textdokumente mit Titel-Dateinamen und Versionen."""

from __future__ import annotations

import json
import os
import re
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from app.atomic_io import atomic_write_json

SCHEMA_VERSION = 1


@dataclass
class TextDocument:
    title: str = "Unbenannter Text"
    text: str = ""
    notes: str = ""
    character_ids: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def safe_text_title(title: str) -> str:
    clean = re.sub(r"[\\/\x00-\x1f]+", "-", str(title).strip())
    clean = re.sub(r"\s+", " ", clean).strip(" .-")
    return clean[:120] or "Unbenannter Text"


def text_path(root: Path, title: str) -> Path:
    return root / "daten" / "texte" / f"{safe_text_title(title)}.json"


def _version_path(root: Path, title: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    return root / "daten" / "texte" / ".versionen" / safe_text_title(title) / f"{stamp}.json"


def _normalize_ids(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    result: list[str] = []
    seen: set[str] = set()
    for raw in values:
        value = " ".join(str(raw or "").split())
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _validate_payload(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("Textdokument muss ein JSON-Objekt enthalten.")
    schema = raw.get("schema_version", SCHEMA_VERSION)
    if schema != SCHEMA_VERSION:
        raise ValueError("Unbekannte Textdokument-Version.")
    title = safe_text_title(str(raw.get("title") or ""))
    text = str(raw.get("text") or "").replace("\r\n", "\n").replace("\r", "\n")
    notes = str(raw.get("notes") or "").replace("\r\n", "\n").replace("\r", "\n")
    if "\0" in text or "\0" in notes:
        raise ValueError("Text enthält unzulässige Steuerzeichen.")
    created = str(raw.get("created_at") or "").strip() or _now()
    updated = str(raw.get("updated_at") or "").strip() or created
    for label, value in (("Erstellzeit", created), ("Änderungszeit", updated)):
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError(f"{label} ist beschädigt.") from error
    return {
        "schema_version": SCHEMA_VERSION,
        "title": title,
        "text": text,
        "notes": notes,
        "character_ids": _normalize_ids(raw.get("character_ids", [])),
        "created_at": created,
        "updated_at": updated,
    }


def load_text_document(path: Path) -> TextDocument:
    payload = _validate_payload(json.loads(path.read_text(encoding="utf-8")))
    return TextDocument(
        title=str(payload["title"]), text=str(payload["text"]), notes=str(payload["notes"]),
        character_ids=list(payload["character_ids"]), created_at=str(payload["created_at"]),
        updated_at=str(payload["updated_at"]),
    )


def list_text_documents(root: Path) -> list[Path]:
    folder = root / "daten" / "texte"
    if not folder.is_dir():
        return []
    return sorted(
        (path for path in folder.glob("*.json") if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def save_text_document(root: Path, document: TextDocument, previous_path: Path | None = None) -> Path:
    now = _now()
    created = document.created_at or now
    payload = _validate_payload({
        "schema_version": SCHEMA_VERSION,
        **asdict(document),
        "title": document.title,
        "created_at": created,
        "updated_at": now,
    })
    target = text_path(root, str(payload["title"]))

    if target.is_file():
        current = _validate_payload(json.loads(target.read_text(encoding="utf-8")))
        comparable_current = {key: value for key, value in current.items() if key != "updated_at"}
        comparable_new = {key: value for key, value in payload.items() if key != "updated_at"}
        if comparable_current != comparable_new:
            atomic_write_json(_version_path(root, target.stem), current)

    atomic_write_json(target, payload)

    # Wird der Titel geändert, wird der alte Dateiname erst nach erfolgreichem
    # Schreiben des neuen Stands in die Versionen verschoben. Scheitert dieser
    # Zusatzschritt, bleiben beide Dateien erhalten statt Daten zu verlieren.
    if previous_path is not None:
        try:
            old = previous_path.resolve()
            new = target.resolve()
            if old != new and old.is_file():
                backup = _version_path(root, old.stem)
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(old, backup)
        except OSError:
            pass

    document.title = str(payload["title"])
    document.created_at = str(payload["created_at"])
    document.updated_at = str(payload["updated_at"])
    document.character_ids = list(payload["character_ids"])
    return target


def document_payload(document: TextDocument) -> dict[str, object]:
    return deepcopy(_validate_payload({"schema_version": SCHEMA_VERSION, **asdict(document)}))
