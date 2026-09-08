"""Laienfreundliche Recovery- und Debug-Oberfläche."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from app.event_log import EventLogger
from app.recovery_ui import ZOOM_LEVELS, available_areas, filter_events, repetition_summary, technical_details, zoom_font_size
from app.texts import TextRegistry
from app.ui_standards import COLORS, FONTS, SPACING, configure_global_style, severity_display


class Dashboard:
    def __init__(self, root: tk.Tk, texts: TextRegistry, logger: EventLogger) -> None:
        self.root, self.texts, self.logger = root, texts, logger
        self.zoom_percent = 100
        self._event_by_item: dict[str, dict] = {}
        self._all_events: list[dict] = []
        self.severity_var = tk.StringVar(value="ALLE")
        self.area_var = tk.StringVar(value="ALLE")
        self.zoom_var = tk.StringVar(value="100 %")
        root.title(texts.get("app.name", "TOOL_2026_Multi"))
        root.geometry("1060x680")
        root.minsize(820, 520)
        configure_global_style(root, self.zoom_percent)
        self._build_menu()
        self._build_content()
        self._bind_keyboard()
        self.refresh()
        self.severity_filter.focus_set()

    def _build_menu(self) -> None:
        menu = tk.Menu(self.root)
        debug = tk.Menu(menu, tearoff=False)
        debug.add_command(label="Ausgewähltes Ereignis öffnen", command=self.open_selected_event, accelerator="Enter")
        debug.add_command(label=self.texts.get("menu.debug.open", "Alle Debug/Log-Ereignisse öffnen"), command=self.show_log)
        debug.add_command(label=self.texts.get("menu.debug.refresh", "Anzeige aktualisieren"), command=self.refresh, accelerator="F5")
        menu.add_cascade(label=self.texts.get("menu.debug", "Debug/Log"), menu=debug)
        self.root.config(menu=menu)

    def _build_content(self) -> None:
        frame = ttk.Frame(self.root, padding=SPACING["xl"])
        frame.pack(fill="both", expand=True)
        self.main_frame = frame
        ttk.Label(frame, text="Debug- und Recovery-Zentrale", style="Title.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Fehler filtern, Details öffnen und Wiederholungen erkennen. Technische Angaben bleiben zunächst verborgen.",
                  style="Muted.TLabel", wraplength=920).pack(anchor="w", pady=(SPACING["s"], SPACING["m"]))

        self.ready = tk.Label(frame, text=f"🟢 {self.texts.get('status.ready', 'System bereit')}", anchor="w",
                              padx=12, pady=8, bg=COLORS["surface_alt"], fg=COLORS["green"],
                              font=("TkDefaultFont", FONTS["body_size"], "bold"))
        self.ready.pack(fill="x", pady=(0, SPACING["m"]))

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=(0, SPACING["m"]))
        ttk.Label(controls, text="Schweregrad:").pack(side="left")
        self.severity_filter = ttk.Combobox(controls, textvariable=self.severity_var, state="readonly", width=13,
                                            values=("ALLE", "INFO", "HINWEIS", "WARNUNG", "FEHLER", "KRITISCH", "SCHWER", "ABSTURZ"), takefocus=True)
        self.severity_filter.pack(side="left", padx=(SPACING["s"], SPACING["m"]))
        self.severity_filter.bind("<<ComboboxSelected>>", lambda _event: self._apply_filters())

        ttk.Label(controls, text="Bereich:").pack(side="left")
        self.area_filter = ttk.Combobox(controls, textvariable=self.area_var, state="readonly", width=18, takefocus=True)
        self.area_filter.pack(side="left", padx=(SPACING["s"], SPACING["m"]))
        self.area_filter.bind("<<ComboboxSelected>>", lambda _event: self._apply_filters())

        ttk.Label(controls, text="Anzeigegröße:").pack(side="left")
        self.zoom_filter = ttk.Combobox(controls, textvariable=self.zoom_var, state="readonly", width=8,
                                        values=tuple(f"{level} %" for level in ZOOM_LEVELS), takefocus=True)
        self.zoom_filter.pack(side="left", padx=(SPACING["s"], 0))
        self.zoom_filter.bind("<<ComboboxSelected>>", self._zoom_changed)

        columns = ("time", "severity", "area", "repeat", "summary")
        self.table = ttk.Treeview(frame, columns=columns, show="headings", height=10, takefocus=True, selectmode="browse")
        for key, title, width in (("time", "Zeit", 150), ("severity", "Ampel / Schwere", 135),
                                  ("area", "Bereich", 110), ("repeat", "Wiederholung", 110),
                                  ("summary", "Einfache Erklärung", 430)):
            self.table.heading(key, text=title)
            self.table.column(key, width=width, stretch=key == "summary")
        for severity in ("INFO", "HINWEIS", "WARNUNG", "FEHLER", "KRITISCH", "SCHWER", "ABSTURZ"):
            _, color = severity_display(severity)
            self.table.tag_configure(severity, foreground=color)
        self.table.pack(fill="both", expand=True)
        self.table.bind("<Double-1>", lambda _event: self.open_selected_event())
        self.table.bind("<Return>", lambda _event: self.open_selected_event())

        actions = ttk.Frame(frame)
        actions.pack(fill="x", pady=SPACING["m"])
        self.open_button = ttk.Button(actions, text="Ausgewähltes Ereignis öffnen", command=self.open_selected_event, takefocus=True)
        self.open_button.pack(side="left")
        ttk.Button(actions, text="Alle Ereignisse als Text", command=self.show_log, takefocus=True).pack(side="left", padx=SPACING["s"])
        ttk.Button(actions, text="Aktualisieren", command=self.refresh, takefocus=True).pack(side="left")
        self.status = ttk.Label(frame, text="", style="Muted.TLabel")
        self.status.pack(anchor="w", pady=(SPACING["s"], 0))

    def _bind_keyboard(self) -> None:
        self.root.bind("<F5>", lambda _event: self.refresh())
        self.root.bind("<Control-plus>", lambda _event: self._step_zoom(1))
        self.root.bind("<Control-equal>", lambda _event: self._step_zoom(1))
        self.root.bind("<Control-minus>", lambda _event: self._step_zoom(-1))
        self.root.bind("<Control-0>", lambda _event: self.set_zoom(100))

    def refresh(self) -> None:
        self._all_events = self.logger.recent(100)
        areas = available_areas(self._all_events)
        self.area_filter.configure(values=areas)
        if self.area_var.get() not in areas:
            self.area_var.set("ALLE")
        self._apply_filters()

    def _apply_filters(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        self._event_by_item.clear()
        events = filter_events(self._all_events, self.severity_var.get(), self.area_var.get())
        for event in events:
            severity = str(event.get("severity", "")).upper()
            lamp, _ = severity_display(severity)
            count, _first_seen = repetition_summary(event)
            repeat_text = f"{count}×" if count > 1 else "einmalig"
            item = self.table.insert("", "end", values=(str(event.get("time", ""))[:19].replace("T", " "),
                              f"{lamp} {severity}", event.get("area", ""), repeat_text, event.get("summary", "")), tags=(severity,))
            self._event_by_item[item] = event
        if events:
            first = self.table.get_children()[0]
            self.table.selection_set(first)
            self.table.focus(first)
        self.status.config(text=f"{len(events)} Ereignis(se) passen zum Filter · insgesamt {len(self._all_events)} geladen.")

    def selected_event(self) -> dict | None:
        selection = self.table.selection()
        return self._event_by_item.get(selection[0]) if selection else None

    def open_selected_event(self) -> None:
        event = self.selected_event()
        if event is None:
            messagebox.showinfo("Kein Ereignis ausgewählt", "Bitte zuerst eine Zeile auswählen.", parent=self.root)
            return
        self.show_event_details(event)

    def show_event_details(self, event: dict) -> None:
        window = tk.Toplevel(self.root)
        window.title("Ereignisdetails")
        window.geometry("760x610")
        window.minsize(640, 480)
        configure_global_style(window, self.zoom_percent)
        window.transient(self.root)
        body = ttk.Frame(window, padding=SPACING["l"])
        body.pack(fill="both", expand=True)
        severity = str(event.get("severity", "")).upper()
        lamp, _color = severity_display(severity)
        ttk.Label(body, text=f"{lamp} {severity} · {event.get('area', '')}", style="Title.TLabel").pack(anchor="w")
        ttk.Label(body, text=str(event.get("summary") or "Keine Erklärung vorhanden."), wraplength=690).pack(anchor="w", pady=(SPACING["m"], SPACING["l"]))

        count, first_seen = repetition_summary(event)
        facts = (
            ("Zeit", str(event.get("time") or "Unbekannt")[:19].replace("T", " ")),
            ("Wiederholungen", str(count)),
            ("Erstes Auftreten", first_seen[:19].replace("T", " ")),
            ("Schutz", str(event.get("safe_action") or "Keine Angabe")),
            ("Nächster Schritt", str(event.get("next_step") or "Keine Angabe")),
        )
        for title, value in facts:
            row = ttk.Frame(body)
            row.pack(fill="x", pady=SPACING["xs"])
            ttk.Label(row, text=f"{title}:", width=19).pack(side="left", anchor="n")
            ttk.Label(row, text=value, wraplength=520).pack(side="left", fill="x", expand=True)

        tech_frame = ttk.Frame(body)
        tech_text = tk.Text(tech_frame, height=9, wrap="word", padx=10, pady=10, bg=COLORS["surface"], fg=COLORS["text"],
                            insertbackground=COLORS["text"], relief="flat", takefocus=True)
        tech_text.insert("1.0", technical_details(event))
        tech_text.config(state="disabled")
        tech_text.pack(fill="both", expand=True)
        state = {"open": False}

        def toggle_technical() -> None:
            state["open"] = not state["open"]
            if state["open"]:
                tech_frame.pack(fill="both", expand=True, pady=(SPACING["m"], 0))
                toggle.config(text="Technische Details ausblenden")
            else:
                tech_frame.pack_forget()
                toggle.config(text="Technische Details anzeigen")

        toggle = ttk.Button(body, text="Technische Details anzeigen", command=toggle_technical, takefocus=True)
        toggle.pack(anchor="w", pady=(SPACING["l"], SPACING["s"]))
        close = ttk.Button(body, text="Schließen", command=window.destroy, takefocus=True)
        close.pack(anchor="e")
        window.bind("<Escape>", lambda _event: window.destroy())
        toggle.focus_set()

    def show_log(self) -> None:
        window = tk.Toplevel(self.root)
        window.title(self.texts.get("log.title", "Debug/Log – alle Ereignisse"))
        window.geometry("840x540")
        configure_global_style(window, self.zoom_percent)
        text = tk.Text(window, wrap="word", padx=16, pady=16, bg=COLORS["surface"], fg=COLORS["text"],
                       insertbackground=COLORS["text"], relief="flat", takefocus=True)
        text.pack(fill="both", expand=True)
        events = filter_events(self._all_events, self.severity_var.get(), self.area_var.get())
        content = "\n\n".join(self.logger.human_report(event) for event in events)
        text.insert("1.0", content or self.texts.get("dashboard.empty", "Keine passenden Ereignisse vorhanden."))
        text.config(state="disabled")
        window.bind("<Escape>", lambda _event: window.destroy())
        text.focus_set()

    def _zoom_changed(self, _event: object = None) -> None:
        self.set_zoom(int(self.zoom_var.get().split()[0]))

    def _step_zoom(self, direction: int) -> None:
        current = ZOOM_LEVELS.index(self.zoom_percent)
        target = max(0, min(len(ZOOM_LEVELS) - 1, current + direction))
        self.set_zoom(ZOOM_LEVELS[target])

    def set_zoom(self, percent: int) -> None:
        if percent not in ZOOM_LEVELS:
            return
        self.zoom_percent = percent
        self.zoom_var.set(f"{percent} %")
        configure_global_style(self.root, percent)
        self.ready.configure(font=("TkDefaultFont", zoom_font_size(FONTS["body_size"], percent), "bold"))
        self.root.update_idletasks()


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
