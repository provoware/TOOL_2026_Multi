"""Löschen schützt Namensbezüge, Restprofile und geprüfte Vorzustände."""
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from app.profile_deletion import DeleteError, delete_profile, preview_profile_delete
from app.profile_management import ProfileAccessError
from app.profile_file_io import FILES
from app.profile_store import CATEGORIES, DEFAULT_PROFILES, load_profiles
from app.profile_transaction import JOURNAL, ProfileRecoveryError, recover_profile_transaction


class Interrupted(BaseException):
    pass


class ProfileDeletionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / 'daten/profile'
        self.folder.mkdir(parents=True)
        self.raw = {'Test': {'Genres': ['Du\u0308ster'], 'Zusatz': {'privat': 7}},
                    'Anderes': {'Genres': ['  Fremdwert  '], 'Unbekannt': [1, 2]}}
        self.path = self.write(0, self.raw)
        self.before = self.path.read_bytes()

    def write(self, index, payload):
        path = self.folder / FILES[index]
        path.write_text(json.dumps(payload, ensure_ascii=False) + '  ', encoding='utf-8')
        return path

    def favorites(self, name):
        return {'schema': 1, 'favorites': {name: {cat: [] for cat in CATEGORIES}}}

    def history(self, name):
        return [{'timestamp': '2026-11-01', 'profile': name, 'output': 'historisch',
                 'amounts': {cat: int(cat == 'Genres') for cat in CATEGORIES}}]

    def test_preview_is_read_only_and_lists_all_known_and_extra_fields(self):
        plan = preview_profile_delete(self.root, 'Test')
        self.assertTrue(plan.allowed)
        self.assertEqual(plan.categories, tuple((cat, int(cat == 'Genres')) for cat in CATEGORIES))
        self.assertEqual(plan.extra_fields, ('Zusatz',))
        self.assertEqual(plan.remaining_profiles, 1)
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertEqual([p.name for p in self.folder.iterdir()], [FILES[0]])

    def test_only_selected_profile_removed_other_raw_values_and_metadata_preserved(self):
        favorites = self.write(1, self.favorites('Anderes'))
        history = self.write(2, self.history('Anderes'))
        metadata = favorites.read_bytes(), history.read_bytes()
        self.assertEqual(delete_profile(self.root, preview_profile_delete(self.root, 'Test')), 'Test')
        self.assertEqual(json.loads(self.path.read_text()), {'Anderes': self.raw['Anderes']})
        self.assertEqual((favorites.read_bytes(), history.read_bytes()), metadata)
        self.assertFalse((self.folder / JOURNAL).exists())

    def test_default_preview_does_not_create_store_and_delete_materializes_remaining(self):
        self.path.unlink()
        plan = preview_profile_delete(self.root, 'HardTechno')
        self.assertTrue(plan.allowed)
        self.assertFalse(self.path.exists())
        delete_profile(self.root, plan)
        self.assertEqual(load_profiles(self.root), {key: value for key, value in DEFAULT_PROFILES.items() if key != 'HardTechno'})

    def test_last_profile_remains_protected_even_when_empty(self):
        for values in ({}, {'Genres': ['Wert']}):
            self.write(0, {'Test': values})
            before = self.path.read_bytes()
            plan = preview_profile_delete(self.root, 'Test')
            self.assertFalse(plan.allowed)
            self.assertEqual(plan.remaining_profiles, 0)
            with self.assertRaises(DeleteError):
                delete_profile(self.root, plan)
            self.assertEqual(self.path.read_bytes(), before)

    def test_empty_favorite_and_historical_references_include_canonical_aliases(self):
        for index, payload_factory in ((1, self.favorites), (2, self.history)):
            for name in ('Test', ' TEST ', 'test'):
                with self.subTest(index=index, name=name):
                    path = self.write(index, payload_factory(name))
                    plan = preview_profile_delete(self.root, 'Test')
                    self.assertFalse(plan.allowed)
                    self.assertEqual(plan.favorite_links + plan.history_links, 1)
                    with self.assertRaises(DeleteError):
                        delete_profile(self.root, plan)
                    self.assertEqual(self.path.read_bytes(), self.before)
                    path.unlink()
        self.write(0, {'Ä': {}, 'Anderes': {}})
        self.write(1, self.favorites('A\u0308'))
        self.assertFalse(preview_profile_delete(self.root, 'Ä').allowed)

    def test_any_changed_file_added_removed_or_byte_changed_invalidates_plan(self):
        for index, payload in ((0, self.raw), (1, self.favorites('Anderes')), (2, self.history('Anderes'))):
            with self.subTest(index=index):
                plan = preview_profile_delete(self.root, 'Test')
                path = self.write(index, payload)
                path.write_bytes(path.read_bytes() + b' ')
                with self.assertRaises(DeleteError):
                    delete_profile(self.root, plan)
                plan = preview_profile_delete(self.root, 'Test')
                if index:
                    path.unlink()
                    with self.assertRaises(DeleteError):
                        delete_profile(self.root, plan)
        self.assertIn('Test', load_profiles(self.root))

    def test_wrong_root_forged_plan_unknown_legacy_and_ambiguous_names_refused(self):
        plan = preview_profile_delete(self.root, 'Test')
        for forged in (None, replace(plan, root='/anders'), replace(plan, remaining_profiles=99), replace(plan, extra_fields=())):
            with self.assertRaises(DeleteError):
                delete_profile(self.root, forged)
        with tempfile.TemporaryDirectory() as directory:
            other = Path(directory)
            folder = other / 'daten/profile'; folder.mkdir(parents=True)
            (folder / FILES[0]).write_bytes(self.before)
            with self.assertRaises(DeleteError):
                delete_profile(other, plan)
        for payload, name in ((self.raw, 'unknown'), ({' Test ': {}, 'Anderes': {}}, 'Test'),
                              ({'Ä': {}, 'A\u0308': {}}, 'Ä')):
            self.write(0, payload)
            with self.assertRaises(DeleteError):
                preview_profile_delete(self.root, name)

    def test_corrupt_symlink_and_pending_snapshot_fail_closed(self):
        metadata = self.folder / FILES[1]
        metadata.write_text('{')
        with self.assertRaises(ProfileAccessError):
            preview_profile_delete(self.root, 'Test')
        metadata.unlink()
        metadata.symlink_to(self.folder / 'missing')
        with self.assertRaises(ProfileAccessError):
            preview_profile_delete(self.root, 'Test')
        metadata.unlink()
        (self.folder / JOURNAL).write_text('{}')
        with self.assertRaises(ProfileRecoveryError):
            preview_profile_delete(self.root, 'Test')
        self.assertEqual(self.path.read_bytes(), self.before)

    def test_real_replace_failure_preserves_original_and_clears_journal(self):
        import os
        real = os.replace
        def fail(source, target):
            if Path(target) == self.path:
                raise OSError('Speicher voll')
            return real(source, target)
        with patch('app.atomic_io.os.replace', side_effect=fail), self.assertRaises(OSError):
            delete_profile(self.root, preview_profile_delete(self.root, 'Test'))
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertFalse((self.folder / JOURNAL).exists())
        self.assertEqual(list(self.folder.glob('*.tmp')), [])

    def test_interruption_after_delete_and_failed_rollback_remain_recoverable(self):
        import app.profile_transaction as tx
        publish = tx._publish
        def crash(folder, name, raw):
            publish(folder, name, raw)
            raise Interrupted()
        with patch.object(tx, '_publish', crash), self.assertRaises(Interrupted):
            delete_profile(self.root, preview_profile_delete(self.root, 'Test'))
        self.assertNotIn('Test', json.loads(self.path.read_text()))
        with self.assertRaises(ProfileRecoveryError):
            load_profiles(self.root)
        with patch.object(tx, '_publish', side_effect=OSError('Schreibschutz')):
            with self.assertRaises(ProfileRecoveryError):
                recover_profile_transaction(self.root)
        self.assertTrue((self.folder / JOURNAL).exists())
        self.assertTrue(recover_profile_transaction(self.root))
        self.assertEqual(self.path.read_bytes(), self.before)
