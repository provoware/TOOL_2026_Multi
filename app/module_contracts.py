"""Registrierung und stabile Modulverträge ohne dynamisches Ausführen fremder Plugins."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Protocol, runtime_checkable

from app.atomic_io import atomic_write_json

MAX_BYTES = 128 * 1024
_ID = re.compile(r"[a-z][a-z0-9_]{1,39}\Z")
_VERSION = re.compile(r"[0-9]{1,6}\.[0-9]{1,6}\.[0-9]{1,6}\Z")


@runtime_checkable
class ModuleInterface(Protocol):
    """Leichter Vertrag für später explizit angebundene Fenster."""
    def refresh(self) -> None: ...
    def set_zoom(self, percent: int) -> None: ...


@dataclass(frozen=True)
class ModuleDefinition:
    module_id: str
    title: str
    version: str
    capabilities: tuple[str, ...]
    api_version: int = 1

    def __post_init__(self):
        if (not isinstance(self.module_id, str) or not _ID.fullmatch(self.module_id)
                or not isinstance(self.title, str) or not self.title.strip()
                or len(self.title) > 100 or not isinstance(self.version, str)
                or not _VERSION.fullmatch(self.version) or self.api_version != 1):
            raise ValueError("Ungültiger Modulvertrag.")
        if (not isinstance(self.capabilities, tuple)
                or len(self.capabilities) > 20
                or any(not isinstance(v, str) or not _ID.fullmatch(v) for v in self.capabilities)
                or len(self.capabilities) != len(set(self.capabilities))):
            raise ValueError("Ungültige oder doppelte Modulfähigkeiten.")


# Ausschließlich im Quellcode überprüfte vorhandene Modulkennungen;
# kein Laden von Pfaden, Python-Modulnamen oder Code aus Archivdaten.
BUILTIN_MODULES = (
    ModuleDefinition("songs", "Songtexte", "1.0.0", ("edit", "search")),
    ModuleDefinition("genres", "Genres und Zufall", "1.0.0", ("edit", "search")),
    ModuleDefinition("todo", "Aufgaben", "1.0.0", ("edit",)),
    ModuleDefinition("calendar", "Kalender", "1.0.0", ("edit",)),
    ModuleDefinition("ideas", "Ideenarchiv", "1.0.0", ("edit", "search")),
    ModuleDefinition("books", "Buchwerkstatt", "1.0.0", ("edit",)),
    ModuleDefinition("accounts", "Kontometadaten", "1.0.0", ("edit", "search")),
    ModuleDefinition("quicklinks", "Link-Schnellstarter", "1.0.0", ("edit",)),
    ModuleDefinition("wiki", "Wiki", "1.0.0", ("edit", "search")),
    ModuleDefinition("module_builder", "Modulbaukasten", "1.0.0", ("view", "edit", "import", "export")),
    ModuleDefinition("development_pool", "Entwicklungspool", "1.0.0", ("view", "edit", "export")),
)

# Erst diese bereits mit fester Fensterklasse bekannten Zusatzmodule sind
# zur Laufzeit abschaltbar. Kernmodule bleiben hiervon unangetastet.
OPTIONAL_MODULES = ("ideas", "accounts", "quicklinks", "wiki")


def _catalog_path(root):
    return Path(root) / "daten" / "modulbaukasten" / "katalog.json"


def validate_catalog(raw, definitions=BUILTIN_MODULES):
    if not isinstance(raw, dict) or set(raw) != {"schema_version", "modules"} or raw["schema_version"] != 1:
        raise ValueError("Modulkatalog hat eine unbekannte Struktur.")
    registered = {d.module_id: d for d in definitions}
    values = raw["modules"]
    if not isinstance(values, list) or len(values) > 128:
        raise ValueError("Ungültige Zahl registrierter Module.")
    ids = set()
    clean = []
    for item in values:
        if not isinstance(item, dict) or set(item) != {"id", "version", "enabled"}:
            raise ValueError("Modulkatalog enthält unerlaubte Felder.")
        name, version, enabled = item["id"], item["version"], item["enabled"]
        if (not isinstance(name, str) or name not in registered
                or name in ids or version != registered[name].version
                or type(enabled) is not bool):
            raise ValueError("Unbekanntes, doppeltes oder inkompatibles Modul.")
        ids.add(name)
        clean.append({"id": name, "version": version, "enabled": enabled})
    return {"schema_version": 1, "modules": sorted(clean, key=lambda entry: entry["id"])}


def load_catalog(root, definitions=BUILTIN_MODULES):
    path = _catalog_path(root)
    if not path.exists() and not path.is_symlink():
        return {"schema_version": 1, "modules": []}
    if path.is_symlink() or path.stat().st_size > MAX_BYTES:
        raise ValueError("Modulkatalog ist ein Link oder zu groß.")
    return validate_catalog(json.loads(path.read_text(encoding="utf-8")), definitions)


def set_registered(root, module_id, *, enabled, definitions=BUILTIN_MODULES):
    """Registrierung ist Metadatenfreigabe, kein Import oder Programmstart.

    Vorhandene Hauptmodul-Schaltflächen werden noch nicht durch diesen
    Katalog deaktiviert. Das ist bewusst kein dynamischer Plugin-Lader.
    """
    if type(enabled) is not bool:
        raise ValueError("Aktivierung muss Ja oder Nein sein.")
    definitions_by_id = {d.module_id: d for d in definitions}
    if module_id not in definitions_by_id:
        raise ValueError("Modulkennung ist nicht im geprüften Katalog.")
    state = load_catalog(root, definitions)
    entries = [item for item in state["modules"] if item["id"] != module_id]
    entries.append({"id": module_id, "version": definitions_by_id[module_id].version, "enabled": enabled})
    state["modules"] = entries
    clean = validate_catalog(state, definitions)
    atomic_write_json(_catalog_path(root), clean)
    return clean


def describe(root, definitions=BUILTIN_MODULES):
    registered = {item["id"]: item["enabled"] for item in load_catalog(root, definitions)["modules"]}
    return [{"id": d.module_id, "title": d.title, "version": d.version,
             "api_version": d.api_version, "capabilities": list(d.capabilities),
             "catalog_enabled": registered.get(d.module_id, False)}
            for d in definitions]


def is_module_enabled(root, module_id, definitions=BUILTIN_MODULES):
    """Bereits vorhandene Module sind standardmäßig weiterhin zugänglich."""
    known = {d.module_id for d in definitions}
    if module_id not in known:
        raise ValueError("Unbekannte Modulkennung.")
    entries = load_catalog(root, definitions)["modules"]
    return next((item["enabled"] for item in entries if item["id"] == module_id), True)


def set_module_preferences(root, selections, definitions=BUILTIN_MODULES):
    """Alle ausgewählten Menüschalter werden zusammen und atomar gespeichert."""
    if (not isinstance(selections, dict) or not selections
            or any(key not in OPTIONAL_MODULES or type(value) is not bool
                   for key, value in selections.items())):
        raise ValueError("Nur bekannte Zusatzmodule dürfen geschaltet werden.")
    definitions_by_id = {item.module_id: item for item in definitions}
    if any(key not in definitions_by_id for key in selections):
        raise ValueError("Unbekannte Modulversion.")
    previous = load_catalog(root, definitions)
    old = {item["id"]: item for item in previous["modules"]}
    for name, enabled in selections.items():
        old[name] = {"id": name, "version": definitions_by_id[name].version,
                     "enabled": enabled}
    state = validate_catalog({"schema_version": 1, "modules": list(old.values())}, definitions)
    atomic_write_json(_catalog_path(root), state)
    return state
