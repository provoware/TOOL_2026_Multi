"""Zentral registrierte Oberflächentexte laden."""

from __future__ import annotations

import json
from pathlib import Path


class TextRegistry:
    def __init__(self, path: Path) -> None:
        self._texts = json.loads(path.read_text(encoding="utf-8"))["texts"]

    def get(self, key: str, fallback: str) -> str:
        value = self._texts.get(key)
        return value if isinstance(value, str) and value.strip() else fallback
