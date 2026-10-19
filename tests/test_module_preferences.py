"""Echte Modulzustände, atomare Mehrfachänderung und Standard-Verfügbarkeit."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from app import module_contracts as modules


class ModulePreferencesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_existing_builtins_enabled_by_default(self):
        for ident in modules.OPTIONAL_MODULES:
            self.assertTrue(modules.is_module_enabled(self.root, ident))
        self.assertIn("wiki", {m.module_id for m in modules.BUILTIN_MODULES})
        with self.assertRaises(ValueError):
            modules.is_module_enabled(self.root, "../evil")

    def test_persist_multiple_switches_and_keep_data(self):
        (self.root / "daten").mkdir()
        payload = self.root / "daten/private.txt"
        payload.write_text("Persönlicher Text")
        modules.set_module_preferences(self.root, {"ideas": False, "wiki": False})
        self.assertFalse(modules.is_module_enabled(self.root, "ideas"))
        self.assertFalse(modules.is_module_enabled(self.root, "wiki"))
        self.assertTrue(modules.is_module_enabled(self.root, "quicklinks"))
        modules.set_module_preferences(self.root, {"wiki": True})
        self.assertTrue(modules.is_module_enabled(self.root, "wiki"))
        self.assertEqual(payload.read_text(), "Persönlicher Text")

    def test_reject_unknown_or_core_and_preserve_old_state(self):
        modules.set_module_preferences(self.root, {"ideas": False})
        before = modules.load_catalog(self.root)
        for values in ({"songs": False}, {"unknown": True}, {"wiki": "false"}, {}):
            with self.assertRaises(ValueError):
                modules.set_module_preferences(self.root, values)
        self.assertEqual(modules.load_catalog(self.root), before)
        with patch.object(modules, "atomic_write_json", side_effect=OSError("kein Platz")):
            with self.assertRaises(OSError):
                modules.set_module_preferences(self.root, {"ideas": True})
        self.assertEqual(modules.load_catalog(self.root), before)
