"""Datenmodell, Bibliotheksspeicherung, Versionen und Exporte für Songtexte."""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

SECTION_TYPES = (
    "Intro", "Strophe", "Pre-Chorus", "Refrain", "Hook", "Bridge", "Outro", "Spoken", "Instrumental"
)
SONG_STATUSES = ("Idee", "Entwurf", "Überarbeitung", "Fertig")
META_HEADERS = {
    "TITEL": "title",
    "GENRE": "genre",
    "STIMMUNG": "mood",
    "STIL": "style",
    "STIMME": "voice",
    "BESONDERHEITEN": "special",
    "TAGS": "tags",
    "STATUS": "status",
    "FAVORIT": "favorite",
}


@dataclass
class SongSection:
    kind: str
    text: str = ""


@dataclass
class SongDocument:
    title: str = ""
    genre: str = ""
    mood: str = ""
    style: str = ""
    voice: str = ""
    special: str = ""
    tags: list[str] = field(default_factory=list)
    status: str = "Idee"
    favorite: bool = False
    other: str = ""
    sections: list[SongSection] = field(default_factory=list)

    def render(self) -> str:
        lines = [f"TITEL: {self.title.strip() or 'Unbenannt'}"]
        for label, value in (
            ("GENRE", self.genre), ("STIMMUNG", self.mood), ("STIL", self.style),
            ("STIMME", self.voice), ("BESONDERHEITEN", self.special),
        ):
            if value.strip():
                lines.append(f"{label}: {value.strip()}")
        tags = [tag.strip() for tag in self.tags if tag.strip()]
        if tags:
            lines.append(f"TAGS: {', '.join(tags)}")
        lines.append(f"STATUS: {self.status if self.status in SONG_STATUSES else 'Idee'}")
        lines.append(f"FAVORIT: {'Ja' if self.favorite else 'Nein'}")
        lines.append("")
        for section in self.sections:
            lines.append(f"[{section.kind}]")
            lines.append(section.text.rstrip())
            lines.append("")
        if self.other.strip():
            lines.extend(("[Sonstiges]", self.other.rstrip(), ""))
        return "\n".join(lines).rstrip() + "\n"

    def lyrics_only(self) -> str:
        lines: list[str] = []
        for section in self.sections:
            lines.extend((f"[{section.kind}]", section.text.rstrip(), ""))
        return "\n".join(lines).rstrip() + "\n"

    def markdown(self) -> str:
        lines = [f"# {self.title.strip() or 'Unbenannt'}", ""]
        metadata = (
            ("Genre", self.genre), ("Stimmung", self.mood), ("Stil", self.style),
            ("Stimme", self.voice), ("Besonderheiten", self.special),
            ("Tags", ", ".join(self.tags)), ("Status", self.status),
            ("Favorit", "Ja" if self.favorite else "Nein"),
        )
        for label, value in metadata:
            if value.strip():
                lines.append(f"**{label}:** {value.strip()}")
        lines.append("")
        for section in self.sections:
            lines.extend((f"## {section.kind}", "", section.text.rstrip(), ""))
        if self.other.strip():
            lines.extend(("## Sonstiges", "", self.other.rstrip(), ""))
        return "\n".join(lines).rstrip() + "\n"


def safe_title(title: str) -> str:
    """Erzeugt einen Linux-tauglichen Dateinamen ohne Pfadbestandteile."""
    clean = re.sub(r"[\\/\x00-\x1f]+", "-", title.strip())
    clean = re.sub(r"\s+", " ", clean).strip(" .-")
    return clean[:120] or "Unbenannter Song"


def song_path(root: Path, title: str) -> Path:
    return root / "daten" / "songtexte" / f"{safe_title(title)}.txt"


def _atomic_write(target: Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)


def _version_folder(root: Path, title: str) -> Path:
    return root / "daten" / "songtexte" / ".versionen" / safe_title(title)


def _version_path(root: Path, title: str) -> Path:
    folder = _version_folder(root, title)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    return folder / f"{stamp}.txt"


def save_song(root: Path, document: SongDocument) -> Path:
    """Schreibt atomar und sichert den vorherigen abweichenden Stand als Version."""
    target = song_path(root, document.title)
    content = document.render()
    if target.is_file():
        previous = target.read_text(encoding="utf-8")
        if previous == content:
            return target
        _atomic_write(_version_path(root, document.title), previous)
    _atomic_write(target, content)
    return target


def restore_version(root: Path, current_path: Path, version_path: Path) -> tuple[Path, Path | None]:
    """Stellt eine Version wieder her und sichert davor den aktuellen Stand."""
    song_folder = (root / "daten" / "songtexte").resolve()
    current = current_path.resolve()
    if current.parent != song_folder or current.suffix.lower() != ".txt" or not current.is_file():
        raise ValueError("Die aktuelle Songdatei liegt nicht im erlaubten Songordner.")
    current_document = load_song(current)
    expected_version_folder = _version_folder(root, current_document.title).resolve()
    version = version_path.resolve()
    if version.parent != expected_version_folder or version.suffix.lower() != ".txt" or not version.is_file():
        raise ValueError("Der gewählte Versionsstand gehört nicht zu diesem Song.")
    current_text = current.read_text(encoding="utf-8")
    old_text = version.read_text(encoding="utf-8")
    if current_text == old_text:
        return current, None
    backup = _version_path(root, current_document.title)
    _atomic_write(backup, current_text)
    _atomic_write(current, old_text)
    return current, backup


def parse_song(text: str, fallback_title: str = "") -> SongDocument:
    """Liest 0.7.0/0.8.0-Songs sowie Status- und Favoritfelder ab 0.9.0."""
    document = SongDocument(title=fallback_title)
    current_kind: str | None = None
    current_lines: list[str] = []

    def finish_section() -> None:
        nonlocal current_kind, current_lines
        if current_kind is None:
            return
        value = "\n".join(current_lines).strip("\n")
        if current_kind == "Sonstiges":
            document.other = value
        else:
            document.sections.append(SongSection(current_kind, value))
        current_kind, current_lines = None, []

    for raw in text.splitlines():
        section_match = re.fullmatch(r"\[([^\]]+)\]", raw.strip())
        if section_match:
            finish_section()
            current_kind = section_match.group(1).strip()
            continue
        if current_kind is not None:
            current_lines.append(raw)
            continue
        if ":" in raw:
            label, value = raw.split(":", 1)
            attr = META_HEADERS.get(label.strip().upper())
            cleaned = value.strip()
            if attr == "tags":
                document.tags = [part.strip() for part in value.split(",") if part.strip()]
            elif attr == "favorite":
                document.favorite = cleaned.casefold() in {"ja", "yes", "true", "1", "favorit"}
            elif attr == "status":
                document.status = cleaned if cleaned in SONG_STATUSES else "Idee"
            elif attr:
                setattr(document, attr, cleaned)
    finish_section()
    if not document.title.strip():
        document.title = fallback_title or "Unbenannter Song"
    if not document.sections:
        document.sections.append(SongSection("Strophe"))
    return document


def load_song(path: Path) -> SongDocument:
    return parse_song(path.read_text(encoding="utf-8"), path.stem)


def list_songs(root: Path) -> list[Path]:
    folder = root / "daten" / "songtexte"
    if not folder.is_dir():
        return []
    files = [path for path in folder.glob("*.txt") if path.is_file()]
    return sorted(files, key=lambda path: path.stat().st_mtime, reverse=True)


def list_versions(root: Path, title: str) -> list[Path]:
    folder = _version_folder(root, title)
    if not folder.is_dir():
        return []
    return sorted((path for path in folder.glob("*.txt") if path.is_file()), reverse=True)


def export_song(root: Path, document: SongDocument, export_format: str, *, lyrics_only: bool = False) -> Path:
    """Exportiert eine Kopie, ohne die Arbeitsdatei oder Versionsstände zu verändern."""
    export_format = export_format.lower()
    if lyrics_only:
        export_format = "txt"
        content = document.lyrics_only()
        suffix = "_nur-songtext"
    elif export_format == "txt":
        content, suffix = document.render(), ""
    elif export_format in {"md", "markdown"}:
        export_format, content, suffix = "md", document.markdown(), ""
    elif export_format == "json":
        payload = asdict(document)
        content, suffix = json.dumps(payload, ensure_ascii=False, indent=2) + "\n", ""
    else:
        raise ValueError(f"Nicht unterstütztes Exportformat: {export_format}")
    target = root / "daten" / "songtexte" / "export" / f"{safe_title(document.title)}{suffix}.{export_format}"
    _atomic_write(target, content)
    return target
