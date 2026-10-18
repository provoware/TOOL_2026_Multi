"""Synthetische Archivladezeiten nach Prozesszustand und Datenmenge vergleichen."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
from time import perf_counter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app import book_store
from app import module_archive

GROUPS = {'klein': 1, 'mittel': 25, 'gross': 100}


def fixture(count):
    books = []
    for index in range(count):
        book = book_store.new_book()
        book.update(id=f'book_{index}', title=f'Messbuch {index}')
        book['chapters'][0].update(id=f'chapter_{index}', content='x' * 4096)
        books.append(book)
    return book_store.validate({'schema_version': 1, 'books': books})


def worker(root, count, repeats):
    # Erstes Lesen und Wiederholungen im selben neuen Prozess separat ausweisen.
    samples = []
    for index in range(repeats + 1):
        start = perf_counter()
        state = book_store.load(root)
        elapsed = (perf_counter() - start) * 1000
        if len(state['books']) != count:
            raise ValueError('Falsche Zahl geladener Bücher.')
        samples.append({'state': 'first_read' if index == 0 else 'repeated_read', 'ms': elapsed})
    return samples


def run(rounds=3, repeats=10, temp_parent=None):
    if not 1 <= rounds <= 20 or not 1 <= repeats <= 100:
        raise ValueError('Grenzen: 1–20 neue Prozesse je Gruppe, 1–100 wiederholte Lesevorgänge.')
    samples = []
    with tempfile.TemporaryDirectory(prefix='provoware-laden-', dir=temp_parent) as folder:
        root = Path(folder)
        for group, count in GROUPS.items():
            module_archive.save(root, 'buecher', fixture(count), book_store.validate)
            size = module_archive.state_path(root, 'buecher').stat().st_size
            for round_index in range(rounds):
                start = perf_counter()
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).resolve()), '--worker', str(root),
                     '--count', str(count), '--repeats', str(repeats)],
                    cwd=ROOT, capture_output=True, text=True, timeout=30, check=True)
                process_ms = (perf_counter() - start) * 1000
                values = json.loads(result.stdout)
                samples.append({'group': group, 'books': count, 'bytes': size,
                                'round': round_index + 1, 'process_total_ms': process_ms,
                                'loads': values})
    medians = {}
    for group in GROUPS:
        rows = [row for row in samples if row['group'] == group]
        medians[group] = {state: statistics.median(
            value['ms'] for row in rows for value in row['loads'] if value['state'] == state)
            for state in ('first_read', 'repeated_read')}
    return {'schema_version': 1, 'python': platform.python_version(),
            'system': platform.platform(), 'rounds': rounds, 'repeats': repeats,
            'samples': samples, 'median_ms': medians,
            'os_cache_state': 'uncontrolled; fixtures were just written',
            'application_cache': 'No book/archive load cache exists; hit ratio not applicable',
            'scope': 'Fresh Python process plus book archive load; no dashboard or OS-cold-start claim'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rounds', type=int, default=3)
    parser.add_argument('--repeats', type=int, default=10)
    parser.add_argument('--temp-parent', type=Path)
    parser.add_argument('--worker', type=Path, help=argparse.SUPPRESS)
    parser.add_argument('--count', type=int, default=1, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not 1 <= args.repeats <= 100 or not 1 <= args.count <= 500:
        parser.error('Arbeitsgrenze überschritten.')
    try:
        result = worker(args.worker, args.count, args.repeats) if args.worker else run(
            args.rounds, args.repeats, args.temp_parent)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f'Ladebenchmark abgebrochen: {error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
