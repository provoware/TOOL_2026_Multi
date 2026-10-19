import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from app.data_search import DataSearch


class DataSearchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = self.root / 'daten'
        self.data.mkdir()

    def search(self, query, **kwargs):
        scan = DataSearch(self.root, query, **kwargs)
        list(scan.batches())
        return scan.result

    def test_unicode_filename_and_literal_text_and_unchanged_bytes(self):
        file = self.data / 'Straße.txt'
        raw = 'Erste Zeile\nGRÜSSE [x].\nStraße\n'.encode('utf-8')
        file.write_bytes(raw)
        result = self.search('STRASSE')
        self.assertEqual([(h['path'], h['line']) for h in result.hits], [('Straße.txt', 0), ('Straße.txt', 3)])
        self.assertEqual(self.search('[x].').hits[0]['line'], 2)
        self.assertEqual(file.read_bytes(), raw)
        self.assertEqual(list(self.root.iterdir()), [self.data])
        self.assertEqual(result.reason, 'done')

    def test_names_and_contents_are_independently_selectable(self):
        (self.data / 'titel.txt').write_text('inhalt')
        self.assertFalse(self.search('titel', names=False).hits)
        self.assertFalse(self.search('inhalt', contents=False).hits)
        self.assertEqual(len(self.search('titel', contents=False).hits), 1)

    def test_links_special_hidden_and_external_content_not_read(self):
        external = self.root / 'secret.txt'
        external.write_text('geheim')
        (self.data / 'link.txt').symlink_to(external)
        (self.data / 'linked-dir').symlink_to(self.root, target_is_directory=True)
        (self.data / '.versionen').mkdir()
        (self.data / '.versionen/alt.txt').write_text('geheim')
        (self.data / '.hidden.txt').write_text('geheim')
        self.assertEqual(self.search('geheim').hits, [])
        (self.data / 'link.txt').unlink()
        (self.data / 'linked-dir').unlink()
        import os
        os.mkfifo(self.data / 'pipe.txt')
        self.assertEqual(self.search('geheim').hits, [])

    def test_symlink_data_root_rejected(self):
        self.data.rmdir()
        self.data.symlink_to(self.root)
        with self.assertRaises(ValueError):
            self.search('secret')

    def test_hit_limit_reported_even_for_last_file(self):
        (self.data / 'probe.txt').write_text('match\n' * 300)
        result = self.search('match', names=False)
        self.assertEqual(len(result.hits), 200)
        self.assertEqual(result.reason, 'limit')

    def test_large_binary_invalid_utf8_are_skipped(self):
        (self.data / 'gross.txt').write_bytes(b'x' * (1024 * 1024 + 1))
        (self.data / 'binary.txt').write_bytes(b'x\0xx')
        (self.data / 'invalid.txt').write_bytes(b'\xff')
        result = self.search('x', names=False)
        self.assertEqual(result.hits, [])
        self.assertEqual(result.skipped, 3)

    def test_cancel_time_and_entry_limits(self):
        self.assertEqual(self.search('x', cancelled=lambda: True).reason, 'cancelled')
        with patch('app.data_search.MAX_SECONDS', 0):
            self.assertEqual(self.search('x').reason, 'time')
        (self.data / 'probe.txt').write_text('x')
        with patch('app.data_search.MAX_ENTRIES', 1):
            self.assertEqual(self.search('x').reason, 'limit')
        with patch('app.data_search.MAX_BYTES', 1):
            self.assertEqual(self.search('x', names=False).reason, 'done')
            (self.data / 'zweite.txt').write_text('xxx')
            self.assertEqual(self.search('x', names=False).reason, 'limit')

    def test_invalid_request_and_missing_root(self):
        for query in ('', ' ', 'x' * 201):
            with self.assertRaises(ValueError):
                DataSearch(self.root, query)
        with self.assertRaises(ValueError):
            DataSearch(self.root, 'x', names=False, contents=False)
        self.data.rmdir()
        self.assertEqual(self.search('x').reason, 'missing')
