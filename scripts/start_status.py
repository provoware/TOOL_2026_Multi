#!/usr/bin/env python3
"""Grafische Startanzeige mit atomar gespeicherten Checkpoints und Konsolenfallback."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

STEPS = [
    "Python prüfen",
    "Umgebung vorbereiten",
    "Abhängigkeiten prüfen",
    "Projekt prüfen",
    "Anwendung starten",
]
COLORS = {
    "pending": "#9AA7BA",
    "running": "#FFD166",
    "ok": "#66D39A",
    "failed": "#FF6B7A",
}
SYMBOLS = {"pending": "⚫", "running": "🟡", "ok": "🟢", "failed": "🔴"}


def initial_state() -> dict:
    return {
        "schema_version": 1,
        "phase": "running",
        "progress": 0,
        "message": "Start wird vorbereitet …",
        "steps": [{"label": label, "status": "pending"} for label in STEPS],
    }


def read_state(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if data.get("schema_version") == 1 else initial_state()
    except (FileNotFoundError, json.JSONDecodeError, OSError, AttributeError):
        return initial_state()


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def set_step(path: Path, step_number: int, status: str, message: str) -> None:
    if not 1 <= step_number <= len(STEPS):
        raise ValueError("Ungültige Checkpoint-Nummer")
    if status not in COLORS:
        raise ValueError("Ungültiger Checkpoint-Status")
    state = read_state(path)
    state["steps"][step_number - 1]["status"] = status
    state["message"] = message
    completed = sum(item["status"] == "ok" for item in state["steps"])
    state["progress"] = int(completed * 100 / len(STEPS))
    if status == "failed":
        state["phase"] = "failed"
    write_state(path, state)


def finish(path: Path, message: str) -> None:
    state = read_state(path)
    for step in state["steps"]:
        if step["status"] != "failed":
            step["status"] = "ok"
    state.update({"phase": "done", "progress": 100, "message": message})
    write_state(path, state)


def gui(path: Path) -> int:
    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        return 0

    root = tk.Tk()
    root.title("TOOL_2026_Multi – sicherer Start")
    root.geometry("660x390")
    root.resizable(False, False)
    background, surface, text, muted = "#121722", "#1B2330", "#F4F7FB", "#B8C3D4"
    root.configure(bg=background)

    tk.Label(root, text="TOOL_2026_Multi", bg=background, fg=text,
             font=("TkDefaultFont", 19, "bold")).pack(anchor="w", padx=28, pady=(24, 4))
    tk.Label(root, text="Vollautomatischer Start · echte Checkpoints", bg=background, fg=muted,
             font=("TkDefaultFont", 10)).pack(anchor="w", padx=28, pady=(0, 18))

    card = tk.Frame(root, bg=surface, padx=18, pady=14)
    card.pack(fill="x", padx=28)
    labels = []
    for _ in STEPS:
        label = tk.Label(card, bg=surface, fg=muted, anchor="w", font=("TkDefaultFont", 11))
        label.pack(fill="x", pady=3)
        labels.append(label)

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    style.configure("Start.Horizontal.TProgressbar", troughcolor="#243044", background="#42D7C7", borderwidth=0)
    progress = ttk.Progressbar(root, style="Start.Horizontal.TProgressbar", maximum=100, length=604)
    progress.pack(padx=28, pady=(20, 8))
    message = tk.Label(root, bg=background, fg=text, anchor="w", font=("TkDefaultFont", 10))
    message.pack(fill="x", padx=28)

    def refresh() -> None:
        state = read_state(path)
        for index, item in enumerate(state["steps"]):
            status = item.get("status", "pending")
            labels[index].config(text=f"{SYMBOLS.get(status, '⚫')}  {item['label']}",
                                 fg=COLORS.get(status, muted))
        progress["value"] = state.get("progress", 0)
        message.config(text=state.get("message", ""))
        if state.get("phase") == "done":
            root.after(800, root.destroy)
            return
        if state.get("phase") == "failed":
            root.after(8000, root.destroy)
            return
        root.after(180, refresh)

    refresh()
    root.mainloop()
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Nutzung: start_status.py <init|set|finish|gui> <statusdatei> [...]", file=sys.stderr)
        return 2
    command, path = argv[1], Path(argv[2])
    if command == "init":
        write_state(path, initial_state())
    elif command == "set" and len(argv) >= 6:
        set_step(path, int(argv[3]), argv[4], " ".join(argv[5:]))
    elif command == "finish" and len(argv) >= 4:
        finish(path, " ".join(argv[3:]))
    elif command == "gui":
        return gui(path)
    else:
        print("Ungültiger Aufruf.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
