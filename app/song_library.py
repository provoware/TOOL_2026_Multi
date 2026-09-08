"""Songbibliothek für vorhandene Arbeitsdateien und schreibgeschützte Versionsstände."""

from __future__ import annotations

import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import ttk
from typing import Callable

from app.song_document import list_songs, list_versions, load_song
from app.ui_standards import COLORS, SPACING, configure_global_style


class SongLibrary:
    def __init__(self, parent: tk.Misc, project_root: Path, zoom_percent: int,
                 open_song: Callable[[Path], None]) -> None:
        self.project_root = project_root
        self.open_song_callback = open_song
        self._paths: dict[str, Path] = {}
        self.window = tk.Toplevel(parent)
        self.window.title("Songbibliothek")
        self.window.geometry("900x600")
        self.window.minsize(720, 480)
        configure_global_style(self.window, zoom_percent)
        self._build()
        self.refresh()
        self.window.bind("<Escape>", lambda _event: self.window.destroy())

    def _build(self) -> None:
        outer = ttk.Frame(self.window, padding=SPACING["l"])
        outer.pack(fill="both", expand=True)
        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, SPACING["m"]))
        ttk.Label(header, text="Songbibliothek", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Aktualisieren", command=self.refresh).pack(side="right")

        columns = ("title", "genre", "modified", "versions")
        self.table = ttk.Treeview(outer, columns=columns, show="headings", selectmode="browse")
        for key, title, width in (
            ("title", "Titel", 330), ("genre", "Genre", 180),
            ("modified", "Zuletzt bearbeitet", 170), ("versions", "Versionen", 90),
        ):
            self.table.heading(key, text=title)
            self.table.column(key, width=width, stretch=key in {"title", "genre"})
        self.table.pack(fill="both", expand=True)
        self.table.bind("<Double-1>", lambda _event: self.open_selected())
        self.table.bind("<Return>", lambda _event: self.open_selected())

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(SPACING["m"], 0))
        ttk.Button(actions, text="Song öffnen", command=self.open_selected).pack(side="left")
        ttk.Button(actions, text="Versionsstände ansehen", command=self.show_versions).pack(side="left", padx=SPACING["s"])
        self.status = ttk.Label(actions, text="", style="Muted.TLabel")
        self.status.pack(side="right")

    def refresh(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        self._paths.clear()
        paths = list_songs(self.project_root)
        for path in paths:
            try:
                document = load_song(path)
                modified = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                versions = len(list_versions(self.project_root, document.title))
                item = self.table.insert("", "end", values=(document.title, document.genre, modified, versions))
                self._paths[item] = path
            except (OSError, UnicodeError, ValueError):
                continue
        if self.table.get_children():
            first = self.table.get_children()[0]
            self.table.selection_set(first)
            self.table.focus(first)
        self.status.config(text=f"{len(self._paths)} Song(s)")

    def selected_path(self) -> Path | None:
        selected = self.table.selection()
        return self._paths.get(selected[0]) if selected else None

    def open_selected(self) -> None:
        path = self.selected_path()
        if path is not None:
            self.open_song_callback(path)

    def show_versions(self) -> None:
        path = self.selected_path()
        if path is None:
            return
        document = load_song(path)
        versions = list_versions(self.project_root, document.title)
        window = tk.Toplevel(self.window)
        window.title(f"Versionsstände – {document.title}")
        window.geometry("760x520")
        body = ttk.Frame(window, padding=SPACING["l"])
        body.pack(fill="both", expand=True)
        ttk.Label(body, text=f"Versionsstände · {document.title}", style="Title.TLabel").pack(anchor="w")
        ttk.Label(body, text="Die Liste ist schreibgeschützt. Öffnen zeigt den damaligen Inhalt, ohne den aktuellen Song zu verändern.",
                  style="Muted.TLabel").pack(anchor="w", pady=(SPACING["s"], SPACING["m"]))
        listing = tk.Listbox(body, height=8, exportselection=False, bg=COLORS["surface"], fg=COLORS["text"], relief="flat")
        listing.pack(fill="x")
        for version in versions:
            listing.insert("end", version.stem)
        preview = tk.Text(body, wrap="word", state="disabled", bg=COLORS["surface"], fg=COLORS["text"], relief="flat", padx=10, pady=10)
        preview.pack(fill="both", expand=True, pady=(SPACING["m"], 0))

        def load_preview(_event: object = None) -> None:
            selection = listing.curselection()
            if not selection:
                return
            text = versions[int(selection[0])].read_text(encoding="utf-8")
            preview.config(state="normal")
            preview.delete("1.0", "end")
            preview.insert("1.0", text)
            preview.config(state="disabled")

        listing.bind("<<ListboxSelect>>", load_preview)
        if versions:
            listing.selection_set(0)
            load_preview()
        else:
            preview.config(state="normal")
            preview.insert("1.0", "Noch keine älteren Versionsstände vorhanden.")
            preview.config(state="disabled")
        window.bind("<Escape>", lambda _event: window.destroy())
