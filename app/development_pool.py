"""Lokaler Entwicklungs-/Arbeitsverzeichnispool mit Kopien und begrenzten Archiven."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from uuid import uuid4
import zipfile

from app import module_archive as archive
from app.atomic_io import atomic_publish_file

MODULE, COLLECTION = "entwicklungspool", "projects"
STATES = ("offen", "aktiv", "fertig", "archiviert")
MAX_FILES = 500
MAX_FILE = 16 * 1024 * 1024
MAX_TOTAL = 64 * 1024 * 1024


def validate_project(raw):
    if not isinstance(raw, dict) or set(raw) != {"id", "name", "description", "status"}:
        raise ValueError("Ungültiger Projektbestand.")
    archive.identifier(raw["id"])
    archive.text(raw["name"], "Projektname", required=True, limit=150)
    archive.text(raw["description"], "Beschreibung", limit=4000)
    if raw["status"] not in STATES:
        raise ValueError("Unbekannter Projektstatus.")
    return deepcopy(raw)


def validate(raw):
    if (not isinstance(raw, dict) or set(raw) != {"schema_version", COLLECTION}
            or raw["schema_version"] != 1 or not isinstance(raw[COLLECTION], list)
            or len(raw[COLLECTION]) > 200):
        raise ValueError("Ungültiger Entwicklungsarchivbestand.")
    projects = [validate_project(x) for x in raw[COLLECTION]]
    if (len({p["id"] for p in projects}) != len(projects)
            or len({p["name"].casefold() for p in projects}) != len(projects)):
        raise ValueError("Projektkennungen oder Namen sind doppelt.")
    return {"schema_version": 1, COLLECTION: projects}


def load(root):
    return archive.load(root, MODULE, validate,
                        lambda: {"schema_version": 1, COLLECTION: []})


def _pool_dir(root):
    root = Path(root).resolve()
    path = root / "daten" / MODULE
    if path.is_symlink() or (root / "daten").is_symlink():
        raise ValueError("Verknüpfter Poolordner wird nicht verwendet.")
    return path


def workspace(root, project_id):
    archive.identifier(project_id)
    parent = _pool_dir(root) / "arbeitsordner"
    if parent.is_symlink() or (parent / project_id).is_symlink():
        raise ValueError("Projektarbeitsordner darf kein symbolischer Link sein.")
    return parent / project_id


def put(root, project):
    record = validate_project(project)
    state = load(root)
    existing = next((i for i, x in enumerate(state[COLLECTION]) if x["id"] == record["id"]), None)
    created_folder = None
    if existing is None:
        target = workspace(root, record["id"])
        if target.exists():
            raise ValueError("Arbeitsordner ist bereits vorhanden.")
        target.mkdir(parents=True)
        created_folder = target
        state[COLLECTION].append(record)
    else:
        target = workspace(root, record["id"])
        if not target.is_dir():
            raise ValueError("Projektarbeitsordner fehlt.")
        state[COLLECTION][existing] = record
    try:
        archive.save(root, MODULE, state, validate)
    except BaseException:
        if created_folder is not None:
            created_folder.rmdir()
        raise
    return deepcopy(record)


def _project(root, project_id):
    return next((p for p in load(root)[COLLECTION] if p["id"] == project_id),
                None)


def _files(root, project_id):
    if _project(root, project_id) is None:
        raise ValueError("Unbekanntes Projekt.")
    source = workspace(root, project_id)
    if not source.is_dir() or source.is_symlink():
        raise ValueError("Projektarbeitsordner fehlt.")
    result, total = [], 0
    for item in sorted(source.rglob("*")):
        mode = item.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise ValueError("Links oder Spezialdateien sind nicht erlaubt.")
        size = item.stat().st_size
        total += size
        if size > MAX_FILE or total > MAX_TOTAL or len(result) >= MAX_FILES:
            raise ValueError("Projektarbeitsordner überschreitet Schutzgrenzen.")
        result.append((item.relative_to(source).as_posix(), size))
    return source, result


def list_files(root, project_id):
    return [name for name, _ in _files(root, project_id)[1]]


def copy_workspace(root, project_id):
    """Erzeugt unabhängige nummerierte Kopien unter daten/, niemals Überschreiben."""
    source, entries = _files(root, project_id)
    copies = _pool_dir(root) / "kopien"
    if copies.is_symlink():
        raise ValueError("Kopierziel ist ein Link.")
    copies.mkdir(parents=True, exist_ok=True)
    target = Path(tempfile.mkdtemp(prefix=project_id + "-", dir=copies))
    try:
        for relative, size in entries:
            original = source / relative
            descriptor = os.open(original, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            try:
                if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                    raise ValueError("Datei hat sich in einen Link verwandelt.")
                dest = target / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                with os.fdopen(descriptor, "rb", closefd=False) as input_stream, dest.open("xb") as output:
                    data = input_stream.read(MAX_FILE + 1)
                    if len(data) != size:
                        raise ValueError("Projektdatei wurde während der Kopie verändert.")
                    output.write(data)
            finally:
                os.close(descriptor)
        return target
    except BaseException:
        shutil.rmtree(target)
        raise


def archive_workspace(root, project_id, destination):
    """Schützt persönliche Projekte vor Archiv-Überschreiben und ZIP-Pfadtricks."""
    project = _project(root, project_id)
    if project is None:
        raise ValueError("Projekt nicht gefunden.")
    source, files = _files(root, project_id)
    target = archive.export_target(root, destination)
    if target.exists() or target.is_symlink():
        raise ValueError("Archivziel existiert bereits.")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmpname = tempfile.mkstemp(prefix=".provoware-pool-", suffix=".tmp", dir=target.parent)
    os.close(fd)
    temporary = Path(tmpname)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as output:
            output.writestr("projekt.json", json.dumps(project, ensure_ascii=False))
            for relative, size in files:
                path = source / relative
                if path.is_symlink() or path.stat().st_size != size:
                    raise ValueError("Projekt wurde während der Archivierung verändert.")
                output.write(path, arcname="arbeit/" + relative)
        with zipfile.ZipFile(temporary) as check:
            if check.testzip() is not None or set(check.namelist()) != {
                    "projekt.json", *("arbeit/" + name for name, _ in files)}:
                raise ValueError("Archiv wurde nicht korrekt geschrieben.")
        if target.exists():
            raise ValueError("Archiv wurde inzwischen erstellt.")
        atomic_publish_file(temporary, target)
        return target
    finally:
        temporary.unlink(missing_ok=True)
