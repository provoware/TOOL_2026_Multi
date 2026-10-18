import tempfile
import unittest
from pathlib import Path
from scripts import ladebenchmark as bench


class LoadBenchmarkTests(unittest.TestCase):
    def test_real_worker_processes_are_isolated_and_grouped(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sentinel = root / 'arbeit'
            sentinel.write_bytes(b'unveraendert')
            result = bench.run(1, 2, root)
            self.assertEqual(list(root.iterdir()), [sentinel])
            self.assertEqual(sentinel.read_bytes(), b'unveraendert')
        self.assertEqual(len(result['samples']), 3)
        self.assertEqual(set(result['median_ms']), set(bench.GROUPS))
        for row in result['samples']:
            self.assertEqual([v['state'] for v in row['loads']],
                             ['first_read', 'repeated_read', 'repeated_read'])
            self.assertGreater(row['process_total_ms'], 0)
        self.assertIn('uncontrolled', result['os_cache_state'])

    def test_work_limits(self):
        for rounds, repeats in ((0, 1), (21, 1), (1, 0), (1, 101)):
            with self.assertRaises(ValueError):
                bench.run(rounds, repeats)
