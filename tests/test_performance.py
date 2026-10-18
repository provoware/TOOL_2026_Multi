"""Isolierte Leistungsdaten: opt-in, Datenschutz, Rotation und fehlertolerante Messung."""
from copy import deepcopy
from datetime import date, timedelta
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from app import performance as perf
from app.atomic_io import atomic_write_text
from app.performance_report import report
from app import book_store, snippet_store


class PerformanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.old = perf._ACTIVE
        self.tracker = perf.activate(self.root)

    def tearDown(self):
        perf._ACTIVE = self.old
        self.temp.cleanup()

    def enable(self):
        self.tracker.configure(True)

    def test_default_off_has_no_file_side_effect_and_does_not_inspect_content(self):
        self.assertFalse(self.tracker.enabled)
        with perf.observe('file.write', content=object()):
            pass
        self.assertTrue(self.tracker.flush())
        self.assertEqual([], list(self.root.iterdir()))

    def test_config_persists_and_data_write_is_batched_without_recursion(self):
        self.enable()
        for _ in range(5):
            self.tracker.record('module.open', 'books', 12)
        self.assertFalse(self.tracker.data_path.exists())
        self.assertTrue(self.tracker.flush())
        payload = json.loads(self.tracker.data_path.read_text())
        rows = payload['days'][date.today().isoformat()]
        self.assertEqual(1, len(rows))
        self.assertEqual(5, next(iter(rows.values()))['count'])
        restored = perf.Performance(self.root)
        self.assertTrue(restored.enabled)
        self.assertEqual(payload, restored.snapshot())
        with patch('app.atomic_io.atomic_write_json') as writer:
            self.assertTrue(self.tracker.flush())
            writer.assert_not_called()

    def test_central_writer_measures_bytes_and_never_stores_paths_or_contents(self):
        self.enable()
        target = self.root / 'daten/buecher/SECRET-TITLE.txt'
        atomic_write_text(target, 'Private Zwischenablage äöü')
        data = self.tracker.snapshot()
        encoded = json.dumps(data)
        self.assertNotIn('SECRET', encoded)
        self.assertNotIn('Zwischenablage', encoded)
        self.assertNotIn(str(self.root), encoded)
        row = next(iter(data['days'][date.today().isoformat()].values()))
        self.assertEqual(len('Private Zwischenablage äöü'.encode('utf-8')), row['bytes'])
        self.assertEqual(1, row['count'])

    def test_failed_writer_keeps_original_and_counts_only_one_failed_attempt(self):
        target = self.root / 'daten/buecher/book.json'
        atomic_write_text(target, 'Original')
        self.enable()
        with patch('app.atomic_io.os.replace', side_effect=OSError('PRIVATE ERROR')):
            with self.assertRaises(OSError):
                atomic_write_text(target, 'Nicht übernommen')
        self.assertEqual('Original', target.read_text())
        row = next(iter(self.tracker.snapshot()['days'][date.today().isoformat()].values()))
        self.assertEqual(1, row['count'])
        self.assertEqual(1, row['errors'])
        self.assertNotIn('PRIVATE', json.dumps(self.tracker.snapshot()))

    def test_broken_metrics_do_not_block_working_file_write(self):
        self.enable()
        with patch.object(self.tracker, 'record', side_effect=RuntimeError('Messung kaputt')):
            atomic_write_text(self.root / 'work.txt', 'Gespeichert')
        self.assertEqual('Gespeichert', (self.root / 'work.txt').read_text())
        self.assertIn('ausgelassen', self.tracker.last_error)

    def test_failed_flush_preserves_old_statistics_and_pending_memory(self):
        self.enable()
        self.tracker.record('module.open', 'books', 3)
        self.assertTrue(self.tracker.flush())
        before = self.tracker.data_path.read_bytes()
        self.tracker.record('module.open', 'books', 5)
        with patch('app.atomic_io.atomic_write_json', side_effect=OSError('voll')):
            self.assertFalse(self.tracker.flush())
        self.assertEqual(before, self.tracker.data_path.read_bytes())
        self.assertTrue(self.tracker.dirty)
        self.assertTrue(self.tracker.flush())
        self.assertEqual(2, next(iter(self.tracker.snapshot()['days'][date.today().isoformat()].values()))['count'])

    def test_disable_stops_collection_but_keeps_history_until_clear(self):
        self.enable()
        self.tracker.record('app.start', elapsed_ms=10)
        self.tracker.configure(False)
        self.tracker.record('app.start', elapsed_ms=20)
        self.assertEqual(1, next(iter(self.tracker.snapshot()['days'][date.today().isoformat()].values()))['count'])
        work = self.root / 'daten/user.txt'
        work.parent.mkdir(exist_ok=True)
        work.write_text('Arbeit')
        self.tracker.clear()
        self.assertEqual({}, self.tracker.snapshot()['days'])
        self.assertFalse(self.tracker.enabled)
        self.assertFalse(self.tracker.data_path.exists())
        self.assertEqual('Arbeit', work.read_text())
        self.assertFalse(perf.Performance(self.root).enabled)

    def test_retention_and_selection_are_bounded(self):
        self.enable()
        self.tracker.record('app.start', elapsed_ms=4)
        rows = self.tracker.data['days'][date.today().isoformat()]
        self.tracker.data['days'][(date.today() - timedelta(days=31)).isoformat()] = deepcopy(rows)
        self.tracker.configure(True, 7)
        self.assertEqual(1, len(self.tracker.snapshot()['days']))
        self.assertEqual({}, self.tracker.snapshot(7, ('file.write',))['days'])
        with self.assertRaises(ValueError):
            self.tracker.snapshot(31)

    def test_corrupt_or_extended_payload_is_never_silently_replaced(self):
        self.tracker.data_path.parent.mkdir(parents=True)
        self.tracker.data_path.write_text('{"schema_version":1,"days":{},"private":"SECRET"}')
        tracker = perf.activate(self.root)
        self.assertTrue(tracker.read_error)
        self.assertFalse(tracker.flush())
        with self.assertRaises(ValueError):
            tracker.configure(True)
        self.assertIn('SECRET', tracker.data_path.read_text())
        tracker.clear()
        tracker.configure(True)
        self.assertFalse(tracker.read_error)

    def test_unknown_names_invalid_counts_and_nonfinite_durations_are_rejected(self):
        self.enable()
        for operation, area, duration in [('PRIVATE', 'books', 1), ('module.open', 'PRIVATE', 1), ('module.open', 'books', float('nan'))]:
            with self.assertRaises(ValueError):
                self.tracker.record(operation, area, duration)
        self.tracker.record('app.start', elapsed_ms=5)
        data = self.tracker.snapshot()
        row = next(iter(data['days'][date.today().isoformat()].values()))
        row['count'] = -1
        with self.assertRaises(ValueError):
            perf.validate(data)

    def test_unchanged_book_and_snippet_saves_are_counted_without_extra_reads(self):
        self.enable()
        book = book_store.new_book()
        book['title'] = 'Geheim'
        book_store.put(self.root, book)
        book_store.put(self.root, book)
        values = {'workflow': 'Coding', 'category': 'Privat', 'title': 'Geheim', 'content': 'Privattext', 'color': 'Standard', 'size': 'Mittel'}
        item = snippet_store.put(self.root, values)
        snippet_store.put(self.root, values, item['id'])
        groups = self.tracker.snapshot(30, ('save.attempt',))['days'][date.today().isoformat()]
        self.assertEqual(2, len(groups))
        for row in groups.values():
            self.assertEqual(2, row['count'])
            self.assertEqual(1, row['unchanged'])
        self.assertNotIn('Geheim', json.dumps(groups))

    def test_report_uses_approximate_quantiles_only_after_enough_samples(self):
        self.enable()
        self.tracker.record('module.open', 'books', 3)
        self.assertIn('Weniger als 20', report(self.tracker.snapshot()))
        for _ in range(19):
            self.tracker.record('module.open', 'books', 3)
        summary = report(self.tracker.snapshot())
        self.assertIn('≤ 5 ms', summary)
        self.assertIn('Grobe 95%', summary)
        self.assertIn('keine SSD', summary)
