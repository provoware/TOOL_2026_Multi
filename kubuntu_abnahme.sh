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

SESSION="${XDG_SESSION_TYPE:-}"
SESSION="${SESSION,,}"
[[ "$SESSION" == "wayland" ]] || fehler "Die Kubuntu-26.04-Endabnahme benötigt eine echte Plasma-Wayland-Sitzung. Melde dich bei 'Plasma (Wayland)' an und starte die Abnahme erneut."
[[ -n "${WAYLAND_DISPLAY:-}" ]] || fehler "Es wurde keine Wayland-Anzeige erkannt (WAYLAND_DISPLAY fehlt)."
case "${QT_QPA_PLATFORM:-}" in
  xcb|xcb:*) fehler "Qt ist ausdrücklich auf X11/XWayland (xcb) gezwungen. Entferne QT_QPA_PLATFORM=xcb und starte erneut." ;;
  offscreen|minimal) fehler "Qt ist auf einen Test-Backendwert gesetzt. Für die reale Abnahme darf QT_QPA_PLATFORM nicht offscreen/minimal sein." ;;
esac

exec "$VENV/bin/python" scripts/kubuntu_abnahme.py
