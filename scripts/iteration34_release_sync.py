from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: erwartete genau 1 Fundstelle, gefunden {count}")
    return text.replace(old, new, 1)


# MANIFEST – maschinenlesbarer Projektstand.
manifest_path = ROOT / "MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["schema_version"] = max(int(manifest.get("schema_version", 0)), 27)
manifest["tool"]["version"] = "0.17.0"
manifest["tool"]["date"] = "2026-09-12"
manifest["iteration"] = {
    "number": 34,
    "goal": "Charakterfibel und Texteditor als nutzbare Module integrieren sowie Daten-, UI-, Import- und Startstandards vereinheitlichen",
    "completed": 8,
    "open_next": 1,
}
separation = manifest.setdefault("separation", {})
separation["character_data"] = "daten/charaktere/charaktere.json"
separation["text_editor_data"] = "daten/texte/"
validation = manifest.setdefault("validation", {})
validation.update({
    "iteration34_technical_ci_run": 685,
    "iteration34_technical_ci_result": "success",
    "iteration34_technical_logic_tests": 104,
    "iteration34_technical_gui_tests": 74,
    "iteration34_technical_release_files": 46,
    "iteration34_technical_native_wayland_smoke": True,
    "iteration34_technical_restore_gate": True,
    "iteration34_technical_restore_status": "OK",
    "iteration34_technical_restore_sha256": "1f1f46f35d5e733385c77e39c45366a812ce6b92f5a0786faaf948dbfddb4d41",
    "iteration34_technical_tested_head_sha": "8b5525541cff430f9e820a02adf44f469acc43a7",
    "iteration34_release_version": "0.17.0",
})
files = manifest.setdefault("files", [])
if not any(item.get("path") == "docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md" for item in files):
    files.append({
        "path": "docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md",
        "release": False,
        "purpose": "Charakterfibel, Texteditor, Daten-/UI-Standards, Backlog und CI-/Restore-Evidence",
    })
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# README – sichtbarer Stand und neue sofort nutzbare Funktionen.
text = read("README.md")
old_header = "> **Version:** 0.16.1 · **Stand:** 10.09.2026 · **Status:** ausführbarer Kern, automatische Voll-/Restore- und native Wayland-Prüfung aktiv, reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme noch offen"
new_header = "> **Version:** 0.17.0 · **Stand:** 12.09.2026 · **Status:** ausführbarer Kern mit Charakterfibel und Texteditor; automatische Voll-/Restore- und native Wayland-Prüfung aktiv, reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme noch offen"
text = replace_once(text, old_header, new_header, label="README-Version")
text = replace_once(
    text,
    "- 🟢 **Songtexte** – neue Songs schreiben, vorhandene Songs suchen, filtern, sortieren und öffnen\n",
    "- 🟢 **Songtexte** – neue Songs schreiben, vorhandene Songs suchen, filtern, sortieren und öffnen\n- 🟢 **Charakterfibel** – konsistente Figuren zentral speichern, suchen und für andere Schreibmodule referenzierbar halten\n- 🟢 **Texteditor** – allgemeine Texte mit Titel/Dateiname, Haupttext, Abschlussnotizen, Versionen und Charakterbezug bearbeiten\n",
    label="README-Direktmodule",
)
text = replace_once(
    text,
    "Die linke Navigation stellt diese fertigen Wege zuerst unter **Direkt nutzbar** bereit.",
    "Die linke Navigation stellt diese fertigen Wege – einschließlich **Texteditor** und **Charakterfibel** – zuerst unter **Direkt nutzbar** bereit.",
    label="README-Navigation",
)
iteration34_block = """## Neu in 0.17.0 – Charaktere, Texteditor und gemeinsame Standards\n\n- **Charakterfibel:** eigener atomarer Datenbestand mit stabilen Charakter-IDs und wiederverwendbaren Feldern für Schreibmodule.\n- **Texteditor:** eigener Arbeitsbereich mit sicherem Titel/Dateinamen, Haupttext, Abschlussnotizen, Versionierung und Charakterreferenzen.\n- **Genres & Vorgaben:** Komma-Eingaben wie `düster, treibend, melodisch` werden bereinigt und als einzelne Datenbankwerte gespeichert; Dubletten werden vermieden.\n- **Songtexte:** neben Standardbereichen können eigene validierte Bereichsnamen angelegt werden.\n- **JSON-Hilfe:** die Fehlerhilfe zeigt eine exakte Songtext-Importvorlage; zusätzlich liegt `vorlagen/songtext_import_vorlage.json` im Projekt.\n- **Startschutz:** fehlen benötigte Arbeitsordner, zeigt Provoware Ziel und Zweck und fragt vor dem Erstellen ausdrücklich nach Zustimmung; anschließend wird Schreibbarkeit validiert.\n- **Eingabekontrast:** Eingabe- und Auswahlfelder verwenden themeweit einen eigenen Kontrasthintergrund mit kontrastgeprüfter Schrift.\n- **Projektplanung:** neun größere Modulvorhaben wurden mit einzeln abhakbaren Unteraufgaben in den Todo-Bestand aufgenommen.\n\n"""
marker = "## Was ist noch geplant?\n"
if iteration34_block not in text:
    text = replace_once(text, marker, iteration34_block + marker, label="README-Iteration34")
text = replace_once(
    text,
    "3. Songbereich wählen oder hinzufügen.\n",
    "3. Standard-Songbereich wählen oder einen eigenen Bereichsnamen eingeben.\n",
    label="README-Songbereich",
)
text = replace_once(
    text,
    "Die eingebauten Startprofile werden beim bloßen Start nicht unnötig als Nutzerdatendatei geschrieben.\n",
    "Mehrere Werte können mit Komma eingegeben werden. Jeder bereinigte Begriff wird einzeln gespeichert; vorhandene Dubletten werden nicht erneut angelegt.\n\nDie eingebauten Startprofile werden beim bloßen Start nicht unnötig als Nutzerdatendatei geschrieben.\n",
    label="README-Profile",
)
text = replace_once(
    text,
    "Technische Details bleiben standardmäßig ausgeblendet.\n",
    "Technische Details bleiben standardmäßig ausgeblendet. Über **JSON-Importvorlage** lässt sich zusätzlich die exakte Struktur für extern vorbereitete Songtexte anzeigen und kopieren.\n",
    label="README-Hilfe",
)
text = replace_once(
    text,
    "- Profile, Todo und Kalender\n",
    "- Profile, Charakterfibel, Texteditor, Todo und Kalender\n- Komma-Eingaben, freie Songbereiche, JSON-Importstruktur und Startordner-Validierung\n",
    label="README-Tests",
)
text = replace_once(
    text,
    "- `docs/ITERATION29_PRESENTATION_POLICY.md` – Architekturhärtung, zentrale Präsentationspolicy und Release-Vollständigkeit\n",
    "- `docs/ITERATION29_PRESENTATION_POLICY.md` – Architekturhärtung, zentrale Präsentationspolicy und Release-Vollständigkeit\n- `docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md` – Charakterfibel, Texteditor, gemeinsame Daten-/UI-Standards und Abnahme\n",
    label="README-Doku",
)
write("README.md", text)


# Laienanleitung – neue Bedienwege konkret erklären.
text = read("ANLEITUNG_LAIEN.md")
text = replace_once(
    text,
    "- **Songtexte**\n- **Genres & Vorgaben**\n",
    "- **Songtexte**\n- **Charakterfibel**\n- **Texteditor**\n- **Genres & Vorgaben**\n",
    label="Anleitung-Direktmodule",
)
text = replace_once(
    text,
    "- **Songtexte**\n- **Genres & Vorgaben**\n- **Todo-Liste**\n",
    "- **Songtexte**\n- **Texteditor**\n- **Charakterfibel**\n- **Genres & Vorgaben**\n- **Todo-Liste**\n",
    label="Anleitung-Navigation",
)
text = replace_once(
    text,
    "Mögliche Bereiche sind zum Beispiel Strophe, Refrain, Intro, Bridge oder Outro.\n",
    "Mögliche Bereiche sind zum Beispiel Strophe, Refrain, Intro, Bridge oder Outro. Du kannst zusätzlich einen eigenen Namen eintippen, zum Beispiel **Pre-Drop** oder **Gesprochenes Outro**. Ungültige/leere Namen werden nicht übernommen.\n",
    label="Anleitung-Songbereiche",
)
text = replace_once(
    text,
    "4. Neuen Wert eingeben und **Wert hinzufügen** anklicken.\n",
    "4. Einen oder mehrere Werte eingeben und **Wert hinzufügen** anklicken. Mehrere Werte mit Komma trennen, zum Beispiel `düster, treibend, melodisch`. Jeder Begriff wird einzeln gespeichert; Dubletten werden übersprungen.\n",
    label="Anleitung-Kommawerte",
)
module_block = """---\n\n# Charakterfibel\n\nÖffnen über **Direkt nutzbar → Charakterfibel**. Hier pflegst du Figuren zentral, damit spätere Schreibmodule auf denselben Bestand zugreifen können. Gespeichert werden unter anderem Name, Rolle, Aussehen, Persönlichkeit, Motivation, Hintergrund, Beziehungen, Sprache, Stärken, Schwächen, Tags und Notizen. Jeder Charakter erhält intern eine stabile Kennung.\n\n---\n\n# Texteditor\n\nÖffnen über **Direkt nutzbar → Texteditor**. Der Titel bestimmt einen sicheren Dateinamen. Darunter liegen die große Schreibfläche und ein separates Abschlussnotizenfeld. Texte werden atomar gespeichert und können auf Charaktere aus der Charakterfibel verweisen. `Strg+S` speichert sofort.\n\n"""
marker = "# Aufgaben / Todo-Liste\n"
if module_block not in text:
    text = replace_once(text, marker, module_block + marker, label="Anleitung-Module")
text = replace_once(
    text,
    "Technische Details bleiben zunächst ausgeblendet und können bei Bedarf geöffnet werden.\n",
    "Technische Details bleiben zunächst ausgeblendet und können bei Bedarf geöffnet werden. Mit **JSON-Importvorlage** kannst du zusätzlich die exakte Struktur für extern vorbereitete Songtexte anzeigen und in die Zwischenablage kopieren. Dieselbe Vorlage liegt unter `vorlagen/songtext_import_vorlage.json`.\n",
    label="Anleitung-JSON",
)
startup_block = """\n## Wenn benötigte Arbeitsordner fehlen\n\nFehlt beim Start ein benötigter Tool-/Datenordner, legt Provoware ihn nicht still im Hintergrund an. Es zeigt den vorgesehenen Pfad und Zweck und fragt zuerst nach Zustimmung. Bei **Nein** wird nichts erstellt. Bei **Ja** wird der Ordner angelegt und anschließend auf Schreibbarkeit geprüft. Schlägt das fehl, bekommst du eine verständliche Fehlermeldung statt eines halbfertigen Starts.\n"""
marker = "---\n\n# Kubuntu 26.04 / Wayland prüfen\n"
if startup_block not in text:
    text = replace_once(text, marker, startup_block + "\n" + marker, label="Anleitung-Startordner")
write("ANLEITUNG_LAIEN.md", text)


# TODO.md – statischer Entwicklungsstand und detaillierter Backlog.
text = read("TODO.md")
text = replace_once(text, "Stand: 2026-09-10", "Stand: 2026-09-12", label="TODO-Datum")
iteration34 = """## Iteration 34 – Charakterfibel, Texteditor und gemeinsame Standards\n\n**Hauptziel:** Zwei produktiv nutzbare Module hinzufügen und gemeinsame Daten-/UI-/Import-/Startstandards vereinheitlichen.\n\n### Umsetzung\n\n- 🟢 Charakterfibel mit atomarem Datenbestand, stabilen IDs, Suche/Bearbeitung und wiederverwendbaren Charakterreferenzen.\n- 🟢 universeller Texteditor mit Titel→Dateiname, Haupttext, Abschlussnotizen, Versionierung, Autosave und Charakterbezug.\n- 🟢 Genres, Stimmungen, Stil, Stimme und Besonderheiten akzeptieren Komma-Listen und speichern jeden bereinigten Wert einzeln; Dubletten werden verhindert.\n- 🟢 Songtexteditor erlaubt eigene validierte Bereichsnamen zusätzlich zu den Standardbereichen.\n- 🟢 Hilfe enthält eine kopierbare exakte JSON-Importvorlage; zusätzliche Datei `vorlagen/songtext_import_vorlage.json`.\n- 🟢 Startvalidierung fragt vor dem Erstellen fehlender Arbeitsordner nach Zustimmung und prüft anschließend Schreibbarkeit.\n- 🟢 Eingabe-/Auswahlfelder erhalten zentral einen kontrastierenden Theme-Hintergrund mit kontrastgeprüfter Schrift.\n- 🟢 neue Module sind eigenständige Top-Level-Fenster und verwenden die vorhandenen Zoom-/Theme-/Accessibility-Standards.\n- 🟢 Projekt-Todo ergänzt die neun Modulvorhaben idempotent als 9 Hauptaufgaben plus 48 separat abhakbare Unteraufgaben.\n\n### Technische Abnahme vor Versionssync\n\n- 🟢 bereinigter Feature-Head `8b5525541cff430f9e820a02adf44f469acc43a7` in Grundprüfung **#685** vollständig erfolgreich.\n- 🟢 **104 Logik-/Regressionstests** und **74 PySide6-GUI-Tests** erfolgreich.\n- 🟢 **46 Release-Betriebsdateien**, Headless-Start und nativer Qt-Wayland-Smoke erfolgreich.\n- 🟢 Vollprojekt-Restore `OK`, SHA-256 `1f1f46f35d5e733385c77e39c45366a812ce6b92f5a0786faaf948dbfddb4d41`.\n- 🟡 finale v0.17.0-Versions-/Dokumentationssynchronisierung wird anschließend erneut vollständig geprüft.\n\n## Detaillierter Modul-Backlog zum Abhaken\n\n### 1. Charakterfibel\n- [x] atomarer Charakterdatenbestand und stabile IDs\n- [x] Such-/Bearbeitungsoberfläche\n- [x] Kernfelder für Rolle, Aussehen, Persönlichkeit, Motivation, Hintergrund, Beziehungen, Sprache, Stärken, Schwächen, Tags und Notizen\n- [x] Zugriffsmöglichkeit aus dem Texteditor\n- [ ] Zugriff aus weiteren Schreibmodulen standardisieren\n\n### 2. Profil- & Accountmanager\n- [ ] Webseite/URL, Profilname optional, verwendete E-Mail-Adresse, Passworthinweis und Sonstiges\n- [ ] frei ergänzbare Felder\n- [ ] Gruppen, Suche, Filter und Schnellwiederfinden\n- [ ] Schutzkonzept: keine Passwörter unverschlüsselt speichern\n- [ ] Import/Export, Backup, Restore und Datenschutzprüfung\n\n### 3. Universeller Texteditor\n- [x] Titel bestimmt sicheren Dateinamen\n- [x] große Schreibfläche und Abschlussnotizenfeld\n- [x] atomare Speicherung, Versionierung und Autosave\n- [x] Charakterfibel-Zugriff\n- [ ] farbliche Text-/Strukturhilfen weiter ausbauen\n\n### 4. Textfragment- und Ideenarchiv\n- [ ] einzelne oder mehrere Verse, Sätze, Fragmente und Schlagworte speichern\n- [ ] Tags, Herkunft und Volltextsuche\n- [ ] übersichtliche Karten-/Listenansicht\n- [ ] Drag-and-drop in einen seitlichen Kompositionsbereich\n- [ ] neue Texte aus Fragmenten erzeugen, ohne Originale zu löschen\n\n### 5. Autonomes Updatemodul\n- [ ] ZIP-Dateien sicher prüfen und entpacken\n- [ ] Manifest, Version, Prüfsummen und Integrität vor Änderung validieren\n- [ ] vollständigen Checkpoint/Backup vor jedem Update erzeugen\n- [ ] Update zuerst isoliert im Staging testen\n- [ ] automatisierte Tests vor Aktivierung erzwingen\n- [ ] atomare Aktivierung und Nachprüfung\n- [ ] automatischen Rollback bei Fehlern\n- [ ] Rechte-/Bestätigungsdialoge für riskante Änderungen; kein blindes Überschreiben\n\n### 6. Projektmodulbaukasten / Plugin-System\n- [ ] standardisierte Projektvorlagen\n- [ ] Modul-/Plugin-Manifest definieren\n- [ ] stabile Plugin-Schnittstellen statt Direktzugriff auf Kerninternas\n- [ ] Plugins aktivieren/deaktivieren, ohne Kerncode zu beschädigen\n- [ ] Abhängigkeits-, Versions- und Kompatibilitätsprüfung\n- [ ] Test-/Stagingbereich für neue Module\n\n### 7. Rechte Schnellstarter-Symbolleiste\n- [ ] schmale persistente rechte Symbolleiste\n- [ ] URL-Starter hinzufügen, bearbeiten und entfernen\n- [ ] URL validieren und sicher im Standardbrowser öffnen\n- [ ] Name, Symbol und Gruppe speichern\n- [ ] Beispiele für YouTube, Suno und eigene Seiten\n- [ ] Tastatur-, Tooltip- und Screenreader-Unterstützung\n\n### 8. Wikimodul\n- [ ] mehrere getrennte Wissensbasen\n- [ ] Artikel mit Titel, Text, Tags und Verknüpfungen\n- [ ] Volltextsuche und Querverweise\n- [ ] dokumentierter Import/Export\n- [ ] Versionierung, Backup und Zugriff anderer Module\n\n### 9. Arbeitsverzeichnis- und Entwicklungspool\n- [ ] mehrere Arbeits-/Poolordner persistent speichern und direkt öffnen\n- [ ] dateimanagerartige Übersicht\n- [ ] Status Entwicklung/Beta/stabil/archiviert\n- [ ] funktionierende Beta-/Release-Stände sicher ins Archiv duplizieren\n- [ ] niemals bestehende Archive überschreiben; eindeutige Namen/Versionen\n- [ ] organisieren, umbenennen und Metadaten bearbeiten\n- [ ] Vor-/Nachprüfung und nachvollziehbares Protokoll\n\n"""
marker = "## Danach\n"
if iteration34 not in text:
    text = replace_once(text, marker, iteration34 + marker, label="TODO-Iteration34")
write("TODO.md", text)


# CHANGELOG – v0.17.0 oben einfügen.
text = read("CHANGELOG.md")
entry = """## 0.17.0 – 2026-09-12 – Charakterfibel, Texteditor und gemeinsame Daten-/UI-Standards\n\n### Neu\n- Charakterfibel als eigenständiges Modul mit atomarem Datenbestand, stabilen Charakter-IDs, Suche/Bearbeitung und wiederverwendbaren Charakterreferenzen,\n- universeller Texteditor mit sicherem Titel/Dateinamen, Haupttext, Abschlussnotizen, Versionierung, Autosave und Charakterbezug,\n- frei benennbare, validierte Songtextbereiche zusätzlich zu den Standardbereichen,\n- exakte JSON-Songtext-Importvorlage in der Fehlerhilfe und als `vorlagen/songtext_import_vorlage.json`,\n- Startordner-Validierung mit ausdrücklicher Zustimmung vor dem Erstellen und anschließender Schreibbarkeitsprüfung.\n\n### Geändert\n- Genres, Stimmungen, Stil, Stimme und Besonderheiten zerlegen Komma-Eingaben in einzelne bereinigte Datenbankwerte und verhindern Dubletten,\n- Charakterfibel und Texteditor in Schnellkacheln, Navigation, Fensterregistry, Zoom/Theme und Accessibility integriert,\n- Eingabe- und Auswahlfelder erhalten zentral einen kontrastierenden Theme-Hintergrund mit kontrastgeprüfter Schrift,\n- Todo-Bestand wird idempotent um neun Projektmodule mit 48 separat abhakbaren Unteraufgaben ergänzt, ohne bestehende oder archivierte Aufgaben zu überschreiben.\n\n### Schutz und technische Abnahme\n- keine bestehenden Nutzerdaten gelöscht oder überschrieben,\n- neue Charakter-/Textdaten werden atomar gespeichert,\n- autonomes Updatemodul bewusst nur als Sicherheits-Backlog aufgenommen; kein blindes Selbstüberschreiben implementiert,\n- bereinigter Feature-Head `8b5525541cff430f9e820a02adf44f469acc43a7` in Grundprüfung **#685** vollständig grün: **104 Logiktests**, **74 GUI-Tests**, **46 Release-Dateien**, Headless-Start, nativer Qt-Wayland-Smoke und Restore `OK`,\n- Restore-SHA-256 `1f1f46f35d5e733385c77e39c45366a812ce6b92f5a0786faaf948dbfddb4d41`,\n- finale v0.17.0-Synchronisierung wird vor Merge erneut vollständig geprüft.\n\n"""
if entry not in text:
    text = replace_once(text, "# Änderungsverlauf\n\n", "# Änderungsverlauf\n\n" + entry, label="CHANGELOG-v017")
write("CHANGELOG.md", text)


# Iterationsdokument.
doc = """# Iteration 34 – Charakterfibel, Texteditor und gemeinsame Daten-/UI-Standards\n\n## Ziel\n\nZwei neue produktive Module bereitstellen und gleichzeitig wiederverwendbare Standards für Eingaben, Kontrast, Datenbanklisten, Importhilfe und Startordner etablieren.\n\n## Umgesetzt\n\n1. **Charakterfibel** mit atomarem JSON-Bestand, stabilen IDs, Such-/Bearbeitungsoberfläche und Feldern für konsistente Charaktere.\n2. **Texteditor** mit Titel→Dateiname, Haupttext, Abschlussnotizen, Versionierung/Autosave und Charakterreferenzen.\n3. **Komma-Normalisierung** für Genres, Stimmungen, Stil, Stimme und Besonderheiten: trimmen, leere Werte verwerfen, case-insensitive Dubletten vermeiden, einzeln speichern.\n4. **Eigene Songbereiche** zusätzlich zu Standardbereichen; Namen werden normalisiert und validiert.\n5. **JSON-Importhilfe** mit exakter Struktur und kopierbarer Vorlage; zusätzliche Vorlagendatei im Projekt.\n6. **Startvalidierung**: fehlende Arbeitsordner nur nach sichtbarer Zustimmung erstellen, danach Schreibbarkeit prüfen.\n7. **UI-Standard**: Eingaben/Auswahlfelder erhalten themeweit einen kontrastierenden Hintergrund; bestehende Zoom-/Theme-/Accessibility-Engine wird weiterverwendet.\n8. **Todo-Backlog**: neun Modulvorhaben plus 48 separat abhakbare Unteraufgaben idempotent ergänzt.\n\n## Sicherheitsgrenzen\n\n- Bestehende Nutzerdateien werden nicht gelöscht.\n- Neue Datenbestände nutzen atomare Schreibwege.\n- Backlog-Ergänzung arbeitet mit stabilen IDs und respektiert aktive sowie archivierte Aufgaben.\n- Das spätere Updatemodul wird nicht als unkontrollierter Selbstüberschreiber implementiert; vorgesehen ist ZIP-Prüfung → Integrität/Manifest → Checkpoint → Staging → Tests → Aktivierung → Nachprüfung → Rollback.\n- Keine neue externe Laufzeitabhängigkeit.\n\n## Technische Abnahme vor Versionssync\n\n- Branch-Head: `8b5525541cff430f9e820a02adf44f469acc43a7`\n- GitHub-Grundprüfung: **#685 – success**\n- Logik-/Regressionstests: **104**\n- PySide6-GUI-Tests: **74**\n- Release-Betriebsdateien: **46**\n- Headless-Start: **OK**\n- nativer Qt-Wayland-Smoke: **OK** (`QApplication.platformName() = wayland`)\n- Vollprojekt-Restore: **OK**\n- Restore-SHA-256: `1f1f46f35d5e733385c77e39c45366a812ce6b92f5a0786faaf948dbfddb4d41`\n\nDie sichtbare reale Kubuntu-26.04-/KDE-Plasma-Wayland-Abnahme bleibt separat erforderlich; Offscreen-/Weston-CI ersetzt keine reale Sichtprüfung.\n\n## Release-Schritt\n\nDie Version wird mit diesem Synchronisationslauf auf **0.17.0** gesetzt. Danach muss der vollständig synchronisierte Head nochmals Vollprüfung, 100–200-%-GUI-Regression, nativen Wayland-Smoke und Restore-Gate bestehen, bevor PR #45 gemergt werden darf.\n"""
write("docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md", doc)


# Vollständigkeitsprüfung um das neue Iterationsdokument ergänzen.
text = read("scripts/pruefen.sh")
needle = "docs/ITERATION29_PRESENTATION_POLICY.md)"
replacement = "docs/ITERATION29_PRESENTATION_POLICY.md docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md)"
text = replace_once(text, needle, replacement, label="Pruefen-Iteration34-Doku")
write("scripts/pruefen.sh", text)
