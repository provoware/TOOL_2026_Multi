import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPushButton


ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "scripts" / "ui_shadow_entry.py"


def _load_entry():
    spec = importlib.util.spec_from_file_location("provoware_ui_shadow_entry_harness", ENTRY)
    if spec is None or spec.loader is None:
        raise RuntimeError("ui_shadow_entry.py konnte nicht geladen werden")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UiShadowHarnessGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.entry = _load_entry()

    def test_shadow_dashboard_uses_same_presentation_stack_as_main(self):
        namespace = self.entry._load_shadow_runtime()
        factory = namespace["_provoware_production_dashboard_factory"]
        with tempfile.TemporaryDirectory() as tmp:
            dashboard = factory(Path(tmp))
            try:
                self.assertIsNotNone(getattr(dashboard, "_provoware_laptop_layout_filter", None))
                controller = getattr(dashboard, "_provoware_navigation_ux", None)
                self.assertIsNotNone(controller)
                self.assertEqual(len(controller.ready_buttons), 7)
                planned = [
                    button for button in dashboard.findChildren(QPushButton)
                    if button.property("planned") is True and button.objectName() == "navButton"
                ]
                self.assertTrue(planned)
                self.assertTrue(all(not button.isVisible() for button in planned))
            finally:
                dashboard.close()
                QApplication.processEvents()

    def test_shadow_core_factories_keep_exact_three_window_contract(self):
        namespace = self.entry._load_shadow_runtime()
        with tempfile.TemporaryDirectory() as tmp:
            factories = tuple(namespace["_core_factories"](Path(tmp), 150))
        self.assertEqual(len(factories), 3)
        self.assertTrue(all(callable(factory) for factory in factories))


if __name__ == "__main__":
    unittest.main()
