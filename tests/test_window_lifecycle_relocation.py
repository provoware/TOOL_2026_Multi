"""Die bisherigen Dashboard-Importe bleiben nach der Auslagerung erhalten."""
import unittest

from app import ui, window_lifecycle


class WindowLifecycleRelocationTests(unittest.TestCase):
    def test_all_existing_import_names_remain_identical(self):
        for name in ("_open_managed_window", "_show_module_window",
                     "_prepare_module_window", "_ManagedWindowRegistration"):
            with self.subTest(name=name):
                self.assertIs(getattr(ui, name), getattr(window_lifecycle, name))


if __name__ == "__main__":
    unittest.main()
