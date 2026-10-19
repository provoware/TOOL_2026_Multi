"""Validierte FFmpeg-Überblendung mit begrenzter Intensität.

Einblendungen pro Bild sind zunächst nur eine gleichmäßige Alpha-Überblendung,
keine Überlagerung zweier Bilder. Ein echter xfade-Übergang folgt getrennt.
"""
from __future__ import annotations

def fade_filter(index, duration, intensity):
    if (type(index) is not int or index<0 or type(duration) not in (int,float)
        or duration<1 or duration>30 or type(intensity) is not int
        or not 0<=intensity<=100):
        raise ValueError("Ungültige Effektparameter.")
    strength=round(min(duration/3,2.0)*intensity/100,3)
    if strength==0:
        return ""
    return f"fade=t=in:st=0:d={strength:.3f},fade=t=out:st={max(0,duration-strength):.3f}:d={strength:.3f},"
