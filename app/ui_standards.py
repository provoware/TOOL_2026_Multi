"""Globale Oberflächenstandards für Farben, Abstände und Statusdarstellung."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

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
FONTS = {"body": ("TkDefaultFont", 11), "title": ("TkDefaultFont", 20, "bold")}

SEVERITY_STATUS = {
    "INFO": ("🟢", COLORS["green"]),
    "HINWEIS": ("🟢", COLORS["green"]),
    "WARNUNG": ("🟡", COLORS["yellow"]),
    "FEHLER": ("🔴", COLORS["red"]),
    "SCHWER": ("🔴", COLORS["red"]),
    "ABSTURZ": ("🔴", COLORS["red"]),
}


def configure_global_style(root: tk.Tk) -> ttk.Style:
    """Wendet einen einzigen, wiederverwendbaren Stil auf Standardbausteine an."""
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    root.configure(background=COLORS["background"])
    style.configure(".", font=FONTS["body"], background=COLORS["background"], foreground=COLORS["text"])
    style.configure("TFrame", background=COLORS["background"])
    style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"])
    style.configure("Title.TLabel", font=FONTS["title"], foreground=COLORS["text"])
    style.configure("Muted.TLabel", foreground=COLORS["muted"])
    style.configure("TButton", padding=(SPACING["m"], SPACING["s"]))
    style.map("TButton", foreground=[("disabled", COLORS["blocked"])])
    style.configure("Treeview", rowheight=30, background=COLORS["surface"], fieldbackground=COLORS["surface"],
                    foreground=COLORS["text"], borderwidth=0)
    style.configure("Treeview.Heading", background=COLORS["surface_alt"], foreground=COLORS["text"],
                    font=("TkDefaultFont", 10, "bold"))
    style.map("Treeview", background=[("selected", COLORS["surface_alt"])])
    return style


def severity_display(severity: str) -> tuple[str, str]:
    """Liefert Ampelsymbol und Textfarbe für einen Schweregrad."""
    return SEVERITY_STATUS.get(severity.upper(), ("⚫", COLORS["blocked"]))
