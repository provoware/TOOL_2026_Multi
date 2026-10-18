"""Acht reale Fenster: Tastaturfokus, technische Namen, Zoom und Theme-Kontraste.

Die Tests prüfen maschinell messbare Eigenschaften. Ein Tastatur-/Screenreader-
Praxistest bleibt ausdrücklich notwendig; es wird nichts an der GUI verändert.
"""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QToolButton, QWidget

from app.accessibility_contracts import MODULES, contrast_ok
from app.ui_quality_contracts import SUPPORTED_THEMES, SUPPORTED_ZOOMS, release_matrix
from app.ui_standards import theme_colors
from app.calendar_window import CalendarWindow
from app.character_window import CharacterWindow
from app.profile_editor import ProfileEditor
from app.song_editor import SongEditor
from app.song_library import SongLibrary
from app.text_editor_window import TextEditorWindow
from app.todo_window import TodoWindow
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


class EightWindowAccessibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_8_windows_have_keyboard_focusable_labelled_actions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            factories = {
                "Dashboard": lambda: Dashboard(FakeTexts(), FakeLogger(), root),
                "SongEditor": lambda: SongEditor(root),
                "TextEditorWindow": lambda: TextEditorWindow(root),
                "SongLibrary": lambda: SongLibrary(root, 100, lambda _path: None),
                "CalendarWindow": lambda: CalendarWindow(root),
                "TodoWindow": lambda: TodoWindow(root),
                "CharacterWindow": lambda: CharacterWindow(root),
                "ProfileEditor": lambda: ProfileEditor(root),
            }
            self.assertEqual(set(factories), set(MODULES))
            for module, factory in factories.items():
                with self.subTest(module=module):
                    window = factory()
                    try:
                        # Dies ist eine strukturelle Tastaturreihenfolge-Prüfung:
                        # Qts Fokusverkettung muss einen Zyklus ohne tote Enden bilden.
                        window.show()
                        self.app.processEvents()
                        actions = [control for cls in (QPushButton, QToolButton)
                                   for control in window.findChildren(cls)
                                   if control.isEnabled() and control.isVisibleTo(window)]
                        self.assertTrue(actions, "Kein bedienbares Element gefunden")
                        for button in actions:
                            self.assertNotEqual(button.focusPolicy(), Qt.NoFocus)
                            # Qt erstellt Kalender-Steuerknöpfe selbst. Ihre
                            # Screenreader-Ausgabe bleibt ein offener Praxistest.
                            if button.objectName().startswith("qt_calendar_"):
                                continue
                            self.assertTrue(
                                button.accessibleName().strip() or button.text().strip(),
                                f"Unbenannter Anwendungsschalter: {button.objectName()}")
                        focusables = [button for button in actions
                                      if button.focusPolicy() & Qt.TabFocus]
                        self.assertTrue(focusables, "Keine mit Tab erreichbare Aktion")
                        start = focusables[0]
                        seen = set()
                        current = start
                        for _ in range(2000):
                            if current in seen:
                                break
                            seen.add(current)
                            current = current.nextInFocusChain()
                        self.assertIs(current, start, "Fokusfolge enthält eine Sackgasse")
                    finally:
                        if isinstance(window, SongEditor):
                            window._closing_after_save = True
                        if isinstance(window, Dashboard):
                            window._closing_after_save = True
                        if isinstance(window, TextEditorWindow):
                            window._saved_snapshot = window._snapshot()
                        window.close()
                        self.app.processEvents()

    def test_theme_palette_text_contrast_at_each_supported_zoom(self):
        pairs = (
            ("text", "background"), ("text", "surface"), ("text", "surface_alt"),
            ("text", "input_bg"), ("muted", "background"),
            ("placeholder", "input_bg"), ("inverse_text", "accent"),
        )
        for theme in SUPPORTED_THEMES:
            palette = theme_colors(theme)
            for zoom in SUPPORTED_ZOOMS:
                with self.subTest(theme=theme, zoom=zoom):
                    self.assertTrue(any(case.theme == theme and case.zoom == zoom
                                        for case in release_matrix()))
                    for fore, back in pairs:
                        self.assertTrue(contrast_ok(palette[fore], palette[back]),
                                        f"{theme}/{zoom}: {fore} auf {back} unter 4,5:1")


if __name__ == "__main__":
    unittest.main()
