# Iteration 20 – Repository-Hygiene

Stand: 2026-09-09

## Hauptziel

Das GitHub-Repository von eindeutig lokalen bzw. reproduzierbaren Artefakten bereinigen und denselben Müll künftig automatisch aus dem Versionsstand fernhalten, ohne Produktlogik oder Nutzerdaten zu verändern.

## Befund

- Der rekursive `main`-Baum enthielt keine versionierten Logs, ZIPs, Backups, `.pyc`, `__pycache__`, Tempdateien oder virtuelle Umgebungen.
- Im Repository-Root lag genau ein auffälliges Fremdartefakt: `ChatGPT Image 8. Sept. 2026, 02_16_14.png` mit 2.056.107 Bytes.
- Für diese Datei wurde keine Referenz im aktuellen Quell- oder Dokumentationsbestand gefunden.
- PR #2 stammte aus einem deutlich älteren Projektstand, war nicht mergebar und durch die inzwischen integrierte Struktur/UI-/Regression-Entwicklung überholt.
- Zwei ältere Branches sind noch vorhanden: `iteration-18-output-consistency` ist gegenüber `main` divergiert; der alte Codex-Branch liegt 20 Commits hinter `main`. Eine sichere Branch-Löschung wird mit dem verfügbaren Connector nicht erzwungen.
- `README.md` weist noch den älteren Stand 0.13.1 aus; diese reine Dokumentationsabweichung wurde bewusst nicht in den Hygiene-Patch gemischt.

## Änderung

1. Unreferenziertes 2,05-MB-Root-Bild entfernt.
2. `.gitignore` um typische unsortierte lokale Bildexporte im Repository-Root ergänzt; bewusst keine globale PNG-Sperre eingeführt.
3. `tests/test_repo_hygiene.py` ergänzt. Der Test prüft im echten Git-Checkout nur versionierte Dateien und meldet:
   - Laufzeit-/Ausgabeordner im Git-Bestand,
   - typische lokale/temporäre Dateien,
   - unsortierte ChatGPT-/Screenshot-Dateien im Root,
   - einzelne Root-Dateien über 1 MB.
4. Die bestehende Vollprüfung führt den Hygiene-Test automatisch mit aus.
5. PR #2 als überholt geschlossen; kein alter Code wurde übernommen.

## Restore-Rückfall und ursächlicher Fix

Die erste Grundprüfung #335 zeigte keinen Produktfehler. `bash scripts/pruefen.sh --full` war bereits erfolgreich, aber das anschließende Restore-Gate scheiterte, weil `tests/test_repo_hygiene.py` auch im entpackten Restore `git ls-files` aufrief. Ein wiederhergestelltes Versions-ZIP enthält absichtlich kein `.git`.

Der kleinste ursächliche Fix begrenzt deshalb ausschließlich den Git-spezifischen Hygiene-Test: Fehlen Git-Metadaten, wird nur dieser Test als im Restore nicht anwendbar übersprungen. Vollprüfung, Manifestvergleich, ZIP/SHA-Prüfung, Headless-Start und das eigentliche Restore-Gate bleiben unverändert aktiv.

## Schutzgrenzen

- Keine Nutzerdaten verändert oder gelöscht.
- Keine Anwendungs-, Speicher-, Backup-, Restore- oder UI-Fachlogik verändert.
- Keine pauschale Bilddatei-Sperre: bewusst gepflegte Assets können weiterhin in passenden Unterordnern versioniert werden.
- Branch-Bereinigung außerhalb des vorhandenen Connector-Funktionsumfangs wurde nicht durch erzwungene Ref-Manipulation ersetzt.

## Abnahme / Evidence

- Grundprüfung #335: Vollprüfung grün, Restore-Gate wegen des Git-Kontextfehlers rot.
- Korrigierter Head: `caefca0d51b158ac9a3c8cfedc6fb18e0899a580`.
- Grundprüfung #337: **success**.
- Schritt `Vollständige Grundprüfung ausführen`: **success**.
- Schritt `Vollprojekt wiederherstellen und prüfen`: **success**.
- PR #21 wurde danach per Squash-Merge in `main` übernommen.
- resultierender Main-Commit: `aa66dc5ed106e470a533c4dd9f65cf80b726b05c`.

Damit ist der Repository-Hygiene-Patch einschließlich Regression und Restore-Nachweis abgeschlossen. Der Status-Sync enthält ausschließlich Dokumentations-/Manifest-Nachführung.
