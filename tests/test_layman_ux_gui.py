import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QHeaderView, QPushButton

from app.calendar_window import CalendarWindow
from app.profile_editor import ProfileEditor
from app.recovery_center import RecoveryCenter
from app.song_document import SongDocument, SongSection
from app.song_editor import SongEditor
from app.song_library import SongLibrary
from app.todo_window import TodoWindow
from app.ui import Dashboard
from app.ui_standards import COLORS, UI_FONT_FAMILY


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


def _rgb(hex_color: str) -> tuple[float, float, float]:
    return tuple(int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5))


def _luminance(hex_color: str) -> float:
    channels = []
    for channel in _rgb(hex_color):
        channels.append(channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _contrast(a: str, b: str) -> float:
    first, second = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (first + 0.05) / (second + 0.05)


class LaymanUxGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.dashboard = Dashboard(FakeTexts(), FakeLogger(), self.root)
        self.dashboard.show()
        self.app.processEvents()

    def tearDown(self):
        self.dashboard._closing_after_save = True
        self.dashboard.close()
        self.app.processEvents()
        self.temp.cleanup()

    def test_dashboard_names_actions_truthfully(self):
        self.assertIn("Songs", self.dashboard.search_entry.placeholderText())
        self.assertEqual(self.dashboard.quit_button.text(), "Programm beenden")
        self.assertEqual(self.dashboard.quick_info_label.text(), "Projekt-Notiz:")
        buttons = self.dashboard.findChildren(QPushButton)
        self.assertTrue(any(button.text().startswith("①  Songtexte öffnen") for button in buttons))
        self.assertFalse(any(button.text() == "Logout" for button in buttons))

    def test_planned_tiles_are_visibly_marked(self):
        tiles = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.objectName() == "tileButton"
        ]
        self.assertEqual(len(tiles), 7)
        planned = [button for button in tiles if button.property("planned") is True]
        self.assertEqual(len(planned), 5)
        self.assertTrue(all("In Planung" in button.text() for button in planned))

    def test_empty_song_library_has_visible_new_song_entry(self):
        self.dashboard.open_song_library()
        self.app.processEvents()
        library = self.dashboard._song_library
        self.assertIsNotNone(library)
        buttons = library.findChildren(QPushButton)
        self.assertTrue(any("Neuen Song schreiben" in button.text() for button in buttons))
        self.assertIn("Neuen Song schreiben", library.status_label.text())

    def test_subwindows_explain_the_next_step(self):
        todo = TodoWindow(self.root)
        calendar = CalendarWindow(self.root)
        profile = ProfileEditor(self.root)
        library = SongLibrary(self.root, 100, lambda _path: None)
        editor = SongEditor(
            self.root,
            document=SongDocument(title="Test", sections=[SongSection("Strophe"), SongSection("Refrain")]),
        )
        recovery = RecoveryCenter(FakeTexts(), FakeLogger())
        try:
            self.assertIn("Aufgabe", todo.status_label.text())
            self.assertIn("Datum", calendar.status_label.text())
            self.assertIn("Profil", profile.status_label.text())
            self.assertIn("Song", library.search_entry.placeholderText())
            self.assertIn("automatisch", editor.status_label.text())
            self.assertIn("Fehlerhilfe", recovery.windowTitle())
        finally:
            editor._closing_after_save = True
            editor.close()
            todo.close()
            calendar.close()
            profile.close()
            library.close()
            recovery.close()
            self.app.processEvents()

    def test_song_library_never_fails_silently_without_selection(self):
        library = SongLibrary(self.root, 100, lambda _path: None)
        try:
            with patch("app.song_library.QMessageBox.information") as info:
                library.open_selected()
                library.show_versions()
                self.assertEqual(info.call_count, 2)
        finally:
            library.close()

    def test_song_section_removal_requires_confirmation(self):
        editor = SongEditor(
            self.root,
            document=SongDocument(title="Test", sections=[SongSection("Strophe"), SongSection("Refrain")]),
        )
        try:
            self.assertEqual(len(editor.document.sections), 2)
            with patch("app.song_editor.QMessageBox.question", return_value=0):
                editor.remove_section()
            self.assertEqual(len(editor.document.sections), 2)
        finally:
            editor._closing_after_save = True
            editor.close()

    def test_responsive_dashboard_changes_space_distribution(self):
        self.dashboard.resize(1020, 700)
        self.app.processEvents()
        compact_sidebar = self.dashboard.sidebar.width()
        compact_search = self.dashboard.search_entry.width()

        self.dashboard.resize(1500, 850)
        self.app.processEvents()
        self.assertGreater(self.dashboard.sidebar.width(), compact_sidebar)
        self.assertGreater(self.dashboard.search_entry.width(), compact_search)

    def test_zoom_keeps_core_controls_accessible_at_compact_effective_width(self):
        self.dashboard.resize(1280, 790)
        self.dashboard.set_zoom(125)
        self.app.processEvents()
        self.assertGreaterEqual(self.dashboard.sidebar.width(), 190)
        self.assertGreaterEqual(self.dashboard.search_entry.width(), 180)
        self.assertTrue(self.dashboard.search_entry.isVisible())
        nav_scroll = getattr(self.dashboard, "_provoware_nav_scroll", None)
        self.assertIsNotNone(nav_scroll)
        self.assertTrue(nav_scroll.isVisible())

    def test_song_library_columns_use_available_width(self):
        library = SongLibrary(self.root, 100, lambda _path: None)
        library.resize(1180, 720)
        library.show()
        self.app.processEvents()
        try:
            header = library.table.header()
            self.assertEqual(header.sectionResizeMode(0), QHeaderView.Stretch)
            self.assertEqual(header.sectionResizeMode(5), QHeaderView.Stretch)
            self.assertEqual(header.sectionResizeMode(7), QHeaderView.ResizeToContents)
        finally:
            library.close()

    def test_modern_font_and_core_contrasts(self):
        self.assertEqual(self.dashboard.font().family(), UI_FONT_FAMILY)
        self.assertGreaterEqual(_contrast(COLORS["text"], COLORS["background"]), 4.5)
        self.assertGreaterEqual(_contrast(COLORS["muted"], COLORS["background"]), 4.5)
        self.assertGreaterEqual(_contrast(COLORS["accent"], COLORS["background"]), 4.5)


if __name__ == "__main__":
    unittest.main()
