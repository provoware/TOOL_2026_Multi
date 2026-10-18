# Iteration 42 – Dashboard-Layout aus Issue #86

Stand: 18.10.2026 · Version 0.18.2 · TOOL_2026_Multi / provoware/TOOL_2026_Multi

## Ziel, Basis und eingefrorener Plan

Ein Hauptziel: die 24 Fehler und acht Warnungen aus [Issue #86](https://github.com/provoware/TOOL_2026_Multi/issues/86) beheben. Basis ist der nach ausdrücklicher Freigabe gemergte und technisch geprüfte Main `526a423f484a9ef045643d30dc8e908cbed35d09`, Quellbaum `5d06e5523b49d5e68fd5e38031a3c40e2b6a1438`. Isolierter Git-Arbeitsbereich mit lokalem Sicherungscommit desselben Quellbaums; vorhandene Nutzerarbeiten bleiben unberührt.

1. Geometrie und originale CI-Warnungen bestimmen.
2. Kleinste Layoutkorrektur und reproduzierende GUI-Tests.
3. Vollständige Matrix, Vollprüfung, Informationstexte und ein konsolidierter GitHub-Commit.

Keine Änderungen an Nutzerdaten, Speicherung, Diagnose-Messlogik oder Prüfgrenzen. Kein neues Framework, keine zusätzliche Bibliothek.

## Ursache und endgültige Korrektur

**CONFIRMED:** Bei 1600×900 / 100 % erhielt die Vorgabenkarte nur 234 Pixel Höhe, benötigte mit den vorhandenen Auswahlfeldern aber 300 Pixel. Der bisher nur ab 125 % genutzte höhere Kompakt-Grenzwert wird nun bei allen Zoomstufen angewendet. Zusätzlich reservierte die ausgeblendete zweite Rasterzeile wegen ihres Stretch-Faktors weiterhin Höhe. Ihr Faktor ist nun null, solange die Planungskarten ausgeblendet sind, und wird beim Vergrößern wiederhergestellt. Die vorhandene Höhen-Grenze 860 bleibt erhalten; es gibt keinen neuen Grenzwert.

Die acht originalen GitHub-Warnungen betreffen ausschließlich das Sidebar-Label „Textbaustein-Buttons“ bei 150 % auf 1600×900 und 1920×1080 in jeweils vier Farben. Dort steht nun wie bei den übrigen kompakten Menüeinträgen „Textbuttons“. Der vollständige zugängliche Name und dieselbe Aktion bleiben erhalten; bei 100 % kommt die volle Beschriftung zurück.

Zwei neue GUI-Regressionen prüfen konkrete Überschneidungsfreiheit, Mindesthöhe, wiederholtes Verkleinern/Vergrößern, Wiederherstellung der Planungskarten sowie die Breite und den zugänglichen Namen des Menüeintrags. Der Layouttest schlug am unveränderten Ausgangsstand reproduzierbar fehl.

## Prüfnachweis und Grenzen

Lokale Vollprüfung: **200 Logiktests, 150 GUI-Tests, 67 freigegebene Betriebsdateien und Headless-Start erfolgreich**. Die gezielte Nachbarprüfung bestand 29 Tests. Lokale vollständige Release-Matrix: **60 Fälle, 180 Fenster, 0 Fehler, 0 Warnungen**. Prüfungen und Grenzwerte sind unverändert. Finale Vollprüfung sowie PR-/Wayland-/Restore-/ZIP-Nachweise werden am finalen GitHub-Head geführt und nicht aus älteren Ständen übernommen.

Die reale Kubuntu-/Plasma-Bedienung bleibt offen. Eine automatisierte Geometrieprüfung ersetzt keine sichtbare Zielrechner-Abnahme.

## Effizienz und Fehlerdisziplin

Der erste Ansatz berücksichtigte den natürlichen Kartenbedarf und reagierte auf zusätzliche Layout-Ereignisse. Er bestand gezielte Tests, störte aber im vollständigen Raster die Reihenfolge bestehender Laptop-Anpassungen. Die Matrix erkannte dies: zunächst vier neue Überlappungen und zwölf Warnungen; eine zwischenzeitliche Vereinheitlichung der Label-Zuständigkeit beseitigte die Warnungen, aber nicht die vier Überlappungen. Dieser Ansatz wurde vollständig zurückgenommen. Der endgültige Patch nutzt vorhandene Regeln und ist deutlich kleiner. Keine dieser Zwischenlösungen wurde nach GitHub übertragen.

Lehre: Bei mehreren Präsentations-Controllern zunächst vorhandene Platzverteilung und Ereignisreihenfolge prüfen. Ein gezielter grüner Test genügt bei Darstellungsänderungen nicht als vollständige Abnahme. Die zusätzlichen Matrixläufe hatten jeweils eine konkrete neue Änderung als Anlass; der verworfene Ansatz bleibt als unnötiger Entwicklungsaufwand dokumentiert. Keine pauschale Effizienzsteigerung oder Qualitätsnote ohne belastbare Vergleichsbasis.

Bestehende große UI-Dateien wurden bewusst nicht nebenbei aufgeteilt; die wenigen zielgerichteten Zeilen vermeiden ein zusätzliches Wartungsrefactoring in dieser Fehlerkorrektur.

## Fortschritt und nächste Iteration

Umsetzung: **2 von 2 Befundgruppen korrigiert** (`██████████`). Abnahme: lokale Matrix bestanden; finaler GitHub-Nachweis gehört zum PR. Externe Zielrechner-Abnahme weiterhin offen. Änderungsvolumen und ZIP-Links stehen am finalen PR.

Fünf Folgevorhaben:
1. **Priorisierte Empfehlung:** reproduzierbaren Zielrechner-/Overhead-Benchmark für die freiwillige Leistungsdiagnose erstellen.
2. Reale Kubuntu-/Plasma-Abnahme einschließlich Zwischenablage und Wörterbuch abschließen.
3. Kalt-/Warmstart und feste Datenmengengruppen getrennt messen.
4. Nur vorhandene app-eigene Caches messen und begrenzen.
5. Fehlerwiederholungen und Prüfläufe je abgenommenem Paket über vergleichbare Iterationen bewerten.

Nächster Entwicklungsauftrag: ein kleines Benchmarkscript mit dokumentierten Messbedingungen, voraussichtlich wenige Entwicklerdateien ohne zusätzliche Abhängigkeit. Kein neues Nutzermodul und keine Erweiterung des laufenden Layoutauftrags. Lernkreislauf: reproduzierbarer Befund → minimale Korrektur → passende Regression → vollständige relevante Matrix → belegtes Ergebnis.
