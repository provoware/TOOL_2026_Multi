# Iteration 28 – Kubuntu 26.04 / Wayland

## Hauptziel

TOOL_2026_Multi auf Kubuntu 26.04 LTS mit KDE Plasma Wayland als offizielles Zielsystem umstellen, ohne den normalen Programmstart unnötig auf ein einzelnes Qt-Backend festzunageln.

## Technischer Scope

- `kubuntu_abnahme.sh` verlangt für die reale Endabnahme eine echte Wayland-Sitzung.
- `scripts/kubuntu_abnahme.py` prüft Ubuntu/Kubuntu-Basis 26.04, KDE/Plasma, `WAYLAND_DISPLAY`, eine nicht-X11-erzwungene Qt-Plattformvorgabe und den tatsächlich gestarteten Qt-QPA-Plattformnamen.
- `scripts/wayland_smoke.py` erlaubt einen echten nativen Qt-Wayland-Smoke-Test in CI.
- GitHub Actions startet dafür einen isolierten headless Weston-Compositor; die bestehenden Offscreen-Regressionen bleiben unverändert erhalten.
- X11 wird nicht aktiv aus der normalen Laufzeit entfernt. Es ist lediglich kein gültiger Pass für die neue Kubuntu-26.04-Endabnahme.

## Schutzgrenzen

- keine Nutzerdatenformate geändert,
- keine Song-, Profil-, Todo- oder Kalenderdaten verändert,
- keine Speicher-, Backup- oder Restore-Fachlogik verändert,
- `schnellstart.sh` bleibt backend-neutral und setzt `QT_QPA_PLATFORM` nicht künstlich,
- reale sichtbare Zielsystem-Abnahme bleibt zusätzlich erforderlich; CI beweist den nativen Qt-Wayland-Start, ersetzt aber keinen echten Kubuntu-/Plasma-Bildschirm.

## Abnahme

Technik-Evidence und finale Versions-Evidence werden nach den jeweiligen vollständigen CI-/Restore-Gates ergänzt.
