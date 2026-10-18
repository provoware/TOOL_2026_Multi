"""Persönliche Daten sichern und ausschließlich in einen neuen Ordner zurückholen."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
import uuid
import zipfile
from datetime import datetime, timezone

MAX_FILES = 10000
MAX_FILE = 64 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
INDEX = 'sicherung.json'


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def inventory(source):
    if source.is_symlink() or not source.is_dir():
        raise ValueError('Der Datenordner fehlt oder ist eine Verknüpfung.')
    files, total = {}, 0
    for path in sorted(source.rglob('*')):
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode) or not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
            raise ValueError('Verknüpfungen und Spezialdateien werden nicht gesichert.')
        if path.is_dir():
            continue
        size = path.stat().st_size
        total += size
        if size > MAX_FILE or total > MAX_TOTAL or len(files) >= MAX_FILES:
            raise ValueError('Die feste Größen- oder Dateigrenze wurde überschritten.')
        files[path.relative_to(source).as_posix()] = {'size': size, 'sha256': digest(path)}
    return files


def checked_index(archive):
    infos = archive.infolist()
    if len(infos) > MAX_FILES + 1 or len({i.filename for i in infos}) != len(infos):
        raise ValueError('Zu viele oder doppelte Archiveinträge.')
    total = 0
    for info in infos:
        name = info.filename
        path = PurePosixPath(name)
        mode = info.external_attr >> 16
        if (path.is_absolute() or '..' in path.parts or '\\' in name
                or path.as_posix() != name or info.is_dir()
                or stat.S_IFMT(mode) not in (0, stat.S_IFREG) or info.flag_bits & 1
                or info.file_size > MAX_FILE):
            raise ValueError('Unsicherer Archiveintrag.')
        total += info.file_size
    if total > MAX_TOTAL or archive.getinfo(INDEX).file_size > 4 * 1024 * 1024:
        raise ValueError('Archiv ist zu groß.')
    metadata = json.loads(archive.read(INDEX))
    if not isinstance(metadata, dict) or metadata.get('schema_version') != 1:
        raise ValueError('Unbekanntes Sicherungsformat.')
    files = metadata.get('files')
    if not isinstance(files, dict) or len(files) > MAX_FILES:
        raise ValueError('Ungültiges Dateiverzeichnis.')
    if {i.filename for i in infos} != {INDEX, *('daten/' + name for name in files)}:
        raise ValueError('Archiv und Dateiverzeichnis stimmen nicht überein.')
    for name, row in files.items():
        if (not isinstance(row, dict) or type(row.get('size')) is not int
                or row['size'] < 0 or archive.getinfo('daten/' + name).file_size != row['size']
                or not isinstance(row.get('sha256'), str) or len(row['sha256']) != 64):
            raise ValueError('Ungültiger Größen- oder Prüfsummeneintrag.')
    return metadata


def restore(backup, destination):
    backup, destination = Path(backup), Path(destination)
    expected = backup.with_suffix(backup.suffix + '.sha256').read_text(encoding='utf-8').split()[0]
    if digest(backup) != expected:
        raise ValueError('Die Prüfsumme stimmt nicht. Keine Daten wurden ersetzt.')
    with zipfile.ZipFile(backup) as archive:
        metadata = checked_index(archive)
        # Atomare Reservierung: Auch ein leerer vorhandener Ordner bleibt geschützt.
        destination.mkdir(parents=False, exist_ok=False, mode=0o700)
        try:
            for name, row in metadata['files'].items():
                target = destination / 'daten' / name
                target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                with archive.open('daten/' + name) as source, target.open('xb') as output:
                    os.chmod(target, 0o600)
                    shutil.copyfileobj(source, output, length=1024 * 1024)
                if digest(target) != row['sha256']:
                    raise ValueError('Eine Dateiprüfsumme stimmt nicht.')
            (destination / 'daten').mkdir(exist_ok=True, mode=0o700)
            if inventory(destination / 'daten') != metadata['files']:
                raise ValueError('Die wiederhergestellten Dateien weichen ab.')
        except BaseException:
            shutil.rmtree(destination)
            raise
    return metadata


def create(source, output):
    source, output = Path(source), Path(output)
    if output.resolve().is_relative_to(source.resolve()):
        raise ValueError('Sicherungen müssen außerhalb des Datenordners liegen.')
    before = inventory(source)
    output.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = output / f'Provoware_Daten_{stamp}_{uuid.uuid4().hex[:12]}.zip'
    metadata = {'schema_version': 1, 'utc': stamp, 'files': before}
    descriptor, temporary = tempfile.mkstemp(prefix='.datensicherung-', dir=output)
    os.close(descriptor)
    temporary = Path(temporary)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(INDEX, json.dumps(metadata, ensure_ascii=False))
            for name in before:
                archive.write(source / name, 'daten/' + name)
        if inventory(source) != before:
            raise ValueError('Daten wurden während der Sicherung verändert. Programm schließen und erneut versuchen.')
        # Prüft das fertige ZIP und jeden Inhalt vor Veröffentlichung.
        with zipfile.ZipFile(temporary) as archive:
            checked_index(archive)
            for name, row in before.items():
                if hashlib.sha256(archive.read('daten/' + name)).hexdigest() != row['sha256']:
                    raise ValueError('Sicherungsinhalt stimmt nicht überein.')
        with temporary.open('rb') as stream:
            os.fsync(stream.fileno())
        os.link(temporary, backup)  # Kein vorhandenes Archiv überschreiben.
        checksum = backup.with_suffix(backup.suffix + '.sha256')
        with checksum.open('x', encoding='utf-8') as stream:
            os.chmod(checksum, 0o600)
            stream.write(f'{digest(backup)}  {backup.name}\n')
            stream.flush()
            os.fsync(stream.fileno())
        with tempfile.TemporaryDirectory(prefix='.daten-restore-', dir=output) as folder:
            restore(backup, Path(folder) / 'pruefung')
    finally:
        temporary.unlink(missing_ok=True)
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    backup = commands.add_parser('sichern')
    backup.add_argument('--daten', type=Path, required=True)
    backup.add_argument('--ziel', type=Path, required=True)
    backup.add_argument('--programm-geschlossen', action='store_true', required=True,
                        help='Nur bei geschlossenem Provoware sichern; verhindert uneinheitliche Datenstände.')
    recover = commands.add_parser('wiederherstellen')
    recover.add_argument('--archiv', type=Path, required=True)
    recover.add_argument('--neu', type=Path, required=True, help='Neuer, noch nicht vorhandener Ordner')
    args = parser.parse_args()
    try:
        if args.command == 'sichern':
            result = create(args.daten, args.ziel)
            print(f'Sicherung und isolierte Wiederherstellung geprüft: {result}')
        else:
            metadata = restore(args.archiv, args.neu)
            print(f'{len(metadata["files"])} Dateien geprüft in neuem Ordner: {args.neu}')
    except (OSError, ValueError, KeyError, IndexError, zipfile.BadZipFile) as error:
        parser.exit(1, f'Datensicherung abgebrochen ({type(error).__name__}): {error}\n'
                       'Vorhandene Arbeitsdaten wurden nicht ersetzt. Pfade und freien Speicher prüfen.\n')


if __name__ == '__main__':
    main()
