# Iteration 38 – Fensterführung, kleine Displays und Eingabefokus

## Ausgangslage

Die reale 1920×1080-Sichtprüfung von Version 0.17.2 zeigte einen technisch funktionierenden, aber visuell unruhigen Song-Arbeitsweg: Dashboard, Songbibliothek und Songtexteditor konnten gleichzeitig übereinanderliegen. Eingabefelder verwendeten den Theme-Akzent bereits im Normalzustand, optionale Songangaben und Bibliotheksfilter beanspruchten auf kleinen Fenstern dauerhaft Höhe, und das sichtbare `&` in „Hilfe & Fehlerhilfe“ wurde von Qt als Mnemonik interpretiert.

## Umsetzung

- Öffnet die Songbibliothek einen Editor, wird die Bibliothek für diese Bearbeitungssitzung verborgen. Der Editor erhält Fokus. Nach dem Schließen des letzten Editors kehrt die Bibliothek kontrolliert zurück.
- Ein manuelles Öffnen der Bibliothek während eines sichtbaren Songeditors erzeugt kein zusätzliches Überlappungsfenster; der vorhandene Editor wird stattdessen aktiviert.
- Songeditor und Songbibliothek erhalten portable Fensterzustände in `daten/ui/fenster.json`. Gespeichert werden Normalgeometrie und Maximiert-Status, niemals Songinhalte.
- Gespeicherte Positionen werden nur übernommen, wenn noch ein sinnvoll sichtbarer Schnitt mit einem aktuellen Monitor besteht. Andernfalls wird das Fenster auf der verfügbaren Arbeitsfläche neu zentriert und begrenzt.
- Die Mindestgrößen wurden auf laptopgeeignete Grenzen reduziert. Ein reiner Geometrie-Test deckt explizit eine 1366×768-Arbeitsfläche ab.
- Songeditor: Stil, Stimme, Besonderheiten und Tags liegen in **Weitere Angaben** und werden im Kompaktmodus automatisch eingeklappt.
- Songbibliothek: Filter, Sortierung und Gruppierung liegen in einem einklappbaren Filterbereich; im Kompaktmodus bekommt die Songtabelle Vorrang.
- Der Modul-Kompaktmodus greift bei Breite unter 1180 px, Höhe unter 760 px oder ab 150 % Zoom. Ein manueller Klick kann die ausgeblendeten Angaben jederzeit wieder öffnen.
- Normale Eingabefelder haben einen neutralen Rand. Der aktive Eingabefokus verwendet den Theme-Akzent; Fehler und bestätigte gültige Zustände besitzen zentrale rote bzw. grüne Feldzustände.
- Eingabehintergründe wurden abgedunkelt und Platzhalterfarben explizit kontrastreich definiert.
- „Hilfe & Fehlerhilfe“ verwendet intern `&&`, damit Qt tatsächlich ein einzelnes sichtbares `&` zeichnet. Der Screenreader-Name bleibt wörtlich „Hilfe & Fehlerhilfe“.

## Sicherheitsgrenzen

Song-, Profil-, Todo- und Kalenderformate bleiben unverändert. Die neue Fensterdatei enthält ausschließlich Zahlenwerte für Position/Größe und einen Maximiert-Schalter. Ein Schreibfehler der Fensterdatei blockiert weder Speichern noch Schließen. Ungültige oder nicht mehr sichtbare Geometrie wird ignoriert statt blind wiederhergestellt.

## Regression

Neue GUI-Regressionen prüfen den 1366×768-Geometrie-Clamp, Kompaktmodus nach Höhe/Zoom, Bibliothek→Editor→Bibliothek-Fokusfluss, portable Fensterzustände ohne Songdatei-Nebeneffekt, neutrale Fokus-/Statusfarben und die Qt-Escapierung des Hilfe-Ampersands. Die bestehende automatische Testentdeckung nimmt diese Tests ohne zusätzliche Shell-Testliste auf.

## Erster technischer Gate und Korrektur

Der erste vollständige PR-Gate **#795** bestätigte alle **113 Logik-/Regressionstests** sowie ein gültiges Release-Manifest mit **48 Betriebsdateien**. Von **83 GUI-Tests** waren 81 grün; genau zwei Screenreader-Prüfungen blockierten die Freigabe. Ursache war kein Funktions- oder Fensterfehler, sondern die zentrale Accessibility-Bereinigung: Bei direkt erzeugten Dashboard-Fenstern blieb der interne Qt-Text `ⓘ Hilfe && Fehlerhilfe` als zugänglicher Name erhalten.

Die Ursache wurde zentral in `_clean_accessible_text()` korrigiert: `&&` wird für Hilfstechnologien zu einem einzelnen `&` normalisiert und das Info-Symbol `ⓘ` wie die übrigen Navigationssymbole entfernt. Dadurch bleibt die sichtbare Qt-Escapierung korrekt, während der Screenreader wörtlich **„Hilfe & Fehlerhilfe“** erhält. Die Prüfung wurde nicht abgeschwächt.

Weil der erste Gate bei den zwei GUI-Regressionen stoppte, wurden Wayland-Smoke, Restore und ZIP-Erzeugung dort bewusst **nicht** ausgeführt. Erst ein nachfolgender vollständig grüner Gate darf als technische Freigabeevidenz gelten.

## Abnahme

Der erneute vollständige CI-/Wayland-/Restore-/ZIP-Gate auf dem korrigierten Iteration-38-Head ist noch ausstehend. Eine reale Sichtprüfung auf Kubuntu 26.04 / Plasma Wayland bleibt zusätzlich erforderlich, besonders bei 1366×768 und 125/150/175/200 %.
