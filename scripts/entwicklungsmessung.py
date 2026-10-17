"""Misst GitHub-Prüfaufwand; offline mit --datei oder ausdrücklich online.

Es werden keine Nutzerdaten bearbeitet und keine zusätzlichen Pakete benötigt.
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import median
from urllib.request import Request, urlopen


def _datum(text: str | None) -> datetime | None:
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def auswerten(runs: list[dict], pr: dict | None = None,
             protokoll: str | None = None) -> dict:
    fertig = [r for r in runs if r.get("status") == "completed"]
    dauern = []
    for r in fertig:
        start, ende = _datum(r.get("run_started_at")), _datum(r.get("updated_at"))
        if start is not None and ende is not None and ende >= start:
            dauern.append((ende - start).total_seconds() / 60)
    revisonen = Counter(str(r["head_sha"]) for r in runs if r.get("head_sha"))
    ergebnis = {
        "laeufe": len(runs),
        "abgeschlossen": len(fertig),
        "erfolgreich": sum(r.get("conclusion") == "success" for r in fertig),
        "pr_laeufe": sum(r.get("event") == "pull_request" for r in runs),
        "push_laeufe": sum(r.get("event") == "push" for r in runs),
        "weitere_laeufe_gleicher_commits": sum(n - 1 for n in revisonen.values() if n > 1),
        "median_minuten_geschaetzt": round(median(dauern), 2) if dauern else None,
    }
    if pr is not None:
        ergebnis["aenderungsumfang"] = {
            "dateien": pr.get("changed_files"),
            "neue_zeilen": pr.get("additions"),
            "entfernte_zeilen": pr.get("deletions"),
        }
    if protokoll is not None:
        ergebnis["paket_zwischenspeicher"] = (
            "Treffer" if "Cache restored from key" in protokoll
            else "Neu angelegt" if "Cache saved with the key" in protokoll
            else "Nicht nachgewiesen"
        )
    return ergebnis


def _github(repo: str) -> list[dict]:
    teile = repo.split("/")
    if len(teile) != 2 or not all(teil and teil.replace("-", "").replace("_", "").isalnum()
                                  for teil in teile):
        raise ValueError("Repo im Format Eigentümer/Name angeben")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Provoware-Messung"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=100"
    with urlopen(Request(url, headers=headers), timeout=15) as response:
        return json.loads(response.read())["workflow_runs"]


def main() -> None:
    p = argparse.ArgumentParser(description="Aufwand der GitHub-Entwicklung messen")
    quelle = p.add_mutually_exclusive_group(required=True)
    quelle.add_argument("--datei", type=Path, help="gespeicherte GitHub-JSON, ganz ohne Internet")
    quelle.add_argument("--online", action="store_true", help="GitHub einmal abfragen")
    p.add_argument("--repo", default="provoware/TOOL_2026_Multi")
    p.add_argument("--pr-datei", type=Path, help="optional: gespeicherter GitHub-PR-Bericht")
    p.add_argument("--protokoll", type=Path, help="optional: bereits gespeichertes Prüfprotokoll")
    args = p.parse_args()
    daten = _github(args.repo) if args.online else json.loads(args.datei.read_text(encoding="utf-8"))
    laeufe = daten["workflow_runs"] if isinstance(daten, dict) else daten
    pr = json.loads(args.pr_datei.read_text(encoding="utf-8")) if args.pr_datei else None
    log = args.protokoll.read_text(encoding="utf-8") if args.protokoll else None
    print(json.dumps(auswerten(laeufe, pr, log), ensure_ascii=False, indent=2))
    print("Hinweis: Laufzeiten sind Näherungswerte. Doppelte Commits bedeuten")
    print("nicht zwangsläufig unnötige Prüfungen; sie müssen einzeln bewertet werden.")


if __name__ == "__main__":
    main()
