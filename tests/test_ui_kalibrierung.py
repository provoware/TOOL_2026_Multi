import json
from pathlib import Path
import tempfile
import unittest
from scripts.ui_kalibrierung import evaluate


class CalibrationTests(unittest.TestCase):
    def payload(self, number):
        return {'schema_version': 1, 'mode': 'shadow', 'profile': 'release',
                'git_sha': f'{number:040x}', 'run_number': number,
                'finished_utc': '2026-10-18T12:00:00Z',
                'summary': {'status': 'green', 'matrix_cases': 60, 'window_instances': 180,
                            'errors': 0, 'warnings': 0},
                'metrics': [{} for _ in range(180)], 'findings': []}

    def test_no_evidence_never_promotes(self):
        result = evaluate([])
        self.assertFalse(result['review_candidate'])
        self.assertFalse(result['gate_activated'])

    def test_three_distinct_clean_runs_only_recommend_review(self):
        with tempfile.TemporaryDirectory() as folder:
            paths = []
            for number in (1, 2, 3):
                path = Path(folder) / f'{number}.json'
                path.write_text(json.dumps(self.payload(number)))
                paths.append(path)
            result = evaluate(paths)
            self.assertTrue(result['review_candidate'])
            self.assertFalse(result['gate_activated'])
            self.assertFalse(evaluate([paths[0]] * 3)['review_candidate'])
            broken = self.payload(3)
            broken['findings'] = [{'severity': 'error'}]
            paths[-1].write_text(json.dumps(broken))
            self.assertFalse(evaluate(paths)['review_candidate'])

    def test_pr_local_and_infrastructure_evidence_do_not_qualify(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'probe.json'
            for field, value in (('git_sha', 'local'), ('profile', 'pr'), ('finished_utc', 'bad')):
                raw = self.payload(1)
                raw[field] = value
                path.write_text(json.dumps(raw))
                self.assertFalse(evaluate([path])['rows'][0]['eligible'])
            path.write_text('bad json')
            self.assertFalse(evaluate([path])['review_candidate'])
