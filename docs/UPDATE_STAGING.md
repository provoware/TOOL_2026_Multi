# Update-Staging: getrennt prüfen, noch nicht aktivieren

Version 0.18.4-Prüfkandidat · Iteration 50 · Basis b3272f7.

Das Werkzeug prüft Runtime-ZIPs aus dem vorhandenen Release-Builder. Vollprojekt-ZIPs, persönliche Daten und Dateien außerhalb des freigegebenen Runtime-Manifests werden nicht akzeptiert. Die Paket-Prüfsumme muss aus einer unabhängig vertrauenswürdigen Quelle stammen; ein gemeinsam mit einem manipulierten ZIP ausgetauschter Hash beweist keine Echtheit. Signaturprüfung und aktive Installation sind noch nicht implementiert.

1. Ausgangsmanifest und gewünschte Paket-Prüfsumme bestimmen.
2. Archiv struktur-, größen-, versions- und identitätsbezogen prüfen.
3. In einen eigenen Ordner außerhalb des aktiven Projekts entpacken, Inhalte nachprüfen und statischen Prüfbericht erzeugen.

Beispiel, im Projektordner:

```bash
sha256sum MANIFEST.json
python3 scripts/update_staging.py --root . --archiv /pfad/update.zip --sha256 VERTRAUENSWUERDIGER_PAKETHASH --basis-sha256 ANGEZEIGTER_MANIFESTHASH --staging-parent /pfad/vorhandener_getrennter_ordner
```

Der übergeordnete Staging-Ordner muss existieren und vollständig außerhalb des aktiven Projektordners liegen. Jeder Aufruf reserviert einen neuen privaten Unterordner. Vorhandene Kandidaten werden nicht überschrieben; Fehler entfernen nur den vom Aufruf angelegten Ordner. Arbeitsdaten und aktive Programmdateien bleiben erhalten.

Geprüft werden SHA-256 des kopierten Archivs, Ausgangsmanifest vor/nach der Prüfung, Programm-/Repositoryidentität, streng neuere numerische Version, vollständige und exakte Runtime-Dateiliste, Pfadsicherheit, Dateitypen, Dateigrößen und CRC. Nach dem Entpacken werden die tatsächlich geschriebenen Bytes mit den während des Entpackens berechneten Hashes verglichen. Python wird nur mit dem vertrauenswürdigen Parser als Syntax gelesen; JSON wird geparst. Abhängigkeiten müssen feste Paketversionen ohne URLs oder Installationsoptionen enthalten.

Grenzen: ZIP bis 32 MiB, 1000 Dateien, 8 MiB je entpackter Datei und 64 MiB Gesamtinhalt. Keine Links, Spezialdateien, doppelte/kollidierende Pfade, verschlüsselten Einträge, Traversal, Arbeitsdaten oder versteckten Projektinternas. Ausführungsbits werden nur als private Eigentümerrechte übernommen; Sonderbits nicht übernommen.

`stage-report.json` nennt den Status **STATICALLY_VERIFIED_NOT_ACTIVATABLE**, Basis-/Paket- und Einzeldateihashes sowie statisch geprüfte Dateien. `activation_allowed` bleibt falsch, `candidate_code_executed` falsch und `runtime_tests` ausdrücklich NOT_RUN. Der Bericht ist kein vertrauenswürdiges Aktivierungsticket und darf von einem späteren Installer nicht ungeprüft übernommen werden.

Nicht enthalten: Ausführung von Paketcode, Netzinstallation, aktive Programmumschaltung, Produktivbackup, Rollback oder eine bestandene Laufzeitprüfung des Kandidaten. Vor späterer Aktivierung sind eine echte isolierte Ausführungsumgebung, vertrauenswürdige Herkunft, Checkpoint, vollständige Laufzeitprüfung und atomare Umschaltung mit Rückfallweg erforderlich.

Elf Schutztests prüfen falsche Paket-/Basis-SHAs, Versionsrückschritte, fremde Identität, Traversal, Datenpfade, Links, unerwartete/fehlende/kollidierende Dateien, Syntaxfehler, Installationsoptionen, Größenlimits, fehlgeschlagenes Berichtsschreiben und Änderung der Basis während der Prüfung. Ein Paket mit ausführbarem Sentinel-Code beweist, dass dieser nicht ausgeführt wird. Alle Mutationen erfolgen in temporären Testbereichen.

## Optionale Laufzeitprobe im getrennten Linux-Namensraum

Zusätzlich zur statischen Prüfung ist jetzt eine *optionale, verweigernde* Laufzeitprobe verfügbar. Sie darf nur bereits unverändert geprüfte Kandidaten testen. Benötigt wird `bubblewrap` (`bwrap`) mit funktionierenden Benutzer-/Netz-/Dateinamensräumen. Ohne diese Voraussetzungen wird **kein Kandidat gestartet**; die Anwendung installiert nichts automatisch.

`python3 scripts/update_sandbox.py --root . --staging /pfad/zum/provoware-update-ordner`

Die Probe startet ausschließlich im getrennten Namensraum, bindet den Kandidaten nur lesend ein, hat kein eingebundenes HOME/Projekt-/Datenverzeichnis und keinen Netzwerkzugriff. Sie führt ausschließlich den schon vorhandenen Headless-Programmeinstieg des Kandidaten aus. Fehler, abweichende Prüfsummen und Zeitüberschreitung blockieren den Lauf. Der Bericht `sandbox-report.json` ist **kein Aktivierungsticket**: `activation_allowed=false` bleibt immer bestehen. Ein echter Sicherheitsnachweis gegen bösartigen Kernel-Code oder ein vollständiger GUI-/Regressionstest ist dies nicht. Ein künftiger Update-Installer benötigt weitere unabhängige Schutzschritte; Rückkehr zur alten Version und Produktiv-Checkpoint fehlen weiterhin.

## Nachfolgende Programmsicherung

Nach erfolgreichem statischem Staging ist eine gesonderte **reine Programmsicherung** möglich. Sie erstellt eine Checkpoint-Kopie ausschließlich der freigegebenen Betriebsdateien und kann sie in einen neuen, isolierten Rückkehrordner übertragen. Das ersetzt weder die persönliche Datensicherung noch eine Aktivierung und kann das laufende Programm nicht überschreiben. Anleitung und Grenzen: [Programmsicherung](UPDATE_CHECKPOINT.md).
