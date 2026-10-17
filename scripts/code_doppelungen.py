"""Zeigt identische Python-Anweisungsfolgen für eine gezielte Codeprüfung.

Nur lesend. Ein Treffer bedeutet nicht automatisch, dass Code entfernt werden soll.
"""
from __future__ import annotations

import argparse
import ast
import json
from collections import defaultdict
from pathlib import Path


def finde_doppelungen(ordner: Path, anweisungen: int = 4) -> list[dict]:
    if anweisungen < 2:
        raise ValueError("Mindestens zwei Anweisungen nötig")
    muster = defaultdict(list)
    for datei in sorted(ordner.glob("*.py")):
        baum = ast.parse(datei.read_text(encoding="utf-8"), filename=str(datei))
        for knoten in ast.walk(baum):
            if not isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef,
                                       ast.If, ast.For, ast.While, ast.Try, ast.With)):
                continue
            for art in ("body", "orelse", "finalbody"):
                teile = getattr(knoten, art, [])
                for i in range(max(0, len(teile) - anweisungen + 1)):
                    abschnitt = teile[i:i + anweisungen]
                    key = tuple(ast.dump(x, include_attributes=False) for x in abschnitt)
                    muster[key].append({
                        "datei": datei.name, "von": abschnitt[0].lineno,
                        "bis": abschnitt[-1].end_lineno,
                    })
    gefunden = [{"anzahl": len(orte), "stellen": orte}
                for orte in muster.values() if len(orte) > 1]
    return sorted(gefunden, key=lambda t: (
        -t["anzahl"], t["stellen"][0]["datei"], t["stellen"][0]["von"]))


def main() -> None:
    p = argparse.ArgumentParser(description="Mögliche Code-Doppelungen finden")
    p.add_argument("--ordner", type=Path, default=Path(__file__).resolve().parents[1] / "app")
    p.add_argument("--anweisungen", type=int, default=4)
    p.add_argument("--max-treffer", type=int, default=15)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    gefunden = finde_doppelungen(args.ordner, args.anweisungen)
    auswahl = gefunden[:max(0, args.max_treffer)]
    if args.json:
        print(json.dumps({"insgesamt": len(gefunden), "treffer": auswahl},
                         ensure_ascii=False, indent=2))
        return
    print(f"Mögliche gleiche Codefolgen: {len(gefunden)}")
    for nr, treffer in enumerate(auswahl, 1):
        stellen = ", ".join(f"{s['datei']}:{s['von']}-{s['bis']}"
                            for s in treffer["stellen"])
        print(f"{nr}. {treffer['anzahl']} Fundstellen: {stellen}")
    print("Hinweis: Diese Fundstellen vor jeder Vereinfachung fachlich prüfen.")


if __name__ == "__main__":
    main()
