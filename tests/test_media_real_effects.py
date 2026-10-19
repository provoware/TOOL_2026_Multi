"""Realer FFmpeg-Vergleich: Einblendungsstärke 0 % gegen 80 %."""
import shutil
import subprocess
import tempfile
from pathlib import Path
import unittest

from app.media_jobs import slideshow_command
from app.media_verify import verify_video


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                     "FFmpeg und FFprobe sind nicht installiert")
class RealVideoEffectsTests(unittest.TestCase):
    def test_render_and_compare_fade_frames(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            picture=root/"red.png"
            # Erzeugung eines echten Bildes ohne zusätzliche Netzwerkdienste.
            from PySide6.QtGui import QImage
            image=QImage(64,64,QImage.Format_RGB32)
            image.fill(0xFF0000)
            self.assertTrue(image.save(str(picture)))
            hashes=[]
            for amount in (0,80):
                destination=root/f"fade_{amount}.mp4"
                args,target,seconds=slideshow_command(
                    root,[str(picture)],str(destination),seconds=2,fade=amount)
                done=subprocess.run(["ffmpeg",*args,str(target)],
                                    capture_output=True,timeout=40,check=False)
                self.assertEqual(done.returncode,0,done.stderr[-2000:])
                info=verify_video(target)
                self.assertAlmostEqual(info["duration_seconds"],2,delta=0.3)
                frame=subprocess.run(
                    ["ffmpeg","-hide_banner","-loglevel","error","-ss","0.04",
                     "-i",str(target),"-frames:v","1","-f","md5","-"],
                    capture_output=True,timeout=20,check=False)
                self.assertEqual(frame.returncode,0,frame.stderr[-2000:])
                hashes.append(frame.stdout)
            self.assertNotEqual(hashes[0],hashes[1],
                "80 % Blende muss eine andere tatsächliche Videofarbe erzeugen.")
