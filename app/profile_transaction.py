"""Rücknehmbarer Drei-Dateien-Wechsel unter exklusiver, prozessweiter Sperre.

Ein vorhandenes Journal bedeutet immer: vor erneuter Nutzung zurückrollen.
Es enthält ausschließlich feste Dateinamen und exakte Vor-/Nachherbytes.
"""
import base64
import fcntl
import hashlib
import json
import os
import stat
from pathlib import Path
from contextlib import contextmanager

from app.atomic_io import _write_text, _fsync_directory
from app.profile_file_io import FILES, MAX_FILE_BYTES, profile_folder, read_bytes

JOURNAL = '.profile-rename-journal.json'
LOCK = '.profile-rename.lock'
MAX_JOURNAL_BYTES = 140 * 1024 * 1024


class ProfileRecoveryError(RuntimeError):
    """Profile sind bis zur erfolgreichen Wiederherstellung gesperrt."""


def _text(key, fallback):
    from app.profile_store import input_text
    return input_text('transaction.' + key, fallback)


def ensure_ready(root):
    path = Path(root) / 'daten' / 'profile' / JOURNAL
    if path.exists() or path.is_symlink():
        raise ProfileRecoveryError(_text('pending', 'Eine Profiländerung ist unvollständig. Profile bleiben geschützt. Bitte das Programm neu starten; bei erneutem Fehler Hilfe & Fehlerhilfe öffnen.'))


def check_write(target):
    # Nur die drei gemeinsamen Profilbestände sperren, nicht Logs/andere Module.
    if target.name in FILES and target.parent.name == 'profile' and target.parent.parent.name == 'daten':
        ensure_ready(target.parent.parent.parent)


@contextmanager
def _lock(root):
    folder = profile_folder(root)
    folder.mkdir(parents=True, exist_ok=True)
    fd = os.open(folder / LOCK, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError('Ungültige Profilsperrdatei.')
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ProfileRecoveryError(_text('writer', 'Eine andere Profiländerung läuft. Es wurde nichts überschrieben.')) from error
        yield folder
    finally:
        os.close(fd)


def _hash(raw):
    return hashlib.sha256(raw).hexdigest() if raw is not None else None


def _encode(raw):
    return base64.b64encode(raw).decode('ascii') if raw is not None else None


def _decode(value):
    if value is None:
        return None
    if not isinstance(value, str) or len(value) > (MAX_FILE_BYTES + 2) // 3 * 4:
        raise ValueError('Ungültige Wiederherstellungsdaten.')
    raw = base64.b64decode(value, validate=True)
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError('Wiederherstellungsdaten sind zu groß.')
    raw.decode('utf-8')
    return raw


def _journal(root):
    raw = read_bytes(root, JOURNAL, MAX_JOURNAL_BYTES)
    if raw is None:
        return None
    from app.profile_management import _unique_object
    data = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_object)
    if not isinstance(data, dict) or set(data) != {'schema', 'root', 'files'} or data['schema'] != 1:
        raise ValueError('Ungültiges Wiederherstellungsjournal.')
    if data['root'] != str(profile_folder(root).parent.parent) or not isinstance(data['files'], dict) or set(data['files']) != set(FILES):
        raise ValueError('Wiederherstellung gehört nicht zu diesem Speicherort.')
    records = {}
    for name, record in data['files'].items():
        if not isinstance(record, dict) or set(record) != {'before', 'after', 'before_sha', 'after_sha'}:
            raise ValueError('Ungültiger Wiederherstellungseintrag.')
        before, after = _decode(record['before']), _decode(record['after'])
        if (_hash(before), _hash(after)) != (record['before_sha'], record['after_sha']):
            raise ValueError('Wiederherstellungsprüfsumme stimmt nicht.')
        records[name] = before, after
    return records


def _publish(folder, name, raw):
    path = folder / name
    if raw is None:
        path.unlink(missing_ok=True)
        _fsync_directory(folder)
    else:
        _write_text(path, raw.decode('utf-8'))


def _recover_locked(root, folder):
    records = _journal(root)
    if records is None:
        return False
    # Erst ALLE Zustände prüfen; fremde Bytes niemals durch ein altes Backup ersetzen.
    current = {name: read_bytes(root, name) for name in FILES}
    if any(current[name] not in pair for name, pair in records.items()):
        raise ValueError('Profilbestand weicht vom gesicherten Vor-/Nachherstand ab.')
    for name, (before, _after) in records.items():
        if current[name] != before:
            _publish(folder, name, before)
    (folder / JOURNAL).unlink()
    _fsync_directory(folder)
    return True


def recover_profile_transaction(root):
    """Nur nach Erwerb des regulären Einzelinstanzschutzes, vor Dashboard-Lesen."""
    path = Path(root) / 'daten' / 'profile' / JOURNAL
    if not path.exists() and not path.is_symlink():
        return False
    try:
        with _lock(root) as folder:
            return _recover_locked(root, folder)
    except Exception as error:
        raise ProfileRecoveryError(_text('recovery_failed', 'Die Profilwiederherstellung konnte nicht abgeschlossen werden. Profile bleiben gesperrt; Journal und vorhandene Dateien wurden zum Prüfen erhalten.')) from error


def write_profile_transaction(root, updates, fingerprints):
    """Übernimmt geprüfte UTF-8-Nachherbytes oder stellt den Vorzustand wieder her."""
    if set(updates) - set(FILES) or len(fingerprints) != len(FILES):
        raise ValueError('Ungültiger Profil-Schreibumfang.')
    with _lock(root) as folder:
        ensure_ready(root)
        before = {name: read_bytes(root, name) for name in FILES}
        if tuple(_hash(before[name]) for name in FILES) != fingerprints:
            raise ValueError(_text('changed', 'Profilbestand geändert. Bitte die Änderung erneut prüfen.'))
        after = {name: updates.get(name, before[name]) for name in FILES}
        for raw in after.values():
            if raw is not None:
                if not isinstance(raw, bytes) or len(raw) > MAX_FILE_BYTES:
                    raise ValueError('Ungültiger Profil-Nachherstand.')
                raw.decode('utf-8')
        payload = {'schema': 1, 'root': str(folder.parent.parent), 'files': {
            name: {'before': _encode(before[name]), 'after': _encode(after[name]),
                   'before_sha': _hash(before[name]), 'after_sha': _hash(after[name])} for name in FILES}}
        # Journal muss vollständig veröffentlicht sein, bevor Bestandsbytes wechseln.
        _write_text(folder / JOURNAL, json.dumps(payload, ensure_ascii=True))
        try:
            if any(read_bytes(root, name) != before[name] for name in FILES):
                raise ValueError('Profilbestand vor dem Schreiben geändert.')
            for name in FILES:
                if after[name] != before[name]:
                    _publish(folder, name, after[name])
            (folder / JOURNAL).unlink()  # Commitpunkt; vorher konservativ zurückrollen.
            _fsync_directory(folder)
        except Exception as error:
            try:
                _recover_locked(root, folder)
            except Exception as recovery_error:
                raise ProfileRecoveryError(_text('rollback_failed', 'Die Profiländerung wurde unterbrochen und konnte noch nicht vollständig zurückgenommen werden. Profile bleiben gesperrt. Bitte neu starten; Journal nicht löschen.')) from recovery_error
            raise error
