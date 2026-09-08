"""Datenmodell und sichere Speicherung für Songtexte."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

SECTION_TYPES = (
    "Intro", "Strophe", "Pre-Chorus", "Refrain", "Hook", "Bridge", "Outro", "Spoken", "Instrumental"
)


@dataclass
class SongSection:
    kind: str
    text: str = ""


@dataclass
class SongDocument:
    title: str = ""
    genre: str = ""
    other: str = ""
    sections: list[SongSection] = field(default_factory=list)

    def render(self) -> str:
        lines = [f"TITEL: {self.title.strip() or 'Unbenannt'}"]
        if self.genre.strip():
            lines.append(f"GENRE: {self.genre.strip()}")
        lines.append("")
        for section in self.sections:
            lines.append(f"[{section.kind}]")
            lines.append(section.text.rstrip())
            lines.append("")
        if self.other.strip():
            lines.extend(("[Sonstiges]", self.other.rstrip(), ""))
        return "\n".join(lines).rstrip() + "\n"


def safe_title(title: str) -> str:
    """Erzeugt einen Linux-tauglichen Dateinamen ohne Pfadbestandteile."""
    clean = re.sub(r"[\\/\x00-\x1f]+", "-", title.strip())
    clean = re.sub(r"\s+", " ", clean).strip(" .-")
    return clean[:120] or "Unbenannter Song"


def song_path(root: Path, title: str) -> Path:
    return root / "daten" / "songtexte" / f"{safe_title(title)}.txt"


def save_song(root: Path, document: SongDocument) -> Path:
    """Schreibt den aktuellen Song atomar unter seinem Titel."""
    target = song_path(root, document.title)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(document.render())
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)
    return target
