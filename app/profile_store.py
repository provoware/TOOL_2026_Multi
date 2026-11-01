"""Lokaler, atomar gespeicherter Profilbestand für wiederverwendbare DB-Eingaben."""

from __future__ import annotations

import copy
import csv
import unicodedata
import json
from pathlib import Path
from functools import lru_cache

from app.atomic_io import atomic_write_json
from app.texts import TextRegistry

CATEGORIES = ("Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten")

DEFAULT_PROFILES = {
    "HardTechno": {
        "Genres": ["Hard Techno", "Schranz", "Industrial Techno", "Acid Techno"],
        "Stimmungen": ["treibend", "düster", "aggressiv", "hypnotisch"],
        "Stil": ["hart", "minimalistisch", "repetitiv", "druckvoll"],
        "Stimme": ["gesprochen", "verzerrt", "gerufen"],
        "Besonderheiten": ["harte Kicks", "Acid-Lines", "Breakdowns"],
    },
    "Chill": {
        "Genres": ["Chillout", "Downtempo", "Ambient", "Lo-Fi"],
        "Stimmungen": ["entspannt", "sanft", "träumerisch", "gelassen"],
        "Stil": ["minimalistisch", "atmosphärisch", "warm", "ruhig"],
        "Stimme": ["weich", "instrumental", "geflüstert"],
        "Besonderheiten": ["weiche Klangflächen", "sanfte Übergänge", "warme Bässe"],
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


@lru_cache(maxsize=1)
def _input_registry() -> TextRegistry:
    return TextRegistry(Path(__file__).resolve().parent.parent / "texte/registry.json")


def input_text(key: str, fallback: str) -> str:
    return _input_registry().get("profile.input." + key, fallback)


def comparison_key(value: str) -> str:
    """Vergleicht kanonisch gleiche Texte, ohne gespeicherte Werte umzuschreiben."""
    return unicodedata.normalize("NFC", _normalize_value(value).casefold())


def normalize_new_value(value: str) -> str:
    """Nur neue Eingaben normalisieren; Altbestände bleiben im Ladeweg unverändert."""
    if not isinstance(value, str):
        raise ValueError(input_text('value_type', "Wert muss Text sein."))
    if any((ord(char) < 32 and char != "\t") or ord(char) == 127 for char in value):
        raise ValueError(input_text('controls', "Wert enthält unzulässige Steuerzeichen oder Zeilenumbrüche."))
    return unicodedata.normalize("NFC", _normalize_value(value))


def _validate(data: object) -> dict[str, dict[str, list[str]]]:
    if not isinstance(data, dict):
        raise ValueError("Profildatei muss ein JSON-Objekt enthalten.")
    result: dict[str, dict[str, list[str]]] = {}
    seen_profiles: set[str] = set()
    for raw_name, raw_categories in data.items():
        if not isinstance(raw_name, str):
            raise ValueError("Profilname muss Text sein.")
        name = _clean_profile_name(raw_name)
        profile_key = name.casefold()
        if profile_key in seen_profiles:
            raise ValueError("Profildatei enthält doppelte Profilnamen.")
        seen_profiles.add(profile_key)
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
                if not isinstance(raw_value, str):
                    raise ValueError(f"Kategorie {category} in Profil {name} enthält einen Wert, der kein Text ist.")
                value = _normalize_value(raw_value)
                key = value.casefold()
                if key in seen:
                    raise ValueError(f"Kategorie {category} in Profil {name} enthält doppelte Werte.")
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
    clean = _validate(profiles)
    return atomic_write_json(store_path(root), clean)


def add_profile(root: Path, name: str) -> str:
    clean_name = unicodedata.normalize("NFC", _clean_profile_name(name))
    profiles = load_profiles(root)
    if any(comparison_key(existing) == comparison_key(clean_name) for existing in profiles):
        raise ValueError("Dieses Profil gibt es bereits.")
    profiles[clean_name] = {category: [] for category in CATEGORIES}
    save_profiles(root, profiles)
    return clean_name


def add_value(root: Path, profile: str, category: str, value: str) -> str:
    if category not in CATEGORIES:
        raise ValueError("Unbekannte Kategorie.")
    clean_value = normalize_new_value(value)
    profiles = load_profiles(root)
    if profile not in profiles:
        raise ValueError("Profil wurde nicht gefunden.")
    if any(comparison_key(existing) == comparison_key(clean_value) for existing in profiles[profile][category]):
        raise ValueError("Dieser Wert ist bereits vorhanden.")
    profiles[profile][category].append(clean_value)
    save_profiles(root, profiles)
    return clean_value


def _csv_boundary_spaces(value: str) -> str:
    """Leerraum nach einem Schlusszitat erlauben, Inhalt und Escape-Zitate erhalten."""
    output: list[str] = []
    quoted, field_start, closed = False, True, False
    index = 0
    while index < len(value):
        char = value[index]
        if quoted and char == '"':
            if value[index:index + 2] == '""':
                output.append('""')
                index += 2
                continue
            quoted, closed = False, True
        elif not quoted:
            if closed and char == " ":
                end = index
                while end < len(value) and value[end] == " ":
                    end += 1
                if end < len(value) and value[end] != ",":
                    raise ValueError(input_text("quotes", "Anführungszeichen sind unvollständig oder falsch gesetzt."))
                index = end
                continue
            if char == ",":
                field_start, closed = True, False
            elif field_start and char != " ":
                quoted = char == '"'
                field_start = False
        output.append(char)
        index += 1
    return "".join(output)


def split_input_values(value: str, *, keep_duplicates: bool = False) -> list[str]:
    """Zerlegt eine Komma-Eingabe in bereinigte, innerhalb der Eingabe eindeutige Werte."""
    if not isinstance(value, str):
        raise ValueError(input_text('list_type', "Bitte eine Textliste eingeben."))
    # Zeilenwechsel nicht als zusätzliche CSV-Zeilen oder unsichtbare Werte annehmen.
    if any((ord(char) < 32 and char != "\t") or ord(char) == 127 for char in value):
        raise ValueError(input_text('one_line', "Bitte alle Werte in einer Zeile ohne Steuerzeichen eingeben."))
    try:
        fields = next(csv.reader([_csv_boundary_spaces(value.replace("\t", " ").strip())],
                                 skipinitialspace=True, strict=True), [])
    except csv.Error as error:
        raise ValueError(input_text('quotes', "Anführungszeichen sind unvollständig oder falsch gesetzt.")) from error
    result: list[str] = []
    seen: set[str] = set()
    for raw in fields:
        if not raw.strip():
            continue
        cleaned = normalize_new_value(raw)
        key = comparison_key(cleaned)
        if key in seen and not keep_duplicates:
            continue
        seen.add(key)
        result.append(cleaned)
    if not result:
        raise ValueError("Bitte mindestens einen Wert eingeben.")
    return result


def preview_values(root: Path, profile: str, category: str, value_text: str) -> dict:
    """Prüft ohne Schreiben; zählt Wiederholungen und Bestandsdubletten getrennt."""
    if category not in CATEGORIES:
        raise ValueError("Unbekannte Kategorie.")
    candidates = split_input_values(value_text, keep_duplicates=True)
    profiles = load_profiles(root)
    if profile not in profiles:
        raise ValueError("Profil wurde nicht gefunden.")
    existing = {comparison_key(value) for value in profiles[profile][category]}
    seen: set[str] = set()
    added, present, repeated = [], [], []
    for value in candidates:
        key = comparison_key(value)
        if key in seen:
            repeated.append(value)
        elif key in existing:
            present.append(value)
        else:
            added.append(value)
        seen.add(key)
    return {"new": added, "present": present, "repeated": repeated}


def add_values(root: Path, profile: str, category: str, value_text: str) -> list[str]:
    """Speichert eine Komma-Liste als einzelne DB-Einträge in genau einem atomaren Schreibvorgang."""
    if category not in CATEGORIES:
        raise ValueError("Unbekannte Kategorie.")
    candidates = split_input_values(value_text)
    profiles = load_profiles(root)
    if profile not in profiles:
        raise ValueError("Profil wurde nicht gefunden.")
    existing = {comparison_key(value) for value in profiles[profile][category]}
    added: list[str] = []
    for candidate in candidates:
        key = comparison_key(candidate)
        if key in existing:
            continue
        profiles[profile][category].append(candidate)
        existing.add(key)
        added.append(candidate)
    if added:
        save_profiles(root, profiles)
    return added


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


def validate_profile_import(data: object) -> dict[str, dict[str, list[str]]]:
    """Neue Importdaten prüfen; kanonische Mehrdeutigkeiten nie still zusammenführen."""
    validated = _validate(data)
    # Der Alt-Ladevalidator bereinigt Leerraum. Neue Rohwerte vorher prüfen,
    # damit er verbotene Zeilenumbrüche nicht vor der Importprüfung entfernt.
    for record in data.values():
        for category in CATEGORIES:
            for value in record.get(category, []):
                normalize_new_value(value)
    result: dict[str, dict[str, list[str]]] = {}
    names: set[str] = set()
    for name, record in validated.items():
        name = unicodedata.normalize("NFC", name)
        key = comparison_key(name)
        if key in names:
            raise ValueError(input_text('import_profiles', "Import enthält gleichwertige Unicode-Profilnamen."))
        names.add(key)
        result[name] = {}
        for category, values in record.items():
            normalized = [normalize_new_value(value) for value in values]
            if len({comparison_key(value) for value in normalized}) != len(normalized):
                raise ValueError(input_text('import_values', "Import enthält gleichwertige Unicode-Werte in einer Kategorie."))
            result[name][category] = normalized
    return result
