"""Datensparsame Lernhistorie für wiederkehrende Fehler."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class RegressionManager:
    """Merkt Fehlermuster, ohne Inhalte oder persönliche Daten zu sammeln."""

    def __init__(self, state_path: Path) -> None:
        self.state_path = state_path

    def learn(self, area: str, exception_type: str, cause: str) -> dict[str, Any]:
        signature = self._signature(area, exception_type, cause)
        state = self._read_state()
        now = datetime.now(timezone.utc).isoformat()
        entry = state.setdefault("patterns", {}).setdefault(signature, {
            "area": area, "exception_type": exception_type, "count": 0, "first_seen": now
        })
        entry.setdefault("first_seen", now)
        entry["count"] += 1
        entry["last_seen"] = now
        self._write_state(state)
        return {"signature": signature, "count": entry["count"],
                "repeated": entry["count"] > 1, "first_seen": entry["first_seen"],
                "last_seen": entry["last_seen"]}

    @staticmethod
    def prevention_hint(learned: dict[str, Any]) -> str:
        if learned["repeated"]:
            return "Dieses Fehlermuster trat erneut auf. Bitte den genannten Prüfschritt vor dem nächsten Versuch ausführen."
        return "Dieses Fehlermuster wurde für spätere Vergleiche vorgemerkt."

    @staticmethod
    def _signature(area: str, exception_type: str, cause: str) -> str:
        normalized = " ".join(cause.lower().split())[:200]
        raw = f"{area}|{exception_type}|{normalized}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:16]

    def _read_state(self) -> dict[str, Any]:
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            return data if data.get("schema_version") == 1 else self._empty_state()
        except (FileNotFoundError, json.JSONDecodeError, OSError, AttributeError):
            return self._empty_state()

    @staticmethod
    def _empty_state() -> dict[str, Any]:
        return {"schema_version": 1, "patterns": {}}

    def _write_state(self, state: dict[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.state_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(temporary, self.state_path)
