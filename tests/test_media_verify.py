import json
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import unittest
from app import media_verify

class VerifyTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.path=Path(self.t.name)/"video.mp4"
        self.path.write_bytes(b"test")
    def test_valid_video_and_required_audio(self):
        payload={"format":{"duration":"3.2"},"streams":[
            {"codec_type":"video","width":1280,"height":720},
            {"codec_type":"audio"}]}
        with patch("app.media_verify.shutil.which",return_value="/usr/bin/ffprobe"),patch(
            "app.media_verify.subprocess.run",return_value=SimpleNamespace(
                returncode=0,stdout=json.dumps(payload).encode(),stderr=b"")):
            self.assertTrue(media_verify.verify_video(self.path,require_audio=True)["audio"])
    def test_reject_missing_audio_and_bad_output(self):
        payload={"format":{"duration":"3.2"},"streams":[{"codec_type":"video","width":1280,"height":720}]}
        with patch("app.media_verify.shutil.which",return_value="/usr/bin/ffprobe"),patch(
            "app.media_verify.subprocess.run",return_value=SimpleNamespace(
                returncode=0,stdout=json.dumps(payload).encode(),stderr=b"")):
            with self.assertRaises(ValueError):
                media_verify.verify_video(self.path,require_audio=True)
        with patch("app.media_verify.shutil.which",return_value=None):
            with self.assertRaises(ValueError):
                media_verify.verify_video(self.path)
