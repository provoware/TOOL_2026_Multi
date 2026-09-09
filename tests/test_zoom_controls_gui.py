import os
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pathlib import Path

from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtWidgets import QApplication, QComboBox, QPushButton, QScrollArea

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


class FakeWheel:
    def __init__(self, delta):
        self._delta = delta
        self.accepted = False

    def type(self):
        return QEvent.Type.Wheel

    def modifiers(self):
        return Qt.KeyboardModifier.ControlModifier

    def angleDelta(self):
        return QPoint(0, self._delta)

    def accept(self):
        self.accepted = True


class ZoomControlsGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dashboard = Dashboard(FakeTexts(), FakeLogger(), Path(self.temp.name))
        self.dashboard.show()
        self.app.processEvents()

    def tearDown(self):
        self.dashboard._closing_after_save = True
        self.dashboard.close()
        self.app.processEvents()
        self.temp.cleanup()

    def test_ctrl_wheel_changes_zoom_and_consumes_event(self):
        event = FakeWheel(120)
        self.assertTrue(self.dashboard.eventFilter(self.dashboard, event))
        self.assertTrue(event.accepted)
        self.assertEqual(self.dashboard.zoom_percent, 125)
        self.assertEqual(self.dashboard.zoom_label.text(), "125 %")

    def test_zoom_bounds_and_reset(self):
        self.dashboard.set_zoom(200)
        self.dashboard._step_zoom(1)
        self.assertEqual(self.dashboard.zoom_percent, 200)
        self.dashboard.set_zoom(100)
        self.assertEqual(self.dashboard.zoom_label.text(), "100 %")

    def test_font_buttons_exist(self):
        texts = [button.text() for button in self.dashboard.findChildren(QPushButton)]
        self.assertIn("A−", texts)
        self.assertIn("A+", texts)

    def test_zoom_200_reflows_cards_and_uses_scroll_instead_of_compressing(self):
        self.dashboard.resize(1594, 900)
        self.dashboard.set_zoom(200)
        self.app.processEvents()

        nav_scroll = getattr(self.dashboard, "_provoware_nav_scroll", None)
        card_scroll = getattr(self.dashboard, "_provoware_dashboard_scroll", None)
        grid = getattr(self.dashboard, "_provoware_dashboard_grid", None)
        self.assertIsInstance(nav_scroll, QScrollArea)
        self.assertIsInstance(card_scroll, QScrollArea)
        self.assertIsNotNone(grid)
        self.assertGreater(nav_scroll.verticalScrollBar().maximum(), 0)
        self.assertGreater(card_scroll.verticalScrollBar().maximum(), 0)

        columns = []
        for index in range(grid.count()):
            _row, column, _row_span, _column_span = grid.getItemPosition(index)
            columns.append(column)
        self.assertEqual(columns, [0, 0, 0, 0])

    def test_zoom_200_sidebar_entries_do_not_overlap(self):
        self.dashboard.resize(1594, 900)
        self.dashboard.set_zoom(200)
        self.app.processEvents()

        entries = [entry for entry in self.dashboard._nav_entries if entry.isVisible()]
        self.assertGreater(len(entries), 10)
        previous_bottom = -1
        for entry in entries:
            geometry = entry.geometry()
            self.assertGreater(geometry.height(), 0)
            self.assertGreater(geometry.top(), previous_bottom)
            previous_bottom = geometry.bottom()

    def test_zoom_200_profile_rows_do_not_overlap(self):
        self.dashboard.resize(1594, 900)
        self.dashboard.set_zoom(200)
        self.app.processEvents()

        combos = [combo for combo in self.dashboard.db_boxes.values() if isinstance(combo, QComboBox)]
        previous_bottom = -1
        for combo in combos:
            geometry = combo.geometry()
            self.assertGreater(geometry.height(), 0)
            self.assertGreater(geometry.top(), previous_bottom)
            previous_bottom = geometry.bottom()

    def test_zoom_reflow_is_reversible(self):
        self.dashboard.resize(1594, 900)
        self.dashboard.set_zoom(200)
        self.app.processEvents()
        self.dashboard.set_zoom(100)
        self.app.processEvents()

        grid = getattr(self.dashboard, "_provoware_dashboard_grid", None)
        self.assertIsNotNone(grid)
        positions = set()
        for index in range(grid.count()):
            row, column, _row_span, _column_span = grid.getItemPosition(index)
            positions.add((row, column))
        self.assertEqual(positions, {(0, 0), (0, 1), (1, 0), (1, 1)})


if __name__ == "__main__":
    unittest.main()
