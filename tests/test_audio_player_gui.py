"""Audioplayer-Playlist und GUI-Lebenszyklus ohne echte Audiowiedergabe."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import tempfile
import unittest
from PySide6.QtWidgets import QApplication
from app.audio_player_window import AudioPlayerWindow
from app import media_files


class AudioPlayerGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_playlist_controls_and_zoom(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            track = root / "ton.wav"
            track.write_bytes(b"RIFF" + b"0" * 120)
            media_files.save_playlist(root, {"schema_version": 1, "paths": [str(track)]})
            player = AudioPlayerWindow(root)
            try:
                player.show()
                self.assertEqual(player.listing.count(), 1)
                player.volume.setValue(25)
                self.assertEqual(player.volume.value(), 25)
                player.set_zoom(150)
                self.assertEqual(player.zoom_percent, 150)
                player.listing.setCurrentRow(0)
                player.remove_selected()
                self.assertEqual(media_files.load_playlist(root)["paths"], [])
            finally:
                player.stop()
                player.close()
                self.app.processEvents()
