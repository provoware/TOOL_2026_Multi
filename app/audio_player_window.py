"""Lokaler Audioplayer mit gespeicherter Playlist und QtMultimedia."""
from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QFileDialog, QHBoxLayout, QLabel, QListWidget, QMessageBox, QSlider,
)
from app import media_files as store, module_archive as archive
from app.atomic_io import atomic_write_json
from app.module_widgets import ModuleWindow, button


class AudioPlayerWindow(ModuleWindow):
    def __init__(self, root, zoom_percent=100, parent=None):
        self.module = "audio"
        self.paths = []
        super().__init__(root, "Audioplayer · Playlist", zoom_percent, parent)
        self.player = QMediaPlayer(self)
        self.sound = QAudioOutput(self)
        self.player.setAudioOutput(self.sound)
        self.sound.setVolume(0.6)
        self.listing = QListWidget()
        self.listing.setAccessibleName("Playlist der lokalen Audiodateien")
        self.listing.itemDoubleClicked.connect(lambda _item: self.play_selected())
        self.outer.addWidget(self.listing, 1)
        row = QHBoxLayout()
        button(row, "Dateien hinzufügen", self.add_tracks)
        button(row, "Auswahl entfernen", self.remove_selected)
        self.outer.addLayout(row)
        controls = QHBoxLayout()
        button(controls, "◀", self.previous)
        button(controls, "▶", self.play_selected)
        button(controls, "Pause", self.pause)
        button(controls, "Stopp", self.stop)
        button(controls, "▶▶", self.next)
        self.outer.addLayout(controls)
        self.progress = QSlider(Qt.Horizontal)
        self.progress.setAccessibleName("Wiedergabeposition")
        self.progress.setRange(0, 0)
        self.progress.sliderMoved.connect(self.player.setPosition)
        self.outer.addWidget(self.progress)
        level = QHBoxLayout()
        level.addWidget(QLabel("Lautstärke"))
        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(60)
        self.volume.valueChanged.connect(lambda v: self.sound.setVolume(v / 100))
        level.addWidget(self.volume)
        self.outer.addLayout(level)
        self.player.positionChanged.connect(self.progress.setValue)
        self.player.durationChanged.connect(self.progress.setMaximum)
        self.player.mediaStatusChanged.connect(self._media_status)
        self.player.errorOccurred.connect(self._media_error)
        self.refresh()
        self.finish()

    def snapshot(self):
        return tuple(self.paths)

    def refresh(self):
        try:
            self.paths = store.load_playlist(self.root)["paths"]
            self._render()
        except (OSError, ValueError) as error:
            self.error("Playlist nicht lesbar", error)

    def _render(self):
        self.listing.clear()
        for path in self.paths:
            name = Path(path).name
            self.listing.addItem(name if Path(path).is_file() else name + " (Datei fehlt)")

    def _save(self):
        store.save_playlist(self.root, {"schema_version": 1, "paths": self.paths})
        self.remember()

    def save(self):
        try:
            self._save()
            return True
        except (OSError, ValueError) as error:
            self.error("Playlist nicht gespeichert", error)
            return False

    def add_tracks(self):
        chosen, _ = QFileDialog.getOpenFileNames(
            self, "Lokale Audiodateien wählen", "", "Audio (*.mp3 *.ogg *.wav *.flac *.m4a *.aac)")
        if not chosen:
            return
        try:
            entries = [str(store.media_path(path, store.AUDIO)) for path in chosen]
            merged = list(dict.fromkeys([*self.paths, *entries]))
            state = store.validate_playlist({"schema_version": 1, "paths": merged})
            self.paths = state["paths"]
            if self.save():
                self._render()
        except (OSError, ValueError) as error:
            self.error("Audiodateien nicht hinzugefügt", error)

    def remove_selected(self):
        row = self.listing.currentRow()
        if row < 0:
            return
        previous = list(self.paths)
        self.paths.pop(row)
        if self.save():
            self.stop()
            self._render()
        else:
            self.paths = previous

    def play_selected(self):
        row = self.listing.currentRow()
        if row < 0 and self.paths:
            row = 0
            self.listing.setCurrentRow(0)
        if row < 0:
            self.status.setText("Bitte zunächst Musikdateien auswählen.")
            return
        try:
            local = store.media_path(self.paths[row], store.AUDIO)
            self.player.setSource(QUrl.fromLocalFile(str(local)))
            self.player.play()
        except (OSError, ValueError) as error:
            self.error("Musikdatei nicht spielbar", error)

    def previous(self):
        if self.paths:
            self.listing.setCurrentRow(max(0, self.listing.currentRow() - 1))
            self.play_selected()

    def next(self):
        if self.paths:
            self.listing.setCurrentRow((self.listing.currentRow() + 1) % len(self.paths))
            self.play_selected()

    def pause(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def stop(self):
        self.player.stop()

    def _media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia and self.paths:
            self.next()

    def _media_error(self, error, message):
        if error != QMediaPlayer.Error.NoError:
            self.status.setText("Wiedergabefehler: " + (message or "Audiodatei nicht lesbar."))

    def export_data(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Playlist exportieren", "playlist.json", "JSON (*.json)")
        if filename:
            try:
                atomic_write_json(archive.export_target(self.root, filename),
                                  store.validate_playlist({"schema_version": 1, "paths": self.paths}))
            except (OSError, ValueError) as error:
                self.error("Playlistexport fehlgeschlagen", error)

    def import_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Playlist importieren", "", "JSON (*.json)")
        if not filename:
            return
        try:
            source = Path(filename)
            if source.stat().st_size > 250_000:
                raise ValueError("Playlistdatei zu groß.")
            incoming = store.validate_playlist(json.loads(source.read_text(encoding="utf-8")))
            merged = list(dict.fromkeys([*self.paths, *incoming["paths"]]))
            data = store.validate_playlist({"schema_version": 1, "paths": merged})
            if QMessageBox.question(self, "Import bestätigen",
                    f"{len(incoming['paths'])} Einträge prüfen und ergänzen?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                self.paths = data["paths"]
                if self.save():
                    self._render()
        except (OSError, ValueError) as error:
            self.error("Playlistimport fehlgeschlagen", error)

    def closeEvent(self, event):
        self.stop()
        super().closeEvent(event)
