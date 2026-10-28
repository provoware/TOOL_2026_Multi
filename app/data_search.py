"""Begrenzte, rein lesende Suche ohne Indexdateien und ohne Linkverfolgung."""
from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path
import stat
from time import monotonic

TEXT_TYPES = {'.txt', '.md', '.json', '.csv', '.log', '.ini', '.cfg', '.yaml', '.yml',
              '.toml', '.xml', '.html', '.css', '.js', '.ts', '.py', '.sh', '.rst', '.tex'}
MAX_FILE = 1024 * 1024
MAX_BYTES = 32 * 1024 * 1024
MAX_ENTRIES = 5000
MAX_HITS = 200
MAX_SECONDS = 10


@dataclass
class SearchResult:
    hits: list = field(default_factory=list)
    scanned: int = 0
    skipped: int = 0
    bytes_read: int = 0
    denied: int = 0
    denied_paths: list = field(default_factory=list)
    reason: str = 'running'


class DataSearch:
    def __init__(self, root, query, *, names=True, contents=True, cancelled=lambda: False, search_path=None):
        if not isinstance(query, str) or not query.strip() or len(query) > 200:
            raise ValueError('Bitte einen Suchtext mit 1 bis 200 Zeichen eingeben.')
        if not names and not contents:
            raise ValueError('Dateinamen oder Textinhalte auswählen.')
        self.data = Path(search_path).expanduser().absolute() if search_path is not None else Path(root) / 'daten'
        self.query = query.strip().casefold()
        self.names, self.contents, self.cancelled = names, contents, cancelled
        self.result = SearchResult()

    def record_denied(self, path):
        self.result.denied += 1
        if len(self.result.denied_paths) < 10:
            self.result.denied_paths.append(str(path))

    def _stop(self, started):
        if self.cancelled():
            self.result.reason = 'cancelled'
        elif monotonic() - started >= MAX_SECONDS:
            self.result.reason = 'time'
        elif self.result.scanned >= MAX_ENTRIES or len(self.result.hits) >= MAX_HITS:
            self.result.reason = 'limit'
        return self.result.reason != 'running'

    def _read(self, directory_fd, name):
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory_fd)
        with os.fdopen(descriptor, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_FILE:
                return None
            remaining = MAX_BYTES - self.result.bytes_read
            raw = stream.read(min(MAX_FILE + 1, remaining + 1))
            self.result.bytes_read += len(raw)
            if len(raw) > MAX_FILE or self.result.bytes_read > MAX_BYTES or b'\0' in raw:
                return None
            return raw.decode('utf-8-sig')

    def _file_hits(self, relative, name, directory_fd):
        hits = []
        if self.names and self.query in relative.casefold():
            hits.append({'path': relative, 'line': 0, 'excerpt': ''})
        if self.contents and Path(name).suffix.casefold() in TEXT_TYPES:
            try:
                text = self._read(directory_fd, name)
                if text is None:
                    self.result.skipped += 1
                    return hits
                for number, line in enumerate(text.splitlines(), 1):
                    if self.query in line.casefold():
                        hits.append({'path': relative, 'line': number, 'excerpt': line[:500]})
                    if len(hits) + len(self.result.hits) >= MAX_HITS:
                        break
            except PermissionError:
                self.record_denied(self.data / relative)
                self.result.skipped += 1
            except (OSError, UnicodeError):
                self.result.skipped += 1
        return hits

    def batches(self):
        started = monotonic()
        # Auch eine Verknüpfung in einem Elternordner würde os.fwalk
        # trotz follow_symlinks=False bis zur Suchwurzel durchlaufen.
        if any(path.is_symlink() for path in (self.data, *self.data.parents)):
            raise ValueError(
                'Der Suchordner oder ein übergeordneter Ordner ist eine Verknüpfung. '
                'Bitte den ursprünglichen Ordner auswählen.'
            )
        try:
            mode = self.data.stat().st_mode
            if not stat.S_ISDIR(mode):
                raise ValueError('Bitte einen Ordner als Suchpfad auswählen, keine einzelne Datei.')
        except FileNotFoundError:
            self.result.reason = 'missing'
            return
        except PermissionError:
            self.record_denied(self.data)
            self.result.reason = 'permission'
            return
        def inaccessible(error):
            self.result.skipped += 1
            if isinstance(error, PermissionError):
                self.record_denied(error.filename or self.data)
        # fwalk hält Verzeichnisdeskriptoren; openat + NOFOLLOW schützt auch bei
        # einem zwischen Prüfung und Lesen ausgetauschten Dateilink.
        for directory, dirs, files, directory_fd in os.fwalk(self.data, follow_symlinks=False, onerror=inaccessible):
            if self._stop(started):
                return
            self.result.scanned += 1
            dirs[:] = sorted(name for name in dirs if not name.startswith('.'))
            yield []
            for name in sorted(files):
                if self._stop(started):
                    return
                self.result.scanned += 1
                if name.startswith('.'):
                    continue
                try:
                    mode = os.stat(name, dir_fd=directory_fd, follow_symlinks=False).st_mode
                    if not stat.S_ISREG(mode):
                        self.result.skipped += 1
                        yield []
                        continue
                    relative = (Path(directory) / name).relative_to(self.data).as_posix()
                    hits = self._file_hits(relative, name, directory_fd)
                except PermissionError:
                    self.record_denied(Path(directory) / name)
                    self.result.skipped += 1
                    hits = []
                except OSError:
                    self.result.skipped += 1
                    hits = []
                hits = hits[:MAX_HITS - len(self.result.hits)]
                self.result.hits.extend(hits)
                yield hits
                if len(self.result.hits) >= MAX_HITS or self.result.bytes_read > MAX_BYTES:
                    self.result.reason = 'limit'
                    return
        self.result.reason = 'permission' if self.result.denied else 'done'
