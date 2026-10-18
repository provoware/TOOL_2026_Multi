"""Start-Fehlerfälle isoliert, ohne Netz und ohne echte Paketinstallation."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
STUB = '''#!{python}
import os, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[2]
args = sys.argv[1:]
with (root / 'calls').open('a') as out:
    out.write(repr(args) + '\\n')
if args[:2] == ['-m', 'pip']:
    if os.environ.get('PIP_FAIL'): sys.exit(1)
    (root / 'installed').touch()
elif args == ['scripts/start_dependencies.py']:
    if os.environ.get('MISSING') and not (root / 'installed').exists(): sys.exit(1)
elif args[:3] == ['-m', 'app.main', '--headless-check']:
    if os.environ.get('HEADLESS_FAIL'): sys.exit(1)
elif args[:2] == ['-m', 'scripts.process_watch']:
    (root / 'launched').touch()
'''


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'Projekt mit Leerzeichen'
        self.root.mkdir()
        shutil.copy2(ROOT / 'schnellstart.sh', self.root)
        (self.root / 'requirements.txt').write_text('PySide6==6.11.2\n')
        (self.root / 'app').mkdir()
        (self.root / 'app/main.py').touch()
        (self.root / 'daten').mkdir()
        (self.root / 'daten/arbeit').write_bytes(b'geschuetzt')
        binary = self.root / '.venv/bin'
        binary.mkdir(parents=True)
        interpreter = binary / 'python'
        interpreter.write_text(STUB.format(python=sys.executable))
        interpreter.chmod(0o755)
        (self.root / '.venv/.requirements.sha256').write_text(
            hashlib.sha256((self.root / 'requirements.txt').read_bytes()).hexdigest())

    def launch(self, **extra):
        env = dict(os.environ, PYTHON=sys.executable, DISPLAY='', WAYLAND_DISPLAY='')
        for name in ('MISSING', 'PIP_FAIL', 'HEADLESS_FAIL'):
            env.pop(name, None)
        env.update(extra)
        result = subprocess.run(['bash', str(self.root / 'schnellstart.sh')],
                                cwd='/', env=env, capture_output=True, text=True, timeout=15)
        self.assertEqual((self.root / 'daten/arbeit').read_bytes(), b'geschuetzt')
        return result

    def test_valid_marker_still_checks_packages(self):
        result = self.launch()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('scripts/start_dependencies.py', (self.root / 'calls').read_text())
        self.assertNotIn("'pip'", (self.root / 'calls').read_text())
        self.assertTrue((self.root / 'launched').exists())

    def test_missing_package_reinstalls_despite_valid_marker(self):
        result = self.launch(MISSING='1')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('--force-reinstall', (self.root / 'calls').read_text())
        self.assertTrue((self.root / 'launched').exists())

    def test_install_failure_does_not_launch_or_change_marker(self):
        marker = self.root / '.venv/.requirements.sha256'
        before = marker.read_bytes()
        result = self.launch(MISSING='1', PIP_FAIL='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / 'launched').exists())
        self.assertEqual(marker.read_bytes(), before)
        self.assertIn('Arbeitsdaten bleiben erhalten', result.stdout)

    def test_broken_interpreter_does_not_recreate_existing_environment(self):
        (self.root / '.venv/bin/python').write_text('#!/unavailable/python\n')
        result = self.launch()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('.venv-alt', result.stdout)
        self.assertFalse((self.root / 'launched').exists())

    def test_existing_incomplete_environment_is_preserved(self):
        (self.root / '.venv/bin/python').unlink()
        result = self.launch()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / '.venv/bin/python').exists())
        self.assertIn('beschädigt', result.stdout)

    def test_headless_error_stops_before_gui_and_launch(self):
        result = self.launch(HEADLESS_FAIL='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / 'launched').exists())
        self.assertNotIn('QtWidgets', (self.root / 'calls').read_text())
