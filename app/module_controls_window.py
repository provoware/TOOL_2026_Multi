"""Echte Bediensteuerung bekannter Module ohne Fremdcode und ohne Datenlöschung."""
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)
from app import module_contracts
from app.ui_standards import apply_global_style


class ModuleControlsWindow(QWidget):
    def __init__(self, root, zoom_percent=100, can_disable=None, on_saved=None, parent=None):
        super().__init__(parent, Qt.Window)
        self.root = Path(root)
        self.zoom_percent = zoom_percent
        self.can_disable = can_disable or (lambda _id: True)
        self.on_saved = on_saved or (lambda: None)
        self.setWindowTitle("Module verwalten")
        self.resize(650, 550)
        self.setMinimumSize(490, 390)
        layout = QVBoxLayout(self)
        headline = QLabel("Zusatzmodule ein- und ausschalten")
        headline.setWordWrap(True)
        layout.addWidget(headline)
        help_text = QLabel(
            "Abschalten sperrt den Start des Moduls über Menü und Tastatur. "
            "Vorhandene Daten bleiben erhalten. Bitte geöffnete Modulfenster vorher schließen."
        )
        help_text.setWordWrap(True)
        layout.addWidget(help_text)
        self.checks = {}
        definitions = {d.module_id: d for d in module_contracts.BUILTIN_MODULES}
        for name in module_contracts.OPTIONAL_MODULES:
            check = QCheckBox(definitions[name].title)
            check.setAccessibleName("Modul " + definitions[name].title + " aktivieren")
            self.checks[name] = check
            layout.addWidget(check)
        layout.addStretch()
        self.status = QLabel("")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        submit = QPushButton("Moduleinstellungen speichern")
        submit.clicked.connect(self.save)
        layout.addWidget(submit)
        close = QPushButton("Schließen")
        close.clicked.connect(self.close)
        layout.addWidget(close)
        self._baseline = {}
        self.refresh()
        self.set_zoom(zoom_percent)

    def snapshot(self):
        return {key: checkbox.isChecked() for key, checkbox in self.checks.items()}

    def refresh(self):
        try:
            values = {key: module_contracts.is_module_enabled(self.root, key)
                      for key in self.checks}
            for key, enabled in values.items():
                self.checks[key].setChecked(enabled)
            self._baseline = values
            self.status.setText("Moduleinstellungen geladen.")
        except (OSError, ValueError) as error:
            self.status.setText("Modulregister beschädigt: " + str(error))

    def set_zoom(self, percent):
        self.zoom_percent = percent
        apply_global_style(self, percent)

    def save(self):
        desired = self.snapshot()
        for name, enabled in desired.items():
            if not enabled and not self.can_disable(name):
                QMessageBox.warning(
                    self, "Modul ist noch geöffnet",
                    "Bitte das betreffende Modulfenster zuerst schließen. "
                    "Ungespeicherte Änderungen werden nicht verworfen."
                )
                return False
        try:
            module_contracts.set_module_preferences(self.root, desired)
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "Nicht gespeichert", str(error))
            self.status.setText("Modulsteuerung konnte nicht gespeichert werden.")
            return False
        self._baseline = desired
        self.on_saved()
        self.status.setText("Moduleinstellungen gespeichert. Bestehende Daten bleiben erhalten.")
        return True

    def confirm_leave(self):
        if self.snapshot() == self._baseline:
            return True
        answer = QMessageBox.question(
            self, "Ungespeicherte Einstellungen",
            "Änderungen speichern? Ja = speichern, Nein = verwerfen, Abbrechen = bleiben.",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel,
        )
        if answer == QMessageBox.No:
            self.discard_draft()
            return True
        return answer == QMessageBox.Yes and self.save()

    def discard_draft(self):
        for key, enabled in self._baseline.items():
            self.checks[key].setChecked(enabled)

    def closeEvent(self, event):
        if self.confirm_leave():
            event.accept()
        else:
            event.ignore()
