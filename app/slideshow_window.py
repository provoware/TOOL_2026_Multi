"""Serielle FFmpeg-Verarbeitung: Slideshow und Video mit neuer Audiospur."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import time
from uuid import uuid4

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import (
    QFileDialog, QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QMessageBox, QProgressBar, QSpinBox,
)
from app import media_files as media, media_jobs as jobs, module_archive as archive
from app.media_verify import verify_video
from app import media_queue
from app.atomic_io import atomic_write_json
from app.module_widgets import ModuleWindow, button


class SlideshowWindow(ModuleWindow):
    def __init__(self, root, zoom_percent=100, parent=None):
        self.module = "slideshow"
        self.images = []
        self.audio = ""
        self.video = ""
        self.temp_output = None
        self.final_output = None
        self.estimate = None
        self.cancelled = False
        self.process = None
        self.buffer = ""
        self.progress_seconds = 0
        self.active_queue_id = None
        super().__init__(root, "Video & Slideshow · FFmpeg", zoom_percent, parent)
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.WrapAllRows)
        self.outer.addLayout(form)
        self.mode = QComboBox()
        self.mode.addItems(["Bilder als Video", "Video mit Audio verbinden"])
        form.addRow("Verarbeitung", self.mode)
        self.image_list = QListWidget()
        self.image_list.setMaximumHeight(165)
        self.image_list.setAccessibleName("Bilder in Abspielreihenfolge")
        self.outer.addWidget(self.image_list)
        row = QHBoxLayout()
        button(row, "Bilder hinzufügen", self.add_images)
        button(row, "Bild entfernen", self.remove_image)
        self.outer.addLayout(row)
        self.seconds = QSpinBox()
        self.seconds.setRange(1, 30)
        self.seconds.setValue(5)
        self.seconds.setSuffix(" Sekunden je Bild")
        form.addRow("Bilddauer", self.seconds)
        self.fade = QSpinBox()
        self.fade.setRange(0, 100)
        self.fade.setSuffix(" %")
        self.fade.setAccessibleName("Intensität der Ein- und Ausblendung")
        form.addRow("Ein-/Ausblendung", self.fade)
        row2 = QHBoxLayout()
        self.audio_label = QLineEdit()
        self.audio_label.setReadOnly(True)
        self.audio_label.setPlaceholderText("Optional bei Bildern")
        row2.addWidget(self.audio_label)
        button(row2, "Audio wählen", self.add_audio)
        form.addRow("Tonspur", row2)
        row3 = QHBoxLayout()
        self.video_label = QLineEdit()
        self.video_label.setReadOnly(True)
        row3.addWidget(self.video_label)
        button(row3, "Video wählen", self.add_video)
        form.addRow("Video-Eingabe", row3)
        row4 = QHBoxLayout()
        self.output = QLineEdit()
        self.output.setAccessibleName("Neuer MP4-Ausgabepfad")
        row4.addWidget(self.output)
        button(row4, "Speicherziel", self.choose_output)
        form.addRow("Ausgabe-MP4", row4)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.outer.addWidget(self.progress)
        controls = QHBoxLayout()
        button(controls, "Starten", self.start)
        button(controls, "Einreihen", self.enqueue_current)
        button(controls, "Nächsten Auftrag", self.run_next)
        button(controls, "Abbrechen", self.cancel)
        self.outer.addLayout(controls)
        self.queue_list = QListWidget()
        self.queue_list.setMaximumHeight(105)
        self.queue_list.setAccessibleName("Gespeicherte Videowarteschlange")
        self.outer.addWidget(self.queue_list)
        self.refresh_queue()
        self.outer.addWidget(QLabel(
            "FFmpeg arbeitet einzeln im Hintergrund. Bis zu 20 Bilder, maximal 30 Sekunden je Bild. "
            "Bestehende Ausgabedateien werden nie überschrieben."
        ))
        self.refresh()
        self.finish()

    def snapshot(self):
        return (tuple(self.images), self.audio, self.video, self.mode.currentIndex(),
                self.seconds.value(), self.fade.value(), self.output.text())

    def _preset(self):
        return {"schema_version": 1, "images": list(self.images),
                "audio": self.audio, "video": self.video,
                "mode": self.mode.currentIndex(), "seconds": self.seconds.value()}

    @staticmethod
    def _validate_preset(p):
        if (not isinstance(p, dict) or set(p) != {
                "schema_version", "images", "audio", "video", "mode", "seconds"}
                or p["schema_version"] != 1 or type(p["mode"]) is not int
                or p["mode"] not in (0, 1) or type(p["seconds"]) is not int
                or not 1 <= p["seconds"] <= 30 or not isinstance(p["images"], list)
                or len(p["images"]) > 20 or not isinstance(p["audio"], str)
                or not isinstance(p["video"], str)):
            raise ValueError("Unbekanntes oder zu großes Videoprojekt.")
        result = dict(p)
        result["images"] = [str(media.media_path(v, media.IMAGE, exists=False)) for v in p["images"]]
        if len(set(result["images"])) != len(result["images"]):
            raise ValueError("Doppelte Bildpfade.")
        result["audio"] = str(media.media_path(p["audio"], media.AUDIO, exists=False)) if p["audio"] else ""
        result["video"] = str(media.media_path(p["video"], media.VIDEO, exists=False)) if p["video"] else ""
        return result

    def _preset_path(self):
        root = Path(self.root)
        if (root / "daten").is_symlink() or (root / "daten/medien").is_symlink():
            raise ValueError("Videoprojektordner darf kein Link sein.")
        return root / "daten/medien/slideshow.json"

    def refresh(self):
        target = self._preset_path()
        if target.exists():
            try:
                if target.is_symlink() or target.stat().st_size > 100_000:
                    raise ValueError("Videoprojektdatei zu groß oder verknüpft.")
                self._apply(self._validate_preset(json.loads(target.read_text(encoding="utf-8"))))
            except (OSError, ValueError) as error:
                self.error("Videoprojekt nicht lesbar", error)

    def _apply(self, value):
        self.images = list(value["images"])
        self.audio = value["audio"]
        self.video = value["video"]
        self.mode.setCurrentIndex(value["mode"])
        self.seconds.setValue(value["seconds"])
        self.image_list.clear()
        self.image_list.addItems([Path(p).name for p in self.images])
        self.audio_label.setText(self.audio)
        self.video_label.setText(self.video)
        self.remember()

    def save(self):
        try:
            atomic_write_json(self._preset_path(), self._validate_preset(self._preset()))
            self.remember()
            self.status.setText("Videoprojekt lokal gesichert.")
            return True
        except (OSError, ValueError) as error:
            self.error("Videoprojekt nicht gespeichert", error)
            return False

    def discard_draft(self):
        self._apply({"images": [], "audio": "", "video": "", "mode": 0, "seconds": 5})

    def add_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Bilder auswählen", "", "Bilder (*.jpg *.jpeg *.png *.bmp *.webp)")
        if not files:
            return
        try:
            paths = [str(media.media_path(path, media.IMAGE)) for path in files]
            new = list(dict.fromkeys([*self.images, *paths]))
            if len(new) > 20:
                raise ValueError("Höchstens 20 Bilder je Auftrag.")
            self.images = new
            self.image_list.clear()
            self.image_list.addItems([Path(p).name for p in self.images])
        except (OSError, ValueError) as error:
            self.error("Bilder nicht hinzugefügt", error)

    def remove_image(self):
        index = self.image_list.currentRow()
        if index >= 0:
            self.images.pop(index)
            self.image_list.takeItem(index)

    def add_audio(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Tonspur auswählen", "", "Audio (*.mp3 *.wav *.ogg *.flac *.m4a *.aac)")
        if filename:
            try:
                self.audio = str(media.media_path(filename, media.AUDIO))
                self.audio_label.setText(self.audio)
            except (OSError, ValueError) as error:
                self.error("Tonspur nicht geeignet", error)

    def add_video(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Video auswählen", "", "Videos (*.mp4 *.mov *.mkv *.webm)")
        if filename:
            try:
                self.video = str(media.media_path(filename, media.VIDEO))
                self.video_label.setText(self.video)
            except (OSError, ValueError) as error:
                self.error("Videodatei nicht geeignet", error)

    def choose_output(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Neue MP4-Ausgabe", "video.mp4", "MP4 (*.mp4)")
        if filename:
            self.output.setText(filename)

    def start(self):
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            self.status.setText("Erst den laufenden Auftrag beenden oder abbrechen.")
            return False
        if shutil.which("ffmpeg") is None:
            self.status.setText("FFmpeg fehlt. Bitte die Start-/Diagnosefunktion verwenden.")
            return False
        try:
            if self.mode.currentIndex() == 0:
                args, target, estimate = jobs.slideshow_command(
                    self.root, self.images, self.output.text(),
                    seconds=self.seconds.value(), audio=self.audio or None,
                    fade=self.fade.value())
            else:
                args, target, estimate = jobs.video_audio_command(
                    self.root, self.video, self.audio, self.output.text())
        except (OSError, ValueError) as error:
            self.error("Videoauftrag nicht gestartet", error)
            return False
        self.final_output = target
        self.temp_output = target.parent / (".provoware-" + uuid4().hex + ".mp4")
        self.estimate = estimate
        self.cancelled = False
        self.buffer = ""
        self.progress_seconds = 0
        self.progress.setValue(0)
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_progress)
        self.process.finished.connect(self.finished)
        self.process.errorOccurred.connect(self.process_error)
        self.process.start("ffmpeg", [*args, str(self.temp_output)])
        self.status.setText("Videoauftrag läuft. Ein Auftrag zur Zeit.")
        return True

    def refresh_queue(self):
        try:
            jobs = media_queue.load(self.root, recover_running=self.process is None)
            self.queue_list.clear()
            self.queue_list.addItems([x["status"] + " · " + Path(x["output"]).name
                                      for x in jobs["jobs"]])
        except (OSError, ValueError) as error:
            self.status.setText("Warteschlange nicht lesbar: " + str(error))

    def enqueue_current(self):
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            self.status.setText("Laufender Auftrag zuerst fertigstellen.")
            return
        try:
            if self.mode.currentIndex() == 0:
                jobs.slideshow_command(self.root, self.images, self.output.text(),
                    seconds=self.seconds.value(), audio=self.audio or None, fade=self.fade.value())
                kind = "slideshow"
                inputs = self.images + ([self.audio] if self.audio else [])
            else:
                jobs.video_audio_command(self.root, self.video, self.audio, self.output.text())
                kind = "video_audio"
                inputs = [self.video, self.audio]
            media_queue.enqueue(self.root, kind=kind, inputs=inputs,
                output=self.output.text(), seconds=self.seconds.value(), fade=self.fade.value())
            self.refresh_queue()
            self.status.setText("Auftrag gespeichert. Über 'Nächsten Auftrag' starten.")
        except (OSError, ValueError) as error:
            self.error("Einreihen nicht möglich", error)

    def run_next(self):
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            return
        try:
            waiting = next((x for x in media_queue.load(self.root)["jobs"]
                            if x["status"] == "waiting"), None)
            if waiting is None:
                self.status.setText("Keine wartenden Videoaufträge.")
                return
            if waiting["kind"] == "slideshow":
                self.mode.setCurrentIndex(0)
                self.images = list(waiting["inputs"])
                self.audio = ""
                if self.images and Path(self.images[-1]).suffix.lower() in media.AUDIO:
                    self.audio = self.images.pop()
                self.image_list.clear()
                self.image_list.addItems([Path(p).name for p in self.images])
                self.audio_label.setText(self.audio)
            else:
                self.mode.setCurrentIndex(1)
                self.video, self.audio = waiting["inputs"]
                self.video_label.setText(self.video)
                self.audio_label.setText(self.audio)
            self.seconds.setValue(waiting["seconds"])
            self.fade.setValue(waiting["fade"])
            self.output.setText(waiting["output"])
            media_queue.transition(self.root, waiting["id"], "running")
            self.active_queue_id = waiting["id"]
            if not self.start():
                media_queue.transition(self.root, waiting["id"], "failed")
                self.active_queue_id = None
            self.refresh_queue()
        except (OSError, ValueError) as error:
            self.active_queue_id = None
            self.error("Warteschlangenstart fehlgeschlagen", error)

    def read_progress(self):
        if self.process is None:
            return
        self.buffer += bytes(self.process.readAllStandardOutput()).decode("utf-8", "replace")
        if len(self.buffer) > 16_384:
            self.buffer = self.buffer[-4096:]
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            if line.startswith("out_time_ms=") and self.estimate:
                try:
                    self.progress_seconds = int(line.split("=", 1)[1]) / 1_000_000
                    self.progress.setValue(min(99, int(100 * self.progress_seconds / self.estimate)))
                except ValueError:
                    pass
            if line.startswith("speed=") and self.estimate:
                speed = line.split("=", 1)[1].strip().rstrip("x")
                try:
                    factor = float(speed)
                    if factor > 0:
                        eta = max(0, int((self.estimate - self.progress_seconds) / factor))
                        self.status.setText(f"Verarbeitung: {self.progress.value()} % · ungefähr {eta} s verbleibend")
                except ValueError:
                    pass

    def cancel(self):
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            self.cancelled = True
            self.process.kill()
            self.status.setText("Auftrag abgebrochen; Teilausgabe wird entfernt.")

    def process_error(self, error):
        del error
        self.status.setText("FFmpeg-Aufruf fehlgeschlagen. Prüfe FFmpeg und Eingabedateien.")

    def finished(self, exit_code, exit_status):
        output = self.temp_output
        process = self.process
        self.process = None
        try:
            if (not self.cancelled and exit_status == QProcess.NormalExit and exit_code == 0
                    and output is not None and output.is_file() and output.stat().st_size > 0
                    and self.final_output is not None and not self.final_output.exists()):
                # Hardlink innerhalb desselben Ausgabeordners schlägt bei fremder,
                # inzwischen angelegter Zieldatei ab statt sie zu überschreiben.
                with output.open("rb") as stream:
                    os.fsync(stream.fileno())
                verify_video(output, require_audio=bool(self.audio))
                os.link(output, self.final_output)
                self.progress.setValue(100)
                self.status.setText("Video fertig gespeichert: " + str(self.final_output))
            else:
                self.status.setText("Kein fertiges Video erzeugt; Originaldateien bleiben erhalten.")
        except OSError as error:
            self.status.setText("Ausgabe konnte nicht veröffentlicht werden: " + str(error))
        finally:
            if self.active_queue_id is not None:
                try:
                    media_queue.transition(self.root, self.active_queue_id,
                        "done" if self.progress.value() == 100 and not self.cancelled else "failed")
                except (OSError, ValueError) as error:
                    self.status.setText("Warteschlangenstatus nicht gesichert: " + str(error))
                self.active_queue_id = None
                self.refresh_queue()
            if output is not None:
                output.unlink(missing_ok=True)
            if process is not None:
                process.deleteLater()

    def import_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Videoprojekt importieren", "", "JSON (*.json)")
        if not filename or not self.confirm_leave():
            return
        try:
            path = Path(filename)
            if path.stat().st_size > 100_000:
                raise ValueError("Projektdatei zu groß.")
            self._apply(self._validate_preset(json.loads(path.read_text(encoding="utf-8"))))
            self.status.setText("Videoprojekt geladen. Vorhandene Projektdatei bleibt unverändert.")
        except (OSError, ValueError) as error:
            self.error("Import fehlgeschlagen", error)

    def export_data(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Videoprojekt exportieren", "video_projekt.json", "JSON (*.json)")
        if filename:
            try:
                atomic_write_json(archive.export_target(self.root, filename),
                                  self._validate_preset(self._preset()))
                self.status.setText("Videoprojekt exportiert.")
            except (OSError, ValueError) as error:
                self.error("Export fehlgeschlagen", error)

    def closeEvent(self, event):
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            answer = QMessageBox.question(self, "Videoauftrag läuft",
                "Verarbeitung abbrechen und Teilausgabe löschen?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if answer != QMessageBox.Yes:
                event.ignore()
                return
            self.cancel()
        super().closeEvent(event)
