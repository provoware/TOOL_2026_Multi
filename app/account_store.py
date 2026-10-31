"""Kontometadaten ohne Passwortfeld oder Zugangsdaten-URL; kein Geheimnistresor."""
from copy import deepcopy
import re
import sys
from urllib.parse import urlsplit, parse_qsl
from app import module_archive as archive
from app import record_store

MODULE, COLLECTION = 'konten', 'accounts'
SECRET_NAMES = ('password', 'passwort', 'token', 'secret', 'apikey', 'pin', 'totp',
                'privatekey', 'seed', 'recoverycode', 'wiederherstellungscode')


def secret_name(name):
    compact = re.sub(r'[^a-z0-9]', '', name.casefold())
    return any((compact.startswith('pin') or compact.endswith('pin')) if word == 'pin'
               else word in compact for word in SECRET_NAMES)


def validate_url(raw):
    archive.text(raw, 'Webadresse', required=True, limit=2048)
    parsed = urlsplit(raw)
    if (parsed.scheme not in ('https', 'http') or not parsed.hostname
            or parsed.username is not None or parsed.password is not None
            or any(ord(c) < 33 or ord(c) == 127 for c in raw)
            or any(secret_name(key) for key, _value in (parse_qsl(parsed.query) + parse_qsl(parsed.fragment)))):
        raise ValueError('Bitte eine http(s)-Webadresse ohne Zugangsdaten oder Geheimnisparameter verwenden.')
    try:
        parsed.port
    except ValueError as error:
        raise ValueError('Die Webadresse enthält einen ungültigen Port.') from error
    return raw


def validate_record(raw):
    fields = {'id', 'url', 'name', 'email', 'hint', 'notes', 'group', 'custom'}
    if not isinstance(raw, dict) or set(raw) != fields:
        raise ValueError('Kontoeintrag enthält unbekannte Felder; Passwortfelder sind nicht erlaubt.')
    archive.identifier(raw['id'])
    validate_url(raw['url'])
    for key, limit in (('name',200), ('email',320), ('hint',200), ('notes',10000), ('group',80)):
        archive.text(raw[key], key, limit=limit)
    email = raw['email']
    if email and (email.count('@') != 1 or any(c.isspace() for c in email) or email.startswith('@') or email.endswith('@')):
        raise ValueError('Bitte die E-Mail-Adresse prüfen oder leer lassen.')
    custom = raw['custom']
    if not isinstance(custom, dict) or len(custom) > 30:
        raise ValueError('Höchstens 30 zusätzliche Textfelder.')
    for name, value in custom.items():
        archive.text(name, 'Feldname', required=True, limit=80)
        archive.text(value, 'Feldinhalt', limit=1000)
        if secret_name(name):
            raise ValueError('Zusatzfelder dürfen keine Passwörter, Tokens, PINs oder Schlüssel aufnehmen.')
    return deepcopy(raw)


def validate(raw):
    return record_store.validate_collection(raw, COLLECTION, validate_record)


def load(root):
    return archive.load(root, MODULE, validate, lambda: {'schema_version':1, COLLECTION:[]})


def put(root, record):
    return record_store.put(root, sys.modules[__name__], record)


def import_copies(root, raw):
    return record_store.import_copies(root, sys.modules[__name__], raw)
