"""Validierte lokale Link-Schnellstarter ohne automatischen Netzwerkzugriff."""
from copy import deepcopy
from uuid import uuid4
import sys
from app import module_archive as archive, record_store
from app.account_store import validate_url

MODULE, COLLECTION = 'schnellstarter', 'links'


def validate_record(raw):
    if not isinstance(raw, dict) or set(raw) != {'id', 'name', 'url', 'group', 'icon'}:
        raise ValueError('Der Schnellstarter-Eintrag enthält ungültige Felder.')
    archive.identifier(raw['id'])
    archive.text(raw['name'], 'Name', required=True, limit=80)
    validate_url(raw['url'])
    archive.text(raw['group'], 'Gruppe', limit=60)
    archive.text(raw['icon'], 'Symboltext', limit=3)
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in raw['name'] + raw['group'] + raw['icon']):
        raise ValueError('Steuerzeichen sind in Bezeichnungen nicht erlaubt.')
    return deepcopy(raw)


def validate(raw):
    state = record_store.validate_collection(raw, COLLECTION, validate_record)
    names, urls = set(), set()
    for item in state[COLLECTION]:
        group = item['group'].strip().casefold()
        name_key = (group, item['name'].strip().casefold())
        url_key = (group, item['url'].strip().casefold())
        if name_key in names or url_key in urls:
            raise ValueError('In dieser Gruppe ist der Name oder die Webadresse bereits vorhanden.')
        names.add(name_key)
        urls.add(url_key)
    return state


def load(root):
    return archive.load(root, MODULE, validate, lambda: {'schema_version': 1, COLLECTION: []})


def put(root, record):
    return record_store.put(root, sys.modules[__name__], record)


def remove(root, identifier):
    archive.identifier(identifier)
    state = load(root)
    current = len(state[COLLECTION])
    state[COLLECTION] = [item for item in state[COLLECTION] if item['id'] != identifier]
    if len(state[COLLECTION]) == current:
        return False
    archive.save(root, MODULE, state, validate)
    return True


def import_copies(root, incoming):
    incoming = validate(incoming)
    state = load(root)
    count = 0
    for raw in incoming[COLLECTION]:
        item = deepcopy(raw)
        item['id'] = uuid4().hex
        probe = {**state, COLLECTION: state[COLLECTION] + [item]}
        try:
            validate(probe)
        except ValueError:
            continue  # Identische Namen/Adressen weder überschreiben noch doppeln.
        state = probe
        count += 1
    if count:
        archive.save(root, MODULE, state, validate)
    return count
