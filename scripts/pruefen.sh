#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
MODE="${1:---full}"
[[ "$MODE" == "--full" || "$MODE" == "--runtime" ]] || { printf 'Nutzung: %s [--full|--runtime]\n' "$0" >&2; exit 2; }
fehler=0
pruefe_datei(){ [[ -f "$1" ]] && printf '🟢 vorhanden: %s\n' "$1" || { printf '🔴 fehlt: %s\n' "$1"; fehler=1; }; }

runtime_dateien=(MANIFEST.json ANLEITUNG_LAIEN.md requirements.txt schnellstart.sh app/main.py app/event_log.py app/regression.py app/redaction.py app/texts.py app/ui.py app/ui_standards.py scripts/pruefen.sh scripts/start_status.py scripts/process_watch.py texte/registry.json)
for datei in "${runtime_dateien[@]}"; do pruefe_datei "$datei"; done
if [[ "$MODE" == "--full" ]]; then
  entwickler_dateien=(README.md AGENTS.md TODO.md CHANGELOG.md scripts/veroeffentlichen.py scripts/iteration_restore.py scripts/backup_erstellen.sh tests/test_event_management.py tests/test_release_builder.py tests/test_security_watch.py tests/test_restore.py tests/regression_registry.json agents/INFO_DATEIEN_AGENT.md)
  for datei in "${entwickler_dateien[@]}"; do pruefe_datei "$datei"; done
fi

printf '\nPrüfe Shell-Syntax …\n'
bash -n schnellstart.sh || fehler=1
bash -n scripts/pruefen.sh || fehler=1
bash -n scripts/backup_erstellen.sh || fehler=1

printf '\nPrüfe JSON-Dateien …\n'
python3 -m json.tool MANIFEST.json >/dev/null || fehler=1
python3 -m json.tool texte/registry.json >/dev/null || fehler=1
[[ "$MODE" != "--full" ]] || python3 -m json.tool tests/regression_registry.json >/dev/null || fehler=1

printf '\nPrüfe Python-Syntax …\n'
python3 -m py_compile app/*.py scripts/start_status.py scripts/process_watch.py || fehler=1
if [[ "$MODE" == "--full" ]]; then
  python3 -m py_compile scripts/veroeffentlichen.py scripts/iteration_restore.py tests/*.py || fehler=1
  printf '\nPrüfe Rückfall-, Release-, Sicherheits- und Restorebausteine …\n'
  python3 -m unittest tests.test_event_management tests.test_release_builder tests.test_security_watch tests.test_restore || fehler=1
  python3 scripts/veroeffentlichen.py --check-only || fehler=1
fi

printf '\nPrüfe Startunterbau ohne Oberfläche …\n'
python3 -m app.main --headless-check || fehler=1

if (( fehler != 0 )); then
  printf '\n🔴 Prüfung fehlgeschlagen. Keine Reparaturschleife gestartet.\n'
  exit 1
fi
printf '\n🟢 Prüfung erfolgreich.\n'
