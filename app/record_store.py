"""Gemeinsame atomare Ablage einfacher eigenständiger Moduldatensätze."""
from copy import deepcopy
from uuid import uuid4
from app import module_archive as archive


def validate_collection(raw, collection, validate_record):
    if not isinstance(raw, dict) or set(raw) != {'schema_version', collection} or raw['schema_version'] != 1:
        raise ValueError('Unbekannter oder beschädigter Modulbestand.')
    records = raw[collection]
    if not isinstance(records, list) or len(records) > 2000:
        raise ValueError('Höchstens 2000 Einträge pro Modul.')
    clean = [validate_record(item) for item in records]
    if len({item['id'] for item in clean}) != len(clean):
        raise ValueError('Eintragskennungen müssen eindeutig sein.')
    return {'schema_version': 1, collection: clean}


def put(root, store, record):
    record = store.validate_record(record)
    state = store.load(root)
    records = state[store.COLLECTION]
    index = next((i for i, item in enumerate(records) if item['id'] == record['id']), None)
    if index is None:
        records.append(record)
    else:
        records[index] = record
    archive.save(root, store.MODULE, state, store.validate)
    return record


def import_copies(root, store, imported):
    imported = store.validate(imported)
    state = store.load(root)
    for record in imported[store.COLLECTION]:
        record = deepcopy(record)
        record['id'] = uuid4().hex
        state[store.COLLECTION].append(record)
    archive.save(root, store.MODULE, state, store.validate)
    return len(imported[store.COLLECTION])
