import os
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFrame, QLabel, QPushButton, QWidget

from app.song_document import SongDocument, save_song
from app.ui import Dashboard, _open_managed_window
from app.laptop_layout import install_laptop_layout
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


class FakeManagedWindow:
    def __init__(self, *, visible: bool = False) -> None:
        self.visible = visible
        self.raise_calls = 0
        self.activate_calls = 0
        self.show_calls = 0
        self.refresh_calls = 0
        self.preparations: list[str] = []

    def isVisible(self) -> bool:
        return self.visible

    def raise_(self) -> None:
        self.raise_calls += 1

    def activateWindow(self) -> None:
        self.activate_calls += 1

    def show(self) -> None:
        self.visible = True
        self.show_calls += 1

    def refresh(self) -> None:
        self.refresh_calls += 1


class FakeDashboardManagedWindow(QWidget):
    """Minimales QWidget für Registry-, Zoom- und Refresh-Regressionen."""

    def __init__(self, *, visible: bool = True) -> None:
        super().__init__()
        self._test_visible = visible
        self.zoom_calls: list[int] = []
        self.refresh_calls = 0

    def isVisible(self) -> bool:
        return self._test_visible

    def set_zoom(self, percent: int) -> None:
        self.zoom_calls.append(percent)

    def refresh(self) -> None:
        self.refresh_calls += 1


def _luminance(hex_color: str) -> float:
    channels = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]

    def linear(value: float) -> float:
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = map(linear, channels)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _contrast(first: str, second: str) -> float:
    light, dark = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


class ManagedWindowLifecycleTests(unittest.TestCase):
    def test_visible_window_is_prepared_activated_and_refreshed_without_recreation(self):
        current = FakeManagedWindow(visible=True)
        factory_calls = 0

        def factory() -> FakeManagedWindow:
            nonlocal factory_calls
            factory_calls += 1
            return FakeManagedWindow()

        result = _open_managed_window(
            current,
            factory,
            prepare_visible=lambda window: window.preparations.append("sichtbar"),
            prepare_before_show=lambda window: window.preparations.append("zeigen"),
        )

        self.assertIs(result, current)
        self.assertEqual(factory_calls, 0)
        self.assertEqual(current.preparations, ["sichtbar"])
        self.assertEqual(current.raise_calls, 1)
        self.assertEqual(current.activate_calls, 1)
        self.assertEqual(current.refresh_calls, 1)
        self.assertEqual(current.show_calls, 0)

    def test_hidden_window_is_recreated_by_default_and_only_show_path_is_prepared(self):
        hidden = FakeManagedWindow(visible=False)
        replacement = FakeManagedWindow(visible=False)
        result = _open_managed_window(
            hidden,
            lambda: replacement,
            prepare_visible=lambda window: window.preparations.append("sichtbar"),
            prepare_before_show=lambda window: window.preparations.append("zeigen"),
        )

        self.assertIs(result, replacement)
        self.assertEqual(hidden.show_calls, 0)
        self.assertEqual(replacement.preparations, ["zeigen"])
        self.assertEqual(replacement.show_calls, 1)
        self.assertEqual(replacement.refresh_calls, 0)
        self.assertEqual(replacement.raise_calls, 0)
        self.assertEqual(replacement.activate_calls, 0)

    def test_hidden_window_can_be_reused_and_refreshed_after_show(self):
        hidden = FakeManagedWindow(visible=False)
        factory_calls = 0

        def factory() -> FakeManagedWindow:
            nonlocal factory_calls
            factory_calls += 1
            return FakeManagedWindow()

        result = _open_managed_window(
            hidden,
            factory,
            reuse_hidden=True,
            refresh_after_show=True,
        )

        self.assertIs(result, hidden)
        self.assertEqual(factory_calls, 0)
        self.assertEqual(hidden.show_calls, 1)
        self.assertEqual(hidden.refresh_calls, 1)
        self.assertEqual(hidden.raise_calls, 0)
        self.assertEqual(hidden.activate_calls, 0)


class DashboardReferenceGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.app.setProperty("provowareTheme", DEFAULT_THEME)
        self.temp = tempfile.TemporaryDirectory()
        self.dashboard = Dashboard(FakeTexts(), FakeLogger(), Path(self.temp.name))
        install_laptop_layout(self.dashboard)
        self.dashboard.resize(1280, 790)
        self.dashboard.show()
        self.app.processEvents()

    def tearDown(self):
        set_application_theme(DEFAULT_THEME)
        self.dashboard._closing_after_save = True
        self.dashboard.close()
        self.app.processEvents()
        self.temp.cleanup()

    @staticmethod
    def _close_fake_windows(*windows: QWidget) -> None:
        for window in windows:
            window.close()
            window.deleteLater()

    def test_managed_window_registry_is_single_source_for_current_windows(self):
        song_editor = FakeDashboardManagedWindow()
        song_library = FakeDashboardManagedWindow()
        recovery = FakeDashboardManagedWindow()
        profile = FakeDashboardManagedWindow()
        todo = FakeDashboardManagedWindow()
        calendar = FakeDashboardManagedWindow()
        self.dashboard._song_editors = [song_editor]  # type: ignore[list-item]
        self.dashboard._song_library = song_library  # type: ignore[assignment]
        self.dashboard._recovery_center = recovery  # type: ignore[assignment]
        self.dashboard._profile_editor = profile  # type: ignore[assignment]
        self.dashboard._todo_window = todo  # type: ignore[assignment]
        self.dashboard._calendar_window = calendar  # type: ignore[assignment]

        registrations = self.dashboard._managed_window_registry()
        registered_windows = [registration.window for registration in registrations]
        self.assertEqual(
            registered_windows,
            [self.dashboard, song_editor, song_library, recovery, profile, todo, calendar],
        )
        self.assertEqual(len({id(window) for window in registered_windows}), len(registered_windows))
        self.assertTrue(self.dashboard._is_managed_widget(todo))
        outsider = QWidget()
        self.assertFalse(self.dashboard._is_managed_widget(outsider))
        outsider.close()
        outsider.deleteLater()
        self._close_fake_windows(song_editor, song_library, recovery, profile, todo, calendar)

    def test_managed_window_registry_drives_zoom_for_every_current_side_window(self):
        song_editor = FakeDashboardManagedWindow()
        song_library = FakeDashboardManagedWindow()
        recovery = FakeDashboardManagedWindow()
        profile = FakeDashboardManagedWindow()
        todo = FakeDashboardManagedWindow()
        calendar = FakeDashboardManagedWindow()
        self.dashboard._song_editors = [song_editor]  # type: ignore[list-item]
        self.dashboard._song_library = song_library  # type: ignore[assignment]
        self.dashboard._recovery_center = recovery  # type: ignore[assignment]
        self.dashboard._profile_editor = profile  # type: ignore[assignment]
        self.dashboard._todo_window = todo  # type: ignore[assignment]
        self.dashboard._calendar_window = calendar  # type: ignore[assignment]

        self.dashboard.set_zoom(150)

        self.assertEqual(song_editor.zoom_percent, 150)
        for window in (song_library, recovery, profile, todo, calendar):
            self.assertEqual(window.zoom_calls, [150])
        self._close_fake_windows(song_editor, song_library, recovery, profile, todo, calendar)

    def test_managed_window_registry_preserves_dashboard_refresh_scope(self):
        song_library = FakeDashboardManagedWindow(visible=True)
        recovery = FakeDashboardManagedWindow(visible=True)
        profile = FakeDashboardManagedWindow(visible=True)
        todo = FakeDashboardManagedWindow(visible=True)
        calendar = FakeDashboardManagedWindow(visible=True)
        self.dashboard._song_library = song_library  # type: ignore[assignment]
        self.dashboard._recovery_center = recovery  # type: ignore[assignment]
        self.dashboard._profile_editor = profile  # type: ignore[assignment]
        self.dashboard._todo_window = todo  # type: ignore[assignment]
        self.dashboard._calendar_window = calendar  # type: ignore[assignment]

        self.dashboard.refresh()

        self.assertEqual(song_library.refresh_calls, 0)
        self.assertEqual(profile.refresh_calls, 0)
        self.assertEqual(recovery.refresh_calls, 1)
        self.assertEqual(todo.refresh_calls, 1)
        self.assertEqual(calendar.refresh_calls, 1)
        self._close_fake_windows(song_library, recovery, profile, todo, calendar)

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

    def test_1366x768_at_125_uses_laptop_compact_without_losing_core_actions(self):
        self.dashboard.resize(1366, 768)
        self.dashboard.set_zoom(125)
        self.app.processEvents()

        self.assertTrue(self.dashboard.property("provowareLaptopCompact"))

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
        self.assertFalse(self.dashboard.status_legend.isVisible())

        profile_buttons = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.text() in {"Profile & Werte bearbeiten", "Profile bearbeiten", "Profile"}
        ]
        self.assertEqual(len(profile_buttons), 1)
        self.assertEqual(profile_buttons[0].text(), "Profile")
        self.assertLessEqual(self.dashboard.db_profile_combo.maximumWidth(), 120)

        profile_label = next(label for label in self.dashboard.findChildren(QLabel) if label.text() == "Profil:")
        self.assertFalse(profile_label.isVisible())
        self.assertTrue(self.dashboard.todo_nav_button.isVisible())
        self.assertTrue(self.dashboard.calendar_nav_button.isVisible())
        self.assertTrue(self.dashboard.recovery_nav_button.isVisible())

        self.dashboard.toggle_sidebar()
        self.app.processEvents()
        self.dashboard.toggle_sidebar()
        self.app.processEvents()
        self.assertTrue(all(not button.isVisible() for button in planned_nav))
        self.assertTrue(self.dashboard.todo_nav_button.isVisible())

    def test_laptop_compact_restores_full_large_layout(self):
        self.dashboard.resize(1366, 768)
        self.dashboard.set_zoom(125)
        self.app.processEvents()
        self.assertTrue(self.dashboard.property("provowareLaptopCompact"))

        self.dashboard.resize(1594, 926)
        self.app.processEvents()

        self.assertFalse(self.dashboard.property("provowareLaptopCompact"))
        cards = [frame for frame in self.dashboard.findChildren(QFrame) if frame.objectName() == "card"]
        self.assertEqual(len([card for card in cards if card.isVisible()]), 4)
        planned_nav = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.objectName() == "navButton" and button.property("planned") is True
        ]
        self.assertTrue(all(button.isVisible() for button in planned_nav))
        self.assertTrue(self.dashboard.status_legend.isVisible())
        profile_button = next(
            button for button in self.dashboard.findChildren(QPushButton)
            if button.text() in {"Profile & Werte bearbeiten", "Profile bearbeiten", "Profile"}
        )
        self.assertEqual(profile_button.text(), "Profile & Werte bearbeiten")
        profile_label = next(label for label in self.dashboard.findChildren(QLabel) if label.text() == "Profil:")
        self.assertTrue(profile_label.isVisible())

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
        ready_tiles = [button for button in tiles if button.property("ready") is True]
        planned_tiles = [button for button in tiles if button.property("planned") is True]
        self.assertEqual(len(ready_tiles), 2)
        self.assertTrue(all(button.isVisible() for button in ready_tiles))
        self.assertTrue(all(not button.isVisible() for button in planned_tiles))
        self.assertTrue(self.dashboard.theme_combo.isVisible())

        self.dashboard.set_zoom(100)
        self.app.processEvents()
        self.assertTrue(all(button.isVisible() for button in planned_nav))
        self.assertTrue(all(button.isVisible() for button in tiles))
        self.assertEqual(len([card for card in cards if card.isVisible()]), 4)

    def test_200_percent_laptop_reflows_recent_songs_without_clipping_categories(self):
        for index in range(5):
            save_song(
                Path(self.temp.name),
                SongDocument(
                    title=f"Sehr langer häufig verwendeter Songtitel Nummer {index + 1}",
                    genre="HardTechno",
                ),
            )
        self.dashboard.refresh_recent_songs()
        self.dashboard.resize(1446, 794)
        self.dashboard.set_zoom(200)
        self.app.processEvents()
        self.app.processEvents()

        self.assertEqual(self.dashboard.app_title_label.text(), "Provoware Dashboard 2026")
        self.assertFalse(self.dashboard.header_subtitle.isVisible())
        self.assertTrue(self.dashboard.recent_combo.isVisible())
        self.assertTrue(self.dashboard.recent_open_button.isVisible())
        self.assertEqual(self.dashboard.recent_combo.count(), 5)
        self.assertTrue(all(not widget.isVisible() for widget in self.dashboard._recent_widgets))
        self.assertTrue(self.dashboard.recent_all_button.isVisible())

        for label in self.dashboard.findChildren(QLabel):
            if label.text() in {"Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten"}:
                with self.subTest(label=label.text()):
                    required = label.fontMetrics().horizontalAdvance(label.text()) + 12
                    self.assertGreaterEqual(label.width(), required)

    def test_managed_child_window_is_promoted_to_nonmodal_top_level_module(self):
        child = FakeDashboardManagedWindow()
        child.setParent(self.dashboard)
        self.assertFalse(child.isWindow())

        result = _open_managed_window(None, lambda: child)
        self.app.processEvents()

        self.assertIs(result, child)
        self.assertTrue(result.isWindow())
        self.assertEqual(result.windowModality(), Qt.NonModal)
        self.assertTrue(result.property("provowareModuleWindow"))
        self._close_fake_windows(child)

    def test_all_dashboard_modules_open_as_independent_windows(self):
        openers = (
            (lambda: self.dashboard.open_profile_editor("Genres"), "_profile_editor"),
            (self.dashboard.open_todo, "_todo_window"),
            (self.dashboard.open_calendar, "_calendar_window"),
            (self.dashboard.open_song_library, "_song_library"),
            (self.dashboard.open_recovery, "_recovery_center"),
        )
        opened = []
        for opener, attribute in openers:
            opener()
            self.app.processEvents()
            window = getattr(self.dashboard, attribute)
            self.assertIsNotNone(window)
            with self.subTest(module=attribute):
                self.assertTrue(window.isWindow())
                self.assertEqual(window.windowModality(), Qt.NonModal)
                self.assertTrue(window.property("provowareModuleWindow"))
            opened.append(window)
        for window in opened:
            window.close()
            window.deleteLater()
        self.app.processEvents()

    def test_direct_song_editor_is_also_an_independent_module_window(self):
        self.dashboard.open_song_editor()
        self.app.processEvents()
        editor = self.dashboard._song_editors[-1]
        self.assertTrue(editor.isWindow())
        self.assertEqual(editor.windowModality(), Qt.NonModal)
        self.assertTrue(editor.property("provowareModuleWindow"))
        editor.close()
        self.app.processEvents()

    def test_four_themes_keep_core_colors_wcag_readable(self):
        self.assertEqual(THEME_NAMES, ("Amber", "Türkis", "Lila", "Kontrast"))
        for theme_name, palette in THEMES.items():
            for key in ("text", "muted", "accent", "cyan", "green", "yellow", "red"):
                with self.subTest(theme=theme_name, color=key):
                    self.assertGreaterEqual(_contrast(palette[key], palette["background"]), 4.5)
            with self.subTest(theme=theme_name, component_border="surface"):
                self.assertGreaterEqual(_contrast(palette["border"], palette["surface"]), 3.0)

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