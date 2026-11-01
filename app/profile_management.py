"""Profilnamen mit bewusster Bezugsvorschau und geprüftem Lesestand ändern."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from app.profile_store import DEFAULT_PROFILES, _clean_profile_name, _validate, comparison_key, input_text
from app.atomic_io import atomic_write_json
from app.profile_file_io import FILES, read_bytes
from app.profile_transaction import ensure_ready, write_profile_transaction, ProfileRecoveryError
from app.genre_favorites import validate_favorites
from app.genre_random import _history_validate

MAX_RENAME_FILE_BYTES = 16 * 1024 * 1024


def t(key, fallback):
    return input_text('rename.' + key, fallback)


class RenameError(ValueError):
    """Erwartete sichere Ablehnung, ohne Änderungen am Bestand."""


class ProfileAccessError(RuntimeError):
    """Unerwarteter oder nicht sicher lesbarer Bestand; im UI protokollieren."""


@dataclass(frozen=True)
class RenamePlan:
    root: str
    old_name: str
    new_name: str
    fingerprints: tuple[str | None, ...]
    favorite_links: int
    history_links: int
    value_count: int
    transfer_links: bool = False
    unsafe_links: int = 0

    @property
    def allowed(self):
        return not self.unsafe_links and (self.transfer_links or not (self.favorite_links or self.history_links))


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(t('json_duplicate', 'Die Datei enthält doppelte JSON-Schlüssel; die Umbenennung ist gesperrt.'))
        result[key] = value
    return result


def _read_file(root, name, default):
    raw = read_bytes(root, name, MAX_RENAME_FILE_BYTES)
    if raw is None:
        return copy.deepcopy(default), None
    return json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_object), hashlib.sha256(raw).hexdigest()


def _snapshot(root):
    root = Path(os.path.abspath(root))
    try:
        ensure_ready(root)
        if root.resolve() != root:
            raise ProfileAccessError(t('links', 'Profilpfade dürfen für diese Änderung keine Verknüpfungen enthalten.'))
        defaults = (DEFAULT_PROFILES, {'schema': 1, 'favorites': {}}, [])
        records = [_read_file(root, name, default) for name, default in zip(FILES, defaults)]
        profiles = _validate(records[0][0])
        favorites = validate_favorites(records[1][0])
        history = _history_validate(records[2][0])
        return root, profiles, favorites, history, tuple(record[1] for record in records), records[0][0], [record[0] for record in records]
    except (ProfileAccessError, ProfileRecoveryError):
        raise
    except (OSError, ValueError, TypeError, RuntimeError) as error:
        raise ProfileAccessError(t('read', 'Profilbestand oder Verknüpfungen konnten nicht sicher gelesen werden.')) from error


def _plan(snapshot, old_name, new_name, transfer_links=False):
    root, profiles, favorites, history, fingerprints, raw_profiles, _raw_records = snapshot
    if not isinstance(old_name, str) or old_name not in profiles:
        raise RenameError(t('old_missing', 'Das ausgewählte Profil wurde nicht gefunden. Bitte die Auswahl aktualisieren.'))
    if old_name not in raw_profiles:
        raise RenameError(t('legacy_name', 'Der gespeicherte Profilname enthält abweichenden Leerraum. Eine automatische Bereinigung ist gesperrt.'))
    if not isinstance(new_name, str):
        raise RenameError(t('name_type', 'Bitte einen neuen Profilnamen als Text eingeben.'))
    try:
        new_name = unicodedata.normalize('NFC', _clean_profile_name(new_name))
    except ValueError as error:
        raise RenameError(str(error)) from error
    old_key, new_key = comparison_key(old_name), comparison_key(new_name)
    if sum(comparison_key(name) == old_key for name in profiles) != 1:
        raise RenameError(t('ambiguous', 'Gleichwertige alte Profilnamen sind mehrdeutig. Es wurde nichts geändert.'))
    if old_name == new_name:
        raise RenameError(t('same', 'Bitte einen anderen Profilnamen eingeben.'))
    if any(name != old_name and comparison_key(name) == new_key for name in profiles):
        raise RenameError(t('duplicate', 'Ein gleichwertiger Profilname ist bereits vorhanden. Profile werden nicht zusammengeführt.'))
    keys = {old_key, new_key}
    try:
        favorite_links = sum(comparison_key(name) in keys for name in favorites)
        history_links = sum(comparison_key(entry['profile']) in keys for entry in history)
    except ValueError as error:
        raise ProfileAccessError(t('references', 'Verknüpfte Profilnamen konnten nicht eindeutig geprüft werden.')) from error
    references = list(favorites) + [entry['profile'] for entry in history]
    unsafe_links = sum(comparison_key(name) in keys and name != old_name for name in references)
    return RenamePlan(str(root), old_name, new_name, fingerprints, favorite_links,
                      history_links, sum(len(values) for values in profiles[old_name].values()), bool(transfer_links), unsafe_links)


def preview_profile_rename(root: Path, old_name: str, new_name: str, *, transfer_links: bool = False) -> RenamePlan:
    """Schreibfreie Vorschau inklusive alter und neuer Favoriten-/Verlaufsbezüge."""
    return _plan(_snapshot(root), old_name, new_name, transfer_links)


def rename_profile(root: Path, plan: RenamePlan) -> str:
    """Geprüfte Umbenennung; Aufrufer benötigt den regulären Einzelinstanzschutz."""
    if not isinstance(plan, RenamePlan):
        raise RenameError(t('plan', 'Bitte die Umbenennung zuerst prüfen.'))
    snapshot = _snapshot(root)
    current = _plan(snapshot, plan.old_name, plan.new_name, plan.transfer_links)
    if current != plan:
        raise RenameError(t('changed', 'Bestand oder Speicherort geändert. Bitte erneut prüfen.'))
    if not current.allowed:
        raise RenameError(t('blocked', 'Favoriten oder Verlauf verwenden den alten oder neuen Namen. Die Umbenennung ist zum Schutz dieser Verknüpfungen gesperrt.'))
    profiles = {(plan.new_name if name == plan.old_name else name): values
                for name, values in snapshot[5].items()}
    _validate(profiles)
    if plan.transfer_links and (plan.favorite_links or plan.history_links):
        _write_linked(snapshot, plan, profiles)
    else:
        atomic_write_json(Path(current.root) / 'daten' / 'profile' / FILES[0], profiles)
    return current.new_name


def _write_linked(snapshot, plan, profiles):
    raw = copy.deepcopy(snapshot[6])
    raw[0] = profiles
    favorites = raw[1]['favorites']
    if plan.old_name in favorites:
        favorites[plan.new_name] = favorites.pop(plan.old_name)
    for entry in raw[2]:
        if entry['profile'] == plan.old_name:
            entry['profile'] = plan.new_name
    changed = {FILES[0]}
    if plan.old_name in snapshot[6][1]['favorites']:
        changed.add(FILES[1])
    if any(entry['profile'] == plan.old_name for entry in snapshot[6][2]):
        changed.add(FILES[2])
    updates = {name: (json.dumps(payload, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
               for name, payload in zip(FILES, raw) if name in changed}
    write_profile_transaction(Path(plan.root), updates, plan.fingerprints)
