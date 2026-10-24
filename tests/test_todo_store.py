import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.todo_store import (
    active_tasks, add_task, archived_tasks, complete_task, load_state, save_state, store_path,
)


class TodoStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_empty_start_does_not_create_user_file(self):
        state = load_state(self.root)
        self.assertEqual(state["active"], [])
        self.assertEqual(state["archive"], [])
        self.assertFalse(store_path(self.root).exists())

    def test_add_task_with_optional_due(self):
        task = add_task(self.root, "  Rechnung   bezahlen ", "Notiz", "2026-09-10T14:30")
        self.assertEqual(task["title"], "Rechnung bezahlen")
        self.assertEqual(task["due"], "2026-09-10T14:30")
        loaded = active_tasks(self.root)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["note"], "Notiz")

    def test_due_rejects_timezone_to_match_calendar_local_time(self):
        with self.assertRaises(ValueError):
            add_task(self.root, "Test", due="2026-09-10T14:30+02:00")
        self.assertFalse(store_path(self.root).exists())

    def test_complete_moves_task_to_archive_without_deleting_it(self):
        task = add_task(self.root, "Test")
        moved = complete_task(self.root, str(task["id"]))
        self.assertIsNotNone(moved["completed_at"])
        self.assertEqual(active_tasks(self.root), [])
        archive = archived_tasks(self.root)
        self.assertEqual(len(archive), 1)
        self.assertEqual(archive[0]["id"], task["id"])
        self.assertEqual(archive[0]["title"], "Test")

    def test_invalid_due_and_empty_title_are_rejected(self):
        with self.assertRaises(ValueError):
            add_task(self.root, "")
        with self.assertRaises(ValueError):
            add_task(self.root, "Test", due="morgen irgendwann")
        self.assertFalse(store_path(self.root).exists())

    def test_atomic_replace_failure_preserves_previous_state(self):
        add_task(self.root, "Vorher")
        target = store_path(self.root)
        before = target.read_bytes()
        state = load_state(self.root)
        state["active"].append({
            "id": "zweite", "title": "Zweite", "note": "", "due": None,
            "created_at": "2026-09-08T04:00:00+00:00", "completed_at": None,
        })
        with patch("app.atomic_io.os.replace", side_effect=OSError("simuliert")):
            with self.assertRaises(OSError):
                save_state(self.root, state)
        self.assertEqual(before, target.read_bytes())
        self.assertEqual(list(target.parent.glob(f".{target.name}.*.tmp")), [])

    def test_saved_json_contains_both_lists(self):
        task = add_task(self.root, "Archivtest")
        complete_task(self.root, str(task["id"]))
        data = json.loads(store_path(self.root).read_text(encoding="utf-8"))
        self.assertEqual(data["active"], [])
        self.assertEqual(len(data["archive"]), 1)
        self.assertEqual(data["schema_version"], 1)


    def test_personal_and_development_views_use_ids_and_preserve_source_bytes(self):
        from app.todo_store import ensure_project_module_backlog, task_groups
        ensure_project_module_backlog(self.root)
        legacy = load_state(self.root)['active'][0]
        personal = add_task(self.root, legacy['title'], 'Eigene Aufgabe mit gleichem Namen')
        complete_task(self.root, legacy['id'])
        before = store_path(self.root).read_bytes()
        groups = task_groups(self.root)
        self.assertEqual([item['id'] for item in groups['active']], [personal['id']])
        self.assertEqual(groups['archive'], [])
        self.assertTrue(any(item['id'] == legacy['id'] and item['completed_at'] for item in groups['development']))
        self.assertEqual(store_path(self.root).read_bytes(), before)
        self.assertEqual(sum(map(len, groups.values())), sum(len(v) for k, v in load_state(self.root).items() if k != 'schema_version'))

    def test_modified_legacy_title_remains_recognizable_and_reads_one_snapshot(self):
        from app.todo_store import ensure_project_module_backlog, task_groups
        ensure_project_module_backlog(self.root)
        state = load_state(self.root)
        state['active'][0]['title'] = 'Von mir umbenannter Altauftrag'
        save_state(self.root, state)
        with patch('app.todo_store.load_state', return_value=state) as load:
            groups = task_groups(self.root)
        load.assert_called_once_with(self.root)
        self.assertFalse(groups['active'])
        self.assertTrue(any(item['title'] == 'Von mir umbenannter Altauftrag' for item in groups['development']))

    def test_legacy_separation_survives_backup_and_restore(self):
        from app.todo_store import ensure_project_module_backlog, task_groups
        from scripts.datensicherung import create, restore
        ensure_project_module_backlog(self.root)
        personal = add_task(self.root, 'Meine Aufgabe')
        complete_task(self.root, personal['id'])
        before = store_path(self.root).read_bytes()
        archive = create(self.root / 'daten', self.root / 'backup')
        restored = self.root / 'wiederhergestellt'
        restore(archive, restored)
        self.assertEqual(store_path(restored).read_bytes(), before)
        self.assertEqual(task_groups(restored), task_groups(self.root))


if __name__ == "__main__":
    unittest.main()
