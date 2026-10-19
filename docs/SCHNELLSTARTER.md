# Rechte Link-Schnellstarter-Leiste (in main seit 0.18.5)

## Aufgabe und Einstieg
Lokale Webadressen – beispielsweise YouTube, Suno und eigene Projektseiten – nach Name, Gruppe und optionalem kurzen Symboltext speichern. Die rechte schmale Leiste wird bei großen Fenstern (mindestens 1500 px, Zoom bis 125 %) gezeigt. Bei kleineren Fenstern bleibt der gesamte Arbeitsbereich frei; die Verwaltung ist immer im Modulmenü oben links oder mit **Strg+Alt+L** erreichbar.

## Bedienung
Im Modulfenster einen Eintrag anlegen, Name und `https://`- oder `http://`-Adresse eintragen und optional eine Gruppe sowie einen Symboltext hinzufügen. Eintrag speichern; im Listenfeld suchen, auswählen, bearbeiten, bewusst im Standardbrowser öffnen oder nach Rückfrage löschen. Import und Export verwenden die bestehenden sicheren Modularchive. Bereits vorhandene Namen oder Adressen werden innerhalb derselben Gruppe nicht verdoppelt.

## Schutzgrenzen
- Reine Offline-Ablage unter `daten/schnellstarter/bestand.json`; **keine** automatische Webanfrage. Die Internetverbindung wird erst durch bewusstes Öffnen im externen Browser verwendet.
- URL-Prüfung verwendet den bereits vorhandenen Konten-Webadressvertrag; keine `file:`-, `javascript:`- oder bekannten Geheimnisparameter.
- Atomare Speicherung und unveränderte Daten bei Fehlern; bestätigtes Löschen, kein automatisches Löschen doppelter Bestände.
- Schutz vor ungültigen JSON-Importen, 10-MB-Limit und maximal 2000 Einträgen; Exportpfade dürfen keine Projektdateien überschreiben.
- Die schmale Leiste zeigt bis zu sechs Verknüpfungen; alle Einträge bleiben über **Liste** erreichbar.
- Barrierearm: zugängliche Beschriftungen, Tastaturbedienung und dieselben Zoom-/Theme-Standards wie andere Module.

## Prüfstand
Quell- und GUI-Tests für Eingaben, Dopplungen, Import, Löschbestätigung, Speicherfehler, Browserübergabe, Zoom und Leiste liegen unter `tests/test_quicklinks*.py`. Eine tatsächliche Zielrechner-Bedienabnahme findet erst am Ende des Gesamtprojekts statt.
