"""Expliziter Entwicklerstart einer bereits vorbereiteten verwalteten Installation.

Ohne sicheren 'current'-Zeiger und gültige unabhängige Datenablage wird
kein Programm ausgeführt. Kein Migrations- oder Aktivierungsbefehl.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.managed_bootstrap import run_managed


def main():
    parser = argparse.ArgumentParser(description="Verwalteten Slot mit unabhängigen Daten starten")
    parser.add_argument("installation", type=Path)
    args = parser.parse_args()
    try:
        return run_managed(args.installation)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Verwalteter Programmstart gesperrt: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
