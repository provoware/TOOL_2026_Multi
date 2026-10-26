"""Regression: lesbare Dashboard-Werte und nutzbare Schreibfläche bei 200 % Zoom."""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QVBoxLayout, QWidget

from app.main import configure_dashboard_presentation
from app.song_editor import SongEditor
from app.ui import Dashboard
from app.ui_standards import combo_text_width
from scripts.ui_shadow_gate import ViewportSpec, _apply_case, _text_fit_findings


class _Texts:
    def get(self, _key, default=""):
        return default


class _Logger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


class UiTextFitGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_dashboard_labels_and_combos_fit_at_critical_viewports(self):
        cases = ((1366, 768, 100), (1366, 768, 125), (1366, 768, 150),
                 (1366, 768, 175), (1366, 768, 200),
                 (1600, 900, 150), (1920, 1080, 200))
        with tempfile.TemporaryDirectory() as tmp:
            dashboard = configure_dashboard_presentation(
                Dashboard(_Texts(), _Logger(), Path(tmp)))
            try:
                for width, height, zoom in cases:
                    with self.subTest(width=width, height=height, zoom=zoom):
                        _apply_case(dashboard, ViewportSpec(width, height, zoom, "Amber"))
                        labels = [label for label in dashboard.findChildren(QLabel)
                                  if label.isVisibleTo(dashboard) and label.text() in {
                                      "Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten",
                                  }]
                        self.assertEqual(len(labels), 5)
                        for label in labels:
                            self.assertGreaterEqual(
                                label.contentsRect().width(),
                                label.fontMetrics().horizontalAdvance(label.text()),
                                f"{label.text()} bei {zoom} % ist abgeschnitten",
                            )
                        title = dashboard.app_title_label
                        self.assertGreaterEqual(title.contentsRect().width(),
                                                title.fontMetrics().horizontalAdvance(title.text()))
                        for combo in (dashboard.db_profile_combo, dashboard.theme_combo):
                            self.assertGreaterEqual(combo.width(), combo_text_width(combo))
                        findings = _text_fit_findings(dashboard, f"{width}x{height}_z{zoom}")
                        self.assertEqual(findings, [])
            finally:
                dashboard._closing_after_save = True
                dashboard.close()
                self.app.processEvents()

    def test_shadow_gate_detects_real_text_overflows(self):
        window = QWidget()
        layout = QVBoxLayout(window)
        label = QLabel("Besonderheiten")
        label.setFixedWidth(40)
        layout.addWidget(label)
        combo = QComboBox()
        combo.addItem("HardTechno")
        combo.setFixedWidth(60)
        layout.addWidget(combo)
        try:
            window.show()
            self.app.processEvents()
            findings = _text_fit_findings(window, "synthetic")
            self.assertEqual(
                {item["code"] for item in findings},
                {"UI-LABEL-TEXT-CLIPPED", "UI-COMBO-TEXT-CLIPPED"},
            )
            self.assertTrue(all(item["required_px"] > item["available_px"]
                                for item in findings))
        finally:
            window.close()
            self.app.processEvents()

    def test_song_editor_200_percent_keeps_writing_and_preview_usable(self):
        with tempfile.TemporaryDirectory() as tmp:
            editor = SongEditor(Path(tmp), zoom_percent=200)
            try:
                _apply_case(editor, ViewportSpec(1366, 768, 200, "Amber"))
                self.assertGreaterEqual(editor.section_text.height(), 180)
                self.assertGreaterEqual(editor.preview.height(), 180)
                self.assertFalse(editor.guide_label.isVisible())
                self.assertFalse(editor.character_frame.isVisible())
                self.assertFalse(editor.other_text.isVisible())
                self.assertTrue(editor.character_toggle.isVisible())
                self.assertTrue(editor.notes_toggle.isVisible())

                editor.section_text.setPlainText("Mein Text bleibt trotz Zoom erhalten.")
                editor.other_text.setPlainText("Meine Notiz bleibt erhalten.")
                editor.character_toggle.setChecked(True)
                editor.notes_toggle.setChecked(True)
                self.app.processEvents()
                self.assertTrue(editor.character_frame.isVisible())
                self.assertTrue(editor.other_text.isVisible())
                self.assertEqual(editor.section_text.toPlainText(),
                                 "Mein Text bleibt trotz Zoom erhalten.")
                self.assertEqual(editor.other_text.toPlainText(),
                                 "Meine Notiz bleibt erhalten.")

                _apply_case(editor, ViewportSpec(1366, 768, 150, "Amber"))
                self.assertTrue(editor.guide_label.isVisible())
                self.assertTrue(editor.character_frame.isVisible())
                self.assertTrue(editor.other_text.isVisible())
                self.assertFalse(editor.character_toggle.isVisible())
                self.assertFalse(editor.notes_toggle.isVisible())
                self.assertEqual(editor.section_text.toPlainText(),
                                 "Mein Text bleibt trotz Zoom erhalten.")
            finally:
                editor._closing_after_save = True
                editor.close()
                self.app.processEvents()


if __name__ == "__main__":
    unittest.main()
