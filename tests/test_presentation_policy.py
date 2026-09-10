import unittest

from app.presentation_policy import (
    HIGH_ZOOM_MIN_PERCENT,
    WIDE_MIN_WIDTH_PX,
    classify_presentation,
    normalize_zoom,
)


class PresentationPolicyTests(unittest.TestCase):
    def test_zoom_is_bounded_and_invalid_values_are_safe(self):
        self.assertEqual(normalize_zoom(None), 100)
        self.assertEqual(normalize_zoom("125"), 125)
        self.assertEqual(normalize_zoom(50), 100)
        self.assertEqual(normalize_zoom(250), 200)

    def test_reference_laptop_1366x768_at_125_percent_is_compact(self):
        state = classify_presentation(width_px=1366, height_px=768, zoom_percent=125)
        self.assertTrue(state.laptop_compact)
        self.assertTrue(state.restricted_navigation)
        self.assertFalse(state.high_zoom)

    def test_large_reference_view_is_not_compact(self):
        state = classify_presentation(width_px=1594, height_px=926, zoom_percent=125)
        self.assertFalse(state.laptop_compact)
        self.assertFalse(state.restricted_navigation)

    def test_wide_boundary_disables_laptop_compact_mode(self):
        state = classify_presentation(
            width_px=WIDE_MIN_WIDTH_PX,
            height_px=768,
            zoom_percent=125,
        )
        self.assertTrue(state.wide)
        self.assertFalse(state.laptop_compact)

    def test_high_zoom_is_restricted_without_being_laptop_compact(self):
        state = classify_presentation(
            width_px=1366,
            height_px=768,
            zoom_percent=HIGH_ZOOM_MIN_PERCENT,
        )
        self.assertTrue(state.high_zoom)
        self.assertFalse(state.laptop_compact)
        self.assertTrue(state.restricted_navigation)

    def test_minimum_window_size_participates_in_classification(self):
        state = classify_presentation(
            width_px=900,
            height_px=500,
            minimum_width_px=1594,
            minimum_height_px=926,
            zoom_percent=125,
        )
        self.assertEqual(state.width_px, 1594)
        self.assertEqual(state.height_px, 926)
        self.assertFalse(state.laptop_compact)

    def test_non_dashboard_never_activates_dashboard_laptop_mode(self):
        state = classify_presentation(
            width_px=1366,
            height_px=768,
            zoom_percent=125,
            dashboard=False,
        )
        self.assertFalse(state.laptop_compact)
        self.assertFalse(state.restricted_navigation)


if __name__ == "__main__":
    unittest.main()
