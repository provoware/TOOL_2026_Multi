"""Strikte lokale Dateipfade und persönliche Playlists für Multimedia-Module."""
from __future__ import annotations

import json
from pathlib import Path
from app.atomic_io import atomic_write_json

AUDIO = frozenset({".mp3", ".ogg", ".wav", ".flac", ".m4a", ".aac"})
IMAGE = frozenset({".jpg", ".jpeg", ".png", ".bmp", ".webp"})
VIDEO = frozenset({".mp4", ".mov", ".mkv", ".webm"})
MAX_PLAYLIST = 500
MAX_IMAGE = 25 * 1024 * 1024


def media_path(raw, suffixes, *, exists=True):
    if not isinstance(raw, (str, Path)) or not str(raw) or "\0" in str(raw):
        raise ValueError("Ungültiger Medienpfad.")
    source = Path(raw).expanduser()
    if not source.is_absolute() or source.is_symlink():
        raise ValueError("Bitte eine reguläre lokale Datei auswählen.")
    if ".." in source.parts or source.suffix.lower() not in suffixes:
        raise ValueError("Dateiformat oder Verzeichnispfad wird nicht unterstützt.")
    target = source.resolve(strict=exists)
    if exists and not target.is_file():
        raise ValueError("Die Mediendatei existiert nicht.")
    if target.suffix.lower() not in suffixes:
        raise ValueError("Dateiendung ist nicht zugelassen.")
    if exists and target.stat().st_size > 2 * 1024 * 1024 * 1024:
        raise ValueError("Mediendatei ist zu groß.")
    return target


def _playlist_path(root):
    root = Path(root)
    if (root / "daten").is_symlink() or (root / "daten/medien").is_symlink():
        raise ValueError("Playlistordner ist eine Verknüpfung.")
    return root / "daten/medien/playlist.json"


def validate_playlist(value):
    if not isinstance(value, dict) or set(value) != {"schema_version", "paths"} or value["schema_version"] != 1:
        raise ValueError("Playlist hat ein unbekanntes Format.")
    paths = value["paths"]
    if not isinstance(paths, list) or len(paths) > MAX_PLAYLIST:
        raise ValueError("Höchstens 500 Dateien in der Playlist.")
    result, unique = [], set()
    for path in paths:
        name = str(media_path(path, AUDIO, exists=False))
        if name.casefold() in unique:
            raise ValueError("Doppelte Mediendatei.")
        unique.add(name.casefold())
        result.append(name)
    return {"schema_version": 1, "paths": result}


def load_playlist(root):
    target = _playlist_path(root)
    if not target.exists():
        return {"schema_version": 1, "paths": []}
    if target.is_symlink() or target.stat().st_size > 250_000:
        raise ValueError("Playlistdatei ist eine Verknüpfung oder zu groß.")
    return validate_playlist(json.loads(target.read_text(encoding="utf-8")))


def save_playlist(root, state):
    return atomic_write_json(_playlist_path(root), validate_playlist(state))
