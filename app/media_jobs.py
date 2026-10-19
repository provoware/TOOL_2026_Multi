"""Sichere FFmpeg-Befehle für Bilderslideshows und Video-Audio-Kombination.

Keine Shell, kein Überschreiben fremder Dateien. Aufträge werden im Fenster
seriell über QProcess ausgeführt und können jederzeit abgebrochen werden.
"""
from __future__ import annotations
from pathlib import Path
import re
from app import media_files as media
from app import module_archive


def output_target(root, destination, sources):
    if not isinstance(destination, (str, Path)) or not str(destination):
        raise ValueError("Ausgabe ist nicht gewählt.")
    target = Path(destination).expanduser()
    if not target.is_absolute() or target.suffix.lower() != ".mp4" or ".." in target.parts:
        raise ValueError("Ausgabename muss ein absoluter MP4-Dateipfad sein.")
    if target.is_symlink() or target.exists():
        raise ValueError("Ausgabedatei existiert bereits und wird nicht überschrieben.")
    target = module_archive.export_target(root, target)
    if target in [Path(v).resolve() for v in sources]:
        raise ValueError("Eingabe- und Ausgabedatei müssen getrennt sein.")
    if not target.parent.is_dir():
        raise ValueError("Ausgabeordner fehlt.")
    return target


def slideshow_command(root, images, destination, *, seconds=5, audio=None):
    if (not isinstance(images, (list, tuple)) or not 1 <= len(images) <= 20
            or isinstance(seconds, bool) or not isinstance(seconds, (int, float))
            or not 1 <= seconds <= 30):
        raise ValueError("Es werden 1 bis 20 Bilder und 1 bis 30 Sekunden je Bild benötigt.")
    pics = [media.media_path(item, media.IMAGE) for item in images]
    if len(set(pics)) != len(pics):
        raise ValueError("Bilder dürfen nicht mehrfach gewählt werden.")
    if any(path.stat().st_size > media.MAX_IMAGE for path in pics):
        raise ValueError("Bild ist für die Diashow zu groß.")
    sound = media.media_path(audio, media.AUDIO) if audio else None
    target = output_target(root, destination, pics + ([sound] if sound else []))
    inputs = []
    for pic in pics:
        inputs += ["-loop", "1", "-t", f"{seconds:.3f}", "-i", str(pic)]
    if sound:
        inputs += ["-stream_loop", "-1", "-i", str(sound)]
    blocks = [f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,"
              f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=25,setsar=1,format=yuv420p[v{i}]"
              for i in range(len(pics))]
    blocks.append("".join(f"[v{i}]" for i in range(len(pics))) +
                  f"concat=n={len(pics)}:v=1:a=0[outv]")
    args = ["-hide_banner", "-loglevel", "error", "-nostdin", "-progress", "pipe:1",
            "-n", *inputs, "-filter_complex", ";".join(blocks), "-map", "[outv]"]
    if sound:
        args += ["-map", f"{len(pics)}:a:0", "-c:a", "aac"]
    args += ["-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-movflags", "+faststart", "-t", str(len(pics) * seconds)]
    return args, target, len(pics) * seconds


def video_audio_command(root, video, audio, destination):
    movie = media.media_path(video, media.VIDEO)
    sound = media.media_path(audio, media.AUDIO)
    target = output_target(root, destination, [movie, sound])
    return (["-hide_banner", "-loglevel", "error", "-nostdin",
             "-progress", "pipe:1", "-n",
             "-i", str(movie), "-stream_loop", "-1", "-i", str(sound),
             "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
             "-c:a", "aac", "-shortest", "-movflags", "+faststart"], target, None)
