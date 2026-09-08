"""Zentrale Bereinigung sensibler Werte vor Protokollierung."""

from __future__ import annotations

import re

_REPLACEMENTS = (
    (re.compile(r"(?i)\b(authorization\s*:\s*bearer)\s+[^\s,;]+"), r"\1 <GEHEIM>"),
    (re.compile(r"(?i)\b(password|passwort|token|secret|api[_-]?key|access[_-]?key)\s*([:=])\s*([^\s,;]+)"), r"\1\2<GEHEIM>"),
    (re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._~+/=-]{8,}"), r"\1 <GEHEIM>"),
    (re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])"), "<E-MAIL>"),
    (re.compile(r"(?<!\w)/home/[^/\s]+"), "/home/<BENUTZER>"),
)


def redact(value: object, *, limit: int | None = None) -> str:
    """Entfernt typische Geheimnisse und persönliche Pfad-/Mailanteile."""
    text = "" if value is None else str(value)
    for pattern, replacement in _REPLACEMENTS:
        text = pattern.sub(replacement, text)
    if limit is not None and limit >= 0:
        return text[:limit]
    return text
