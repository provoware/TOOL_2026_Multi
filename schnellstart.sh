#!/usr/bin/env bash
set -Eeuo pipefail

PROJEKTORDNER="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
UMGEBUNG="$PROJEKTORDNER/.venv"
PYTHON="${PYTHON:-python3}"

meldung() { printf '%s\n' "$*"; }
fehler() { printf 'FEHLER: %s\n' "$*" >&2; exit 1; }

cd "$PROJEKTORDNER"

command -v "$PYTHON" >/dev/null 2>&1 || fehler "Python 3 wurde nicht gefunden. Bitte Python 3 über die Paketverwaltung installieren."

if [[ ! -x "$UMGEBUNG/bin/python" ]]; then
  meldung "[1/4] Abgeschirmte Python-Umgebung wird angelegt …"
  "$PYTHON" -m venv "$UMGEBUNG" || fehler "Die Python-Umgebung konnte nicht angelegt werden. Unter Ubuntu/Kubuntu kann das Paket python3-venv fehlen."
else
  meldung "[1/4] Python-Umgebung ist vorhanden."
fi

meldung "[2/4] Benötigte Pakete werden abgeglichen …"
"$UMGEBUNG/bin/python" -m pip install --disable-pip-version-check -r requirements.txt >/dev/null || fehler "Benötigte Pakete konnten nicht eingerichtet werden."

meldung "[3/4] Projekt wird einmal geprüft …"
bash scripts/pruefen.sh || fehler "Die Vorprüfung meldet einen Fehler. Details stehen direkt oberhalb dieser Meldung."

meldung "[4/4] Anwendung wird gestartet …"
if [[ -f "$PROJEKTORDNER/app/main.py" ]]; then
  exec "$UMGEBUNG/bin/python" -m app.main
fi

meldung "Noch keine Anwendung vorhanden. Die Entwicklungsgrundlage ist korrekt eingerichtet; app/main.py folgt in der nächsten Implementierungsiteration."
