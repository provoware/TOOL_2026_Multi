"""Erweiterungsvertrag ohne dynamische Codeausführung.

Ein Fremdpaket darf ausschließlich ein genau definiertes JSON-Dokument mit
verifizierten Aktionen liefern. Python-/Shell-Programme werden nicht geladen.
"""
from __future__ import annotations

import json
from pathlib import Path

from app import module_permissions

ALLOWED_ACTIONS = frozenset(("view", "search", "edit"))
MAX_FILE = 64 * 1024
MAX_ACTIONS = 24


def validate_extension(raw):
    if not isinstance(raw, dict) or set(raw) != {
        "schema_version", "module_id", "actions"}:
        raise ValueError("Unbekannter Erweiterungsvertrag.")
    if type(raw["schema_version"]) is not int or raw["schema_version"] != 1:
        raise ValueError("Nicht unterstützte Vertragsversion.")
    from app.module_archive import identifier
    module_id = identifier(raw["module_id"])
    actions = raw["actions"]
    if not isinstance(actions, list) or not 1 <= len(actions) <= MAX_ACTIONS:
        raise ValueError("Die Erweiterung enthält zu viele oder keine Aktionen.")
    validated = []
    for action in actions:
        if not isinstance(action, dict) or set(action) != {"action", "arguments"}:
            raise ValueError("Aktion enthält unerlaubte Felder.")
        kind, args = action["action"], action["arguments"]
        if kind not in ALLOWED_ACTIONS or not isinstance(args, dict):
            raise PermissionError("Unzulässiger Ausführungstyp.")
        if kind == "view" and args:
            raise ValueError("Ansicht besitzt keine Argumente.")
        if kind == "search":
            if set(args) != {"needle"} or not isinstance(args["needle"], str) or len(args["needle"]) > 160:
                raise ValueError("Ungültiger Suchbegriff.")
        if kind == "edit":
            if set(args) != {"values"} or not isinstance(args["values"], dict):
                raise ValueError("Falsches Bearbeitungsformat.")
            if (len(args["values"]) > 12 or
                any(not isinstance(k, str) or not isinstance(v, str) or
                    len(v) > 20000 for k, v in args["values"].items())):
                raise ValueError("Felder überschreiten die erlaubten Grenzen.")
        validated.append({"action": kind, "arguments": dict(args)})
    return {"schema_version": 1, "module_id": module_id, "actions": validated}


def load_extension(path):
    source = Path(path)
    if source.is_symlink() or not source.is_file() or source.stat().st_size > MAX_FILE:
        raise ValueError("Erweiterungsdatei fehlt, ist verknüpft oder zu groß.")
    data = source.read_bytes()
    if len(data) > MAX_FILE:
        raise ValueError("Erweiterungsdatei ist zu groß.")
    return validate_extension(json.loads(data.decode("utf-8")))


def execute_approved(root, document, *, approved=False):
    """Explizite Freigabe, nur eine Aktion pro Aufruf; keine Fremdcodeausführung.

    Mehrfachausführung ohne atomaren Gesamtvertrag wird absichtlich verweigert.
    """
    if type(approved) is not bool or not approved:
        raise PermissionError("Eine ausdrückliche Zustimmung ist erforderlich.")
    data = validate_extension(document)
    if len(data["actions"]) != 1:
        raise PermissionError("Mehrfachaktionen benötigen eine gesonderte Freigabe.")
    row = data["actions"][0]
    return module_permissions.dispatch(
        root, data["module_id"], row["action"], approved=True,
        needle=row["arguments"].get("needle", ""),
        values=row["arguments"].get("values"),
    )
