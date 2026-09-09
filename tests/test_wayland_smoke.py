import unittest


class WaylandSmokeTests(unittest.TestCase):
    def test_smoke_script_is_importable_without_starting_qt(self):
        from scripts import wayland_smoke

        self.assertTrue(callable(wayland_smoke.main))


if __name__ == "__main__":
    unittest.main()
