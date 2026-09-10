import json
import tempfile
import unittest
from pathlib import Path

from app.character_store import get_character, list_characters, upsert_character
from app.import_schema import song_document_from_import, song_import_template, song_import_template_text
from app.profile_store import add_values, load_profiles
from app.song_document import normalize_section_name
from app.startup_validation import ensure_runtime_folders, missing_paths
from app.text_editor_store import TextDocument, load_text_document, save_text_document
from app.todo_store import PROJECT_MODULE_BACKLOG, PROJECT_MODULE_SUBTASKS, PROJECT_MODULE_TASK_COUNT, ensure_project_module_backlog, load_state


class Iteration34CoreTests(unittest.TestCase):
    def test_comma_profile_input_is_stored_as_individual_deduplicated_values(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            added = add_values(root, "HardTechno", "Genres", "Gabber, Darktek, gabber,  Acidcore  ,")
            self.assertEqual(added, ["Gabber", "Darktek", "Acidcore"])
            values = load_profiles(root)["HardTechno"]["Genres"]
            self.assertIn("Gabber", values)
            self.assertIn("Darktek", values)
            self.assertIn("Acidcore", values)
            self.assertEqual(sum(value.casefold() == "gabber" for value in values), 1)

    def test_custom_song_section_name_is_normalized_and_brackets_are_rejected(self):
        self.assertEqual(normalize_section_name("  Drop   Finale  "), "Drop Finale")
        with self.assertRaises(ValueError):
            normalize_section_name("[Kaputt]")

    def test_import_template_is_exact_valid_json_and_builds_document(self):
        payload = json.loads(song_import_template_text())
        self.assertEqual(payload, song_import_template())
        document = song_document_from_import(payload)
        self.assertEqual(document.title, "Beispieltitel")
        self.assertEqual(document.sections[-1].kind, "Eigener Bereichsname")

    def test_startup_validation_never_creates_without_permission(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "provoware"
            before = tuple(missing_paths(root))
            self.assertTrue(before)
            self.assertFalse(ensure_runtime_folders(root, lambda _paths: False))
            self.assertFalse(root.exists())

    def test_startup_validation_creates_and_validates_after_permission(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "provoware"
            asked = []
            self.assertTrue(ensure_runtime_folders(root, lambda paths: asked.append(paths) or True))
            self.assertEqual(len(asked), 1)
            self.assertEqual(missing_paths(root), ())
            for name in ("daten", "logs", "berichte", "backups"):
                self.assertTrue((root / name).is_dir())

    def test_character_store_is_reusable_and_searchable(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            saved = upsert_character(root, {
                "name": "Mara", "role": "Hauptfigur", "age": "32",
                "personality": "ruhig, präzise", "motivation": "Wahrheit finden",
                "tags": "mystery, ermittlerin, Mystery",
            })
            self.assertIsNotNone(get_character(root, str(saved["id"])))
            self.assertEqual(saved["tags"], ["mystery", "ermittlerin"])
            self.assertEqual([item["name"] for item in list_characters(root, "präzise")], ["Mara"])

    def test_text_editor_title_becomes_filename_and_notes_survive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            document = TextDocument(
                title="Meine Szene", text="Erster Absatz", notes="Noch überarbeiten",
                character_ids=["abc", "abc", "def"],
            )
            path = save_text_document(root, document)
            self.assertEqual(path.name, "Meine Szene.json")
            loaded = load_text_document(path)
            self.assertEqual(loaded.notes, "Noch überarbeiten")
            self.assertEqual(loaded.character_ids, ["abc", "def"])

    def test_project_module_backlog_is_idempotent_and_preserves_existing_todos(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = ensure_project_module_backlog(root)
            second = ensure_project_module_backlog(root)
            self.assertEqual(first, PROJECT_MODULE_TASK_COUNT)
            self.assertEqual(second, 0)
            state = load_state(root)
            self.assertEqual(len(state["active"]), PROJECT_MODULE_TASK_COUNT)
            self.assertGreater(len(PROJECT_MODULE_SUBTASKS), 40)
            titles = {task["title"] for task in state["active"]}
            self.assertTrue(any("Charakterfibel" in title for title in titles))
            self.assertTrue(any("Wikimodul" in title for title in titles))
            self.assertTrue(any("Updatemodul" in title for title in titles))


if __name__ == "__main__":
    unittest.main()
