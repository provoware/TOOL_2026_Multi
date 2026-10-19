# Provoware-Multimedia – Grundmodule

Alle drei Programme sind Offline-Werkzeuge und erscheinen über das Modulmenü. Die gemeinsamen Farbthemen und Vergrößerungsstufen bleiben erhalten.

## Audioplayer (Strg+Alt+U)
Über **Dateien hinzufügen** wählst du lokale MP3-, OGG-, WAV-, FLAC-, M4A- oder AAC-Dateien. Die Liste bleibt nach Programmneustart gespeichert. Doppelklick oder Wiedergabe startet die ausgewählte Datei. Vorheriger/Nächster Titel, Pause, Stopp, Zeitposition und Lautstärke sind direkt erreichbar. Playlist-Import und -Export verwenden lokales JSON. Fehlende Audiodateien werden als fehlend angezeigt und nicht heimlich entfernt.

## Bildvorschau (Strg+Alt+O)
Wähle lokale JPG-, PNG-, BMP- oder WEBP-Dateien. Die gespeicherte Bildliste hat bis zu 200 Einträge, mit Vorheriges/Nächstes. Das Programm prüft Dateien vor der Vorschau (maximal 25 MB, begrenzte Pixelzahl) und reduziert große Bilder vor dem Anzeigen. Originalbilder werden nicht geändert. Listen lassen sich als JSON exportieren und importieren.

## Video & Slideshow (Strg+Alt+V)
Du brauchst das separat vorhandene Kommandozeilenprogramm **FFmpeg**. Für ein einfaches MP4 kannst du ein oder bis zu 20 Bilder wählen, je Bild 1–30 Sekunden einstellen und optional Ton hinzufügen. Alternativ kombinierst du ein vorhandenes Video mit einer neuen Tonspur. Jeder Auftrag läuft einzeln ohne blockierende Bildschirmbedienung. Die Anzeige gibt bei Slideshows Fortschritt und ungefähre Restzeit an; **Abbrechen** stoppt die Verarbeitung. Die Ausgabe wird zunächst als getrennte temporäre Datei geschrieben und nur bei Erfolg unter dem Zielnamen angelegt. **Vorhandene Dateien werden niemals ersetzt.**

Slideshow-Vorgaben werden lokal als JSON gesichert und exportiert. Für Video-Audio-Kombinationen ist die genaue Restzeitanzeige noch nicht umgesetzt. Es gibt derzeit keine frei wählbaren Überblendungs-/Intensitätseffekte und keine Auftragswarteschlange. Eine umfangreiche tatsächliche Mediendekodierung und Bild-/Tonbewertung ist Teil der späteren Endabnahme, nicht der aktuellen GUI-Basisprüfung.

Bei fehlenden Systemcodecs können einzelne Audiodateien oder Videoformate nicht abgespielt werden. Dann bleiben Originaldateien erhalten und eine Fehlermeldung wird angezeigt.
