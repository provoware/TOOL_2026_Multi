"""Profilbasierter Kreativ-Zufallsgenerator mit lokalem Archiv und Verlauf."""
from __future__ import annotations

from pathlib import Path
from datetime import date

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDateEdit, QFileDialog, QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QScrollArea,
    QSpinBox, QTextEdit, QVBoxLayout, QWidget,
)

from app.genre_random import (
    QUICK_AMOUNTS, archive_export, archive_import, generate, history_load,
    preset_save, presets_load, rename_value,
)
from app.genre_favorites import (
    favorite_values, set_favorite, monthly_report_text, export_monthly_report,
)
from app.profile_store import CATEGORIES, add_profile, add_values, load_profiles, remove_value
from app.ui_standards import SPACING, apply_global_style


class GenreRandomWindow(QWidget):
    """Eine einzige Datenquelle für Profile, Kategorien und Generator."""

    def __init__(self, root: Path, zoom_percent: int = 100, parent: QWidget | None = None):
        super().__init__(parent, Qt.Window)
        self.root, self.zoom_percent = root, zoom_percent
        self.setWindowTitle("Genres & Kreativ-Zufall")
        self.resize(1100, 760)
        self.setMinimumSize(820, 570)
        self._build()
        self.set_zoom(zoom_percent)
        self.refresh()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        title = QLabel("Genres & Kreativ-Zufall · Profile und Archiv")
        title.setObjectName("sectionTitle")
        outer.addWidget(title)
        line = QHBoxLayout()
        line.addWidget(QLabel("Profil:"))
        self.profile_combo = QComboBox()
        self.profile_combo.setAccessibleName("Aktives Profil für Archiv und Zufall")
        self.profile_combo.currentTextChanged.connect(self._refresh_archive)
        line.addWidget(self.profile_combo, 1)
        self.new_profile = QLineEdit()
        self.new_profile.setPlaceholderText("Neuer Profilname, z. B. Chill")
        self.new_profile.setAccessibleName("Neuen Profilnamen eingeben")
        line.addWidget(self.new_profile)
        self._button(line, "Profil anlegen", self.create_profile)
        outer.addLayout(line)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        body = QWidget()
        column = QVBoxLayout(body)

        archive_frame = QFrame()
        archive_frame.setObjectName("innerCard")
        archive_box = QVBoxLayout(archive_frame)
        archive_box.addWidget(QLabel("Archiv · einzelne Begriffe kommagetrennt eingeben"))
        archive_choice = QHBoxLayout()
        archive_choice.addWidget(QLabel("Kategorie:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        self.category_combo.currentTextChanged.connect(self._refresh_archive)
        archive_choice.addWidget(self.category_combo)
        self.count_label = QLabel("0 Einträge")
        archive_choice.addWidget(self.count_label)
        archive_choice.addStretch()
        archive_box.addLayout(archive_choice)
        self.filter_entry = QLineEdit()
        self.filter_entry.setPlaceholderText("Archiv durchsuchen …")
        self.filter_entry.textChanged.connect(self._refresh_archive)
        archive_box.addWidget(self.filter_entry)
        self.archive_list = QListWidget()
        self.archive_list.setAccessibleName("Alphabetisches Archiv der ausgewählten Kategorie")
        archive_box.addWidget(self.archive_list)
        input_row = QHBoxLayout()
        self.value_entry = QLineEdit()
        self.value_entry.setPlaceholderText("z. B. Hard Techno, Acid Techno, Schranz")
        self.value_entry.setAccessibleName("Einen oder mehrere kommagetrennte Archivbegriffe eingeben")
        self.value_entry.returnPressed.connect(self.add_entries)
        input_row.addWidget(self.value_entry, 1)
        self._button(input_row, "Hinzufügen", self.add_entries)
        self._button(input_row, "Umbenennen", self.rename_entry)
        self._button(input_row, "Entfernen", self.delete_entry)
        self._button(input_row, "☆ / ★ Favorit", self.toggle_favorite)
        archive_box.addLayout(input_row)
        io = QHBoxLayout()
        self._button(io, "Archiv als JSON exportieren", self.export_archive)
        self._button(io, "JSON importieren", self.import_archive)
        archive_box.addLayout(io)
        column.addWidget(archive_frame)

        random_frame = QFrame()
        random_frame.setObjectName("innerCard")
        generator_box = QVBoxLayout(random_frame)
        generator_box.addWidget(QLabel("Suno-Stilgenerator · Mengen pro Kategorie festlegen"))
        grid = QGridLayout()
        grid.addWidget(QLabel("Kategorie"), 0, 0)
        grid.addWidget(QLabel("Menge"), 0, 1)
        grid.addWidget(QLabel("Schnellauswahl"), 0, 2)
        self.spins = {}
        for row, category in enumerate(CATEGORIES, start=1):
            grid.addWidget(QLabel(category), row, 0)
            spin = QSpinBox()
            spin.setRange(0, 999)
            spin.setAccessibleName(f"Menge für {category}")
            spin.setValue(3 if row <= 3 else 0)
            grid.addWidget(spin, row, 1)
            quick = QHBoxLayout()
            for amount in QUICK_AMOUNTS:
                self._button(quick, str(amount), lambda _=False, s=spin, n=amount: s.setValue(n))
            grid.addLayout(quick, row, 2)
            self.spins[category] = spin
        generator_box.addLayout(grid)
        self.only_favorites = QCheckBox("★ Nur Favoriten für die Zufallsauswahl verwenden")
        self.only_favorites.setAccessibleName("Ausschließlich markierte Favoriten generieren")
        self.only_favorites.setToolTip(
            "Berücksichtigt nur die mit ★ gekennzeichneten Begriffe im gewählten Profil.")
        generator_box.addWidget(self.only_favorites)
        presets = QHBoxLayout()
        for number in range(3):
            self._button(presets, f"Vorlage {number + 1} laden",
                         lambda _=False, n=number: self.load_preset(n))
            self._button(presets, f"Vorlage {number + 1} speichern",
                         lambda _=False, n=number: self.save_preset(n))
        generator_box.addLayout(presets)
        self.generate_button = QPushButton("🎲 Suno-Stiltext generieren und kopieren")
        self.generate_button.setObjectName("primaryButton")
        self.generate_button.clicked.connect(self.generate_result)
        generator_box.addWidget(self.generate_button)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setAccessibleName("Suno-kompatibler Stiltext, kommagetrennt")
        self.output.setPlaceholderText("Für Suno: direkt in »Styles / Style of Music« einfügen. Keine Liedtext-Tags.")
        generator_box.addWidget(self.output)
        self._button(generator_box, "Ergebnis erneut kopieren", self.copy_result)
        column.addWidget(random_frame)

        history_frame = QFrame()
        history_frame.setObjectName("innerCard")
        history_box = QVBoxLayout(history_frame)
        history_box.addWidget(QLabel("Verlauf · dauerhaft gespeicherte Generierungen"))
        self.history_filter = QLineEdit()
        self.history_filter.setPlaceholderText("Verlauf durchsuchen …")
        self.history_filter.textChanged.connect(self.refresh_history)
        history_box.addWidget(self.history_filter)
        self.history_list = QListWidget()
        self.history_list.setAccessibleName("Gespeicherte Zufallsergebnisse mit Zeitstempel")
        history_box.addWidget(self.history_list)
        self._button(history_box, "Markiertes Ergebnis kopieren", self.copy_history)
        column.addWidget(history_frame)

        stats_frame = QFrame()
        stats_frame.setObjectName("innerCard")
        stats_box = QVBoxLayout(stats_frame)
        stats_box.addWidget(QLabel("Genres-Statistik · Monatsauswertung am Stichtag"))
        stats_row = QHBoxLayout()
        stats_row.addWidget(QLabel("Stichtag:"))
        self.month_cutoff = QDateEdit()
        self.month_cutoff.setCalendarPopup(True)
        self.month_cutoff.setDate(QDate.currentDate())
        self.month_cutoff.setDisplayFormat("dd.MM.yyyy")
        self.month_cutoff.setAccessibleName("Stichtag für die monatliche Genres-Auswertung")
        stats_row.addWidget(self.month_cutoff)
        self._button(stats_row, "ⓘ Auswertung erklärt", self.report_help)
        self._button(stats_row, "Monat ansehen", self.report_preview)
        self._button(stats_row, "Monat als TXT exportieren", self.report_export)
        stats_box.addLayout(stats_row)
        stats_box.addWidget(QLabel(
            "Ausgewertet werden nur Genre-Zufallsergebnisse vom Monatsanfang bis zum gewählten Tag."))
        column.addWidget(stats_frame)

        scroll.setWidget(body)
        outer.addWidget(scroll, 1)
        self.status = QLabel("Bereit. Profil wählen, Mengen einstellen und generieren.")
        self.status.setWordWrap(True)
        outer.addWidget(self.status)
        self._button(outer, "Schließen", self.close)

    @staticmethod
    def _button(layout, text: str, action) -> QPushButton:
        button = QPushButton(text)
        button.clicked.connect(action)
        layout.addWidget(button)
        return button

    def _message(self, title: str, error: Exception) -> None:
        self.status.setText(f"{title}: {error} · Bestehende Daten bleiben erhalten.")
        QMessageBox.warning(self, title, f"Es wurde nichts verändert.\n\nGrund: {error}")

    def set_zoom(self, percent: int) -> None:
        self.zoom_percent = percent
        apply_global_style(self, percent)

    def refresh(self) -> None:
        current = self.profile_combo.currentText()
        try:
            profiles = load_profiles(self.root)
        except Exception as error:
            self._message("Profile nicht lesbar", error)
            return
        from PySide6.QtCore import QSignalBlocker
        with QSignalBlocker(self.profile_combo):
            self.profile_combo.clear()
            self.profile_combo.addItems(sorted(profiles, key=str.casefold))
            if current in profiles:
                self.profile_combo.setCurrentText(current)
        self._refresh_archive()
        self.refresh_history()

    def _refresh_archive(self, *_args) -> None:
        profile, category = self.profile_combo.currentText(), self.category_combo.currentText()
        self.archive_list.clear()
        if not profile or category not in CATEGORIES:
            self.count_label.setText("0 Einträge")
            return
        try:
            entries = load_profiles(self.root)[profile][category]
        except Exception as error:
            self._message("Archiv nicht lesbar", error)
            return
        self.count_label.setText(f"{len(entries)} Einträge")
        text = self.filter_entry.text().casefold()
        try:
            stars = {v.casefold() for v in favorite_values(self.root, profile, category)}
        except Exception as error:
            self._message("Favoriten nicht lesbar", error)
            return
        for entry in sorted((entry for entry in entries if text in entry.casefold()), key=str.casefold):
            from PySide6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(("★ " if entry.casefold() in stars else "☆ ") + entry)
            item.setData(Qt.UserRole, entry)
            self.archive_list.addItem(item)

    def create_profile(self) -> None:
        try:
            name = add_profile(self.root, self.new_profile.text())
        except Exception as error:
            self._message("Profil konnte nicht angelegt werden", error)
            return
        self.new_profile.clear()
        self.refresh()
        self.profile_combo.setCurrentText(name)

    def add_entries(self) -> None:
        try:
            added = add_values(self.root, self.profile_combo.currentText(),
                               self.category_combo.currentText(), self.value_entry.text())
        except Exception as error:
            self._message("Einträge nicht gespeichert", error)
            return
        self.value_entry.clear()
        self._refresh_archive()
        self.status.setText(f"{len(added)} neue Einträge gespeichert; bestehende Duplikate übersprungen.")

    def rename_entry(self) -> None:
        selected = self.archive_list.currentItem()
        if selected is None:
            self.status.setText("Bitte zuerst einen Eintrag markieren.")
            return
        try:
            rename_value(self.root, self.profile_combo.currentText(),
                         self.category_combo.currentText(), selected.data(Qt.UserRole), self.value_entry.text())
        except Exception as error:
            self._message("Eintrag nicht bearbeitet", error)
            return
        self.value_entry.clear()
        self._refresh_archive()

    def delete_entry(self) -> None:
        selected = self.archive_list.currentItem()
        if selected is None:
            self.status.setText("Bitte zuerst einen Eintrag markieren.")
            return
        if QMessageBox.question(self, "Eintrag entfernen",
                                f"„{selected.data(Qt.UserRole)}“ wirklich entfernen?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return
        try:
            remove_value(self.root, self.profile_combo.currentText(),
                         self.category_combo.currentText(), selected.data(Qt.UserRole))
        except Exception as error:
            self._message("Eintrag nicht entfernt", error)
            return
        self._refresh_archive()

    def export_archive(self) -> None:
        target, _ = QFileDialog.getSaveFileName(self, "Archiv exportieren", "profile-export.json", "JSON (*.json)")
        if not target:
            return
        try:
            archive_export(self.root, Path(target))
            self.status.setText("Archiv wurde vollständig exportiert.")
        except Exception as error:
            self._message("Export fehlgeschlagen", error)

    def import_archive(self) -> None:
        source, _ = QFileDialog.getOpenFileName(self, "Archiv importieren", "", "JSON (*.json)")
        if not source:
            return
        try:
            result = archive_import(self.root, Path(source))
        except Exception as error:
            self._message("Import fehlgeschlagen", error)
            return
        self.refresh()
        self.status.setText(f"{result['profiles']} Profile und {result['values']} Werte ergänzt.")

    def toggle_favorite(self) -> None:
        selected = self.archive_list.currentItem()
        if selected is None:
            self.status.setText("Bitte zuerst einen Archivbegriff markieren.")
            return
        profile, category = self.profile_combo.currentText(), self.category_combo.currentText()
        value = selected.data(Qt.UserRole)
        try:
            was_favorite = any(v.casefold() == value.casefold()
                               for v in favorite_values(self.root, profile, category))
            set_favorite(self.root, profile, category, value, not was_favorite)
        except Exception as error:
            self._message("Favorit konnte nicht geändert werden", error)
            return
        self._refresh_archive()
        self.status.setText(
            f"{'★ Als Favorit markiert' if not was_favorite else '☆ Favorit aufgehoben'}: {value}")

    def _report_date(self) -> date:
        return self.month_cutoff.date().toPython()

    def report_help(self) -> None:
        QMessageBox.information(
            self, "Genres-Monatsauswertung",
            "Hier werden ausschließlich die gespeicherten Zufallsergebnisse im Genres-Modul "
            "vom 1. des gewählten Monats bis zum Stichtag (einschließlich) gezählt.\n\n"
            "Das Ergebnis enthält die Anzahl der Ziehungen, verwendete Profile, Kategorien, "
            "Favoriten-Zufallsziehungen und häufig gezogene Begriffe.\n\n"
            "Mit „Monat ansehen“ erscheint ein Vorschaufenster. "
            "„Monat als TXT exportieren“ speichert nur nach deiner Dateiauswahl "
            "einen gut lesbaren Bericht. GitHub-Projekte gehören nicht zu dieser Auswertung.")

    def report_preview(self) -> None:
        try:
            text = monthly_report_text(self.root, self._report_date())
        except Exception as error:
            self._message("Monatsauswertung nicht lesbar", error)
            return
        QMessageBox.information(self, "Genres-Monatsauswertung", text)

    def report_export(self) -> None:
        cutoff = self._report_date()
        target, _ = QFileDialog.getSaveFileName(
            self, "Monatsauswertung als Textdatei speichern",
            f"genres-auswertung-{cutoff:%Y-%m}-{cutoff:%d}.txt",
            "Textdatei (*.txt)")
        if not target:
            self.status.setText("Auswertung nicht exportiert: Dateiauswahl abgebrochen.")
            return
        try:
            export_monthly_report(self.root, cutoff, Path(target))
        except Exception as error:
            self._message("Monatsbericht nicht gespeichert", error)
            return
        self.status.setText(f"Genres-Monatsbericht bis {cutoff:%d.%m.%Y} gespeichert.")

    def amounts(self) -> dict[str, int]:
        return {cat: spin.value() for cat, spin in self.spins.items()}

    def save_preset(self, number: int) -> None:
        try:
            preset_save(self.root, number, self.amounts())
        except Exception as error:
            self._message("Vorlage nicht gespeichert", error)
            return
        self.status.setText(f"Mengenvorlage {number + 1} gespeichert.")

    def load_preset(self, number: int) -> None:
        try:
            values = presets_load(self.root)[number]
        except Exception as error:
            self._message("Vorlage nicht lesbar", error)
            return
        for cat in CATEGORIES:
            self.spins[cat].setValue(values[cat])
        self.status.setText(f"Mengenvorlage {number + 1} geladen.")

    def generate_result(self) -> None:
        profile = self.profile_combo.currentText()
        if not profile:
            self.status.setText("Bitte zuerst ein Profil auswählen.")
            return
        try:
            entry = generate(self.root, profile, self.amounts(),
                             favorites_only=self.only_favorites.isChecked())
        except Exception as error:
            self._message("Zufall nicht generiert", error)
            return
        self.output.setPlainText(entry["output"])
        QApplication.clipboard().setText(entry["output"])
        self.refresh_history()
        kind = "Favoriten-Zufall" if self.only_favorites.isChecked() else "Gesamtes Archiv"
        self.status.setText(f"{kind}: Stiltext gespeichert und kopiert · in Sunos Feld »Styles« einfügen.")

    def copy_result(self) -> None:
        QApplication.clipboard().setText(self.output.toPlainText())
        self.status.setText("Ergebnis kopiert.")

    def refresh_history(self, *_args) -> None:
        self.history_list.clear()
        try:
            entries = history_load(self.root)
        except Exception as error:
            self._message("Verlauf nicht lesbar", error)
            return
        needle = self.history_filter.text().casefold()
        for entry in reversed(entries):
            mode = " ★ Favoriten" if entry.get("favorites_only") else ""
            label = f"{entry['timestamp']} | {entry['profile']}{mode} | {entry['output']}"
            if needle in label.casefold():
                self.history_list.addItem(label)
                self.history_list.item(self.history_list.count() - 1).setData(
                    Qt.UserRole, entry["output"])

    def copy_history(self) -> None:
        item = self.history_list.currentItem()
        if item is None:
            self.status.setText("Bitte zuerst einen Verlaufseintrag markieren.")
            return
        QApplication.clipboard().setText(item.data(Qt.UserRole))
        self.status.setText("Verlaufsergebnis kopiert.")
