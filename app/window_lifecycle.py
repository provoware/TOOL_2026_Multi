"""Gemeinsame Verwaltung eigenständiger Programmfenster.

Der Ablauf ist ohne fachliche Änderung aus dem Dashboard ausgelagert.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol, TypeVar

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget


class _ManagedWindow(Protocol):
    """Kleinster gemeinsamer Lebenszyklus der vom Dashboard verwalteten Fenster."""

    def isVisible(self) -> bool: ...
    def raise_(self) -> None: ...
    def activateWindow(self) -> None: ...
    def show(self) -> None: ...
    def refresh(self) -> None: ...


ManagedWindowT = TypeVar("ManagedWindowT", bound=_ManagedWindow)


def _prepare_module_window(window: QWidget) -> None:
    """Kennzeichnet Module als eigenständige, nicht-modale Fenster.

    Der Dashboard-Parent bleibt als Besitzbeziehung erhalten, aber ``Qt.Window``
    verhindert ein versehentliches Einbetten in das Hauptfenster. Damit hat jedes
    Modul seine eigene Fensterdekoration und kann unabhängig geschlossen werden.
    """
    window.setWindowFlag(Qt.Window, True)
    window.setWindowModality(Qt.NonModal)
    window.setProperty("provowareModuleWindow", True)


def _show_module_window(window: QWidget) -> None:
    _prepare_module_window(window)
    ensure_on_screen = getattr(window, "ensure_on_screen", None)
    if callable(ensure_on_screen):
        ensure_on_screen()
    window.show()


def _open_managed_window(
    current: ManagedWindowT | None,
    factory: Callable[[], ManagedWindowT],
    *,
    prepare_visible: Callable[[ManagedWindowT], None] | None = None,
    prepare_before_show: Callable[[ManagedWindowT], None] | None = None,
    reuse_hidden: bool = False,
    refresh_after_show: bool = False,
) -> ManagedWindowT:
    """Aktiviert ein sichtbares Fenster oder zeigt exakt den vorgesehenen Ersatz.

    Standardmäßig wird ein nur noch verborgenes Fenster wie bisher durch ein neues
    ersetzt. Fenster mit bewusst persistentem Zustand, derzeit der Kalender, können
    über ``reuse_hidden`` denselben verdeckten Zustand erneut anzeigen.
    """
    if current is not None and current.isVisible():
        if prepare_visible is not None:
            prepare_visible(current)
        current.raise_()
        current.activateWindow()
        current.refresh()
        return current

    window = current if reuse_hidden and current is not None else factory()
    if isinstance(window, QWidget):
        _prepare_module_window(window)
    if prepare_before_show is not None:
        prepare_before_show(window)
    ensure_on_screen = getattr(window, "ensure_on_screen", None)
    if callable(ensure_on_screen):
        ensure_on_screen()
    window.show()
    if refresh_after_show:
        window.refresh()
    return window


@dataclass(frozen=True)
class _ManagedWindowRegistration:
    """Eine aktuelle Fensterreferenz mit zentral definierten gemeinsamen Aktionen."""

    window: QWidget
    apply_zoom: Callable[[int], None] | None = None
    refresh_when_visible: Callable[[], None] | None = None

