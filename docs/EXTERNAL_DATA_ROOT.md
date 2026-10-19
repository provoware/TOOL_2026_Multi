# Getrennte Nutzerdaten – kontrollierter Start (Entwicklungsstand 67)

Der normale Provoware-Schnellstart bleibt **unverändert benutzbar**, wenn keine zusätzliche Einstellung gesetzt ist.

Für vorbereitete Programm-Slots lässt sich die Umgebungsvariable `PROVOWARE_DATA_ROOT` auf einen eigenen Datenordner setzen. Der Start prüft dort einen Migrationsmarker, die Existenz von `daten/`, die Unabhängigkeit vom Programmordner und den erlaubten Schema-Vertrag. Fehlt eine Bedingung, wird der Start verweigert. Die aktuelle Kopierprobe erzeugt diesen Marker im neuen persönlichen Datenordner; das bisherige Programm und seine Daten werden nicht verändert.

Der Einstieg `scripts/managed_start.py` nimmt ausschließlich eine **bereits ausdrücklich aktivierte** verwaltete Installation mit `current → slots/<Version>` an. Ein unbestätigter Wechsel wird beim Start auf den alten Slot zurückgenommen; der Schnellstart wird unter Sperre gegen parallele Versionswechsel ausgeführt. Versagt eine als neu aktivierte Version, wird der alte Versionszeiger wiederhergestellt. **Persönliche Dateien werden dabei weder gelöscht noch durch ältere Datenstände ersetzt.**

Die vorliegende neue Kopierprobe bleibt absichtlich **ohne** aktiven `current`-Zeiger. Es existiert noch kein produktiv freigegebener Assistent, der den regulären alten Start durch das neue Verfahren ersetzt. Das erfordert einen gesonderten Freigabevertrag einschließlich Daten-/Versionstests und der einmaligen Kubuntu-Gesamtabnahme am Projektende.

Vor der Freigabe bleiben auch Tests auf Datenformatänderungen zwischen Versionen und ein vollständiger Weg für die sichere Aktualisierung gemeinsam genutzter Daten erforderlich.
