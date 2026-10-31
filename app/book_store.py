"""Bücher mit stabilen Kapitelkennungen und überprüfbarer Hierarchie."""
from __future__ import annotations

from copy import deepcopy
from uuid import uuid4

from app import module_archive as archive

MODULE = 'buecher'
KINDS = ('Leer', 'Hörspiel', 'Satire & Geschichte', 'Sachausarbeitung', 'Tutorial')
TEMPLATES = {
    'Leer': [('Erstes Kapitel', '')],
    'Hörspiel': [('Idee & Besetzung', 'Logline:\nFiguren:\nOrt und Zeit:\n'),
                 ('Szene 1', '[ATMOSPHÄRE: ]\n[GERÄUSCH: ]\nERZÄHLER: \nFIGUR: \n'),
                 ('Finale', 'Auflösung:\nLetztes Klangbild:\n')],
    'Satire & Geschichte': [('Prämisse', 'Worum geht es?\nZiel der Satire:\nPerspektive:\n'),
                           ('Einstieg', 'Figur und Alltag:\nErster Widerspruch:\n'),
                           ('Eskalation', 'Übertreibung:\nUnerwartete Wendung:\n'),
                           ('Pointe', 'Vorbereitung:\nPointe und Nachklang:\n')],
    'Sachausarbeitung': [('Fragestellung', 'Thema:\nLeitfrage:\nAbgrenzung:\n'),
                         ('Grundlagen', 'Begriffe:\nStand des Wissens:\n'),
                         ('Analyse', 'These:\nBeleg:\nGegenargument:\n'),
                         ('Fazit', 'Ergebnis:\nGrenzen:\nAusblick:\n'),
                         ('Quellen', 'Autor – Titel – Jahr – Fundstelle / URL – Abrufdatum\n')],
    'Tutorial': [('Ziel & Voraussetzungen', 'Nach diesem Tutorial kannst du:\nBenötigt werden:\n'),
                 ('Schritt für Schritt', '1. Vorbereitung\n2. Durchführung\n3. Ergebnis prüfen\n'),
                 ('Beispiel', 'Ausgangslage:\nEingabe:\nErwartetes Ergebnis:\n'),
                 ('Fehlerhilfe', 'Problem:\nUrsache:\nLösung:\n'),
                 ('Übung & Checkliste', '☐ Ziel erreicht\n☐ Ergebnis geprüft\nNächste Übung:\n')],
}
ELEMENTS = {
    'Hörspiel': {'Dialog': '\nFIGUR (Sprechweise): \n', 'Geräusch': '\n[GERÄUSCH: Beschreibung]\n',
                 'Musik': '\n[MUSIK: Stimmung, Einsatz, Ausblendung]\n', 'Regie': '\n[REGIE: Handlung / Pause]\n'},
    'Satire & Geschichte': {'Dialog': '\n„“, sagte die Figur.\n', 'Wendung': '\n[WENDUNG: Erwartung und überraschende Umkehr]\n',
                           'Pointe': '\n[POINTE: Vorbereitung → Bruch → Nachklang]\n'},
    'Sachausarbeitung': {'These & Beleg': '\nThese:\nBeleg:\nEinordnung:\n', 'Quelle': '\n[Quelle: Autor, Titel, Jahr, Seite / URL]\n',
                         'Gegenargument': '\nGegenargument:\nAbwägung:\n'},
    'Tutorial': {'Schritt': '\nSchritt: \nSo geht es:\nErwartetes Ergebnis:\n', 'Code': '\n```\nCode hier einfügen\n```\n',
                 'Fehlerhilfe': '\nProblem:\nUrsache:\nLösung:\n'},
    'Leer': {'Notiz': '\n[NOTIZ: ]\n', 'Checkliste': '\n☐ Aufgabe\n☐ Ergebnis prüfen\n'},
}


def new_chapter(title, content='', parent=None):
    return {'id': uuid4().hex, 'parent': parent, 'title': title, 'content': content,
            'notes': '', 'status': 'Entwurf'}


def new_book(kind='Leer'):
    if kind not in KINDS:
        raise ValueError('Unbekannte Buchvorlage.')
    return {'id': uuid4().hex, 'title': '', 'kind': kind, 'audience': '', 'notes': '',
            'chapters': [new_chapter(title, body) for title, body in TEMPLATES[kind]]}


def empty_state():
    return {'schema_version': 1, 'books': []}


def validate_book(book):
    if not isinstance(book, dict) or book.get('kind') not in KINDS:
        raise ValueError('Buchtyp ist ungültig.')
    archive.identifier(book.get('id'))
    for field in ('title', 'audience', 'notes'):
        archive.text(book.get(field), field, required=field == 'title')
    chapters = book.get('chapters')
    if not isinstance(chapters, list) or len(chapters) > 2000:
        raise ValueError('Kapitel-Liste ist ungültig (höchstens 2000).')
    by_id = {}
    for chapter in chapters:
        if not isinstance(chapter, dict):
            raise ValueError('Kapitel ist beschädigt.')
        key = archive.identifier(chapter.get('id'))
        if key in by_id:
            raise ValueError('Kapitelkennungen müssen eindeutig sein.')
        by_id[key] = chapter
        for field in ('title', 'content', 'notes'):
            archive.text(chapter.get(field), field, required=field == 'title')
        if chapter.get('status') not in ('Entwurf', 'Überarbeiten', 'Fertig'):
            raise ValueError('Unbekannter Kapitelstatus.')
    for chapter in chapters:
        parent, seen = chapter.get('parent'), {chapter['id']}
        while parent is not None:
            if (not isinstance(parent, str) or parent not in by_id
                    or parent in seen or len(seen) >= 8):
                raise ValueError('Kapitelstruktur enthält fehlende Eltern, einen Kreis oder mehr als acht Ebenen.')
            seen.add(parent)
            parent = by_id[parent].get('parent')
    return deepcopy(book)


def validate(raw):
    if not isinstance(raw, dict) or raw.get('schema_version') != 1 or not isinstance(raw.get('books'), list):
        raise ValueError('Unbekannte oder beschädigte Buch-Datenversion.')
    if len(raw['books']) > 500:
        raise ValueError('Höchstens 500 Bücher je Bestand.')
    books = [validate_book(book) for book in raw['books']]
    if len({b['id'] for b in books}) != len(books):
        raise ValueError('Doppelte Buchkennungen.')
    return {'schema_version': 1, 'books': books}


def load(root):
    return archive.load(root, MODULE, validate, empty_state)


def put(root, book):
    book = validate_book(book)
    state = load(root)
    index = next((i for i, b in enumerate(state['books']) if b['id'] == book['id']), None)
    from app.performance import note_save
    note_save('books', index is not None and state['books'][index] == book)
    if index is None:
        state['books'].append(book)
    else:
        state['books'][index] = book
    archive.save(root, MODULE, state, validate)
    return book


def copy_book(book):
    copy = deepcopy(book)
    copy['id'] = uuid4().hex
    mapping = {c['id']: uuid4().hex for c in copy['chapters']}
    for chapter in copy['chapters']:
        chapter['id'] = mapping[chapter['id']]
        chapter['parent'] = mapping.get(chapter['parent'])
    return copy


def import_copies(root, imported):
    imported = validate(imported)
    state = load(root)
    state['books'].extend(copy_book(book) for book in imported['books'])
    archive.save(root, MODULE, state, validate)
    return len(imported['books'])


def ordered_chapters(book):
    def visit(parent, level):
        for chapter in book['chapters']:
            if chapter['parent'] == parent:
                yield chapter, level
                yield from visit(chapter['id'], level + 1)
    yield from visit(None, 1)


def manuscript(book, markdown=True):
    book = validate_book(book)
    lines = [('# ' if markdown else '') + book['title'], '']
    for chapter, level in ordered_chapters(book):
        heading = '#' * min(level + 1, 6) + ' ' if markdown else '  ' * (level - 1)
        lines.extend([heading + chapter['title'], '', chapter['content'], ''])
    return '\n'.join(lines)


def move_chapter(book, key, direction):
    item = next(c for c in book['chapters'] if c['id'] == key)
    peers = [i for i, c in enumerate(book['chapters']) if c['parent'] == item['parent']]
    position = peers.index(book['chapters'].index(item))
    other = position + direction
    if 0 <= other < len(peers):
        a, b = peers[position], peers[other]
        book['chapters'][a], book['chapters'][b] = book['chapters'][b], book['chapters'][a]
