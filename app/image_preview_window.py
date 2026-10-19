"""Bildvorschau mit lokalen Listen, Größenbegrenzung und skaliertem Qt-Bildleser."""
from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QImageReader, QPixmap
from PySide6.QtWidgets import (
    QFileDialog, QHBoxLayout, QLabel, QListWidget, QScrollArea,
)
from app import media_files as media, module_archive as archive
from app.atomic_io import atomic_write_json
from app.module_widgets import ModuleWindow, button

MAX_IMAGES = 200


def _image_list_file(root):
    root = Path(root)
    if (root / "daten").is_symlink() or (root / "daten/medien").is_symlink():
        raise ValueError("Bildlistenordner darf kein Link sein.")
    return root / "daten/medien/bilder.json"


def validate_images(raw):
    if not isinstance(raw, dict) or set(raw) != {"schema_version", "paths"} or raw["schema_version"] != 1:
        raise ValueError("Unbekannte Bildliste.")
    paths = raw["paths"]
    if not isinstance(paths, list) or len(paths) > MAX_IMAGES:
        raise ValueError("Höchstens 200 Bilder pro Liste.")
    names = [str(media.media_path(p, media.IMAGE, exists=False)) for p in paths]
    if len({p.casefold() for p in names}) != len(names):
        raise ValueError("Doppelte Bilddatei.")
    return {"schema_version": 1, "paths": names}


class ImagePreviewWindow(ModuleWindow):
    def __init__(self, root, zoom_percent=100, parent=None):
        self.module = "bildvorschau"
        self.paths = []
        self.current = -1
        self.pixmap = None
        super().__init__(root, "Bildvorschau · lokale Fotos", zoom_percent, parent)
        self.listing = QListWidget()
        self.listing.setMaximumHeight(160)
        self.listing.setAccessibleName("Gespeicherte lokale Bilder")
        self.listing.currentRowChanged.connect(self.show_at)
        self.outer.addWidget(self.listing)
        row = QHBoxLayout()
        button(row, "Bilder auswählen", self.choose_images)
        button(row, "Vorheriges", self.previous)
        button(row, "Nächstes", self.next)
        self.outer.addLayout(row)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.label = QLabel("Bilder wählen")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setAccessibleName("Skalierte Bildvorschau")
        self.scroll.setWidget(self.label)
        self.outer.addWidget(self.scroll, 1)
        self.refresh()
        self.finish()

    def snapshot(self):
        return tuple(self.paths)

    def load_state(self):
        target = _image_list_file(self.root)
        if not target.exists():
            return {"schema_version": 1, "paths": []}
        if target.is_symlink() or target.stat().st_size > 200_000:
            raise ValueError("Bildliste beschädigt oder zu groß.")
        return validate_images(json.loads(target.read_text(encoding="utf-8")))

    def refresh(self):
        try:
            self.paths = self.load_state()["paths"]
            self.render()
        except (OSError, ValueError) as error:
            self.error("Bildliste nicht lesbar", error)

    def save(self):
        try:
            atomic_write_json(_image_list_file(self.root), validate_images(
                {"schema_version": 1, "paths": self.paths}))
            self.remember()
            return True
        except (OSError, ValueError) as error:
            self.error("Bildliste nicht gespeichert", error)
            return False

    def render(self):
        self.listing.blockSignals(True)
        self.listing.clear()
        self.listing.addItems([Path(p).name for p in self.paths])
        self.listing.blockSignals(False)
        if self.paths:
            self.listing.setCurrentRow(0)
            self.show_at(0)
        else:
            self.current = -1
            self.pixmap = None
            self.label.setText("Noch keine Bilder ausgewählt.")

    def choose_images(self):
        selected, _ = QFileDialog.getOpenFileNames(
            self, "Bilddateien hinzufügen", "", "Bilder (*.png *.jpg *.jpeg *.bmp *.webp)")
        if not selected:
            return
        previous = list(self.paths)
        try:
            names = [str(media.media_path(p, media.IMAGE)) for p in selected]
            self.paths = validate_images({
                "schema_version": 1, "paths": list(dict.fromkeys([*self.paths, *names]))
            })["paths"]
            if self.save():
                self.render()
            else:
                self.paths = previous
        except (OSError, ValueError) as error:
            self.paths = previous
            self.error("Bilder nicht übernommen", error)

    def show_at(self, row):
        if row < 0 or row >= len(self.paths):
            return
        try:
            source = media.media_path(self.paths[row], media.IMAGE)
            if source.stat().st_size > media.MAX_IMAGE:
                raise ValueError("Bild ist größer als 25 MB.")
            reader = QImageReader(str(source))
            reader.setAutoTransform(True)
            size = reader.size()
            if (not size.isValid() or size.width() > 16000 or size.height() > 16000
                    or size.width() * size.height() > 40_000_000):
                raise ValueError("Bildabmessungen sind zu groß oder unlesbar.")
            bound = size.scaled(QSize(2200, 2200), Qt.KeepAspectRatio)
            reader.setScaledSize(bound)
            decoded = reader.read()
            if decoded.isNull():
                raise ValueError("Bildformat konnte nicht gelesen werden.")
            self.pixmap = QPixmap.fromImage(decoded)
            self.current = row
            self._fit()
            self.status.setText(f"Bild {row + 1} / {len(self.paths)}: {source.name}")
        except (OSError, ValueError) as error:
            self.pixmap = None
            self.label.setText("Bild kann nicht angezeigt werden.")
            self.error("Bildvorschau fehlgeschlagen", error)

    def _fit(self):
        if self.pixmap is not None:
            self.label.setPixmap(self.pixmap.scaled(
                self.scroll.viewport().size(), Qt.KeepAspectRatio,
                Qt.SmoothTransformation))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "scroll"):
            self._fit()

    def previous(self):
        if self.paths:
            self.listing.setCurrentRow(max(0, self.current - 1))

    def next(self):
        if self.paths:
            self.listing.setCurrentRow(min(len(self.paths) - 1, self.current + 1))

    def export_data(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Bildliste exportieren", "bilder.json", "JSON (*.json)")
        if filename:
            try:
                atomic_write_json(archive.export_target(self.root, filename),
                                  validate_images({"schema_version": 1, "paths": self.paths}))
            except (OSError, ValueError) as error:
                self.error("Bildliste nicht exportiert", error)

    def import_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Bildliste importieren", "", "JSON (*.json)")
        if not filename:
            return
        try:
            source = Path(filename)
            if source.stat().st_size > 200_000:
                raise ValueError("Importdatei ist zu groß.")
            items = validate_images(json.loads(source.read_text(encoding="utf-8")))
            previous = list(self.paths)
            self.paths = validate_images({"schema_version": 1, "paths":
                     list(dict.fromkeys([*self.paths, *items["paths"]]))})["paths"]
            if self.save():
                self.render()
            else:
                self.paths = previous
        except (OSError, ValueError) as error:
            self.error("Bildliste nicht importiert", error)
