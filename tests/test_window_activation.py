"""Regression: einheitliche Fensteraktivierung erhält Reihenfolge und Verhalten."""
import unittest
from unittest.mock import Mock

from app.window_lifecycle import _activate_window, _open_managed_window


class ActivationTests(unittest.TestCase):
    def test_activation_order_is_unchanged(self):
        log = []
        window = Mock()
        window.raise_.side_effect = lambda: log.append("raise")
        window.activateWindow.side_effect = lambda: log.append("activate")
        _activate_window(window)
        self.assertEqual(log, ["raise", "activate"])

    def test_reused_visible_window_is_activated_then_refreshed(self):
        log = []
        window = Mock()
        window.isVisible.return_value = True
        window.raise_.side_effect = lambda: log.append("raise")
        window.activateWindow.side_effect = lambda: log.append("activate")
        window.refresh.side_effect = lambda: log.append("refresh")
        result = _open_managed_window(window, factory=lambda: self.fail("No new window"))
        self.assertIs(result, window)
        self.assertEqual(log, ["raise", "activate", "refresh"])


if __name__ == "__main__":
    unittest.main()
