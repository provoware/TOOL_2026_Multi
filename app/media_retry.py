"""Bewusstes und nichtdestruktives Wiederholen fehlgeschlagener Videoaufträge."""
from __future__ import annotations
from pathlib import Path
from app import media_queue, media_files, media_jobs

def retry_failed(root, job_id, *, approved=False):
    if approved is not True:
        raise PermissionError("Wiederholung benötigt eine ausdrückliche Freigabe.")
    state=media_queue.load(root)
    job=next((x for x in state["jobs"] if x["id"]==job_id),None)
    if job is None or job["status"] not in ("failed","interrupted"):
        raise ValueError("Nur fehlgeschlagene oder unterbrochene Aufträge sind wiederholbar.")
    if any(x["status"]=="running" for x in state["jobs"]):
        raise ValueError("Ein anderer Auftrag läuft bereits.")
    if Path(job["output"]).exists() or Path(job["output"]).is_symlink():
        raise ValueError("Das Ausgabeziel ist inzwischen belegt. Keine Datei überschreiben.")
    if job["kind"]=="video_audio":
        if len(job["inputs"])!=2:
            raise ValueError("Video-/Audiopfad fehlt.")
        media_jobs.video_audio_command(root,*job["inputs"],job["output"])
    else:
        sources=list(job["inputs"])
        audio=None
        if sources and Path(sources[-1]).suffix.lower() in media_files.AUDIO:
            audio=sources.pop()
        if job.get("transition","none")=="none":
            media_jobs.slideshow_command(root,sources,job["output"],
                seconds=job["seconds"],fade=job["fade"],audio=audio)
        else:
            media_jobs.crossfade_command(root,sources,job["output"],
                seconds=job["seconds"],transition=job["transition"],
                intensity=job["fade"],audio=audio)
    return media_queue.transition(root,job_id,"waiting")
