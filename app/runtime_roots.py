"""Explizite, geprüfte Trennung von Programmcode und dauerhaften Nutzerdaten.

Ohne Opt-in bleibt die bestehende Projektstruktur vollständig unverändert.
Ein unabhängiger Datenordner wird nur mit passendem lokalen Migrationsmarker
akzeptiert. Diese Funktion aktiviert oder migriert keine Installation.
"""
from __future__ import annotations

import json
from pathlib import Path

VARIABLE = "PROVOWARE_DATA_ROOT"
MARKER = ".provoware-managed-data.json"


def runtime_root(code_root, environment=None):
    code = Path(code_root).resolve(strict=True)
    if environment is None:
        import os
        environment = os.environ
    value = environment.get(VARIABLE)
    if not value:
        return code
    if not isinstance(value, str) or not value.startswith("/") or "\x00" in value:
        raise ValueError("Externer Datenpfad muss absolut sein.")
    supplied = Path(value)
    if supplied.is_symlink():
        raise ValueError("Datenordner darf keine Verknüpfung sein.")
    data = supplied.resolve(strict=True)
    if (not data.is_dir() or data == code or data.is_relative_to(code)
            or code.is_relative_to(data)):
        raise ValueError("Daten und Programm müssen in getrennten Ordnern liegen.")
    marker = data / MARKER
    if marker.is_symlink() or not marker.is_file() or marker.stat().st_size > 4096:
        raise ValueError("Für den externen Datenordner fehlt der Prüfmarker.")
    try:
        content = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("Prüfmarker des externen Datenordners ist nicht lesbar oder beschädigt.") from error
    if (not isinstance(content, dict) or set(content) !=
            {"schema_version", "purpose", "activation_allowed"}
            or content["schema_version"] != 1
            or content["purpose"] != "provoware-managed-data"
            or content["activation_allowed"] is not False):
        raise ValueError("Unbekannter oder aktivierender Datenmarker.")
    personal = data / "daten"
    if personal.is_symlink() or not personal.is_dir():
        raise ValueError("Persönliche Daten fehlen oder sind verknüpft.")
    return data
