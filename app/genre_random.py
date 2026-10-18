"""Lokaler profilbasierter Kreativ-Zufallsgenerator ohne Qt-Abhängigkeit.

Bestehende Profile werden ausschließlich über app.profile_store verwaltet.
JSON-Publikation erfolgt atomar; Fehleingaben ändern keine Nutzerdaten.
"""
from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path

from app.atomic_io import atomic_write_json
from app.profile_store import (
    CATEGORIES, add_values, load_profiles, save_profiles, split_input_values,
)

QUICK_AMOUNTS = (3, 6, 9, 12, 15)
DEFAULT_PRESETS = (
    {"Genres": 3, "Stimmungen": 3, "Stil": 3, "Stimme": 0, "Besonderheiten": 0},
    {"Genres": 6, "Stimmungen": 6, "Stil": 6, "Stimme": 3, "Besonderheiten": 3},
    {"Genres": 9, "Stimmungen": 9, "Stil": 9, "Stimme": 6, "Besonderheiten": 6},
)


def generator_path(root: Path) -> Path:
    return root / "daten" / "profile" / "zufallseinstellungen.json"


def history_path(root: Path) -> Path:
    return root / "daten" / "profile" / "zufallsverlauf.json"


def _amounts(values: dict[str, int]) -> dict[str, int]:
    if not isinstance(values, dict) or set(values) != set(CATEGORIES):
        raise ValueError("Mengen müssen für alle fünf Kategorien vorhanden sein.")
    for key, value in values.items():
        if type(value) is not int or not 0 <= value <= 999:
            raise ValueError(f"Ungültige Menge für {key}: 0 bis 999 erforderlich.")
    if not any(values.values()):
        raise ValueError("Bitte mindestens eine Kategorie mit einer Menge größer 0 wählen.")
    return dict(values)


def presets_load(root: Path) -> list[dict[str, int]]:
    path = generator_path(root)
    if not path.exists():
        return [dict(p) for p in DEFAULT_PRESETS]
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema") != 1 or not isinstance(raw.get("presets"), list) or len(raw["presets"]) != 3:
        raise ValueError("Die drei Mengenvorlagen sind beschädigt.")
    return [_amounts(p) for p in raw["presets"]]


def preset_save(root: Path, number: int, amounts: dict[str, int]) -> Path:
    if type(number) is not int or not 0 <= number < 3:
        raise ValueError("Die Vorlagennummer muss 1, 2 oder 3 sein.")
    checked = _amounts(amounts)
    presets = presets_load(root)
    presets[number] = checked
    return atomic_write_json(generator_path(root), {"schema": 1, "presets": presets})


def _history_validate(raw: object) -> list[dict]:
    if not isinstance(raw, list):
        raise ValueError("Die Verlaufsliste ist beschädigt.")
    result = []
    for entry in raw:
        if not isinstance(entry, dict) or not all(isinstance(entry.get(k), str) for k in ("timestamp", "profile", "output")):
            raise ValueError("Ein Verlaufseintrag ist beschädigt.")
        amounts = entry.get("amounts")
        if not isinstance(amounts, dict) or set(amounts) != set(CATEGORIES):
            raise ValueError("Die Verlaufs-Mengen sind beschädigt.")
        _amounts(amounts)
        result.append(entry)
    return result


def history_load(root: Path) -> list[dict]:
    path = history_path(root)
    return _history_validate(json.loads(path.read_text(encoding="utf-8"))) if path.exists() else []


def generate(root: Path, profile: str, amounts: dict[str, int],
             *, rng: random.Random | None = None) -> dict:
    """Prüft *alle* Mengen vor einer einzigen dauerhaft protokollierten Ziehung."""
    checked = _amounts(amounts)
    profiles = load_profiles(root)
    if profile not in profiles:
        raise ValueError("Bitte ein vorhandenes Profil auswählen.")
    data = profiles[profile]
    for cat in CATEGORIES:
        count = checked[cat]
        if count > len(data[cat]):
            raise ValueError(f"„{cat}“: {count} gewünscht, aber nur {len(data[cat])} vorhanden. Menge bitte verringern.")
    generator = rng or random.SystemRandom()
    drawn: dict[str, list[str]] = {}
    already_selected: set[str] = set()
    for cat in CATEGORIES:
        candidates = [item for item in data[cat] if item.casefold() not in already_selected]
        if len(candidates) < checked[cat]:
            raise ValueError(
                f"„{cat}“: zu wenige unterschiedliche Begriffe für die Gesamtausgabe. "
                "Menge verringern oder weitere Archivbegriffe hinzufügen."
            )
        drawn[cat] = generator.sample(candidates, checked[cat])
        already_selected.update(item.casefold() for item in drawn[cat])
    output = ", ".join(item for cat in CATEGORIES for item in drawn[cat])
    entry = {
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "profile": profile, "amounts": checked, "categories": drawn, "output": output,
    }
    history = history_load(root)
    atomic_write_json(history_path(root), history + [entry])
    return entry


def archive_export(root: Path, destination: Path) -> Path:
    if not destination.name.lower().endswith(".json"):
        raise ValueError("Exportdatei muss auf .json enden.")
    return atomic_write_json(destination, {"schema": 1, "profiles": load_profiles(root)})


def archive_import(root: Path, source: Path) -> dict[str, int]:
    """Validiert den kompletten Export vor dem einzigen Schreibvorgang.

    Import ergänzt fehlende Werte, überschreibt keine bestehenden Profile.
    """
    raw = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema") != 1 or not isinstance(raw.get("profiles"), dict):
        raise ValueError("Ungültiger Profil-Export.")
    # Der vorhandene Store validiert sämtliche Profilnamen und Werte inklusive Duplikaten.
    # Die Prüfung erfolgt in einem isolierten In-Memory-Zwischenschritt.
    incoming = raw["profiles"]
    current = load_profiles(root)
    from app.profile_store import _validate
    validated = _validate(incoming)
    combined = {key: {cat: list(vals) for cat, vals in record.items()} for key, record in current.items()}
    counts = {"profiles": 0, "values": 0}
    for name, record in validated.items():
        actual = next((p for p in combined if p.casefold() == name.casefold()), None)
        if actual is None:
            actual = name
            combined[actual] = {cat: [] for cat in CATEGORIES}
            counts["profiles"] += 1
        for cat in CATEGORIES:
            seen = {value.casefold() for value in combined[actual][cat]}
            for item in record[cat]:
                if item.casefold() not in seen:
                    combined[actual][cat].append(item)
                    seen.add(item.casefold())
                    counts["values"] += 1
    if counts["profiles"] or counts["values"]:
        save_profiles(root, combined)
    return counts


def rename_value(root: Path, profile: str, category: str, old: str, new: str) -> None:
    """Ändert einen Begriff atomar und erkennt doppelte Ziele ohne Datenverlust."""
    if category not in CATEGORIES:
        raise ValueError("Unbekannte Kategorie.")
    candidate = split_input_values(new)
    if len(candidate) != 1:
        raise ValueError("Beim Bearbeiten bitte genau einen Wert eingeben.")
    profiles = load_profiles(root)
    if profile not in profiles:
        raise ValueError("Profil wurde nicht gefunden.")
    values = profiles[profile][category]
    try:
        index = values.index(old)
    except ValueError as exc:
        raise ValueError("Der ursprüngliche Begriff wurde nicht gefunden.") from exc
    if any(item.casefold() == candidate[0].casefold() for i, item in enumerate(values) if i != index):
        raise ValueError("Dieser Begriff existiert bereits.")
    values[index] = candidate[0]
    save_profiles(root, profiles)
