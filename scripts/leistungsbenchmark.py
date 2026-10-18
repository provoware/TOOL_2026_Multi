"""Isolierter Schreibbenchmark; keine Messung realer Arbeitsinhalte."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
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
from app import performance
from app.atomic_io import _write_text, atomic_write_text

MODES = ('baseline', 'disabled', 'enabled')


def run(rounds=9, writes=100, size=4096, temp_parent=None):
    if not 3 <= rounds <= 60 or not 1 <= writes <= 10000 or not 1 <= size <= 1048576:
        raise ValueError('Grenzen: 3–60 Runden, 1–10000 Schreibvorgänge, 1–1048576 Bytes.')
    previous = performance.current()
    samples = []
    try:
        with tempfile.TemporaryDirectory(prefix='provoware-benchmark-', dir=temp_parent) as folder:
            root = Path(folder)
            target = root / 'daten/texte/probe.txt'
            content = 'x' * size
            for index in range(rounds):
                for mode in MODES[index % 3:] + MODES[:index % 3]:
                    tracker = performance.activate(root)
                    tracker.enabled = mode == 'enabled'
                    writer = _write_text if mode == 'baseline' else atomic_write_text
                    # Gleicher Warm-up pro Modus, außerhalb des Messfensters.
                    writer(target, content)
                    tracker.data = {'schema_version': 1, 'days': {}}
                    tracker.dirty = False
                    start = perf_counter()
                    for _ in range(writes):
                        writer(target, content)
                    write_ms = (perf_counter() - start) * 1000
                    start = perf_counter()
                    if not tracker.flush():
                        raise RuntimeError(tracker.last_error)
                    flush_ms = (perf_counter() - start) * 1000
                    if target.read_bytes() != content.encode('utf-8'):
                        raise RuntimeError('Schreibergebnis stimmt nicht überein.')
                    rows = tracker.snapshot()['days']
                    count = sum(row['count'] for day in rows.values() for row in day.values())
                    if count != (writes if mode == 'enabled' else 0):
                        raise RuntimeError('Messzähler stimmt nicht überein.')
                    samples.append({'round': index + 1, 'mode': mode,
                                    'write_ms': write_ms, 'flush_ms': flush_ms,
                                    'total_ms': write_ms + flush_ms, 'count': count})
                    tracker.data_path.unlink(missing_ok=True)
    finally:
        performance._ACTIVE = previous
    medians = {mode: statistics.median(s['total_ms'] for s in samples if s['mode'] == mode)
               for mode in MODES}
    overhead = {mode: (medians[mode] / medians['baseline'] - 1) * 100
                for mode in MODES[1:]}
    return {'schema_version': 1, 'utc': datetime.now(timezone.utc).isoformat(),
            'python': platform.python_version(), 'system': platform.platform(),
            'rounds': rounds, 'writes_per_round': writes, 'bytes_per_write': size,
            'samples': samples, 'median_total_ms': medians, 'overhead_percent': overhead,
            'scope': 'Synthetic warmed atomic writes; one flush per batch. No GUI/startup or target-device acceptance.',
            'one_percent_target_proven': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rounds', type=int, default=9)
    parser.add_argument('--writes', type=int, default=100)
    parser.add_argument('--bytes', type=int, default=4096)
    parser.add_argument('--temp-parent', type=Path, help='Datenträger für isolierte temporäre Messdateien')
    args = parser.parse_args()
    try:
        result = run(args.rounds, args.writes, args.bytes, args.temp_parent)
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(1, f'Benchmark abgebrochen: {error}\n')
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True,
                          text=True, timeout=5, check=False)
    result['source_head'] = head.stdout.strip() if head.returncode == 0 else None
    result['source_dirty'] = bool(subprocess.run(
        ['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True,
        text=True, timeout=5, check=True).stdout)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
