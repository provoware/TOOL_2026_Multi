"""Begrenztes Lesen fester Profildateien ohne Verknüpfungen oder FIFO-Blockade."""
import os
import stat
from pathlib import Path

FILES = ('db_profile.json', 'genre_favoriten.json', 'zufallsverlauf.json')
MAX_FILE_BYTES = 16 * 1024 * 1024


def profile_folder(root):
    root = Path(os.path.abspath(root))
    folder = root / 'daten' / 'profile'
    if folder.resolve() != folder:
        raise ValueError('Profilpfade enthalten Verknüpfungen.')
    return folder


def read_bytes(root, name, limit=MAX_FILE_BYTES):
    path = profile_folder(root) / name
    if path.is_symlink():
        raise ValueError('Profildatei ist eine Verknüpfung.')
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return None
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError('Profildatei ist nicht regulär oder zu groß.')
        raw = stream.read(limit + 1)
        if len(raw) > limit:
            raise ValueError('Profildatei ist zu groß.')
    return raw
