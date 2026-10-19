from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import startbenchmark as bench


class StartBenchmarkTests(unittest.TestCase):
    def test_real_app_process_isolated_first_and_repeat(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);sentinel=root/'arbeit';sentinel.write_text('unveraendert')
            with patch.dict(bench.GROUPS,{'probe':1},clear=True):result=bench.run(2,'offscreen',root)
            self.assertEqual(list(root.iterdir()),[sentinel])
            self.assertEqual(sentinel.read_text(),'unveraendert')
        self.assertEqual([r['state'] for r in result['samples']],['first_launch_in_series','repeat_launch'])
        for sample in result['samples']:
            self.assertGreater(sample['ready_ms'],0)
            self.assertGreater(sample['process_total_ms'],sample['ready_ms'])
            self.assertEqual(sample['qpa'],'offscreen')
            self.assertTrue(sample['visible'])
        self.assertFalse(result['cold_os_start_proven'])

    def test_limits_and_nonfixture_worker_rejected(self):
        with self.assertRaises(ValueError):bench.run(1)
        with self.assertRaises(ValueError):bench.run(11)
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(OSError):bench.worker(Path(folder),1)
