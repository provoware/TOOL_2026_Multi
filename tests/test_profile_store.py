import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.profile_store import (
    CATEGORIES, DEFAULT_PROFILES, add_profile, add_value, load_profiles,
    remove_value, save_profiles, store_path,
)


class ProfileStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_defaults_are_available_without_writing_user_file(self):
        profiles = load_profiles(self.root)
        self.assertIn("HardTechno", profiles)
        self.assertIn("HipHop/Rap", profiles)
        self.assertIn("Hörspiele", profiles)
        self.assertFalse(store_path(self.root).exists())
        self.assertEqual(set(profiles["HardTechno"]), set(CATEGORIES))

    def test_profile_and_values_are_isolated_and_duplicates_rejected(self):
        add_profile(self.root, "Ambient")
        add_value(self.root, "Ambient", "Genres", "Dark Ambient")
        profiles = load_profiles(self.root)
        self.assertIn("Dark Ambient", profiles["Ambient"]["Genres"])
        self.assertNotIn("Dark Ambient", profiles["HardTechno"]["Genres"])
        with self.assertRaises(ValueError):
            add_value(self.root, "Ambient", "Genres", "dark ambient")

    def test_remove_value_persists_without_touching_other_categories(self):
        profiles = load_profiles(self.root)
        before_moods = list(profiles["HardTechno"]["Stimmungen"])
        remove_value(self.root, "HardTechno", "Genres", "Schranz")
        after = load_profiles(self.root)
        self.assertNotIn("Schranz", after["HardTechno"]["Genres"])
        self.assertEqual(before_moods, after["HardTechno"]["Stimmungen"])

    def test_invalid_profile_name_is_rejected(self):
        with self.assertRaises(ValueError):
            add_profile(self.root, "../falsch")

    def test_atomic_replace_failure_preserves_existing_file(self):
        target = save_profiles(self.root, DEFAULT_PROFILES)
        before = target.read_bytes()
        changed = load_profiles(self.root)
        changed["HardTechno"]["Genres"].append("Testgenre")
        with patch("app.profile_store.os.replace", side_effect=OSError("simuliert")):
            with self.assertRaises(OSError):
                save_profiles(self.root, changed)
        self.assertEqual(before, target.read_bytes())
        self.assertFalse(target.with_suffix(target.suffix + ".tmp").exists())

    def test_saved_json_is_valid(self):
        add_profile(self.root, "Eigene Sammlung")
        data = json.loads(store_path(self.root).read_text(encoding="utf-8"))
        self.assertIn("Eigene Sammlung", data)


if __name__ == "__main__":
    unittest.main()
