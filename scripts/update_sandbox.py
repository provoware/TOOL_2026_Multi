"""Optionaler Linux-Isolationscheck eines bereits statisch geprüften Update-Stagings."""
import argparse
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app.update_sandbox import run_isolated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--staging", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = run_isolated(args.root, args.staging)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(2, f"Isolierte Prüfung nicht ausgeführt: {error}\n")
    print(f"Status: {report['status']}. Aktivierung stets gesperrt.")
    if report["runtime_tests"] != "PASS":
        parser.exit(1)


if __name__ == "__main__":
    main()
