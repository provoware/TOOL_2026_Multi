# Persönliche Daten sichern und zurückholen

Programm zuerst schließen. Der vollständige Inhalt aller regulären Dateien in `daten/` wird gesichert, einschließlich versteckter Versionen. Leere Unterordner werden nicht gespeichert; das Programm kann benötigte Arbeitsordner wieder anlegen. Es werden keine Nutzerdaten gelöscht oder in den laufenden Datenbestand zurückgeschrieben.

Im Projektordner:

```bash
python3 scripts/datensicherung.py sichern --daten daten --ziel /pfad/zum/zweiten/datentraeger --programm-geschlossen
```

Es entstehen ein eindeutig benanntes ZIP und eine `.zip.sha256`-Prüfsummendatei. Beide gemeinsam aufbewahren. Nach dem Schreiben prüft das Werkzeug das gesamte ZIP und stellt es probeweise in einem eigenen temporären Ordner wieder her. Nur ein erfolgreicher Abschluss bestätigt diesen Vergleich. Die Arbeitsdateien werden davor und danach verglichen; bei Veränderungen wird die Sicherung abgebrochen. Dies ersetzt keinen transaktionalen Snapshot eines gleichzeitig laufenden Programms: deshalb vorher schließen.

Die Sicherung enthält persönliche Inhalte und ist **nicht verschlüsselt**. Der Werkzeugordner ist kein Cloud-Upload. ZIP, Prüfsumme und zurückgeholte Dateien erhalten private Dateirechte. Einen geschützten Datenträger verwenden. Prüfsummen erkennen versehentliche Änderungen; sie belegen keine Echtheit gegenüber jemandem, der ZIP und Prüfsumme gemeinsam austauscht.

Zum Zurückholen:

```bash
python3 scripts/datensicherung.py wiederherstellen --archiv /pfad/Provoware_Daten_DATUM_KENNUNG.zip --neu /pfad/neuer_pruefordner
```

Der Zielordner darf noch nicht existieren; sein übergeordneter Ordner muss existieren. Das Ergebnis liegt unter `neuer_pruefordner/daten/`. Vorhandene Ordner werden auch dann abgelehnt, wenn sie leer sind. ZIP-Prüfsumme, Dateiliste, Einzelprüfsummen und Größen werden geprüft. Bei Fehlern wird nur der gerade neu angelegte Prüfordner entfernt. Das Werkzeug aktiviert die Daten nicht automatisch. Den geprüften Datenordner bei geschlossenem Programm erst bewusst übernehmen; bestehenden Bestand zuvor separat erhalten.

Grenzen: 10000 Dateien, 64 MiB pro Datei und insgesamt 512 MiB einschließlich Archivindex; keine Links, Spezialdateien, verschlüsselten oder fremden ZIP-Formate. Sicherungsziel außerhalb des Datenordners. Größenüberschreitungen werden gemeldet, nicht durch Ausschluss einzelner Arbeitsdateien umgangen. Keine automatische Rotation oder Löschung älterer Sicherungen.

Automatische Schutztests: Unicode, Binärdaten, versteckte Versionen, leerer Bestand, veränderte Quelldaten, vorhandenes Ziel, Links, Traversal, fremde Einträge, Größenlimit, fehlende/falsche Archivprüfsumme sowie falsche Einzelprüfsumme. Alle Mutationen finden in temporären Testordnern statt.


## Projekt-Notizen und ältere Bestände

Neue Projekt-Notizen liegen unter `daten/notizen/projekt-notizen.txt`. Die bestätigte Altübernahme erzeugt zusätzlich bytegenaue Dateien `daten/notizen/altbestand-<SHA-256>.txt`. Beide gehören ohne Änderung des ZIP-Formats zur regulären persönlichen Sicherung und werden isoliert unter denselben relativen Datenpfaden zurückgeholt.

Die alte `Entwicklerinformation.txt` im Projektstamm wird niemals still gelöscht, umgeschrieben oder automatisch übernommen. Vorhandene Altbestände werden im Dashboard beim Speichern einer Notiz ausdrücklich zur Übernahme angeboten. **Ja** erhält eine geprüfte Kopie; **Nein** lässt den Altbestand außerhalb des Daten-ZIPs und zeigt diese Einschränkung; **Abbrechen** erhält die aktuelle Eingabe ohne neuen Speichervorgang. Ein abgelehnter Dialog wird erst nach einem Programmneustart erneut angeboten. Vor einer vollständigen persönlichen Sicherung die gewünschte Altübernahme bestätigen oder die Originaldatei zusätzlich separat sichern.

Identischer Inhalt ergibt dieselbe Altkopie. Bei geänderter Quelldatei entsteht eine neue Kopie; vorhandene abweichende Zieldateien werden nicht überschrieben. Originalbytes, insbesondere alte Zeilenenden und unbekannte Zeichenkodierungen, bleiben in Altkopien erhalten. Automatische Zusammenführung und Aktivierung zurückgeholter Dateien finden nicht statt. Ein isolierter Restore-Test prüft neue Notizen und bestätigte Altkopien gemeinsam. Ein konfigurierter externer Laufzeit-Datenstamm wird über denselben an das Dashboard übergebenen Wurzelpfad verwendet; Programmordner werden dadurch nicht beschrieben.

Grenze: jede Notizdatei höchstens 4 MiB. Verknüpfte Notizpfade und Spezialdateien werden abgewiesen. Diese gezielten Prüfungen ersetzen nicht den separaten allgemeinen Audit zur Absicherung sämtlicher Datenpfade gegen nebenläufige Pfadaustausche (`PV-AUD-17`).

### Automatisierte Prüfung zu PV-AUD-01

Im isolierten Implementierungsstand wurden 77 gezielte und angrenzende Logik-/GUI-Prüfungen erfolgreich ausgeführt: Notizen, bestätigte Altübernahme, Datensicherung/Restore, Song-Speicherwege, Laienführung, Laufzeit-Datenwurzel, Dokumentationskonsistenz und Dashboard. Das Release-Manifest enthält weiterhin 147 gültige Betriebsdateien; `git diff --check` ist ohne Befund. Sämtliche Dateimutationen dieser Tests erfolgen in temporären Testordnern. Vollständige GitHub-Prüfung, Wayland, UI-Evidenz, Vollprojekt-Restore und ZIP-Erzeugung werden am zugehörigen PR geführt; hier wird keine reale Kubuntu-Endabnahme behauptet.
