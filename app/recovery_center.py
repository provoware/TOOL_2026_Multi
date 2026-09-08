"""Eigenständige PySide6-Recovery-Zentrale außerhalb der Dashboard-Hauptfläche."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QComboBox, QDialog, QFormLayout, QFrame, QHBoxLayout, QLabel, QMessageBox,
    QPushButton, QTextEdit, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,
)

from app.event_log import EventLogger
from app.recovery_ui import ZOOM_LEVELS, available_areas, filter_events, repetition_summary, technical_details
from app.texts import TextRegistry
from app.ui_standards import apply_global_style, severity_display


class RecoveryCenter(QWidget):
    """Zeigt Diagnose- und Recovery-Ereignisse als einzelnes Werkzeugfenster."""

    def __init__(self, texts: TextRegistry, logger: EventLogger, zoom_percent: int = 100,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.Window)
        self.texts, self.logger = texts, logger
        self.zoom_percent = zoom_percent
        self._all_events: list[dict] = []
        self._event_by_item: dict[int, dict] = {}
        self.setWindowTitle("Recovery")
        self.resize(1000, 680)
        self.setMinimumSize(760, 520)
        self._build()
        apply_global_style(self, zoom_percent)
        QShortcut(QKeySequence("F5"), self, activated=self.refresh)
        QShortcut(QKeySequence("Escape"), self, activated=self.close)
        self.refresh()

    def _build(self) -> None:
        body = QVBoxLayout(self)
        body.setContentsMargins(18, 18, 18, 18)
        body.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel("Recovery")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        hint = QLabel("Fehler, Ereignisse und Wiederholungen")
        hint.setObjectName("muted")
        header.addWidget(hint)
        header.addStretch(1)
        refresh_button = QPushButton("Aktualisieren")
        refresh_button.clicked.connect(self.refresh)
        header.addWidget(refresh_button)
        body.addLayout(header)

        self.ready = QLabel(f"● {self.texts.get('status.ready', 'System bereit')}")
        self.ready.setObjectName("statusGood")
        body.addWidget(self.ready)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Schweregrad:"))
        self.severity_filter = QComboBox()
        self.severity_filter.addItems(("ALLE", "INFO", "HINWEIS", "WARNUNG", "FEHLER", "KRITISCH", "SCHWER", "ABSTURZ"))
        self.severity_filter.currentTextChanged.connect(self._apply_filters)
        controls.addWidget(self.severity_filter)
        controls.addWidget(QLabel("Bereich:"))
        self.area_filter = QComboBox()
        self.area_filter.currentTextChanged.connect(self._apply_filters)
        controls.addWidget(self.area_filter)
        controls.addWidget(QLabel("Anzeigegröße:"))
        self.zoom_filter = QComboBox()
        self.zoom_filter.addItems([f"{value} %" for value in ZOOM_LEVELS])
        self.zoom_filter.setCurrentText(f"{self.zoom_percent} %")
        self.zoom_filter.currentTextChanged.connect(self._zoom_changed)
        controls.addWidget(self.zoom_filter)
        controls.addStretch(1)
        body.addLayout(controls)

        self.table = QTreeWidget()
        self.table.setColumnCount(5)
        self.table.setHeaderLabels(("Zeit", "Ampel / Schwere", "Bereich", "Wiederholung", "Einfache Erklärung"))
        self.table.setRootIsDecorated(False)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 155)
        self.table.setColumnWidth(1, 145)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 115)
        self.table.itemDoubleClicked.connect(lambda *_args: self.open_selected_event())
        body.addWidget(self.table, 1)

        actions = QHBoxLayout()
        self.open_button = QPushButton("Ausgewähltes Ereignis öffnen")
        self.open_button.clicked.connect(self.open_selected_event)
        actions.addWidget(self.open_button)
        log_button = QPushButton("Alle Ereignisse als Text")
        log_button.clicked.connect(self.show_log)
        actions.addWidget(log_button)
        actions.addStretch(1)
        self.status = QLabel("")
        self.status.setObjectName("muted")
        actions.addWidget(self.status)
        body.addLayout(actions)

    def refresh(self) -> None:
        self._all_events = self.logger.recent(100)
        current = self.area_filter.currentText() or "ALLE"
        self.area_filter.blockSignals(True)
        self.area_filter.clear()
        self.area_filter.addItems(list(available_areas(self._all_events)))
        self.area_filter.setCurrentText(current if self.area_filter.findText(current) >= 0 else "ALLE")
        self.area_filter.blockSignals(False)
        self._apply_filters()

    def _apply_filters(self, *_args: object) -> None:
        self.table.clear()
        self._event_by_item.clear()
        events = filter_events(self._all_events, self.severity_filter.currentText(), self.area_filter.currentText() or "ALLE")
        for event in events:
            severity = str(event.get("severity", "")).upper()
            lamp, color = severity_display(severity)
            count, _first_seen = repetition_summary(event)
            item = QTreeWidgetItem((
                str(event.get("time", ""))[:19].replace("T", " "),
                f"{lamp} {severity}",
                str(event.get("area", "")),
                f"{count}×" if count > 1 else "einmalig",
                str(event.get("summary", "")),
            ))
            item.setForeground(1, QColor(color))
            self.table.addTopLevelItem(item)
            self._event_by_item[id(item)] = event
        if self.table.topLevelItemCount():
            self.table.setCurrentItem(self.table.topLevelItem(0))
        self.status.setText(f"{len(events)} Ereignis(se) passen zum Filter · insgesamt {len(self._all_events)} geladen.")

    def selected_event(self) -> dict | None:
        item = self.table.currentItem()
        return self._event_by_item.get(id(item)) if item is not None else None

    def open_selected_event(self) -> None:
        event = self.selected_event()
        if event is None:
            QMessageBox.information(self, "Kein Ereignis ausgewählt", "Bitte zuerst eine Zeile auswählen.")
            return
        self.show_event_details(event)

    def show_event_details(self, event: dict) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Ereignisdetails")
        dialog.resize(760, 610)
        layout = QVBoxLayout(dialog)
        severity = str(event.get("severity", "")).upper()
        lamp, _color = severity_display(severity)
        title = QLabel(f"{lamp} {severity} · {event.get('area', '')}")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)
        summary = QLabel(str(event.get("summary") or "Keine Erklärung vorhanden."))
        summary.setWordWrap(True)
        layout.addWidget(summary)
        count, first_seen = repetition_summary(event)
        form = QFormLayout()
        for label, value in (
            ("Zeit", str(event.get("time") or "Unbekannt")[:19].replace("T", " ")),
            ("Wiederholungen", str(count)),
            ("Erstes Auftreten", first_seen[:19].replace("T", " ")),
            ("Schutz", str(event.get("safe_action") or "Keine Angabe")),
            ("Nächster Schritt", str(event.get("next_step") or "Keine Angabe")),
        ):
            value_label = QLabel(value)
            value_label.setWordWrap(True)
            form.addRow(f"{label}:", value_label)
        layout.addLayout(form)
        tech = QTextEdit()
        tech.setReadOnly(True)
        tech.setPlainText(technical_details(event))
        tech.hide()
        layout.addWidget(tech, 1)
        toggle = QPushButton("Technische Details anzeigen")
        def toggle_technical() -> None:
            tech.setVisible(not tech.isVisible())
            toggle.setText("Technische Details ausblenden" if tech.isVisible() else "Technische Details anzeigen")
        toggle.clicked.connect(toggle_technical)
        layout.addWidget(toggle)
        close_button = QPushButton("Schließen")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button, alignment=Qt.AlignRight)
        apply_global_style(dialog, self.zoom_percent)
        dialog.exec()

    def show_log(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(self.texts.get("log.title", "Debug/Log – alle Ereignisse"))
        dialog.resize(840, 540)
        layout = QVBoxLayout(dialog)
        text = QTextEdit()
        text.setReadOnly(True)
        events = filter_events(self._all_events, self.severity_filter.currentText(), self.area_filter.currentText() or "ALLE")
        text.setPlainText("\n\n".join(self.logger.human_report(event) for event in events)
                          or self.texts.get("dashboard.empty", "Keine passenden Ereignisse vorhanden."))
        layout.addWidget(text)
        apply_global_style(dialog, self.zoom_percent)
        dialog.exec()

    def _zoom_changed(self, value: str) -> None:
        try:
            self.set_zoom(int(value.split()[0]))
        except (ValueError, IndexError):
            return

    def set_zoom(self, percent: int) -> None:
        if percent not in ZOOM_LEVELS:
            return
        self.zoom_percent = percent
        self.zoom_filter.blockSignals(True)
        self.zoom_filter.setCurrentText(f"{percent} %")
        self.zoom_filter.blockSignals(False)
        apply_global_style(self, percent)
