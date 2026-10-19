# Iteration 64 – sichere Anschlussfunktionen

**Status:** Entwicklungszweig, kein fertiger produktiver Updater.

1. Update: Die neue Funktion `audit_legacy_install` arbeitet ausschließlich lesend und weist auf blockierende Bedingungen einer Migration hin. Sie darf keine bestehende Installation umbauen. Ihre Antwort `activation_allowed` bleibt **immer falsch**, bis getrennte Datenhaltung, geprüfter Startweg und atomare Wiederherstellung entwickelt wurden.
2. Modulbaukasten: `module_runtime.save_record()` und `query()` machen bereits geprüfte Formulare als einfache eigenständige Datensammlungen nutzbar. Der Datenbestand liegt unter `daten/modulinstanzen/<id>.json`, wird nur nach strengem Vertrag geschrieben und kann keine fremden Dateien oder Programme ausführen. Echte Drittplugin-Laufzeit weiterhin nicht zulässig.
3. Video: `verify_video()` prüft neue MP4-Ausgaben mit FFprobe, bevor die fertige Datei den gewünschten Namen erhält. Ein Fehler verhindert die Veröffentlichung. Übergänge, Stapel und Effektparameter sind ausdrücklich nicht Bestandteil dieser Iteration.
4. Entwicklungspool: `import_project_copy()` prüft ZIP-Archive auf sichere relative Pfade, Dateianzahl, Größe und Dateitypen und legt das Projekt als neue Kopie an. Vorhandene Arbeitsordner werden nie überschrieben.

Alle Komponenten benötigen eine vollständige automatische Qualitätssicherung und dürfen vor grünem CI nicht in `main` integriert werden. Die manuelle Kubuntu-Praxisabnahme ist für das Ende der gesamten Entwicklung fest vorgesehen.
