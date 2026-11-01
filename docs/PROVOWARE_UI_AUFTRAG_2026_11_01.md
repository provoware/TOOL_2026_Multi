# Professioneller Umsetzungsauftrag – Dashboard nach Screenshot 01.11.2026

**Repo:** provoware/TOOL_2026_Multi · **Version zu Beginn:** 0.18.5 · **Auftrag:** Issue #161 · **Stand:** 01.11.2026.

## Kopierbarer Entwicklungsauftrag für Codex / GitHub-Agenten

Du bist leitender PySide6-Entwickler, UI-Architekt, Fachberater für Musik-Datenbanken und Qualitätsprüfer. Überarbeite das vorhandene lokale Kubuntu-Programm `TOOL_2026_Multi` nach dem Nutzer-Screenshot und den in #161 einzeln erfassten 13 Wünschen. Benutze die bestehenden Module, Datenwege und Tests; baue keine zweite Datenbank, keinen Cloudzwang und kein anderes UI-Framework ein.

### Nicht verhandelbare Regeln
1. Lies vor Änderungen `AGENTS.md`, `TODO.md`, `docs/MODULPLAN_2026.md`, vorhandene PRs und den tatsächlichen GitHub-HEAD. Behandle neue Wünsche als Next Queue, sofern ein anderer Plan eingefroren ist.
2. Nur **ein Hauptziel je PR**. Beginne mit dem P0-Menüproblem. Für alle weiteren Wünsche neue kleine, voneinander unabhängige Schritte planen; keine unüberschaubare Gesamtersetzung.
3. Datenbestand geschützt: `daten/profile/db_profile.json` ist alleinige Quelle; `app.profile_store.add_values` und `app.genre_random` wiederverwenden. Profile ohne Einwilligung weder leeren noch überschreiben.
4. Native Qt-Mittel: `QScrollArea` für Menü/Listen, `QSplitter` und vorhandene Rastergriffe für Größen, Qt-Layouts plus Größenpolitik für dynamischen Platz. Keine Unterdrückung notwendiger Scrollleisten. Schrift bei kleinen Fenstern **nicht** automatisch unlesbar verkleinern.
5. Header gliedern: Titel/Navigation, Suche/Aktionen und Projektnotiz. Projekt-Notiz-Schreibschutz und bestehende Rückfragen beibehalten.
6. Dashboard-Schnelleingabe: Profil wählen → Kategorie wählen → mehrere Werte per Komma → Vorschau `neu/bereits vorhanden/fehlerhaft` → bewusst speichern → aktualisierte Auswahl und Weiterverwendung. Ungültige Eingaben lassen alle Altwerte unverändert.
7. Texte, Hilfen und Fehlermeldungen ausschließlich in verständlichem Deutsch; alle Bedienelemente für Tastatur und möglichst Screenreader benennen. Platzhalter optisch schwächer und semantisch getrennt von tatsächlichen Nutzerwerten.
8. Ein eigener Einstellungen-Bereich bündelt Themen, Zoom, Leisten, dynamische Buttonanpassung, Ansichtsreset und bei Bedarf Schriftgrößen. Benutzeroberflächenkonfiguration von privaten Projekt-/Kreativdaten trennen.
9. Textbuttons modern gruppiert mit klarer Farb-/Aktionshierarchie und Stern-Favoriten; rechts aufklappbar Schnellaktionen oben, Favoriten darunter. Beide Leisten optional; keine verdeckte Hauptarbeitsfläche.
10. Ereignisanzeige mindestens fünf letzte Einträge mit Zeit, Klartext, Grad und Details. Keine sensiblen Werte in der Kurzübersicht.
11. Musikdaten: Unterscheide echte Genres (z. B. MusicBrainz/Discogs) von Stimmungswörtern, Produktionsstilen, Stimmen und kreativen Effekten. Erstelle eine breite, geprüfte Ausgangsstruktur; je neuem Profil/Kategorie sind **100 fachlich verschiedene** Werte das Ziel. Keine inflationären Fantasiegenres zum Erreichen einer Zahl. Dokumentiere Quelle, Nutzungsbedingungen, Dublettenprüfung und fehlende Abdeckung. Erweiterte Kataloge nur **optional** und nach expliziter Auswahl importieren.
12. Jede Änderung: reproduzierbarer Vorher-Befund, kleiner Patch, gezielte Tests, volle GitHub-Prüfung nach bestehenden Gates, eigens getesteter main-Stand **nach** Merge, klare Ampel. Kein „grün“ ohne Evidenz.
13. Halte Datum, Ausführung, Status, Pfade, Tests und Git-Commit in `TODO.md`, `CHANGELOG.md` und den passenden Projektunterlagen konsistent. Keine vorzeitige finale Kubuntu-Abnahme.

### Prüfpunkte / Messwerte
- **Sichtbarkeit:** Alle Kernfunktionen bei 1020×650, 1366×768, 1600×900, 1920×1080 sowie gesonderte 800×600-Funktionsprobe erreichbar; Vergrößerung 100/125/150/175/200 %, Maus, Tab/Pfeiltasten, Scrollleiste.
- **W3C WCAG 2.2 AA:** normaler Text mindestens 4,5:1; großer Text 3:1; aktive Steuerungsgrenzen und Grafikindikatoren 3:1; 200-%-Textvergrößerung; Klickziel mindestens 24×24 CSS-Pixel bzw. anwendbare Ausnahme. 44×44 als Komfortziel, **nicht** mit AA-Pflicht verwechseln.
- **Gestaltung:** Hintergrund des Fensters, der Leisten, Arbeitskarten, Eingabefelder und Aktionsschalter durch eigenständige Farbtöne unterscheiden. Sichtbarer Kontrast bei normal, hover, aktiv, Fehler, deaktiviert und Fokus; reine Neonränder nie einziges Signal.
- **Profilimport:** atomar, sicher, idempotent (zweites Importieren erzeugt keine neuen Werte), Unicode-konform, Groß-/Kleinschreibung ignorieren, keine versteckten Änderungen am Bestand.
- **Freigabe:** GUI-, Daten-, Tastatur-, Status-, Wiederherstellungs-, Wayland- und CI-Nachweise werden dem gleichen Stand/Commit zugeordnet. Vor einer Gesamtfreigabe Restblocker ausweisen.

### Reihenfolge
**Iteration A:** P0-Menü-Ende scrollbar (Code, Regression, PR). **B:** Kopf/Kacheln/Ansichtseinstellungen. **C:** profilgebundene Schnellerfassung. **D:** Favoriten/Sidebar/Textbuttons. **E:** fachlich geprüfter Profilkatalog. **F:** Gesamtkontrolle.

**Quellen:** https://www.w3.org/TR/WCAG22/ · https://doc.qt.io/qt-6/qscrollarea.html · https://doc.qt.io/qt-6/qsplitter.html · https://musicbrainz.org/genres · https://support.discogs.com/hc/en-us/articles/360005055213-Database-Guidelines-9-Genres-Styles

### Recovery Key / aktuelle Grenze
Ausgangs-main: `4f188bb77d3e2aa803987dda39563efc4a266589`. Erste Änderung: `app/navigation_ux.py` auf Branch `fix/ux26-01-scrollbare-navigation-20261101`. Bestehender Modulplan bleibt maßgeblich. **Ein Prüfzweig ist weder geprüft noch veröffentlicht**, solange passende CI und main-Nachkontrolle fehlen.
