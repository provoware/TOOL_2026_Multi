#!/usr/bin/env bash
set -Eeuo pipefail

PROJEKTORDNER="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
UMGEBUNG="$PROJEKTORDNER/.venv"
DATENBASIS="${PROVOWARE_DATA_ROOT:-$PROJEKTORDNER}"
PYTHON="${PYTHON:-python3}"
STATUSDATEI="$DATENBASIS/logs/startstatus.json"
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

# Jede externe Startprüfung besitzt eine feste Zeitgrenze.
command -v timeout >/dev/null 2>&1 || { printf '🔴 Das Systemwerkzeug timeout fehlt (Paket coreutils).\n' >&2; exit 1; }
cd "$PROJEKTORDNER"
command -v "$PYTHON" >/dev/null 2>&1 || { printf '🔴 Die benötigte Python-3-Grundlage wurde nicht gefunden.\n' >&2; exit 1; }
if [[ -n "${PROVOWARE_DATA_ROOT:-}" ]]; then
  "$PYTHON" -c 'import sys; from app.runtime_roots import runtime_root; runtime_root(sys.argv[1])' "$PROJEKTORDNER" || fehler "Der getrennte Datenordner ist nicht sicher vorbereitet. Die alte Installation wurde nicht verändert."
fi
mkdir -p "$DATENBASIS/logs"
"$PYTHON" "$STATUSWERKZEUG" init "$STATUSDATEI" >/dev/null 2>&1 || true
checkpoint 1 ok "Grundlage ist vorhanden."

checkpoint 2 running "Startumgebung wird vorbereitet."
if [[ ! -e "$UMGEBUNG" && ! -L "$UMGEBUNG" ]]; then
  timeout 60 "$PYTHON" -m venv "$UMGEBUNG" || fehler "Die geschützte Startumgebung konnte nicht angelegt werden. Unter Ubuntu/Kubuntu kann das Paket python3-venv fehlen."
fi
[[ -x "$UMGEBUNG/bin/python" && ! -L "$UMGEBUNG" ]] || fehler "Die Startumgebung .venv ist beschädigt. Arbeitsdaten bleiben erhalten. Benenne nur .venv in .venv-alt um und starte erneut."
timeout 15 "$UMGEBUNG/bin/python" -c 'import sys; from pathlib import Path; assert sys.prefix != sys.base_prefix and Path(sys.prefix).resolve() == Path(sys.argv[1]).resolve()' "$UMGEBUNG" >/dev/null 2>&1 || fehler "Python in .venv funktioniert nicht als eigene Umgebung. Arbeitsdaten bleiben erhalten. Benenne nur .venv in .venv-alt um und starte erneut."
checkpoint 2 ok "Startumgebung ist bereit."

checkpoint 3 running "Benötigte Programmteile werden geprüft."
if grep -Eq '^[[:space:]]*[^#[:space:]]' requirements.txt; then
  ANFORDERUNGS_HASH="$(sha256sum requirements.txt | awk '{print $1}')"
  HASH_DATEI="$UMGEBUNG/.requirements.sha256"
  NEU_INSTALLIEREN=()
  if ! timeout 20 "$UMGEBUNG/bin/python" scripts/start_dependencies.py >/dev/null 2>&1; then
    NEU_INSTALLIEREN=(--force-reinstall)
  fi
  if [[ ! -f "$HASH_DATEI" ]] || [[ "$(cat "$HASH_DATEI")" != "$ANFORDERUNGS_HASH" ]] || (( ${#NEU_INSTALLIEREN[@]} )); then
    timeout 180 "$UMGEBUNG/bin/python" -m pip install --disable-pip-version-check --timeout 20 --retries 1 "${NEU_INSTALLIEREN[@]}" -r requirements.txt >/dev/null || fehler "Benötigte Programmteile konnten nicht eingerichtet werden. Arbeitsdaten bleiben erhalten. Prüfe Internetverbindung und freien Speicher und starte erneut; bei defektem pip benenne nur .venv in .venv-alt um."
    timeout 20 "$UMGEBUNG/bin/python" scripts/start_dependencies.py >/dev/null 2>&1 || fehler "Die installierten Programmteile sind noch nicht verwendbar. Arbeitsdaten bleiben erhalten. Benenne nur .venv in .venv-alt um und starte erneut."
    printf '%s' "$ANFORDERUNGS_HASH" > "$HASH_DATEI"
  fi
fi
checkpoint 3 ok "Benötigte Programmteile sind bereit."

if [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] && "$UMGEBUNG/bin/python" -c 'import PySide6' >/dev/null 2>&1; then
  "$UMGEBUNG/bin/python" "$STATUSWERKZEUG" gui "$STATUSDATEI" >/dev/null 2>&1 &
fi

checkpoint 4 running "Projekt wird kurz auf Startfehler geprüft."
timeout 30 "$UMGEBUNG/bin/python" -m app.main --headless-check || fehler "Die Startprüfung hat einen Fehler gefunden. Vorhandene Projektdaten wurden dabei nicht verändert."
checkpoint 4 ok "Projektprüfung erfolgreich."

checkpoint 5 running "Programmoberfläche wird vorbereitet."
timeout 20 "$UMGEBUNG/bin/python" -c 'from PySide6.QtWidgets import QApplication; print("Oberfläche bereit")' >/dev/null || fehler "Die Programmoberfläche konnte nicht vorbereitet werden."
checkpoint 5 ok "Programmoberfläche ist bereit."

checkpoint 6 running "Provoware wird geöffnet."
[[ -f "$PROJEKTORDNER/app/main.py" ]] || fehler "Die Hauptprogrammdatei app/main.py fehlt."
checkpoint 6 ok "Alle Startprüfungen sind erfolgreich."
"$PYTHON" "$STATUSWERKZEUG" finish "$STATUSDATEI" "🟢 Start erfolgreich. Provoware wird jetzt geöffnet." >/dev/null 2>&1 || true
exec "$UMGEBUNG/bin/python" -m scripts.process_watch --root "$DATENBASIS" -- "$UMGEBUNG/bin/python" -m app.main
