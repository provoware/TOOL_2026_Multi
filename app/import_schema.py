"""Exakte, maschinenlesbare JSON-Struktur für externe Songtext-Importe."""

from __future__ import annotations

import json
from copy import deepcopy

from app.song_document import SONG_STATUSES, SongDocument, SongSection

SONG_IMPORT_TEMPLATE: dict[str, object] = {
    "title": "Beispieltitel",
    "genre": "Hard Techno",
    "mood": "treibend, düster",
    "style": "direkt, repetitiv",
    "voice": "tiefe Stimme",
    "special": "lange Drops",
    "tags": ["beispiel", "techno"],
    "status": "Idee",
    "favorite": False,
    "other": "Optionale abschließende Notizen zum Song.",
    "sections": [
        {"kind": "Intro", "text": "Text des Intros"},
        {"kind": "Strophe", "text": "Text der ersten Strophe"},
        {"kind": "Eigener Bereichsname", "text": "Auch frei benannte Bereiche sind erlaubt."},
    ],
}

SONG_IMPORT_FIELD_HELP: tuple[tuple[str, str, str], ...] = (
    ("title", "Text, Pflicht", "Songtitel; bestimmt später den Dateinamen."),
    ("genre", "Text, optional", "Genre oder mehrere Angaben als normaler Text."),
    ("mood", "Text, optional", "Stimmung."),
    ("style", "Text, optional", "Stil."),
    ("voice", "Text, optional", "Stimme/Stimmcharakter."),
    ("special", "Text, optional", "Besonderheiten."),
    ("tags", "Liste aus Texten", "Tags einzeln als JSON-Liste."),
    ("status", "Text", "Idee, Entwurf, Überarbeitung oder Fertig."),
    ("favorite", "true/false", "Favoritenstatus als JSON-Boolesch."),
    ("other", "Text, optional", "Abschließende Notizen."),
    ("sections", "Liste, Pflicht", "Jeder Bereich braucht kind und text."),
)


def song_import_template() -> dict[str, object]:
    return deepcopy(SONG_IMPORT_TEMPLATE)


def song_import_template_text() -> str:
    return json.dumps(SONG_IMPORT_TEMPLATE, ensure_ascii=False, indent=2) + "\n"


def song_import_help_text() -> str:
    lines = [
        "JSON-Importvorlage für Songtexte",
        "",
        "Die Feldnamen müssen exakt wie unten geschrieben werden. Zusätzliche unbekannte Felder werden nicht benötigt.",
        "",
    ]
    for name, field_type, description in SONG_IMPORT_FIELD_HELP:
        lines.append(f"• {name}: {field_type} — {description}")
    lines.extend(("", "Exakte Vorlage:", song_import_template_text()))
    return "\n".join(lines)


def song_document_from_import(payload: object) -> SongDocument:
    """Validiert die dokumentierte Struktur und erzeugt ein SongDocument."""
    if not isinstance(payload, dict):
        raise ValueError("Import muss ein JSON-Objekt enthalten.")
    title = str(payload.get("title") or "").strip()
    if not title:
        raise ValueError("Pflichtfeld title fehlt.")
    raw_sections = payload.get("sections")
    if not isinstance(raw_sections, list) or not raw_sections:
        raise ValueError("Pflichtfeld sections muss mindestens einen Bereich enthalten.")
    sections: list[SongSection] = []
    for index, raw in enumerate(raw_sections, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"sections[{index}] muss ein Objekt sein.")
        kind = " ".join(str(raw.get("kind") or "").split())
        if not kind:
            raise ValueError(f"sections[{index}].kind fehlt.")
        if "[" in kind or "]" in kind or "\0" in kind:
            raise ValueError(f"sections[{index}].kind enthält unzulässige Zeichen.")
        sections.append(SongSection(kind=kind[:80], text=str(raw.get("text") or "")))
    raw_tags = payload.get("tags", [])
    if not isinstance(raw_tags, list):
        raise ValueError("tags muss eine JSON-Liste sein.")
    tags = [" ".join(str(item).split()) for item in raw_tags if " ".join(str(item).split())]
    status = str(payload.get("status") or "Idee")
    if status not in SONG_STATUSES:
        raise ValueError("status ist ungültig.")
    favorite = payload.get("favorite", False)
    if not isinstance(favorite, bool):
        raise ValueError("favorite muss true oder false sein.")
    return SongDocument(
        title=title,
        genre=str(payload.get("genre") or "").strip(),
        mood=str(payload.get("mood") or "").strip(),
        style=str(payload.get("style") or "").strip(),
        voice=str(payload.get("voice") or "").strip(),
        special=str(payload.get("special") or "").strip(),
        tags=tags,
        status=status,
        favorite=favorite,
        other=str(payload.get("other") or ""),
        sections=sections,
    )
