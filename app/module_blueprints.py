"""Strikt deklarativer Modulbaukasten: Vorlagen ohne Python-Code und Fremd-Plugins."""
from __future__ import annotations

from copy import deepcopy
import re
from uuid import uuid4

from app import module_archive as archive

MODULE = "modulentwuerfe"
COLLECTION = "blueprints"
CAPABILITIES = frozenset({"view", "edit", "search", "import", "export"})
FIELD_TYPES = frozenset({"text", "paragraph", "number", "date"})
IDENT = re.compile(r"[a-z][a-z0-9_]{1,39}\Z")
MAX_BLUEPRINTS = 200


def validate_blueprint(raw):
    keys = {"id", "title", "description", "fields", "capabilities"}
    if not isinstance(raw, dict) or set(raw) != keys:
        raise ValueError("Modulentwurf enthält unbekannte Felder.")
    archive.identifier(raw["id"])
    archive.text(raw["title"], "Modultitel", required=True, limit=100)
    archive.text(raw["description"], "Beschreibung", limit=1000)
    fields = raw["fields"]
    if not isinstance(fields, list) or not 1 <= len(fields) <= 12:
        raise ValueError("Ein Modul benötigt 1 bis 12 Eingabefelder.")
    unique = set()
    for field in fields:
        if not isinstance(field, dict) or set(field) != {"id", "label", "type"}:
            raise ValueError("Ungültiges Modul-Eingabefeld.")
        ident = field["id"]
        if not isinstance(ident, str) or not IDENT.fullmatch(ident) or ident in unique:
            raise ValueError("Feldkennungen müssen eindeutig und sicher sein.")
        unique.add(ident)
        archive.text(field["label"], "Feldbezeichnung", required=True, limit=80)
        if field["type"] not in FIELD_TYPES:
            raise ValueError("Unbekannter Feldtyp.")
    caps = raw["capabilities"]
    if (not isinstance(caps, list) or len(caps) > len(CAPABILITIES)
            or len(caps) != len(set(caps)) or not set(caps) <= CAPABILITIES
            or "view" not in caps):
        raise ValueError("Modulberechtigungen sind unbekannt oder widersprüchlich.")
    return deepcopy(raw)


def validate(raw):
    if (not isinstance(raw, dict) or set(raw) != {"schema_version", COLLECTION}
            or raw["schema_version"] != 1
            or not isinstance(raw[COLLECTION], list) or len(raw[COLLECTION]) > MAX_BLUEPRINTS):
        raise ValueError("Unbekanntes Modulentwurfarchiv.")
    items = [validate_blueprint(v) for v in raw[COLLECTION]]
    if (len({i["id"] for i in items}) != len(items)
            or len({i["title"].casefold() for i in items}) != len(items)):
        raise ValueError("Modulkennungen und Titel dürfen nicht doppelt vorkommen.")
    return {"schema_version": 1, COLLECTION: items}


def load(root):
    return archive.load(root, MODULE, validate,
                        lambda: {"schema_version": 1, COLLECTION: []})


def put(root, record):
    item = validate_blueprint(record)
    state = load(root)
    rows = state[COLLECTION]
    idx = next((n for n, row in enumerate(rows) if row["id"] == item["id"]), None)
    if idx is None:
        rows.append(item)
    else:
        rows[idx] = item
    archive.save(root, MODULE, state, validate)
    return deepcopy(item)


def remove(root, ident):
    archive.identifier(ident)
    state = load(root)
    old = len(state[COLLECTION])
    state[COLLECTION] = [x for x in state[COLLECTION] if x["id"] != ident]
    if len(state[COLLECTION]) == old:
        raise ValueError("Der Modulentwurf wurde nicht gefunden.")
    archive.save(root, MODULE, state, validate)


def import_copies(root, raw):
    entries = validate(raw)[COLLECTION]
    state = load(root)
    used = {x["title"].casefold() for x in state[COLLECTION]}
    for item in entries:
        item = deepcopy(item)
        item["id"] = uuid4().hex
        stem, counter = item["title"], 2
        while item["title"].casefold() in used:
            suffix = f" (Kopie {counter})"
            item["title"] = stem[:100-len(suffix)] + suffix
            counter += 1
        used.add(item["title"].casefold())
        state[COLLECTION].append(item)
    archive.save(root, MODULE, state, validate)
    return len(entries)


def preview_definition(item):
    """Die öffentliche Schnittstelle liefert NUR Daten, keine Importpfade/Callbacks."""
    item = validate_blueprint(item)
    return {"api_version": 1, "title": item["title"],
            "fields": deepcopy(item["fields"]),
            "capabilities": list(item["capabilities"]), "executable": False}
