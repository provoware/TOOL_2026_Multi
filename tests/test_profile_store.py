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

    def test_corrupt_duplicate_values_are_rejected_not_silently_removed(self):
        target = store_path(self.root)
        target.parent.mkdir(parents=True, exist_ok=True)
        broken = {"Test": {category: [] for category in CATEGORIES}}
        broken["Test"]["Genres"] = ["Ambient", "ambient"]
        target.write_text(json.dumps(broken), encoding="utf-8")
        with self.assertRaises(ValueError):
            load_profiles(self.root)

    def test_remove_value_persists_without_touching_other_categories(self):
        profiles = load_profiles(self.root)
        before_moods = list(profiles["HardTechno"]["Stimmungen"])
        remove_value(self.root, "HardTechno", "Genres", "Schranz")
        after = load_profiles(self.root)
        self.assertNotIn("Schranz", after["HardTechno"]["Genres"])
        self.assertEqual(before_moods, after["HardTechno"]["Stimmungen"])

    def test_control_characters_in_profile_name_are_rejected(self):
        with self.assertRaises(ValueError):
            add_profile(self.root, "falsch\nzweite Zeile")

    def test_slash_is_allowed_for_fachprofile(self):
        profiles = load_profiles(self.root)
        self.assertIn("HipHop/Rap", profiles)

    def test_atomic_replace_failure_preserves_existing_file(self):
        target = save_profiles(self.root, DEFAULT_PROFILES)
        before = target.read_bytes()
        changed = load_profiles(self.root)
        changed["HardTechno"]["Genres"].append("Testgenre")
        with patch("app.atomic_io.os.replace", side_effect=OSError("simuliert")):
            with self.assertRaises(OSError):
                save_profiles(self.root, changed)
        self.assertEqual(before, target.read_bytes())
        self.assertEqual(list(target.parent.glob(f".{target.name}.*.tmp")), [])

    def test_saved_json_is_valid(self):
        add_profile(self.root, "Eigene Sammlung")
        data = json.loads(store_path(self.root).read_text(encoding="utf-8"))
        self.assertIn("Eigene Sammlung", data)


if __name__ == "__main__":
    unittest.main()
