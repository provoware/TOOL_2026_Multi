# Iteration 13 – Zoom und Schriftgröße

## Ziel
Die bestehende zentrale PySide6-Skalierung soll zusätzlich mit `Strg + Mausrad` und sichtbaren Bedienelementen steuerbar sein, ohne ein zweites Schriftgrößensystem einzuführen.

## Umsetzung
- `Strg + Mausrad hoch`: nächste größere Zoomstufe.
- `Strg + Mausrad runter`: nächste kleinere Zoomstufe.
- `Strg++`, `Strg+-`, `Strg+0` bleiben bestehen.
- Statusleiste zeigt `A−`, aktuelle Prozentstufe und `A+`.
- Zoomstufen bleiben 100/125/150/175/200 %.
- Dashboard-Ereignisfilter gilt für verwaltete Qt-Fenster: Dashboard, Songeditor, Songbibliothek und Recovery.
- Schriftgrößen und Abstände folgen weiterhin ausschließlich den zentralen QSS-Standards.

## Schutz
- keine Nutzerdaten werden verändert,
- keine neue Abhängigkeit,
- keine parallele Schriftgrößenkonfiguration,
- Eventfilter wird beim Schließen entfernt.

## Abnahme
- Ctrl-Mausrad ändert Zoom und verbraucht das Ereignis,
- Grenzen 100–200 % werden eingehalten,
- sichtbare A−/A+-Bedienung vorhanden,
- bestehende GUI-/Recovery-/Song-/Restore-Gates bleiben grün.
