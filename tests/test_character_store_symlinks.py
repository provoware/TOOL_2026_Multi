"""Rückfalltests: Charakterdaten dürfen keine fremden Verknüpfungsziele nutzen."""
import tempfile
import unittest
from pathlib import Path

from app.character_store import empty_state, load_state, save_state, upsert_character


class CharacterStoreLinkTests(unittest.TestCase):
    def test_existing_and_broken_links_are_rejected_without_external_writes(self):
        for component in ("daten", "charaktere", "charaktere.json"):
            for dangling in (False, True):
                with self.subTest(component=component, dangling=dangling):
                    with tempfile.TemporaryDirectory() as tmp:
                        root = Path(tmp) / "projekt"
                        root.mkdir()
                        outside = Path(tmp) / "ausserhalb"
                        outside.mkdir()
                        if component == "daten":
                            link = root / "daten"
                            destination = outside / "daten"
                            external_file = destination / "charaktere" / "charaktere.json"
                        elif component == "charaktere":
                            link = root / "daten" / "charaktere"
                            destination = outside / "charaktere"
                            external_file = destination / "charaktere.json"
                        else:
                            link = root / "daten" / "charaktere" / "charaktere.json"
                            destination = outside / "charaktere.json"
                            external_file = destination
                        link.parent.mkdir(parents=True, exist_ok=True)
                        if not dangling:
                            external_file.parent.mkdir(parents=True, exist_ok=True)
                            external_file.write_text(
                                '{"schema_version": 1, "characters": []}', encoding="utf-8"
                            )
                            before = external_file.read_bytes()
                        link.symlink_to(destination, target_is_directory=component != "charaktere.json")

                        for operation in (
                            lambda: load_state(root),
                            lambda: upsert_character(root, {"name": "Testfigur"}),
                            lambda: save_state(root, empty_state()),
                        ):
                            with self.assertRaisesRegex(ValueError, "Verknüpfungen"):
                                operation()
                        self.assertTrue(link.is_symlink())
                        if dangling:
                            self.assertFalse(destination.exists())
                        else:
                            self.assertEqual(external_file.read_bytes(), before)

    def test_regular_character_path_remains_usable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            character = upsert_character(root, {"name": "Testfigur"})
            self.assertEqual(load_state(root)["characters"][0]["id"], character["id"])


if __name__ == "__main__":
    unittest.main()
