"""Erstellt eine sichere Programmsicherung und eine isolierte Rückkehrkopie."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app.update_checkpoint import create_checkpoint, restore_to_new_slot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--staging", type=Path, required=True)
    parser.add_argument("--checkpoint-parent", type=Path, required=True)
    parser.add_argument("--restore-parent", type=Path)
    args = parser.parse_args()
    try:
        path, receipt = create_checkpoint(args.root, args.staging, args.checkpoint_parent)
        print(f"Programmsicherung geprüft: {path}")
        if args.restore_parent is not None:
            restored = restore_to_new_slot(path, args.restore_parent, args.root)
            print(f"Rückkehrkopie geprüft: {restored}")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Sicherungs-/Rückkehrprüfung abgebrochen: {error}\n"
                       "Die aktuelle Installation wurde nicht verändert.\n")
    print(f"Gesicherte Version: {receipt['version']}. Aktivierung weiterhin gesperrt.")


if __name__ == "__main__":
    main()
