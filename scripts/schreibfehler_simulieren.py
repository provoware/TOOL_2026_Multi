#!/usr/bin/env python3
"""Begrenzte Simulation typischer Schreibfehler ohne echten Datenträgerverbrauch."""

from __future__ import annotations

import errno
import json
import os
import tempfile
from pathlib import Path
from typing import Callable

Writer = Callable[[Path, str], None]


def atomic_probe_write(target: Path, content: str, writer: Writer | None = None) -> None:
    temporary = target.with_suffix(target.suffix + ".tmp")
    writer = writer or (lambda path, text: path.write_text(text, encoding="utf-8"))
    try:
        writer(temporary, content)
        os.replace(temporary, target)
    except OSError:
        temporary.unlink(missing_ok=True)
        raise


def _failing_writer(error_number: int) -> Writer:
    def fail(_path: Path, _content: str) -> None:
        raise OSError(error_number, os.strerror(error_number))
    return fail


def simulate(error_number: int) -> dict[str, object]:
    with tempfile.TemporaryDirectory() as temp:
        target = Path(temp) / "bestand.txt"
        target.write_text("BESTAND", encoding="utf-8")
        caught = None
        try:
            atomic_probe_write(target, "NEUER STAND", _failing_writer(error_number))
        except OSError as error:
            caught = error.errno
        safe = caught == error_number and target.read_text(encoding="utf-8") == "BESTAND" and not target.with_suffix(".txt.tmp").exists()
        return {
            "errno": error_number,
            "name": errno.errorcode.get(error_number, "UNBEKANNT"),
            "caught": caught,
            "bestand_unveraendert": safe,
            "status": "OK" if safe else "FEHLER",
        }


def run_simulations() -> list[dict[str, object]]:
    return [simulate(errno.ENOSPC), simulate(errno.EROFS)]


def main() -> int:
    results = run_simulations()
    print(json.dumps({"schema_version": 1, "results": results}, ensure_ascii=False, indent=2))
    return 0 if all(item["status"] == "OK" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
