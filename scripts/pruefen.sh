#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fehler=0
pruefe_datei() {
  local datei="$1"
  if [[ -f "$datei" ]]; then
    printf '🟢 vorhanden: %s\n' "$datei"
  else
    printf '🔴 fehlt: %s\n' "$datei"
    fehler=1
  fi
}

printf 'TOOL_2026_Multi – begrenzte Grundprüfung\n'
printf '%s\n' '--------------------------------------'

for datei in README.md AGENTS.md TODO.md CHANGELOG.md MANIFEST.json ANLEITUNG_LAIEN.md requirements.txt schnellstart.sh; do
  pruefe_datei "$datei"
done

printf '\nPrüfe Shell-Syntax …\n'
bash -n schnellstart.sh || fehler=1
bash -n scripts/pruefen.sh || fehler=1
bash -n scripts/backup_erstellen.sh || fehler=1

printf '\nPrüfe JSON-Dateien …\n'
python3 -m json.tool MANIFEST.json >/dev/null || fehler=1
python3 -m json.tool texte/registry.json >/dev/null || fehler=1

if [[ -f app/main.py ]]; then
  printf '\nPrüfe Python-Syntax der geänderten Anwendungsmodule …\n'
  python3 -m py_compile app/*.py tests/test_event_management.py || fehler=1

  printf '\nPrüfe Ereignis- und Rückfallmanagement …\n'
  python3 -m unittest tests.test_event_management || fehler=1
fi

if (( fehler != 0 )); then
  printf '\n🔴 Prüfung fehlgeschlagen. Es wurden keine automatischen Reparaturschleifen gestartet.\n'
  exit 1
fi

printf '\n🟢 Grundprüfung erfolgreich.\n'
