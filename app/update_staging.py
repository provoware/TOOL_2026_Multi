"""Update-Pakete isoliert prüfen; keine Aktivierung und kein Ausführen fremden Codes."""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import zipfile

from app.atomic_io import atomic_write_json

MAX_ARCHIVE = 32 * 1024 * 1024
MAX_FILE = 8 * 1024 * 1024
MAX_TOTAL = 64 * 1024 * 1024
MAX_FILES = 1000
IDENTITY = ('TOOL_2026_Multi', 'provoware/TOOL_2026_Multi')
ROOT_FILES = {'MANIFEST.json', 'README.md', 'ANLEITUNG_LAIEN.md',
              'requirements.txt', 'schnellstart.sh', 'kubuntu_abnahme.sh'}
ROOT_DIRS = {'app', 'scripts', 'texte', 'vorlagen', 'docs'}
REQUIRED = {'MANIFEST.json', 'requirements.txt', 'schnellstart.sh', 'app/main.py'}


def sha256(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{1,8}\.\d{1,8}\.\d{1,8}', value):
        raise ValueError('Programmversion ist ungültig.')
    return tuple(map(int, value.split('.')))


def safe_name(name):
    if not isinstance(name, str) or not name or len(name) > 240:
        raise ValueError('Ungültiger Paketpfad.')
    path = PurePosixPath(name)
    if (path.is_absolute() or path.as_posix() != name or '..' in path.parts
            or any(c in name for c in ('\\', ':', '\0'))
            or any(part.startswith('.') or part != part.strip() for part in path.parts)):
        raise ValueError('Unsicherer Paketpfad.')
    if (len(path.parts) == 1 and name not in ROOT_FILES
            or len(path.parts) > 1 and path.parts[0] not in ROOT_DIRS):
        raise ValueError('Paket enthält nicht freigegebene Arbeits- oder interne Dateien.')
    return path


def identity(manifest):
    if not isinstance(manifest, dict) or not isinstance(manifest.get('tool'), dict):
        raise ValueError('Ungültiges Programmmanifest.')
    tool = manifest['tool']
    if (tool.get('name'), tool.get('repository')) != IDENTITY:
        raise ValueError('Das Paket gehört nicht zu diesem Programm/Repository.')
    version(tool.get('version'))
    return tool


def inspect_archive(archive, current):
    infos = archive.infolist()
    if not infos or len(infos) > MAX_FILES:
        raise ValueError('Zu viele oder keine Paketdateien.')
    names, total = set(), 0
    for item in infos:
        name = safe_name(item.filename).as_posix()
        folded = name.casefold()
        mode = item.external_attr >> 16
        if (folded in names or item.is_dir() or item.flag_bits & 1
                or stat.S_IFMT(mode) not in (0, stat.S_IFREG)
                or item.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)):
            raise ValueError('Doppelte, verschlüsselte oder besondere Paketdatei.')
        names.add(folded)
        total += item.file_size
        if item.file_size > MAX_FILE or total > MAX_TOTAL:
            raise ValueError('Paket überschreitet die feste Größenbegrenzung.')
    if archive.getinfo('MANIFEST.json').file_size > 2 * 1024 * 1024:
        raise ValueError('Paketmanifest ist zu groß.')
    candidate = json.loads(archive.read('MANIFEST.json'))
    tool = identity(candidate)
    if version(tool['version']) <= version(identity(current)['version']):
        raise ValueError('Das Paket muss eine neuere Programmversion enthalten.')
    entries = candidate.get('files')
    if not isinstance(entries, list) or len(entries) > MAX_FILES:
        raise ValueError('Paketmanifest enthält keine gültige Dateiliste.')
    released, all_paths = set(), set()
    for entry in entries:
        if not isinstance(entry, dict) or type(entry.get('release')) is not bool:
            raise ValueError('Ungültiger Freigabeeintrag im Paketmanifest.')
        name = entry.get('path')
        if not isinstance(name, str) or name.casefold() in all_paths:
            raise ValueError('Doppelter oder ungültiger Manifestpfad.')
        all_paths.add(name.casefold())
        if entry['release']:
            released.add(safe_name(name).as_posix())
    if set(i.filename for i in infos) != released or not REQUIRED <= released:
        raise ValueError('ZIP-Inhalt entspricht nicht exakt den freigegebenen Manifestdateien.')
    return candidate


def _copy_package(source, target):
    descriptor = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_ARCHIVE:
            raise ValueError('Update muss eine reguläre ZIP-Datei bis 32 MiB sein.')
        with target.open('xb') as output:
            os.chmod(target, 0o600)
            remaining = MAX_ARCHIVE + 1
            while remaining:
                block = stream.read(min(1024 * 1024, remaining))
                if not block:
                    break
                output.write(block)
                remaining -= len(block)
            if output.tell() > MAX_ARCHIVE:
                raise ValueError('Update-Datei ist während des Lesens zu groß geworden.')
            output.flush()
            os.fsync(output.fileno())


def _extract(archive, candidate):
    hashes = {}
    for item in archive.infolist():
        target = candidate.joinpath(*safe_name(item.filename).parts)
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with archive.open(item) as source, target.open('xb') as output:
            os.chmod(target, 0o700 if (item.external_attr >> 16) & 0o111 else 0o600)
            digest = hashlib.sha256()
            remaining = item.file_size
            while remaining:
                chunk = source.read(min(remaining, 1024 * 1024))
                if not chunk:
                    raise ValueError('Paketdatei wurde unvollständig gelesen.')
                output.write(chunk)
                digest.update(chunk)
                remaining -= len(chunk)
            if source.read(1):
                raise ValueError('Paketdatei ist größer als angekündigt.')
            output.flush()
            os.fsync(output.fileno())
        if sha256(target) != digest.hexdigest():
            raise ValueError('Entpackte Paketdatei stimmt nicht mit dem Archiv überein.')
        hashes[item.filename] = digest.hexdigest()
    return hashes


def _static_checks(candidate):
    checked = []
    for path in sorted(candidate.rglob('*')):
        if path.suffix == '.py':
            ast.parse(path.read_bytes(), filename=path.relative_to(candidate).as_posix())
            checked.append(path.relative_to(candidate).as_posix())
        elif path.suffix == '.json':
            json.loads(path.read_text(encoding='utf-8'))
            checked.append(path.relative_to(candidate).as_posix())
    for raw in (candidate / 'requirements.txt').read_text(encoding='utf-8').splitlines():
        line = raw.split('#', 1)[0].strip()
        if line and not re.fullmatch(r'[A-Za-z0-9_.-]+==[A-Za-z0-9_.+!-]+', line):
            raise ValueError('Abhängigkeiten müssen feste Paketversionen ohne Installationsoptionen verwenden.')
    return checked


def stage_update(root, package, expected_sha, basis_sha, staging_parent):
    for value in (expected_sha, basis_sha):
        if not isinstance(value, str) or not re.fullmatch(r'[a-fA-F0-9]{64}', value):
            raise ValueError('Eine vollständige SHA-256-Prüfsumme ist erforderlich.')
    root = Path(root).resolve(strict=True)
    current_path = root / 'MANIFEST.json'
    if sha256(current_path) != basis_sha.lower():
        raise ValueError('Ausgangsmanifest wurde verändert. Kein Staging angelegt.')
    current = json.loads(current_path.read_text(encoding='utf-8'))
    identity(current)
    parent = Path(staging_parent).resolve(strict=True)
    if parent.is_relative_to(root):
        raise ValueError('Staging muss vollständig außerhalb des aktiven Projektordners liegen.')
    owned = Path(tempfile.mkdtemp(prefix='provoware-update-', dir=parent))
    try:
        copied = owned / 'package.zip'
        _copy_package(package, copied)
        if sha256(copied) != expected_sha.lower():
            raise ValueError('Paketprüfsumme stimmt nicht. Staging wird verworfen.')
        with zipfile.ZipFile(copied) as archive:
            manifest = inspect_archive(archive, current)
            candidate = owned / 'candidate'
            candidate.mkdir(mode=0o700)
            hashes = _extract(archive, candidate)
        checked = _static_checks(candidate)
        if sha256(current_path) != basis_sha.lower():
            raise ValueError('Ausgangsmanifest wurde während der Prüfung verändert.')
        receipt = {'schema_version': 1, 'status': 'STATICALLY_VERIFIED_NOT_ACTIVATABLE',
                   'basis_manifest_sha256': basis_sha.lower(), 'package_sha256': expected_sha.lower(),
                   'from_version': current['tool']['version'], 'to_version': manifest['tool']['version'],
                   'files': hashes, 'static_checks': checked, 'activation_allowed': False,
                   'candidate_code_executed': False, 'runtime_tests': 'NOT_RUN',
                   'active_project_changed': False}
        atomic_write_json(owned / 'stage-report.json', receipt)
        return owned, receipt
    except BaseException:
        shutil.rmtree(owned)
        raise
