"""GUI-Prüfung: Wiki-Menü, Textschutz, Zoom und Rückkehr."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QMessageBox

from app.wiki_window import WikiWindow
from app import wiki_store as wiki
from app.ui import Dashboard
from app.event_log import EventLogger
from app.texts import TextRegistry


class WikiGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_wiki_save_search_version_and_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = WikiWindow(Path(tmp))
            try:
                window.show()
                window.title_field.setText("Kapitel")
                window.content_field.setPlainText("Erster Gedanke")
                self.assertTrue(window.save())
                self.assertEqual(len(wiki.load(Path(tmp))["articles"]), 1)
                window.content_field.setPlainText("Zweiter Gedanke")
                self.assertTrue(window.save())
                self.assertEqual(len(wiki.load(Path(tmp))["articles"][0]["revisions"]), 1)
                window.search_entry.setText("Zweiter")
                self.assertEqual(window.listing.count(), 1)
                for zoom in (100, 150, 200):
                    window.set_zoom(zoom)
                window.title_field.setText("Ungespeichert")
                with patch("app.module_widgets.QMessageBox.exec", return_value=QMessageBox.Cancel):
                    self.assertFalse(window.confirm_leave())
            finally:
                window.discard_draft()
                window.close()
                self.app.processEvents()

    def test_dashboard_wiki_menu_registry_and_zoom(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sources = Path(__file__).resolve().parents[1]
            dashboard = Dashboard(TextRegistry(sources / "texte/registry.json"), EventLogger(root, "0.18.5"), root)
            try:
                dashboard.show()
                self.assertTrue(any("Wiki" in a.text() for a in dashboard.module_menu.actions()))
                dashboard.open_wiki()
                self.assertIsNotNone(dashboard._wiki_window)
                dashboard.set_zoom(150)
                self.assertEqual(dashboard._wiki_window.zoom_percent, 150)
                self.assertIn(dashboard._wiki_window, [x.window for x in dashboard._managed_window_registry()])
            finally:
                if dashboard._wiki_window:
                    dashboard._wiki_window.discard_draft()
                    dashboard._wiki_window.close()
                dashboard._closing_after_save = True
                dashboard.close()
                self.app.processEvents()
