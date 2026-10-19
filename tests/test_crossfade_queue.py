"""Überblendungsart bleibt auch in persistenten Aufträgen erhalten."""
import os
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import media_queue
from app.atomic_io import atomic_write_json
from PySide6.QtWidgets import QApplication,QMessageBox
from app.slideshow_window import SlideshowWindow


class CrossfadeQueueTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def test_queue_keeps_transition_and_old_jobs_remain_valid(self):
        old={"schema_version":1,"jobs":[{
          "id":"legacy","kind":"slideshow","status":"waiting",
          "inputs":["/tmp/a.png"],"output":"/tmp/out.mp4",
          "seconds":5,"fade":0}]}
        path=self.root/"daten/medien/job_queue.json"
        path.parent.mkdir(parents=True)
        atomic_write_json(path,old)
        self.assertEqual(media_queue.load(self.root)["jobs"][0]["transition"],"none")
        newer=media_queue.enqueue(self.root,kind="slideshow",
          inputs=["/tmp/a.png","/tmp/b.png"],output="/tmp/new.mp4",
          seconds=5,fade=80,transition="wipeleft")
        self.assertEqual(newer["transition"],"wipeleft")
        self.assertEqual(media_queue.load(self.root)["jobs"][1]["transition"],"wipeleft")
        with self.assertRaises(ValueError):
            media_queue.enqueue(self.root,kind="slideshow",
              inputs=["/tmp/a.png"],output="/tmp/bad.mp4",
              seconds=5,fade=30,transition="fade")

    def test_forged_transition_fails(self):
        with self.assertRaises(ValueError):
            media_queue.validate({"schema_version":1,"jobs":[{
                "id":"x","kind":"slideshow","status":"waiting",
                "inputs":["/tmp/a.png","/tmp/b.png"],"output":"/tmp/new.mp4",
                "seconds":5,"fade":90,"transition":"evil=execute"}]})


class CrossfadeQueueGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=QApplication.instance() or QApplication([])

    def test_video_ui_enqueues_real_transition_and_retry_needs_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            one=root/"one.png"
            two=root/"two.png"
            one.write_bytes(b"data")
            two.write_bytes(b"data")
            win=SlideshowWindow(root)
            try:
                win.images=[str(one),str(two)]
                win.output.setText(str(root/"my_movie.mp4"))
                win.fade.setValue(80)
                win.transition.setCurrentIndex(2)
                win.enqueue_current()
                queued=media_queue.load(root)["jobs"]
                self.assertEqual(len(queued),1)
                self.assertEqual(queued[0]["transition"],"wipeleft")
                job=queued[0]
                media_queue.transition(root,job["id"],"running")
                media_queue.transition(root,job["id"],"failed")
                with patch("app.slideshow_window.QMessageBox.question",
                           return_value=QMessageBox.No):
                    win.retry_failed()
                self.assertEqual(media_queue.load(root)["jobs"][0]["status"],"failed")
                with patch("app.slideshow_window.QMessageBox.question",
                           return_value=QMessageBox.Yes):
                    win.retry_failed()
                self.assertEqual(media_queue.load(root)["jobs"][0]["status"],"waiting")
            finally:
                win.discard_draft()
                win.close()
                self.app.processEvents()
