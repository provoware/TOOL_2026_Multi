"""Verlustfreie Migrationsprobe: trennt Programmdateien und Daten als neue Kopien.

KEIN Wechsel des produktiven Schnellstarts, KEIN Löschen des Altbestands.
Das Ergebnis dient ausschließlich der späteren geprüften Installation.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from app.atomic_io import atomic_write_json
from app.update_checkpoint import _copy_regular, _released
from app.update_staging import identity, sha256

MAX_FILES=12000
MAX_TOTAL=4*1024*1024*1024
MAX_FILE=512*1024*1024


def _copy_checked(source, target, maximum):
    flags=os.O_RDONLY | getattr(os,"O_NOFOLLOW",0) | getattr(os,"O_NONBLOCK",0)
    fd=os.open(source,flags)
    try:
        initial=os.fstat(fd)
        if not stat.S_ISREG(initial.st_mode) or initial.st_size>maximum:
            raise ValueError("Keine reguläre Datei oder Datei zu groß.")
        target.parent.mkdir(parents=True,exist_ok=True)
        h=hashlib.sha256()
        count=0
        with os.fdopen(fd,"rb",closefd=False) as reader,target.open("xb") as writer:
            while piece:=reader.read(1024*1024):
                count+=len(piece)
                if count>maximum:
                    raise ValueError("Quell-Datei wurde zu groß.")
                writer.write(piece);h.update(piece)
            writer.flush();os.fsync(writer.fileno())
        after=os.fstat(fd)
        if (count!=initial.st_size or after.st_ino!=initial.st_ino
                or after.st_size!=initial.st_size or after.st_mtime_ns!=initial.st_mtime_ns):
            raise ValueError("Quelldatei während der Migration verändert.")
        if sha256(target)!=h.hexdigest():
            raise ValueError("Kopierte Datei weicht vom Original ab.")
        return count
    finally:
        os.close(fd)


def prepare_legacy_copy(source_root, empty_target_parent):
    source=Path(source_root).resolve(strict=True)
    parent=Path(empty_target_parent).resolve(strict=True)
    if (parent==source or parent.is_relative_to(source)
            or source.is_relative_to(parent)
            or not parent.is_dir() or parent.is_symlink()):
        raise ValueError("Getrennter Zielordner außerhalb des alten Programms erforderlich.")
    manifest=source/"MANIFEST.json"
    if manifest.is_symlink() or not manifest.is_file() or manifest.stat().st_size>250000:
        raise ValueError("Programmmanifest fehlt oder ist ungeeignet.")
    data=json.loads(manifest.read_text(encoding="utf-8"))
    identity(data)
    release=_released(data)
    old_data=source/"daten"
    if old_data.is_symlink() or (old_data.exists() and not old_data.is_dir()):
        raise ValueError("Persönliche Daten sind verknüpft oder unlesbar.")
    if not release:
        raise ValueError("Programmdateiliste ist leer.")
    files=[]
    if old_data.exists():
        for path in sorted(old_data.rglob("*")):
            if path.is_symlink():
                raise ValueError("Links innerhalb persönlicher Daten werden nicht migriert.")
            if path.is_dir():
                continue
            if not stat.S_ISREG(path.lstat().st_mode):
                raise ValueError("Spezialdateien dürfen nicht migriert werden.")
            files.append(path)
            if len(files)>MAX_FILES:
                raise ValueError("Zu viele persönliche Dateien.")
    target=Path(tempfile.mkdtemp(prefix="provoware-legacy-copy-",dir=parent))
    try:
        slot=target/"slots"/"base"
        slot.mkdir(parents=True)
        copied_total=0
        for relative in release:
            before=source/relative
            if (before.is_symlink() or not before.is_file()
                    or any(parent.is_symlink() for parent in before.parents if parent.is_relative_to(source))):
                raise ValueError("Programmdatei fehlt oder ist verknüpft.")
            size=_copy_checked(before,slot/relative,MAX_FILE)
            copied_total+=size
            if copied_total>MAX_TOTAL:
                raise ValueError("Kopiermenge überschritten.")
        new_data=target/"persistent"/"daten"
        new_data.mkdir(parents=True)
        for file in files:
            relative=file.relative_to(old_data)
            copied_total+=_copy_checked(file,new_data/relative,MAX_FILE)
            if copied_total>MAX_TOTAL:
                raise ValueError("Kopiermenge überschritten.")
        if sha256(manifest)!=sha256(slot/"MANIFEST.json"):
            raise ValueError("Programmmanifest wurde beim Kopieren verändert.")
        atomic_write_json(target/"migration-report.json",{
            "schema_version":1,
            "status":"COPY_VERIFIED_NOT_ACTIVATED",
            "version":identity(data)["version"],
            "program_files":len(release),
            "personal_files":len(files),
            "bytes_copied":copied_total,
            "old_installation_changed":False,
            "activation_allowed":False,
            "data_path":str(new_data),
        })
        return target
    except BaseException:
        shutil.rmtree(target)
        raise
