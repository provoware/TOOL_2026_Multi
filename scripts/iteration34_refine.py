from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Refinement-Anker nicht eindeutig in {path}: {count} Treffer")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


# Eingabewerte durch dieselbe bestehende Einzelwert-Validierung schicken.
replace_once(
    "app/profile_store.py",
    '''        cleaned = " ".join(raw.strip().split())
        if not cleaned:
            continue
        key = cleaned.casefold()''',
    '''        if not raw.strip():
            continue
        cleaned = _normalize_value(raw)
        key = cleaned.casefold()''',
)

# Detailpunkte der neun Modulpläne als echte, einzeln abhakbare Todos bereitstellen.
replace_once(
    "app/todo_store.py",
    ''')


def store_path(root: Path) -> Path:
''',
    ''')

PROJECT_MODULE_SUBTASKS: tuple[tuple[str, str], ...] = (
    ("01.1 · Charakterfibel – Datenmodell & sichere Speicherung", "Charakterdaten atomar speichern, Schema validieren und bestehende Daten bei Schreibfehlern erhalten."),
    ("01.2 · Charakterfibel – Such- & Bearbeitungsoberfläche", "Suchen, auswählen, neu anlegen und bestehende Charaktere verständlich bearbeiten."),
    ("01.3 · Charakterfibel – gemeinsame Modul-Schnittstelle", "Stabile Charakter-IDs und lesende Schnittstelle für Texteditor, Hörspiel, Wiki und spätere Module bereitstellen."),
    ("01.4 · Charakterfibel – vollständige Charakterfelder", "Rolle, Alter, Aussehen, Persönlichkeit, Motivation, Hintergrund, Beziehungen, Sprache, Stärken, Schwächen, Tags und Notizen prüfen."),
    ("01.5 · Charakterfibel – Zoom, Wayland, Backup & Recovery abnehmen", "100–200 %, Tastatur, Kontrast, Wayland und Wiederherstellung real und automatisiert prüfen."),

    ("02.1 · Accountmanager – Schutzkonzept festlegen", "Vor Implementierung klären: keine Passwörter im Klartext; Passworthinweise und sensible Felder geschützt behandeln."),
    ("02.2 · Accountmanager – Grundfelder", "Webseite/URL, Profilname optional, genutzte E-Mail-Adresse, Passworthinweis und Sonstiges speichern."),
    ("02.3 · Accountmanager – eigene Felder", "Zusätzliche benutzerdefinierte Felder je Eintrag sicher anlegen, umbenennen und entfernen können."),
    ("02.4 · Accountmanager – Gruppen, Suche & Schnellfinden", "Einträge gruppieren, filtern und über mehrere Felder schnell wiederfinden."),
    ("02.5 · Accountmanager – Import/Export, Backup & Datenschutz", "Datenformat dokumentieren, Sicherung/Restore testen und sensible Inhalte bei Diagnoseexporten schützen."),

    ("03.1 · Texteditor – Titel wird sicherer Dateiname", "Titel validieren und als Linux-kompatiblen Dateinamen verwenden; Umbenennung ohne Datenverlust."),
    ("03.2 · Texteditor – Schreibfläche & Abschlussnotizen", "Große Schreibfläche und getrenntes abschließendes Notizenfeld bereitstellen."),
    ("03.3 · Texteditor – Versionen & Autosave", "Atomare Speicherung, sichere Versionen und 5-Minuten-Autosave validieren."),
    ("03.4 · Texteditor – Charakterfibel anbinden", "Charaktere aus zentralem Bestand auswählen/referenzieren, ohne Daten zu duplizieren."),
    ("03.5 · Texteditor – Farb-, Zoom- & Wayland-Abnahme", "Einheitliche UI-Standards, Eingabekontrast und 100–200-%-Darstellung prüfen."),

    ("04.1 · Fragmentarchiv – Fragment-Datenmodell", "Schlagworte, Sätze, Verse und längere Fragmente einzeln oder gesammelt verlustfrei speichern."),
    ("04.2 · Fragmentarchiv – Herkunft, Tags & Suche", "Quelle/Herkunft, Tags, Status und Volltextsuche vorsehen."),
    ("04.3 · Fragmentarchiv – übersichtliche Bibliothek", "Karten-/Listenansicht mit Filtern, Vorschau und gut lesbaren Zuständen entwickeln."),
    ("04.4 · Fragmentarchiv – Drag-and-drop-Komposition", "Fragmente per Ziehen in einen seitlichen Kompositionsbereich legen und frei anordnen."),
    ("04.5 · Fragmentarchiv – neue Texte ohne Originalverlust", "Zusammengesetzte Texte speichern/exportieren; Ursprungsfragmente niemals automatisch löschen."),

    ("05.1 · Updatemodul – ZIP sicher prüfen & entpacken", "ZIP-Pfadtraversal, unerwartete Dateien und ungültige Archive vor Entpacken blockieren."),
    ("05.2 · Updatemodul – Manifest, Version & Integrität", "Version, Dateiliste und Prüfsummen vor jeder Änderung validieren."),
    ("05.3 · Updatemodul – Backup/Checkpoint", "Vor jedem Update einen vollständigen, validierten Rückkehrpunkt erzeugen."),
    ("05.4 · Updatemodul – Staging & automatische Prüfung", "Update zunächst isoliert anwenden und vollständige Tests ausführen, bevor es aktiv wird."),
    ("05.5 · Updatemodul – Rollback", "Bei Fehler automatisch auf den letzten geprüften Stand zurückkehren und Ursache protokollieren."),
    ("05.6 · Updatemodul – Rechte & Freigaben", "Riskante System-/Rechteänderungen nie blind ausführen; Ziel, Wirkung und Alternative verständlich bestätigen lassen."),

    ("06.1 · Projektbaukasten – Projektvorlagen", "Standardisierte, laienverständlich benannte Projektstrukturen mit README, TODO, Doku, Logs und Regeln erzeugen."),
    ("06.2 · Projektbaukasten – Modul-/Plugin-Manifest", "Name, Version, Fähigkeiten, Abhängigkeiten und Kompatibilität maschinenlesbar beschreiben."),
    ("06.3 · Projektbaukasten – stabile Plugin-Schnittstellen", "Plugins nur über definierte APIs anbinden; keine unkontrollierten Direktzugriffe auf Kerninternas."),
    ("06.4 · Projektbaukasten – Aktivieren/Deaktivieren", "Module reversibel ein-/ausschalten, ohne Kerndaten oder andere Plugins zu beschädigen."),
    ("06.5 · Projektbaukasten – Abhängigkeiten & Kompatibilität", "Versionskonflikte vor Aktivierung erkennen und verständlich erklären."),
    ("06.6 · Projektbaukasten – Test-/Stagingbereich", "Neue Plugins isoliert prüfen und erst nach erfolgreicher Regression freigeben."),

    ("07.1 · Schnellstarterleiste – rechte schmale Symbolleiste", "Platzsparenden, ein-/ausblendbaren rechten Randbereich entwickeln."),
    ("07.2 · Schnellstarterleiste – Starter verwalten", "Starter hinzufügen, bearbeiten, sortieren, gruppieren und entfernen können."),
    ("07.3 · Schnellstarterleiste – URL-Validierung", "Nur plausible http/https-Ziele akzeptieren und fehlerhafte Eingaben verständlich melden."),
    ("07.4 · Schnellstarterleiste – Symbole & Beispiele", "Name/Symbol speichern; YouTube, Suno und eigene Seiten als Beispiele unterstützen."),
    ("07.5 · Schnellstarterleiste – sichere Browseröffnung & Accessibility", "Externen Standardbrowser nutzen; Tooltip, Tastaturfokus und Screenreader-Namen bereitstellen."),

    ("08.1 · Wikimodul – mehrere Wissensbasen", "Getrennte Wissensbasen anlegen, umbenennen, auswählen und strukturiert verwalten."),
    ("08.2 · Wikimodul – Artikelmodell", "Titel, Inhalt, Tags, Kategorie, Quellenhinweis und Querverweise speichern."),
    ("08.3 · Wikimodul – Volltextsuche & Verknüpfungen", "Artikel schnell finden und interne Beziehungen sichtbar navigierbar machen."),
    ("08.4 · Wikimodul – dokumentierter Import/Export", "Offenes JSON-/Textformat mit exakter Vorlage und Validierung bereitstellen."),
    ("08.5 · Wikimodul – Versionen, Backup & Modulzugriff", "Artikelversionen sichern und lesenden Zugriff für andere Module definieren."),

    ("09.1 · Arbeitsverzeichnisse – persistente Ordnerliste", "Mehrere Entwicklungspool-/Arbeitsordner dauerhaft speichern und direkt anspringen."),
    ("09.2 · Arbeitsverzeichnisse – dateimanagerartige Übersicht", "Ordner/Dateien übersichtlich anzeigen, filtern und im System-Dateimanager öffnen."),
    ("09.3 · Arbeitsverzeichnisse – Entwicklungsstatus", "Projekte als Entwicklung, Beta, stabil oder archiviert kennzeichnen und filtern."),
    ("09.4 · Arbeitsverzeichnisse – sichere Archivkopien", "Funktionierende Beta-/Release-Stände duplizieren; niemals vorhandene Archive überschreiben."),
    ("09.5 · Arbeitsverzeichnisse – Organisation & Metadaten", "Archivnamen, Version, Notiz, Datum und Zuordnung bearbeiten, ohne Projektdateien unnötig umzuschreiben."),
    ("09.6 · Arbeitsverzeichnisse – Vor-/Nachprüfung & Protokoll", "Quelle/Ziel, freier Speicher und Ergebnis validieren; Kopiervorgänge nachvollziehbar protokollieren."),
)

PROJECT_MODULE_TASK_COUNT = len(PROJECT_MODULE_BACKLOG) + len(PROJECT_MODULE_SUBTASKS)


def store_path(root: Path) -> Path:
''',
)
replace_once(
    "app/todo_store.py",
    '''    for title, note in PROJECT_MODULE_BACKLOG:
''',
    '''    for title, note in (*PROJECT_MODULE_BACKLOG, *PROJECT_MODULE_SUBTASKS):
''',
)

# Bestehende Regressionen auf den neuen Sollzustand umstellen.
replace_once(
    "tests/test_layman_ux_gui.py",
    '''        self.assertEqual(len(planned), 5)
        self.assertTrue(all("In Planung" in button.text() for button in planned))''',
    '''        self.assertEqual(len(planned), 3)
        ready = [button for button in tiles if button.property("ready") is True]
        self.assertEqual(len(ready), 4)
        self.assertTrue(all("In Planung" in button.text() for button in planned))
        self.assertTrue(any("Charakterfibel" in button.text() for button in ready))
        self.assertTrue(any("Texteditor" in button.text() for button in ready))''',
)
replace_once(
    "tests/test_dashboard_reference_gui.py",
    '''        self.assertEqual(len(ready_tiles), 2)
        self.assertTrue(all(button.isVisible() for button in ready_tiles))''',
    '''        self.assertEqual(len(ready_tiles), 4)
        self.assertTrue(all(button.isVisible() for button in ready_tiles))
        self.assertTrue(any("Charakterfibel" in button.text() for button in ready_tiles))
        self.assertTrue(any("Texteditor" in button.text() for button in ready_tiles))''',
)
replace_once(
    "tests/test_todo_gui.py",
    '''    def test_add_without_due_and_archive_after_complete(self):
        self.window.title_entry.setText("Milch kaufen")''',
    '''    def test_add_without_due_and_archive_after_complete(self):
        baseline_active = len(active_tasks(self.root))
        baseline_archive = len(archived_tasks(self.root))
        self.window.title_entry.setText("Milch kaufen")''',
)
replace_once(
    "tests/test_todo_gui.py",
    '''        self.assertEqual(len(active_tasks(self.root)), 1)
        self.assertEqual(self.window.active_table.rowCount(), 1)
        self.window.active_table.selectRow(0)
        self.window.complete_selected()
        self.app.processEvents()
        self.assertEqual(active_tasks(self.root), [])
        self.assertEqual(len(archived_tasks(self.root)), 1)
        self.assertEqual(self.window.archive_table.rowCount(), 1)''',
    '''        self.assertEqual(len(active_tasks(self.root)), baseline_active + 1)
        self.assertEqual(self.window.active_table.rowCount(), baseline_active + 1)
        row = next(
            row for row in range(self.window.active_table.rowCount())
            if self.window.active_table.item(row, 0).text() == "Milch kaufen"
        )
        self.window.active_table.selectRow(row)
        self.window.complete_selected()
        self.app.processEvents()
        self.assertEqual(len(active_tasks(self.root)), baseline_active)
        self.assertEqual(len(archived_tasks(self.root)), baseline_archive + 1)
        self.assertEqual(self.window.archive_table.rowCount(), baseline_archive + 1)''',
)
replace_once(
    "tests/test_iteration34_core.py",
    "from app.todo_store import PROJECT_MODULE_BACKLOG, ensure_project_module_backlog, load_state",
    "from app.todo_store import PROJECT_MODULE_BACKLOG, PROJECT_MODULE_SUBTASKS, PROJECT_MODULE_TASK_COUNT, ensure_project_module_backlog, load_state",
)
replace_once(
    "tests/test_iteration34_core.py",
    '''            self.assertEqual(first, len(PROJECT_MODULE_BACKLOG))
            self.assertEqual(second, 0)
            state = load_state(root)
            self.assertEqual(len(state["active"]), len(PROJECT_MODULE_BACKLOG))''',
    '''            self.assertEqual(first, PROJECT_MODULE_TASK_COUNT)
            self.assertEqual(second, 0)
            state = load_state(root)
            self.assertEqual(len(state["active"]), PROJECT_MODULE_TASK_COUNT)
            self.assertGreater(len(PROJECT_MODULE_SUBTASKS), 40)''',
)

# Eingabekontrast nicht nur im CSS suchen, sondern numerisch >= 4.5:1 absichern.
replace_once(
    "tests/test_iteration34_gui.py",
    "from app.ui_standards import app_stylesheet, theme_colors",
    "from app.ui_standards import THEMES, app_stylesheet, theme_colors",
)
replace_once(
    "tests/test_iteration34_gui.py",
    '''class Iteration34GuiTests(unittest.TestCase):
''',
    '''def _luminance(hex_color: str) -> float:
    values = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    values = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in values]
    return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2]


def _contrast(first: str, second: str) -> float:
    light, dark = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


class Iteration34GuiTests(unittest.TestCase):
''',
)
replace_once(
    "tests/test_iteration34_gui.py",
    '''        self.assertIn(colors["input_bg"], css)
        self.assertIn(colors["input_border"], css)
        sample = CharacterWindow(self.root, 100)''',
    '''        self.assertIn(colors["input_bg"], css)
        self.assertIn(colors["input_border"], css)
        for palette in THEMES.values():
            self.assertGreaterEqual(_contrast(palette["text"], palette["input_bg"]), 4.5)
        sample = CharacterWindow(self.root, 100)''',
)

# Textversionen nur anlegen, wenn sich fachlicher Inhalt wirklich geändert hat.
replace_once(
    "app/text_editor_store.py",
    '''    if target.is_file():
        current = json.loads(target.read_text(encoding="utf-8"))
        if _validate_payload(current) != payload:
            atomic_write_json(_version_path(root, target.stem), _validate_payload(current))
''',
    '''    if target.is_file():
        current = _validate_payload(json.loads(target.read_text(encoding="utf-8")))
        comparable_current = {key: value for key, value in current.items() if key != "updated_at"}
        comparable_new = {key: value for key, value in payload.items() if key != "updated_at"}
        if comparable_current != comparable_new:
            atomic_write_json(_version_path(root, target.stem), current)
''',
)

# Release-Manifest muss alle neuen Runtime-Module und die öffentliche Importvorlage enthalten.
replace_once(
    "MANIFEST.json",
    '''    {"path":"app/navigation_ux.py","release":true,"purpose":"Laienfreundliche Menü-Hierarchie mit einklappbaren geplanten Bereichen"},
    {"path":"app/atomic_io.py","release":true,''',
    '''    {"path":"app/navigation_ux.py","release":true,"purpose":"Laienfreundliche Menü-Hierarchie mit einklappbaren geplanten Bereichen"},
    {"path":"app/startup_validation.py","release":true,"purpose":"Explizite Startordner-Prüfung mit Zustimmung vor Erstellung und Schreibtest"},
    {"path":"app/character_store.py","release":true,"purpose":"Atomarer wiederverwendbarer Charakterfibel-Datenbestand"},
    {"path":"app/character_window.py","release":true,"purpose":"Eigenständiges Charakterfibel-Modul"},
    {"path":"app/text_editor_store.py","release":true,"purpose":"Atomare allgemeine Textdokumente mit Versionen"},
    {"path":"app/text_editor_window.py","release":true,"purpose":"Eigenständiger allgemeiner Texteditor mit Charakterreferenzen"},
    {"path":"app/import_schema.py","release":true,"purpose":"Exakte validierbare JSON-Importstruktur für Songtexte"},
    {"path":"app/atomic_io.py","release":true,''',
)
replace_once(
    "MANIFEST.json",
    '''    {"path":"texte/registry.json","release":true,"purpose":"Zentrale Nutzertexte"},
    {"path":"README.md","release":false,''',
    '''    {"path":"texte/registry.json","release":true,"purpose":"Zentrale Nutzertexte"},
    {"path":"vorlagen/songtext_import_vorlage.json","release":true,"purpose":"Weitergebbare exakte JSON-Beispielvorlage für Songtextimporte"},
    {"path":"README.md","release":false,''',
)
replace_once(
    "MANIFEST.json",
    '''    {"path":"tests/test_process_consistency.py","release":false,"purpose":"Atomar-, Direktstart-, Mehrfachstart- und Wächterregression"},''',
    '''    {"path":"tests/test_process_consistency.py","release":false,"purpose":"Atomar-, Direktstart-, Mehrfachstart- und Wächterregression"},
    {"path":"tests/test_iteration34_core.py","release":false,"purpose":"Kernregressionen für neue Module, Import, Startordner, Komma-Eingaben und Todo-Backlog"},
    {"path":"tests/test_iteration34_gui.py","release":false,"purpose":"GUI-Regressionen für Charakterfibel, Texteditor, freie Songbereiche und Eingabekontrast"},''',
)

# Runtime-Check prüft die mitgelieferte Importvorlage ebenfalls.
replace_once(
    "scripts/pruefen.sh",
    '''scripts/kubuntu_abnahme.py texte/registry.json)''',
    '''scripts/kubuntu_abnahme.py texte/registry.json vorlagen/songtext_import_vorlage.json)''',
)
replace_once(
    "scripts/pruefen.sh",
    '''python3 -m json.tool texte/registry.json >/dev/null || fehler=1
''',
    '''python3 -m json.tool texte/registry.json >/dev/null || fehler=1
python3 -m json.tool vorlagen/songtext_import_vorlage.json >/dev/null || fehler=1
''',
)

print("Iteration-34-Refinement vollständig angewendet.")
