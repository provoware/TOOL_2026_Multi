"""GUI-Regression: Sternauswahl, Monatsvorschau und lokales Projektregister."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from app.genre_random_window import GenreRandomWindow
from app.genre_random import history_load
from app.genre_favorites import monthly_report_text
from app.github_projects_window import GitHubProjectsWindow
from app.github_projects import load_projects


class FavoritesAndProjectsGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_star_favorite_generation_and_genre_only_month_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            window = GenreRandomWindow(root)
            try:
                window.profile_combo.setCurrentText("HardTechno")
                window.category_combo.setCurrentText("Genres")
                item = next(window.archive_list.item(i) for i in range(window.archive_list.count())
                            if window.archive_list.item(i).data(Qt.UserRole).casefold() == "schranz")
                window.archive_list.setCurrentItem(item)
                window.toggle_favorite()
                item = next(window.archive_list.item(i) for i in range(window.archive_list.count())
                            if window.archive_list.item(i).data(Qt.UserRole).casefold() == "schranz")
                self.assertTrue(item.text().startswith("★ "))
                for spin in window.spins.values():
                    spin.setValue(0)
                window.spins["Genres"].setValue(1)
                window.only_favorites.setChecked(True)
                window.generate_result()
                self.assertEqual(window.output.toPlainText().casefold(), "schranz")
                self.assertEqual(self.app.clipboard().text(), window.output.toPlainText())
                self.assertTrue(history_load(root)[0]["favorites_only"])
                with patch.object(QMessageBox, "information") as popup:
                    window.report_preview()
                    self.assertIn("Genres-Zufall", popup.call_args.args[2])
                self.assertIn("Favoriten-Ziehungen: 1",
                              monthly_report_text(root, window._report_date()))
            finally:
                window.close()

    def test_project_editor_copy_edit_and_status_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            window = GitHubProjectsWindow(root)
            try:
                window.project.setText("Werkzeug A")
                window.repo.setText("provoware/werkzeug-a")
                window.url.setText("https://github.com/provoware/werkzeug-a")
                window.notes.setPlainText("Projektstand und wichtigste Notizen")
                window.todo_input.setText("Tests ausführen")
                window.add_todo()
                window.save_current()
                self.assertEqual(window.list.count(), 1)
                self.assertEqual(load_projects(root)[0]["status"], "offen")
                window.status_combo.setCurrentIndex(1)
                window.save_current()
                self.assertEqual(load_projects(root)[0]["status"], "fertig")
                self.assertEqual(len(load_projects(root)[0]["todos"]), 1)
                window._copy(window.url.text())
                self.assertEqual(self.app.clipboard().text(),
                                 "https://github.com/provoware/werkzeug-a")
            finally:
                window.close()


if __name__ == "__main__":
    unittest.main()
