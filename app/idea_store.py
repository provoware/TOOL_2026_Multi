"""Textfragmente, Tags und Herkunft; Kompositionen erhalten die Originale."""
from copy import deepcopy
import sys
from app import module_archive as archive
from app import record_store

MODULE, COLLECTION = 'ideen', 'ideas'


def validate_record(raw):
    if not isinstance(raw, dict) or set(raw) != {'id', 'title', 'content', 'tags', 'origin'}:
        raise ValueError('Ungültige Idee.')
    archive.identifier(raw['id'])
    archive.text(raw['title'], 'Titel', required=True, limit=200)
    archive.text(raw['content'], 'Textfragment', required=True)
    archive.text(raw['origin'], 'Herkunft', limit=2000)
    tags = raw['tags']
    if not isinstance(tags, list) or len(tags) > 100:
        raise ValueError('Höchstens 100 Schlagworte.')
    for tag in tags:
        archive.text(tag, 'Schlagwort', required=True, limit=80)
    return deepcopy(raw)


def validate(raw):
    return record_store.validate_collection(raw, COLLECTION, validate_record)


def load(root):
    return archive.load(root, MODULE, validate, lambda: {'schema_version': 1, COLLECTION: []})


def put(root, record):
    return record_store.put(root, sys.modules[__name__], record)


def import_copies(root, raw):
    return record_store.import_copies(root, sys.modules[__name__], raw)
