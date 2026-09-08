"""Songbibliothek mit Suche, Filtern, Gruppierung und sicherer Versionswiederherstellung."""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Callable

from app.song_document import SONG_STATUSES, SongDocument, list_songs, list_versions, load_song, restore_version
from app.ui_standards import COLORS, SPACING, configure_global_style

FILTER_ALL = "Alle"
SORT_OPTIONS = ("Zuletzt bearbeitet", "Titel", "Genre", "Tags", "Status")
GROUP_OPTIONS = ("Keine", "Genre", "Tags", "Status")


@dataclass(frozen=True)
class SongRow:
    path: Path
    document: SongDocument
    modified: float
    versions: int


def _norm(value: str) -> str:
    return value.strip().casefold()


def song_matches(row: SongRow, search: str = "", *, genre: str = FILTER_ALL, mood: str = FILTER_ALL,
                 style: str = FILTER_ALL, voice: str = FILTER_ALL, tag: str = FILTER_ALL,
                 status: str = FILTER_ALL, favorites_only: bool = False) -> bool:
    document = row.document
    needle = _norm(search)
    searchable = " ".join((document.title, document.genre, document.mood, document.style,
                           document.voice, " ".join(document.tags))).casefold()
    if needle and needle not in searchable:
        return False
    fields = ((genre, document.genre), (mood, document.mood), (style, document.style),
              (voice, document.voice), (status, document.status))
    if any(selected != FILTER_ALL and _norm(selected) != _norm(actual) for selected, actual in fields):
        return False
    if tag != FILTER_ALL and _norm(tag) not in {_norm(item) for item in document.tags}:
        return False
    if favorites_only and not document.favorite:
        return False
    return True


def sort_rows(rows: list[SongRow], sort_by: str) -> list[SongRow]:
    if sort_by == "Titel":
        key, reverse = lambda row: _norm(row.document.title), False
    elif sort_by == "Genre":
        key, reverse = lambda row: (_norm(row.document.genre), _norm(row.document.title)), False
    elif sort_by == "Tags":
        key, reverse = lambda row: (_norm(", ".join(row.document.tags)), _norm(row.document.title)), False
    elif sort_by == "Status":
        order = {status: index for index, status in enumerate(SONG_STATUSES)}
        key, reverse = lambda row: (order.get(row.document.status, 99), _norm(row.document.title)), False
    else:
        key, reverse = lambda row: row.modified, True
    return sorted(rows, key=key, reverse=reverse)


def row_group(row: SongRow, group_by: str) -> str:
    if group_by == "Genre":
        return row.document.genre.strip() or "Ohne Genre"
    if group_by == "Tags":
        return ", ".join(row.document.tags) or "Ohne Tags"
    if group_by == "Status":
        return row.document.status or "Idee"
    return ""


class SongLibrary:
    def __init__(self, parent: tk.Misc, project_root: Path, zoom_percent: int,
                 open_song: Callable[[Path], None]) -> None:
        self.project_root = project_root
        self.open_song_callback = open_song
        self.zoom_percent = zoom_percent
        self._paths: dict[str, Path] = {}
        self._rows: list[SongRow] = []
        self.search_var = tk.StringVar()
        self.genre_var = tk.StringVar(value=FILTER_ALL)
        self.mood_var = tk.StringVar(value=FILTER_ALL)
        self.style_var = tk.StringVar(value=FILTER_ALL)
        self.voice_var = tk.StringVar(value=FILTER_ALL)
        self.tag_var = tk.StringVar(value=FILTER_ALL)
        self.status_var = tk.StringVar(value=FILTER_ALL)
        self.favorite_only_var = tk.BooleanVar(value=False)
        self.sort_var = tk.StringVar(value="Zuletzt bearbeitet")
        self.group_var = tk.StringVar(value="Keine")
        self.window = tk.Toplevel(parent)
        self.window.title("Songbibliothek")
        self.window.geometry("1180x720")
        self.window.minsize(920, 580)
        configure_global_style(self.window, zoom_percent)
        self._build()
        self.refresh()
        self.window.bind("<Escape>", lambda _event: self.window.destroy())
        self.window.bind("<F5>", lambda _event: self.refresh())

    def _build(self) -> None:
        outer = ttk.Frame(self.window, padding=SPACING["l"])
        outer.pack(fill="both", expand=True)
        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, SPACING["m"]))
        ttk.Label(header, text="Songbibliothek", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Aktualisieren", command=self.refresh, takefocus=True).pack(side="right")

        search_row = ttk.Frame(outer)
        search_row.pack(fill="x", pady=(0, SPACING["s"]))
        ttk.Label(search_row, text="Suche:").pack(side="left")
        self.search_entry = ttk.Entry(search_row, textvariable=self.search_var, takefocus=True)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=SPACING["s"])
        self.search_entry.bind("<KeyRelease>", lambda _event: self.apply_view())
        ttk.Label(search_row, text="Titel · Genre · Stimmung · Stil · Stimme · Tags", style="Muted.TLabel").pack(side="left")

        filters = ttk.LabelFrame(outer, text="Filter", padding=SPACING["s"])
        filters.pack(fill="x", pady=(0, SPACING["s"]))
        self.filter_boxes: dict[str, ttk.Combobox] = {}
        for index, (label, variable) in enumerate((
            ("Genre", self.genre_var), ("Stimmung", self.mood_var), ("Stil", self.style_var),
            ("Stimme", self.voice_var), ("Tags", self.tag_var), ("Status", self.status_var),
        )):
            ttk.Label(filters, text=f"{label}:").grid(row=0, column=index, sticky="w", padx=(0, SPACING["xs"]))
            box = ttk.Combobox(filters, textvariable=variable, values=(FILTER_ALL,), state="readonly", width=15, takefocus=True)
            box.grid(row=1, column=index, sticky="ew", padx=(0, SPACING["s"]))
            box.bind("<<ComboboxSelected>>", lambda _event: self.apply_view())
            filters.columnconfigure(index, weight=1)
            self.filter_boxes[label] = box
        self.favorite_check = ttk.Checkbutton(filters, text="★ Nur Favoriten", variable=self.favorite_only_var,
                                              command=self.apply_view, takefocus=True)
        self.favorite_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=(SPACING["s"], 0))
        ttk.Button(filters, text="Filter zurücksetzen", command=self.reset_filters, takefocus=True).grid(
            row=2, column=4, columnspan=2, sticky="e", pady=(SPACING["s"], 0))

        view = ttk.Frame(outer)
        view.pack(fill="x", pady=(0, SPACING["m"]))
        ttk.Label(view, text="Sortierung:").pack(side="left")
        sort_box = ttk.Combobox(view, textvariable=self.sort_var, values=SORT_OPTIONS, state="readonly", width=20, takefocus=True)
        sort_box.pack(side="left", padx=(SPACING["s"], SPACING["m"]))
        sort_box.bind("<<ComboboxSelected>>", lambda _event: self.apply_view())
        ttk.Label(view, text="Gruppierung:").pack(side="left")
        group_box = ttk.Combobox(view, textvariable=self.group_var, values=GROUP_OPTIONS, state="readonly", width=16, takefocus=True)
        group_box.pack(side="left", padx=SPACING["s"])
        group_box.bind("<<ComboboxSelected>>", lambda _event: self.apply_view())

        columns = ("favorite", "title", "genre", "mood", "status", "tags", "modified", "versions")
        self.table = ttk.Treeview(outer, columns=columns, show="tree headings", selectmode="browse", takefocus=True)
        self.table.heading("#0", text="Gruppe")
        self.table.column("#0", width=150, stretch=False)
        definitions = (
            ("favorite", "★", 42), ("title", "Titel", 235), ("genre", "Genre", 120),
            ("mood", "Stimmung", 120), ("status", "Status", 115), ("tags", "Tags", 190),
            ("modified", "Zuletzt bearbeitet", 145), ("versions", "Versionen", 75),
        )
        for key, title, width in definitions:
            self.table.heading(key, text=title)
            self.table.column(key, width=width, stretch=key in {"title", "tags"})
        self.table.pack(fill="both", expand=True)
        self.table.bind("<Double-1>", lambda _event: self.open_selected())
        self.table.bind("<Return>", lambda _event: self.open_selected())

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(SPACING["m"], 0))
        ttk.Button(actions, text="Song öffnen", command=self.open_selected, takefocus=True).pack(side="left")
        ttk.Button(actions, text="Versionsstände / Wiederherstellen", command=self.show_versions, takefocus=True).pack(
            side="left", padx=SPACING["s"])
        self.status_label = ttk.Label(actions, text="", style="Muted.TLabel")
        self.status_label.pack(side="right")

    @staticmethod
    def _values(rows: list[SongRow], attribute: str) -> tuple[str, ...]:
        found: set[str] = set()
        for row in rows:
            value = getattr(row.document, attribute)
            if isinstance(value, list):
                found.update(item.strip() for item in value if item.strip())
            elif str(value).strip():
                found.add(str(value).strip())
        return (FILTER_ALL, *sorted(found, key=str.casefold))

    def _update_filter_values(self) -> None:
        mapping = {
            "Genre": "genre", "Stimmung": "mood", "Stil": "style", "Stimme": "voice", "Tags": "tags"
        }
        for label, attribute in mapping.items():
            self.filter_boxes[label].configure(values=self._values(self._rows, attribute))
        self.filter_boxes["Status"].configure(values=(FILTER_ALL, *SONG_STATUSES))

    def refresh(self) -> None:
        rows: list[SongRow] = []
        for path in list_songs(self.project_root):
            try:
                document = load_song(path)
                rows.append(SongRow(path, document, path.stat().st_mtime,
                                    len(list_versions(self.project_root, document.title))))
            except (OSError, UnicodeError, ValueError):
                continue
        self._rows = rows
        self._update_filter_values()
        self.apply_view()

    def apply_view(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        self._paths.clear()
        rows = [row for row in self._rows if song_matches(
            row, self.search_var.get(), genre=self.genre_var.get(), mood=self.mood_var.get(),
            style=self.style_var.get(), voice=self.voice_var.get(), tag=self.tag_var.get(),
            status=self.status_var.get(), favorites_only=bool(self.favorite_only_var.get()))]
        rows = sort_rows(rows, self.sort_var.get())
        group_by = self.group_var.get()
        parents: dict[str, str] = {}
        for row in rows:
            parent = ""
            if group_by != "Keine":
                group = row_group(row, group_by)
                parent = parents.get(group, "")
                if not parent:
                    parent = self.table.insert("", "end", text=group, values=("", "", "", "", "", "", "", ""), open=True)
                    parents[group] = parent
            document = row.document
            modified = datetime.fromtimestamp(row.modified).strftime("%Y-%m-%d %H:%M")
            item = self.table.insert(parent, "end", values=(
                "★" if document.favorite else "", document.title, document.genre, document.mood,
                document.status, ", ".join(document.tags), modified, row.versions,
            ))
            self._paths[item] = row.path
        if self._paths:
            first = next(iter(self._paths))
            self.table.selection_set(first)
            self.table.focus(first)
        self.status_label.config(text=f"{len(rows)} von {len(self._rows)} Song(s)")

    def reset_filters(self) -> None:
        self.search_var.set("")
        for variable in (self.genre_var, self.mood_var, self.style_var, self.voice_var, self.tag_var, self.status_var):
            variable.set(FILTER_ALL)
        self.favorite_only_var.set(False)
        self.apply_view()
        self.search_entry.focus_set()

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
        window.geometry("820x600")
        window.minsize(680, 500)
        configure_global_style(window, self.zoom_percent)
        body = ttk.Frame(window, padding=SPACING["l"])
        body.pack(fill="both", expand=True)
        ttk.Label(body, text=f"Versionsstände · {document.title}", style="Title.TLabel").pack(anchor="w")
        ttk.Label(body, text="Erst Vorschau prüfen. Wiederherstellen sichert den aktuellen Stand automatisch als neue Version.",
                  style="Muted.TLabel", wraplength=760).pack(anchor="w", pady=(SPACING["s"], SPACING["m"]))
        listing = tk.Listbox(body, height=8, exportselection=False, bg=COLORS["surface"], fg=COLORS["text"], relief="flat")
        listing.pack(fill="x")
        for version in versions:
            listing.insert("end", version.stem)
        preview = tk.Text(body, wrap="word", state="disabled", bg=COLORS["surface"], fg=COLORS["text"],
                          relief="flat", padx=10, pady=10, takefocus=True)
        preview.pack(fill="both", expand=True, pady=(SPACING["m"], SPACING["s"]))
        result_var = tk.StringVar(value="")
        ttk.Label(body, textvariable=result_var, style="Muted.TLabel").pack(anchor="w")

        def selected_version() -> Path | None:
            selection = listing.curselection()
            return versions[int(selection[0])] if selection else None

        def load_preview(_event: object = None) -> None:
            version = selected_version()
            if version is None:
                return
            text = version.read_text(encoding="utf-8")
            preview.config(state="normal")
            preview.delete("1.0", "end")
            preview.insert("1.0", text)
            preview.config(state="disabled")

        def restore_selected() -> None:
            version = selected_version()
            if version is None:
                return
            try:
                _target, backup = restore_version(self.project_root, path, version)
            except Exception as error:
                result_var.set(f"🔴 Wiederherstellung fehlgeschlagen: {type(error).__name__}")
                messagebox.showerror("Nicht wiederhergestellt", str(error), parent=window)
                return
            if backup is None:
                result_var.set("🟡 Dieser Versionsstand entspricht bereits dem aktuellen Song.")
            else:
                result_var.set(f"🟢 Wiederhergestellt · vorheriger Stand gesichert als {backup.name}")
                self.refresh()

        listing.bind("<<ListboxSelect>>", load_preview)
        actions = ttk.Frame(body)
        actions.pack(fill="x", pady=(SPACING["s"], 0))
        self.restore_button = ttk.Button(actions, text="Diese Version wiederherstellen", command=restore_selected,
                                         takefocus=True, state="normal" if versions else "disabled")
        self.restore_button.pack(side="left")
        ttk.Button(actions, text="Schließen", command=window.destroy, takefocus=True).pack(side="right")
        if versions:
            listing.selection_set(0)
            load_preview()
        else:
            preview.config(state="normal")
            preview.insert("1.0", "Noch keine älteren Versionsstände vorhanden.")
            preview.config(state="disabled")
        window.bind("<Escape>", lambda _event: window.destroy())
