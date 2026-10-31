"""Persönliche Projekt-Notizen und ausdrücklich bestätigte Altkopien."""
from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
import stat
import tempfile

from app.atomic_io import atomic_write_text

NOTE_FILE = Path('daten/notizen/projekt-notizen.txt')
LEGACY_FILE = 'Entwicklerinformation.txt'
MAX_NOTES_BYTES = 4 * 1024 * 1024


def _checked_path(root, relative):
    root = Path(root)
    for path in (root, *(root / Path(*relative.parts[:i]) for i in range(1, len(relative.parts) + 1))):
        if path.is_symlink():
            raise ValueError('Der Notizpfad darf keine Verknüpfung enthalten.')
    return root / relative


def _read_regular(path):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_NOTES_BYTES:
            raise ValueError('Notizdatei ist keine reguläre Datei oder größer als 4 MiB.')
        raw = stream.read(MAX_NOTES_BYTES + 1)
        if len(raw) > MAX_NOTES_BYTES:
            raise ValueError('Notizdatei ist größer als 4 MiB.')
        return raw


def _legacy_snapshot(root):
    source = _checked_path(root, Path(LEGACY_FILE))
    try:
        raw = _read_regular(source)
    except FileNotFoundError:
        return None
    name = 'altbestand-' + hashlib.sha256(raw).hexdigest() + '.txt'
    target = _checked_path(root, Path('daten/notizen') / name)
    return source, raw, target


def legacy_notes_pending(root):
    snapshot = _legacy_snapshot(root)
    if snapshot is None:
        return False
    _, raw, target = snapshot
    try:
        return _read_regular(target) != raw
    except FileNotFoundError:
        return True


def preserve_legacy_notes(root, *, approved=False):
    """Erhält alte Bytes ohne Überschreiben und ohne Änderung der Quelldatei."""
    if approved is not True:
        raise PermissionError('Alte Notizen nur nach ausdrücklicher Zustimmung übernehmen.')
    snapshot = _legacy_snapshot(root)
    if snapshot is None:
        return None
    source, raw, target = snapshot
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix='.alt-notizen-', dir=target.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)  # Eine vorhandene Altkopie nie ersetzen.
        except FileExistsError:
            if _read_regular(target) != raw:
                raise ValueError('Vorhandene Altkopie weicht ab und wurde nicht überschrieben.')
        if _read_regular(source) != raw or _read_regular(target) != raw:
            raise ValueError('Alte Notizen haben sich während der Übernahme geändert. Bitte erneut prüfen.')
    finally:
        temporary.unlink(missing_ok=True)
    return target


def append_developer_info(root: Path, text: str) -> Path:
    """Behält den bisherigen Funktionsnamen für vorhandene Aufrufer bei."""
    clean = ' '.join(str(text).splitlines()).strip()
    if not clean:
        raise ValueError('Die Schnelleingabe ist leer.')
    if any(ord(char) < 32 or ord(char) == 127 for char in clean):
        raise ValueError('Steuerzeichen sind in Projekt-Notizen nicht erlaubt.')
    target = _checked_path(root, NOTE_FILE)
    try:
        previous = _read_regular(target)
    except FileNotFoundError:
        previous = b''
    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
    content = previous.decode('utf-8') + f'[{timestamp}] {clean}\n'
    if len(content.encode('utf-8')) > MAX_NOTES_BYTES:
        raise ValueError('Projekt-Notizen sind größer als 4 MiB. Vorhandene Notizen bleiben erhalten.')
    return atomic_write_text(target, content)
