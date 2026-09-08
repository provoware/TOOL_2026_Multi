# Iteration 4 – Recovery, Prozesswache und Log-Datenschutz

## Restore-Gate
`scripts/iteration_restore.py` erzeugt ein Vollprojekt-ZIP ohne `.git`, `.venv`, Logs, Berichte, Backups, Release- und Cache-Daten. Anschließend werden SHA-256 und ZIP-Struktur geprüft. Entpackt wird ausschließlich in einen neuen Ordner. Erst nach identischem Manifest, `scripts/pruefen.sh --full` und `app.main --headless-check` entsteht `restore_status: OK`.

## Headless-Start
Der Headless-Weg lädt Manifest und Textregistrierung sowie den realen Programmeinstieg, erzeugt aber kein Tk-Fenster und keine Laufzeitlogs. GUI-Importe erfolgen erst im normalen Startpfad.

## Prozesswache
`scripts/process_watch.py` ist ein separater Elternprozess. Ein Rückgabecode ungleich 0 oder ein Signalabschluss erzeugt einen Wächterbericht. Damit können auch harte Abbrüche erfasst werden, die der Kindprozess selbst nicht mehr protokollieren kann.

## Log-Bereinigung
`app/redaction.py` wird vor Persistierung und vor dem Regression-Lernen angewendet. Bereinigt werden typische Secret-Zuweisungen, Bearer-Tokens, Mailadressen und Linux-Home-Benutzernamen. Die Tests stellen sicher, dass die Beispielgeheimnisse weder JSONL, TXT-Bericht noch Rückfallzustand erreichen.
