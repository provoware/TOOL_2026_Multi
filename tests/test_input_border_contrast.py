"""WCAG-nahe Eingaberandkontrast-Regressionsprüfung aller Provoware-Themes.

Der Eingaberand ist für die optische Unterscheidung des Eingabefeldes wichtig.
Das Minimum von 3:1 sichert die Erkennbarkeit ohne allein auf Neonfokus zu setzen.
"""

import unittest

from app.ui_standards import THEME_NAMES, THEMES, app_stylesheet


def relative_luminance(color: str) -> float:
    if not isinstance(color, str) or len(color) != 7 or not color.startswith("#"):
        raise ValueError("Farbe muss #RRGGBB sein")
    rgb = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [channel / 12.92 if channel <= 0.04045
              else ((channel + 0.055) / 1.055) ** 2.4 for channel in rgb]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first: str, second: str) -> float:
    light, dark = sorted([relative_luminance(first), relative_luminance(second)],
                         reverse=True)
    return (light + 0.05) / (dark + 0.05)


class InputBorderContrastTests(unittest.TestCase):
    def test_all_input_borders_have_minimum_three_to_one(self):
        for theme_name in THEME_NAMES:
            with self.subTest(theme=theme_name):
                palette = THEMES[theme_name]
                actual = contrast_ratio(palette["input_border"], palette["input_bg"])
                self.assertGreaterEqual(actual, 3.0, f"{theme_name}: {actual:.2f}:1")

    def test_all_theme_text_and_placeholders_remain_readable(self):
        for theme_name in THEME_NAMES:
            with self.subTest(theme=theme_name):
                p = THEMES[theme_name]
                self.assertGreaterEqual(contrast_ratio(p["text"], p["surface"]), 4.5)
                self.assertGreaterEqual(contrast_ratio(p["placeholder"], p["input_bg"]), 4.5)

    def test_stylesheet_uses_same_checked_border_colors(self):
        for theme_name in THEME_NAMES:
            with self.subTest(theme=theme_name):
                palette = THEMES[theme_name]
                css = app_stylesheet(100, theme_name)
                self.assertIn(f"border:1px solid {palette['input_border']}", css)


if __name__ == "__main__":
    unittest.main()
