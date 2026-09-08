import os
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pathlib import Path

from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtWidgets import QApplication, QPushButton

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


if __name__ == "__main__":
    unittest.main()
