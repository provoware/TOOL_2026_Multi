"""Sicherheits- und Datenprüfungen deklarativer Modulentwürfe."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from app import module_blueprints as b, module_archive as archive


def sample(title="Mein Modul"):
    return {"id": "modul_1", "title": title, "description": "eigene Sammlung",
            "fields": [{"id": "field_1", "label": "Titel", "type": "text"}],
            "capabilities": ["view", "edit"]}


class ModuleBlueprintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_create_update_preview_and_import(self):
        b.put(self.root, sample())
        self.assertEqual(b.preview_definition(sample())["executable"], False)
        self.assertEqual(len(b.load(self.root)["blueprints"]), 1)
        raw = b.load(self.root)
        self.assertEqual(b.import_copies(self.root, raw), 1)
        self.assertEqual(len(b.load(self.root)["blueprints"]), 2)
        self.assertIn("Kopie", b.load(self.root)["blueprints"][1]["title"])

    def test_disallow_unsafe_permissions_code_and_duplicate_fields(self):
        for bad in ({"capabilities": ["view", "execute"]},
                    {"fields": [{"id": "../file", "label": "Datei", "type": "text"}]},
                    {"fields": [{"id": "field_1", "label": "A", "type": "text"},
                                {"id": "field_1", "label": "B", "type": "text"}]},
                    {"entrypoint": "os.system('/tmp/fremd')"}):
            record = {**sample(), **bad}
            with self.assertRaises(ValueError):
                b.validate_blueprint(record)
        with self.assertRaises(ValueError):
            b.validate_blueprint({**sample(), "fields": []})

    def test_atomic_failure_keeps_original(self):
        b.put(self.root, sample())
        datafile = archive.state_path(self.root, b.MODULE)
        before = datafile.read_bytes()
        with patch.object(archive, "atomic_write_json", side_effect=OSError("Speicher voll")):
            with self.assertRaises(OSError):
                b.put(self.root, sample("Neuer Name"))
        self.assertEqual(before, datafile.read_bytes())

    def test_removing_one_does_not_damage_other(self):
        b.put(self.root, sample())
        b.put(self.root, {**sample("Zweites Modul"), "id": "modul_2"})
        b.remove(self.root, "modul_1")
        self.assertEqual(b.load(self.root)["blueprints"][0]["title"], "Zweites Modul")
