#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
MODE="${1:---full}"
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT/.venv/bin/python"
else
  PYTHON_BIN="${PYTHON_BIN:-python3}"
fi
[[ "$MODE" == "--full" || "$MODE" == "--quick" || "$MODE" == "--runtime" ]] || {
  printf 'Nutzung: %s [--quick|--full|--runtime]\n' "$0" >&2
  exit 2
}

fehler=0
pruefe_datei() {
  [[ -f "$1" ]] && printf '🟢 vorhanden: %s\n' "$1" || {
    printf '🔴 fehlt: %s\n' "$1"
    fehler=1
  }
}

printf 'Prüfe freigegebene Betriebsdateien aus MANIFEST.json …\n'
while IFS= read -r datei; do
  pruefe_datei "$datei"
done < <(
  "$PYTHON_BIN" - <<'PY'
import json
from pathlib import Path
manifest = json.loads(Path("MANIFEST.json").read_text(encoding="utf-8"))
for entry in manifest.get("files", []):
    if entry.get("release") is True:
        path = entry.get("path")
        if isinstance(path, str) and path:
            print(path)
PY
)

if [[ "$MODE" != "--runtime" ]]; then
  printf '\nPrüfe kleine feste Entwickler-Grundausstattung …\n'
  entwickler_dateien=(
    README.md AGENTS.md TODO.md CHANGELOG.md
    tests/regression_registry.json agents/INFO_DATEIEN_AGENT.md
    docs/ENTWICKLUNGSREGELN.md docs/FEHLER_UND_REGRESSION.md
    docs/ITERATIONSBERICHT_VORLAGE.md docs/ITERATION37_MAINTENANCE_HELP.md
    scripts/veroeffentlichen.py scripts/schreibfehler_simulieren.py scripts/wayland_smoke.py
  )
  for datei in "${entwickler_dateien[@]}"; do
    pruefe_datei "$datei"
  done
fi

printf '\nPrüfe Shell-Syntax automatisch …\n'
mapfile -t shell_dateien < <(
  find . -maxdepth 2 -type f -name '*.sh' \
    -not -path './.git/*' -not -path './.venv/*' \
    -not -path './backups/*' -not -path './release/*' | sort
)
for datei in "${shell_dateien[@]}"; do
  bash -n "$datei" || fehler=1
done

printf '\nPrüfe statische JSON-Dateien …\n'
mapfile -t json_dateien < <(
  "$PYTHON_BIN" - <<'PY'
import json
from pathlib import Path
manifest = json.loads(Path("MANIFEST.json").read_text(encoding="utf-8"))
paths = {"MANIFEST.json"}
for entry in manifest.get("files", []):
    path = entry.get("path")
    if isinstance(path, str) and path.endswith(".json") and Path(path).is_file():
        paths.add(path)
if Path("tests/regression_registry.json").is_file():
    paths.add("tests/regression_registry.json")
for path in sorted(paths):
    print(path)
PY
)
for datei in "${json_dateien[@]}"; do
  "$PYTHON_BIN" -m json.tool "$datei" >/dev/null || fehler=1
done

printf '\nPrüfe Python-Prüfumgebung …\n'
if ! "$PYTHON_BIN" -c 'import PySide6' >/dev/null 2>&1; then
  printf '🔴 PySide6 fehlt in %s. Starte zuerst schnellstart.sh oder verwende PYTHON_BIN=/pfad/zur/python-umgebung.\n' "$PYTHON_BIN"
  exit 3
fi

printf '\nPrüfe Python-Syntax automatisch …\n'
python_ziele=(app scripts)
[[ "$MODE" == "--runtime" ]] || python_ziele+=(tests)
"$PYTHON_BIN" -m compileall -q "${python_ziele[@]}" || fehler=1

if [[ "$MODE" != "--runtime" ]]; then
  printf '\nPrüfe automatisch alle Logik-/Regressionstests …\n'
  mapfile -t logik_tests < <(
    find tests -maxdepth 1 -type f -name 'test_*.py' ! -name '*_gui.py' -printf '%f\n' \
      | sort | sed -e 's/\.py$//' -e 's#^#tests.#'
  )
  if (( ${#logik_tests[@]} == 0 )); then
    printf '🔴 Keine Logiktests gefunden.\n'
    fehler=1
  else
    "$PYTHON_BIN" -m unittest "${logik_tests[@]}" || fehler=1
  fi

  printf '\nSimuliere vollen/geschützten Datenträger ohne echten Speicherverbrauch …\n'
  "$PYTHON_BIN" scripts/schreibfehler_simulieren.py >/dev/null || fehler=1
fi

if [[ "$MODE" == "--full" ]]; then
  printf '\nPrüfe automatisch alle PySide6-GUI-Tests …\n'
  export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
  mapfile -t gui_tests < <(
    find tests -maxdepth 1 -type f -name '*_gui.py' -printf '%f\n' \
      | sort | sed -e 's/\.py$//' -e 's#^#tests.#'
  )
  if (( ${#gui_tests[@]} == 0 )); then
    printf '🔴 Keine GUI-Tests gefunden.\n'
    fehler=1
  else
    "$PYTHON_BIN" -m unittest "${gui_tests[@]}" || fehler=1
  fi

  printf '\nPrüfe Release-Manifest …\n'
  "$PYTHON_BIN" scripts/veroeffentlichen.py --check-only || fehler=1
fi

printf '\nPrüfe Startunterbau ohne Oberfläche …\n'
"$PYTHON_BIN" -m app.main --headless-check || fehler=1

if (( fehler != 0 )); then
  printf '\n🔴 Prüfung fehlgeschlagen. Keine Reparaturschleife gestartet.\n'
  exit 1
fi
printf '\n🟢 Prüfung erfolgreich.\n'
