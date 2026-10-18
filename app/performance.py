"""Begrenzte lokale Leistungsaggregate; Inhalte und freie Messnamen sind ausgeschlossen."""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from datetime import date, timedelta
import json
import math
import os
from pathlib import Path
import re
from threading import RLock
from time import perf_counter

OPERATIONS = ('app.start', 'module.open', 'archive.load', 'file.write', 'save.attempt')
AREAS = ('app', 'books', 'snippets', 'songs', 'texts', 'profiles', 'todo',
         'calendar', 'characters', 'diagnostics', 'exports', 'other')
BUCKETS = (1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 10000)
MAX_BYTES = 2 * 1024 * 1024
MAX_ROWS = 128
_ACTIVE = None
_SUPPRESSED = ContextVar('performance_suppressed', default=False)
WINDOW_AREAS = {'BookWindow': 'books', 'SnippetWindow': 'snippets',
                'TextEditorWindow': 'texts', 'SongLibrary': 'songs',
                'ProfileEditor': 'profiles', 'TodoWindow': 'todo',
                'CalendarWindow': 'calendar', 'CharacterWindow': 'characters',
                'RecoveryCenter': 'diagnostics'}
PATH_AREAS = {'buecher': 'books', 'textbausteine': 'snippets', 'songtexte': 'songs',
              'texte': 'texts', 'profile': 'profiles', 'todo': 'todo',
              'kalender': 'calendar', 'charaktere': 'characters'}


def _read(path):
    with Path(path).open('rb') as stream:
        value = stream.read(MAX_BYTES + 1)
    if len(value) > MAX_BYTES:
        raise ValueError('Leistungsdatei ist zu groß.')
    return json.loads(value.decode('utf-8'))


def validate(raw):
    if not isinstance(raw, dict) or set(raw) != {'schema_version', 'days'} or raw['schema_version'] != 1:
        raise ValueError('Ungültige Leistungsdatenversion.')
    days = raw['days']
    if not isinstance(days, dict) or len(days) > 31:
        raise ValueError('Ungültige Tagesliste.')
    fields = {'count', 'errors', 'unchanged', 'bytes', 'total_ms', 'max_ms', 'buckets'}
    for day, rows in days.items():
        if not isinstance(day, str) or date.fromisoformat(day).isoformat() != day:
            raise ValueError('Ungültiger Messtag.')
        if not isinstance(rows, dict) or len(rows) > MAX_ROWS:
            raise ValueError('Zu viele Messgruppen.')
        for key, row in rows.items():
            if not isinstance(key, str):
                raise ValueError('Ungültiger Messschlüssel.')
            parts = key.split('|')
            if len(parts) != 3 or not re.fullmatch(r'\d{1,8}\.\d{1,8}\.\d{1,8}', parts[0]):
                raise ValueError('Ungültige Programmversion.')
            if parts[1] not in OPERATIONS or parts[2] not in AREAS or not isinstance(row, dict) or set(row) != fields:
                raise ValueError('Nicht erlaubte Messfelder.')
            for name in ('count', 'errors', 'unchanged', 'bytes'):
                if type(row[name]) is not int or not 0 <= row[name] < 2**63:
                    raise ValueError('Ungültiger Zähler.')
            for name in ('total_ms', 'max_ms'):
                if type(row[name]) not in (float, int) or not math.isfinite(row[name]) or row[name] < 0:
                    raise ValueError('Ungültige Messdauer.')
            buckets = row['buckets']
            if (not isinstance(buckets, list) or len(buckets) != len(BUCKETS) + 1
                    or any(type(n) is not int or n < 0 for n in buckets)
                    or sum(buckets) != row['count'] or row['errors'] > row['count']
                    or row['unchanged'] > row['count'] or row['max_ms'] > row['total_ms']):
                raise ValueError('Inkonsistente Messgruppe.')
    return deepcopy(raw)


@contextmanager
def suppressed():
    token = _SUPPRESSED.set(True)
    try:
        yield
    finally:
        _SUPPRESSED.reset(token)


class Performance:
    def __init__(self, root, version='0.18.1'):
        if not re.fullmatch(r'\d{1,8}\.\d{1,8}\.\d{1,8}', version):
            raise ValueError('Ungültige Programmversion.')
        self.root, self.version = Path(root).resolve(), version
        self.settings_path = self.root / 'daten/ui/leistung.json'
        self.data_path = self.root / 'logs/leistung/statistik.json'
        self.enabled, self.retention = False, 30
        self.data = {'schema_version': 1, 'days': {}}
        self.last_error, self.read_error, self.dirty = '', False, False
        self.lock = RLock()
        try:
            if self.settings_path.exists():
                settings = _read(self.settings_path)
                if (set(settings) != {'schema_version', 'enabled', 'retention_days'}
                        or settings['schema_version'] != 1 or type(settings['enabled']) is not bool
                        or type(settings['retention_days']) is not int or not 1 <= settings['retention_days'] <= 30):
                    raise ValueError('Ungültige Messeinstellungen.')
                self.enabled, self.retention = settings['enabled'], settings['retention_days']
            if self.data_path.exists():
                self.data = validate(_read(self.data_path))
            self._prune()
        except (OSError, ValueError, TypeError, KeyError, AttributeError):
            self.enabled, self.read_error = False, True
            self.last_error = 'Messdatei nicht lesbar. Erhebung bleibt aus; vorhandene Datei bleibt erhalten. Zum Neustart Messdaten ausdrücklich löschen.'

    def _prune(self):
        cutoff = (date.today() - timedelta(days=self.retention - 1)).isoformat()
        expired = [day for day in self.data['days'] if day < cutoff]
        for day in expired:
            del self.data['days'][day]
        self.dirty = self.dirty or bool(expired)

    def configure(self, enabled, retention=30):
        if type(enabled) is not bool or type(retention) is not int or not 1 <= retention <= 30:
            raise ValueError('Ungültige Messeinstellung.')
        if self.read_error:
            raise ValueError(self.last_error)
        from app.atomic_io import atomic_write_json
        with self.lock, suppressed():
            atomic_write_json(self.settings_path, {'schema_version': 1, 'enabled': enabled, 'retention_days': retention})
            self.enabled, self.retention = enabled, retention
            self._prune()
        self.flush()

    def area_for_path(self, target):
        # Nur die logische Zielgruppe wird benötigt, keine Dateisystemauflösung.
        # Reale Pfadgrenzen des Exports werden getrennt im Exportweg geprüft.
        path = Path(os.path.abspath(target))
        if path.is_relative_to(self.root / 'logs') or path.is_relative_to(self.root / 'berichte'):
            return 'diagnostics'
        if path.is_relative_to(self.root / 'daten'):
            relative = path.relative_to(self.root / 'daten')
            return PATH_AREAS.get(relative.parts[0] if relative.parts else '', 'other')
        return 'exports'

    def record(self, operation, area='app', elapsed_ms=0.0, *, failed=False, size=0, unchanged=False):
        if not self.enabled or _SUPPRESSED.get():
            return
        if operation not in OPERATIONS or area not in AREAS:
            raise ValueError('Messname ist nicht erlaubt.')
        if (type(elapsed_ms) not in (int, float) or not math.isfinite(elapsed_ms) or elapsed_ms < 0
                or type(size) is not int or size < 0):
            raise ValueError('Ungültiger Messwert.')
        key = f'{self.version}|{operation}|{area}'
        with self.lock:
            self._prune()
            rows = self.data['days'].setdefault(date.today().isoformat(), {})
            if key not in rows and len(rows) >= MAX_ROWS:
                self.last_error = 'Messgruppengrenze erreicht; weitere Gruppen werden nicht erfasst.'
                return
            row = rows.setdefault(key, {'count': 0, 'errors': 0, 'unchanged': 0,
                                        'bytes': 0, 'total_ms': 0.0, 'max_ms': 0.0,
                                        'buckets': [0] * (len(BUCKETS) + 1)})
            row['count'] += 1
            row['errors'] += int(bool(failed))
            row['unchanged'] += int(bool(unchanged))
            row['bytes'] += size
            row['total_ms'] += elapsed_ms
            row['max_ms'] = max(row['max_ms'], elapsed_ms)
            bucket = next((i for i, limit in enumerate(BUCKETS) if elapsed_ms <= limit), len(BUCKETS))
            row['buckets'][bucket] += 1
            self.dirty = True

    def snapshot(self, days=30, operations=OPERATIONS):
        if type(days) is not int or not 1 <= days <= 30 or any(op not in OPERATIONS for op in operations):
            raise ValueError('Ungültige Berichtsauswahl.')
        cutoff = (date.today() - timedelta(days=days - 1)).isoformat()
        with self.lock:
            result = {'schema_version': 1, 'days': {}}
            for day, rows in self.data['days'].items():
                selected = {key: deepcopy(row) for key, row in rows.items()
                            if key.split('|')[1] in operations}
                if day >= cutoff and selected:
                    result['days'][day] = selected
            return validate(result)

    def flush(self):
        if self.read_error:
            return False
        try:
            from app.atomic_io import atomic_write_json
            with self.lock, suppressed():
                self._prune()
                if not self.dirty:
                    return True
                payload = validate(self.data)
                if len(json.dumps(payload).encode('utf-8')) > MAX_BYTES:
                    raise ValueError('Messdateigrenze erreicht.')
                atomic_write_json(self.data_path, payload)
                self.dirty, self.last_error = False, ''
            return True
        except Exception as error:
            self.last_error = f'Messdaten nicht gespeichert ({type(error).__name__}). Arbeitsdaten werden dadurch nicht blockiert.'
            return False

    def clear(self):
        from app.atomic_io import atomic_write_json
        with self.lock, suppressed():
            atomic_write_json(self.settings_path, {'schema_version': 1, 'enabled': False, 'retention_days': self.retention})
            self.enabled = False
            self.data_path.unlink(missing_ok=True)
            self.data = {'schema_version': 1, 'days': {}}
            self.dirty, self.read_error, self.last_error = False, False, ''


def activate(root, version='0.18.1'):
    global _ACTIVE
    _ACTIVE = Performance(root, version)
    return _ACTIVE


def current(root=None):
    if root is not None and (_ACTIVE is None or _ACTIVE.root != Path(root).resolve()):
        return activate(root)
    return _ACTIVE


class Sample:
    area = 'app'
    size = 0
    unchanged = False


@contextmanager
def observe(operation, area='app', *, target=None, content=None, encoding='utf-8'):
    tracker = _ACTIVE
    if tracker is None or not tracker.enabled or _SUPPRESSED.get():
        yield None
        return
    sample, failed = Sample(), False
    sample.area = area
    start = perf_counter()
    try:
        if target is not None:
            sample.area = tracker.area_for_path(target)
        if content is not None:
            sample.size = len(content.encode(encoding))
    except Exception:
        sample.area, sample.size = 'other', 0
    try:
        yield sample
    except BaseException:
        failed = True
        raise
    finally:
        try:
            tracker.record(operation, sample.area, (perf_counter() - start) * 1000,
                           failed=failed, size=sample.size, unchanged=sample.unchanged)
        except Exception as error:
            tracker.last_error = f'Messwert ausgelassen ({type(error).__name__}).'


def note_save(area, unchanged=False):
    if _ACTIVE is not None:
        try:
            _ACTIVE.record('save.attempt', area, unchanged=unchanged)
        except Exception:
            pass
