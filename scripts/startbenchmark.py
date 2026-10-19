"""Echten Programmstart mit synthetischen Daten in neuen Prozessen messen."""
from __future__ import annotations
import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from time import perf_counter_ns

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
GROUPS = {'klein': 1, 'gross': 100}
MARKER = '.startbenchmark-fixture.json'


def fixture(root, count):
    from app.song_document import SongDocument, SongSection, save_song
    for name in ('daten', 'logs', 'berichte', 'backups', 'texte'):
        (root / name).mkdir(parents=True)
    shutil.copyfile(ROOT / 'MANIFEST.json', root / 'MANIFEST.json')
    shutil.copyfile(ROOT / 'texte/registry.json', root / 'texte/registry.json')
    for index in range(count):
        save_song(root, SongDocument(title=f'Messsong {index}', sections=[SongSection('Strophe', 'x' * 4096)]))
    (root / MARKER).write_text(json.dumps({'purpose':'synthetic-startbenchmark-v1','root':str(root.resolve())}))


def worker(root, started_ns):
    marker = json.loads((root / MARKER).read_text())
    if marker != {'purpose':'synthetic-startbenchmark-v1','root':str(root.resolve())}:
        raise ValueError('Kein synthetischer Benchmarkordner.')
    if not root.name.startswith('case-') or not root.parent.name.startswith('provoware-startbenchmark-'):
        raise ValueError('Worker darf nur den eigenen temporären Messbereich starten.')
    from PySide6 import QtWidgets
    from PySide6.QtCore import QTimer
    import app.main as entry
    entry.ROOT = root
    original = QtWidgets.QApplication
    result = {}

    class ProbeApplication(original):
        def exec(self):
            def ready():
                result.update(ready_ms=(perf_counter_ns() - started_ns) / 1_000_000,
                              qpa=self.platformName(), visible=any(w.isVisible() for w in self.topLevelWidgets()))
                self.exit(0)
            QTimer.singleShot(0, ready)
            QTimer.singleShot(10000, lambda: self.exit(2))
            return super().exec()

    # Nur im kurzlebigen Probeprozess; produktive Dateien werden nicht gepatcht.
    QtWidgets.QApplication = ProbeApplication
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            code = entry.main()
    finally:
        QtWidgets.QApplication = original
    if code != 0 or not result.get('visible'):
        raise ValueError('Programmstart erreichte kein sichtbares Dashboard in der Ereignisschleife.')
    return result


def run(rounds=3, qpa='offscreen', temp_parent=None):
    if not 2 <= rounds <= 10 or qpa not in ('offscreen', 'wayland', 'xcb'):
        raise ValueError('2–10 Starts je Gruppe und eine unterstützte Qt-Plattform wählen.')
    samples = []
    with tempfile.TemporaryDirectory(prefix='provoware-startbenchmark-',dir=temp_parent) as folder:
        for group, count in GROUPS.items():
            root = Path(folder) / ('case-' + group)
            fixture(root, count)
            for index in range(rounds):
                start = perf_counter_ns()
                process = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker-root',str(root),
                                          '--start-ns',str(start)], cwd=ROOT,
                                         env=dict(os.environ,QT_QPA_PLATFORM=qpa),capture_output=True,text=True,
                                         timeout=25,check=True)
                total = (perf_counter_ns() - start) / 1_000_000
                values = json.loads(process.stdout)
                samples.append({'group':group,'songs':count,'state':'first_launch_in_series' if index == 0 else 'repeat_launch',
                                'round':index+1,'process_total_ms':total,**values})
    return {'schema_version':1,'python':platform.python_version(),'system':platform.platform(),
            'samples':samples,'readiness':'first event-loop callback after real app.main.main show/refresh',
            'process':'fresh Python process for every sample','os_cache':'uncontrolled; no cache flushing',
            'cold_os_start_proven':False,'target_device_acceptance':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rounds',type=int,default=3)
    parser.add_argument('--qpa',choices=('offscreen','wayland','xcb'),default='offscreen')
    parser.add_argument('--temp-parent',type=Path)
    parser.add_argument('--worker-root',type=Path,help=argparse.SUPPRESS)
    parser.add_argument('--start-ns',type=int,default=0,help=argparse.SUPPRESS)
    args=parser.parse_args()
    try:
        if args.worker_root:
            if args.start_ns <= 0:raise ValueError('Startzeit fehlt.')
            result=worker(args.worker_root,args.start_ns)
        else:
            result=run(args.rounds,args.qpa,args.temp_parent)
    except (OSError,ValueError,subprocess.SubprocessError) as error:
        parser.exit(1,f'Startmessung abgebrochen: {error}\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':main()
