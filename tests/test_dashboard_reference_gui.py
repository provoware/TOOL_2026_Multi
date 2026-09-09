import os
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFrame, QPushButton

from app.ui import Dashboard
from app.ui_standards import (
    COLORS, DEFAULT_THEME, THEMES, THEME_NAMES, geometry_scaled, scaled,
    set_application_theme,
)


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


def _luminance(hex_color: str) -> float:
    channels = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]

    def linear(value: float) -> float:
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = map(linear, channels)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _contrast(first: str, second: str) -> float:
    light, dark = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


class DashboardReferenceGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.app.setProperty("provowareTheme", DEFAULT_THEME)
        self.temp = tempfile.TemporaryDirectory()
        self.dashboard = Dashboard(FakeTexts(), FakeLogger(), Path(self.temp.name))
        self.dashboard.resize(1280, 790)
        self.dashboard.show()
        self.app.processEvents()

    def tearDown(self):
        set_application_theme(DEFAULT_THEME)
        self.dashboard._closing_after_save = True
        self.dashboard.close()
        self.app.processEvents()
        self.temp.cleanup()

    def test_reference_title_framework_and_modern_dark_accent_theme(self):
        self.assertEqual(self.dashboard.windowTitle(), "Provoware-Datenbank-Dashboard 2026")
        self.assertEqual(COLORS["accent"], "#FFB11B")
        self.assertLess(int(COLORS["background"][1:3], 16), 20)
        self.assertTrue(type(self.dashboard).__mro__[1].__module__.startswith("PySide6"))

    def test_reference_has_sidebar_tile_strip_and_responsive_two_by_two_cards(self):
        self.assertGreaterEqual(self.dashboard.sidebar.width(), 210)
        self.assertLessEqual(self.dashboard.sidebar.width(), 240)
        cards = [frame for frame in self.dashboard.findChildren(QFrame) if frame.objectName() == "card"]
        self.assertEqual(len(cards), 4)
        widths = [card.width() for card in cards]
        heights = [card.height() for card in cards]
        self.assertGreater(min(widths), 300)
        self.assertLess(max(widths) / min(widths), 1.40)
        self.assertGreater(min(heights), 180)
        self.assertLess(max(heights) / min(heights), 1.30)
        tiles = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.objectName() == "tileButton"
        ]
        self.assertEqual(len(tiles), 7)

    def test_responsive_sidebar_and_search_follow_window_width(self):
        self.dashboard.resize(1020, 700)
        self.app.processEvents()
        self.assertEqual(self.dashboard.sidebar.width(), 198)
        self.assertEqual(self.dashboard.search_entry.width(), 190)

        self.dashboard.resize(1500, 850)
        self.app.processEvents()
        self.assertEqual(self.dashboard.sidebar.width(), 258)
        self.assertEqual(self.dashboard.search_entry.width(), 320)

    def test_high_zoom_keeps_font_growth_but_caps_geometry_growth(self):
        self.assertEqual(scaled(10, 200), 20)
        self.assertEqual(geometry_scaled(54, 100), 54)
        self.assertLessEqual(geometry_scaled(54, 200), 68)
        self.assertLess(geometry_scaled(54, 200), scaled(54, 200))

    def test_high_zoom_removes_redundant_planning_duplicates_and_restores_them(self):
        self.dashboard.resize(1600, 900)
        self.dashboard.set_zoom(200)
        self.app.processEvents()

        planned_nav = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.objectName() == "navButton" and button.property("planned") is True
        ]
        self.assertTrue(planned_nav)
        self.assertTrue(all(not button.isVisible() for button in planned_nav))

        cards = [frame for frame in self.dashboard.findChildren(QFrame) if frame.objectName() == "card"]
        visible_cards = [card for card in cards if card.isVisible()]
        self.assertEqual(len(visible_cards), 2)

        tiles = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.objectName() == "tileButton"
        ]
        self.assertEqual(len(tiles), 7)
        self.assertTrue(all(button.isVisible() for button in tiles))
        self.assertTrue(self.dashboard.theme_combo.isVisible())

        self.dashboard.set_zoom(100)
        self.app.processEvents()
        self.assertTrue(all(button.isVisible() for button in planned_nav))
        self.assertEqual(len([card for card in cards if card.isVisible()]), 4)

    def test_four_themes_keep_core_colors_wcag_readable(self):
        self.assertEqual(THEME_NAMES, ("Amber", "Türkis", "Lila", "Kontrast"))
        for theme_name, palette in THEMES.items():
            for key in ("text", "muted", "accent", "cyan", "green", "yellow", "red"):
                with self.subTest(theme=theme_name, color=key):
                    self.assertGreaterEqual(_contrast(palette[key], palette["background"]), 4.5)

    def test_theme_selector_is_keyboard_and_screenreader_accessible(self):
        self.assertEqual(self.dashboard.theme_combo.count(), 4)
        self.assertEqual(self.dashboard.theme_combo.accessibleName(), "Farbtheme auswählen")
        self.assertEqual(self.dashboard.theme_combo.focusPolicy(), Qt.StrongFocus)
        self.assertTrue(self.dashboard.search_entry.accessibleName())
        self.assertEqual(self.dashboard.search_entry.focusPolicy(), Qt.StrongFocus)
        self.assertTrue(self.dashboard.quit_button.accessibleName())

        tiles = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.objectName() == "tileButton"
        ]
        self.assertTrue(all(button.accessibleName() for button in tiles))

        self.dashboard.theme_combo.setCurrentText("Kontrast")
        self.app.processEvents()
        self.assertEqual(self.dashboard.theme_name, "Kontrast")
        self.assertIn("#000000", self.dashboard.styleSheet())
        self.assertIn("#FFD800", self.dashboard.styleSheet())

    def test_recovery_occurs_once_in_dashboard_controls(self):
        buttons = [button for button in self.dashboard.findChildren(QPushButton) if "Recovery" in button.text()]
        self.assertEqual(len(buttons), 1)
        self.assertIs(buttons[0], self.dashboard.recovery_nav_button)

    def test_sidebar_collapses_without_destroying_navigation(self):
        self.assertFalse(self.dashboard.nav_collapsed)
        self.dashboard.toggle_sidebar()
        self.app.processEvents()
        self.assertTrue(self.dashboard.nav_collapsed)
        self.assertEqual(self.dashboard.sidebar.width(), 56)
        self.dashboard.toggle_sidebar()
        self.app.processEvents()
        self.assertGreaterEqual(self.dashboard.sidebar.width(), 190)

    def test_productive_gui_sources_contain_no_tkinter(self):
        root = Path(__file__).resolve().parent.parent
        for relative in (
            "app/ui.py", "app/song_editor.py", "app/song_library.py",
            "app/recovery_center.py", "app/ui_standards.py", "scripts/start_status.py",
        ):
            self.assertNotIn("tkinter", (root / relative).read_text(encoding="utf-8").casefold(), relative)


if __name__ == "__main__":
    unittest.main()
