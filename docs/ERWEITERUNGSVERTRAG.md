# Kontrollierte Erweiterungsschnittstelle

Eine Zusatzvorlage darf als kleine JSON-Datei mit `schema_version=1`, `module_id` und einer Liste geprüfter `actions` beschrieben werden. Es sind ausschließlich die eingebauten Aktionen **view**, **search** und **edit** zugelassen. Jede tatsächliche Ausführung benötigt eine ausdrückliche Benutzerfreigabe über `execute_approved(..., approved=True)`. Mehrere Aktionen in einem Schritt werden abgewiesen; unbekannte Felder, Programmaufrufe und Links ebenfalls. Die Berechtigung muss auch in der Modulvorlage vorhanden sein.

**Wichtig:** Das Format führt keinen fremden Python-Code aus und ist kein signiertes Plugin- oder Sandboxing-System. Für ausführbare Erweiterungen sind unabhängig davon echte Betriebssystem-Isolierung, Rechteeinwilligung, Paketprüfung und separate Ende-zu-Ende-Tests notwendig. Der gewöhnliche Kubuntu-Endtest bleibt bis zur vollständigen Modulentwicklung ausgesetzt.
