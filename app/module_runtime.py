"""Nutzbare Formularmodule aus freigegebenen JSON-Entwürfen, ohne Codeausführung."""
from __future__ import annotations

from copy import deepcopy
from datetime import date
from pathlib import Path
import json
import re
from uuid import uuid4

from app import module_blueprints as blueprints
from app.atomic_io import atomic_write_json

MAX_RECORDS = 1000
MAX_BYTES = 2_000_000


def definition(root, module_id):
    items = blueprints.load(root)["blueprints"]
    return next((item for item in items if item["id"] == module_id), None)


def _path(root, module_id):
    from app.module_archive import identifier
    identifier(module_id)
    path = Path(root) / "daten" / "modulinstanzen"
    if (Path(root) / "daten").is_symlink() or path.is_symlink():
        raise ValueError("Verknüpftes Modulverzeichnis ist nicht zulässig.")
    return path / (module_id + ".json")


def validate_record(blueprint, record):
    if not isinstance(record, dict) or set(record) != {"id", "values"}:
        raise ValueError("Datensatz besitzt unerlaubte Felder.")
    from app.module_archive import identifier
    identifier(record["id"])
    values = record["values"]
    expected = {field["id"]: field["type"] for field in blueprint["fields"]}
    if not isinstance(values, dict) or set(values) != set(expected):
        raise ValueError("Feldbestand stimmt nicht mit dem Modulentwurf überein.")
    for key, kind in expected.items():
        value = values[key]
        if not isinstance(value, str) or len(value) > 20_000 or "\0" in value:
            raise ValueError("Unzulässiger Feldinhalt.")
        if kind == "number" and value and not re.fullmatch(r"-?\d{1,15}(?:\.\d{1,8})?", value):
            raise ValueError("Zahleneingabe ist ungültig.")
        if kind == "date" and value:
            try:
                date.fromisoformat(value)
            except ValueError as error:
                raise ValueError("Datum benötigt JJJJ-MM-TT.") from error
    return deepcopy(record)


def load(root, module_id):
    blueprint = definition(root, module_id)
    if blueprint is None:
        raise ValueError("Unbekannter Modulentwurf.")
    target = _path(root, module_id)
    if not target.exists():
        return {"schema_version": 1, "module_id": module_id, "records": []}
    if target.is_symlink() or target.stat().st_size > MAX_BYTES:
        raise ValueError("Moduldaten zu groß oder verknüpft.")
    raw = json.loads(target.read_text(encoding="utf-8"))
    if (not isinstance(raw, dict) or set(raw) != {"schema_version", "module_id", "records"}
            or raw["schema_version"] != 1 or raw["module_id"] != module_id
            or not isinstance(raw["records"], list) or len(raw["records"]) > MAX_RECORDS):
        raise ValueError("Moduldaten sind unbekannt oder beschädigt.")
    clean = [validate_record(blueprint, entry) for entry in raw["records"]]
    if len({item["id"] for item in clean}) != len(clean):
        raise ValueError("Doppelte Moduldatensätze.")
    return {"schema_version": 1, "module_id": module_id, "records": clean}


def save_record(root, module_id, values, record_id=None):
    blueprint = definition(root, module_id)
    if blueprint is None or "edit" not in blueprint["capabilities"]:
        raise ValueError("Modul ist nicht zum Bearbeiten freigegeben.")
    record = validate_record(blueprint, {"id": record_id or uuid4().hex, "values": values})
    state = load(root, module_id)
    idx = next((i for i, old in enumerate(state["records"]) if old["id"] == record["id"]), None)
    if idx is None:
        state["records"].append(record)
    else:
        state["records"][idx] = record
    if len(state["records"]) > MAX_RECORDS:
        raise ValueError("Moduldatensätze überschreiten das Limit.")
    blob = json.dumps(state, ensure_ascii=False).encode("utf-8")
    if len(blob) > MAX_BYTES:
        raise ValueError("Modulbestand ist zu groß.")
    atomic_write_json(_path(root, module_id), state)
    return deepcopy(record)


def query(root, module_id, needle=""):
    blueprint = definition(root, module_id)
    if blueprint is None:
        raise ValueError("Unbekannter Modulentwurf.")
    if needle and "search" not in blueprint["capabilities"]:
        raise ValueError("Suchfunktion wurde nicht freigegeben.")
    return [item for item in load(root, module_id)["records"]
            if needle.casefold() in " ".join(item["values"].values()).casefold()]
