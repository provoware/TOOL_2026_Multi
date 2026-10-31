"""PV-TODO-LINK-01: Keine Lese- oder Schreibzugriffe über Daten-Verknüpfungen."""
import tempfile
import unittest
from pathlib import Path

from app.todo_store import add_task, empty_state, load_state, save_state, store_path


class TodoStoreLinkTests(unittest.TestCase):
    def test_existing_and_broken_links_are_rejected_without_external_writes(self):
        for component in ("daten", "todo", "todo.json"):
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
                            external_file = destination / "todo" / "todo.json"
                        elif component == "todo":
                            link = root / "daten" / "todo"
                            destination = outside / "todo"
                            external_file = destination / "todo.json"
                        else:
                            link = root / "daten" / "todo" / "todo.json"
                            destination = outside / "todo.json"
                            external_file = destination
                        link.parent.mkdir(parents=True, exist_ok=True)
                        if not dangling:
                            external_file.parent.mkdir(parents=True, exist_ok=True)
                            external_file.write_text(
                                '{"schema_version": 1, "active": [], "archive": []}',
                                encoding="utf-8",
                            )
                            before = external_file.read_bytes()
                        link.symlink_to(destination, target_is_directory=component != "todo.json")

                        for operation in (
                            lambda: load_state(root),
                            lambda: add_task(root, "Neue Aufgabe"),
                            lambda: save_state(root, empty_state()),
                        ):
                            with self.assertRaisesRegex(ValueError, "Verknüpfungen"):
                                operation()
                        if dangling:
                            self.assertFalse(destination.exists())
                        else:
                            self.assertEqual(external_file.read_bytes(), before)

    def test_regular_todo_path_remains_usable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = add_task(root, "Normale Aufgabe")
            self.assertEqual(load_state(root)["active"][0]["id"], task["id"])
            self.assertTrue(store_path(root).is_file())


if __name__ == "__main__":
    unittest.main()
