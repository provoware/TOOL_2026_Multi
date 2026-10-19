"""Vertragstests: keine Ausführung unbekannten Modulkodes durch JSON."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from app import module_contracts as mods


class ModuleContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_strict_builtin_whitelist_and_persistence(self):
        self.assertTrue(all(not m["catalog_enabled"] for m in mods.describe(self.root)))
        state = mods.set_registered(self.root, "ideas", enabled=True)
        self.assertEqual(state["modules"][0]["id"], "ideas")
        self.assertTrue(next(x for x in mods.describe(self.root) if x["id"] == "ideas")["catalog_enabled"])
        self.assertEqual(mods.load_catalog(self.root), state)
        mods.set_registered(self.root, "ideas", enabled=False)
        self.assertFalse(next(x for x in mods.describe(self.root) if x["id"] == "ideas")["catalog_enabled"])

    def test_reject_unknown_ids_versions_and_untrusted_paths(self):
        with self.assertRaises(ValueError):
            mods.set_registered(self.root, "../../malware", enabled=True)
        with self.assertRaises(ValueError):
            mods.set_registered(self.root, "ideas", enabled="true")
        invalid = {"schema_version": 1, "modules": [{"id": "ideas", "version": "999.0.0", "enabled": True}]}
        with self.assertRaises(ValueError):
            mods.validate_catalog(invalid)
        invalid["modules"][0] = {"id": "ideas", "version": "1.0.0", "enabled": True, "path": "/tmp/evil.py"}
        with self.assertRaises(ValueError):
            mods.validate_catalog(invalid)

    def test_no_dynamic_import_even_for_registered_catalog(self):
        with patch("builtins.__import__", side_effect=AssertionError("kein Fremdcodeimport")):
            clean = mods.validate_catalog({"schema_version": 1, "modules": [
                {"id": "ideas", "version": "1.0.0", "enabled": True}]})
        self.assertEqual(clean["modules"][0]["id"], "ideas")

    def test_duplicate_invalid_and_broken_archives_preserved(self):
        path = self.root / "daten/modulbaukasten/katalog.json"
        path.parent.mkdir(parents=True)
        raw = {"schema_version": 1, "modules": [
            {"id": "ideas", "version": "1.0.0", "enabled": True},
            {"id": "ideas", "version": "1.0.0", "enabled": True}]}
        path.write_text(json.dumps(raw))
        before = path.read_bytes()
        with self.assertRaises(ValueError):
            mods.set_registered(self.root, "songs", enabled=True)
        self.assertEqual(path.read_bytes(), before)

    def test_symlink_and_write_error_do_not_destroy_old_state(self):
        outside = self.root / "outside.json"
        outside.write_text("{}")
        path = self.root / "daten/modulbaukasten/katalog.json"
        path.parent.mkdir(parents=True)
        path.symlink_to(outside)
        with self.assertRaises(ValueError):
            mods.load_catalog(self.root)
        path.unlink()
        mods.set_registered(self.root, "songs", enabled=False)
        before = path.read_bytes()
        with patch.object(mods, "atomic_write_json", side_effect=OSError("Datenträger voll")):
            with self.assertRaises(OSError):
                mods.set_registered(self.root, "songs", enabled=True)
        self.assertEqual(before, path.read_bytes())


if __name__ == "__main__":
    unittest.main()
