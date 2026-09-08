import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from app.profile_editor import ProfileEditor
from app.profile_store import add_value, load_profiles
from app.ui import Dashboard


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


class ProfileGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_editor_switches_profile_and_category(self):
        editor = ProfileEditor(self.root, initial_category="Stimmungen")
        editor.show()
        self.app.processEvents()
        self.assertEqual(editor.category_combo.currentText(), "Stimmungen")
        self.assertGreaterEqual(editor.profile_combo.count(), 3)
        editor.profile_combo.setCurrentText("HardTechno")
        self.app.processEvents()
        visible = [editor.values_list.item(i).text() for i in range(editor.values_list.count())]
        self.assertIn("treibend", visible)
        editor.close()

    def test_dashboard_profile_selection_populates_matching_values(self):
        dashboard = Dashboard(FakeTexts(), FakeLogger(), self.root)
        dashboard.show()
        self.app.processEvents()
        dashboard.db_profile_combo.setCurrentText("HipHop/Rap")
        self.app.processEvents()
        genres = [dashboard.db_boxes["Genres"].itemText(i) for i in range(dashboard.db_boxes["Genres"].count())]
        self.assertIn("Boom Bap", genres)
        self.assertNotIn("Schranz", genres)
        dashboard._closing_after_save = True
        dashboard.close()

    def test_editor_change_refreshes_dashboard_without_restart(self):
        dashboard = Dashboard(FakeTexts(), FakeLogger(), self.root)
        dashboard.show()
        self.app.processEvents()
        add_value(self.root, "HardTechno", "Genres", "Hardgroove")
        dashboard.refresh_db_profiles()
        dashboard.db_profile_combo.setCurrentText("HardTechno")
        self.app.processEvents()
        genres = [dashboard.db_boxes["Genres"].itemText(i) for i in range(dashboard.db_boxes["Genres"].count())]
        self.assertIn("Hardgroove", genres)
        dashboard._closing_after_save = True
        dashboard.close()

    def test_defaults_cover_requested_profiles(self):
        profiles = load_profiles(self.root)
        self.assertEqual({"HardTechno", "HipHop/Rap", "Hörspiele"} - set(profiles), set())


if __name__ == "__main__":
    unittest.main()
