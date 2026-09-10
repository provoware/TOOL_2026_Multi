from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise RuntimeError(f"Patchanker nicht eindeutig in {path}: {text.count(old)} Treffer")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


# 1) Profile: Komma-Eingabe atomar in Einzelwerte zerlegen.
replace_once(
    "app/profile_store.py",
    '''    save_profiles(root, profiles)\n    return clean_value\n\n\ndef remove_value''',
    '''    save_profiles(root, profiles)\n    return clean_value\n\n\ndef split_input_values(value: str) -> list[str]:\n    """Zerlegt eine Komma-Eingabe in bereinigte, innerhalb der Eingabe eindeutige Werte."""\n    result: list[str] = []\n    seen: set[str] = set()\n    for raw in str(value).split(","):\n        cleaned = " ".join(raw.strip().split())\n        if not cleaned:\n            continue\n        key = cleaned.casefold()\n        if key in seen:\n            continue\n        seen.add(key)\n        result.append(cleaned)\n    if not result:\n        raise ValueError("Bitte mindestens einen Wert eingeben.")\n    return result\n\n\ndef add_values(root: Path, profile: str, category: str, value_text: str) -> list[str]:\n    """Speichert eine Komma-Liste als einzelne DB-Einträge in genau einem atomaren Schreibvorgang."""\n    if category not in CATEGORIES:\n        raise ValueError("Unbekannte Kategorie.")\n    candidates = split_input_values(value_text)\n    profiles = load_profiles(root)\n    if profile not in profiles:\n        raise ValueError("Profil wurde nicht gefunden.")\n    existing = {value.casefold() for value in profiles[profile][category]}\n    added: list[str] = []\n    for candidate in candidates:\n        key = candidate.casefold()\n        if key in existing:\n            continue\n        profiles[profile][category].append(candidate)\n        existing.add(key)\n        added.append(candidate)\n    if added:\n        save_profiles(root, profiles)\n    return added\n\n\ndef remove_value''',
)

replace_once(
    "app/profile_editor.py",
    "from app.profile_store import CATEGORIES, add_profile, add_value, load_profiles, remove_value",
    "from app.profile_store import CATEGORIES, add_profile, add_values, load_profiles, remove_value",
)
replace_once(
    "app/profile_editor.py",
    'self.value_entry.setPlaceholderText("Neuen Wert eingeben …")',
    'self.value_entry.setPlaceholderText("Einen oder mehrere Werte eingeben · mit Komma trennen …")\n        self.value_entry.setToolTip("Beispiel: düster, treibend, melodisch. Jeder Begriff wird einzeln gespeichert.")',
)
replace_once(
    "app/profile_editor.py",
    '''        try:\n            value = add_value(self.project_root, profile, category, self.value_entry.text())\n        except Exception as error:\n            QMessageBox.warning(self, "Wert nicht gespeichert", f"Es wurde kein Wert hinzugefügt.\\n\\nGrund: {error}")\n            return\n        self.value_entry.clear()\n        self._changed()\n        self.status_label.setText(f"„{value}“ gespeichert.")\n        self.value_entry.setFocus()''',
    '''        try:\n            values = add_values(self.project_root, profile, category, self.value_entry.text())\n        except Exception as error:\n            QMessageBox.warning(self, "Wert nicht gespeichert", f"Es wurde kein Wert hinzugefügt.\\n\\nGrund: {error}")\n            return\n        self.value_entry.clear()\n        self._changed()\n        if values:\n            self.status_label.setText(f"{len(values)} Wert(e) einzeln gespeichert: {', '.join(values)}")\n        else:\n            self.status_label.setText("Alle eingegebenen Werte waren bereits vorhanden · keine Dubletten angelegt.")\n        self.value_entry.setFocus()''',
)

# 2) Songtext: freie, aber sichere Bereichsnamen.
replace_once(
    "app/song_document.py",
    '''def song_path(root: Path, title: str) -> Path:\n''',
    '''def normalize_section_name(value: str) -> str:\n    """Normalisiert Standard- und frei benannte Songbereiche ohne das Textformat zu beschädigen."""\n    cleaned = " ".join(str(value or "").strip().split())\n    if not cleaned:\n        raise ValueError("Bereichsname darf nicht leer sein.")\n    if any(char in cleaned for char in "[]\\0") or any(ord(char) < 32 for char in cleaned):\n        raise ValueError("Bereichsname enthält unzulässige Zeichen.")\n    return cleaned[:80]\n\n\ndef song_path(root: Path, title: str) -> Path:\n''',
)
replace_once(
    "app/song_editor.py",
    "from app.song_document import SECTION_TYPES, SONG_STATUSES, SongDocument, SongSection, export_song, save_song",
    "from app.song_document import SECTION_TYPES, SONG_STATUSES, SongDocument, SongSection, export_song, normalize_section_name, save_song",
)
replace_once(
    "app/song_editor.py",
    '''        self.section_type = QComboBox()\n        self.section_type.addItems(SECTION_TYPES)\n        self.section_type.setCurrentText("Strophe")''',
    '''        self.section_type = QComboBox()\n        self.section_type.addItems(SECTION_TYPES)\n        self.section_type.setEditable(True)\n        self.section_type.setInsertPolicy(QComboBox.NoInsert)\n        self.section_type.setToolTip("Standardbereich wählen oder einen eigenen Bereichsnamen eintippen.")\n        if self.section_type.lineEdit() is not None:\n            self.section_type.lineEdit().setPlaceholderText("Standard wählen oder eigenen Namen eingeben")\n        self.section_type.setCurrentText("Strophe")''',
)
replace_once(
    "app/song_editor.py",
    '''    def add_section(self) -> None:\n        self._store_current_section()\n        self.document.sections.append(SongSection(self.section_type.currentText() or "Strophe"))\n        self._refresh_section_list()''',
    '''    def add_section(self) -> None:\n        self._store_current_section()\n        try:\n            kind = normalize_section_name(self.section_type.currentText() or "Strophe")\n        except ValueError as error:\n            QMessageBox.information(self, "Bereich nicht angelegt", str(error))\n            return\n        self.document.sections.append(SongSection(kind))\n        if self.section_type.findText(kind) < 0:\n            self.section_type.addItem(kind)\n        self.section_type.setCurrentText(kind)\n        self._refresh_section_list()''',
)

# 3) Hilfe: genaue JSON-Vorlage in der sichtbaren Fehler-/Hilfefläche.
replace_once(
    "app/recovery_center.py",
    "from app.event_log import EventLogger",
    "from app.event_log import EventLogger\nfrom app.import_schema import song_import_help_text, song_import_template_text",
)
replace_once(
    "app/recovery_center.py",
    '''        refresh_button = QPushButton("Meldungen aktualisieren")\n        refresh_button.clicked.connect(self.refresh)\n        header.addWidget(refresh_button)''',
    '''        import_button = QPushButton("JSON-Importvorlage")\n        import_button.setToolTip("Zeigt die exakte JSON-Struktur für extern vorbereitete Songtexte.")\n        import_button.clicked.connect(self.show_import_template)\n        header.addWidget(import_button)\n        refresh_button = QPushButton("Meldungen aktualisieren")\n        refresh_button.clicked.connect(self.refresh)\n        header.addWidget(refresh_button)''',
)
replace_once(
    "app/recovery_center.py",
    '''    def refresh(self) -> None:\n''',
    '''    def show_import_template(self) -> None:\n        from PySide6.QtWidgets import QApplication\n\n        dialog = QDialog(self)\n        dialog.setWindowTitle("JSON-Importvorlage · Songtexte")\n        dialog.resize(860, 680)\n        layout = QVBoxLayout(dialog)\n        title = QLabel("JSON-Importvorlage für Songtexte")\n        title.setObjectName("sectionTitle")\n        layout.addWidget(title)\n        help_label = QLabel(\n            "Diese Struktur kann an außenstehende Personen weitergegeben werden. "\n            "Feldnamen und Datentypen müssen für einen späteren Import exakt eingehalten werden."\n        )\n        help_label.setObjectName("muted")\n        help_label.setWordWrap(True)\n        layout.addWidget(help_label)\n        text = QTextEdit()\n        text.setReadOnly(True)\n        text.setPlainText(song_import_help_text())\n        layout.addWidget(text, 1)\n        buttons = QHBoxLayout()\n        copy_button = QPushButton("JSON in Zwischenablage kopieren")\n        copy_button.setObjectName("primaryButton")\n        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(song_import_template_text()))\n        buttons.addWidget(copy_button)\n        buttons.addStretch(1)\n        close = QPushButton("Schließen")\n        close.clicked.connect(dialog.accept)\n        buttons.addWidget(close)\n        layout.addLayout(buttons)\n        apply_global_style(dialog, self.zoom_percent)\n        dialog.exec()\n\n    def refresh(self) -> None:\n''',
)

# 4) Todo: alle gewünschten Modulideen als idempotenten, detaillierten Projektplan aufnehmen.
replace_once(
    "app/todo_store.py",
    "from uuid import uuid4",
    "from uuid import NAMESPACE_URL, uuid4, uuid5",
)
replace_once(
    "app/todo_store.py",
    '''SCHEMA_VERSION = 1\n''',
    '''SCHEMA_VERSION = 1\n\nPROJECT_MODULE_BACKLOG: tuple[tuple[str, str], ...] = (\n    ("01 · Charakterfibel", "Ziel: konsistente, detaillierte Charaktere zentral pflegen.\\n☐ Datenmodell und atomare Speicherung\\n☐ Such-/Bearbeitungsoberfläche\\n☐ wiederverwendbare Charakter-IDs/API für andere Module\\n☐ Rollen, Aussehen, Persönlichkeit, Motivation, Hintergrund, Beziehungen, Sprache, Stärken, Schwächen, Tags und Notizen\\n☐ Zoom/Wayland/Recovery-Abnahme"),\n    ("02 · Profil- & Accountmanager", "Ziel: Webseiten-/Profilzugänge strukturiert und schnell wiederfinden.\\n☐ Webseite/URL, Profilname optional, verwendete E-Mail-Adresse, Passworthinweis und Sonstiges\\n☐ frei ergänzbare eigene Felder\\n☐ Gruppen, Suche und Filter\\n☐ Passwörter selbst nicht unverschlüsselt speichern; Schutzkonzept vor Umsetzung festlegen\\n☐ Import/Export, Backup, Restore und Datenschutzprüfung"),\n    ("03 · Universeller Texteditor", "Ziel: allgemeiner, farblich unterstützter Editor.\\n☐ Titel bestimmt sicheren Dateinamen\\n☐ große Schreibfläche und abschließendes Notizenfeld\\n☐ atomare Speicherung und Versionen\\n☐ Zugriff auf Charakterfibel\\n☐ einheitliche UI-/Zoom-/Wayland-Standards"),\n    ("04 · Textfragment- und Ideenarchiv", "Ziel: unvollendete Verse, Sätze, Textstücke und Schlagworte wiederverwerten.\\n☐ Fragmente einzeln oder gesammelt speichern\\n☐ Tags, Herkunft und Suche\\n☐ übersichtliche Karten-/Listenansicht\\n☐ Drag-and-drop in einen seitlichen Kompositionsbereich\\n☐ neue Texte aus mehreren Fragmenten zusammensetzen, ohne Originale zu löschen"),\n    ("05 · Autonomes Updatemodul", "Ziel: Updates weitgehend automatisch, aber datensicher durchführen.\\n☐ ZIP-Dateien prüfen und sicher entpacken\\n☐ Manifest, Version und Integrität vor Änderung validieren\\n☐ vollständiges Backup/Checkpoint vor Umsetzung\\n☐ Update in Staging testen, erst danach aktivieren\\n☐ automatischer Rollback bei Fehler\\n☐ Rechte-/Bestätigungsdialog für riskante Änderungen; kein blindes Systemüberschreiben"),\n    ("06 · Projektmodulbaukasten / Plugin-System", "Ziel: Projektstrukturen erstellen und dauerhaft erweiterbar halten.\\n☐ standardisierte Projektvorlagen\\n☐ Manifest für Module/Plugins\\n☐ definierte Plugin-Schnittstellen statt Direktzugriff\\n☐ Aktivieren/Deaktivieren ohne Kerncode zu beschädigen\\n☐ Abhängigkeits-, Versions- und Kompatibilitätsprüfung\\n☐ Test-/Stagingbereich für neue Module"),\n    ("07 · Rechte Schnellstarter-Symbolleiste", "Ziel: schmale persistente Symbolleiste für häufige Webziele.\\n☐ Starter hinzufügen/bearbeiten/entfernen\\n☐ URL validieren\\n☐ Name, Symbol und Gruppe speichern\\n☐ Beispiele YouTube, Suno und eigene Seiten\\n☐ Tastatur/Tooltip/Screenreader und sichere externe Browseröffnung"),\n    ("08 · Wikimodul", "Ziel: mehrere getrennte Wissensbasen verwalten.\\n☐ Wissensbasis anlegen/umbenennen\\n☐ Artikel mit Titel, Text, Tags und Verknüpfungen\\n☐ Volltextsuche und Querverweise\\n☐ Import/Export in dokumentiertem Format\\n☐ Versionen, Backup und Zugriff anderer Module"),\n    ("09 · Arbeitsverzeichnis- und Entwicklungspool", "Ziel: häufige Projektordner dateimanagerartig persistent verwalten.\\n☐ mehrere Arbeits-/Poolordner speichern und direkt öffnen\\n☐ Status wie Entwicklung, Beta, stabil und archiviert\\n☐ funktionierende Beta-/Release-Stände sicher ins Archiv duplizieren\\n☐ niemals bestehende Archive überschreiben; eindeutige Namen/Versionen\\n☐ organisieren, umbenennen und Metadaten bearbeiten\\n☐ Vor-/Nachprüfung sowie nachvollziehbares Protokoll"),\n)\n''',
)
replace_once(
    "app/todo_store.py",
    '''def active_tasks(root: Path) -> list[dict[str, object]]:\n''',
    '''def ensure_project_module_backlog(root: Path) -> int:\n    """Ergänzt die neun gewünschten Modulvorhaben genau einmal, ohne bestehende Todos anzutasten."""\n    state = load_state(root)\n    active = list(state["active"])\n    archive = list(state["archive"])\n    existing_titles = {str(item["title"]).casefold() for item in [*active, *archive]}\n    existing_ids = {str(item["id"]) for item in [*active, *archive]}\n    added = 0\n    now = _now_utc()\n    for title, note in PROJECT_MODULE_BACKLOG:\n        task_id = uuid5(NAMESPACE_URL, f"provoware-projektmodul:{title}").hex\n        if title.casefold() in existing_titles or task_id in existing_ids:\n            continue\n        active.append({\n            "id": task_id, "title": title, "note": note, "due": None,\n            "created_at": now, "completed_at": None,\n        })\n        existing_titles.add(title.casefold())\n        existing_ids.add(task_id)\n        added += 1\n    if added:\n        state["active"] = active\n        save_state(root, state)\n    return added\n\n\ndef active_tasks(root: Path) -> list[dict[str, object]]:\n''',
)
replace_once(
    "app/todo_window.py",
    "from app.todo_store import active_tasks, add_task, archived_tasks, complete_task",
    "from app.todo_store import active_tasks, add_task, archived_tasks, complete_task, ensure_project_module_backlog",
)
replace_once(
    "app/todo_window.py",
    '''        self._build()\n        self.set_zoom(zoom_percent)\n        self.refresh()\n        self.title_entry.setFocus()''',
    '''        self._build()\n        try:\n            added_backlog = ensure_project_module_backlog(self.project_root)\n        except Exception as error:\n            added_backlog = 0\n            self.status_label.setText(f"Projektmodul-Plan konnte nicht ergänzt werden · vorhandene Todos bleiben erhalten. Grund: {error}")\n        self.set_zoom(zoom_percent)\n        self.refresh()\n        if added_backlog:\n            self.status_label.setText(f"{added_backlog} Projektmodule als detaillierte Todos ergänzt · vorhandene Aufgaben blieben erhalten.")\n        self.title_entry.setFocus()''',
)

# 5) Zentrale Eingabefelder: deutlich eigener Kontrasthintergrund mit lesbarer Schrift.
for old, new in (
    ('"inverse_text": "#07111A",', '"inverse_text": "#07111A", "input_bg": "#50657A", "input_border": "#FFB11B",'),
    ('"inverse_text": "#041012",', '"inverse_text": "#041012", "input_bg": "#426970", "input_border": "#40F2E2",'),
    ('"inverse_text": "#13081A",', '"inverse_text": "#13081A", "input_bg": "#725184", "input_border": "#DFA0FF",'),
    ('"inverse_text": "#000000",', '"inverse_text": "#000000", "input_bg": "#606060", "input_border": "#FFFFFF",'),
):
    replace_once("app/ui_standards.py", old, new)

replace_once(
    "app/ui_standards.py",
    '''    QLineEdit, QTextEdit, QPlainTextEdit, QListWidget, QTreeWidget, QTableWidget {\n        background:{colors['surface']}; color:{colors['text']};\n        border:1px solid {colors['border']}; border-radius:{radius}px;\n        padding:{geometry_scaled(5, zoom_percent)}px;\n        selection-background-color:{colors['accent_soft']}; selection-color:{colors['text']};\n    }\n    QLineEdit { min-height:{control_height}px; }\n    QComboBox {\n        background:{colors['surface']}; color:{colors['text']};\n        border:1px solid {colors['border']}; border-radius:{radius}px;''',
    '''    QLineEdit, QTextEdit, QPlainTextEdit {\n        background:{colors['input_bg']}; color:{colors['text']};\n        border:1px solid {colors['input_border']}; border-radius:{radius}px;\n        padding:{geometry_scaled(5, zoom_percent)}px;\n        selection-background-color:{colors['accent_soft']}; selection-color:{colors['text']};\n    }\n    QListWidget, QTreeWidget, QTableWidget {\n        background:{colors['surface']}; color:{colors['text']};\n        border:1px solid {colors['border']}; border-radius:{radius}px;\n        padding:{geometry_scaled(5, zoom_percent)}px;\n        selection-background-color:{colors['accent_soft']}; selection-color:{colors['text']};\n    }\n    QLineEdit { min-height:{control_height}px; }\n    QComboBox {\n        background:{colors['input_bg']}; color:{colors['text']};\n        border:1px solid {colors['input_border']}; border-radius:{radius}px;''',
)

# 6) Dashboard: zwei neue Module als echte Einzelfenster integrieren.
replace_once(
    "app/ui.py",
    "from app.calendar_window import CalendarWindow",
    "from app.calendar_window import CalendarWindow\nfrom app.character_window import CharacterWindow",
)
replace_once(
    "app/ui.py",
    "from app.todo_window import TodoWindow",
    "from app.todo_window import TodoWindow\nfrom app.text_editor_window import TextEditorWindow",
)
replace_once(
    "app/ui.py",
    '''        self._calendar_window: CalendarWindow | None = None\n        self.nav_collapsed = False''',
    '''        self._calendar_window: CalendarWindow | None = None\n        self._character_window: CharacterWindow | None = None\n        self._text_editor_window: TextEditorWindow | None = None\n        self.nav_collapsed = False''',
)
replace_once(
    "app/ui.py",
    '''            ("♫\\nSongtexte", self.open_song_library, False, "Songtexte"),\n            ("▣\\nHörspiele\\nIn Planung", lambda: self._planned("Hörspiele"), True, "Hörspiele"),\n            ("▤\\nBlogartikel\\nIn Planung", lambda: self._planned("Blogartikel"), True, "Blogartikel"),\n            ("▥\\nGenres", lambda: self.open_profile_editor("Genres"), False, "Genres"),''',
    '''            ("♫\\nSongtexte", self.open_song_library, False, "Songtexte"),\n            ("♙\\nCharakterfibel", self.open_character_fibel, False, "Charakterfibel"),\n            ("✎\\nTexteditor", self.open_text_editor, False, "Texteditor"),\n            ("▥\\nGenres", lambda: self.open_profile_editor("Genres"), False, "Genres"),''',
)
replace_once(
    "app/ui.py",
    '''        self._add_nav(layout, "  ♫  Songtexte", self.open_song_library)\n        self._add_nav(layout, "  ▣  Hörspiele · geplant", lambda: self._planned("Hörspiele"), planned=True)''',
    '''        self._add_nav(layout, "  ♫  Songtexte", self.open_song_library)\n        self._add_nav(layout, "  ✎  Texteditor", self.open_text_editor)\n        self._add_nav(layout, "  ♙  Charakterfibel", self.open_character_fibel)\n        self._add_nav(layout, "  ▣  Hörspiele · geplant", lambda: self._planned("Hörspiele"), planned=True)''',
)
replace_once(
    "app/ui.py",
    '''            (self._todo_window, True),\n            (self._calendar_window, True),\n        )''',
    '''            (self._todo_window, True),\n            (self._calendar_window, True),\n            (self._character_window, False),\n            (self._text_editor_window, False),\n        )''',
)
replace_once(
    "app/ui.py",
    '''    def open_todo(self) -> None:\n''',
    '''    def open_character_fibel(self) -> None:\n        self._character_window = _open_managed_window(\n            self._character_window,\n            lambda: CharacterWindow(self.project_root, self.zoom_percent, parent=self),\n        )\n\n    def open_text_editor(self) -> None:\n        self._text_editor_window = _open_managed_window(\n            self._text_editor_window,\n            lambda: TextEditorWindow(self.project_root, self.zoom_percent, parent=self),\n            refresh_after_show=True,\n        )\n\n    def open_todo(self) -> None:\n''',
)

# 7) Menüaufbereitung kennt die neuen sofort nutzbaren Wege und kürzt sie bei 200 %.
replace_once(
    "app/navigation_ux.py",
    '''        song = _find_button(widgets, "Songtexte")\n        genres = _find_button(widgets, "Genres")''',
    '''        song = _find_button(widgets, "Songtexte")\n        text_editor = _find_button(widgets, "Texteditor")\n        characters = _find_button(widgets, "Charakterfibel")\n        genres = _find_button(widgets, "Genres")''',
)
replace_once(
    "app/navigation_ux.py",
    '''        self.ready_buttons = [\n            self._set_ready_button(song, "♫  Songtexte"),\n            self._set_ready_button(\n                genres, f"▦  {self._t('navigation.ready.profile', 'Genres & Vorgaben')}"\n            ),''',
    '''        self.ready_buttons = [\n            self._set_ready_button(song, "♫  Songtexte"),\n            self._set_ready_button(text_editor, "✎  Texteditor"),\n            self._set_ready_button(characters, "♙  Charakterfibel"),\n            self._set_ready_button(\n                genres, f"▦  {self._t('navigation.ready.profile', 'Genres & Vorgaben')}"\n            ),''',
)
replace_once(
    "app/navigation_ux.py",
    '''        self.dashboard.song_nav_button = song  # type: ignore[attr-defined]\n        self.dashboard.profile_nav_button = genres  # type: ignore[attr-defined]''',
    '''        self.dashboard.song_nav_button = song  # type: ignore[attr-defined]\n        self.dashboard.text_editor_nav_button = text_editor  # type: ignore[attr-defined]\n        self.dashboard.character_nav_button = characters  # type: ignore[attr-defined]\n        self.dashboard.profile_nav_button = genres  # type: ignore[attr-defined]''',
)
replace_once(
    "app/navigation_ux.py",
    '''        labels = (\n            "♫  Songtexte",\n            "▦  Vorgaben" if high_zoom else f"▦  {self._t('navigation.ready.profile', 'Genres & Vorgaben')}",\n            "✓  Todo-Liste",\n            "▦  Kalender",\n            "⚕  Fehlerhilfe" if high_zoom else "⚕  Fehlerhilfe (Recovery)",\n        )''',
    '''        labels = (\n            "♫  Songtexte",\n            "✎  Editor" if high_zoom else "✎  Texteditor",\n            "♙  Charaktere" if high_zoom else "♙  Charakterfibel",\n            "▦  Vorgaben" if high_zoom else f"▦  {self._t('navigation.ready.profile', 'Genres & Vorgaben')}",\n            "✓  Todo-Liste",\n            "▦  Kalender",\n            "⚕  Fehlerhilfe" if high_zoom else "⚕  Fehlerhilfe (Recovery)",\n        )''',
)

# 8) Start: fehlende Arbeitsordner niemals stillschweigend anlegen.
replace_once(
    "app/main.py",
    '''        from app.navigation_ux import install_navigation_ux\n\n        app = QApplication.instance() or QApplication([])''',
    '''        from app.navigation_ux import install_navigation_ux\n        from app.startup_validation import ensure_runtime_folders_gui\n\n        app = QApplication.instance() or QApplication([])''',
)
replace_once(
    "app/main.py",
    '''        configure_application(app)\n\n        guard = acquire_instance_guard(ROOT)''',
    '''        configure_application(app)\n\n        if not ensure_runtime_folders_gui(ROOT):\n            return 2\n\n        guard = acquire_instance_guard(ROOT)''',
)

# Testdouble des bestehenden Starttests an die neue, bewusst separate Startprüfung anpassen.
replace_once(
    "tests/test_diagnostics_logging.py",
    '''        fake_navigation = types.SimpleNamespace(install_navigation_ux=lambda *_args: None)\n        with tempfile.TemporaryDirectory() as temp:''',
    '''        fake_navigation = types.SimpleNamespace(install_navigation_ux=lambda *_args: None)\n        fake_startup = types.SimpleNamespace(ensure_runtime_folders_gui=lambda *_args: True)\n        with tempfile.TemporaryDirectory() as temp:''',
)
replace_once(
    "tests/test_diagnostics_logging.py",
    '''"app.ui_standards": fake_standards, "app.laptop_layout": fake_laptop, "app.navigation_ux": fake_navigation}):''',
    '''"app.ui_standards": fake_standards, "app.laptop_layout": fake_laptop, "app.navigation_ux": fake_navigation, "app.startup_validation": fake_startup}):''',
)

# Vollprüfung kennt alle neuen Betriebs- und Testdateien.
replace_once(
    "scripts/pruefen.sh",
    "app/navigation_ux.py app/atomic_io.py",
    "app/navigation_ux.py app/startup_validation.py app/character_store.py app/character_window.py app/text_editor_store.py app/text_editor_window.py app/import_schema.py app/atomic_io.py",
)
replace_once(
    "scripts/pruefen.sh",
    "tests/test_process_consistency.py tests/regression_registry.json",
    "tests/test_process_consistency.py tests/test_iteration34_core.py tests/test_iteration34_gui.py tests/regression_registry.json",
)
replace_once(
    "scripts/pruefen.sh",
    "tests.test_process_consistency tests.test_kubuntu_acceptance",
    "tests.test_process_consistency tests.test_iteration34_core tests.test_kubuntu_acceptance",
)
replace_once(
    "scripts/pruefen.sh",
    "tests.test_todo_gui tests.test_calendar_gui || fehler=1",
    "tests.test_todo_gui tests.test_calendar_gui tests.test_iteration34_gui || fehler=1",
)

print("Iteration-34-Patch vollständig angewendet.")
