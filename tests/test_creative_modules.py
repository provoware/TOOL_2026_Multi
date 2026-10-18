"""Geschützte Datenwege und vollständige Modul-Rundreisen in isolierten Ordnern."""
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from app import book_store as books, snippet_store as snippets, module_archive as archive
from app.spelling import check_words


class CreativeModuleTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.values = dict(workflow='Coding', category='Tests', title='Analyse',
                           content='Hallo {{Name}}!\n  Code\n', color='Blau', size='Mittel')

    def tearDown(self):
        self.temp.cleanup()

    def snippet(self, **changes):
        return snippets.put(self.root, {**self.values, **changes})

    def test_loading_empty_modules_has_no_write_side_effect(self):
        self.assertEqual([], snippets.load(self.root)['snippets'])
        self.assertEqual([], books.load(self.root)['books'])
        self.assertEqual([], list(self.root.iterdir()))

    def test_content_is_exact_and_render_does_not_recursively_replace_values(self):
        item = self.snippet()
        self.assertEqual(self.values['content'], snippets.load(self.root)['snippets'][0]['content'])
        self.assertEqual('Hallo {{Other}}!\n  Code\n', snippets.render(item['content'], {'Name': '{{Other}}'}))
        with self.assertRaises(ValueError):
            snippets.render(item['content'], {})
        self.assertEqual(['Name'], snippets.placeholders('{{Name}} {{Name}}'))

    def test_variants_keep_original_and_number_monotonically(self):
        first = self.snippet()
        variant = snippets.put(self.root, {**self.values, 'content': 'Neu'}, variant_of=first['id'])
        self.assertEqual(first['group'], variant['group'])
        self.assertEqual(2, variant['version'])
        self.assertEqual(first, snippets.load(self.root)['snippets'][0])
        self.assertNotEqual(first['id'], variant['id'])

    def test_month_statistics_and_edit_preservation(self):
        item = self.snippet()
        snippets.record_copy(self.root, item['id'], datetime(2026, 10, 1))
        snippets.record_copy(self.root, item['id'], datetime(2026, 11, 1))
        snippets.record_copy(self.root, item['id'], datetime(2026, 10, 31))
        edited = snippets.put(self.root, {**self.values, 'title': 'Umbenannt'}, item['id'])
        self.assertEqual({'2026-10': 2, '2026-11': 1}, edited['monthly'])
        report = snippets.monthly_report(snippets.load(self.root), '2026-10')
        self.assertIn('2 Kopiervorgänge', report)
        self.assertIn('Umbenannt', report)

    def test_workflow_validation_and_category_order(self):
        snippets.add_workflow(self.root, 'Recherche')
        with self.assertRaises(ValueError):
            snippets.add_workflow(self.root, 'coding')
        a, b = self.snippet(), self.snippet(title='Zweiter')
        snippets.move(self.root, b['id'], -1)
        self.assertEqual([b['id'], a['id']], [s['id'] for s in snippets.load(self.root)['snippets']])

    def test_snippet_archive_import_remaps_groups_and_resets_counters(self):
        first = self.snippet()
        snippets.put(self.root, self.values, variant_of=first['id'])
        snippets.record_copy(self.root, first['id'])
        before = snippets.load(self.root)
        path = self.root / 'export.json'
        archive.export_archive(path, snippets.MODULE, before, snippets.validate, root=self.root)
        data = archive.read_archive(path, snippets.MODULE, snippets.validate)
        self.assertEqual(2, snippets.import_copies(self.root, data))
        items = snippets.load(self.root)['snippets']
        self.assertEqual(4, len({s['id'] for s in items}))
        self.assertEqual(items[2]['group'], items[3]['group'])
        self.assertNotEqual(items[0]['group'], items[2]['group'])
        self.assertEqual({}, items[2]['monthly'])
        self.assertEqual(before, {'schema_version': 1, 'workflows': snippets.load(self.root)['workflows'], 'snippets': items[:2]})
        with self.assertRaises(ValueError):
            archive.read_archive(path, books.MODULE, books.validate)

    def test_invalid_or_failed_save_leaves_bytes_unchanged(self):
        self.snippet()
        target = archive.state_path(self.root, snippets.MODULE)
        before = target.read_bytes()
        with self.assertRaises(ValueError):
            self.snippet(size='Riesig')
        with patch('app.module_archive.atomic_write_json', side_effect=OSError('voll')):
            with self.assertRaises(OSError):
                self.snippet(title='Nicht gespeichert')
        self.assertEqual(before, target.read_bytes())
        state = snippets.load(self.root)
        state['snippets'][0]['monthly'] = {'2026-99': -1}
        with self.assertRaises(ValueError):
            snippets.import_copies(self.root, state)
        self.assertEqual(before, target.read_bytes())

    def test_export_cannot_replace_internal_data_even_via_symlink(self):
        self.snippet()
        target = archive.state_path(self.root, snippets.MODULE)
        original = target.read_bytes()
        with self.assertRaises(ValueError):
            archive.export_archive(target, snippets.MODULE, snippets.load(self.root), snippets.validate, root=self.root)
        alias = self.root / 'alias.json'
        alias.symlink_to(target)
        with self.assertRaises(ValueError):
            archive.export_target(self.root, alias)
        with self.assertRaises(ValueError):
            archive.export_target(self.root, self.root / 'MANIFEST.json')
        self.assertEqual(original, target.read_bytes())

    def test_archive_size_and_schema_limits(self):
        path = self.root / 'large.json'
        path.write_bytes(b' ' * (archive.MAX_BYTES + 1))
        with self.assertRaises(ValueError):
            archive.read_json(path)
        path.write_text('{"format":"provoware.module","module":"buecher","schema_version":2}')
        with self.assertRaises(ValueError):
            archive.read_archive(path, books.MODULE, books.validate)

    def book(self, kind='Hörspiel'):
        book = books.new_book(kind)
        book['title'] = 'Mein Buch'
        return book

    def test_all_templates_validate_and_export_without_private_notes(self):
        for kind in books.KINDS:
            book = self.book(kind)
            book['notes'] = 'PRIVATE RECHERCHE'
            book['chapters'][0]['notes'] = 'PRIVATE KAPITELNOTIZ'
            saved = books.put(self.root, book)
            text = books.manuscript(saved)
            self.assertIn('# Mein Buch', text)
            self.assertNotIn('PRIVATE', text)
        self.assertEqual(5, len(books.load(self.root)['books']))

    def test_hierarchy_order_copy_and_roundtrip(self):
        book = self.book()
        parent = book['chapters'][0]['id']
        child = books.new_chapter('Unterkapitel', 'Inhalt', parent)
        book['chapters'].append(child)
        books.move_chapter(book, book['chapters'][1]['id'], -1)
        saved = books.put(self.root, book)
        path = self.root / 'books.json'
        archive.export_archive(path, books.MODULE, books.load(self.root), books.validate, root=self.root)
        books.import_copies(self.root, archive.read_archive(path, books.MODULE, books.validate))
        original, copied = books.load(self.root)['books']
        self.assertEqual(saved, original)
        self.assertNotEqual(original['id'], copied['id'])
        self.assertEqual(books.manuscript(original), books.manuscript(copied))
        self.assertTrue({c['id'] for c in original['chapters']}.isdisjoint(c['id'] for c in copied['chapters']))
        self.assertIn('### Unterkapitel', books.manuscript(copied))

    def test_corrupt_hierarchies_never_replace_saved_books(self):
        book = books.put(self.root, self.book())
        target = archive.state_path(self.root, books.MODULE)
        before = target.read_bytes()
        for parent in (book['chapters'][0]['id'], 'missing'):
            corrupt = deepcopy(book)
            corrupt['chapters'][0]['parent'] = parent
            with self.assertRaises(ValueError):
                books.put(self.root, corrupt)
        corrupt = deepcopy(book)
        corrupt['chapters'][1]['id'] = corrupt['chapters'][0]['id']
        with self.assertRaises(ValueError):
            books.put(self.root, corrupt)
        self.assertEqual(before, target.read_bytes())

    def test_optional_spellcheck_missing_and_timeout(self):
        with patch('app.spelling.shutil.which', return_value=None):
            with self.assertRaisesRegex(ValueError, 'aspell'):
                check_words('Text')
        with patch('app.spelling.shutil.which', return_value='/usr/bin/aspell'), patch(
                'app.spelling.subprocess.run', side_effect=subprocess.TimeoutExpired('aspell', 5)):
            with self.assertRaises(subprocess.TimeoutExpired):
                check_words('Text')
