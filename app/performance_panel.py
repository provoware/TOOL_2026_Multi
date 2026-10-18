"""Ein-/Ausschalten, Vorschau und ausdrücklicher Export der lokalen Leistungsmessung."""
from __future__ import annotations

import json
from pathlib import Path
from PySide6.QtCore import QSignalBlocker
from PySide6.QtWidgets import (QCheckBox, QFileDialog, QHBoxLayout, QLabel,
                              QMessageBox, QSpinBox, QTabWidget, QTextEdit, QVBoxLayout, QWidget)
from app.atomic_io import atomic_write_text
from app.module_archive import export_target
from app.module_widgets import button, scroll_panel, t
from app.performance import current, suppressed
from app.performance_report import report


class PerformancePanel(QWidget):
    def __init__(self, root, parent=None):
        super().__init__(parent)
        self.tracker = current(root)
        outer = QVBoxLayout(self)
        scroll, controls = scroll_panel()
        outer.addWidget(scroll, 1)
        explanation = QLabel(t('performance_hint',
            'Die zusätzliche Messung ist freiwillig und zunächst aus. Erfasst werden nur feste technische Aktionen, Laufzeiten, Zähler und Bytezahlen. Texte, Titel und Zwischenablage werden nicht erfasst. Es gibt keine automatische Übertragung.'))
        explanation.setWordWrap(True)
        controls.addWidget(explanation)
        self.enabled = QCheckBox(t('performance_enable', 'Lokale Leistungsmessung einschalten'))
        self.enabled.setAccessibleName(self.enabled.text())
        self.enabled.setChecked(self.tracker.enabled)
        self.enabled.toggled.connect(self._configure)
        controls.addWidget(self.enabled)
        row = QHBoxLayout()
        row.addWidget(QLabel(t('performance_retention', 'Messdaten aufbewahren (Tage):')))
        self.retention = QSpinBox()
        self.retention.setRange(1, 30)
        self.retention.setValue(self.tracker.retention)
        self.retention.setAccessibleName(t('performance_retention', 'Messdaten aufbewahren (Tage):'))
        self.retention.valueChanged.connect(self._configure)
        row.addWidget(self.retention)
        controls.addLayout(row)
        row = QHBoxLayout()
        row.addWidget(QLabel(t('performance_days', 'Bericht: letzte Tage')))
        self.days = QSpinBox()
        self.days.setRange(1, 30)
        self.days.setValue(7)
        self.days.setAccessibleName(t('performance_days', 'Bericht: letzte Tage'))
        self.days.valueChanged.connect(self.refresh)
        row.addWidget(self.days)
        controls.addLayout(row)
        self.groups = {}
        for label, operations in [
                (t('performance_loads', 'Ladezeiten'), ('app.start', 'module.open', 'archive.load')),
                (t('performance_writes', 'Dateischreibzugriffe'), ('file.write',)),
                (t('performance_saves', 'Speicherversuche'), ('save.attempt',))]:
            check = QCheckBox(label)
            check.setChecked(True)
            check.toggled.connect(self.refresh)
            controls.addWidget(check)
            self.groups[check] = operations
        self.previews = QTabWidget()
        self.previews.setMinimumHeight(220)
        self.summary = QTextEdit()
        self.summary.setReadOnly(True)
        self.summary.setAccessibleName(t('performance_summary', 'Tagesübersicht der Leistungsmessung'))
        self.json_preview = QTextEdit()
        self.json_preview.setReadOnly(True)
        self.json_preview.setAccessibleName(t('performance_json', 'Bereinigte JSON-Exportvorschau'))
        self.previews.addTab(self.summary, t('performance_summary_short', 'Übersicht'))
        self.previews.addTab(self.json_preview, t('performance_json_short', 'JSON-Vorschau'))
        controls.addWidget(self.previews, 1)
        row = QHBoxLayout()
        button(row, t('refresh', 'Aktualisieren'), self.refresh)
        button(row, t('performance_export', 'Gewählte Messdaten exportieren'), self.export)
        controls.addLayout(row)
        button(controls, t('performance_delete', 'Alle Leistungsdaten löschen und Messung ausschalten'), self.clear)
        note = QLabel(t('performance_note',
            'Messdaten werden höchstens alle 60 Sekunden und beim regulären Beenden gesammelt gespeichert. Bis zu eine Minute kann bei einem Absturz fehlen. Ausschalten behält vorhandene Messdaten; Löschen entfernt sie. Cache und physische SSD-Schreibmengen werden noch nicht ermittelt.'))
        note.setWordWrap(True)
        controls.addWidget(note)
        self.status = QLabel()
        self.status.setWordWrap(True)
        outer.addWidget(self.status)
        self.refresh()

    def payload(self):
        operations = tuple(op for check, values in self.groups.items() if check.isChecked() for op in values)
        return self.tracker.snapshot(self.days.value(), operations)

    def refresh(self, *_args):
        data = self.payload()
        self.summary.setPlainText(report(data))
        self.json_preview.setPlainText(json.dumps(data, ensure_ascii=False, indent=2))
        state = t('performance_on', 'Messung läuft lokal.') if self.tracker.enabled else t('performance_off', 'Zusätzliche Messung ist aus.')
        self.status.setText(self.tracker.last_error or state)

    def _configure(self, *_args):
        try:
            self.tracker.configure(self.enabled.isChecked(), self.retention.value())
        except Exception as error:
            QMessageBox.warning(self, t('performance_config_failed', 'Messeinstellung nicht gespeichert'), str(error))
            with QSignalBlocker(self.enabled), QSignalBlocker(self.retention):
                self.enabled.setChecked(self.tracker.enabled)
                self.retention.setValue(self.tracker.retention)
        self.refresh()

    def export(self):
        data = self.payload()
        self.refresh()
        target, selected = QFileDialog.getSaveFileName(self, t('performance_export', 'Gewählte Messdaten exportieren'),
                                                       'leistungsbericht.json', 'JSON (*.json);;Text (*.txt)')
        if not target:
            return
        try:
            target = export_target(self.tracker.root, target)
            if Path(target).is_relative_to(self.tracker.root / 'logs'):
                raise ValueError(t('performance_export_path', 'Bitte außerhalb des Protokollordners exportieren.'))
            text = report(data) if '*.txt' in selected else json.dumps(data, ensure_ascii=False, indent=2) + '\n'
            with suppressed():
                atomic_write_text(target, text)
            self.status.setText(t('performance_exported', 'Die angezeigte Auswahl wurde exportiert. Es wurde nichts hochgeladen.'))
        except Exception as error:
            QMessageBox.warning(self, t('export_failed', 'Export fehlgeschlagen'), str(error))

    def clear(self):
        if QMessageBox.question(self, t('performance_delete_short', 'Leistungsdaten löschen'),
                                t('performance_delete_confirm', 'Alle zusätzlichen Leistungsdaten löschen und die Messung ausschalten? Arbeitsdaten und Fehlerprotokolle bleiben erhalten.'),
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return
        try:
            self.tracker.clear()
            with QSignalBlocker(self.enabled):
                self.enabled.setChecked(False)
            self.refresh()
        except Exception as error:
            QMessageBox.warning(self, t('performance_delete_failed', 'Leistungsdaten nicht gelöscht'), str(error))
