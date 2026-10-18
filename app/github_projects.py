"""Offline-Projektverzeichnis für GitHub-Repositories mit offenen/erledigten Projekten."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4

from app.atomic_io import atomic_write_json

REPO_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/[A-Za-z0-9_.-]{1,100}$")
STATES = ("offen", "fertig")


def catalog_path(root: Path) -> Path:
    return root / "daten" / "github_projekte.json"


def _clean_record(raw: object) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("Ein Projekteintrag ist ungültig.")
    if set(raw) != {"id", "project", "repo", "url", "notes", "status", "todos"}:
        raise ValueError("Unbekannte oder fehlende Projektfelder.")
    project, repo, url, notes, status = (raw[key] for key in
                                         ("project", "repo", "url", "notes", "status"))
    if not all(isinstance(value, str) for value in (project, repo, url, notes, status)):
        raise ValueError("Projektfelder müssen Texte enthalten.")
    project, repo, url = project.strip(), repo.strip(), url.strip()
    if not 1 <= len(project) <= 120 or not REPO_RE.fullmatch(repo):
        raise ValueError("Projektname oder GitHub-Name ungültig. Erwartet: Eigentümer/Repository.")
    parts = urlsplit(url)
    segments = parts.path.strip("/").split("/")
    if (parts.scheme != "https" or parts.netloc.lower() != "github.com"
            or parts.username or parts.password or parts.query or parts.fragment
            or len(segments) != 2 or "/".join(segments).casefold() != repo.casefold()):
        raise ValueError("GitHub-URL muss https://github.com/Eigentümer/Repository entsprechen.")
    if len(notes) > 20000 or status not in STATES:
        raise ValueError("Notiz zu lang oder Projektstatus ungültig.")
    ident = raw["id"]
    if not isinstance(ident, str) or not re.fullmatch(r"[0-9a-f]{32}", ident):
        raise ValueError("Projekt-ID ungültig.")
    todos = raw["todos"]
    if not isinstance(todos, list) or len(todos) > 300:
        raise ValueError("Aufgabenliste ungültig.")
    cleaned = []
    seen = set()
    for item in todos:
        if not isinstance(item, dict) or set(item) != {"text", "done"}:
            raise ValueError("Aufgabe ungültig.")
        text, done = item["text"], item["done"]
        if not isinstance(text, str) or not 1 <= len(text.strip()) <= 300 or type(done) is not bool:
            raise ValueError("Aufgabe muss Text und Erledigt-Zustand enthalten.")
        text = text.strip()
        if text.casefold() in seen:
            raise ValueError("Doppelte Aufgabe im Projekt.")
        seen.add(text.casefold())
        cleaned.append({"text": text, "done": done})
    return {"id": ident, "project": project, "repo": repo,
            "url": f"https://github.com/{repo}", "notes": notes,
            "status": status, "todos": cleaned}


def _validate(rows: object) -> list[dict]:
    if not isinstance(rows, list) or len(rows) > 2000:
        raise ValueError("Ungültige Projektliste.")
    result, ids, projects, repos = [], set(), set(), set()
    for row in rows:
        item = _clean_record(row)
        if item["id"] in ids or item["project"].casefold() in projects or item["repo"].casefold() in repos:
            raise ValueError("Doppeltes Projekt, Repository oder Projekt-ID.")
        ids.add(item["id"])
        projects.add(item["project"].casefold())
        repos.add(item["repo"].casefold())
        result.append(item)
    return result


def load_projects(root: Path) -> list[dict]:
    path = catalog_path(root)
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema") != 1:
        raise ValueError("Die GitHub-Projektdatei ist beschädigt.")
    return _validate(raw.get("projects"))


def save_projects(root: Path, rows: list[dict]) -> Path:
    validated = _validate(rows)
    return atomic_write_json(catalog_path(root), {"schema": 1, "projects": validated})


def upsert_project(root: Path, *, ident: str | None = None, project: str,
                   repo: str, url: str, notes: str = "", status: str = "offen",
                   todos: list[dict] | None = None) -> dict:
    entries = load_projects(root)
    old = next((r for r in entries if r["id"] == ident), None) if ident else None
    candidate = _clean_record({
        "id": old["id"] if old else uuid4().hex, "project": project, "repo": repo,
        "url": url, "notes": notes, "status": status,
        "todos": todos if todos is not None else (old["todos"] if old else []),
    })
    entries = [r for r in entries if r["id"] != candidate["id"]]
    save_projects(root, entries + [candidate])
    return candidate


def delete_project(root: Path, ident: str) -> None:
    entries = load_projects(root)
    remaining = [r for r in entries if r["id"] != ident]
    if len(entries) == len(remaining):
        raise ValueError("Das Projekt wurde nicht gefunden.")
    save_projects(root, remaining)


def export_projects(root: Path, destination: Path) -> Path:
    if destination.suffix.lower() != ".json" or destination.resolve() == catalog_path(root).resolve():
        raise ValueError("Export muss eine andere .json-Datei sein.")
    return atomic_write_json(destination, {"schema": 1, "projects": load_projects(root)})


def import_projects(root: Path, source: Path) -> int:
    raw = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema") != 1:
        raise ValueError("Ungültiges Projekt-Importformat.")
    incoming = _validate(raw.get("projects"))
    existing = load_projects(root)
    existing_by_repo = {r["repo"].casefold(): r for r in existing}
    existing_by_project = {r["project"].casefold(): r for r in existing}
    existing_ids = {r["id"] for r in existing}
    merged = list(existing)
    for entry in incoming:
        match = existing_by_repo.get(entry["repo"].casefold())
        if match is not None:
            if (match["project"].casefold() == entry["project"].casefold()
                    and match["url"].casefold() == entry["url"].casefold()):
                continue  # bereits vorhanden, keine heimliche Überschreibung
            raise ValueError("Repository-Konflikt beim Import. Nichts wurde übernommen.")
        if entry["project"].casefold() in existing_by_project:
            raise ValueError("Projektname bereits vergeben. Nichts wurde übernommen.")
        if entry["id"] in existing_ids:
            raise ValueError("Projekt-ID bereits vergeben. Nichts wurde übernommen.")
        merged.append(entry)
        existing_by_repo[entry["repo"].casefold()] = entry
        existing_by_project[entry["project"].casefold()] = entry
        existing_ids.add(entry["id"])
    if len(merged) != len(existing):
        save_projects(root, merged)
    return len(merged) - len(existing)
