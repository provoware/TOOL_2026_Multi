"""Lädt den zentralen Oberflächenstandard mit sicheren Vorgabewerten."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_STYLE: dict[str, Any] = {
    "window": {"width": 900, "height": 560, "min_width": 700, "min_height": 420},
    "spacing": {"small": 6, "medium": 12, "large": 24},
    "colors": {"background": "#F5F7FA", "surface": "#FFFFFF", "text": "#17202A",
               "primary": "#1F5A94", "danger": "#B42318"},
    "table": {"rows": 5, "summary_width": 430},
}


def load_ui_style(path: Path) -> dict[str, Any]:
    """Gibt bei fehlender oder beschädigter Konfiguration sichere Werte zurück."""
    try:
        configured = json.loads(path.read_text(encoding="utf-8"))
        if configured.get("schema_version") != 1:
            return DEFAULT_STYLE
        result = {key: dict(value) for key, value in DEFAULT_STYLE.items()}
        for section, defaults in result.items():
            supplied = configured.get(section)
            if isinstance(supplied, dict):
                defaults.update({key: value for key, value in supplied.items() if key in defaults})
        return result
    except (FileNotFoundError, json.JSONDecodeError, OSError, AttributeError):
        return DEFAULT_STYLE
