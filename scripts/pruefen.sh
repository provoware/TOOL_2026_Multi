#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
MODE="${1:---full}"
[[ "$MODE" == "--full" || "$MODE" == "--runtime" ]] || { printf 'Nutzung: %s [--full|--runtime]\n' "$0" >&2; exit 2; }
fehler=0
pruefe_datei(){ [[ -f "$1" ]] && printf '🟢 vorhanden: %s\n' "$1" || { printf '🔴 fehlt: %s\n' "$1"; fehler=1; }; }

runtime_dateien=(MANIFEST.json ANLEITUNG_LAIEN.md requirements.txt schnellstart.sh kubuntu_abnahme.sh app/main.py app/event_log.py app/regression.py app/redaction.py app/log_maintenance.py app/recovery_ui.py app/recovery_center.py app/quick_note.py app/profile_store.py app/profile_editor.py app/song_document.py app/song_editor.py app/song_library.py app/texts.py app/ui.py app/ui_standards.py scripts/pruefen.sh scripts/start_status.py scripts/process_watch.py scripts/diagnosepaket.py scripts/kubuntu_abnahme.py texte/registry.json)
for datei in "${runtime_dateien[@]}"; do pruefe_datei "$datei"; done
if [[ "$MODE" == "--full" ]]; then
  entwickler_dateien=(README.md AGENTS.md TODO.md CHANGELOG.md scripts/veroeffentlichen.py scripts/iteration_restore.py scripts/backup_erstellen.sh scripts/schreibfehler_simulieren.py tests/test_event_management.py tests/test_release_builder.py tests/test_security_watch.py tests/test_restore.py tests/test_diagnostics_logging.py tests/test_recovery_ui_logic.py tests/test_recovery_ui_gui.py tests/test_song_logic.py tests/test_song_gui.py tests/test_song_library.py tests/test_song_library_gui.py tests/test_song_library_controls.py tests/test_song_library_controls_gui.py tests/test_dashboard_reference_gui.py tests/test_kubuntu_acceptance.py tests/test_zoom_controls_gui.py tests/test_profile_store.py tests/test_profile_gui.py tests/regression_registry.json agents/INFO_DATEIEN_AGENT.md docs/ITERATION6_RECOVERY_UI.md docs/ITERATION7_SONG_WORKFLOW.md docs/ITERATION8_SONG_LIBRARY.md docs/ITERATION9_SONG_LIBRARY_CONTROLS.md docs/ITERATION11_QT_DASHBOARD.md docs/ITERATION12_KUBUNTU_ABNAHME.md docs/ITERATION13_ZOOM.md docs/ITERATION14_DB_PROFILE.md)
  for datei in "${entwickler_dateien[@]}"; do pruefe_datei "$datei"; done
fi

printf '\nPrüfe Shell-Syntax …\n'
bash -n schnellstart.sh || fehler=1
bash -n kubuntu_abnahme.sh || fehler=1
bash -n scripts/pruefen.sh || fehler=1
bash -n scripts/backup_erstellen.sh || fehler=1

printf '\nPrüfe JSON-Dateien …\n'
python3 -m json.tool MANIFEST.json >/dev/null || fehler=1
python3 -m json.tool texte/registry.json >/dev/null || fehler=1
[[ "$MODE" != "--full" ]] || python3 -m json.tool tests/regression_registry.json >/dev/null || fehler=1

printf '\nPrüfe Python-Syntax …\n'
python3 -m py_compile app/*.py scripts/start_status.py scripts/process_watch.py scripts/diagnosepaket.py scripts/kubuntu_abnahme.py || fehler=1
if [[ "$MODE" == "--full" ]]; then
  python3 -m py_compile scripts/veroeffentlichen.py scripts/iteration_restore.py scripts/schreibfehler_simulieren.py tests/*.py || fehler=1
  printf '\nPrüfe Rückfall-, Release-, Sicherheits-, Restore-, Diagnose-, Recovery-, Song-, Profil- und Kubuntu-Abnahmelogik …\n'
  python3 -m unittest tests.test_event_management tests.test_release_builder tests.test_security_watch tests.test_restore tests.test_diagnostics_logging tests.test_recovery_ui_logic tests.test_song_logic tests.test_song_library tests.test_song_library_controls tests.test_profile_store tests.test_kubuntu_acceptance || fehler=1
  printf '\nSimuliere vollen/geschützten Datenträger ohne echten Speicherverbrauch …\n'
  python3 scripts/schreibfehler_simulieren.py >/dev/null || fehler=1
  printf '\nPrüfe Dashboard, Recovery, Songeditor, Songbibliothek, Profile und Zoom in echter PySide6-Oberfläche …\n'
  export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
  python3 -m unittest tests.test_recovery_ui_gui tests.test_song_gui tests.test_song_library_gui tests.test_song_library_controls_gui tests.test_dashboard_reference_gui tests.test_zoom_controls_gui tests.test_profile_gui || fehler=1
  python3 scripts/veroeffentlichen.py --check-only || fehler=1
fi

printf '\nPrüfe Startunterbau ohne Oberfläche …\n'
python3 -m app.main --headless-check || fehler=1

if (( fehler != 0 )); then
  printf '\n🔴 Prüfung fehlgeschlagen. Keine Reparaturschleife gestartet.\n'
  exit 1
fi
printf '\n🟢 Prüfung erfolgreich.\n'