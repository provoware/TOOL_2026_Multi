#!/usr/bin/env python3
"""Kleiner CI-Smoke-Test: PySide6 muss tatsächlich mit dem Wayland-QPA-Backend starten."""

from __future__ import annotations

import sys


def main() -> int:
    from PySide6.QtWidgets import QApplication, QLabel

    app = QApplication.instance() or QApplication(sys.argv)
    platform_name = app.platformName().strip().lower()
    if not platform_name.startswith("wayland"):
        print(f"🔴 Qt läuft nicht nativ über Wayland: {platform_name or 'unbekannt'}", file=sys.stderr)
        return 1
    label = QLabel("Provoware Wayland-Smoke")
    label.show()
    app.processEvents()
    if not label.isVisible():
        print("🔴 Qt-Wayland-Fenster wurde nicht sichtbar initialisiert.", file=sys.stderr)
        return 1
    print(f"🟢 Nativer Qt-Wayland-Start erfolgreich: {platform_name}")
    label.close()
    app.processEvents()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
