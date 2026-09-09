# Iteration 22 – Responsive Design und visuelle Härtung

## Hauptziel

Das bereits laienfreundlich strukturierte Provoware-UI wird auf Grundlage der realen Kubuntu-Screenshots visuell und dynamisch gehärtet. Schwerpunkt sind Lesbarkeit, moderne Hierarchie, flexible Breiten, nutzbare Tabellen und gleichmäßige Abstände. Daten- und Speicherlogik bleiben unverändert.

## Befund aus den realen Screenshots

- Die Oberfläche ist funktional klar, wirkt aber durch viele gleich starke orange Rahmen optisch unruhig.
- Die verwendete Schrift wirkt auf dem Zielsystem teilweise serifartig und relativ klein.
- Feste Breiten führen bei Navigation, Songbereichsliste und Kopfzeile zu unnötigem Abschneiden.
- Die Songbibliothek nutzt die große freie Tabellenbreite nicht optimal; mehrere Spalten werden zu früh gekürzt.
- Splitter und Scrollleisten sind funktional, aber visuell schwach und schwerer greifbar.
- Der frühere GUI-Test verlangte nahezu identische Kartenbreiten und widersprach damit einer sinnvollen dynamischen Inhaltsanpassung.

## Umsetzung

- Zentrale Palette modernisiert: dunklere, ruhigere Flächen; Amber nur noch als gezielter Akzent; Cyan als gut sichtbarer Fokus.
- Explizite systemweite Sans-Serif-Schrift gesetzt, ohne zusätzliche Font-Abhängigkeit.
- Schrift-Hierarchie, Innenabstände, Rundungen, Eingabehöhen und Fokusrahmen zentral vereinheitlicht.
- Karten verwenden neutrale Konturen statt flächendeckender orangefarbener Rahmen.
- Aktive Navigation erhält eine moderne dunkle Auswahlfläche mit linker Akzentlinie.
- Geplante Funktionen bleiben bewusst gestrichelt und visuell nachrangig.
- Responsive Breitenstufen eingeführt: kompakt unter 1100 px, normal ab 1100 px, breit ab 1450 px.
- Dashboard-Navigation und Song-Suchfeld passen ihre Breite an die Fenstergröße an.
- Profilfelder und Beschriftungen werden abhängig vom verfügbaren Platz kompakter oder großzügiger.
- Songeditor-Splitter passt Arbeitsbereich und Gesamtvorschau dynamisch an; Songbereichsliste erhält passende Breite und bei Bedarf horizontales Scrollen.
- Songbibliothek verteilt Tabellenbreite gezielt: Titel und Tags wachsen mit, kurze Status-/Datumsfelder bleiben inhaltsbezogen.
- Splitter, Tabellenköpfe, Tabs und Scrollleisten visuell modernisiert und besser greifbar gemacht.

## Regression aus Iteration 21

GitHub-Grundprüfung Run #368 zeigte nach dem bereits erfolgten Merge von PR #23 drei GUI-Rückfälle:

1. neuer Laien-UX-Test erwartete das Wort `Song` im Suchplatzhalter;
2. alter Recovery-Test erwartete noch die frühere Beschriftung `Recovery`;
3. alter Referenztest verlangte Kartenbreiten mit weniger als 35 px Abweichung und blockierte damit responsive Inhaltsverteilung.

Iteration 22 korrigiert ausschließlich diese veralteten Erwartungen beziehungsweise die zu starre Layoutannahme und ergänzt echte Responsive-Regressionen. Die 75 Logiktests des fehlgeschlagenen Laufs waren bereits vollständig grün; das Restore-Gate wurde wegen des GUI-Testfehlers nicht gestartet.

## Schutzgrenzen

- keine Datenmigration,
- keine Änderung an Song-, Todo-, Kalender- oder Profildaten,
- keine Änderung am atomaren Schreibweg,
- keine Änderung an Backup-/Restore-Fachlogik,
- keine neue Produktfunktion,
- keine externen Fonts oder zusätzlichen Abhängigkeiten.

## Automatische Abnahme

Der finale Branch muss vor Merge vollständig bestehen:

```bash
bash scripts/pruefen.sh --full
```

Zusätzlich muss das bestehende Vollprojekt-Restore-Gate erfolgreich sein. Die reale Kubuntu/KDE-X11-Sichtabnahme bleibt danach der verbindliche letzte visuelle Nachweis auf dem Zielrechner.
