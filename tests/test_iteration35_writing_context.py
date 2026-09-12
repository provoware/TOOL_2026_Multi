import tempfile
import unittest
from pathlib import Path

from app.character_store import character_marker, character_options, upsert_character


class Iteration35WritingContextTests(unittest.TestCase):
    def test_character_options_are_sorted_and_use_one_shared_label_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            second = upsert_character(root, {"name": "Zora", "role": "Gegenspielerin"})
            first = upsert_character(root, {"name": "Ada", "role": "Erzählerin"})

            options = character_options(root)

            self.assertEqual([option.name for option in options], ["Ada", "Zora"])
            self.assertEqual(options[0].character_id, str(first["id"]))
            self.assertEqual(options[0].label, "Ada — Erzählerin")
            self.assertEqual(options[0].reference, "Ada (Erzählerin)")
            self.assertEqual(options[1].character_id, str(second["id"]))

    def test_character_marker_uses_stable_id_and_rejects_missing_character(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            saved = upsert_character(root, {"name": "Nora", "role": "Hauptfigur"})

            self.assertEqual(
                character_marker(root, str(saved["id"])),
                "[Charakter: Nora (Hauptfigur)]",
            )
            with self.assertRaises(ValueError):
                character_marker(root, "nicht-vorhanden")


if __name__ == "__main__":
    unittest.main()
