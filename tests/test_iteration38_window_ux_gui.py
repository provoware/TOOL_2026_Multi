import json
import os
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pathlib import Path
from PySide6.QtCore import QRect, QSize
from PySide6.QtWidgets import QApplication

from app.song_editor import SongEditor
from app.song_library import SongLibrary
from app.ui import Dashboard
from app.ui_standards import app_stylesheet, theme_colors
from app.window_state import fit_rect_to_available


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


class Iteration38WindowUxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        for widget in list(self.app.topLevelWidgets()):
            if isinstance(widget, SongEditor):
                widget._closing_after_save = True
            if isinstance(widget, Dashboard):
                widget._closing_after_save = True
            widget.close()
        self.app.processEvents()
        self.temp.cleanup()

    def test_1366x768_geometry_is_kept_inside_visible_work_area(self):
        available = QRect(0, 0, 1366, 728)
        result = fit_rect_to_available(QRect(-1900, -700, 1600, 1000), available, QSize(760, 560))
        self.assertGreaterEqual(result.left(), 16)
        self.assertGreaterEqual(result.top(), 16)
        self.assertLessEqual(result.right(), available.right() - 16)
        self.assertLessEqual(result.bottom(), available.bottom() - 16)
        self.assertGreaterEqual(result.width(), 760)
        self.assertGreaterEqual(result.height(), 560)

    def test_editor_and_library_use_compact_mode_when_height_or_zoom_needs_it(self):
        editor = SongEditor(self.root, zoom_percent=100)
        editor.resize(1180, 700)
        editor.show()
        self.app.processEvents()
        self.assertTrue(editor._compact_mode)
        self.assertFalse(editor.details_frame.isVisible())
        editor.resize(1200, 800)
        self.app.processEvents()
        self.assertFalse(editor._compact_mode)
        self.assertTrue(editor.details_frame.isVisible())
        editor._closing_after_save = True
        editor.close()

        library = SongLibrary(self.root, 150, lambda _path: None)
        library.resize(1200, 800)
        library.show()
        self.app.processEvents()
        self.assertTrue(library._compact_mode)
        self.assertFalse(library.filters_frame.isVisible())
        library.close()

    def test_library_is_hidden_while_editor_is_active_and_returns_after_close(self):
        dashboard = Dashboard(FakeTexts(), FakeLogger(), self.root)
        dashboard.show()
        dashboard.open_song_library()
        self.app.processEvents()
        library = dashboard._song_library
        self.assertIsNotNone(library)
        self.assertTrue(library.isVisible())

        dashboard.open_song_editor()
        self.app.processEvents()
        self.assertFalse(library.isVisible())
        self.assertEqual(len(dashboard._song_editors), 1)
        editor = dashboard._song_editors[0]
        self.assertTrue(editor.isVisible())

        editor.close_safely()
        self.app.processEvents()
        self.assertEqual(dashboard._song_editors, [])
        self.assertTrue(library.isVisible())
        dashboard._closing_after_save = True
        library.close()
        dashboard.close()

    def test_window_geometry_is_saved_portably_without_touching_song_files(self):
        library = SongLibrary(self.root, 100, lambda _path: None)
        library.setGeometry(40, 50, 900, 600)
        library.show()
        self.app.processEvents()
        library.close()
        self.app.processEvents()
        state_file = self.root / "daten" / "ui" / "fenster.json"
        self.assertTrue(state_file.is_file())
        payload = json.loads(state_file.read_text(encoding="utf-8"))
        self.assertIn("song_library", payload)
        self.assertFalse((self.root / "daten" / "songtexte").exists())

    def test_input_fields_are_neutral_until_focus_and_have_status_colors(self):
        colors = theme_colors("Amber")
        css = app_stylesheet(100, "Amber")
        self.assertNotEqual(colors["input_border"], colors["accent"])
        self.assertIn(f"placeholder-text-color:{colors['placeholder']}", css)
        self.assertIn(f"border:2px solid {colors['accent']}", css)
        self.assertIn(f"border:2px solid {colors['red']}", css)
        self.assertIn(f"border:2px solid {colors['green']}", css)

    def test_help_ampersand_is_escaped_for_qt_but_accessible_name_is_literal(self):
        dashboard = Dashboard(FakeTexts(), FakeLogger(), self.root)
        dashboard.show()
        self.app.processEvents()
        self.assertIn("Hilfe && Fehlerhilfe", dashboard.recovery_nav_button.text())
        self.assertEqual(dashboard.recovery_nav_button.accessibleName(), "Hilfe & Fehlerhilfe")
        dashboard._closing_after_save = True
        dashboard.close()


if __name__ == "__main__":
    unittest.main()
