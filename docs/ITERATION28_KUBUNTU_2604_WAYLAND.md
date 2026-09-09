# Iteration 28 – Kubuntu 26.04 / Wayland

## Hauptziel

TOOL_2026_Multi auf Kubuntu 26.04 LTS mit KDE Plasma Wayland als offizielles Zielsystem umstellen, ohne den normalen Programmstart unnötig auf ein einzelnes Qt-Backend festzunageln.

## Befund

Die bisherige reale Endabnahme war technisch auf X11 festgelegt und verlangte `XDG_SESSION_TYPE=x11` sowie `DISPLAY`. Der normale `schnellstart.sh` war dagegen bereits backend-neutral. Für Kubuntu 26.04 ist deshalb nicht die Anwendung selbst auf einen festen Backendwert umzubauen, sondern die Plattformabnahme auf **native Wayland-Nutzung** umzustellen und zusätzlich in CI einen echten Qt-Wayland-Start nachzuweisen.

## Umsetzung

- `kubuntu_abnahme.sh` verlangt für die offizielle reale Endabnahme eine echte Wayland-Sitzung und `WAYLAND_DISPLAY`.
- Ein ausdrücklich gesetztes `QT_QPA_PLATFORM=xcb` sowie Test-Backends wie `offscreen`/`minimal` werden für die reale Zielsystem-Abnahme abgewiesen.
- `scripts/kubuntu_abnahme.py` prüft Ubuntu/Kubuntu-Basis 26.04, KDE/Plasma, Wayland-Sitzung und den tatsächlich gestarteten Qt-QPA-Plattformnamen.
- `QApplication.platformName()` muss für einen grünen nativen Plattformcheck mit `wayland` beginnen; XWayland/`xcb` wird nicht als nativer Wayland-Pass gewertet.
- `scripts/wayland_smoke.py` ergänzt einen kleinen echten Qt-Wayland-Fensterstart für CI.
- GitHub Actions startet dafür einen isolierten headless Weston-Compositor. Die bisherigen Offscreen-GUI-Regressionen bleiben parallel bestehen.
- `schnellstart.sh` bleibt backend-neutral: kein erzwungenes Wayland, kein erzwungenes X11.
- Die sichtbare Zielsystem-Abnahme umfasst weiterhin Laptoplayout, 125/150/175/200 %, Kontrasttheme und Tastaturfokus und ergänzt Wayland-spezifisch Fenster-, Menü- und Eingabefokus-Verhalten.
- X11 wird nicht künstlich aus der allgemeinen Laufzeit entfernt. Es ist lediglich kein gültiger Pass für die offizielle Kubuntu-26.04-/Wayland-Endabnahme.

## Schutzgrenzen

- keine Nutzerdatenformate geändert,
- keine Song-, Profil-, Todo- oder Kalenderdaten verändert,
- keine Speicher-, Backup- oder Restore-Fachlogik verändert,
- keine neue Laufzeitabhängigkeit für Nutzer ergänzt; Weston wird nur in GitHub Actions für den isolierten Wayland-Smoke installiert,
- reale sichtbare Zielsystem-Abnahme bleibt zusätzlich erforderlich; CI beweist den nativen Qt-Wayland-Start, ersetzt aber keinen echten Kubuntu-26.04-/Plasma-Bildschirm.

## Technische Abnahme vor Versions-Sync

Technischer Head: `a7f2c168ecc3f0a2310fbff874cea33d30793d25`

GitHub-Grundprüfung **#567**:

- 🟢 86 Logik-/Regressionstests,
- 🟢 56 PySide6-GUI-Tests unter `offscreen`,
- 🟢 Release-Manifest: 38 Betriebsdateien,
- 🟢 Headless-Start,
- 🟢 nativer Qt-Wayland-Smoke unter isoliertem Weston; `QApplication.platformName()` meldet `wayland`,
- 🟢 Vollprojekt-Restore `OK`,
- 🟢 Restore-SHA-256 `1283f1399a5d4a675bdc06720ebf5435df38fccbf36d64fb74fd5e1e9748b579`.

Der GitHub-Runner selbst war Ubuntu 24.04.4. Damit ist der native Qt-Wayland-Pfad automatisiert bewiesen, **nicht** jedoch eine reale Kubuntu-26.04-/KDE-Plasma-Sitzung. Genau dafür bleibt `bash kubuntu_abnahme.sh` als sichtbare Zielsystem-Abnahme erforderlich.

## Finale Abnahme

Nach Synchronisierung auf Version 0.16.0 wird der vollständige Block aus Vollprüfung, nativem Wayland-Smoke und Restore erneut auf dem finalen PR-Head ausgeführt. Erst bei vollständig grünem Ergebnis darf gemergt werden.
