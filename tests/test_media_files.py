"""Prüft lokale Pfade, Duplikate, Playlists und fehlende Medien."""
from pathlib import Path
import tempfile
import unittest
from app import media_files as media


class MediaFilesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.audio = self.root / "track.mp3"
        self.audio.write_bytes(b"sound")

    def test_playlist_roundtrip_and_missing_reference(self):
        state = {"schema_version": 1, "paths": [str(self.audio)]}
        media.save_playlist(self.root, state)
        self.assertEqual(media.load_playlist(self.root), state)
        self.audio.unlink()
        self.assertEqual(media.load_playlist(self.root)["paths"], [str(self.audio)])

    def test_reject_duplicate_remote_and_symlink(self):
        with self.assertRaises(ValueError):
            media.validate_playlist({"schema_version": 1, "paths": [str(self.audio), str(self.audio)]})
        for path in ("https://website.invalid/audio.mp3", "../bad.mp3", "/tmp/a.exe"):
            with self.assertRaises(ValueError):
                media.media_path(path, media.AUDIO, exists=False)
        linked = self.root / "link.mp3"
        linked.symlink_to(self.audio)
        with self.assertRaises(ValueError):
            media.media_path(linked, media.AUDIO)

    def test_dangling_playlist_symlink_is_rejected_without_modification(self):
        self.assertEqual(media.load_playlist(self.root), {"schema_version": 1, "paths": []})
        target = self.root / "daten/medien/playlist.json"
        target.parent.mkdir(parents=True)
        target.symlink_to(self.root / "nicht-vorhanden.json")
        with self.assertRaisesRegex(ValueError, "Verknüpfung"):
            media.load_playlist(self.root)
        self.assertTrue(target.is_symlink())
