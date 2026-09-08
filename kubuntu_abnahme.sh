#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"
PYTHON="${PYTHON:-python3}"
cd "$ROOT"

fehler(){ printf '🔴 %s\n' "$*" >&2; exit 1; }
command -v "$PYTHON" >/dev/null 2>&1 || fehler "Python 3 wurde nicht gefunden."
[[ -f requirements.txt ]] || fehler "requirements.txt fehlt."

if [[ ! -x "$VENV/bin/python" ]]; then
  "$PYTHON" -m venv "$VENV" || fehler "Die Python-Umgebung konnte nicht angelegt werden."
fi
HASH="$(sha256sum requirements.txt | awk '{print $1}')"
HASHDATEI="$VENV/.requirements.sha256"
if [[ ! -f "$HASHDATEI" ]] || [[ "$(cat "$HASHDATEI")" != "$HASH" ]]; then
  "$VENV/bin/python" -m pip install --disable-pip-version-check -r requirements.txt >/dev/null \
    || fehler "PySide6 konnte nicht eingerichtet werden."
  printf '%s' "$HASH" > "$HASHDATEI"
fi

[[ "${XDG_SESSION_TYPE:-}" == "x11" ]] || fehler "Diese Endabnahme ist ausschließlich für eine echte X11-Sitzung vorgesehen. Bitte bei der Anmeldung 'Plasma (X11)' wählen."
[[ -n "${DISPLAY:-}" ]] || fehler "Es wurde keine grafische X11-Anzeige erkannt."

exec "$VENV/bin/python" scripts/kubuntu_abnahme.py
