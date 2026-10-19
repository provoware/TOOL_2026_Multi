# Iteration 70 – Sicherer Wiederholungsauftrag und Fremdcodeprobe

Die Video-Wiederholung erlaubt ausschließlich `failed` oder `interrupted`; vor der Wiederholung müssen Benutzerfreigabe, zulässige Eingabedateien und ein freies Ausgabeziel nachgewiesen werden. Bereits vorhandene Ausgabedateien werden nicht überschrieben. Das bloße Wiedereinreihen startet **keinen** FFmpeg-Auftrag.

Der Fremdcode-Probelauf benötigt das Linux-Werkzeug Bubblewrap und trennt seinen eigenen Prozess durch Netzwerk- und Mount-Namensräume. Der Quelltext wird nur lesbar in einen virtuellen Arbeitsordner eingebunden. Es existiert keine automatische Ausführung beim Start, kein Zugriff auf Projektdaten und keine Freigabe der Erweiterung für produktive Nutzung. Die Ausgabe wird als reine JSON-Aktionsbeschreibung geprüft. Fehlende Sandbox, fehlende Zustimmung und fremde Kommandos führen zum Abbruch. Weitere Negativtests gegen Sandbox-Ausbrüche und Limits sind vor produktiver Freigabe nötig.

Eine sichere Umstellung bisheriger Installationen braucht noch einen unabhängig geprüften Launcher-Wechsel samt garantiertem Rollback des *Startweges*. Die Altinstallation und Benutzerdaten dürfen keinesfalls überschrieben werden. Die spätere umfassende manuelle Kubuntu-Abnahme bleibt bis zum Abschluss aller Module ausgesetzt.
