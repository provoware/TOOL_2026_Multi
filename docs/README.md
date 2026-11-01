# Technische Dokumentation – Wegweiser

**Stand:** 18. Oktober 2026

Du musst diese Dateien **nicht** lesen, um Provoware zu benutzen. Für den Alltag helfen zunächst die [einfache Anleitung](../ANLEITUNG_LAIEN.md) und die [Projektübersicht](../README.md).

## Welches Dokument brauche ich?

| Frage | Passende Datei |
|---|---|
| Was funktioniert heute, was fehlt noch? | [Aktueller Stand](AKTUELLER_STAND.md), [verbindlicher Modulplan](MODULPLAN_2026.md) und [Aufgabenübersicht](../TODO.md) |
| Welche Ordner enthalten persönliche Daten? | [Ordnerstruktur](ORDNERSTRUKTUR.md) |
| Wie sind Sicherung und Wiederherstellung bisher geplant? | [Sicherungskonzept](BACKUP_KONZEPT.md) |
| Welche Regeln gelten bei Änderungen? | [Entwicklungsregeln](ENTWICKLUNGSREGELN.md) und [AGENTS](../AGENTS.md) |
| Wie werden Fehler beschrieben und dauerhaft verhindert? | [Fehler und Rückfallprüfungen](FEHLER_UND_REGRESSION.md) |
| Welche Veränderungen gab es? | [Änderungsverlauf](../CHANGELOG.md) |
| Wo finde ich ältere technische Entscheidungen? | Die Berichte `ITERATION*.md` |

## Warum gibt es so viele ältere Berichte?

Jede Entwicklungsrunde wurde einzeln dokumentiert. Die Berichte erklären, welche Änderung damals gemacht und wie sie geprüft wurde. **Sie sind historische Nachweise und keine aktuelle Bedienungsanleitung.**

Ein dort stehender älterer Status muss deshalb nicht mehr der heutige Status sein. Maßgeblich sind `README.md`, `TODO.md`, `CHANGELOG.md` und der tatsächlich getestete GitHub-Stand.

## Einfache Sicherheitsregel

Beim Aufräumen **niemals blind** die Ordner `daten/`, `backups/`, `logs/` oder `berichte/` löschen. Auch bei Wartungsarbeiten an der Dokumentation dürfen persönliche Arbeitsdateien nicht verändert werden.

## Technische Qualitätsprüfung

- Kurzer Prüflauf: `bash scripts/pruefen.sh --quick`
- Vollständige Prüfung: `bash scripts/pruefen.sh --full`
- Die GitHub-Automatik überprüft zusätzlich einen Start unter Qt/Wayland, eine Projekt-Wiederherstellung und die Oberflächendiagnose.
- Die vollständige Oberflächenmatrix umfasst 60 Prüffälle; ein Erfolg im automatischen Test ersetzt keine Sichtprüfung auf dem Zielrechner.

Maßgeblich ist die Versionskennung im Manifest. Der neue Stand 0.18.4 ist ein Prüfkandidat; die Veröffentlichung bleibt getrennt.


## Neue Kreativmodule und nächste Leistungsdiagnose

- [Textbuttons und Buchwerkstatt](TEXTBUTTONS_UND_BUCHWERKSTATT.md) – Bedienung, Grenzen und Prüfumfang.
- [Messplan Diagnose](DIAGNOSE_MESSPLAN.md) – Vorschlag zu Ladezeiten, Schreibzugriffen, Cache, Ressourcen und kontrollierter Weitergabe; noch keine zusätzliche Erhebung.

- [Entwicklungsreview 18.10.2026](ENTWICKLUNGSREVIEW_2026_10_18.md) – belegte Qualität, Umwege, Codesparsamkeit und begrenzter Lernkreislauf.

- [Leistungsdiagnose 0.18.1](LEISTUNGSDIAGNOSE.md) – implementierter erster Ausbauschritt, Opt-in, Export und Messgrenzen.

- [Iteration 42: Dashboard-Layout und vollständige Matrix](ITERATION42_LAYOUT.md)

- [Persönliche Datensicherung](DATENSICHERUNG.md)
- [Schreib- und Ladebenchmarks](LEISTUNGSBENCHMARK.md)
- [UI-Kalibrierung vorbereiten](UI_KALIBRIERUNG.md)
- [Versionsunterlagen 0.18.3](FREIGABE_0_18_3.md)

- [Zentrale Text-/Dateisuche](DATEISUCHE.md)

- [Statisches Update-Staging](UPDATE_STAGING.md)

- [Ideenarchiv und Kontometadaten](IDEEN_UND_KONTEN.md)
- [Prozessstartmessung und Text-Strukturhilfen](STARTMESSUNG_UND_STRUKTUR.md)

- [Versionsunterlagen 0.18.4](FREIGABE_0_18_4.md)

- [Rechte Link-Schnellstarter-Leiste](SCHNELLSTARTER.md) – Bedienung, Datenschutz und Zoomgrenzen.

## Nutzerfreundlichkeit und Laientauglichkeit

- [UX-Analyse und Verbesserungskonzept](UX_KONZEPT_LAIENTAUGLICHKEIT.md) – Analyse vom 24.10.2026 mit belegten Befunden, Empfehlungen, Audit-Zuordnung und geplanten Abnahmeszenarien; keine Aussage über bereits umgesetzte Produktänderungen.

- [UI und Profildaten: 13 Hauptaufgaben, Unteraufgaben und Abnahmekriterien](UI_PROFIL_UNTERAUFGABEN_2026.md) – getrennte Datenbank-, Schnelleingabe-, Dubletten- und Modulabnahme.

- [Profil-/Datenbank-Bestandsabgleich](PROFIL_BESTANDSABGLEICH_2026_11_01.md) – Source, Prüfungen, Unicode-/Quotierungsgrenzen und tatsächliche Startmengen.

- [Profilwerte: Eingabe und Eindeutigkeit](PROFIL_EINGABEREGELN.md) – zitierte Kommas, Unicode, Importschutz und unveränderte Altbestände.

- [Fachliche Profilstruktur und Quellen](PROFIL_FACHSTRUKTUR_2026.md) – Paket B: zwölf Zielprofile, fünf feste Kategorien, Qualitäts- und Herkunftsregeln; [vollständige Planungsmatrix](PROFIL_ZIELMATRIX_2026.json), keine Aktivierung neuer Profildaten.

- [Gemeinsame Profil-Modul-API](PROFIL_MODUL_API.md) – rein lesender Profil-/Kategorie-/Suchvertrag, Unicodefilter und Datenbewahrung.
