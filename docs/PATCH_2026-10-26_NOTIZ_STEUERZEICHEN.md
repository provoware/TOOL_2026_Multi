# Patchnachweis – Projekt-Notizen: Steuerzeichen abweisen (26.10.2026)

**Scope:** ausschließlich die Schnelleingabe des Nicht-Spiel-Tools `TOOL_2026_Multi`; keine Spiele und keine Tool-Zentrale.

## Befund und Nutzen
Die Notiz-Schnelleingabe übernahm bislang unsichtbare Steuerzeichen (z. B. NUL, Tabulator und DEL) in die dauerhaft gespeicherte UTF-8-TXT-Datei. Das kann Anzeige, Suche und Weiterverarbeitung stören. Bestehende Notizen sollen unverändert bleiben, wenn eine Eingabe unzulässig ist.

## Änderung und Abnahme
- Nach der bestehenden Mehrzeilen-Normalisierung werden C0-Steuerzeichen (U+0000–U+001F) und DEL (U+007F) vor jedem Dateizugriff mit einer verständlichen Fehlermeldung zurückgewiesen.
- Leere Eingaben bleiben verboten; normale mehrzeilige Eingaben werden weiterhin als eine Zeile gespeichert.
- Rückfalltest prüft NUL, Tabulator, DEL, unveränderte Bestandsbytes und zulässige Mehrzeileneingabe.

## Nachweis
- Vor dem Patch: isolierter Test mit derselben Funktion und einem atomaren Ersatzschreiber zeigte drei fehlschlagende Unterfälle für NUL, Tabulator und DEL.
- Nach dem Patch: zwei isolierte Testmethoden erfolgreich; Syntaxprüfung der betroffenen Python-Dateien erfolgreich.
- **Nicht nachgewiesen:** komplette Repository-Tests, echte GUI-/Wayland-Abnahme und vollständiger Release-/Manifest-Test. Dafür die GitHub-CI am endgültigen PR-Commit auswerten; bis dahin Entwurf.

## Restrisiko / Freigabe
Eingaben mit Steuerzeichen, die zuvor gespeichert werden konnten, werden künftig ausdrücklich abgewiesen. Bereits gespeicherte Notizen werden weder verändert noch bereinigt. Keine Datenmigration und keine Änderung des Dateiformats. Die gemeinsamen Dateien `CHANGELOG.md`, `TODO.md` und `MANIFEST.json` bleiben wegen parallelem PR #135 unangetastet; Dokumentationsabgleich erst konfliktfrei bei Integration durchführen. Kein automatischer Merge.
