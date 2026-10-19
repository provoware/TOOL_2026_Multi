"""Unverändernde Vorprüfung für sichere Migration bestehender Installationen.

Erst nach dieser Prüfung darf ein späterer Migrations-Assistent geplant werden.
Dieser Baustein besitzt absichtlich keinen Schreib-/Umschaltbefehl.
"""
from __future__ import annotations
from pathlib import Path
import json
import stat
from app.update_checkpoint import _released
from app.update_staging import identity

def audit_legacy_install(root, destination):
    root=Path(root).resolve(strict=True)
    destination=Path(destination).resolve(strict=True)
    reasons=[]
    if not root.is_dir() or not destination.is_dir():
        raise ValueError("Programm und Ziel müssen Verzeichnisse sein.")
    if destination==root or destination.is_relative_to(root) or root.is_relative_to(destination):
        reasons.append("Programm- und Zielverzeichnis müssen unabhängig sein.")
    manifest=root/"MANIFEST.json"
    try:
        if manifest.is_symlink() or manifest.stat().st_size>200_000:
            raise ValueError("Manifest fehlt oder ist ungültig.")
        state=json.loads(manifest.read_text(encoding="utf-8"))
        identity(state)
        files=_released(state)
        for name in files:
            entry=root/name
            if entry.is_symlink() or not entry.is_file() or not stat.S_ISREG(entry.stat().st_mode):
                reasons.append("Freigegebene Programmdatei fehlt oder ist verknüpft: "+name)
        personal=root/"daten"
        if personal.is_symlink():
            reasons.append("Persönliche Daten dürfen nicht hinter einem Link liegen.")
        if personal.exists() and not personal.is_dir():
            reasons.append("Persönlicher Datenpfad ist kein Verzeichnis.")
        if (destination/"current").exists() or (destination/"current").is_symlink():
            reasons.append("Das Migrationsziel enthält bereits einen aktiven Programmzeiger.")
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as e:
        reasons.append("Ungültiger Programmstand: "+str(e))
    # Ein sicherer externer Daten-Lebenszyklus und ein neuer Schnellstart
    # sind noch nicht vorhanden. Produktive Freigabe ist IMMER falsch.
    reasons.append("Getrennter dauerhafter Datenstart und geprüfter Migrations-Rollback fehlen.")
    return {"schema_version":1,"source":str(root),"target":str(destination),
            "ready_for_migration":False,"activation_allowed":False,"blockers":reasons}
