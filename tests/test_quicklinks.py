"""Daten- und Schutzprüfungen des Link-Schnellstarters."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from app import quicklinks_store as store


def item(name='Suno', url='https://suno.com', group='Musik'):
    return {'id': 'link1', 'name': name, 'url': url, 'group': group, 'icon': '♫'}


class QuicklinksStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_add_validate_duplicates_and_remove(self):
        store.put(self.root, item())
        self.assertEqual(len(store.load(self.root)['links']), 1)
        with self.assertRaises(ValueError):
            store.put(self.root, {**item('Anderer Name'), 'id': 'link2'})
        with self.assertRaises(ValueError):
            store.put(self.root, {**item('Datei', 'file:///tmp/private'), 'id': 'link3'})
        with self.assertRaises(ValueError):
            store.put(self.root, {**item('Falsch', 'https://site.org/?token=abc'), 'id': 'link4'})
        self.assertFalse(store.remove(self.root, 'missing'))
        self.assertTrue(store.remove(self.root, 'link1'))
        self.assertEqual(store.load(self.root)['links'], [])

    def test_import_copies_skips_duplicates_without_overwrite(self):
        store.put(self.root, item())
        incoming = {'schema_version': 1, 'links': [item('YouTube', 'https://youtube.com', 'Video')]}
        self.assertEqual(store.import_copies(self.root, incoming), 1)
        self.assertEqual(store.import_copies(self.root, incoming), 0)
        self.assertEqual(len(store.load(self.root)['links']), 2)
        self.assertEqual(store.load(self.root)['links'][0], item())

    def test_failed_write_preserves_saved_entry(self):
        store.put(self.root, item())
        before = store.load(self.root)
        with patch('app.module_archive.atomic_write_json', side_effect=OSError('Datenträger voll')):
            with self.assertRaises(OSError):
                store.put(self.root, {**item(), 'name': 'Geändert'})
        self.assertEqual(before, store.load(self.root))

    def test_labels_reject_del_without_changing_saved_links(self):
        store.put(self.root, item())
        before = store.load(self.root)
        for field in ('name', 'group', 'icon'):
            with self.subTest(field=field):
                bad = {**item(), 'id': 'invalid_' + field,
                       field: item()[field] + '\x7f'}
                with self.assertRaisesRegex(ValueError, 'Steuerzeichen'):
                    store.put(self.root, bad)
                self.assertEqual(store.load(self.root), before)
        store.put(self.root, {**item('Andere Seite', 'https://example.org'),
                                   'id': 'link2'})
        self.assertEqual(len(store.load(self.root)['links']), 2)
