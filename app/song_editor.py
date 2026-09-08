"""Songtexteditor mit strukturierbaren Bereichen, Vorschau und Autosave."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Callable

from app.song_document import SECTION_TYPES, SongDocument, SongSection, save_song
from app.ui_standards import COLORS, SPACING, configure_global_style

AUTOSAVE_MS = 5 * 60 * 1000


class SongEditor:
    def __init__(self, parent: tk.Misc, project_root: Path, zoom_percent: int = 100,
                 on_closed: Callable[["SongEditor"], None] | None = None) -> None:
        self.project_root = project_root
        self.document = SongDocument(title="Unbenannter Song", sections=[SongSection("Strophe")])
        self.on_closed = on_closed
        self._closed = False
        self._autosave_job: str | None = None
        self._active_index: int | None = None
        self._loading_section = False
        self.window = tk.Toplevel(parent)
        self.window.title("Songtexteditor")
        self.window.geometry("1120x720")
        self.window.minsize(900, 580)
        configure_global_style(self.window, zoom_percent)
        self.title_var = tk.StringVar(value=self.document.title)
        self.genre_var = tk.StringVar()
        self.section_type_var = tk.StringVar(value="Strophe")
        self.status_var = tk.StringVar(value="Bereit · Autosave alle 5 Minuten")
        self._build()
        self._load_section(0)
        self._update_preview()
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.bind("<Control-s>", lambda _event: self.save())
        self.window.bind("<Escape>", lambda _event: self.close())
        self._schedule_autosave()
        self.title_entry.focus_set()

    def _build(self) -> None:
        outer = ttk.Frame(self.window, padding=SPACING["l"])
        outer.pack(fill="both", expand=True)
        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, SPACING["m"]))
        ttk.Label(header, text="Songtexteditor", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Speichern", command=self.save).pack(side="right")

        meta = ttk.Frame(outer)
        meta.pack(fill="x", pady=(0, SPACING["m"]))
        ttk.Label(meta, text="Titel:").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(meta, textvariable=self.title_var, width=42)
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=(SPACING["s"], SPACING["l"]))
        ttk.Label(meta, text="Genre (optional):").grid(row=0, column=2, sticky="w")
        self.genre_entry = ttk.Entry(meta, textvariable=self.genre_var, width=28)
        self.genre_entry.grid(row=0, column=3, sticky="ew", padx=(SPACING["s"], 0))
        meta.columnconfigure(1, weight=2)
        meta.columnconfigure(3, weight=1)
        for widget in (self.title_entry, self.genre_entry):
            widget.bind("<FocusOut>", lambda _event: self.save())
            widget.bind("<KeyRelease>", lambda _event: self._update_preview())

        content = ttk.Panedwindow(outer, orient="horizontal")
        content.pack(fill="both", expand=True)
        left = ttk.Frame(content, padding=SPACING["s"])
        right = ttk.Frame(content, padding=SPACING["s"])
        content.add(left, weight=3)
        content.add(right, weight=2)

        section_bar = ttk.Frame(left)
        section_bar.pack(fill="x")
        ttk.Label(section_bar, text="Bereich:").pack(side="left")
        self.section_type = ttk.Combobox(section_bar, textvariable=self.section_type_var,
                                         values=SECTION_TYPES, state="readonly", width=16)
        self.section_type.pack(side="left", padx=SPACING["s"])
        ttk.Button(section_bar, text="Bereich hinzufügen", command=self.add_section).pack(side="left")
        ttk.Button(section_bar, text="Bereich entfernen", command=self.remove_section).pack(side="left", padx=SPACING["s"])

        body = ttk.Frame(left)
        body.pack(fill="both", expand=True, pady=(SPACING["m"], 0))
        self.section_list = tk.Listbox(body, width=24, exportselection=False, bg=COLORS["surface"], fg=COLORS["text"],
                                       selectbackground=COLORS["surface_alt"], relief="flat")
        self.section_list.pack(side="left", fill="y")
        self.section_list.bind("<<ListboxSelect>>", self._section_changed)
        self.section_text = tk.Text(body, wrap="word", undo=True, padx=12, pady=12, bg=COLORS["surface"], fg=COLORS["text"],
                                    insertbackground=COLORS["text"], relief="flat")
        self.section_text.pack(side="left", fill="both", expand=True, padx=(SPACING["s"], 0))
        self.section_text.bind("<FocusOut>", lambda _event: self.save())
        self.section_text.bind("<KeyRelease>", lambda _event: self._section_text_changed())

        ttk.Label(right, text="Vorschau", style="Title.TLabel").pack(anchor="w")
        self.preview = tk.Text(right, wrap="word", state="disabled", padx=12, pady=12, bg=COLORS["surface"], fg=COLORS["text"],
                               insertbackground=COLORS["text"], relief="flat")
        self.preview.pack(fill="both", expand=True, pady=(SPACING["s"], SPACING["m"]))
        ttk.Label(right, text="Sonstiges (optional):").pack(anchor="w")
        self.other_text = tk.Text(right, height=6, wrap="word", padx=10, pady=10, bg=COLORS["surface"], fg=COLORS["text"],
                                  insertbackground=COLORS["text"], relief="flat")
        self.other_text.pack(fill="x", pady=(SPACING["s"], 0))
        self.other_text.bind("<FocusOut>", lambda _event: self.save())
        self.other_text.bind("<KeyRelease>", lambda _event: self._update_preview())

        ttk.Label(outer, textvariable=self.status_var, style="Muted.TLabel").pack(anchor="w", pady=(SPACING["m"], 0))
        self._refresh_section_list()

    def _refresh_section_list(self) -> None:
        self.section_list.delete(0, "end")
        counters: dict[str, int] = {}
        for section in self.document.sections:
            counters[section.kind] = counters.get(section.kind, 0) + 1
            number = f" {counters[section.kind]}" if counters[section.kind] > 1 or section.kind == "Strophe" else ""
            self.section_list.insert("end", f"{section.kind}{number}")

    def _current_index(self) -> int | None:
        selection = self.section_list.curselection()
        return int(selection[0]) if selection else None

    def _store_current_section(self) -> None:
        index = self._active_index
        if index is not None and 0 <= index < len(self.document.sections):
            self.document.sections[index].text = self.section_text.get("1.0", "end-1c")

    def _load_section(self, index: int) -> None:
        if not self.document.sections:
            self._active_index = None
            self.section_text.delete("1.0", "end")
            return
        index = max(0, min(index, len(self.document.sections) - 1))
        self._loading_section = True
        try:
            self.section_list.selection_clear(0, "end")
            self.section_list.selection_set(index)
            self.section_list.activate(index)
            self.section_text.delete("1.0", "end")
            self.section_text.insert("1.0", self.document.sections[index].text)
            self._active_index = index
        finally:
            self._loading_section = False

    def _section_changed(self, _event: object = None) -> None:
        if self._loading_section:
            return
        index = self._current_index()
        if index is not None and index != self._active_index:
            self._store_current_section()
            self._load_section(index)
            self._update_preview()

    def _section_text_changed(self) -> None:
        self._store_current_section()
        self._update_preview()

    def add_section(self) -> None:
        self._store_current_section()
        self.document.sections.append(SongSection(self.section_type_var.get() or "Strophe"))
        self._refresh_section_list()
        self._load_section(len(self.document.sections) - 1)
        self._update_preview()
        self.section_text.focus_set()

    def remove_section(self) -> None:
        index = self._active_index
        if index is None:
            return
        self._store_current_section()
        del self.document.sections[index]
        if not self.document.sections:
            self.document.sections.append(SongSection("Strophe"))
        self._refresh_section_list()
        self._load_section(min(index, len(self.document.sections) - 1))
        self._update_preview()

    def _sync_document(self) -> None:
        self._store_current_section()
        self.document.title = self.title_var.get().strip() or "Unbenannter Song"
        self.document.genre = self.genre_var.get().strip()
        self.document.other = self.other_text.get("1.0", "end-1c")

    def _update_preview(self) -> None:
        self._sync_document()
        self.preview.config(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", self.document.render())
        self.preview.config(state="disabled")

    def save(self, *, reason: str = "gespeichert") -> Path | None:
        if self._closed:
            return None
        try:
            self._sync_document()
            target = save_song(self.project_root, self.document)
            self.status_var.set(f"🟢 {reason}: {target.name}")
            return target
        except Exception as error:
            self.status_var.set(f"🔴 Speichern fehlgeschlagen: {type(error).__name__}")
            messagebox.showerror("Songtext nicht gespeichert", str(error), parent=self.window)
            return None

    def _schedule_autosave(self) -> None:
        self._autosave_job = self.window.after(AUTOSAVE_MS, self._autosave)

    def _autosave(self) -> None:
        if self._closed:
            return
        self.save(reason="Autosave")
        self._schedule_autosave()

    def close(self) -> None:
        if self._closed:
            return
        if self.save(reason="beim Schließen gespeichert") is None:
            return
        self._closed = True
        if self._autosave_job is not None:
            try:
                self.window.after_cancel(self._autosave_job)
            except tk.TclError:
                pass
            self._autosave_job = None
        self.window.destroy()
        if self.on_closed is not None:
            self.on_closed(self)
