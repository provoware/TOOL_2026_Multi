"""Regressionen für Favoriten, Monatsstatistik und sichere GitHub-Projektdaten."""
import json
import random
import tempfile
import unittest
from datetime import date
from pathlib import Path

from app.genre_favorites import (
    favorite_values, set_favorite, monthly_statistics, monthly_report_text,
    export_monthly_report, load_favorites,
)
from app.genre_random import generate, history_load, history_path
from app.github_projects import (
    catalog_path, delete_project, export_projects, import_projects,
    load_projects, upsert_project,
)
from app.profile_store import CATEGORIES, add_values


class FavoritesAndMonthlyTests(unittest.TestCase):
    def test_star_favorites_and_favorites_only_generation_persist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            add_values(root, "HardTechno", "Genres", "SonderTechno")
            self.assertTrue(set_favorite(root, "HardTechno", "Genres", "SonderTechno", True))
            self.assertFalse(set_favorite(root, "HardTechno", "Genres", "sondertechno", True))
            self.assertEqual(favorite_values(root, "HardTechno", "Genres"), ["SonderTechno"])
            counts = {cat: 0 for cat in CATEGORIES}
            counts["Genres"] = 1
            result = generate(root, "HardTechno", counts, rng=random.Random(3),
                              favorites_only=True)
            self.assertEqual(result["output"], "SonderTechno")
            self.assertTrue(history_load(root)[0]["favorites_only"])
            self.assertEqual(len(load_favorites(root)["HardTechno"]["Genres"]), 1)
            self.assertTrue(set_favorite(root, "HardTechno", "Genres", "SonderTechno", False))
            with self.assertRaisesRegex(ValueError, "nur"):
                generate(root, "HardTechno", counts, favorites_only=True)
            self.assertEqual(len(history_load(root)), 1)

    def test_report_is_genre_only_cutoff_inclusive_and_txt_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            add_values(root, "HardTechno", "Genres", "SonderTechno")
            set_favorite(root, "HardTechno", "Genres", "SonderTechno", True)
            counts = {cat: 0 for cat in CATEGORIES}
            counts["Genres"] = 1
            generate(root, "HardTechno", counts, favorites_only=True)
            import datetime
            today = datetime.date.today()
            stats = monthly_statistics(root, today)
            self.assertEqual(stats["total"], 1)
            self.assertEqual(stats["favorite_draws"], 1)
            report = monthly_report_text(root, today)
            self.assertIn("Genres-Zufall", report)
            self.assertIn("Favoriten-Ziehungen: 1", report)
            self.assertNotIn("GitHub-Projekte", report)
            dest = root / "monatsbericht.txt"
            export_monthly_report(root, today, dest)
            self.assertEqual(dest.read_text(encoding="utf-8"), report)
            with self.assertRaises(ValueError):
                export_monthly_report(root, today, root / "daten" / "profile" / "verlauf.txt")

    def test_corrupt_favorite_file_does_not_overwrite_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            set_favorite(root, "HardTechno", "Genres", "Schranz", True)
            from app.genre_favorites import favorites_path
            path = favorites_path(root)
            path.write_text("{kaputt", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                set_favorite(root, "HardTechno", "Genres", "Acid Techno", True)
            self.assertEqual(path.read_text(encoding="utf-8"), "{kaputt")


    def test_malformed_monthly_history_categories_fail_without_changing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = history_path(root)
            path.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "timestamp": "2026-10-27T12:00:00+01:00",
                "profile": "HardTechno", "output": "Schranz",
                "amounts": {cat: int(cat == "Genres") for cat in CATEGORIES},
            }
            for invalid in (None, "ungueltig", {"Genres": [{"falsch": "Wert"}]},
                            {"Genres": [None]}):
                with self.subTest(categories=repr(invalid)):
                    path.write_text(json.dumps([{**entry, "categories": invalid}]), encoding="utf-8")
                    original = path.read_bytes()
                    with self.assertRaisesRegex(ValueError, "Verlaufs-Kategorienfeld"):
                        monthly_statistics(root, date(2026, 10, 27))
                    self.assertEqual(path.read_bytes(), original)
            path.write_text(json.dumps([{**entry, "categories": {"Genres": ["Schranz"]}}]),
                            encoding="utf-8")
            self.assertEqual(monthly_statistics(root, date(2026, 10, 27))["most_common"],
                             [("Schranz", 1)])


class GithubProjectStoreTests(unittest.TestCase):
    @staticmethod
    def example(**extra):
        data = dict(project="Werkzeug", repo="provoware/werkzeug",
                    url="https://github.com/provoware/werkzeug",
                    notes="Lokale Notiz", status="offen",
                    todos=[{"text": "Prüfen", "done": False}])
        data.update(extra)
        return data

    def test_create_edit_finish_delete_and_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = upsert_project(root, **self.example())
            self.assertEqual(load_projects(root)[0]["id"], first["id"])
            updated = upsert_project(root, ident=first["id"],
                                     **self.example(status="fertig",
                                                    todos=[{"text": "Prüfen", "done": True}]))
            self.assertEqual(updated["id"], first["id"])
            self.assertEqual(load_projects(root)[0]["status"], "fertig")
            self.assertTrue(load_projects(root)[0]["todos"][0]["done"])
            delete_project(root, first["id"])
            self.assertEqual(load_projects(root), [])

    def test_duplicate_and_malformed_url_are_rejected_atomically(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upsert_project(root, **self.example())
            before = catalog_path(root).read_bytes()
            for altered in [
                self.example(project="Doppelt"),
                self.example(project="Werkzeug", repo="anderer/name",
                             url="https://github.com/anderer/name"),
                self.example(project="Falsch", repo="anders/name",
                             url="https://notgithub.com/anders/name"),
                self.example(project="Falsch", repo="anders/name",
                             url="https://github.com/anders/name?token=secret"),
            ]:
                with self.assertRaises(ValueError):
                    upsert_project(root, **altered)
                self.assertEqual(catalog_path(root).read_bytes(), before)

    def test_export_and_safe_idempotent_import(self):
        with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as target:
            source_root, target_root = Path(source), Path(target)
            upsert_project(source_root, **self.example())
            backup = export_projects(source_root, source_root / "alle.json")
            self.assertEqual(import_projects(target_root, backup), 1)
            self.assertEqual(import_projects(target_root, backup), 0)
            self.assertEqual(load_projects(target_root)[0]["notes"], "Lokale Notiz")

    def test_corrupted_import_rolls_back_without_partial_updates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upsert_project(root, **self.example())
            before = catalog_path(root).read_bytes()
            file = root / "invalid.json"
            file.write_text(json.dumps({"schema": 1, "projects": [
                {"id": "0" * 32, "project": "Gefälscht", "repo": "provoware/x",
                 "url": "https://github.com/provoware/x", "notes": "",
                 "status": "offen", "todos": []},
                {"id": "a" * 32, "project": "Schlecht", "repo": "x/x",
                 "url": "https://example.com/x/x", "notes": "",
                 "status": "offen", "todos": []}
            ]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                import_projects(root, file)
            self.assertEqual(catalog_path(root).read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
