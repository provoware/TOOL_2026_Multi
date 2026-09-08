"""Verständliche und maschinenlesbare Ereignisprotokollierung."""

from __future__ import annotations

import json
import os
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.atomic_io import atomic_write_text
from app.log_maintenance import quarantine_corrupt_jsonl, rotate_log
from app.redaction import redact
from app.regression import RegressionManager


class EventLogger:
    def __init__(self, root: Path, version: str) -> None:
        self.version = version
        self.jsonl_path = root / "logs" / "ereignisse.jsonl"
        self.report_dir = root / "berichte"
        self.quarantine_dir = root / "logs" / "quarantaene"
        self.regressions = RegressionManager(root / "logs" / "rueckfaelle.json")

    def record(self, *, severity: str, area: str, summary: str, cause: str,
               protection: str, next_step: str, exception: BaseException | None = None) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        area_clean = redact(area, limit=80).upper() or "UNBEKANNT"
        area_id = "".join(ch if ch.isalnum() else "_" for ch in area_clean)[:60] or "UNBEKANNT"
        event_id = f"{area_id}-EREIGNIS-{now:%Y%m%d%H%M%S}-{uuid.uuid4().hex[:6].upper()}"
        summary_clean = redact(summary, limit=1000)
        cause_clean = redact(cause, limit=2000)
        protection_clean = redact(protection, limit=1000)
        next_step_clean = redact(next_step, limit=1000)
        learned = None
        if exception is not None:
            learned = self.regressions.learn(area_clean, type(exception).__name__, cause_clean)
            next_step_clean = redact(f"{next_step_clean} {self.regressions.prevention_hint(learned)}", limit=1400)
        event = {
            "schema_version": 1, "time": now.isoformat(), "event_id": event_id,
            "severity": redact(severity, limit=40), "area": area_clean, "summary": summary_clean,
            "technical_cause": cause_clean, "safe_action": protection_clean,
            "next_step": next_step_clean, "program_version": self.version,
            "exception_type": type(exception).__name__ if exception else None,
            "trace": self._trace(exception), "regression": learned,
        }
        self._persist(event)
        return event

    def _maintain_log(self) -> None:
        quarantine_corrupt_jsonl(self.jsonl_path, self.quarantine_dir)
        rotate_log(self.jsonl_path)

    def recent(self, limit: int = 5) -> list[dict[str, Any]]:
        if limit <= 0 or not self.jsonl_path.exists():
            return []
        try:
            quarantine_corrupt_jsonl(self.jsonl_path, self.quarantine_dir)
            events = [json.loads(line) for line in self.jsonl_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        except (OSError, json.JSONDecodeError):
            return []
        return events[-limit:][::-1]

    def _persist(self, event: dict[str, Any]) -> None:
        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self._maintain_log()
        line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
        # JSONL bleibt absichtlich append-only. Vollständiger Dateiersatz wäre hier semantisch falsch.
        with self.jsonl_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        report = self.report_dir / f"{event['event_id']}.txt"
        atomic_write_text(report, self.human_report(event))

    @staticmethod
    def _trace(exception: BaseException | None) -> str | None:
        if exception is None:
            return None
        return redact("".join(traceback.format_exception(exception)), limit=4000)

    @staticmethod
    def human_report(event: dict[str, Any]) -> str:
        fields = (("EREIGNIS", "event_id"), ("ZEIT", "time"), ("SCHWERE", "severity"),
                  ("BEREICH", "area"), ("WAS IST PASSIERT?", "summary"),
                  ("WAHRSCHEINLICHER GRUND", "technical_cause"),
                  ("WAS WURDE GESCHÜTZT?", "safe_action"),
                  ("WAS KANN ICH JETZT TUN?", "next_step"),
                  ("PROGRAMMVERSION", "program_version"))
        return "\n\n".join(f"{title}\n{event.get(key) or 'Keine Angabe'}" for title, key in fields) + "\n"


def emergency_message(exception: BaseException) -> str:
    return ("Ein unerwarteter Fehler konnte nicht vollständig protokolliert werden. "
            f"Ihre Daten wurden nicht verändert. Technischer Hinweis: {type(exception).__name__}")
