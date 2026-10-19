# Eigenständig startbare, geprüfte Migrationskopie – Entwicklungskandidat

Die bestehende Installation wird **niemals** automatisch überschrieben. Erst wird mit der vorhandenen geschützten Migrationskopie eine getrennte Verzeichnisstruktur erzeugt: `slots/base` enthält den Programmcode; `persistent/daten` enthält eine unabhängige Kopie der persönlichen Daten. Das bisherige Programm bleibt am alten Ort startbar.

Danach kann eine ausdrücklich freigegebene Aktion `activate_independent_copy(neue_kopie, approved=True)` eine zusätzliche, eigenständige Startdatei erzeugen. Vorher werden Migrationsbericht, Datenmarker, Startfähigkeit der Programmversion und der Headless-Programmstart überprüft. Nur bei vollständigem Erfolg entstehen innerhalb **der neuen Kopie** `current → slots/base` und `verwaltet_starten.sh`. Beschädigte oder ungeeignete Kopien werden nicht aktiviert. Ein Fehlschlag löscht ausschließlich die eventuell neu angelegten Zeiger und Starter; persönliche Daten und das alte Programm bleiben erhalten.

Beim Start der neuen Kopie nutzt der verwaltete Schnellstart den getrennten Datenordner. Ein Versionsfehler nach einer späteren geprüften Aktualisierung darf nur auf den letzten intakten **Programm**-Slot zurückschalten; Daten dürfen niemals in eine ältere Fassung zurücküberschrieben werden.

**Noch nicht freigegeben:** automatische Ersetzung des bestehenden Kubuntu-Startsymbols, Datenformatänderungen zwischen alten und neuen Programmversionen sowie ein öffentliches Release. Die komplette manuelle Endabnahme bleibt vereinbarungsgemäß bis zum Abschluss aller Module zurückgestellt.
