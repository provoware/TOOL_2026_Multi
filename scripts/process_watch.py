"""Separater Wächter für harte Prozessabbrüche des Anwendungsprozesses."""

from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.atomic_io import atomic_write_text
from app.process_guard import CONTROLLED_ALREADY_RUNNING_EXIT
from app.redaction import redact


def write_crash_report(root: Path, returncode: int, command: list[str]) -> Path:
    report_dir = root / "berichte"
    report_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    event_id = f"WAECHTER-ABSTURZ-{now:%Y%m%d%H%M%S}"
    cause = f"Kindprozess endete mit Rückgabecode {returncode}."
    if returncode < 0:
        try:
            cause = f"Kindprozess wurde durch Signal {-returncode} ({signal.Signals(-returncode).name}) beendet."
        except ValueError:
            cause = f"Kindprozess wurde durch Signal {-returncode} beendet."
    data = {
        "time": now.isoformat(), "event_id": event_id, "severity": "ABSTURZ",
        "area": "WAECHTER", "summary": "Der Anwendungsprozess endete ohne regulären Erfolg.",
        "technical_cause": redact(cause), "safe_action": "Der Wächter hat keine Nutzerdaten verändert.",
        "next_step": "Öffnen Sie diesen Bericht und den letzten Anwendungslogeintrag.",
        "command": [redact(part) for part in command],
    }
    jsonl = root / "logs" / "ereignisse.jsonl"
    jsonl.parent.mkdir(parents=True, exist_ok=True)
    with jsonl.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    report = report_dir / f"{event_id}.txt"
    atomic_write_text(
        report,
        "WAS IST PASSIERT?\n" + data["summary"] +
        "\n\nWIE WURDE ES ERKANNT?\nDer separate Wächter sah einen fehlerhaften Prozessabschluss." +
        "\n\nWO IST ES PASSIERT?\nAnwendungsprozess" +
        "\n\nWAS WURDE GESCHÜTZT?\n" + data["safe_action"] +
        "\n\nGRUND\n" + data["technical_cause"] +
        "\n\nNÄCHSTER SCHRITT\n" + data["next_step"] + "\n",
    )
    return report


def run(root: Path, command: list[str]) -> int:
    process = subprocess.Popen(command, cwd=root)
    returncode = process.wait()
    if returncode == CONTROLLED_ALREADY_RUNNING_EXIT:
        print("🟡 Dashboard läuft bereits; zweiter Start wurde kontrolliert beendet.", file=sys.stderr)
        return returncode
    if returncode != 0:
        report = write_crash_report(root, returncode, command)
        print(f"🔴 Wächterbericht: {report}", file=sys.stderr)
    return returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("Nach -- muss ein Startbefehl folgen.")
    return run(args.root.resolve(), command)


if __name__ == "__main__":
    raise SystemExit(main())
