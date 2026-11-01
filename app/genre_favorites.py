"""Favoriten und monatsweise Statistik für den profilbasierten Suno-Generator."""
from __future__ import annotations
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from app.atomic_io import atomic_write_json, atomic_write_text
from app.genre_random import history_load
from app.profile_store import CATEGORIES, load_profiles, read_profile
import json


def favorites_path(root: Path) -> Path:
    return root / "daten" / "profile" / "genre_favoriten.json"


def load_favorites(root: Path) -> dict[str, dict[str, list[str]]]:
    from app.profile_transaction import ensure_ready
    ensure_ready(root)
    path = favorites_path(root)
    raw = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schema": 1, "favorites": {}}
    return validate_favorites(raw)


def validate_favorites(raw: object) -> dict[str, dict[str, list[str]]]:
    """Prüft auch einen bereits begrenzt eingelesenen Lesestand ohne Schreiben."""
    if not isinstance(raw, dict) or raw.get("schema") != 1 or not isinstance(raw.get("favorites"), dict):
        raise ValueError("Favoritendatei ist beschädigt.")
    result = {}
    for profile, cats in raw["favorites"].items():
        if not isinstance(profile, str) or not isinstance(cats, dict) or set(cats) != set(CATEGORIES):
            raise ValueError("Favoritenprofil ist ungültig.")
        for cat in CATEGORIES:
            values = cats[cat]
            if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
                raise ValueError("Favoriteneinträge sind ungültig.")
            if len({v.casefold() for v in values}) != len(values):
                raise ValueError("Favoritendatei enthält Duplikate.")
        result[profile] = cats
    return result


def favorite_values(root: Path, profile: str, category: str) -> list[str]:
    if category not in CATEGORIES:
        raise ValueError("Profil oder Kategorie unbekannt.")
    values = read_profile(root, profile, category=category)[category]
    favorites = load_favorites(root).get(profile, {}).get(category, [])
    stored = {v.casefold() for v in favorites}
    return [v for v in values if v.casefold() in stored]


def set_favorite(root: Path, profile: str, category: str, value: str, enabled: bool) -> bool:
    profiles = load_profiles(root)
    if profile not in profiles or category not in CATEGORIES:
        raise ValueError("Profil oder Kategorie unbekannt.")
    actual = next((v for v in profiles[profile][category] if v.casefold() == value.casefold()), None)
    if actual is None:
        raise ValueError("Der Eintrag ist nicht im Archiv.")
    favorites = load_favorites(root)
    record = favorites.setdefault(profile, {cat: [] for cat in CATEGORIES})
    old = record[category]
    current = [v for v in old if v.casefold() != actual.casefold()]
    if enabled:
        current.append(actual)
    if current == old:
        return False
    record[category] = current
    atomic_write_json(favorites_path(root), {"schema": 1, "favorites": favorites})
    return True


def monthly_statistics(root: Path, cutoff: date) -> dict:
    """Vom Monatsanfang bis zum gewählten Stichtag (einschließlich)."""
    entries = []
    for entry in history_load(root):
        try:
            stamp = datetime.fromisoformat(entry["timestamp"]).date()
        except (TypeError, ValueError) as exc:
            raise ValueError("Ein Verlaufs-Zeitstempel ist beschädigt.") from exc
        if stamp.year == cutoff.year and stamp.month == cutoff.month and stamp <= cutoff:
            entries.append(entry)
    profiles = Counter(e["profile"] for e in entries)
    favorite_draws = sum(bool(e.get("favorites_only")) for e in entries)
    categories = Counter()
    values = Counter()
    favorites_used = 0
    all_favorites = load_favorites(root)
    for entry in entries:
        record = entry.get("categories", {})
        if not isinstance(record, dict):
            raise ValueError("Ein Verlaufs-Kategorienfeld ist beschädigt.")
        for cat in CATEGORIES:
            names = record.get(cat, [])
            if not isinstance(names, list) or any(not isinstance(name, str) for name in names):
                raise ValueError("Ein Verlaufs-Kategorienfeld ist beschädigt.")
            categories[cat] += len(names)
            values.update(names)
            favorites = {v.casefold() for v in all_favorites.get(entry["profile"], {}).get(cat, [])}
            favorites_used += sum(v.casefold() in favorites for v in names)
    return {"cutoff": cutoff.isoformat(), "total": len(entries),
            "favorite_draws": favorite_draws,
            "profiles": dict(sorted(profiles.items())),
            "categories": {cat: categories[cat] for cat in CATEGORIES},
            "favorites_used": favorites_used, "most_common": values.most_common(15)}


def monthly_report_text(root: Path, cutoff: date) -> str:
    stats = monthly_statistics(root, cutoff)
    lines = [f"PROVOWARE · Genres-Zufall · Monatsauswertung",
             f"Monat: {cutoff:%Y-%m} · Stichtag: {cutoff.isoformat()} (einschließlich)",
             f"Generierungen: {stats['total']}",
             f"Davon reine Favoriten-Ziehungen: {stats['favorite_draws']}",
             f"Aktuell als Favoriten markierte gezogene Begriffe: {stats['favorites_used']}",
             "", "Profile:"]
    lines += [f"  {name}: {count}" for name, count in stats["profiles"].items()] or ["  Keine"]
    lines += ["", "Kategorien:"]
    lines += [f"  {cat}: {count}" for cat, count in stats["categories"].items()]
    lines += ["", "Häufigste gezogene Begriffe:"]
    lines += [f"  {word}: {count}" for word, count in stats["most_common"]] or ["  Keine"]
    lines += ["", "Hinweis: Favoriten sind der aktuelle Stand, nicht zwingend der Stand am Ziehungstag."]
    return "\n".join(lines) + "\n"


def export_monthly_report(root: Path, cutoff: date, destination: Path) -> Path:
    if destination.suffix.lower() != ".txt":
        raise ValueError("Monatsauswertung muss als .txt gespeichert werden.")
    if destination.resolve().is_relative_to((root / "daten").resolve()):
        raise ValueError("Bericht darf keine internen Projektdaten überschreiben.")
    return atomic_write_text(destination, monthly_report_text(root, cutoff))
