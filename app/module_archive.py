"""Einheitliche, streng geprüfte Archive für eigenständige Kreativmodule."""
from __future__ import annotations

import json
from pathlib import Path
from app.atomic_io import atomic_write_json

MAX_BYTES = 10 * 1024 * 1024
MODULES = {'textbausteine', 'buecher', 'ideen', 'konten', 'schnellstarter', 'wiki', 'modulentwuerfe', 'entwicklungspool'}


def text(value, label='Text', *, required=False, limit=200_000):
    if not isinstance(value, str) or '\0' in value or len(value) > limit:
        raise ValueError(f'{label} ist ungültig oder zu lang.')
    if required and not value.strip():
        raise ValueError(f'{label} darf nicht leer sein.')
    return value


def identifier(value):
    value = text(value, 'Kennung', required=True, limit=80)
    if not all(c.isalnum() or c in '_-' for c in value):
        raise ValueError('Ungültige Kennung.')
    return value


def read_json(path):
    # Begrenztes Lesen schützt auch bei einer während des Lesens wachsenden Datei.
    with Path(path).open('rb') as source:
        data = source.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('Datei ist größer als 10 MB. Bitte ein kleineres Archiv wählen.')
    return json.loads(data.decode('utf-8'))


def state_path(root, module):
    if module not in MODULES:
        raise ValueError('Unbekanntes Modul.')
    root = Path(root)
    target = root / 'daten' / module / 'bestand.json'
    if any(path.is_symlink() for path in (root / 'daten', target.parent, target)):
        raise ValueError('Verknüpfte Modulpfade sind nicht zulässig.')
    return target


def load(root, module, validate, empty):
    target = state_path(root, module)
    from app.performance import observe
    area = {'buecher': 'books', 'textbausteine': 'snippets'}.get(module, 'other')
    with observe('archive.load', area):
        return validate(read_json(target)) if target.exists() else validate(empty())


def save(root, module, state, validate):
    clean = validate(state)
    if len(json.dumps(clean, ensure_ascii=False).encode('utf-8')) > MAX_BYTES:
        raise ValueError('Der Modulbestand ist zu groß (höchstens 10 MB).')
    return atomic_write_json(state_path(root, module), clean)


def export_target(root, target):
    """Verhindert, dass eine frei gewählte Exportdatei Arbeitsdaten ersetzt."""
    root, target = Path(root).resolve(), Path(target).resolve()
    protected_dirs = ('daten', 'app', 'texte', 'scripts', 'tests', 'logs', '.git', '.github')
    protected_files = ('MANIFEST.json', 'requirements.txt', 'README.md',
                       'ANLEITUNG_LAIEN.md', 'TODO.md', 'CHANGELOG.md', 'AGENTS.md',
                       'schnellstart.sh', 'kubuntu_abnahme.sh')
    if any(target.is_relative_to(root / folder) for folder in protected_dirs) or target in {
            root / name for name in protected_files}:
        raise ValueError('Export darf interne Projektdateien oder Arbeitsdaten nicht überschreiben. Bitte einen eigenen Exportordner wählen.')
    return target


def export_archive(target, module, state, validate, *, root):
    return atomic_write_json(export_target(root, target), {
        'format': 'provoware.module', 'module': module, 'schema_version': 1,
        'data': validate(state),
    })


def read_archive(source, module, validate):
    raw = read_json(source)
    if (not isinstance(raw, dict) or raw.get('format') != 'provoware.module'
            or raw.get('module') != module or raw.get('schema_version') != 1):
        raise ValueError('Die Datei hat ein falsches Modul oder eine unbekannte Datenversion.')
    return validate(raw.get('data'))
