import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QCheckBox, QFrame, QLabel, QPushButton

from app.main import configure_dashboard_presentation
from app.song_editor import SongEditor
from app.ui import Dashboard
from app.ui_standards import apply_global_style


class _Texts:
    def get(self, _key: str, default: str = "") -> str:
        return default


class _Logger:
    def recent(self, _limit: int = 100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


def _settle(cycles: int = 6) -> None:
    for _ in range(cycles):
        QApplication.processEvents()


def _card_by_title(window: Dashboard, prefix: str) -> QFrame:
    for card in window.findChildren(QFrame):
        if card.objectName() != "card":
            continue
        for label in card.findChildren(QLabel):
            if label.objectName() == "cardTitle" and label.text().startswith(prefix):
                return card
    raise AssertionError(f"Karte fehlt: {prefix}")


class Iteration39ProductUiFixesGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_checkbox_hit_area_reaches_hard_minimum_at_100_percent(self):
        with tempfile.TemporaryDirectory() as tmp:
            editor = SongEditor(Path(tmp), zoom_percent=100)
            try:
                editor.show()
                _settle()
                self.assertGreaterEqual(editor.favorite_check.height(), 27)
            finally:
                editor.close()
                _settle(2)

    def test_song_editor_primary_and_optional_fields_have_semantic_accessible_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            editor = SongEditor(Path(tmp), zoom_percent=100)
            try:
                expected = {
                    editor.title_entry: "Titel",
                    editor.genre_entry: "Genre",
                    editor.mood_entry: "Stimmung",
                    editor.style_entry: "Stil",
                    editor.voice_entry: "Stimme",
                    editor.special_entry: "Besonderheiten",
                    editor.tags_entry: "Tags (mit Komma trennen)",
                    editor.preview: "Gesamtvorschau",
                }
                for widget, name in expected.items():
                    self.assertEqual(widget.accessibleName(), name)
            finally:
                editor.close()
                _settle(2)

    def test_dashboard_dense_mode_prioritizes_ready_workflows_on_short_height(self):
        with tempfile.TemporaryDirectory() as tmp:
            dashboard = configure_dashboard_presentation(Dashboard(_Texts(), _Logger(), Path(tmp)))
            try:
                dashboard.zoom_percent = 125
                dashboard.set_zoom(125)
                apply_global_style(dashboard, 125, "Türkis")
                dashboard.resize(1568, 828)
                dashboard.show()
                _settle()
                self.assertFalse(_card_by_title(dashboard, "▣  Funktionen").isVisibleTo(dashboard))
                self.assertFalse(_card_by_title(dashboard, "▤  Dateien & Werkzeuge").isVisibleTo(dashboard))
                self.assertTrue(_card_by_title(dashboard, "🚀  So startest du").isVisibleTo(dashboard))
                self.assertTrue(_card_by_title(dashboard, "▦  Daten & Vorgaben").isVisibleTo(dashboard))

                dashboard.resize(1594, 926)
                _settle()
                self.assertTrue(_card_by_title(dashboard, "▣  Funktionen").isVisibleTo(dashboard))
                self.assertTrue(_card_by_title(dashboard, "▤  Dateien & Werkzeuge").isVisibleTo(dashboard))
            finally:
                dashboard._closing_after_save = True
                dashboard.close()
                _settle(2)

    def test_high_zoom_sidebar_keeps_ready_buttons_separated(self):
        with tempfile.TemporaryDirectory() as tmp:
            dashboard = configure_dashboard_presentation(Dashboard(_Texts(), _Logger(), Path(tmp)))
            try:
                dashboard.zoom_percent = 200
                dashboard.set_zoom(200)
                apply_global_style(dashboard, 200, "Kontrast")
                dashboard.resize(1334, 696)
                dashboard.show()
                _settle()
                controller = dashboard._provoware_navigation_ux
                self.assertFalse(controller.ready_heading.isVisibleTo(dashboard))
                self.assertGreaterEqual(controller.layout.spacing(), 4)
                visible = [button for button in controller.ready_buttons if button.isVisibleTo(dashboard)]
                self.assertEqual(len(visible), 7)
                ordered = sorted(visible, key=lambda button: button.mapTo(dashboard, button.rect().topLeft()).y())
                for first, second in zip(ordered, ordered[1:]):
                    first_bottom = first.mapTo(dashboard, first.rect().bottomLeft()).y()
                    second_top = second.mapTo(dashboard, second.rect().topLeft()).y()
                    self.assertLess(first_bottom, second_top)
            finally:
                dashboard._closing_after_save = True
                dashboard.close()
                _settle(2)


if __name__ == "__main__":
    unittest.main()
