"""Nur unverknüpfte Profile nach aktueller Vorschau kontrolliert entfernen."""
from dataclasses import dataclass
from pathlib import Path
import json

from app.profile_management import _snapshot
from app.profile_store import CATEGORIES, _validate, comparison_key, input_text
from app.profile_file_io import FILES
from app.profile_transaction import write_profile_transaction


def t(key, fallback):
    return input_text('delete.' + key, fallback)


class DeleteError(ValueError):
    """Erwartete Ablehnung, ohne Bestandsänderung."""


@dataclass(frozen=True)
class DeletePlan:
    root: str
    name: str
    fingerprints: tuple[str | None, ...]
    categories: tuple[tuple[str, int], ...]
    extra_fields: tuple[str, ...]
    remaining_profiles: int
    favorite_links: int
    history_links: int

    @property
    def allowed(self):
        return self.remaining_profiles > 0 and not (self.favorite_links or self.history_links)


def _plan(snapshot, name):
    root, profiles, favorites, history, fingerprints, raw_profiles, _raw = snapshot
    if not isinstance(name, str) or name not in profiles or name not in raw_profiles:
        raise DeleteError(t('missing', 'Das gespeicherte Profil ist nicht eindeutig verfügbar. Bitte die Auswahl aktualisieren.'))
    key = comparison_key(name)
    if sum(comparison_key(other) == key for other in profiles) != 1:
        raise DeleteError(t('ambiguous', 'Gleichwertige Profilnamen sind mehrdeutig. Es wird nichts gelöscht.'))
    return DeletePlan(
        str(root), name, fingerprints,
        tuple((category, len(profiles[name][category])) for category in CATEGORIES),
        tuple(field for field in raw_profiles[name] if field not in CATEGORIES),
        len(profiles) - 1,
        sum(comparison_key(other) == key for other in favorites),
        sum(comparison_key(entry['profile']) == key for entry in history),
    )


def preview_profile_delete(root: Path, name: str) -> DeletePlan:
    """Schreibfreie Vorschau; auch leere/gleichwertige Zuordnungen zählen als Bezug."""
    return _plan(_snapshot(root), name)


def delete_profile(root: Path, plan: DeletePlan) -> str:
    """Erfordert den regulären Einzelinstanzschutz; keine abhängigen Inhalte löschen."""
    if not isinstance(plan, DeletePlan):
        raise DeleteError(t('first', 'Bitte das Löschen zuerst prüfen.'))
    snapshot = _snapshot(root)
    current = _plan(snapshot, plan.name)
    if current != plan:
        raise DeleteError(t('changed', 'Bestand oder Speicherort geändert. Bitte erneut prüfen und bestätigen.'))
    if current.favorite_links or current.history_links:
        raise DeleteError(t('references', 'Favoriten oder Verlauf verwenden dieses Profil. Löschen ist zum Schutz der Bezüge gesperrt.'))
    if current.remaining_profiles < 1:
        raise DeleteError(t('last', 'Das letzte Profil bleibt erhalten. Bitte zuerst ein anderes Profil anlegen.'))
    remaining = {name: values for name, values in snapshot[5].items() if name != current.name}
    _validate(remaining)
    raw = (json.dumps(remaining, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    write_profile_transaction(Path(current.root), {FILES[0]: raw}, current.fingerprints)
    return current.name
