"""Referenznahes Multimodul-Dashboard mit ausgelagerter Recovery-Zentrale."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Callable

from app.event_log import EventLogger
from app.quick_note import append_developer_info
from app.recovery_center import RecoveryCenter
from app.recovery_ui import ZOOM_LEVELS
from app.song_document import list_songs, load_song
from app.song_editor import SongEditor
from app.song_library import SongLibrary
from app.texts import TextRegistry
from app.ui_standards import COLORS, SPACING, configure_global_style


class Dashboard:
    """Kompaktes Dashboard nach dem Provoware-Referenzentwurf."""

    def __init__(self, root: tk.Tk, texts: TextRegistry, logger: EventLogger,
                 project_root: Path | None = None) -> None:
        self.root, self.texts, self.logger = root, texts, logger
        self.project_root = project_root or Path.cwd()
        self.zoom_percent = 100
        self._song_editors: list[SongEditor] = []
        self._song_library: SongLibrary | None = None
        self._recovery_center: RecoveryCenter | None = None
        self.quick_info_var = tk.StringVar()
        self.quick_status_var = tk.StringVar(value="Bereit.")
        self.search_var = tk.StringVar()
        self.nav_collapsed = False

        root.title("Provoware-Datenbank-Dashboard 2026")
        root.geometry("1280x790")
        root.minsize(1020, 650)
        configure_global_style(root, self.zoom_percent)
        self._build_content()
        self._bind_keyboard()
        root.protocol("WM_DELETE_WINDOW", self.logout)
        self.refresh()
        self.search_entry.focus_set()

    def _build_content(self) -> None:
        shell = ttk.Frame(self.root)
        shell.pack(fill="both", expand=True)

        self._build_header(shell)
        self._build_tiles(shell)

        body = ttk.Frame(shell)
        body.pack(fill="both", expand=True, padx=SPACING["s"], pady=(0, SPACING["s"]))
        self.sidebar = ttk.Frame(body, style="Sidebar.TFrame", width=210)
        self.sidebar.pack(side="left", fill="y", padx=(0, SPACING["s"]))
        self.sidebar.pack_propagate(False)
        self._build_sidebar(self.sidebar)

        main = ttk.Frame(body)
        main.pack(side="left", fill="both", expand=True)
        self._build_quick_info(main)
        self._build_dashboard_grid(main)

        self._build_statusbar(shell)

    def _build_header(self, parent: ttk.Frame) -> None:
        header = ttk.Frame(parent, style="Toolbar.TFrame", padding=(SPACING["m"], SPACING["s"]))
        header.pack(fill="x", padx=SPACING["s"], pady=SPACING["s"])

        logo = tk.Label(header, text="▦", bg=COLORS["surface_soft"], fg=COLORS["accent"],
                        font=("TkDefaultFont", 22, "bold"), padx=8)
        logo.pack(side="left")
        title_box = ttk.Frame(header, style="Toolbar.TFrame")
        title_box.pack(side="left", fill="x", expand=True)
        tk.Label(title_box, text="Provoware-Datenbank-Dashboard 2026",
                 bg=COLORS["surface_soft"], fg=COLORS["text"],
                 font=("TkDefaultFont", 14, "bold")).pack(anchor="w")
        tk.Label(title_box, text="Linux · Python/Tkinter · Erweiterbares Multimodul-Dashboard",
                 bg=COLORS["surface_soft"], fg=COLORS["muted"],
                 font=("TkDefaultFont", 8)).pack(anchor="w")

        search_box = ttk.Frame(header, style="Toolbar.TFrame")
        search_box.pack(side="right")
        ttk.Label(search_box, text="⌕", style="Accent.TLabel").pack(side="left", padx=(0, SPACING["xs"]))
        self.search_entry = ttk.Entry(search_box, textvariable=self.search_var, width=24, takefocus=True)
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", lambda _event: self.open_song_library())
        ttk.Button(search_box, text="Recovery", command=self.open_recovery, takefocus=True).pack(side="left", padx=SPACING["s"])
        ttk.Button(search_box, text="Logout", command=self.logout, takefocus=True).pack(side="left")

    def _build_tiles(self, parent: ttk.Frame) -> None:
        strip = ttk.Frame(parent)
        strip.pack(fill="x", padx=SPACING["s"], pady=(0, SPACING["s"]))
        tiles = (
            ("♫\nSongtexte", self.open_song_library, True),
            ("▣\nHörspiele", lambda: self._planned("Hörspiele"), False),
            ("▤\nBlogartikel", lambda: self._planned("Blogartikel"), False),
            ("▥\nGenres", lambda: self._planned("Genres-Datenbank"), False),
            ("?\nPrompts", lambda: self._planned("Prompts"), False),
            ("⌕\nSuche", lambda: self._planned("Dateisuche"), False),
            ("≡\nDuplikate", lambda: self._planned("Duplikatprüfer"), False),
        )
        for text, command, enabled in tiles:
            button = ttk.Button(strip, text=text, command=command, style="Tile.TButton", takefocus=True)
            button.pack(side="left", fill="x", expand=True, padx=(0, SPACING["xs"]))
            if not enabled:
                button.configure(state="normal")

    def _build_sidebar(self, parent: ttk.Frame) -> None:
        top = ttk.Frame(parent, style="Sidebar.TFrame")
        top.pack(fill="x", padx=SPACING["s"], pady=(SPACING["s"], SPACING["m"]))
        ttk.Button(top, text="☰", command=self.toggle_sidebar, style="Nav.TButton", takefocus=True).pack(side="left")
        ttk.Label(top, text="Navigation", style="Sidebar.TLabel").pack(side="left", padx=SPACING["s"])

        self.nav_labels: list[ttk.Widget] = []
        self._nav_button(parent, "▦  Übersicht", None, active=True)
        self._nav_button(parent, "◈  Modulauswahl", lambda: self._planned("Modulauswahl"))
        self._nav_heading(parent, "Workflow Schreiben")
        self._nav_button(parent, "  ♫  Songtexte", self.open_song_library)
        self._nav_button(parent, "  ▣  Hörspiele", lambda: self._planned("Hörspiele"))
        self._nav_button(parent, "  ▤  Blogartikel", lambda: self._planned("Blogartikel"))
        self._nav_heading(parent, "DB-Eingaben")
        for label in ("Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten", "GitHub-Repositories", "Prompts"):
            self._nav_button(parent, f"  ·  {label}", lambda item=label: self._planned(item))
        self._nav_heading(parent, "Funktionen")
        self._nav_button(parent, "  ◉  Genreszufallsgenerator", lambda: self._planned("Genreszufallsgenerator"))
        self._nav_button(parent, "  ✎  Reimfinder", lambda: self._planned("Reimfinder"))
        self._nav_heading(parent, "Systemanwendungen")
        self._nav_button(parent, "  ⌕  Datenbank-Suche", lambda: self._planned("Datenbank-Suche"))
        self._nav_button(parent, "  ▤  Inhaltssuche Textdateien", lambda: self._planned("Inhaltssuche"))
        self._nav_button(parent, "  ≡  Trefferliste", lambda: self._planned("Trefferliste"))
        self._nav_button(parent, "  ◫  Duplikatprüfer", lambda: self._planned("Duplikatprüfer"))
        self._nav_heading(parent, "Werkzeug")
        self.recovery_nav_button = self._nav_button(parent, "  ⚕  Recovery", self.open_recovery)

    def _nav_heading(self, parent: ttk.Frame, text: str) -> None:
        label = ttk.Label(parent, text=f"⌄  {text}", style="Sidebar.TLabel")
        label.pack(fill="x", padx=SPACING["m"], pady=(SPACING["s"], SPACING["xs"]))
        self.nav_labels.append(label)

    def _nav_button(self, parent: ttk.Frame, text: str, command: Callable[[], None] | None,
                    active: bool = False) -> ttk.Button:
        button = ttk.Button(parent, text=text, command=command or (lambda: None),
                            style="ActiveNav.TButton" if active else "Nav.TButton", takefocus=True)
        button.pack(fill="x", padx=SPACING["s"], pady=1)
        self.nav_labels.append(button)
        return button

    def toggle_sidebar(self) -> None:
        self.nav_collapsed = not self.nav_collapsed
        self.sidebar.configure(width=58 if self.nav_collapsed else 210)
        for widget in self.nav_labels:
            if self.nav_collapsed:
                widget.pack_forget()
            else:
                widget.pack(fill="x", padx=SPACING["s"], pady=1)

    def _build_quick_info(self, parent: ttk.Frame) -> None:
        quick = ttk.Frame(parent, style="Toolbar.TFrame", padding=(SPACING["m"], SPACING["s"]))
        quick.pack(fill="x", pady=(0, SPACING["s"]))
        ttk.Label(quick, text="Entwicklerinfo:", style="Section.TLabel").pack(side="left")
        self.quick_entry = ttk.Entry(quick, textvariable=self.quick_info_var, takefocus=True)
        self.quick_entry.pack(side="left", fill="x", expand=True, padx=SPACING["s"])
        self.quick_entry.bind("<Return>", self._quick_save_enter)
        ttk.Button(quick, text="Speichern", command=self.save_quick_info, takefocus=True).pack(side="left")

    def _card(self, parent: tk.Misc, title: str) -> ttk.Frame:
        border = tk.Frame(parent, bg=COLORS["accent"], padx=1, pady=1)
        card = ttk.Frame(border, style="Card.TFrame", padding=SPACING["m"])
        card.pack(fill="both", expand=True)
        ttk.Label(card, text=title, style="Card.TLabel", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(0, SPACING["s"]))
        return border

    def _build_dashboard_grid(self, parent: ttk.Frame) -> None:
        grid = ttk.Frame(parent)
        grid.pack(fill="both", expand=True)
        grid.columnconfigure(0, weight=1, uniform="cards")
        grid.columnconfigure(1, weight=1, uniform="cards")
        grid.rowconfigure(0, weight=1, uniform="rows")
        grid.rowconfigure(1, weight=1, uniform="rows")

        workflow_border = self._card(grid, "🚀  Workflow Übersicht")
        workflow_border.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING["xs"]), pady=(0, SPACING["xs"]))
        workflow = workflow_border.winfo_children()[0]
        ttk.Label(workflow, text="Kreative Ideen.\nStrukturierte Workflows.\nStarke Ergebnisse.", style="Card.TLabel").pack(anchor="center", pady=SPACING["m"])
        for step in ("①  Idee erfassen", "②  DB-Eingaben ergänzen", "③  Funktionen nutzen", "④  Ergebnisse speichern"):
            ttk.Label(workflow, text=step, style="CardMuted.TLabel").pack(anchor="w", padx=SPACING["l"], pady=2)

        db_border = self._card(grid, "▦  DB-Eingaben")
        db_border.grid(row=0, column=1, sticky="nsew", padx=(SPACING["xs"], 0), pady=(0, SPACING["xs"]))
        db = db_border.winfo_children()[0]
        for label in ("Genres", "Stimmungen", "Stil", "Stimme", "Besonderheiten", "GitHub-Repositories", "Prompts"):
            row = ttk.Frame(db, style="Card.TFrame")
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=label, style="CardMuted.TLabel", width=20).pack(side="left")
            combo = ttk.Combobox(row, values=("Bitte auswählen …",), state="readonly", width=24)
            combo.set("Bitte auswählen …")
            combo.pack(side="left", fill="x", expand=True)

        functions_border = self._card(grid, "▣  Funktionen")
        functions_border.grid(row=1, column=0, sticky="nsew", padx=(0, SPACING["xs"]), pady=(SPACING["xs"], 0))
        functions = functions_border.winfo_children()[0]
        cards = ttk.Frame(functions, style="Card.TFrame")
        cards.pack(fill="both", expand=True)
        for title, subtitle, command in (
            ("◈\nGenreszufallsgenerator", "Zufällige Genres entdecken", lambda: self._planned("Genreszufallsgenerator")),
            ("✎\nReimfinder", "Passende Reime finden", lambda: self._planned("Reimfinder")),
        ):
            ttk.Button(cards, text=f"{title}\n{subtitle}", command=command, style="Tile.TButton", takefocus=True).pack(side="left", fill="both", expand=True, padx=SPACING["xs"], pady=SPACING["xs"])

        system_border = self._card(grid, "▤  Systemanwendungen")
        system_border.grid(row=1, column=1, sticky="nsew", padx=(SPACING["xs"], 0), pady=(SPACING["xs"], 0))
        system = system_border.winfo_children()[0]
        for icon, title, subtitle in (
            ("⌕", "Datenbank-Suche", "Nach Dateien im System suchen"),
            ("▤", "Inhaltssuche Textdateien", "Inhalte in Textdateien durchsuchen"),
            ("≡", "Trefferliste", "Suchergebnisse anzeigen"),
            ("◫", "Duplikatprüfer", "Doppelte Dateien finden"),
        ):
            row = ttk.Frame(system, style="Card.TFrame")
            row.pack(fill="x", pady=3)
            ttk.Label(row, text=icon, style="Card.TLabel", width=3).pack(side="left")
            text = ttk.Frame(row, style="Card.TFrame")
            text.pack(side="left", fill="x", expand=True)
            ttk.Label(text, text=title, style="Card.TLabel").pack(anchor="w")
            ttk.Label(text, text=subtitle, style="CardMuted.TLabel").pack(anchor="w")

    def _build_statusbar(self, parent: ttk.Frame) -> None:
        bar = ttk.Frame(parent, style="Status.TFrame", padding=(SPACING["m"], SPACING["xs"]))
        bar.pack(fill="x", padx=SPACING["s"], pady=(0, SPACING["s"]))
        tk.Label(bar, text="●", bg=COLORS["surface_soft"], fg=COLORS["green"]).pack(side="left")
        tk.Label(bar, textvariable=self.quick_status_var, bg=COLORS["surface_soft"], fg=COLORS["muted"]).pack(side="left", padx=SPACING["s"])
        tk.Label(bar, text="Python/Tkinter  ·  Dark Orange Industrial", bg=COLORS["surface_soft"], fg=COLORS["muted"]).pack(side="right")

    def _bind_keyboard(self) -> None:
        self.root.bind("<F5>", lambda _event: self.refresh())
        self.root.bind("<Control-plus>", lambda _event: self._step_zoom(1))
        self.root.bind("<Control-equal>", lambda _event: self._step_zoom(1))
        self.root.bind("<Control-minus>", lambda _event: self._step_zoom(-1))
        self.root.bind("<Control-0>", lambda _event: self.set_zoom(100))
        self.root.bind("<Control-r>", lambda _event: self.open_recovery())

    def _planned(self, name: str) -> None:
        messagebox.showinfo("Geplanter Bereich", f"{name} ist im Dashboard bereits vorgesehen, aber noch nicht als Fachfunktion freigegeben.", parent=self.root)

    def _quick_save_enter(self, _event: object = None) -> str:
        self.save_quick_info()
        return "break"

    def save_quick_info(self) -> None:
        try:
            target = append_developer_info(self.project_root, self.quick_info_var.get())
        except ValueError:
            self.quick_status_var.set("Bitte zuerst eine kurze Information eingeben.")
            return
        except Exception as error:
            self.quick_status_var.set(f"Speichern fehlgeschlagen: {type(error).__name__}")
            return
        self.quick_info_var.set("")
        self.quick_status_var.set(f"An {target.name} angehängt.")
        self.quick_entry.focus_set()

    def refresh_recent_songs(self) -> None:
        # Die Referenz-Hauptfläche bleibt stabil; vorhandene Songs werden über Bibliothek/Suche geöffnet.
        pass

    def open_song_editor(self) -> None:
        editor = SongEditor(self.root, self.project_root, self.zoom_percent, self._song_editor_closed, on_saved=self._song_saved)
        self._song_editors.append(editor)

    def open_song_path(self, path: Path) -> None:
        try:
            document = load_song(path)
        except Exception as error:
            messagebox.showerror("Song konnte nicht geöffnet werden", str(error), parent=self.root)
            return
        editor = SongEditor(self.root, self.project_root, self.zoom_percent, self._song_editor_closed, document=document, on_saved=self._song_saved)
        self._song_editors.append(editor)

    def open_song_library(self) -> None:
        if self._song_library is not None and self._song_library.window.winfo_exists():
            self._song_library.window.lift()
            self._song_library.refresh()
            return
        self._song_library = SongLibrary(self.root, self.project_root, self.zoom_percent, self.open_song_path)

    def open_recovery(self) -> None:
        if self._recovery_center is not None and self._recovery_center.window.winfo_exists():
            self._recovery_center.window.lift()
            self._recovery_center.refresh()
            return
        self._recovery_center = RecoveryCenter(self.root, self.texts, self.logger, self.zoom_percent)

    def _song_saved(self, _path: Path) -> None:
        if self._song_library is not None and self._song_library.window.winfo_exists():
            self._song_library.refresh()

    def _song_editor_closed(self, editor: SongEditor) -> None:
        if editor in self._song_editors:
            self._song_editors.remove(editor)

    def save_open_song_editors(self) -> bool:
        return all(editor.save(reason="Sitzung gespeichert") is not None for editor in list(self._song_editors))

    def logout(self) -> None:
        if not self.save_open_song_editors():
            messagebox.showerror("Logout gestoppt", "Mindestens ein Songtext konnte nicht gespeichert werden. Die Sitzung bleibt geöffnet.", parent=self.root)
            return
        for editor in list(self._song_editors):
            editor.close()
        self.root.destroy()

    def refresh(self) -> None:
        self.quick_status_var.set("Bereit.")
        if self._recovery_center is not None and self._recovery_center.window.winfo_exists():
            self._recovery_center.refresh()

    def _step_zoom(self, direction: int) -> None:
        current = ZOOM_LEVELS.index(self.zoom_percent)
        target = max(0, min(len(ZOOM_LEVELS) - 1, current + direction))
        self.set_zoom(ZOOM_LEVELS[target])

    def set_zoom(self, percent: int) -> None:
        if percent not in ZOOM_LEVELS:
            return
        self.zoom_percent = percent
        configure_global_style(self.root, percent)
        if self._recovery_center is not None and self._recovery_center.window.winfo_exists():
            self._recovery_center.set_zoom(percent)
        self.root.update_idletasks()


def install_exception_handler(root: tk.Tk, logger: EventLogger, refresh: Callable[[], None]) -> None:
    def report(_kind: type[BaseException], error: BaseException, _trace: object) -> None:
        try:
            event = logger.record(
                severity="FEHLER", area="OBERFLAECHE",
                summary="Eine Aktion wurde sicher abgebrochen.", cause=str(error) or "Unbekannter Programmfehler",
                protection="Die betroffene Aktion wurde beendet; andere Bereiche bleiben verfügbar.",
                next_step="Öffnen Sie Recovery und folgen Sie dem dort genannten Schritt.", exception=error,
            )
            refresh()
            messagebox.showerror("Aktion sicher beendet", f"{event['summary']}\n\n{event['next_step']}\n\nKennung: {event['event_id']}")
        except Exception as logging_error:
            messagebox.showerror("Sicherer Abbruch", f"Die Aktion wurde beendet. Das Protokoll konnte nicht geschrieben werden: {logging_error}")
    root.report_callback_exception = report
