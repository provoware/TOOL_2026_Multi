"""Update-ZIP getrennt prüfen, ohne Installation oder Ausführen des Paketcodes."""
import argparse
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app.update_staging import stage_update


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--archiv', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--basis-sha256', required=True)
    parser.add_argument('--staging-parent', type=Path, required=True)
    args = parser.parse_args()
    try:
        folder, report = stage_update(args.root, args.archiv, args.sha256, args.basis_sha256, args.staging_parent)
    except (OSError, ValueError, KeyError, TypeError, SyntaxError, RecursionError, zipfile.BadZipFile) as error:
        parser.exit(1, f'Update-Prüfung abgebrochen ({type(error).__name__}): {error}\n'
                       'Aktives Programm und Arbeitsdaten wurden nicht ersetzt. Paketquelle, Prüfsumme und Platz prüfen.\n')
    print(f'Statische Prüfung erfolgreich: {folder}')
    print(f'Version {report["from_version"]} → {report["to_version"]}. Paketcode nicht ausgeführt. Aktivierung bleibt gesperrt.')


if __name__ == '__main__':
    main()
