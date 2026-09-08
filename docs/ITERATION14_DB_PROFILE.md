# Iteration 14 – profilbasierte DB-Eingaben

## Ziel
Genres, Stimmungen, Stil, Stimme und Besonderheiten werden nicht mehr nur als leere Platzhalter gezeigt, sondern profilweise verwaltet und direkt im Dashboard auswählbar gemacht.

## Profile
Mitgelieferte Startprofile:
- HardTechno
- HipHop/Rap
- Hörspiele

Die Startwerte stehen im Programmcode und erzeugen beim bloßen Öffnen noch keine Nutzerdatendatei. Erst eine eigene Änderung schreibt den Bestand nach `daten/profile/db_profile.json`.

## Kategorien
- Genres
- Stimmungen
- Stil
- Stimme
- Besonderheiten

GitHub-Repositories und Prompts bleiben außerhalb dieser Fachiteration unverändert als geplante Bereiche bestehen.

## Bedienung
- Kachel `Genres` oder ein DB-Eingabepunkt links öffnet die Profilverwaltung.
- Im Dashboard befindet sich in der DB-Karte eine Profilauswahl.
- Ein Profilwechsel lädt sofort die zugehörigen Werte in die fünf Auswahlfelder.
- Neue Profile und neue Werte können angelegt werden.
- Entfernen eines Werts verlangt eine ausdrückliche Bestätigung.

## Datensicherheit
- JSON wird validiert.
- Speicherung erfolgt über temporäre Datei, `fsync` und atomaren `os.replace`.
- Bei fehlgeschlagenem Ersetzen bleibt der vorherige Bestand unverändert.
- Doppelte Werte werden ohne Beachtung der Groß-/Kleinschreibung verhindert.
- Profile sind voneinander getrennt.
- Es gibt keine automatische Datenmigration vorhandener Songdateien.

## Abnahme
- Standardprofile ohne Schreibzugriff verfügbar.
- Profil- und Kategorieisolation geprüft.
- Duplikatschutz geprüft.
- simulierter atomarer Schreibfehler geprüft.
- Profilwechsel im Dashboard befüllt die passenden Auswahlfelder.
- Änderungen werden ohne Neustart im Dashboard sichtbar.
