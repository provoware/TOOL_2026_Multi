"""Gespeicherte UI-Shadow-Nachweise prüfen; keine automatische Gate-Aktivierung."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.ui_shadow_entry import validate_evidence


def evaluate(paths):
    if len(paths) > 100:
        raise ValueError('Höchstens 100 Nachweise je Auswertung.')
    rows = []
    for path in paths:
        ok, reasons = validate_evidence(Path(path))
        payload = json.loads(Path(path).read_text(encoding='utf-8')) if ok else {}
        summary = payload.get('summary', {})
        sha, run = payload.get('git_sha', ''), str(payload.get('run_number', ''))
        errors = list(reasons)
        if payload.get('profile') != 'release':
            errors.append('Vollständige Release-Matrix erforderlich.')
        if not re.fullmatch(r'[0-9a-f]{40}', str(sha)) or not run.isdigit() or int(run or 0) <= 0:
            errors.append('GitHub-Laufnummer und vollständiger Commit-SHA erforderlich.')
        if (summary.get('status') != 'green' or summary.get('errors') != 0
                or summary.get('warnings') != 0 or payload.get('findings')):
            errors.append('Nachweis ist nicht frei von Fehlern und Warnungen.')
        try:
            finish = datetime.fromisoformat(payload.get('finished_utc', '').replace('Z', '+00:00'))
            if finish.tzinfo is None:
                raise ValueError('Zeitzone fehlt')
        except (ValueError, TypeError):
            errors.append('Gültige Abschlusszeit mit Zeitzone erforderlich.')
            finish = None
        rows.append({'git_sha': sha, 'run_number': run, 'finished': finish,
                     'eligible': not errors, 'reasons': errors})
    # Ein ungeklärter/ungültiger Nachweis verhindert die Empfehlung vollständig.
    clean = [r for r in rows if r['eligible']]
    distinct_runs = len({r['run_number'] for r in clean})
    distinct_heads = len({r['git_sha'] for r in clean})
    enough = len(rows) >= 3 and len(clean) == len(rows) and distinct_runs >= 3 and distinct_heads >= 3
    for row in rows:
        row['finished'] = row['finished'].isoformat() if row['finished'] else None
    return {'schema_version': 1, 'evidence_count': len(rows), 'clean_count': len(clean),
            'distinct_runs': distinct_runs, 'distinct_heads': distinct_heads,
            'review_candidate': enough, 'gate_activated': False, 'rows': rows,
            'next': 'Regeln fachlich kalibrieren; Aktivierung getrennt entscheiden.' if enough
                    else 'Mindestens drei saubere vollständige CI-Läufe verschiedener Stände belegen.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path, nargs='*')
    args = parser.parse_args()
    try:
        result = evaluate(args.evidence)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Auswertung abgebrochen: {error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
