"""Globale Oberflächenstandards für Farben, Abstände, Zoom und Statusdarstellung."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from app.recovery_ui import zoom_font_size

# Referenz: Dark Orange Industrial – dunkle Flächen, feine Konturen, ein Akzent.
COLORS = {
    "background": "#08131F",
    "surface": "#0E1D2B",
    "surface_alt": "#14283A",
    "surface_soft": "#102332",
    "sidebar": "#0A1723",
    "text": "#F4F7FB",
    "muted": "#9AAEC2",
    "accent": "#FF9800",
    "accent_soft": "#6B4308",
    "cyan": "#16D8FF",
    "green": "#40E58C",
    "yellow": "#FFD166",
    "red": "#FF6B7A",
    "blocked": "#708396",
    "border": "#294157",
}

SPACING = {"xs": 4, "s": 7, "m": 10, "l": 16, "xl": 22}
FONTS = {"body_size": 10, "small_size": 9, "title_size": 18, "hero_size": 20}

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
    """Wendet die referenznahe, kompakte Oberflächenhierarchie zentral an."""
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    body = zoom_font_size(FONTS["body_size"], zoom_percent)
    small = zoom_font_size(FONTS["small_size"], zoom_percent)
    title = zoom_font_size(FONTS["title_size"], zoom_percent)
    hero = zoom_font_size(FONTS["hero_size"], zoom_percent)
    root.configure(background=COLORS["background"])

    style.configure(".", font=("TkDefaultFont", body), background=COLORS["background"], foreground=COLORS["text"])
    style.configure("TFrame", background=COLORS["background"])
    style.configure("Sidebar.TFrame", background=COLORS["sidebar"])
    style.configure("Card.TFrame", background=COLORS["surface"], relief="flat")
    style.configure("Toolbar.TFrame", background=COLORS["surface_soft"])
    style.configure("Status.TFrame", background=COLORS["surface_soft"])

    style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"])
    style.configure("Sidebar.TLabel", background=COLORS["sidebar"], foreground=COLORS["text"])
    style.configure("Card.TLabel", background=COLORS["surface"], foreground=COLORS["text"])
    style.configure("CardMuted.TLabel", background=COLORS["surface"], foreground=COLORS["muted"])
    style.configure("Title.TLabel", font=("TkDefaultFont", title, "bold"), foreground=COLORS["text"])
    style.configure("Hero.TLabel", font=("TkDefaultFont", hero, "bold"), foreground=COLORS["text"])
    style.configure("Section.TLabel", font=("TkDefaultFont", body, "bold"), foreground=COLORS["text"])
    style.configure("Muted.TLabel", foreground=COLORS["muted"])
    style.configure("Accent.TLabel", foreground=COLORS["accent"])

    style.configure("TButton", padding=(SPACING["m"], SPACING["s"]), background=COLORS["surface_alt"], foreground=COLORS["text"], borderwidth=1)
    style.map("TButton",
              background=[("active", COLORS["accent_soft"]), ("pressed", COLORS["accent_soft"])],
              foreground=[("disabled", COLORS["blocked"]), ("active", COLORS["text"])])
    style.configure("Nav.TButton", anchor="w", padding=(SPACING["m"], SPACING["s"]), background=COLORS["sidebar"], borderwidth=0)
    style.map("Nav.TButton", background=[("active", COLORS["surface_alt"]), ("pressed", COLORS["accent_soft"])])
    style.configure("ActiveNav.TButton", anchor="w", padding=(SPACING["m"], SPACING["s"]), background=COLORS["accent"], foreground="#08131F", borderwidth=0)
    style.map("ActiveNav.TButton", background=[("active", "#FFAA2B")], foreground=[("active", "#08131F")])
    style.configure("Tile.TButton", padding=(SPACING["m"], SPACING["m"]), background=COLORS["surface"], borderwidth=1)

    style.configure("TEntry", fieldbackground=COLORS["surface"], foreground=COLORS["text"], insertcolor=COLORS["text"], bordercolor=COLORS["border"])
    style.configure("TCombobox", padding=SPACING["xs"], fieldbackground=COLORS["surface"], foreground=COLORS["text"])
    style.map("TCombobox", fieldbackground=[("readonly", COLORS["surface"])], foreground=[("readonly", COLORS["text"])])

    style.configure("Treeview", font=("TkDefaultFont", body), rowheight=zoom_font_size(28, zoom_percent),
                    background=COLORS["surface"], fieldbackground=COLORS["surface"],
                    foreground=COLORS["text"], borderwidth=0)
    style.configure("Treeview.Heading", background=COLORS["surface_alt"], foreground=COLORS["text"],
                    font=("TkDefaultFont", small, "bold"))
    style.map("Treeview", background=[("selected", COLORS["accent_soft"])])
    return style


def severity_display(severity: str) -> tuple[str, str]:
    """Liefert Ampelsymbol und Textfarbe für einen Schweregrad."""
    return SEVERITY_STATUS.get(severity.upper(), ("⚫", COLORS["blocked"]))
