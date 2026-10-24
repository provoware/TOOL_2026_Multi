"""PV-AUD-01: persönliche Notizen, sichere Altkopien und Sicherungs-Roundtrip."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from app import quick_note as notes
from scripts import datensicherung as backup


class QuickNoteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.legacy = self.root / notes.LEGACY_FILE

    def test_new_notes_are_data_and_old_file_is_unchanged(self):
        raw = b'Altbestand\r\n\xff\x00'
        self.legacy.write_bytes(raw)
        target = notes.append_developer_info(self.root, 'Neue\nNotiz')
        self.assertEqual(target, self.root / notes.NOTE_FILE)
        self.assertIn('Neue Notiz', target.read_text())
        self.assertEqual(self.legacy.read_bytes(), raw)
        self.assertTrue(notes.legacy_notes_pending(self.root))

    def test_legacy_consent_required_before_any_copy(self):
        self.legacy.write_bytes(b'Original')
        with self.assertRaises(PermissionError):
            notes.preserve_legacy_notes(self.root)
        self.assertFalse((self.root / 'daten').exists())
        self.assertEqual(self.legacy.read_bytes(), b'Original')

    def test_confirmed_legacy_is_byte_exact_idempotent_and_versioned(self):
        raw = b'Alt\r\n\xff\x00'
        self.legacy.write_bytes(raw)
        first = notes.preserve_legacy_notes(self.root, approved=True)
        self.assertEqual(first.read_bytes(), raw)
        self.assertEqual(first.stat().st_mode & 0o777, 0o600)
        self.assertFalse(notes.legacy_notes_pending(self.root))
        self.assertEqual(notes.preserve_legacy_notes(self.root, approved=True), first)
        self.legacy.write_bytes(raw + b'Neu')
        self.assertTrue(notes.legacy_notes_pending(self.root))
        second = notes.preserve_legacy_notes(self.root, approved=True)
        self.assertNotEqual(first, second)
        self.assertEqual(first.read_bytes(), raw)
        self.assertEqual(second.read_bytes(), raw + b'Neu')

    def test_existing_copy_collision_is_not_overwritten(self):
        self.legacy.write_bytes(b'Original')
        target = notes.preserve_legacy_notes(self.root, approved=True)
        target.write_bytes(b'Abweichender vorhandener Bestand')
        with self.assertRaises(ValueError):
            notes.preserve_legacy_notes(self.root, approved=True)
        self.assertEqual(target.read_bytes(), b'Abweichender vorhandener Bestand')
        self.assertEqual(self.legacy.read_bytes(), b'Original')

    def test_atomic_write_error_preserves_previous_notes(self):
        target = notes.append_developer_info(self.root, 'Erste Notiz')
        before = target.read_bytes()
        with patch('app.atomic_io.os.replace', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                notes.append_developer_info(self.root, 'Zweite Notiz')
        self.assertEqual(target.read_bytes(), before)
        self.assertEqual(list(target.parent.iterdir()), [target])

    def test_invalid_current_encoding_and_size_are_not_overwritten(self):
        target = notes.append_developer_info(self.root, 'Eine Notiz')
        target.write_bytes(b'\xff')
        with self.assertRaises(UnicodeError):
            notes.append_developer_info(self.root, 'Neu')
        self.assertEqual(target.read_bytes(), b'\xff')
        with patch.object(notes, 'MAX_NOTES_BYTES', 0):
            with self.assertRaises(ValueError):
                notes.append_developer_info(self.root, 'Neu')

    def test_linked_data_note_and_legacy_are_rejected(self):
        outside = self.root / 'extern'
        outside.mkdir()
        (self.root / 'daten').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            notes.append_developer_info(self.root, 'Neu')
        (self.root / 'daten').unlink()
        target = notes.append_developer_info(self.root, 'Erste')
        before = target.read_bytes()
        self.legacy.symlink_to(target)
        with self.assertRaises(ValueError):
            notes.preserve_legacy_notes(self.root, approved=True)
        self.legacy.unlink()
        external_file = outside / 'schutz.txt'
        external_file.write_bytes(b'Geschuetzt')
        target.unlink()
        target.symlink_to(external_file)
        with self.assertRaises(ValueError):
            notes.append_developer_info(self.root, 'Neu')
        self.assertEqual(external_file.read_bytes(), b'Geschuetzt')

    def test_changed_legacy_during_copy_is_reported_without_original_overwrite(self):
        self.legacy.write_bytes(b'Original')
        original = notes._read_regular
        def read(path):
            raw = original(path)
            if path == self.legacy:
                self.legacy.write_bytes(b'Geaendert')
            return raw
        with patch.object(notes, '_read_regular', side_effect=read):
            with self.assertRaises(ValueError):
                notes.preserve_legacy_notes(self.root, approved=True)
        self.assertEqual(self.legacy.read_bytes(), b'Geaendert')
        self.assertFalse(list((self.root / 'daten/notizen').glob('.alt-notizen-*')))

    def test_backup_restore_includes_current_and_confirmed_legacy_notes(self):
        self.legacy.write_bytes(b'Alte\r\nNotiz\xff')
        old = notes.preserve_legacy_notes(self.root, approved=True)
        current = notes.append_developer_info(self.root, 'Neue Notiz')
        archive = backup.create(self.root / 'daten', self.root / 'sicherung')
        restored = self.root / 'wiederhergestellt'
        backup.restore(archive, restored)
        for path in (old, current):
            self.assertEqual((restored / path.relative_to(self.root)).read_bytes(), path.read_bytes())
        self.assertEqual(self.legacy.read_bytes(), b'Alte\r\nNotiz\xff')

    def test_external_runtime_root_does_not_write_into_code_root(self):
        code, runtime = self.root / 'programm', self.root / 'arbeitsdaten'
        code.mkdir()
        runtime.mkdir()
        target = notes.append_developer_info(runtime, 'Extern gespeichert')
        self.assertTrue(target.is_relative_to(runtime / 'daten'))
        self.assertEqual(list(code.iterdir()), [])
