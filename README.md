# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern · **Version:** 0.4.0 · **Stand:** 2026-09-08

## Iteration 4 – Recovery-Härtung

Der Entwicklungsunterbau besitzt jetzt vier zusätzliche Schutzschichten:

| Bereich | Status | Nachweis |
|---|---|---|
| Vollprojekt-Restore | 🟢 | ZIP → SHA-256 → neuer Ordner → Manifest → Vollprüfung → Headless-Start |
| Headless-Start | 🟢 | `python3 -m app.main --headless-check` ohne Fenster |
| Prozesswache | 🟢 | separater Elternprozess erkennt fehlerhaften/harten Prozessabschluss |
| Log-Datenschutz | 🟢 | Geheimnisse, Mailadressen und Benutzeranteile in Home-Pfaden werden vor Persistierung bereinigt |
| Startführung | 🟢 | sechs echte Checkpoints inklusive Headless- und Wächterstufe |

## Start

```bash
bash schnellstart.sh
```

Der Start prüft Python, Umgebung, Abhängigkeiten, Laufzeitkern und Headless-Start. Erst danach wird die Anwendung unter der separaten Prozesswache geöffnet.

## Vollprüfung

```bash
bash scripts/pruefen.sh --full
```

## Verifizierte Iterationssicherung

```bash
bash scripts/backup_erstellen.sh
```

Das Sicherungsskript ruft den Restore-Prüfer auf. Ein Stand wird nur als `OK` bewertet, wenn die Prüfsumme stimmt, das ZIP sicher in einen neuen Ordner entpackt wurde, das Manifest identisch ist, die Vollprüfung besteht und der Headless-Start grün ist.

Direkter Aufruf:

```bash
python3 scripts/iteration_restore.py
```

## Datenschutz im Log

`app/redaction.py` bereinigt sensible Muster zentral **vor** JSONL-/TXT-Ausgabe und vor dem Rückfalllernen. Dazu gehören insbesondere Passwort-/Token-/Secret-/API-Key-Werte, Bearer-Tokens, Mailadressen und der Benutzername in `/home/<name>`.
