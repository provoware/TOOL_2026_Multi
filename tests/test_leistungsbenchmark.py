"""Schutzgrenzen des isolierten Entwicklermesswerkzeugs."""
import tempfile
import unittest
from pathlib import Path
from app import performance
from scripts.leistungsbenchmark import run


class BenchmarkTests(unittest.TestCase):
    def test_isolation_counts_and_restore_active_tracker(self):
        previous = performance.current()
        try:
            with tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                sentinel = root / 'bestand.txt'
                sentinel.write_text('unverändert', encoding='utf-8')
                active = performance.activate(root)
                result = run(3, 2, 16, root)
                self.assertIs(performance.current(), active)
                self.assertEqual(list(root.iterdir()), [sentinel])
                self.assertEqual(sentinel.read_text(encoding='utf-8'), 'unverändert')
                self.assertEqual(len(result['samples']), 9)
                for sample in result['samples']:
                    self.assertEqual(sample['count'], 2 if sample['mode'] == 'enabled' else 0)
                self.assertFalse(result['one_percent_target_proven'])
        finally:
            performance._ACTIVE = previous

    def test_reject_unbounded_work_before_writing(self):
        for args in ((2, 1, 1), (61, 1, 1), (3, 0, 1), (3, 10001, 1), (3, 1, 1048577)):
            with self.assertRaises(ValueError):
                run(*args)
