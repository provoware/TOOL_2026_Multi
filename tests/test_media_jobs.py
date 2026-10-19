"""FFmpeg-Filter und Ausgabeschutz ohne tatsächliches Encoding testen."""
from pathlib import Path
import tempfile
import unittest
from app import media_jobs as jobs


class MediaJobsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.picture = self.root / "pic.png"
        self.picture.write_bytes(b"image")
        self.audio = self.root / "track.mp3"
        self.audio.write_bytes(b"audio")
        self.video = self.root / "clip.mp4"
        self.video.write_bytes(b"video")

    def test_slideshow_builds_checked_filter_and_duration(self):
        args, target, length = jobs.slideshow_command(self.root, [str(self.picture)],
                                                      str(self.root / "ausgabe.mp4"), seconds=4, audio=str(self.audio))
        self.assertEqual(length, 4)
        self.assertIn("concat=n=1", " ".join(args))
        self.assertIn("-stream_loop", args)
        self.assertNotIn("-y", args)
        self.assertEqual(target.name, "ausgabe.mp4")

    def test_video_audio_and_existing_target_safety(self):
        args, _, length = jobs.video_audio_command(
            self.root, str(self.video), str(self.audio), str(self.root / "new.mp4"))
        self.assertIsNone(length)
        self.assertIn("-shortest", args)
        with self.assertRaises(ValueError):
            jobs.video_audio_command(self.root, str(self.video), str(self.audio), str(self.video))
        with self.assertRaises(ValueError):
            jobs.slideshow_command(self.root, [str(self.picture)] * 2, str(self.root / "new.mp4"))
        with self.assertRaises(ValueError):
            jobs.slideshow_command(self.root, [str(self.picture)], str(self.root / "new.mp4"), seconds=0)
