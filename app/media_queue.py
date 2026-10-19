"""Persistente, streng serielle Warteschlange für geprüfte FFmpeg-Aufträge.

Nur Zustandsverwaltung, kein automatischer Start nach einem Absturz. Laufende
Aufträge werden beim Wiederherstellen als unterbrochen markiert.
"""
from __future__ import annotations
from pathlib import Path
import json
from uuid import uuid4
from app.atomic_io import atomic_write_json

STATES={"waiting","running","failed","done","interrupted"}
MAX_JOBS=100

def _location(root):
    root=Path(root)
    if (root/"daten").is_symlink() or (root/"daten/medien").is_symlink():
        raise ValueError("Verknüpftes Datenverzeichnis.")
    return root/"daten/medien/job_queue.json"

def validate(data):
    if (not isinstance(data,dict) or set(data)!={"schema_version","jobs"}
        or data["schema_version"]!=1 or not isinstance(data["jobs"],list)
        or len(data["jobs"])>MAX_JOBS):
        raise ValueError("Ungültige Warteschlange.")
    result=[]; seen=set()
    for job in data["jobs"]:
        if not isinstance(job,dict) or set(job)!={"id","kind","status","inputs","output","seconds","fade"}:
            raise ValueError("Ungültige Auftragsfelder.")
        from app.module_archive import identifier
        identifier(job["id"])
        if job["id"] in seen or job["kind"] not in ("slideshow","video_audio") or job["status"] not in STATES:
            raise ValueError("Unzulässiger Auftrag oder doppelte Kennung.")
        seen.add(job["id"])
        if (not isinstance(job["inputs"],list) or not 1<=len(job["inputs"])<=21
            or any(not isinstance(v,str) or not Path(v).is_absolute() or ".." in Path(v).parts for v in job["inputs"])
            or not isinstance(job["output"],str) or not Path(job["output"]).is_absolute()
            or Path(job["output"]).suffix.lower()!=".mp4"
            or type(job["seconds"]) is not int or not 1<=job["seconds"]<=30
            or type(job["fade"]) is not int or not 0<=job["fade"]<=100):
            raise ValueError("Ungültige Auftragsparameter.")
        result.append(dict(job))
    return {"schema_version":1,"jobs":result}

def load(root):
    path=_location(root)
    if not path.exists():
        return {"schema_version":1,"jobs":[]}
    if path.is_symlink() or path.stat().st_size>300_000:
        raise ValueError("Warteschlange ist verknüpft oder zu groß.")
    data=validate(json.loads(path.read_text(encoding="utf-8")))
    changed=False
    for job in data["jobs"]:
        if job["status"]=="running":
            job["status"]="interrupted";changed=True
    if changed:
        atomic_write_json(path,data)
    return data

def enqueue(root,*,kind,inputs,output,seconds=5,fade=0):
    state=load(root)
    job={"id":uuid4().hex,"kind":kind,"status":"waiting","inputs":list(inputs),
         "output":output,"seconds":seconds,"fade":fade}
    state["jobs"].append(job)
    validate(state)
    atomic_write_json(_location(root),state)
    return job

def transition(root,job_id,to_status):
    if to_status not in {"running","done","failed","waiting"}:
        raise ValueError("Unzulässiger Zustand.")
    state=load(root)
    job=next((x for x in state["jobs"] if x["id"]==job_id),None)
    if job is None:
        raise ValueError("Auftrag nicht vorhanden.")
    allowed={"waiting":{"running"},"running":{"done","failed"},"failed":{"waiting"},
             "interrupted":{"waiting"},"done":set()}
    if to_status not in allowed[job["status"]]:
        raise ValueError("Ungültiger Zustandswechsel.")
    if to_status=="running" and any(x["status"]=="running" for x in state["jobs"]):
        raise ValueError("Es darf nur ein FFmpeg-Auftrag laufen.")
    job["status"]=to_status
    atomic_write_json(_location(root),validate(state))
    return dict(job)
