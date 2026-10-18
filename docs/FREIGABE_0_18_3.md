# Provoware 0.18.3 – vorbereitete Versionsunterlagen

TOOL_2026_Multi · Repository provoware/TOOL_2026_Multi.
Status: lokaler Prüfkandidat, nicht veröffentlicht und nicht automatisch mit main zusammengeführt. Die echte Zielrechner-Abnahme wurde auf Nutzerwunsch zurückgestellt.

## Lieferumfang und Änderungen

- Zentrale gespeicherte Text-/Dateisuche mit Trefferliste, Klartextvorschau und Abbruch; keine Dateimutationen oder Indexdateien. Einstieg über Kopf, Kachel und Strg+Umschalt+F.

- Datensicherungswerkzeug mit eindeutigen ZIP-Namen, SHA-256, Inhaltsindex und automatischer isolierter Wiederherstellung. Kein Überschreiben bestehender Rückholziele, kein automatischer Austausch persönlicher Arbeitsdaten.
- Robuster Start: vorhandene defekte `.venv` erhalten, tatsächliche Paketversionen/Qt-Import unabhängig vom Marker prüfen und Installations-/Prüfwege mit Zeitgrenzen versehen.
- Entwicklermessungen: identische Schreibmengen in drei Varianten; Bucharchiv-Laden in neuen Prozessen mit festen Datenklassen und getrennten ersten/wiederholten Lesevorgängen.
- Auswertung gespeicherter UI-Kalibrierungsnachweise mit Dubletten-/Befundschutz; keine automatische Pflicht-Gate-Aktivierung.
- Versionskennung aus dem bestehenden Manifest über den Logger im Dashboard-Fenstertitel. Keine zweite Versionsquelle.

Keine Migration persönlicher Daten. Keine neue externe Abhängigkeit. Python 3 und PySide6 6.11.2; regulärer Start über `bash schnellstart.sh`. Zielplattform bleibt Kubuntu 26.04 / KDE Plasma Wayland; Offscreen-Prüfungen ersetzen diesen Zielrechner nicht.

Das Runtime-ZIP enthält nur die im Manifest freigegebenen Betriebsdateien einschließlich Sicherungs- und Starthilfen. Entwicklerscripts und Tests liegen im vollständigen Projekt-ZIP. Persönliche Dateien, Protokolle, virtuelle Umgebungen und verschachtelte Sicherungen gehören nicht in die Freigabepakete.

## Prüfung und Nachweise

Gezielte Schutztests je Teilauftrag; anschließend `bash scripts/pruefen.sh --full`, vollständige UI-Shadow-Matrix und `scripts/iteration_restore.py` für das vollständige ZIP. Prüfergebnisse werden außerhalb des Quellbaums mit geprüftem HEAD und Prüfsummen aufbewahrt. Dieser Text behauptet keinen CI-Erfolg für einen noch nicht ausgeführten GitHub-Lauf.

Offen und zurückgestellt: sichtbare Kubuntu-/Plasma-Abnahme, reale Zielrechner-Leistungsmessung, finale GitHub-Prüfung des Kandidaten und tatsächliche Veröffentlichung. UI-Pflichtregeln werden erst nach belegter Kalibrierung gesondert aktiviert.

## Sicherer Wechsel und Rückkehr

Vor einem späteren Wechsel Programm schließen und persönliche Daten gemäß [Datensicherungsanleitung](DATENSICHERUNG.md) auf einen zweiten geschützten Datenträger sichern. Neue Programmversion in einen neuen Ordner entpacken. Alte Programm- und Datenordner erhalten. Ein automatischer Update-Manager mit atomarer Aktivierung/Rollback ist weiterhin geplant; diese Version behauptet ihn nicht.

Eine Datenwiederherstellung landet ausschließlich in einem neuen Prüfordner. Erst nach erfolgreichem Dateivergleich bewusst übernehmen. Bei einem Startfehler keine persönlichen Daten löschen; siehe [Anleitung](../ANLEITUNG_LAIEN.md). Die alte Programmversion kann mit ihrem erhaltenen Datenbestand weiterverwendet werden.
