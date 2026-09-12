from __future__ import annotations

import json
from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: erwartet 1 Treffer, gefunden {count}: {old[:90]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# MANIFEST: bestehende Dateiliste und bisherige Evidenz erhalten.
mp = Path("MANIFEST.json")
data = json.loads(mp.read_text(encoding="utf-8"))
data["schema_version"] = 30
data["tool"]["version"] = "0.17.2"
data["tool"]["date"] = "2026-09-12"
data["iteration"] = {
    "number": 37,
    "goal": "Entwicklungsprüfung automatisieren, Repository-Überreste blockieren und Hilfe & Fehlerhilfe durchsuchbar machen",
    "completed": 5,
    "open_next": 1,
}
v = data["validation"]
v.pop("iteration37_ci_result", None)
v.update({
    "iteration37_initial_ci_run": 764,
    "iteration37_initial_ci_result": "failure",
    "iteration37_initial_ci_cause": "Release-Invariant blockierte korrekt: app/help_content.py fehlte im Release-Manifest; Entwickler-Grundausstattung erkannte zusätzlich die fehlende Iteration-37-Dokumentation",
    "iteration37_technical_ci_run": 769,
    "iteration37_technical_ci_result": "success",
    "iteration37_technical_tested_head_sha": "7368488c601160506a7b95a057c3e340bef64e8f",
    "iteration37_logic_tests": 113,
    "iteration37_gui_tests": 77,
    "iteration37_release_files": 47,
    "iteration37_native_wayland_smoke": True,
    "iteration37_restore_gate": True,
    "iteration37_restore_status": "OK",
    "iteration37_restore_sha256": "000b03420cb2a7cddc4ce80885e27aa9f96bdf62aa43a571116f099c16fbb177",
    "iteration37_runtime_release_sha256": "993786558ce564dfbd5deee90ac9b7f1fe0067a321d5e12a7c0859f97cb6f28a",
    "iteration37_final_head_gate": "pending_after_version_sync",
})
mp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# README.
replace_once(
    "README.md",
    "> **Version:** 0.17.1 · **Stand:** 12.09.2026 · **Status:** ausführbarer Kern mit standardisiertem Charakterzugriff in Text- und Songeditor; automatische Voll-/Restore-, native Wayland- und ZIP-Artefakt-Prüfung aktiv, reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme noch offen",
    "> **Version:** 0.17.2 · **Stand:** 12.09.2026 · **Status:** ausführbarer Kern mit durchsuchbarer Hilfe, automatischer Testentdeckung und gehärteter Repository-Hygiene; Voll-/Restore-, native Wayland- und ZIP-Artefakt-Prüfung aktiv, reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme noch offen",
)
replace_once(
    "README.md",
    "- 🟢 **Fehlerhilfe (Recovery)** – einfache Erklärung, Schutzmaßnahme und nächster Schritt",
    "- 🟢 **Hilfe & Fehlerhilfe** – durchsuchbare Schritt-für-Schritt-Hilfe plus verständliche Fehlermeldungen, Schutzmaßnahme und nächster Schritt",
)
replace_once(
    "README.md",
    "während Songtexte, Vorgaben, Todo, Kalender, Fehlerhilfe, Zoom und Farbtheme erreichbar bleiben.",
    "während Songtexte, Vorgaben, Todo, Kalender, Hilfe & Fehlerhilfe, Zoom und Farbtheme erreichbar bleiben.",
)
rp = Path("README.md")
r = rp.read_text(encoding="utf-8")
marker = "## Neu in 0.17.1 – Charakterzugriff in Schreibmodulen\n"
if "## Neu in 0.17.2 – Wartbarkeit, Entwicklungseffizienz und Hilfe" not in r:
    section = """## Neu in 0.17.2 – Wartbarkeit, Entwicklungseffizienz und Hilfe

- **Hilfe & Fehlerhilfe:** F1 öffnet jetzt ein eigenes Hilfezentrum mit durchsuchbaren Alltagsthemen und einem getrennten Reiter für Fehlermeldungen.
- **Schnellere Entwicklung:** `bash scripts/pruefen.sh --quick` prüft Syntax, JSON, alle automatisch gefundenen Logiktests, Schreibfehlersimulation und Headless-Start ohne den langsameren GUI-/Release-Block.
- **Weniger Pflegeaufwand:** `--full` findet neue `tests/test_*.py` und `*_gui.py` automatisch; die freigegebenen Betriebsdateien kommen direkt aus `MANIFEST.json`. Neue Tests müssen nicht mehr in mehreren Shell-Listen nachgetragen werden.
- **Repo-Hygiene:** einmalige Migrations-/Finalisierungshilfen wie `scripts/_iter…`, `scripts/finalize_…` oder temporäre Finalizer-Workflows werden künftig automatisch als Überrest blockiert.
- **Bereinigung:** der nicht mehr benötigte Einmal-Helfer `scripts/_iter33_docs_apply.py` wurde entfernt.
- **Versionsdisziplin:** der vollständig grüne Main-Lauf #750 bleibt der unveränderte Referenzstand für 0.17.1/Iteration 36; diese Wartungsrunde wird getrennt als 0.17.2/Iteration 37 geführt.
- **Technischer Gate:** Grundprüfung #769 bestätigte 113 Logiktests, 77 GUI-Tests, 47 Release-Dateien, nativen Wayland-Start, Restore `OK` und ZIP-Erzeugung; der versionierte 0.17.2-Head wird vor Merge erneut vollständig geprüft.

"""
    if r.count(marker) != 1:
        raise SystemExit("README: 0.17.1-Marker fehlt/mehrfach")
    r = r.replace(marker, section + marker, 1)
start = r.index("## Fehlerhilfe\n")
end = r.index("\n## Anzeige und Zoom\n", start)
r = r[:start] + """## Hilfe & Fehlerhilfe

Öffnen über **Direkt nutzbar → Hilfe & Fehlerhilfe**, `F1` oder weiterhin `Strg+R`.

Der erste Reiter **Schnellhilfe** enthält durchsuchbare Themen wie Start, Songtexte, Texteditor/Charakterfibel, Daten, Fehler, Kubuntu/Wayland sowie Zoom/Tastatur. Jedes Thema nennt konkrete Schritte, eine Alternative und – wo nötig – einen Sicherheitshinweis.

Der zweite Reiter **Fehlermeldungen** behält die Recovery-Funktionen bei und zeigt zuerst:

- Was ist passiert?
- Was wurde geschützt?
- Was soll ich jetzt tun?
- Wie oft ist es passiert?

Technische Details bleiben zunächst ausgeblendet.
""" + r[end:]
r = r.replace("- `Strg+R` = Fehlerhilfe öffnen", "- `F1` = Hilfe & Fehlerhilfe öffnen\n- `Strg+R` = Hilfe & Fehlerhilfe öffnen", 1)
qstart = r.index("## Automatische Qualitätsprüfung\n")
qend = r.index("\nVollständiges Restore-Gate:", qstart)
qblock = """## Automatische Qualitätsprüfung

Für schnelle Entwicklungsrunden:

```bash
bash scripts/pruefen.sh --quick
```

`--quick` prüft Manifest-Dateien, Shell-/JSON-/Python-Syntax, **alle automatisch gefundenen Logik-/Regressionstests**, die Schreibfehlersimulation und den Headless-Start. So muss für kleine Änderungen nicht jedes Mal der deutlich langsamere GUI-/Release-Block laufen.

Vor Merge oder Release bleibt zwingend:

```bash
bash scripts/pruefen.sh --full
```

`--full` ergänzt automatisch **alle `*_gui.py`-Tests**, Release-Vollständigkeit und die komplette Entwicklerprüfung. Neue Testdateien werden über ihr Namensschema entdeckt; eine manuelle Testliste in `scripts/pruefen.sh` ist nicht mehr nötig. Die Runtime-Dateien stammen direkt aus `MANIFEST.json`, damit Manifest, Prüfung und Release nicht auseinanderlaufen.

Die Vollprüfung deckt unter anderem Fachlogik, Datensicherheit, Restore, Song-/Text-/Charakterfunktionen, Todo/Kalender, Hilfe & Fehlerhilfe, Zoom/Fokus, Themes/Kontraste, Navigation, Kubuntu-/Wayland-Erkennung, Release-Publish und Repository-Hygiene ab. Ein Hygiene-Rückfalltest blockiert zusätzlich bekannte lokale Artefakte und einmalige Entwicklungshelfer, bevor sie dauerhaft im Projekt bleiben.

**Referenz vor Iteration 37:** Main-Grundprüfung **#750** auf `d34e5fd643d086f6737eb42448a9a126a6bd3214` war vollständig grün: **111 Logik-/Regressionstests**, **76 GUI-Tests**, **46 Release-Betriebsdateien**, nativer Qt-Wayland-Start und Restore `OK`. Restore-SHA-256: `7b519b36dcb610c125a87d632bfe61ab05131b3c7e99912798f46071fe0804c2`.
"""
rp.write_text(r[:qstart] + qblock + r[qend:], encoding="utf-8")

# Laienanleitung.
replace_once("ANLEITUNG_LAIEN.md", "- **Fehlerhilfe (Recovery)**", "- **Hilfe & Fehlerhilfe**")
replace_once("ANLEITUNG_LAIEN.md", "- **Fehlerhilfe (Recovery)**", "- **Hilfe & Fehlerhilfe**")
ap = Path("ANLEITUNG_LAIEN.md")
a = ap.read_text(encoding="utf-8")
old = """# Fehlerhilfe (Recovery)

Öffnen über:

**Direkt nutzbar → Fehlerhilfe (Recovery)**

Die Fehlerhilfe zeigt zuerst einfache Informationen:

- **Was ist passiert?**
- **Was wurde geschützt?**
- **Was soll ich jetzt tun?**
- **Wie oft ist das passiert?**
"""
new = """# Hilfe & Fehlerhilfe

Öffnen über:

**Direkt nutzbar → Hilfe & Fehlerhilfe**, `F1` oder `Strg+R`.

Oben gibt es zwei Reiter:

1. **Schnellhilfe** – tippe ein einfaches Wort wie `speichern`, `Songtexte`, `Daten`, `Fehler` oder `Wayland` ein. Links wählst du ein Thema, rechts stehen die konkreten Schritte.
2. **Fehlermeldungen** – zeigt verständlich **Was ist passiert?**, **Was wurde geschützt?**, **Was soll ich jetzt tun?** und **Wie oft ist das passiert?**
"""
if a.count(old) != 1:
    raise SystemExit("ANLEITUNG: Hilfe-Block nicht eindeutig")
a = a.replace(old, new, 1)
a = a.replace("- `F5` – Liste / Fehlerhilfe aktualisieren", "- `F1` – Hilfe & Fehlerhilfe öffnen\n- `F5` – aktuelle Liste / Fehlermeldungen aktualisieren", 1)
a = a.replace("- `Strg+R` – Fehlerhilfe öffnen", "- `Strg+R` – Hilfe & Fehlerhilfe öffnen", 1)
tech_marker = "# Technische Prüfung für Entwickler\n"
if "bash scripts/pruefen.sh --quick" not in a:
    intro = """# Technische Prüfung für Entwickler

Für kleine Änderungen zuerst:

```bash
bash scripts/pruefen.sh --quick
```

Vor Merge/Release immer vollständig:

```bash
bash scripts/pruefen.sh --full
```

Neue Testdateien mit Namen `tests/test_*.py` beziehungsweise `*_gui.py` werden automatisch erkannt.

"""
    if a.count(tech_marker) != 1:
        raise SystemExit("ANLEITUNG: Entwickler-Marker fehlt")
    a = a.replace(tech_marker, intro, 1)
a = a.replace("- Fehlerhilfe,", "- Hilfe & Fehlerhilfe,", 1)
ap.write_text(a, encoding="utf-8")

# Changelog.
cp = Path("CHANGELOG.md")
c = cp.read_text(encoding="utf-8")
if "## 0.17.2 – 2026-09-12 – Wartbarkeit, Entwicklungseffizienz und Hilfe" not in c:
    insert = """## 0.17.2 – 2026-09-12 – Wartbarkeit, Entwicklungseffizienz und Hilfe

### Neu
- durchsuchbare **Hilfe & Fehlerhilfe** mit F1-Schnellzugriff, acht alltagsnahen Hilfethemen und getrenntem Fehlermeldungs-Reiter,
- `scripts/pruefen.sh --quick` als kurze Entwicklungsprüfung; `--full` bleibt verbindliches Merge-/Release-Gate,
- automatische Entdeckung aller Logik- und GUI-Testdateien anhand des Namensschemas.

### Geändert / bereinigt
- freigegebene Betriebsdateien werden in der Prüfung direkt aus `MANIFEST.json` gelesen statt in einer zweiten langen Shell-Liste gepflegt,
- zentrale UI-unabhängige Hilfetexte in `app/help_content.py`,
- Einmal-Helfer `scripts/_iter33_docs_apply.py` entfernt,
- Repo-Hygiene blockiert künftig bekannte Einmal-Patch-/Finalizer-Präfixe,
- README-Qualitätsabschnitt von veralteten Iterations-Einzelnachweisen auf den aktuellen Referenz-Gate und das zweistufige Prüfverfahren verdichtet.

### Schutz
- keine Nutzerdaten oder Speicherformate geändert,
- keine neue externe Laufzeitabhängigkeit,
- Recovery-Funktionalität bleibt vollständig erhalten, jetzt als zweiter Reiter innerhalb von Hilfe & Fehlerhilfe,
- Version 0.17.1 / Iteration 36 bleibt über Main-Grundprüfung #750 als unveränderte Referenzbasis dokumentiert.

### Technische Abnahme
- erster technischer PR-Gate **#764** blockierte korrekt: das neue Runtime-Modul `app/help_content.py` fehlte noch im Release-Manifest; zusätzlich wurde die noch fehlende Iteration-37-Dokumentation erkannt. Die 77 GUI-Tests waren bereits vollständig grün.
- korrigierter technischer Head `7368488c601160506a7b95a057c3e340bef64e8f` in Grundprüfung **#769** vollständig grün: **113 Logik-/Regressionstests**, **77 PySide6-GUI-Tests**, **47 Release-Betriebsdateien**, Headless-Start und nativer Qt-Wayland-Smoke erfolgreich.
- Vollprojekt-Restore `OK`, SHA-256 `000b03420cb2a7cddc4ce80885e27aa9f96bdf62aa43a571116f099c16fbb177`; Runtime-Release-SHA-256 `993786558ce564dfbd5deee90ac9b7f1fe0067a321d5e12a7c0859f97cb6f28a`.
- der vollständig auf **0.17.2 / Iteration 37** synchronisierte Freigabe-Head wird vor dem Merge erneut durch denselben Voll-Gate geprüft.

"""
    marker = "## 0.17.1 – 2026-09-12 – Charakterzugriff in Schreibmodulen und vollständige CI-ZIPs\n"
    if c.count(marker) != 1:
        raise SystemExit("CHANGELOG: 0.17.1-Marker fehlt")
    c = c.replace(marker, insert + marker, 1)
cp.write_text(c, encoding="utf-8")

# TODO.
tp = Path("TODO.md")
t = tp.read_text(encoding="utf-8")
if "## Iteration 37 – Wartbarkeit, Entwicklungseffizienz, Repo-Hygiene und Hilfe" not in t:
    block = """## Iteration 36 – Klick-&-Start-/Restore-Härtung

- 🟢 `kubuntu_abnahme.sh` direkt ausführbar (`0755`).
- 🟢 Restore erhält normale Unix-Ausführungsrechte und blockiert Symlink-/Sonderbit-Übernahme.
- 🟢 Main-Grundprüfung #750 auf `d34e5fd643d086f6737eb42448a9a126a6bd3214`: 111 Logiktests, 76 GUI-Tests, 46 Release-Dateien, Wayland und Restore `OK`.
- 🟡 reale sichtbare Kubuntu-26.04-/Plasma-Wayland-Abnahme bleibt separat offen.

## Iteration 37 – Wartbarkeit, Entwicklungseffizienz, Repo-Hygiene und Hilfe

- 🟢 `scripts/pruefen.sh` auf Manifest-basierte Dateiprüfung und automatische Testentdeckung umgestellt.
- 🟢 `--quick` als kurze Entwicklungsprüfung ergänzt; `--full` bleibt verbindliches Release-Gate.
- 🟢 `scripts/_iter33_docs_apply.py` als bestätigten Einmal-Überrest entfernt.
- 🟢 Hygiene-Test blockiert künftig Einmal-Patch-/Finalizer-Helfer.
- 🟢 Hilfe & Fehlerhilfe mit zentralen, durchsuchbaren Hilfethemen und F1-Zugriff umgesetzt; Recovery bleibt getrennt als Fehlermeldungs-Reiter erhalten.
- 🟢 technischer PR-Gate #769 vollständig grün: 113 Logiktests, 77 GUI-Tests, 47 Release-Dateien, nativer Wayland-Smoke, Restore `OK` und ZIP-Artefakte; finaler 0.17.2-Metadatenstand wird vor Merge erneut voll geprüft.

"""
    marker = "## Detaillierter Modul-Backlog zum Abhaken\n"
    if t.count(marker) != 1:
        raise SystemExit("TODO: Backlog-Marker fehlt")
    t = t.replace(marker, block + marker, 1)
tp.write_text(t, encoding="utf-8")

# Entwicklungsregeln.
ep = Path("docs/ENTWICKLUNGSREGELN.md")
e = ep.read_text(encoding="utf-8")
if "## Zweistufige Prüfung für schnellere Entwicklung" not in e:
    block = """## Zweistufige Prüfung für schnellere Entwicklung

- Nach kleinen Codeänderungen zuerst `bash scripts/pruefen.sh --quick`: Syntax, Manifest/JSON, automatisch erkannte Logiktests, Schreibfehler-Simulation und Headless-Start.
- `bash scripts/pruefen.sh --full` bleibt Pflicht vor PR-Merge, Release und nach Änderungen an GUI, Release, Restore oder CI.
- Neue `tests/test_*.py` und `tests/*_gui.py` werden automatisch entdeckt. Sie dürfen nicht zusätzlich in manuellen Shell-Testlisten gepflegt werden.
- Freigegebene Betriebsdateien werden aus `MANIFEST.json` gelesen; parallele manuelle Runtime-Dateilisten sind zu vermeiden.
- Einmalige Patch-/Finalisierungshilfen müssen sich entfernen oder dürfen gar nicht erst committed werden; der Hygiene-Test blockiert bekannte Einmal-Helfer-Präfixe.

"""
    marker = "## Nutzerbeteiligung minimieren\n"
    if e.count(marker) != 1:
        raise SystemExit("ENTWICKLUNGSREGELN: Marker fehlt")
    e = e.replace(marker, block + marker, 1)
ep.write_text(e, encoding="utf-8")

print("Iteration-37-Metadaten und Dokumentation erfolgreich synchronisiert.")
