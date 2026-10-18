import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from scripts import datensicherung as ds


class DataBackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'daten'
        (self.source / 'texte/.versionen').mkdir(parents=True)
        (self.source / 'texte/.versionen/alt.txt').write_bytes(b'\x00\xff')
        (self.source / 'texte/Grüße.txt').write_text('Persönliche Arbeit', encoding='utf-8')
        self.output = self.root / 'backup'

    def test_roundtrip_hidden_binary_unicode_and_non_overwrite(self):
        archive = ds.create(self.source, self.output)
        second = ds.create(self.source, self.output)
        self.assertNotEqual(archive, second)
        dest = self.root / 'neu'
        ds.restore(archive, dest)
        self.assertEqual(ds.inventory(self.source), ds.inventory(dest / 'daten'))
        before = ds.inventory(dest / 'daten')
        with self.assertRaises(FileExistsError):
            ds.restore(archive, dest)
        self.assertEqual(before, ds.inventory(dest / 'daten'))
        self.assertFalse(list(self.output.glob('.daten*')))
        self.assertEqual(archive.stat().st_mode & 0o777, 0o600)

    def test_bad_sha_rejected_before_destination_created(self):
        archive = ds.create(self.source, self.output)
        archive.write_bytes(archive.read_bytes() + b'damage')
        with self.assertRaises(ValueError):
            ds.restore(archive, self.root / 'neu')
        self.assertFalse((self.root / 'neu').exists())

    def test_missing_checksum_fails_closed(self):
        archive = ds.create(self.source, self.output)
        archive.with_suffix('.zip.sha256').unlink()
        with self.assertRaises(FileNotFoundError):
            ds.restore(archive, self.root / 'neu')

    def test_symlink_source_rejected_without_reading_target(self):
        (self.source / 'link').symlink_to(self.root)
        with self.assertRaises(ValueError):
            ds.create(self.source, self.output)

    def test_backup_inside_source_rejected(self):
        with self.assertRaises(ValueError):
            ds.create(self.source, self.source / 'backups')

    def test_changed_source_not_published(self):
        original = ds.inventory
        calls = 0
        def change(source):
            nonlocal calls
            calls += 1
            if calls == 2:
                (self.source / 'new').write_bytes(b'new')
            return original(source)
        with patch.object(ds, 'inventory', side_effect=change):
            with self.assertRaises(ValueError):
                ds.create(self.source, self.output)
        self.assertEqual(list(self.output.iterdir()), [])

    def malicious_archive(self, names, files=None):
        archive = self.root / 'bad.zip'
        with zipfile.ZipFile(archive, 'w') as handle:
            handle.writestr(ds.INDEX, json.dumps({'schema_version': 1, 'files': files or {}}))
            for name in names:
                handle.writestr(name, b'bad')
        archive.with_suffix('.zip.sha256').write_text(ds.digest(archive))
        return archive

    def test_traversal_absolute_backslash_and_unlisted_files_rejected(self):
        for name in ('../escaped', '/escaped', 'daten/../../escaped', 'daten\\escaped', 'extra'):
            with self.subTest(name=name):
                archive = self.malicious_archive([name])
                with self.assertRaises(ValueError):
                    ds.restore(archive, self.root / 'neu')
                self.assertFalse((self.root / 'neu').exists())

    def test_content_hash_mismatch_cleans_only_new_destination(self):
        archive = self.malicious_archive(['daten/probe'], {'probe': {'size': 3, 'sha256': '0' * 64}})
        with self.assertRaises(ValueError):
            ds.restore(archive, self.root / 'neu')
        self.assertFalse((self.root / 'neu').exists())
        self.assertTrue(self.source.exists())

    def test_size_limit_before_publish(self):
        with patch.object(ds, 'MAX_FILE', 1):
            with self.assertRaises(ValueError):
                ds.create(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_empty_data_roundtrip(self):
        empty = self.root / 'leer'
        empty.mkdir()
        archive = ds.create(empty, self.output)
        ds.restore(archive, self.root / 'neu')
        self.assertEqual(ds.inventory(self.root / 'neu/daten'), {})
