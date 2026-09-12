import unittest

from app.ui_quality_contracts import (
    ContractFinding,
    RectSpec,
    contrast_ratio,
    critical_matrix,
    deterministic_window_state_cases,
    evaluate_rect_contract,
    grid_compliance,
    grid_distance,
    intersection_area,
    promotion_decision,
    release_matrix,
    validate_matrix,
)


class UiQualityContractsTests(unittest.TestCase):
    def test_critical_matrix_is_small_unique_and_valid(self):
        matrix = critical_matrix()
        self.assertEqual(len(matrix), 8)
        self.assertEqual(validate_matrix(matrix), ())
        self.assertEqual(len({case.key for case in matrix}), len(matrix))

    def test_release_matrix_covers_all_60_combinations(self):
        matrix = release_matrix()
        self.assertEqual(len(matrix), 60)
        self.assertEqual(validate_matrix(matrix), ())
        self.assertTrue(any(case.width == 1366 and case.height == 768 and case.zoom == 200 for case in matrix))

    def test_grid_distance_accepts_fine_grid_and_flags_clear_miss(self):
        self.assertEqual(grid_distance(16), 0)
        self.assertEqual(grid_distance(17), 1)
        self.assertEqual(grid_distance(18), 2)
        with self.assertRaises(ValueError):
            grid_distance(10, 0)

    def test_grid_compliance_is_ratio_not_all_or_nothing(self):
        self.assertEqual(grid_compliance([]), 1.0)
        self.assertEqual(grid_compliance([4, 8, 12, 16]), 1.0)
        self.assertLess(grid_compliance([2, 6, 10, 14]), 1.0)

    def test_contrast_reference_values_are_sane(self):
        self.assertAlmostEqual(contrast_ratio("#000000", "#FFFFFF"), 21.0, places=3)
        self.assertLess(contrast_ratio("#777777", "#888888"), 4.5)
        with self.assertRaises(ValueError):
            contrast_ratio("black", "#FFFFFF")

    def test_rect_contract_accepts_safe_window(self):
        available = RectSpec(0, 0, 1366, 728)
        rect = RectSpec(16, 16, 1000, 650)
        self.assertEqual(evaluate_rect_contract(rect, available, minimum_width=760, minimum_height=560), ())

    def test_meta_known_bad_rect_is_detected(self):
        available = RectSpec(0, 0, 1366, 728)
        rect = RectSpec(-500, -200, 600, 400)
        findings = evaluate_rect_contract(rect, available, minimum_width=760, minimum_height=560)
        self.assertGreaterEqual(len(findings), 2)
        self.assertTrue(all(isinstance(item, ContractFinding) for item in findings))
        self.assertIn("UI-GEOMETRY-WORKAREA", {item.code for item in findings})

    def test_overlap_detector_distinguishes_touching_from_overlapping(self):
        self.assertEqual(intersection_area(RectSpec(0, 0, 100, 100), RectSpec(100, 0, 100, 100)), 0)
        self.assertEqual(intersection_area(RectSpec(0, 0, 100, 100), RectSpec(80, 80, 100, 100)), 400)

    def test_window_state_fuzz_cases_are_deterministic_and_diverse(self):
        first = deterministic_window_state_cases()
        second = deterministic_window_state_cases()
        self.assertEqual(first, second)
        self.assertGreaterEqual(len(first), 10)
        self.assertTrue(any(case.x < 0 for case in first))
        self.assertTrue(any(case.width > 2000 for case in first))

    def test_promotion_requires_multiple_perfect_runs(self):
        good = {"errors": 0, "infrastructure_errors": 0, "false_positives": 0, "injected_detection_rate": 1.0}
        self.assertFalse(promotion_decision([good, good]).ready)
        self.assertTrue(promotion_decision([good, good, good]).ready)

    def test_promotion_refuses_false_positive_or_incomplete_injection_detection(self):
        good = {"errors": 0, "infrastructure_errors": 0, "false_positives": 0, "injected_detection_rate": 1.0}
        bad = {"errors": 0, "infrastructure_errors": 0, "false_positives": 1, "injected_detection_rate": 0.75}
        decision = promotion_decision([good, good, bad])
        self.assertFalse(decision.ready)
        self.assertTrue(any("Fehlalarme" in reason for reason in decision.reasons))
        self.assertTrue(any("erkannt" in reason for reason in decision.reasons))


if __name__ == "__main__":
    unittest.main()
