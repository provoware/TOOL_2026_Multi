"""Lokaler, atomar gespeicherter Profilbestand für wiederverwendbare DB-Eingaben."""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path

CATEGORIES = ("Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten")

DEFAULT_PROFILES = {
    "HardTechno": {
        "Genres": ["Hard Techno", "Schranz", "Industrial Techno", "Acid Techno"],
        "Stimmungen": ["treibend", "düster", "aggressiv", "hypnotisch"],
        "Stil": ["hart", "minimalistisch", "repetitiv", "druckvoll"],
        "Stimme": ["gesprochen", "verzerrt", "gerufen"],
        "Besonderheiten": ["harte Kicks", "Acid-Lines", "Breakdowns"],
    },
    "HipHop/Rap": {
        "Genres": ["Boom Bap", "Trap", "Conscious Rap", "Deutschrap"],
        "Stimmungen": ["selbstbewusst", "nachdenklich", "düster", "energetisch"],
        "Stil": ["storytelling", "direkt", "technisch", "melodisch"],
        "Stimme": ["gerappt", "ruhig", "rau", "melodisch"],
        "Besonderheiten": ["Punchlines", "mehrsilbige Reime", "Adlibs"],
    },
    "Hörspiele": {
        "Genres": ["Krimi", "Science-Fiction", "Fantasy", "Mystery", "Komödie", "Drama"],
        "Stimmungen": ["spannend", "mysteriös", "heiter", "bedrohlich", "emotional"],
        "Stil": ["dialogbetont", "erzählerisch", "atmosphärisch", "dokumentarisch"],
        "Stimme": ["Erzähler", "Figurenensemble", "flüsternd", "dramatisch"],
        "Besonderheiten": ["Geräuschkulisse", "Szenenwechsel", "Musikbett", "Cliffhanger"],
    },
}


def store_path(root: Path) -> Path:
    return root / "daten" / "profile" / "db_profile.json"


def _clean_profile_name(name: str) -> str:
    if "\0" in name or any(ord(char) < 32 for char in name):
        raise ValueError("Profilname enthält unzulässige Steuerzeichen.")
    value = " ".join(name.strip().split())
    if not value:
        raise ValueError("Profilname darf nicht leer sein.")
    return value


def _normalize_value(value: str) -> str:
    cleaned = " ".join(value.strip().split())
    if not cleaned:
        raise ValueError("Wert darf nicht leer sein.")
    return cleaned


def _validate(data: object) -> dict[str, dict[str, list[str]]]:
    if not isinstance(data, dict):
        raise ValueError("Profildatei muss ein JSON-Objekt enthalten.")
    result: dict[str, dict[str, list[str]]] = {}
    for raw_name, raw_categories in data.items():
        name = _clean_profile_name(str(raw_name))
        if not isinstance(raw_categories, dict):
            raise ValueError(f"Profil {name} ist beschädigt.")
        result[name] = {}
        for category in CATEGORIES:
            values = raw_categories.get(category, [])
            if not isinstance(values, list):
                raise ValueError(f"Kategorie {category} in Profil {name} ist beschädigt.")
            clean_values: list[str] = []
            seen: set[str] = set()
            for raw_value in values:
                value = _normalize_value(str(raw_value))
                key = value.casefold()
                if key not in seen:
                    clean_values.append(value)
                    seen.add(key)
            result[name][category] = clean_values
    return result


def load_profiles(root: Path) -> dict[str, dict[str, list[str]]]:
    target = store_path(root)
    if not target.exists():
        return copy.deepcopy(DEFAULT_PROFILES)
    data = json.loads(target.read_text(encoding="utf-8"))
    return _validate(data)


def save_profiles(root: Path, profiles: dict[str, dict[str, list[str]]]) -> Path:
    target = store_path(root)
    clean = _validate(profiles)
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


def add_profile(root: Path, name: str) -> str:
    clean_name = _clean_profile_name(name)
    profiles = load_profiles(root)
    if any(existing.casefold() == clean_name.casefold() for existing in profiles):
        raise ValueError("Dieses Profil gibt es bereits.")
    profiles[clean_name] = {category: [] for category in CATEGORIES}
    save_profiles(root, profiles)
    return clean_name


def add_value(root: Path, profile: str, category: str, value: str) -> str:
    if category not in CATEGORIES:
        raise ValueError("Unbekannte Kategorie.")
    clean_value = _normalize_value(value)
    profiles = load_profiles(root)
    if profile not in profiles:
        raise ValueError("Profil wurde nicht gefunden.")
    if any(existing.casefold() == clean_value.casefold() for existing in profiles[profile][category]):
        raise ValueError("Dieser Wert ist bereits vorhanden.")
    profiles[profile][category].append(clean_value)
    save_profiles(root, profiles)
    return clean_value


def remove_value(root: Path, profile: str, category: str, value: str) -> None:
    if category not in CATEGORIES:
        raise ValueError("Unbekannte Kategorie.")
    profiles = load_profiles(root)
    if profile not in profiles:
        raise ValueError("Profil wurde nicht gefunden.")
    values = profiles[profile][category]
    for index, existing in enumerate(values):
        if existing == value:
            del values[index]
            save_profiles(root, profiles)
            return
    raise ValueError("Wert wurde nicht gefunden.")
