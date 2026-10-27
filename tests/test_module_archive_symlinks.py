"""Modulbestände dürfen weder über Datei- noch über Ordnerlinks ausweichen."""

import tempfile
import unittest
from pathlib import Path

from app import module_archive as archive


class ModuleArchiveSymlinkTests(unittest.TestCase):
    def test_regular_and_missing_archive_paths_stay_allowed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / 'daten' / 'ideen' / 'bestand.json'
            self.assertEqual(archive.state_path(root, 'ideen'), target)
            target.parent.mkdir(parents=True)
            target.write_text('{}', encoding='utf-8')
            self.assertEqual(archive.state_path(root, 'ideen'), target)

    def test_broken_archive_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / 'daten' / 'ideen' / 'bestand.json'
            target.parent.mkdir(parents=True)
            target.symlink_to(root / 'missing.json')
            self.assertFalse(target.exists())
            with self.assertRaisesRegex(ValueError, 'Verknüpf'):
                archive.state_path(root, 'ideen')
            self.assertTrue(target.is_symlink())

    def test_existing_archive_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            original = root / 'external.json'
            original.write_text('{"important": true}', encoding='utf-8')
            target = root / 'daten' / 'ideen' / 'bestand.json'
            target.parent.mkdir(parents=True)
            target.symlink_to(original)
            with self.assertRaisesRegex(ValueError, 'Verknüpf'):
                archive.state_path(root, 'ideen')
            self.assertEqual(original.read_text(encoding='utf-8'), '{"important": true}')

    def test_linked_data_or_module_folder_is_rejected(self):
        for linked in ('daten', 'ideen'):
            with self.subTest(linked=linked), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                external = root / 'external'
                external.mkdir()
                if linked == 'daten':
                    (root / 'daten').symlink_to(external, target_is_directory=True)
                else:
                    (root / 'daten').mkdir()
                    (root / 'daten' / 'ideen').symlink_to(external, target_is_directory=True)
                with self.assertRaisesRegex(ValueError, 'Verknüpf'):
                    archive.state_path(root, 'ideen')
                self.assertEqual(list(external.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
