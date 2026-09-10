"""Atomarer Todo-Bestand mit aktivem Bereich und Archiv."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid4, uuid5

from app.atomic_io import atomic_write_json

SCHEMA_VERSION = 1

PROJECT_MODULE_BACKLOG: tuple[tuple[str, str], ...] = (
    ("01 · Charakterfibel", "Ziel: konsistente, detaillierte Charaktere zentral pflegen.\n☐ Datenmodell und atomare Speicherung\n☐ Such-/Bearbeitungsoberfläche\n☐ wiederverwendbare Charakter-IDs/API für andere Module\n☐ Rollen, Aussehen, Persönlichkeit, Motivation, Hintergrund, Beziehungen, Sprache, Stärken, Schwächen, Tags und Notizen\n☐ Zoom/Wayland/Recovery-Abnahme"),
    ("02 · Profil- & Accountmanager", "Ziel: Webseiten-/Profilzugänge strukturiert und schnell wiederfinden.\n☐ Webseite/URL, Profilname optional, verwendete E-Mail-Adresse, Passworthinweis und Sonstiges\n☐ frei ergänzbare eigene Felder\n☐ Gruppen, Suche und Filter\n☐ Passwörter selbst nicht unverschlüsselt speichern; Schutzkonzept vor Umsetzung festlegen\n☐ Import/Export, Backup, Restore und Datenschutzprüfung"),
    ("03 · Universeller Texteditor", "Ziel: allgemeiner, farblich unterstützter Editor.\n☐ Titel bestimmt sicheren Dateinamen\n☐ große Schreibfläche und abschließendes Notizenfeld\n☐ atomare Speicherung und Versionen\n☐ Zugriff auf Charakterfibel\n☐ einheitliche UI-/Zoom-/Wayland-Standards"),
    ("04 · Textfragment- und Ideenarchiv", "Ziel: unvollendete Verse, Sätze, Textstücke und Schlagworte wiederverwerten.\n☐ Fragmente einzeln oder gesammelt speichern\n☐ Tags, Herkunft und Suche\n☐ übersichtliche Karten-/Listenansicht\n☐ Drag-and-drop in einen seitlichen Kompositionsbereich\n☐ neue Texte aus mehreren Fragmenten zusammensetzen, ohne Originale zu löschen"),
    ("05 · Autonomes Updatemodul", "Ziel: Updates weitgehend automatisch, aber datensicher durchführen.\n☐ ZIP-Dateien prüfen und sicher entpacken\n☐ Manifest, Version und Integrität vor Änderung validieren\n☐ vollständiges Backup/Checkpoint vor Umsetzung\n☐ Update in Staging testen, erst danach aktivieren\n☐ automatischer Rollback bei Fehler\n☐ Rechte-/Bestätigungsdialog für riskante Änderungen; kein blindes Systemüberschreiben"),
    ("06 · Projektmodulbaukasten / Plugin-System", "Ziel: Projektstrukturen erstellen und dauerhaft erweiterbar halten.\n☐ standardisierte Projektvorlagen\n☐ Manifest für Module/Plugins\n☐ definierte Plugin-Schnittstellen statt Direktzugriff\n☐ Aktivieren/Deaktivieren ohne Kerncode zu beschädigen\n☐ Abhängigkeits-, Versions- und Kompatibilitätsprüfung\n☐ Test-/Stagingbereich für neue Module"),
    ("07 · Rechte Schnellstarter-Symbolleiste", "Ziel: schmale persistente Symbolleiste für häufige Webziele.\n☐ Starter hinzufügen/bearbeiten/entfernen\n☐ URL validieren\n☐ Name, Symbol und Gruppe speichern\n☐ Beispiele YouTube, Suno und eigene Seiten\n☐ Tastatur/Tooltip/Screenreader und sichere externe Browseröffnung"),
    ("08 · Wikimodul", "Ziel: mehrere getrennte Wissensbasen verwalten.\n☐ Wissensbasis anlegen/umbenennen\n☐ Artikel mit Titel, Text, Tags und Verknüpfungen\n☐ Volltextsuche und Querverweise\n☐ Import/Export in dokumentiertem Format\n☐ Versionen, Backup und Zugriff anderer Module"),
    ("09 · Arbeitsverzeichnis- und Entwicklungspool", "Ziel: häufige Projektordner dateimanagerartig persistent verwalten.\n☐ mehrere Arbeits-/Poolordner speichern und direkt öffnen\n☐ Status wie Entwicklung, Beta, stabil und archiviert\n☐ funktionierende Beta-/Release-Stände sicher ins Archiv duplizieren\n☐ niemals bestehende Archive überschreiben; eindeutige Namen/Versionen\n☐ organisieren, umbenennen und Metadaten bearbeiten\n☐ Vor-/Nachprüfung sowie nachvollziehbares Protokoll"),
)


def store_path(root: Path) -> Path:
    return root / "daten" / "todo" / "todo.json"


def empty_state() -> dict[str, object]:
    return {"schema_version": SCHEMA_VERSION, "active": [], "archive": []}


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _clean_text(value: object, *, required: bool = False, field: str = "Text") -> str:
    cleaned = " ".join(str(value or "").strip().split())
    if required and not cleaned:
        raise ValueError(f"{field} darf nicht leer sein.")
    return cleaned


def _validate_due(value: object) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as error:
        raise ValueError("Termin hat kein gültiges Datum/Zeit-Format.") from error
    if parsed.tzinfo is not None:
        raise ValueError("Todo-Termin muss lokale Datum/Zeit ohne Zeitzone enthalten.")
    return parsed.replace(second=0, microsecond=0).isoformat(timespec="minutes")


def _validate_task(raw: object, *, archived: bool) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("Todo-Eintrag ist beschädigt.")
    task_id = _clean_text(raw.get("id"), required=True, field="Todo-ID")
    title = _clean_text(raw.get("title"), required=True, field="Titel")
    note = str(raw.get("note") or "").strip()
    created_at = _clean_text(raw.get("created_at"), required=True, field="Erstellzeit")
    try:
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("Erstellzeit eines Todos ist beschädigt.") from error
    completed_at = raw.get("completed_at")
    if archived:
        completed_at = _clean_text(completed_at, required=True, field="Abschlusszeit")
        try:
            datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("Abschlusszeit eines Todos ist beschädigt.") from error
    else:
        completed_at = None
    return {
        "id": task_id,
        "title": title,
        "note": note,
        "due": _validate_due(raw.get("due")),
        "created_at": created_at,
        "completed_at": completed_at,
    }


def validate_state(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("Todo-Datei muss ein JSON-Objekt enthalten.")
    schema = raw.get("schema_version", SCHEMA_VERSION)
    if schema != SCHEMA_VERSION:
        raise ValueError(f"Unbekannte Todo-Datenversion: {schema}")
    active_raw = raw.get("active", [])
    archive_raw = raw.get("archive", [])
    if not isinstance(active_raw, list) or not isinstance(archive_raw, list):
        raise ValueError("Todo-Datei enthält ungültige Listen.")
    active = [_validate_task(item, archived=False) for item in active_raw]
    archive = [_validate_task(item, archived=True) for item in archive_raw]
    ids = [str(item["id"]) for item in [*active, *archive]]
    if len(ids) != len(set(ids)):
        raise ValueError("Todo-Datei enthält doppelte IDs.")
    return {"schema_version": SCHEMA_VERSION, "active": active, "archive": archive}


def load_state(root: Path) -> dict[str, object]:
    target = store_path(root)
    if not target.exists():
        return empty_state()
    return validate_state(json.loads(target.read_text(encoding="utf-8")))


def save_state(root: Path, state: dict[str, object]) -> Path:
    clean = validate_state(state)
    return atomic_write_json(store_path(root), clean)


def add_task(root: Path, title: str, note: str = "", due: str | None = None) -> dict[str, object]:
    state = load_state(root)
    task = {
        "id": uuid4().hex,
        "title": _clean_text(title, required=True, field="Titel"),
        "note": str(note or "").strip(),
        "due": _validate_due(due),
        "created_at": _now_utc(),
        "completed_at": None,
    }
    active = list(state["active"])
    active.append(task)
    state["active"] = active
    save_state(root, state)
    return deepcopy(task)


def complete_task(root: Path, task_id: str) -> dict[str, object]:
    state = load_state(root)
    active = list(state["active"])
    archive = list(state["archive"])
    for index, task in enumerate(active):
        if task["id"] == task_id:
            moved = dict(task)
            moved["completed_at"] = _now_utc()
            del active[index]
            archive.append(moved)
            state["active"] = active
            state["archive"] = archive
            save_state(root, state)
            return deepcopy(moved)
    raise ValueError("Aufgabe wurde nicht in den aktiven Todos gefunden.")


def ensure_project_module_backlog(root: Path) -> int:
    """Ergänzt die neun gewünschten Modulvorhaben genau einmal, ohne bestehende Todos anzutasten."""
    state = load_state(root)
    active = list(state["active"])
    archive = list(state["archive"])
    existing_titles = {str(item["title"]).casefold() for item in [*active, *archive]}
    existing_ids = {str(item["id"]) for item in [*active, *archive]}
    added = 0
    now = _now_utc()
    for title, note in PROJECT_MODULE_BACKLOG:
        task_id = uuid5(NAMESPACE_URL, f"provoware-projektmodul:{title}").hex
        if title.casefold() in existing_titles or task_id in existing_ids:
            continue
        active.append({
            "id": task_id, "title": title, "note": note, "due": None,
            "created_at": now, "completed_at": None,
        })
        existing_titles.add(title.casefold())
        existing_ids.add(task_id)
        added += 1
    if added:
        state["active"] = active
        save_state(root, state)
    return added


def active_tasks(root: Path) -> list[dict[str, object]]:
    tasks = list(load_state(root)["active"])
    return sorted(tasks, key=lambda item: (item["due"] is None, str(item["due"] or ""), str(item["title"]).casefold()))


def archived_tasks(root: Path) -> list[dict[str, object]]:
    tasks = list(load_state(root)["archive"])
    return sorted(tasks, key=lambda item: str(item["completed_at"] or ""), reverse=True)
