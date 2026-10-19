"""Sichere FFmpeg-Befehle für Bilderslideshows und Video-Audio-Kombination.

Keine Shell, kein Überschreiben fremder Dateien. Aufträge werden im Fenster
seriell über QProcess ausgeführt und können jederzeit abgebrochen werden.
"""
from __future__ import annotations
from pathlib import Path
import re
from app import media_files as media
from app import module_archive
from app.media_effects import fade_filter


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


def slideshow_command(root, images, destination, *, seconds=5, audio=None, fade=0):
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
              f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=25,setsar=1,"
              + fade_filter(i, seconds, fade)
              + f"format=yuv420p[v{i}]"
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


def crossfade_command(root, images, destination, *, seconds=5, transition="fade", intensity=50, audio=None):
    """Echte Bild-zu-Bild-Überblendungen mit verkürzter Gesamtdauer."""
    if transition not in ("fade", "wipeleft", "slideright", "circleopen"):
        raise ValueError("Unbekannter Übergangstyp.")
    if type(intensity) is not int or not 1 <= intensity <= 100:
        raise ValueError("Übergangsstärke muss zwischen 1 und 100 liegen.")
    if not isinstance(images, (list, tuple)) or not 2 <= len(images) <= 20:
        raise ValueError("Mindestens zwei, höchstens zwanzig Bilder benötigt.")
    if type(seconds) not in (int, float) or not 2 <= seconds <= 30:
        raise ValueError("Jedes Bild benötigt 2 bis 30 Sekunden.")
    pics = [media.media_path(item, media.IMAGE) for item in images]
    if len(set(pics)) != len(pics):
        raise ValueError("Doppelte Bilder sind nicht zulässig.")
    if any(path.stat().st_size > media.MAX_IMAGE for path in pics):
        raise ValueError("Bildgröße überschreitet die Schutzgrenze.")
    sound = media.media_path(audio, media.AUDIO) if audio else None
    target = output_target(root, destination, pics + ([sound] if sound else []))
    duration = round(min(1.5, seconds * 0.45) * intensity / 100, 3)
    duration = max(0.1, duration)
    total = round(len(pics) * seconds - (len(pics) - 1) * duration, 3)
    args = ["-hide_banner", "-loglevel", "error", "-nostdin", "-progress", "pipe:1", "-n"]
    for picture in pics:
        args += ["-loop", "1", "-t", f"{seconds:.3f}", "-i", str(picture)]
    if sound:
        args += ["-stream_loop", "-1", "-i", str(sound)]
    parts = []
    for i in range(len(pics)):
        parts.append(
            f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=25,"
            f"setsar=1,format=yuv420p,settb=AVTB[v{i}]"
        )
    last = "v0"
    for i in range(1, len(pics)):
        output = f"x{i}"
        offset = round(i * (seconds - duration), 3)
        parts.append(f"[{last}][v{i}]xfade=transition={transition}:"
                     f"duration={duration:.3f}:offset={offset:.3f}[{output}]")
        last = output
    args += ["-filter_complex", ";".join(parts), "-map", f"[{last}]"]
    if sound:
        args += ["-map", f"{len(pics)}:a:0", "-c:a", "aac"]
    args += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags",
             "+faststart", "-t", f"{total:.3f}"]
    return args, target, total
