# Ideenarchiv und Accountmanager

Version 0.18.4-Prüfkandidat · Iterationen 51/52. Basis: statisches Update-Staging 95f184c.

## Öffnen und gemeinsame Bedienung

Das Symbol oben links im Dashboard öffnet jetzt ein kleines **Modulmenü**. Dort Ideenarchiv oder Profil- & Accountmanager wählen. Tastatur: **Strg+Alt+I** für Ideen, **Strg+Alt+A** für Konten. Es gibt keine zusätzliche Sidebar-Zeile. Beide Fenster verwenden vorhandene Zoom-, Theme-, Import-/Export- und Entwurfsschutzfunktionen. Lange Feldbezeichnungen umbrechen, Formulare sind scrollbar.

Links gespeicherte Einträge durchsuchen und auswählen; rechts bearbeiten und speichern. **Neuen Eintrag anlegen** leert nur das Formular nach einer Rückfrage bei Änderungen. Der gespeicherte Bestand bleibt erhalten. F5 lädt die Liste neu; Strg+S speichert den aktuellen Eintrag. Vor dem Verlassen wird Speichern, Verwerfen oder Abbrechen angeboten. Diese beiden Module führen keinen automatischen zeitgesteuerten Entwurfsspeicher ein.

Importe werden geprüft und nach Bestätigung als neue Kopien mit neuen Kennungen ergänzt. Bestehende Einträge werden nicht still ersetzt. Die regulären Bestände liegen unter `daten/ideen/bestand.json` und `daten/konten/bestand.json`; die vorhandene persönliche Datensicherung erfasst sie. Der gemeinsame Archivschutz begrenzt Bestände auf 10 MiB, zusätzlich höchstens 2000 Einträge je Modul. Beschädigte Bestände werden nicht durch leere Dateien ersetzt.

## Ideen und Kompositionen

Eine Idee hat Titel, beliebigen mehrzeiligen Text, Schlagworte und Herkunft. Komma-Schlagworte werden bereinigt und dedupliziert. Die Suche findet auch Inhalte, Schlagworte und Herkunft. Die Liste zeigt Titel; beim Auswählen stehen alle Angaben rechts.

Ein Fragment aus der Liste in die Kompositionsfläche ziehen oder **Ausgewähltes Fragment als Kopie anfügen** wählen. Dies kopiert Klartext und löscht oder verändert keinen Archiveintrag. Kompositionstitel angeben und **Komposition als neuen Text speichern** wählen. Der neue Text liegt im bestehenden allgemeinen Texteditor. Ein schon vorhandener Titel wird abgewiesen; zum Bearbeiten den vorhandenen Text im Texteditor öffnen oder einen neuen Titel wählen.

Unverändertes erneutes Speichern einer gerade gespeicherten Komposition ist ohne zusätzliche Speicherung möglich. Geänderte Kompositionen mit demselben Titel überschreiben den alten Text nicht. Änderungen an der Komposition haben einen eigenen Verlassensschutz, auch wenn der ausgewählte Archiveintrag unverändert ist. Gewähltes Verwerfen leert die ungespeicherte Komposition; die gespeicherten Quellen bleiben bestehen.

## Kontometadaten und Datenschutz

Konten enthalten eine erforderliche http(s)-Webadresse sowie optionalen Profilnamen, E-Mail, Merkhilfe, Gruppe, Notizen und bis zu 30 eigene Textfelder. Zusatzfelder werden in einer Tabelle mit Feldname und Wert gepflegt. **Feld ergänzen** legt eine neue Zeile an; **Ausgewähltes Feld entfernen** entfernt eine Entwurfszeile. Namen und Werte lassen sich direkt bearbeiten. Leere Zeilen werden beim Speichern übersprungen, doppelte Feldnamen werden abgewiesen. Gruppen können im Listenfilter ausgewählt werden.

**Dies ist kein verschlüsselter Passworttresor.** Es gibt kein Passwortfeld und keine automatische Anmeldung. Reale Passwörter, Tokens, Wiederherstellungscodes und private Schlüssel gehören in einen dafür vorgesehenen Passwortmanager. Bekannte Geheimnisfeldnamen werden abgewiesen; unbekannte Felder auf oberster Ebene ebenfalls. Webadressen mit Benutzer-/Passwortbestandteilen oder erkennbaren Geheimnisparametern in Query/Fragment werden abgewiesen. Der Browser wird nur nach bewusstem Klick auf eine validierte Adresse geöffnet.

Kontometadaten bleiben lokal unverschlüsselt. Das Programm kann nicht erkennen, ob jemand ein echtes Geheimnis in ein beliebig benanntes Freitextfeld oder eine undurchsichtige URL schreibt. Darum sind Warnhinweis und Feldbeschriftungen direkt sichtbar; die Schutzfunktion darf nicht als allgemeine Geheimniserkennung oder Verschlüsselung verstanden werden. E-Mails, Merkhilfen und Notizen können trotzdem privat sein. Vor dem Export erscheint eine eigene Bestätigung mit Hinweis auf diese unverschlüsselten Inhalte. Keine automatische Übertragung oder Übernahme in Diagnosepakete wird ergänzt.

Prüfung: Daten-/GUI-Tests für atomare Erhaltung bei Fehlern, neue Importkennungen, Suche/Tags/Gruppen, Originalschutz bei Kompositionen, Dateikollisionen, Entwurfsabbruch/Verwerfen, bekannte Geheimnisfelder/-URLs, bewussten Browseraufruf, Exportabbruch und persönliche Datensicherungs-/Restore-Integration. Ein eigener Dashboard-Test prüft Modulmenü, eigenständige Fenster, Registry und Zoom-Verteilung.
