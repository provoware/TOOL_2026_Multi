#!/usr/bin/env python3
"""Begrenzte Simulation typischer Schreibfehler gegen den echten Produktions-Schreibweg."""

from __future__ import annotations

import errno
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from app.atomic_io import atomic_write_text


def simulate(error_number: int) -> dict[str, object]:
    with tempfile.TemporaryDirectory() as temp:
        target = Path(temp) / "bestand.txt"
        target.write_text("BESTAND", encoding="utf-8")
        caught = None
        failure = OSError(error_number, os.strerror(error_number))
        try:
            with patch("app.atomic_io.tempfile.mkstemp", side_effect=failure):
                atomic_write_text(target, "NEUER STAND")
        except OSError as error:
            caught = error.errno
        leftovers = list(target.parent.glob(f".{target.name}.*.tmp"))
        safe = (
            caught == error_number
            and target.read_text(encoding="utf-8") == "BESTAND"
            and leftovers == []
        )
        return {
            "errno": error_number,
            "name": errno.errorcode.get(error_number, "UNBEKANNT"),
            "caught": caught,
            "bestand_unveraendert": safe,
            "temp_reste": len(leftovers),
            "status": "OK" if safe else "FEHLER",
        }


def run_simulations() -> list[dict[str, object]]:
    return [simulate(errno.ENOSPC), simulate(errno.EROFS)]


def main() -> int:
    results = run_simulations()
    print(json.dumps({"schema_version": 2, "production_writer": "app.atomic_io.atomic_write_text", "results": results}, ensure_ascii=False, indent=2))
    return 0 if all(item["status"] == "OK" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
