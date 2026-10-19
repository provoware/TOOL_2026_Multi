"""Vollständiger sicherer Kopier- und Opt-in-Startablauf, ohne Altinstallation zu verändern."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from app.atomic_io import atomic_write_json
from app.update_legacy_copy import prepare_legacy_copy
from app.update_independent_activation import activate_independent_copy

class MigrationCopyActivationRoundtripTests(unittest.TestCase):
    def test_copy_and_independent_launcher_preserve_original(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            legacy=root/"legacy"
            legacy.mkdir()
            out=root/"new"
            out.mkdir()
            (legacy/"daten").mkdir()
            (legacy/"daten/important.txt").write_text("UNVERAENDERT")
            (legacy/"scripts").mkdir()
            (legacy/"scripts/managed_start.py").write_text("print('bootstrap')")
            (legacy/"schnellstart.sh").write_text("#!/bin/bash\n")
            manifest={
                "tool":{"name":"TOOL_2026_Multi",
                        "repository":"provoware/TOOL_2026_Multi","version":"0.18.5"},
                "runtime":{"external_data_root":True},
                "files":[
                    {"path":"MANIFEST.json","release":True},
                    {"path":"schnellstart.sh","release":True},
                    {"path":"scripts/managed_start.py","release":True},
                ],
            }
            atomic_write_json(legacy/"MANIFEST.json",manifest)
            copy=prepare_legacy_copy(legacy,out)
            self.assertFalse((copy/"current").exists())
            starter=activate_independent_copy(
                copy,approved=True,
                runner=lambda *args,**kwargs:SimpleNamespace(returncode=0))
            self.assertTrue(starter.exists())
            self.assertEqual((legacy/"daten/important.txt").read_text(),"UNVERAENDERT")
            self.assertEqual((copy/"persistent/daten/important.txt").read_text(),"UNVERAENDERT")
            self.assertTrue((copy/"current").is_symlink())
            self.assertFalse((legacy/"current").exists())
