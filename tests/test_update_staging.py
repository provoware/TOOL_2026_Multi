import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from app import update_staging as stage


class UpdateStagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.active = self.root / 'active'
        self.active.mkdir()
        (self.active / 'daten').mkdir()
        (self.active / 'daten/arbeit').write_bytes(b'persoenlich')
        self.base = {'tool': {'name': 'TOOL_2026_Multi', 'repository': 'provoware/TOOL_2026_Multi', 'version': '0.18.3'}}
        (self.active / 'MANIFEST.json').write_text(json.dumps(self.base))
        self.parent = self.root / 'staging'
        self.parent.mkdir()
        self.package = self.root / 'update.zip'

    def make_package(self, extra=None, version='0.18.4', manifest_change=None):
        entries = {'app/main.py': 'raise RuntimeError("NIEMALS AUSFUEHREN")\n',
                   'requirements.txt': 'PySide6==6.11.2\n', 'schnellstart.sh': '#!/bin/bash\nexit 123\n'}
        entries.update(extra or {})
        manifest = {'tool': {**self.base['tool'], 'version': version},
                    'files': [{'path': name, 'release': True} for name in ['MANIFEST.json', *entries]]}
        if manifest_change:
            manifest_change(manifest)
        with zipfile.ZipFile(self.package, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('MANIFEST.json', json.dumps(manifest))
            for name, content in entries.items():
                archive.writestr(name, content)
        return stage.sha256(self.package)

    def run_stage(self, package_sha=None, basis=None, parent=None):
        return stage.stage_update(self.active, self.package, package_sha or stage.sha256(self.package),
                                  basis or stage.sha256(self.active / 'MANIFEST.json'), parent or self.parent)

    def assert_unchanged(self):
        self.assertEqual((self.active / 'daten/arbeit').read_bytes(), b'persoenlich')
        self.assertEqual(json.loads((self.active / 'MANIFEST.json').read_text()), self.base)

    def test_valid_package_statically_checked_without_running_code(self):
        sentinel = self.root / 'EXECUTED'
        self.make_package({'app/payload.py': f'from pathlib import Path\nPath({str(sentinel)!r}).touch()\n'})
        folder, report = self.run_stage()
        self.assertFalse(sentinel.exists())
        self.assertFalse(report['activation_allowed'])
        self.assertFalse(report['candidate_code_executed'])
        self.assertEqual(report['runtime_tests'], 'NOT_RUN')
        self.assertEqual(report['status'], 'STATICALLY_VERIFIED_NOT_ACTIVATABLE')
        self.assertEqual(stage.sha256(folder / 'candidate/app/main.py'), report['files']['app/main.py'])
        self.assertEqual(len(report['files']), 5)
        self.assert_unchanged()
        second, _ = self.run_stage()
        self.assertNotEqual(folder, second)

    def test_wrong_sha_and_wrong_basis_fail_without_active_changes(self):
        self.make_package()
        for kwargs in ({'package_sha': '0' * 64}, {'basis': '0' * 64}):
            with self.assertRaises(ValueError):
                self.run_stage(**kwargs)
            self.assertEqual(list(self.parent.iterdir()), [])
            self.assert_unchanged()

    def test_invalid_sha_and_parent_inside_active_rejected(self):
        self.make_package()
        with self.assertRaises(ValueError):
            self.run_stage(package_sha='bad')
        with self.assertRaises(ValueError):
            self.run_stage(parent=self.active / 'daten')
        self.assert_unchanged()

    def test_old_equal_or_invalid_versions_rejected(self):
        for version in ('0.18.2', '0.18.3', 'newest', '1.2.3.4'):
            self.make_package(version=version)
            with self.assertRaises(ValueError):
                self.run_stage()
            self.assertEqual(list(self.parent.iterdir()), [])

    def test_wrong_repository_identity_rejected(self):
        self.make_package(manifest_change=lambda m: m['tool'].update(repository='other/repo'))
        with self.assertRaises(ValueError):
            self.run_stage()
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_traversal_absolute_backslash_and_data_files_rejected(self):
        for name in ('../escape', '/escape', 'app/../../escape', 'app\\escape', 'daten/arbeit', '.git/config'):
            self.make_package({name: 'bad'})
            with self.assertRaises(ValueError):
                self.run_stage()
            self.assertEqual(list(self.parent.iterdir()), [])
            self.assert_unchanged()

    def test_unlisted_missing_and_case_duplicate_entries_rejected(self):
        for case in ('unlisted', 'missing', 'case'):
            self.make_package()
            if case == 'missing':
                self.make_package(manifest_change=lambda m: m['files'].append({'path':'app/missing.py','release':True}))
            else:
                with zipfile.ZipFile(self.package, 'a') as archive:
                    archive.writestr('app/OTHER.py' if case == 'case' else 'app/unlisted.py', 'pass')
                if case == 'case':
                    with zipfile.ZipFile(self.package, 'a') as archive:
                        archive.writestr('app/other.py', 'pass')
            with self.assertRaises(ValueError):
                self.run_stage()
            self.assertEqual(list(self.parent.iterdir()), [])

    def test_symlink_archive_and_zip_symlink_rejected(self):
        self.make_package()
        link = self.root / 'link.zip'
        link.symlink_to(self.package)
        with self.assertRaises(OSError):
            stage.stage_update(self.active, link, stage.sha256(self.package),
                               stage.sha256(self.active / 'MANIFEST.json'), self.parent)
        self.make_package({'app/link.py': 'pass'})
        with zipfile.ZipFile(self.package, 'a') as archive:
            info = zipfile.ZipInfo('app/link2.py')
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(info, '/outside')
        with self.assertRaises(ValueError):
            self.run_stage()
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_static_syntax_json_and_install_options_rejected(self):
        for extra in ({'app/bad.py': 'def ???'}, {'texte/bad.json':'{'},
                      {'requirements.txt':'--extra-index-url https://example.invalid\n'}):
            self.make_package(extra)
            with self.assertRaises((ValueError, SyntaxError)):
                self.run_stage()
            self.assertEqual(list(self.parent.iterdir()), [])
            self.assert_unchanged()

    def test_size_bounds_and_failure_cleanup(self):
        self.make_package()
        for name in ('MAX_ARCHIVE', 'MAX_FILE', 'MAX_TOTAL', 'MAX_FILES'):
            with patch.object(stage, name, 1):
                with self.assertRaises(ValueError):
                    self.run_stage()
            self.assertEqual(list(self.parent.iterdir()), [])
        with patch.object(stage, 'atomic_write_json', side_effect=OSError('voll')):
            with self.assertRaises(OSError):
                self.run_stage()
        self.assertEqual(list(self.parent.iterdir()), [])
        self.assert_unchanged()

    def test_real_project_runtime_release_can_be_staged(self):
        from scripts.veroeffentlichen import build_release
        project = Path(__file__).resolve().parent.parent
        self.package, checksum = build_release(project, self.root / 'build')
        folder, report = self.run_stage(package_sha=checksum)
        self.assertTrue((folder / 'candidate/app/main.py').is_file())
        self.assertIn('app/update_staging.py', report['static_checks'])
        self.assertFalse(report['activation_allowed'])
        self.assert_unchanged()

    def test_baseline_change_during_check_discards_owned_staging_only(self):
        self.make_package()
        before = self.active / 'MANIFEST.json'
        original = stage._static_checks
        def change(candidate):
            result = original(candidate)
            before.write_text(json.dumps({**self.base, 'changed':True}))
            return result
        with patch.object(stage, '_static_checks', side_effect=change):
            with self.assertRaises(ValueError):
                self.run_stage()
        self.assertEqual(list(self.parent.iterdir()), [])
        self.assertTrue(json.loads(before.read_text())['changed'])
        self.assertEqual((self.active / 'daten/arbeit').read_bytes(), b'persoenlich')
