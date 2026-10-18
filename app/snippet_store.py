"""Textbausteine: unveränderte Inhalte, Varianten, Reihenfolge und Monatszähler."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import re
from uuid import uuid4

from app import module_archive as archive

MODULE = 'textbausteine'
WORKFLOWS = ('Coding', 'Schreiben', 'Prompting', 'Linux')
COLORS = {'Standard': None, 'Blau': '#244a73', 'Grün': '#235a42',
          'Violett': '#553977', 'Rot': '#73353c', 'Orange': '#71471f'}
SIZES = ('Klein', 'Mittel', 'Groß')
PLACEHOLDER = re.compile(r'\{\{([^{}\n]{1,80})\}\}')


def empty_state():
    return {'schema_version': 1, 'workflows': list(WORKFLOWS), 'snippets': []}


def validate(raw):
    if not isinstance(raw, dict) or raw.get('schema_version') != 1:
        raise ValueError('Unbekannte Textbaustein-Datenversion.')
    flows, snippets = raw.get('workflows'), raw.get('snippets')
    if not isinstance(flows, list) or not 1 <= len(flows) <= 100:
        raise ValueError('Workflow-Liste ist ungültig (1–100 Bereiche).')
    for flow in flows:
        archive.text(flow, 'Workflow', required=True, limit=60)
    if len({f.casefold() for f in flows}) != len(flows):
        raise ValueError('Workflows dürfen nicht doppelt vorkommen.')
    if not isinstance(snippets, list) or len(snippets) > 5000:
        raise ValueError('Textbaustein-Liste ist ungültig (höchstens 5000).')
    ids, groups = set(), set()
    for item in snippets:
        if not isinstance(item, dict):
            raise ValueError('Textbaustein ist beschädigt.')
        key = archive.identifier(item.get('id'))
        if key in ids:
            raise ValueError('Doppelte Textbaustein-Kennung.')
        ids.add(key)
        group = archive.identifier(item.get('group'))
        version = item.get('version')
        if type(version) is not int or version < 1 or (group, version) in groups:
            raise ValueError('Varianten müssen eindeutige Versionsnummern haben.')
        groups.add((group, version))
        for field, limit in (('title', 200), ('category', 100), ('content', 200_000)):
            archive.text(item.get(field), field, required=True, limit=limit)
        if item.get('workflow') not in flows or item.get('color') not in COLORS or item.get('size') not in SIZES:
            raise ValueError('Workflow, Farbe oder Größe ist ungültig.')
        monthly = item.get('monthly')
        if not isinstance(monthly, dict):
            raise ValueError('Monatsstatistik ist beschädigt.')
        for month, count in monthly.items():
            if not isinstance(month, str) or not re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', month):
                raise ValueError('Ungültiger Statistikmonat.')
            if type(count) is not int or count < 0:
                raise ValueError('Ungültiger Verwendungszähler.')
    return deepcopy(raw)


def load(root):
    return archive.load(root, MODULE, validate, empty_state)


def save(root, state):
    return archive.save(root, MODULE, state, validate)


def put(root, values, snippet_id=None, variant_of=None):
    state = load(root)
    old = next((s for s in state['snippets'] if s['id'] == snippet_id), None)
    original = next((s for s in state['snippets'] if s['id'] == variant_of), None)
    if snippet_id and old is None or variant_of and original is None:
        raise ValueError('Textbaustein nicht mehr vorhanden. Bitte Liste aktualisieren.')
    key = old['id'] if old else uuid4().hex
    group = old['group'] if old else original['group'] if original else key
    version = old['version'] if old else max(
        (s['version'] for s in state['snippets'] if s['group'] == group), default=0) + 1
    item = {field: values.get(field, '') for field in ('title', 'category', 'content', 'workflow', 'color', 'size')}
    item.update(id=key, group=group, version=version, monthly=old['monthly'] if old else {})
    from app.performance import note_save
    note_save('snippets', old is not None and old == item)
    if old:
        state['snippets'][state['snippets'].index(old)] = item
    else:
        state['snippets'].append(item)
    save(root, state)
    return deepcopy(item)


def add_workflow(root, name):
    state = load(root)
    state['workflows'].append(name.strip())
    save(root, state)


def move(root, key, direction):
    state = load(root)
    item = next(s for s in state['snippets'] if s['id'] == key)
    peers = [i for i, s in enumerate(state['snippets'])
             if s['workflow'] == item['workflow'] and s['category'] == item['category']]
    position = peers.index(state['snippets'].index(item))
    other = position + direction
    if 0 <= other < len(peers):
        a, b = peers[position], peers[other]
        state['snippets'][a], state['snippets'][b] = state['snippets'][b], state['snippets'][a]
        save(root, state)


def placeholders(content):
    return list(dict.fromkeys(PLACEHOLDER.findall(content)))


def render(content, values):
    missing = [key for key in placeholders(content) if key not in values]
    if missing:
        raise ValueError('Bitte alle Platzhalter ausfüllen: ' + ', '.join(missing))
    return PLACEHOLDER.sub(lambda m: values[m.group(1)], content)


def record_copy(root, key, now=None):
    state = load(root)
    item = next(s for s in state['snippets'] if s['id'] == key)
    month = (now or datetime.now().astimezone()).strftime('%Y-%m')
    item['monthly'][month] = item['monthly'].get(month, 0) + 1
    save(root, state)


def import_copies(root, imported):
    imported = validate(imported)
    state = load(root)
    groups = {s['group']: uuid4().hex for s in imported['snippets']}
    for flow in imported['workflows']:
        existing = next((f for f in state['workflows'] if f.casefold() == flow.casefold()), None)
        if existing is None:
            state['workflows'].append(flow)
    for item in imported['snippets']:
        item['id'] = uuid4().hex
        item['group'] = groups[item['group']]
        item['monthly'] = {}  # Import ist keine Verwendung und verdoppelt keine Zähler.
        item['workflow'] = next(f for f in state['workflows'] if f.casefold() == item['workflow'].casefold())
        state['snippets'].append(item)
    save(root, state)
    return len(imported['snippets'])


def monthly_report(state, month):
    rows = [(s, s['monthly'].get(month, 0)) for s in state['snippets']]
    total = sum(count for _, count in rows)
    lines = [f'Textbausteine · {month} · {total} Kopiervorgänge',
             'Gezählt werden Kopiervorgänge in diesem Programm; keine Nutzung in anderen Apps.', '']
    for item, count in sorted(rows, key=lambda row: -row[1]):
        lines.append(f"{count} × {item['workflow']} / {item['category']} / {item['title']} · V{item['version']}")
    return '\n'.join(lines)
