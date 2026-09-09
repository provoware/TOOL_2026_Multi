# Iteration 20 – Repository-Hygiene

Stand: 2026-09-09

## Hauptziel

Das GitHub-Repository von eindeutig lokalen bzw. reproduzierbaren Artefakten bereinigen und denselben Müll künftig automatisch aus dem Versionsstand fernhalten, ohne Produktlogik oder Nutzerdaten zu verändern.

## Befund

- Der rekursive `main`-Baum enthielt keine versionierten Logs, ZIPs, Backups, `.pyc`, `__pycache__`, Tempdateien oder virtuelle Umgebungen.
- Im Repository-Root lag genau ein auffälliges Fremdartefakt: `ChatGPT Image 8. Sept. 2026, 02_16_14.png` mit 2.056.107 Bytes.
- Für diese Datei wurde keine Referenz im aktuellen Quell- oder Dokumentationsbestand gefunden.
- PR #2 stammt aus einem deutlich älteren Projektstand, ist nicht mergebar und durch die inzwischen integrierte Struktur/UI-/Regression-Entwicklung überholt.

## Änderung

1. Unreferenziertes 2,05-MB-Root-Bild aus dem Iterationsbranch entfernt.
2. `.gitignore` um typische unsortierte lokale Bildexporte im Repository-Root ergänzt; bewusst keine globale PNG-Sperre eingeführt.
3. `tests/test_repo_hygiene.py` ergänzt. Der Test prüft nur versionierte Dateien und meldet:
   - Laufzeit-/Ausgabeordner im Git-Bestand,
   - typische lokale/temporäre Dateien,
   - unsortierte ChatGPT-/Screenshot-Dateien im Root,
   - einzelne Root-Dateien über 1 MB.
4. Die bestehende Vollprüfung führt den Hygiene-Test automatisch mit aus.

## Schutzgrenzen

- Keine Nutzerdaten verändert oder gelöscht.
- Keine Anwendungs-, Speicher-, Backup-, Restore- oder UI-Fachlogik verändert.
- Keine pauschale Bilddatei-Sperre: bewusst gepflegte Assets können weiterhin in passenden Unterordnern versioniert werden.
- Branch-Bereinigung außerhalb des vorhandenen Connector-Funktionsumfangs wird nicht durch erzwungene Ref-Manipulation ersetzt.

## Abnahme

Gezielte Abnahme:

```bash
python3 -m unittest tests.test_repo_hygiene
```

Vollprüfung und Restore-Gate:

```bash
bash scripts/pruefen.sh --full
python3 scripts/iteration_restore.py
```

Der Iterationsbranch darf erst nach grünem GitHub-Actions-Gate gemergt werden. CI-/Restore-Evidence wird nach Abschluss ergänzt.
