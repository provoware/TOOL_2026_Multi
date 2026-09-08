"""Kleine, laienfreundliche Tkinter-Oberfläche."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from app.event_log import EventLogger
from app.texts import TextRegistry


class Dashboard:
    def __init__(self, root: tk.Tk, texts: TextRegistry, logger: EventLogger) -> None:
        self.root, self.texts, self.logger = root, texts, logger
        root.title(texts.get("app.name", "TOOL_2026_Multi"))
        root.geometry("900x560")
        root.minsize(700, 420)
        self._build_menu()
        self._build_content()
        self.refresh()

    def _build_menu(self) -> None:
        menu = tk.Menu(self.root)
        debug = tk.Menu(menu, tearoff=False)
        debug.add_command(label=self.texts.get("menu.debug.open", "Debug/Log öffnen"), command=self.show_log)
        debug.add_command(label=self.texts.get("menu.debug.refresh", "Anzeige aktualisieren"), command=self.refresh)
        menu.add_cascade(label=self.texts.get("menu.debug", "Debug/Log"), menu=debug)
        self.root.config(menu=menu)

    def _build_content(self) -> None:
        frame = ttk.Frame(self.root, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=self.texts.get("dashboard.title", "Übersicht"),
                  font=("TkDefaultFont", 18, "bold")).pack(anchor="w")
        ttk.Label(frame, text=self.texts.get("dashboard.help", "Hier sehen Sie die letzten fünf Ereignisse."),
                  wraplength=760).pack(anchor="w", pady=(6, 18))
        columns = ("time", "severity", "area", "summary")
        self.table = ttk.Treeview(frame, columns=columns, show="headings", height=5)
        for key, title, width in (("time", "Zeit", 160), ("severity", "Schwere", 90),
                                  ("area", "Bereich", 120), ("summary", "Einfache Erklärung", 430)):
            self.table.heading(key, text=title)
            self.table.column(key, width=width, stretch=key == "summary")
        self.table.pack(fill="x")
        ttk.Button(frame, text=self.texts.get("dashboard.open_log", "Debug/Log öffnen"),
                   command=self.show_log).pack(anchor="e", pady=14)
        self.status = ttk.Label(frame, text="")
        self.status.pack(anchor="w", pady=(12, 0))

    def refresh(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        events = self.logger.recent(5)
        for event in events:
            self.table.insert("", "end", values=(event["time"][:19].replace("T", " "),
                              event["severity"], event["area"], event["summary"]))
        self.status.config(text=self.texts.get("dashboard.empty", "Noch keine Ereignisse vorhanden.")
                           if not events else f"{len(events)} von höchstens 5 Ereignissen werden angezeigt.")

    def show_log(self) -> None:
        window = tk.Toplevel(self.root)
        window.title(self.texts.get("log.title", "Debug/Log – Ereignisdetails"))
        window.geometry("820x520")
        text = tk.Text(window, wrap="word", padx=16, pady=16)
        text.pack(fill="both", expand=True)
        events = self.logger.recent(100)
        content = "\n\n".join(self.logger.human_report(event) for event in events)
        text.insert("1.0", content or self.texts.get("dashboard.empty", "Noch keine Ereignisse vorhanden."))
        text.config(state="disabled")


def install_exception_handler(root: tk.Tk, logger: EventLogger, refresh: Callable[[], None]) -> None:
    def report(_kind: type[BaseException], error: BaseException, _trace: object) -> None:
        try:
            event = logger.record(severity="FEHLER", area="OBERFLAECHE",
                summary="Eine Aktion wurde sicher abgebrochen.", cause=str(error) or "Unbekannter Programmfehler",
                protection="Die betroffene Aktion wurde beendet; andere Bereiche bleiben verfügbar.",
                next_step="Öffnen Sie Debug/Log und folgen Sie dem dort genannten Schritt.", exception=error)
            refresh()
            messagebox.showerror("Aktion sicher beendet", f"{event['summary']}\n\n{event['next_step']}\n\nKennung: {event['event_id']}")
        except Exception as logging_error:
            messagebox.showerror("Sicherer Abbruch", f"Die Aktion wurde beendet. Das Protokoll konnte nicht geschrieben werden: {logging_error}")
    root.report_callback_exception = report
