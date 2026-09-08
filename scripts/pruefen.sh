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
python3 -m json.tool configs/ui.json >/dev/null || fehler=1

printf '\nPrüfe Manifest-Grenzen und Verzeichnistrennung …\n'
python3 - <<'PY_LIMITS' || fehler=1
import json
from pathlib import Path

manifest = json.loads(Path("MANIFEST.json").read_text(encoding="utf-8"))
limits = manifest["line_limits"]
groups = {
    "helper_module": list(Path("scripts").glob("*.sh")) + [Path("app/ui_style.py"), Path("app/texts.py")],
    "normal_module": [p for p in Path("app").glob("*.py") if p.name not in {"ui_style.py", "texts.py"}],
    "test_file": list(Path("tests").glob("*.py")),
    "config_file": list(Path("configs").glob("*.json")) + list(Path("texte").glob("*.json")),
    "documentation_file": list(Path("docs").glob("*.md")),
}
failed = False
for group, paths in groups.items():
    for path in paths:
        count = len(path.read_text(encoding="utf-8").splitlines())
        if count > limits[group]:
            print(f"🔴 {path}: {count} Zeilen, erlaubt sind {limits[group]}.")
            failed = True
required = {"tool_core", "configuration", "tooling", "base_data_transfer", "user_data", "texts", "developer_docs", "tests"}
for name, item in manifest["separation"].items():
    if name in required and not Path(item["path"]).is_dir():
        print(f"🔴 Getrennter Bereich fehlt: {item['path']}")
        failed = True
raise SystemExit(1 if failed else 0)
PY_LIMITS

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
