"""Ein fertiges Video wird erst nach strenger ffprobe-Prüfung veröffentlicht."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess

def verify_video(path, *, require_audio=False, timeout=20):
    path=Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size <= 0:
        raise ValueError("Ausgabe ist leer oder verknüpft.")
    probe=shutil.which("ffprobe")
    if probe is None:
        raise ValueError("FFprobe fehlt; Video wird nicht freigegeben.")
    try:
        done=subprocess.run([probe,"-v","error","-show_entries",
            "format=duration:stream=codec_type,width,height", "-of","json",str(path)],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,
            check=False)
    except (OSError,subprocess.TimeoutExpired) as error:
        raise ValueError("Videoausgabe konnte nicht geprüft werden.") from error
    if done.returncode or len(done.stdout)>1_000_000:
        raise ValueError("FFprobe meldet einen Medienfehler.")
    try:
        result=json.loads(done.stdout.decode("utf-8"))
        streams=result["streams"]
        duration=float(result["format"]["duration"])
        if not 0 < duration <= 24*3600:
            raise ValueError("Ungültige Videodauer.")
        if not isinstance(streams,list) or not all(isinstance(s,dict) for s in streams):
            raise ValueError("Ungültige Spurdaten.")
        if not any(
            s.get("codec_type")=="video" and
            isinstance(s.get("width"),int) and s["width"]>0 and
            isinstance(s.get("height"),int) and s["height"]>0
            for s in streams):
            raise ValueError("Video hat keine gültige Bildspur.")
        if require_audio and not any(s.get("codec_type")=="audio" for s in streams):
            raise ValueError("Audiospur fehlt.")
    except (KeyError,TypeError,ValueError,OverflowError) as error:
        raise ValueError("Ungültige FFprobe-Ausgabe.") from error
    return {"duration_seconds":duration,"video":True,
            "audio":any(x.get("codec_type")=="audio" for x in streams)}
