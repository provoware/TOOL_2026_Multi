"""Zwei echte Standbilder werden mittels xfade ineinander übergeführt."""
import shutil
import subprocess
import tempfile
from pathlib import Path
import unittest
from app.media_jobs import crossfade_command
from app.media_verify import verify_video

@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"FFmpeg/FFprobe fehlt")
class RealCrossfadeTests(unittest.TestCase):
    def test_real_video_transition(self):
        from PySide6.QtGui import QImage
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            a=root/"a.png"
            b=root/"b.png"
            for path,color in ((a,0xFF0000),(b,0x0000FF)):
                img=QImage(48,48,QImage.Format_RGB32)
                img.fill(color)
                self.assertTrue(img.save(str(path)))
            args,target,expected=crossfade_command(root,[str(a),str(b)],str(root/"video.mp4"),seconds=2,intensity=65)
            completed=subprocess.run(["ffmpeg",*args,str(target)],stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,timeout=60,check=False)
            self.assertEqual(completed.returncode,0,completed.stderr[-1600:])
            info=verify_video(target)
            self.assertAlmostEqual(info["duration_seconds"],expected,delta=0.3)
