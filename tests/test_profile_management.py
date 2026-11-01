"""Umbenennung schützt Rohbestand, Namensbezüge und geprüften Lesestand."""
import json
import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from app.profile_management import (
    FILES, ProfileAccessError, RenameError, preview_profile_rename, rename_profile,
)
from app.profile_store import CATEGORIES


class ProfileManagementTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / 'daten' / 'profile'
        self.folder.mkdir(parents=True)
        self.raw = {'Test': {'Genres': ['  Du\u0308ster  '], 'Zusatz': {'roh': 7}}, 'Anderes': {}}
        self.write(0, self.raw)
        self.before = (self.folder / FILES[0]).read_bytes()

    def write(self, index, data):
        path = self.folder / FILES[index]
        path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        return path

    def history(self, name):
        return [{'timestamp': '2026-11-01', 'profile': name, 'output': 'historisch',
                 'amounts': {cat: int(cat == 'Genres') for cat in CATEGORIES}}]

    def test_preview_writes_nothing_and_rename_preserves_all_raw_fields(self):
        plan = preview_profile_rename(self.root, 'Test', ' Neu  benannt ')
        self.assertTrue(plan.allowed)
        self.assertEqual(plan.value_count, 1)
        self.assertEqual((self.folder / FILES[0]).read_bytes(), self.before)
        self.assertEqual(rename_profile(self.root, plan), 'Neu benannt')
        raw = json.loads((self.folder / FILES[0]).read_text())
        self.assertEqual(raw, {'Neu benannt': self.raw['Test'], 'Anderes': {}})
        self.assertFalse((self.folder / FILES[1]).exists())
        self.assertFalse((self.folder / FILES[2]).exists())

    def test_defaults_preview_creates_no_files(self):
        (self.folder / FILES[0]).unlink()
        self.assertTrue(preview_profile_rename(self.root, 'HardTechno', 'Neu').allowed)
        self.assertEqual(list(self.folder.iterdir()), [])

    def test_old_and_target_references_block_including_empty_associations(self):
        for name in (' test ', 'NEU', 'Ne\u0308u'):
            with self.subTest(name=name):
                self.write(1, {'schema': 1, 'favorites': {name: {cat: [] for cat in CATEGORIES}}})
                target = 'Nëu' if name == 'Ne\u0308u' else 'Neu'
                plan = preview_profile_rename(self.root, 'Test', target)
                self.assertEqual(plan.favorite_links, 1)
                self.assertFalse(plan.allowed)
                with self.assertRaises(RenameError):
                    rename_profile(self.root, plan)
                self.assertEqual((self.folder / FILES[0]).read_bytes(), self.before)
        (self.folder / FILES[1]).unlink()
        for name in ('TEST', ' neu '):
            self.write(2, self.history(name))
            plan = preview_profile_rename(self.root, 'Test', 'Neu')
            self.assertEqual(plan.history_links, 1)
            with self.assertRaises(RenameError):
                rename_profile(self.root, plan)

    def test_unrelated_metadata_remains_byte_identical(self):
        paths = [self.write(1, {'schema': 1, 'favorites': {'Anderes': {cat: [] for cat in CATEGORIES}}}),
                 self.write(2, self.history('Anderes'))]
        before = [p.read_bytes() for p in paths]
        rename_profile(self.root, preview_profile_rename(self.root, 'Test', 'Neu'))
        self.assertEqual([p.read_bytes() for p in paths], before)

    def test_changed_snapshot_add_remove_and_root_or_forged_plan_refused(self):
        for index, payload in ((0, self.raw), (1, {'schema': 1, 'favorites': {}}), (2, [])):
            with self.subTest(index=index):
                plan = preview_profile_rename(self.root, 'Test', 'Neu')
                path = self.write(index, payload)
                path.write_bytes(path.read_bytes() + b' ')
                with self.assertRaises(RenameError):
                    rename_profile(self.root, plan)
        plan = preview_profile_rename(self.root, 'Test', 'Neu')
        for altered in (replace(plan, root='/different'), replace(plan, value_count=999)):
            with self.assertRaises(RenameError):
                rename_profile(self.root, altered)
        (self.folder / FILES[2]).unlink()
        with self.assertRaises(RenameError):
            rename_profile(self.root, plan)
        with self.assertRaises(RenameError):
            rename_profile(self.root, None)

    def test_name_validation_unicode_collisions_and_case_only(self):
        for old, new in (('missing', 'Neu'), ('Test', 'Test'), ('Test', 'anderes'),
                         ('Test', ''), ('Test', 'bad\nname'), ('Test', None)):
            with self.subTest(old=old, new=new), self.assertRaises(RenameError):
                preview_profile_rename(self.root, old, new)
        plan = preview_profile_rename(self.root, 'Test', 'TEST')
        self.assertTrue(plan.allowed)
        self.write(0, {'Ä': {}, 'Anderes': {}})
        self.assertEqual(preview_profile_rename(self.root, 'Ä', 'A\u0308 neu').new_name, 'Ä neu')
        self.write(0, {'Ä': {}, 'A\u0308': {}})
        with self.assertRaises(RenameError):
            preview_profile_rename(self.root, 'Ä', 'Neu')
        self.write(0, {' Test ': {}})
        with self.assertRaises(RenameError):
            preview_profile_rename(self.root, 'Test', 'Neu')

    def test_corrupt_files_fail_closed(self):
        for index in range(3):
            for raw in (b'{', b'null', b'\xff', b'{"Test":{},"Test":{}}'):
                with self.subTest(index=index, raw=raw):
                    path = self.folder / FILES[index]
                    saved = path.read_bytes() if path.exists() else None
                    path.write_bytes(raw)
                    with self.assertRaises(ProfileAccessError):
                        preview_profile_rename(self.root, 'Test', 'Neu')
                    if saved is None:
                        path.unlink()
                    else:
                        path.write_bytes(saved)
        self.assertEqual((self.folder / FILES[0]).read_bytes(), self.before)

    def test_links_directories_fifo_and_oversize_fail_closed(self):
        path = self.folder / FILES[1]
        for target in (self.folder / 'missing', self.folder / FILES[0]):
            path.symlink_to(target)
            with self.assertRaises(ProfileAccessError):
                preview_profile_rename(self.root, 'Test', 'Neu')
            path.unlink()
        path.mkdir()
        with self.assertRaises(ProfileAccessError):
            preview_profile_rename(self.root, 'Test', 'Neu')
        path.rmdir()
        os.mkfifo(path)
        with self.assertRaises(ProfileAccessError):
            preview_profile_rename(self.root, 'Test', 'Neu')
        path.unlink()
        with patch('app.profile_management.MAX_RENAME_FILE_BYTES', 4):
            with self.assertRaises(ProfileAccessError):
                preview_profile_rename(self.root, 'Test', 'Neu')
        alias = self.root / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ProfileAccessError):
            preview_profile_rename(alias, 'Test', 'Neu')

    def test_atomic_failure_preserves_original_without_temp_debris(self):
        plan = preview_profile_rename(self.root, 'Test', 'Neu')
        with patch('app.atomic_io.os.replace', side_effect=OSError('voll')):
            with self.assertRaises(OSError):
                rename_profile(self.root, plan)
        self.assertEqual((self.folder / FILES[0]).read_bytes(), self.before)
        self.assertEqual([p.name for p in self.folder.iterdir()], [FILES[0]])
