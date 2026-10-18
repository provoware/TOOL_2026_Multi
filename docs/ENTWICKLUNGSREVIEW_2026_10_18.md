# Entwicklungsreview: Qualität, Aufwand und stetige Verbesserung

Stand: 18.10.2026 · TOOL_2026_Multi · PR #84 · Version 0.18.0 als Prüfkandidat

## Bewertung mit belastbaren Grenzen

| Bereich | Bewertung | Begründung |
|---|---|---|
| Funktionale Qualität | Gut automatisch abgesichert; reale Abnahme offen | 25 neue Modultests, atomare Speicherung, Importprüfung, Exportpfadschutz, Entwurfsschutz. Kein belegter Verlust produktiver Arbeitsdaten. |
| Oberflächenqualität | Gemessener Fehler behoben; nicht vollständig am Zielgerät geprüft | UI-Shadow von 6 Fehlern auf 0 Fehler / 0 Warnungen korrigiert; acht PR-Matrixfälle / 24 Fensterinstanzen. Neue Module haben zusätzlich eigene Qt-Tests. |
| Entwicklungseffizienz | Verbesserungsbedürftig | Späte Trennung des uncommitteten Arbeitsstands, nachträgliche GitHub-Übertragung und vermeidbare Übertragungsvorprüfungen verursachten Zusatzarbeit. |
| Qualitative Disziplin | Im Abschluss gut; zu Beginn inkonsequent | Sicherung, Datenisolation, genaue Baumprüfung und Negativtests vorhanden. Der zuerst nur lokale Abschluss entsprach nicht dem erwarteten GitHub-Endpunkt. |
| Codesparsamkeit | Gute gemeinsame Basis; gezielt weiter prüfen | Sieben neue Laufzeitdateien mit zusammen 1355 Zeilen; jede unter 500 Zeilen, keine Funktion darin über 60 Zeilen. Speicherung, Theme, Zoom und Charakterzugriff verwenden vorhandene Wege. |
| Nachvollziehbarkeit | Verbessert | Eigener PR, getrennte vorherige lokale Änderungen, SHA-zugeordnete Prüfläufe und getrennte Kennzeichnung von Implementierung, Vorschlag und realer Abnahme. |

Diese Bewertungen sind fachliche Einordnungen, keine gemessenen Schulnoten. Testanzahl und kurze Dateien beweisen allein weder Fehlerfreiheit noch gute Bedienbarkeit. Die 25 neuen Tests sind in den Gesamttestzahlen enthalten und werden nicht zusätzlich addiert.

## Tatsächliche Prüfdaten

| Nachweis | Erster PR-Stand | Korrigierter Code-/Layoutstand |
|---|---|---|
| Commit | `0ab16bf6b331084881824a3a8e2edb9d657d3639` | `cfc735316c749fd828595eead7d8c2ba60354d5d` |
| GitHub-Lauf | [#1006](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39126658141) | [#1007](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39127077853) |
| Ergebnis des CI-Jobs | erfolgreich | erfolgreich |
| Logiktests | 188 bestanden | 188 bestanden |
| GUI-Tests | 143 bestanden | 144 bestanden |
| UI-Shadow | 6 Fehler, 0 Warnungen | 0 Fehler, 0 Warnungen |
| Jobdauer nach GitHub-Zeitstempeln | 100 s | 106 s |
| Systempakete | 23 s | 24 s |
| Python-Pakete | 4 s | 4 s |
| Vollprüfung | 31 s | 32 s |
| Restore einschließlich erneuter Prüfung | 30 s | 32 s |
| Nativer Qt-Wayland-Start / Restore / ZIP | erfolgreich | erfolgreich |

Der Python-Paketcache ist in Lauf #1007 durch „Cache hit“ und „Cache restored successfully“ nachgewiesen. Die Zeitstempel der GitHub-Schritte haben begrenzte Auflösung. Zwei PR-Läufe mit unterschiedlichem Testumfang erlauben **keine Aussage über einen dauerhaften Leistungsgewinn oder eine Verschlechterung**. Sie gehören auch nicht zur früher vereinbarten Vergleichsserie aus zehn vergleichbaren erfolgreichen main-Läufen. Übertragene Bytes, Entwicklerstunden und konkrete Zeitersparnis wurden nicht gemessen.

Die abschließende Informationsrunde ergänzt diesen Bericht, Entwicklungsregeln und eine kleine Wiederverwendung im Formular. Ihr eigener CI-Nachweis steht am aktuellen Head von [PR #84](https://github.com/provoware/TOOL_2026_Multi/pull/84); die historischen Nachweise oben werden nicht nachträglich als Beleg für neuere Commits ausgegeben. So erzeugt das Nachtragen eines Prüfergebnisses keinen endlosen Evidenz-Commit-Kreislauf.

## Beobachtete Fehler und vermeidbarer Aufwand

| Beobachtung | Einordnung / Ursache | Konsequenz für künftige Arbeit |
|---|---|---|
| Zuerst lokaler Abschluss statt erwartetem GitHub-Endpunkt | Prozessfehler: Lieferweg zu spät konkretisiert | Bekannten Repository-Kontext sofort in den Arbeitsauftrag übernehmen; Branch, PR und offene Merge-Grenze zu Beginn festhalten. |
| Vorhandene uncommittete Hilfe-/Theme-Arbeit erst später vom neuen Scope getrennt | Vermeidbare Portierung und zusätzliche Prüfungen | Vor der ersten Mutation Arbeitsstand und Abhängigkeiten prüfen; neue Arbeit von Anfang an im eigenen Worktree auf festem Ausgangs-SHA durchführen. |
| Vier erfolglose Varianten, einen fehlenden Ausgabeordner anzulegen | Umgebungspfad wurde wie ein nutzbarer Ausgabeweg behandelt | Einmal Ort und Schreibbarkeit prüfen; bei strukturell fehlendem Pfad auf den tatsächlich verfügbaren Lieferweg wechseln. Keine wiederholte Rechteeskalation ohne neue Evidenz. |
| Große Textantwort vor der Übertragung abgeschnitten; danach Unicode-Längenprüfung fehlgeschlagen | Zwei fehlgeschlagene Vorprüfungen: Transportlimit und Codepunkte versus UTF-16 | Übertragungsmenge begrenzen, Unicode-sicher übertragen und den vollständigen Git-Baum vor Veröffentlichung vergleichen. Vorher keinen Remote-Ref ändern. |
| Lokaler CLI-Zugang unbrauchbar, Connector funktionierte | Unterschiedliche Authentifizierungs-/Netzwerkwege | Funktionsfähigen GitHub-Connector für diesen Arbeitsgang beibehalten; denselben unbrauchbaren CLI-Weg nicht erneut probieren. |
| Neues Hilfethema vor „Erste Schritte“ und veränderte Dashboard-Breitenverteilung | Echte lokale Nachbarregressionen | Hilfereihenfolge bewahren; Scrollcontainer anhand ihrer natürlichen Größe prüfen. Bestehende Tests nicht bloß an fehlerhafte Darstellung anpassen. |
| Beim Portieren Versionsdatei veraltet und Kachelanzahlen geändert | Dokumentations-/Testanpassung, nicht automatisch Produktfehler | Versionsangaben aus dem Manifest konsistent pflegen; neben Anzahl auch Bedeutung und Erreichbarkeit der neuen Kacheln prüfen. |
| Verworfener Buchentwurf hätte vom Timer später gespeichert werden können | Vor der Veröffentlichung erkannter Zustandsfehler | Schließen/Verwerfen plus späteren Timerlauf gezielt testen; Entwurf vor dem Verbergen wirklich verwerfen. |
| Export konnte interne Pfade als Ziel erhalten | Vor der Veröffentlichung erkannte Schutzlücke | Aufgelöste Exportziele vor jedem Schreiben prüfen; Negativtest einschließlich symbolischem Link beibehalten. |
| CI-Job grün, UI-Shadow dennoch rot | Bestehender Shadow-Modus blockiert absichtlich nicht | Semantische Evidenz zusätzlich zum Jobstatus lesen. Harte UI-Befunde vor Freigabe beheben; Prüfregeln nicht abschwächen. |
| Sechs harte Überlappungsbefunde im vorhandenen Dashboard | Zusatzbutton verdrängte Profilfelder bei 200 % / Kontrast | Redundanten Button ab 175 % ausblenden, Tastenkürzel erhalten, Rückkehr zu 100 % und Feldgeometrie absichern. |

Dies ist eine Liste beobachteter Ursachen, keine vollständige Fehlerquote aller Tool-Aufrufe. Mehrere Meldungen können dieselbe Ursache betreffen. Insbesondere waren die sechs UI-Meldungen kein Nachweis von sechs unabhängigen Programmfehlern. Wiederholte Prüfungen nach einer tatsächlichen Korrektur, der vorgeschriebene Restore-Test und die main-Abnahme sind notwendige Absicherung; vermeidbar waren vor allem die Umwege, die diese Korrekturen verspätet auslösten.

## Konkrete Codesparsamkeit in dieser Runde

Der vorhandene AST-Doppelungsprüfer fand bei Sequenzen ab vier Anweisungen 18 Kandidatengruppen im gesamten app-Ordner. Eine davon betraf die neuen Dateien: derselbe Formularreset in `discard_draft` und `new_snippet`. `new_snippet` verwendet jetzt die vorhandene Resetfunktion. Dadurch entfallen vier Laufzeit-Codezeilen ohne neue Abstraktion oder Abhängigkeit. Danach meldet der Prüfer 17 Kandidatengruppen insgesamt und keine Gruppe mit Beteiligung der sieben neuen Dateien.

Das ist **kein Nachweis vollständiger Duplikatfreiheit**: Der Prüfer erkennt identische Anweisungsfolgen, keine semantische Ähnlichkeit. Die anderen 17 Hinweise bleiben außerhalb dieses Änderungsscope und werden nicht automatisch umgebaut. Es wurden keine neuen Pflichtpakete, kein zweiter Ereignislogger und keine pauschale Neugestaltung älterer Module eingeführt. Der allgemeine Import-/Exportweg wird zunächst von den zwei neuen Modulen genutzt.

## Wie sich die Entwicklung stetig verbessern kann

Ein begrenzter Lernkreislauf pro abgeschlossener Iteration genügt:

1. **Messen:** SHA, Scope, Testanzahl, Lauf-/Schrittzeiten, Cache-Nachweis, UI-Befunde, Fehlerursachen und Änderungsumfang aus vorhandenen CI-Artefakten übernehmen. Produkt-Leistungsdaten folgen dem getrennten [Messplan](DIAGNOSE_MESSPLAN.md).
2. **Gruppieren:** Gleiche Ursachen zusammenfassen; Produktfehler, Prüfproblem, Umgebung und fehlende Berechtigung getrennt halten. Verdacht bleibt Verdacht, bis er reproduziert ist.
3. **Priorisieren:** Datenverlust-/Sicherheitsrisiko zuerst; danach häufige oder zeitraubende Probleme. Eine wiederholte Ursache bekommt Vorrang vor einem einmaligen kleinen Umweg.
4. **Eine Hypothese testen:** Beispielsweise „unveränderte Autosaves erzeugen unnötige Schreibzugriffe“ oder „ein Scrollcontainer hat die natürliche Kartenbreite verändert“. Kleine, isolierte Änderung plus konkretes Abnahmekriterium wählen.
5. **Vergleichen:** Gleiche Szenarien, Arbeitsmengen und Gates verwenden. Eine Änderung nur übernehmen, wenn ihr Nutzen belegt ist und die Nachbarwege geschützt bleiben; sonst auf dem Arbeitszweig zurücknehmen.
6. **Lernen speichern:** Ursächlichen Regressionstest, kurze übertragbare Arbeitsregel und offenen nächsten Schritt dokumentieren. Keine langen Doppelberichte und keine Wiederholung des gesamten Chats in der Projektdokumentation.
7. **Wirkung später prüfen:** Nach mehreren vergleichbaren Iterationen untersuchen, ob dieselbe Ursache seltener auftritt und der Aufwand pro abgenommenem Änderungspaket sinkt. Eine geänderte Regel allein ist noch keine belegte Verbesserung.

Vorhandene Werkzeuge verwenden: `scripts/entwicklungsmessung.py`, `scripts/code_doppelungen.py`, UI-Shadow, Restore und Manifestprüfung. Ein neues Optimierungsframework ist derzeit nicht begründet. Automatisch dürfen Berichte erzeugt, Auffälligkeiten gruppiert und Verbesserungsvorschläge vorbereitet werden. Änderungen bleiben kleine prüfbare Branch-/PR-Schritte. Qualitätsgrenzen, Datenschutz und Freigaberegeln werden nicht zur Verbesserung einer Kennzahl abgesenkt.

## Messbare Kriterien für die nächsten Iterationen

- Erfolgreicher Erstlauf **einschließlich semantischer UI-Evidenz**, getrennt von bloß grünem Jobstatus.
- Anzahl vollständiger Läufe je tatsächlich unterschiedlichem Commit; zusätzliche Läufe mit Anlass dokumentieren.
- Wiederauftreten derselben Fehlerursache und Anteil vor Veröffentlichung gefundener Probleme; ohne ausreichende Basis keine Prozentzahl behaupten.
- Prüfdauer und Installationszeiten bei vergleichbarem Umfang; mindestens die geplanten zehn erfolgreichen main-Läufe getrennt auswerten.
- Änderungsvolumen, neue Pflichtabhängigkeiten und belegte Wiederverwendung; Codezeilenzahl als Hinweis, nicht als Qualitätsziel.
- Übernahmequote von Vorschlägen und später nachgewiesene Wirkung. Nicht umgesetzte Ideen bleiben in der Warteschlange statt neue Nebenarbeiten auszulösen.

## Fünf nächste Verbesserungen

1. **Priorisierte Empfehlung:** Bei jedem neuen Auftrag zuerst Ausgangs-SHA, isolierten Scope, Lieferweg und Abnahmekriterien festhalten. Das adressiert mehrere beobachtete Umwege, insbesondere die nachträgliche Portierung und die verspätete GitHub-Übertragung.
2. Lokale UI-Shadow-Analyse vor dem ersten GUI-Push als gezielte kurze Vorprüfung nutzen.
3. CI-Lauf-/Schrittzeiten aus vorhandenen Artefakten einmal je Revision zusammenfassen; keine zusätzlichen Vollprüfungen nur für Statistik.
4. Die geplante Produktmessung zuerst auf Ladezeiten, Schreibzugriffe und unveränderte Autosaves begrenzen.
5. Doppelungs- und Funktionsgrößenprüfung nur auf neue oder geänderte Dateien richten; größere Altlasten getrennt priorisieren.

Nächster logischer Schritt: diese konsolidierte Revision einmal vollständig auf GitHub prüfen, danach die offene echte Kubuntu-Abnahme durchführen. Erwartetes Volumen: ein PR-Prüflauf, eine Bildschirm-/Zwischenablage-/Wörterbuch-Abnahmerunde und ein Ergebnisprotokoll. Keine zusätzliche Produkttelemetrie wird durch dieses Review eingeschaltet.
