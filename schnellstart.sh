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
command -v "$PYTHON" >/dev/null 2>&1 || { printf '🔴 Die benötigte Python-3-Grundlage wurde nicht gefunden.\n' >&2; exit 1; }
mkdir -p "$PROJEKTORDNER/logs"
"$PYTHON" "$STATUSWERKZEUG" init "$STATUSDATEI" >/dev/null 2>&1 || true
checkpoint 1 ok "Grundlage ist vorhanden."

checkpoint 2 running "Startumgebung wird vorbereitet."
if [[ ! -x "$UMGEBUNG/bin/python" ]]; then
  "$PYTHON" -m venv "$UMGEBUNG" || fehler "Die geschützte Startumgebung konnte nicht angelegt werden. Unter Ubuntu/Kubuntu kann das Paket python3-venv fehlen."
fi
checkpoint 2 ok "Startumgebung ist bereit."

checkpoint 3 running "Benötigte Programmteile werden geprüft."
if grep -Eq '^[[:space:]]*[^#[:space:]]' requirements.txt; then
  ANFORDERUNGS_HASH="$(sha256sum requirements.txt | awk '{print $1}')"
  HASH_DATEI="$UMGEBUNG/.requirements.sha256"
  if [[ ! -f "$HASH_DATEI" ]] || [[ "$(cat "$HASH_DATEI")" != "$ANFORDERUNGS_HASH" ]]; then
    "$UMGEBUNG/bin/python" -m pip install --disable-pip-version-check -r requirements.txt >/dev/null || fehler "Benötigte Programmteile konnten nicht eingerichtet werden. Prüfe die Internetverbindung und versuche es erneut."
    printf '%s' "$ANFORDERUNGS_HASH" > "$HASH_DATEI"
  fi
fi
checkpoint 3 ok "Benötigte Programmteile sind bereit."

if [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] && "$UMGEBUNG/bin/python" -c 'import PySide6' >/dev/null 2>&1; then
  "$UMGEBUNG/bin/python" "$STATUSWERKZEUG" gui "$STATUSDATEI" >/dev/null 2>&1 &
fi

checkpoint 4 running "Projekt wird kurz auf Startfehler geprüft."
"$UMGEBUNG/bin/python" -m app.main --headless-check || fehler "Die Startprüfung hat einen Fehler gefunden. Vorhandene Projektdaten wurden dabei nicht verändert."
checkpoint 4 ok "Projektprüfung erfolgreich."

checkpoint 5 running "Programmoberfläche wird vorbereitet."
"$UMGEBUNG/bin/python" -c 'from PySide6.QtWidgets import QApplication; print("Oberfläche bereit")' >/dev/null || fehler "Die Programmoberfläche konnte nicht vorbereitet werden."
checkpoint 5 ok "Programmoberfläche ist bereit."

checkpoint 6 running "Provoware wird geöffnet."
[[ -f "$PROJEKTORDNER/app/main.py" ]] || fehler "Die Hauptprogrammdatei app/main.py fehlt."
checkpoint 6 ok "Alle Startprüfungen sind erfolgreich."
"$PYTHON" "$STATUSWERKZEUG" finish "$STATUSDATEI" "🟢 Start erfolgreich. Provoware wird jetzt geöffnet." >/dev/null 2>&1 || true
exec "$UMGEBUNG/bin/python" -m scripts.process_watch --root "$PROJEKTORDNER" -- "$UMGEBUNG/bin/python" -m app.main
