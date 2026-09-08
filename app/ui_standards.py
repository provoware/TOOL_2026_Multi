"""Globale Oberflächenstandards für Farben, Abstände, Zoom und Statusdarstellung."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from app.recovery_ui import zoom_font_size

COLORS = {
    "background": "#121722",
    "surface": "#1B2330",
    "surface_alt": "#243044",
    "text": "#F4F7FB",
    "muted": "#B8C3D4",
    "accent": "#42D7C7",
    "green": "#66D39A",
    "yellow": "#FFD166",
    "red": "#FF6B7A",
    "blocked": "#9AA7BA",
}

SPACING = {"xs": 4, "s": 8, "m": 12, "l": 20, "xl": 28}
FONTS = {"body_size": 11, "small_size": 10, "title_size": 20}

SEVERITY_STATUS = {
    "INFO": ("🟢", COLORS["green"]),
    "HINWEIS": ("🟢", COLORS["green"]),
    "WARNUNG": ("🟡", COLORS["yellow"]),
    "FEHLER": ("🔴", COLORS["red"]),
    "KRITISCH": ("🔴", COLORS["red"]),
    "SCHWER": ("🔴", COLORS["red"]),
    "ABSTURZ": ("🔴", COLORS["red"]),
}


def configure_global_style(root: tk.Misc, zoom_percent: int = 100) -> ttk.Style:
    """Wendet einen einzigen, wiederverwendbaren Stil auf Standardbausteine an."""
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    body = zoom_font_size(FONTS["body_size"], zoom_percent)
    small = zoom_font_size(FONTS["small_size"], zoom_percent)
    title = zoom_font_size(FONTS["title_size"], zoom_percent)
    root.configure(background=COLORS["background"])
    style.configure(".", font=("TkDefaultFont", body), background=COLORS["background"], foreground=COLORS["text"])
    style.configure("TFrame", background=COLORS["background"])
    style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"])
    style.configure("Title.TLabel", font=("TkDefaultFont", title, "bold"), foreground=COLORS["text"])
    style.configure("Muted.TLabel", foreground=COLORS["muted"])
    style.configure("TButton", padding=(SPACING["m"], SPACING["s"]))
    style.map("TButton", foreground=[("disabled", COLORS["blocked"])])
    style.configure("TCombobox", padding=SPACING["xs"])
    style.configure("Treeview", font=("TkDefaultFont", body), rowheight=zoom_font_size(30, zoom_percent),
                    background=COLORS["surface"], fieldbackground=COLORS["surface"],
                    foreground=COLORS["text"], borderwidth=0)
    style.configure("Treeview.Heading", background=COLORS["surface_alt"], foreground=COLORS["text"],
                    font=("TkDefaultFont", small, "bold"))
    style.map("Treeview", background=[("selected", COLORS["surface_alt"])])
    return style


def severity_display(severity: str) -> tuple[str, str]:
    """Liefert Ampelsymbol und Textfarbe für einen Schweregrad."""
    return SEVERITY_STATUS.get(severity.upper(), ("⚫", COLORS["blocked"]))
