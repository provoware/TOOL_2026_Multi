"""Qt-unabhängige Regressionen für Generator, Import und Datenintegrität."""
import json
import random
import tempfile
import unittest
from pathlib import Path

from app.genre_random import (
    archive_export, archive_import, generate, history_load, preset_save,
    presets_load, rename_value,
)
from app.profile_store import CATEGORIES, add_values, load_profiles, save_profiles, store_path


class GenreRandomTests(unittest.TestCase):
    def test_generate_is_unique_in_each_category_and_keeps_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            amounts = {cat: 1 for cat in CATEGORIES}
            item = generate(root, "HardTechno", amounts, rng=random.Random(7))
            self.assertEqual(len(item["output"].split(", ")), 5)
            self.assertEqual(item["profile"], "HardTechno")
            self.assertEqual(history_load(root)[0]["output"], item["output"])
            self.assertTrue(item["timestamp"])

    def test_insufficient_amount_does_not_change_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            counts = {cat: 0 for cat in CATEGORIES}
            counts["Genres"] = 15
            with self.assertRaisesRegex(ValueError, "nur"):
                generate(root, "HardTechno", counts)
            self.assertEqual(history_load(root), [])

    def test_export_import_merges_without_duplicate_or_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            exported = archive_export(root, root / "export.json")
            profiles = load_profiles(root)
            add_values(root, "HardTechno", "Genres", "Neu, schranz, NEU")
            result = archive_import(root, exported)
            self.assertEqual(result["values"], 0)
            genres = load_profiles(root)["HardTechno"]["Genres"]
            self.assertIn("Neu", genres)
            self.assertEqual(sum(x.casefold() == "schranz" for x in genres), 1)

    def test_corrupt_import_leaves_previous_bytes_intact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            add_values(root, "HardTechno", "Genres", "Neu")
            before = store_path(root).read_bytes()
            file = root / "broken.json"
            file.write_text('{"schema":1,"profiles":{"X":{"Genres":["ABC","abc"]}}}', encoding="utf-8")
            with self.assertRaises(ValueError):
                archive_import(root, file)
            self.assertEqual(store_path(root).read_bytes(), before)

    def test_rename_rejects_duplicate_and_preserves_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            save_profiles(root, load_profiles(root))
            before = store_path(root).read_bytes()
            with self.assertRaisesRegex(ValueError, "existiert"):
                rename_value(root, "HardTechno", "Genres", "Schranz", "Acid Techno")
            self.assertEqual(store_path(root).read_bytes(), before)

    def test_three_preset_slots_are_persistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            numbers = {cat: 2 for cat in CATEGORIES}
            preset_save(root, 1, numbers)
            self.assertEqual(presets_load(root)[1], numbers)

if __name__ == "__main__":
    unittest.main()
