# PV-GENRE-STATS-01 – beschädigte Monatsstatistik sicher abweisen

**Datum:** 27.10.2026 · **Basis:** `096dc03ae362eed8141b0dbc0c8e91ab0b8daa2d` · **Bereich:** Genre-Zufall / Monatsauswertung

## Befund
Die Verlaufsprüfung akzeptiert ältere Einträge ohne `categories` aus Kompatibilitätsgründen. Ein beschädigtes vorhandenes `categories`-Feld (z. B. `null` statt Objekt oder ein Objekt als gezogener Begriff) führte in `monthly_statistics` bisher zu `AttributeError` bzw. `TypeError`. Die Monatsauswertung konnte deshalb unerwartet abbrechen.

## Kleinstmögliche Korrektur
Die Monatsauswertung prüft den Typ des Kategorienobjekts und der enthaltenen Begriffe vor der Zählung. Ungültige Daten erzeugen jetzt den bestehenden verständlichen `ValueError("Ein Verlaufs-Kategorienfeld ist beschädigt.")`. Fehlende Kategorien bleiben aus Gründen der Abwärtskompatibilität als leere Auswahl zulässig. Keine Reparatur und kein Überschreiben des Originalverlaufs.

## Abnahmekriterien und Nachweis
- `categories = null` oder Text: kontrollierter `ValueError` statt `AttributeError`.
- `Genres = [Objekt]` oder `[null]`: kontrollierter `ValueError` statt `TypeError`/`AttributeError`.
- Gültige Begriffe werden weiterhin gezählt; beschädigte Verlaufsdateien bleiben bytegleich.
- Isolierte lokale Vorher-Nachher-Nachstellung mit Python: zwei Testmethoden (vier Negativfälle und ein Positivfall) bestanden; die vollständige Repository- und GUI-Prüfung muss GitHub Actions am PR-Commit nachweisen.

## Restrisiko und Integration
Die Änderung betrifft nur die Monatsauswertung, nicht den gesamten Verlaufsimport. Ungewöhnliche andere beschädigte Felder sind nicht Bestandteil dieses Patches. Keine Datenmigration, keine neue Abhängigkeit, kein Spielmodul, kein Release. `MANIFEST.json` bleibt unverändert, weil kein neuer Laufzeitpfad hinzugekommen ist. `TODO.md` und `CHANGELOG.md` werden nicht parallel zu dem offenen PR #135 bearbeitet, der diese Dateien bereits ändert; die Änderung ist hier und im PR dokumentiert.
