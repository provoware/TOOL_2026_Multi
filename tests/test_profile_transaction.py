"""Mehrdateienwechsel: exakte Rücknahme, Neustart und konfliktfreie Sperren."""
import base64
import fcntl
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.profile_file_io import FILES
from app.profile_store import CATEGORIES, load_profiles, save_profiles
from app.genre_random import history_load
from app.genre_favorites import load_favorites
from app.profile_management import preview_profile_rename, rename_profile, RenameError
from app.profile_transaction import (
    JOURNAL, LOCK, ProfileRecoveryError, ensure_ready, recover_profile_transaction,
    write_profile_transaction, _hash,
)


class Interrupted(BaseException):
    pass


class ProfileTransactionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / 'daten/profile'
        self.folder.mkdir(parents=True)
        self.data = [ {'Alt': {'Genres': ['  Du\u0308ster  '], 'Zusatz': {'roh': 7}}, 'Fremd': {}},
                      {'schema': 1, 'Zusatz': 12, 'favorites': {'Alt': {cat: ['Du\u0308ster'] if cat == 'Genres' else [] for cat in CATEGORIES}}},
                      [{'timestamp': '2026-11-01', 'profile': 'Alt', 'output': ' Original ', 'extra': 42,
                        'amounts': {cat: int(cat == 'Genres') for cat in CATEGORIES}}]]
        self.original = {}
        for name, payload in zip(FILES, self.data):
            raw = json.dumps(payload, ensure_ascii=False).encode() + b' \n'
            (self.folder / name).write_bytes(raw)
            self.original[name] = raw

    def plan(self):
        return preview_profile_rename(self.root, 'Alt', 'Neu', transfer_links=True)

    def crash(self, after):
        import app.profile_transaction as tx
        publish = tx._publish
        count = 0
        def interrupt(folder, name, raw):
            nonlocal count
            publish(folder, name, raw)
            count += 1
            if count == after:
                raise Interrupted()
        with patch.object(tx, '_publish', interrupt), self.assertRaises(Interrupted):
            rename_profile(self.root, self.plan())

    def assert_original(self):
        self.assertEqual({name: (self.folder / name).read_bytes() for name in FILES}, self.original)
        self.assertFalse((self.folder / JOURNAL).exists())

    def test_linked_success_needs_explicit_consent_and_preserves_raw_payloads(self):
        self.assertFalse(preview_profile_rename(self.root, 'Alt', 'Neu').allowed)
        plan = self.plan()
        self.assertTrue(plan.allowed)
        self.assertEqual((plan.favorite_links, plan.history_links), (1, 1))
        self.assertEqual(rename_profile(self.root, plan), 'Neu')
        raw = [json.loads((self.folder / name).read_text()) for name in FILES]
        self.assertEqual(raw[0], {'Neu': self.data[0]['Alt'], 'Fremd': {}})
        self.assertEqual(raw[1], {**self.data[1], 'favorites': {'Neu': self.data[1]['favorites']['Alt']}})
        self.assertEqual(raw[2], [{**self.data[2][0], 'profile': 'Neu'}])
        self.assertFalse((self.folder / JOURNAL).exists())
        self.assertEqual(list(load_favorites(self.root)), ['Neu'])
        self.assertEqual(history_load(self.root)[0]['profile'], 'Neu')
        self.assertEqual(recover_profile_transaction(self.root), False)

    def test_target_or_alias_references_still_block(self):
        for name in ('Neu', 'NEU', ' alt '):
            data = json.loads(json.dumps(self.data[1]))
            data['favorites'][name] = {cat: [] for cat in CATEGORIES}
            (self.folder / FILES[1]).write_text(json.dumps(data))
            plan = self.plan()
            self.assertFalse(plan.allowed)
            self.assertGreater(plan.unsafe_links, 0)
            with self.assertRaises(RenameError):
                rename_profile(self.root, plan)
            self.assertEqual((self.folder / FILES[0]).read_bytes(), self.original[FILES[0]])

    def test_each_process_interruption_recovers_exact_bytes_idempotently(self):
        for index in (1, 2, 3):
            with self.subTest(index=index):
                self.crash(index)
                for reader in (load_profiles, load_favorites, history_load):
                    with self.assertRaises(ProfileRecoveryError):
                        reader(self.root)
                with self.assertRaises(ProfileRecoveryError):
                    save_profiles(self.root, {'Fremd': {}})
                with self.assertRaises(ProfileRecoveryError):
                    preview_profile_rename(self.root, 'Alt', 'Anders')
                self.assertTrue(recover_profile_transaction(self.root))
                self.assert_original()
                self.assertFalse(recover_profile_transaction(self.root))

    def test_ordinary_replace_failure_rolls_back_and_removes_journal(self):
        real = os.replace
        def fail(source, target):
            if Path(target).name == FILES[1]:
                raise OSError('voll')
            return real(source, target)
        with patch('app.atomic_io.os.replace', side_effect=fail), self.assertRaises(OSError):
            rename_profile(self.root, self.plan())
        self.assert_original()
        self.assertEqual(list(self.folder.glob('*.tmp')), [])

    def test_failed_rollback_stays_blocked_until_restart_recovery(self):
        import app.profile_transaction as tx
        publish = tx._publish
        count = 0
        def fail(folder, name, raw):
            nonlocal count
            count += 1
            if count >= 2:
                raise OSError('geschützt')
            publish(folder, name, raw)
        with patch.object(tx, '_publish', fail), self.assertRaises(ProfileRecoveryError):
            rename_profile(self.root, self.plan())
        with self.assertRaises(ProfileRecoveryError):
            ensure_ready(self.root)
        self.assertTrue(recover_profile_transaction(self.root))
        self.assert_original()

    def test_recovery_preflights_all_conflicts_before_any_write(self):
        self.crash(2)
        profile_bytes = (self.folder / FILES[0]).read_bytes()
        (self.folder / FILES[2]).write_bytes(b'[]')
        with self.assertRaises(ProfileRecoveryError):
            recover_profile_transaction(self.root)
        self.assertEqual((self.folder / FILES[0]).read_bytes(), profile_bytes)
        self.assertEqual((self.folder / FILES[2]).read_bytes(), b'[]')
        self.assertTrue((self.folder / JOURNAL).exists())
        (self.folder / FILES[2]).write_bytes(self.original[FILES[2]])
        self.assertTrue(recover_profile_transaction(self.root))
        self.assert_original()

    def test_invalid_root_checksum_path_or_bytes_journal_never_changes_data(self):
        self.crash(1)
        path = self.folder / JOURNAL
        original = path.read_bytes()
        data = json.loads(original)
        changes = [dict(data, root='/fremd'), dict(data, schema=999), dict(data, files={'../escape': {}})]
        bad = json.loads(original); bad['files'][FILES[0]]['before_sha'] = 'wrong'; changes.append(bad)
        bad = json.loads(original); bad['files'][FILES[0]]['before'] = '!!!!'; changes.append(bad)
        before = {name: (self.folder / name).read_bytes() for name in FILES}
        for payload in changes:
            with self.subTest(payload=list(payload)):
                path.write_text(json.dumps(payload))
                with self.assertRaises(ProfileRecoveryError):
                    recover_profile_transaction(self.root)
                self.assertEqual({name: (self.folder / name).read_bytes() for name in FILES}, before)
        path.write_bytes(original)
        with patch('app.profile_transaction.MAX_JOURNAL_BYTES', 4):
            with self.assertRaises(ProfileRecoveryError):
                recover_profile_transaction(self.root)
        recover_profile_transaction(self.root)
        self.assert_original()

    def test_stale_snapshot_and_second_writer_are_rejected(self):
        plan = self.plan()
        fingerprints = plan.fingerprints
        with self.assertRaises(ValueError):
            write_profile_transaction(self.root, {'../escape': b'{}'}, fingerprints)
        self.assertFalse((self.root / 'escape').exists())
        with (self.folder / LOCK).open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(ProfileRecoveryError):
                rename_profile(self.root, plan)
        (self.folder / FILES[1]).write_bytes(self.original[FILES[1]] + b' ')
        with self.assertRaises(ValueError):
            write_profile_transaction(self.root, {}, fingerprints)
        self.assertFalse((self.folder / JOURNAL).exists())

    def test_missing_profile_created_from_defaults_is_removed_on_rollback(self):
        (self.folder / FILES[0]).unlink()
        self.data[1]['favorites'] = {'HardTechno': {cat: [] for cat in CATEGORIES}}
        (self.folder / FILES[1]).write_text(json.dumps(self.data[1]))
        plan = preview_profile_rename(self.root, 'HardTechno', 'Neu', transfer_links=True)
        import app.profile_transaction as tx
        publish = tx._publish
        def interrupt(folder, name, raw):
            publish(folder, name, raw)
            raise Interrupted()
        with patch.object(tx, '_publish', interrupt), self.assertRaises(Interrupted):
            rename_profile(self.root, plan)
        recover_profile_transaction(self.root)
        self.assertFalse((self.folder / FILES[0]).exists())

    def test_real_fresh_process_recovers_after_abrupt_exit(self):
        script = '''import os, sys
from pathlib import Path
from app.profile_management import preview_profile_rename, rename_profile
import app.profile_transaction as tx
root = Path(sys.argv[1])
original = tx._publish
def crash(folder, name, raw):
    original(folder, name, raw)
    os._exit(77)
tx._publish = crash
rename_profile(root, preview_profile_rename(root, 'Alt', 'Neu', transfer_links=True))
'''
        result = subprocess.run([sys.executable, '-c', script, str(self.root)], timeout=10)
        self.assertEqual(result.returncode, 77)
        recover = "from pathlib import Path; from app.profile_transaction import recover_profile_transaction; import sys; assert recover_profile_transaction(Path(sys.argv[1]))"
        subprocess.run([sys.executable, '-c', recover, str(self.root)], check=True, timeout=10)
        self.assert_original()

    def test_pending_symlink_or_fifo_journal_and_profile_refused(self):
        path = self.folder / JOURNAL
        for make in (lambda: path.symlink_to(self.folder / 'missing'), lambda: os.mkfifo(path)):
            make()
            with self.assertRaises(ProfileRecoveryError):
                recover_profile_transaction(self.root)
            path.unlink()
        path.symlink_to(self.folder / FILES[0])
        with self.assertRaises(ProfileRecoveryError):
            ensure_ready(self.root)
        self.assertEqual((self.folder / FILES[0]).read_bytes(), self.original[FILES[0]])

    def test_untouched_history_file_remains_byte_identical(self):
        history = self.data[2]
        history[0]['profile'] = 'Fremd'
        path = self.folder / FILES[2]
        path.write_text(json.dumps(history) + '   ')
        before = path.read_bytes()
        rename_profile(self.root, self.plan())
        self.assertEqual(path.read_bytes(), before)
