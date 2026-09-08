#!/usr/bin/env bash
set -Eeuo pipefail

PROJEKTORDNER="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
UMGEBUNG="$PROJEKTORDNER/.venv"
PYTHON="${PYTHON:-python3}"
STATUSDATEI="$PROJEKTORDNER/logs/startstatus.json"
STATUSWERKZEUG="$PROJEKTORDNER/scripts/start_status.py"
AKTUELLER_SCHRITT=1

farbe() { printf '\033[%sm%s\033[0m\n' "$1" "$2"; }
checkpoint() {
  AKTUELLER_SCHRITT="$1"
  "$PYTHON" "$STATUSWERKZEUG" set "$STATUSDATEI" "$1" "$2" "$3" >/dev/null 2>&1 || true
  case "$2" in
    ok) farbe "32" "🟢 [$1/6] $3" ;;
    running) farbe "33" "🟡 [$1/6] $3" ;;
    failed) farbe "31" "🔴 [$1/6] $3" ;;
  esac
}
fehler() {
  checkpoint "$AKTUELLER_SCHRITT" failed "$*"
  farbe "31" "FEHLER: $*"
  exit 1
}

cd "$PROJEKTORDNER"
command -v "$PYTHON" >/dev/null 2>&1 || { printf '🔴 Python 3 wurde nicht gefunden.\n' >&2; exit 1; }
mkdir -p "$PROJEKTORDNER/logs"
"$PYTHON" "$STATUSWERKZEUG" init "$STATUSDATEI" >/dev/null 2>&1 || true
checkpoint 1 ok "Python 3 ist verfügbar."

checkpoint 2 running "Abgeschirmte Python-Umgebung wird geprüft."
if [[ ! -x "$UMGEBUNG/bin/python" ]]; then
  "$PYTHON" -m venv "$UMGEBUNG" || fehler "Die Python-Umgebung konnte nicht angelegt werden. Unter Ubuntu/Kubuntu kann python3-venv fehlen."
fi
checkpoint 2 ok "Python-Umgebung ist bereit."

checkpoint 3 running "Benötigte Pakete werden geprüft."
if grep -Eq '^[[:space:]]*[^#[:space:]]' requirements.txt; then
  ANFORDERUNGS_HASH="$(sha256sum requirements.txt | awk '{print $1}')"
  HASH_DATEI="$UMGEBUNG/.requirements.sha256"
  if [[ ! -f "$HASH_DATEI" ]] || [[ "$(cat "$HASH_DATEI")" != "$ANFORDERUNGS_HASH" ]]; then
    "$UMGEBUNG/bin/python" -m pip install --disable-pip-version-check -r requirements.txt >/dev/null || fehler "Benötigte Pakete konnten nicht eingerichtet werden."
    printf '%s' "$ANFORDERUNGS_HASH" > "$HASH_DATEI"
  fi
fi
checkpoint 3 ok "Abhängigkeiten sind bereit."

if [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] && "$UMGEBUNG/bin/python" -c 'import PySide6' >/dev/null 2>&1; then
  "$UMGEBUNG/bin/python" "$STATUSWERKZEUG" gui "$STATUSDATEI" >/dev/null 2>&1 &
fi

checkpoint 4 running "Projekt wird begrenzt vorgeprüft."
"$UMGEBUNG/bin/python" -m app.main --headless-check || fehler "Der Startunterbau ist nicht vollständig funktionsfähig."
checkpoint 4 ok "Projektprüfung erfolgreich."

checkpoint 5 running "PySide6-Oberfläche wird geprüft."
"$UMGEBUNG/bin/python" -c 'from PySide6.QtWidgets import QApplication; print("PySide6 bereit")' >/dev/null || fehler "PySide6 ist nicht funktionsfähig."
checkpoint 5 ok "PySide6 ist bereit."

checkpoint 6 running "Anwendung wird unter Prozesswache geöffnet."
[[ -f "$PROJEKTORDNER/app/main.py" ]] || fehler "app/main.py fehlt."
checkpoint 6 ok "Alle Start-Checkpoints sind grün."
"$PYTHON" "$STATUSWERKZEUG" finish "$STATUSDATEI" "🟢 Start vollständig geprüft. Anwendung wird geöffnet." >/dev/null 2>&1 || true
exec "$UMGEBUNG/bin/python" -m scripts.process_watch --root "$PROJEKTORDNER" -- "$UMGEBUNG/bin/python" -m app.main
