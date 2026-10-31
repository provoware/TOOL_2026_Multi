"""Rückfalltests: Profildaten dürfen beschädigte Typen nicht still umwandeln."""
import json
import tempfile
import unittest
from pathlib import Path

from app.profile_store import CATEGORIES, load_profiles, save_profiles, store_path


class ProfileStoreInvalidTypesTests(unittest.TestCase):
    def test_non_text_values_in_saved_json_are_rejected_without_rewriting(self):
        for invalid in (None, True, 42, {"falsch": "Objekt"}, ["falsche", "Liste"]):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target = store_path(root)
                target.parent.mkdir(parents=True, exist_ok=True)
                profile = {"Test": {category: [] for category in CATEGORIES}}
                profile["Test"]["Genres"] = [invalid]
                original = json.dumps(profile, ensure_ascii=False).encode("utf-8")
                target.write_bytes(original)

                with self.assertRaisesRegex(ValueError, "kein Text"):
                    load_profiles(root)
                self.assertEqual(target.read_bytes(), original)

    def test_invalid_values_cannot_overwrite_existing_profiles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = save_profiles(root, {"Test": {"Genres": ["Ambient"]}})
            original = target.read_bytes()
            for invalid in (None, False, 123, {"falsch": "Objekt"}, ["Liste"]):
                with self.subTest(invalid=invalid):
                    with self.assertRaisesRegex(ValueError, "kein Text"):
                        save_profiles(root, {"Test": {"Genres": [invalid]}})
                    self.assertEqual(target.read_bytes(), original)

    def test_non_text_profile_name_is_rejected_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = save_profiles(root, {"Test": {"Genres": ["Ambient"]}})
            original = target.read_bytes()
            with self.assertRaisesRegex(ValueError, "Profilname muss Text sein"):
                save_profiles(root, {42: {"Genres": ["Ambient"]}})
            self.assertEqual(target.read_bytes(), original)

    def test_valid_text_values_remain_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            save_profiles(root, {"Test": {"Genres": ["Dark Ambient"]}})
            self.assertEqual(load_profiles(root)["Test"]["Genres"], ["Dark Ambient"])


if __name__ == "__main__":
    unittest.main()
