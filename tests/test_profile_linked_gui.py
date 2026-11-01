"""Bewusste Bezugsmigration und Wiederherstellung vor dem echten Dashboardstart."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtCore import QCoreApplication, QEvent, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from app.event_log import EventLogger
from app.profile_rename_dialog import ProfileRenameDialog
from app.profile_store import CATEGORIES, save_profiles, profile_names
from app.profile_transaction import JOURNAL, ProfileRecoveryError, recover_profile_transaction
from app.process_guard import acquire_instance_guard


class StopProbe(Exception):
    pass


class ProfileLinkedGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = save_profiles(self.root, {'Alt': {'Genres': ['Wert']}, 'Anderes': {}})
        self.before = self.path.read_bytes()
        self.favorites = self.path.parent / 'genre_favoriten.json'
        self.favorites.write_text(json.dumps({'schema': 1, 'favorites': {'Alt': {cat: ['Wert'] if cat == 'Genres' else [] for cat in CATEGORIES}}}))
        self.logger = EventLogger(self.root, 'test')
        self.dialog = ProfileRenameDialog(self.root, 'Alt', logger=self.logger)
        self.dialog.show()
        self.app.processEvents()

    def tearDown(self):
        self.dialog.reject()
        self.dialog.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        self.app.processEvents()
        self.tmp.cleanup()

    def test_explicit_consent_preview_and_action_transfer_favorites(self):
        d = self.dialog
        d.name_entry.setText('Neu')
        self.assertFalse(d.transfer_links.isChecked())
        self.assertFalse(d.check())
        d.transfer_links.setChecked(True)
        self.assertTrue(d.check())
        self.assertIn('gemeinsam', d.preview.toPlainText())
        self.assertEqual(self.path.read_bytes(), self.before)
        d.transfer_links.setChecked(False)
        self.assertFalse(d.rename_button.isEnabled())
        self.assertFalse(d.apply())
        d.transfer_links.setChecked(True)
        d.name_entry.setFocus()
        QTest.keyClick(d.name_entry, Qt.Key_Return)
        self.assertEqual(self.path.read_bytes(), self.before)
        QTest.mouseClick(d.rename_button, Qt.LeftButton)
        self.assertEqual(d.renamed_to, 'Neu')
        self.assertIn('Neu', profile_names(self.root))
        self.assertEqual(json.loads(self.favorites.read_text())['favorites']['Neu']['Genres'], ['Wert'])

    def make_pending(self):
        import app.profile_transaction as tx
        publish = tx._publish
        count = 0
        def fail(folder, name, raw):
            nonlocal count
            count += 1
            if count >= 2:
                raise OSError('geschützt')
            publish(folder, name, raw)
        d = self.dialog
        d.name_entry.setText('Neu')
        d.transfer_links.setChecked(True)
        self.assertTrue(d.check())
        with patch.object(tx, '_publish', fail):
            self.assertFalse(d.apply())
        self.assertTrue((self.path.parent / JOURNAL).exists())

    def test_pending_rollback_reports_honestly_logs_and_preserves_proposal(self):
        self.make_pending()
        d = self.dialog
        self.assertIn('gesperrt', d.preview.toPlainText())
        self.assertNotIn('Name und Bestand bleiben erhalten', d.preview.toPlainText())
        self.assertEqual(d.name_entry.text(), 'Neu')
        self.assertTrue(d.last_event_id)
        event = json.loads(self.logger.jsonl_path.read_text().splitlines()[-1])
        self.assertEqual(event['event_id'], d.last_event_id)
        self.assertIn('gesperrt', event['safe_action'])
        self.assertFalse(d.rename_button.isEnabled())
        self.assertFalse(d.check())
        self.assertIn('gesperrt', d.preview.toPlainText())
        self.assertTrue(recover_profile_transaction(self.root))
        self.assertEqual(self.path.read_bytes(), self.before)

    def run_start_probe(self, dashboard):
        from app import main
        tracker = MagicMock()
        with patch.object(main, 'runtime_root', return_value=self.root), \
             patch('app.startup_validation.ensure_runtime_folders_gui', return_value=True), \
             patch('app.ui_standards.configure_application'), \
             patch('app.performance.activate', return_value=tracker), \
             patch('app.ui.Dashboard', side_effect=dashboard) as factory:
            result = main.main()
        self.assertEqual(result, 1)  # gezielter StopProbe oder sichere Startablehnung
        guard = acquire_instance_guard(self.root)
        self.assertIsNotNone(guard)
        guard.release()
        return factory

    def test_real_main_recovers_under_instance_guard_before_dashboard_reads(self):
        self.make_pending()
        def dashboard(*args):
            self.assertIsNone(acquire_instance_guard(self.root))
            self.assertEqual(self.path.read_bytes(), self.before)
            self.assertIn('Alt', profile_names(self.root))
            self.assertFalse((self.path.parent / JOURNAL).exists())
            raise StopProbe('Absichtlicher Teststopp vor Ereignisschleife')
        factory = self.run_start_probe(dashboard)
        factory.assert_called_once()
        events = [json.loads(line) for line in self.logger.jsonl_path.read_text().splitlines()]
        self.assertTrue(any(event['area'] == 'PROFIL_WIEDERHERSTELLUNG' for event in events))

    def test_real_main_does_not_open_dashboard_if_recovery_is_conflicted(self):
        self.make_pending()
        self.favorites.write_text('{"fremd":true}')
        current = self.path.read_bytes()
        factory = self.run_start_probe(lambda *args: self.fail('Dashboard darf nicht öffnen'))
        factory.assert_not_called()
        self.assertEqual(self.path.read_bytes(), current)
        self.assertEqual(self.favorites.read_text(), '{"fremd":true}')
        self.assertTrue((self.path.parent / JOURNAL).exists())
