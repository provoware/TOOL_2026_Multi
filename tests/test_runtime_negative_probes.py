"""Reale Negativproben: Plugin-Sandbox und Video-Wiederholung."""
import json
import shutil
import tempfile
from pathlib import Path
import unittest

from app import plugin_isolation, media_queue, media_retry


class RetryRecoveryTests(unittest.TestCase):
    def test_interruption_requires_approval_and_does_not_touch_output(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            image=root/"bild.png"
            image.write_bytes(b"image")
            output=root/"ausgabe.mp4"
            job=media_queue.enqueue(root,kind="slideshow",
                    inputs=[str(image)],output=str(output),seconds=2)
            media_queue.transition(root,job["id"],"running")
            self.assertEqual(media_queue.load(root)["jobs"][0]["status"],"interrupted")
            with self.assertRaises(PermissionError):
                media_retry.retry_failed(root,job["id"])
            output.write_bytes(b"original")
            with self.assertRaises(ValueError):
                media_retry.retry_failed(root,job["id"],approved=True)
            self.assertEqual(output.read_bytes(),b"original")
            self.assertEqual(media_queue.load(root)["jobs"][0]["status"],"interrupted")
            output.unlink()
            self.assertEqual(media_retry.retry_failed(root,job["id"],approved=True)["status"],"waiting")


@unittest.skipUnless(shutil.which("bwrap") and Path("/usr/bin/python3").exists(),
                     "Bubblewrap-Praxisprobe braucht Linux und unterstützte User-Namespaces")
class ActualSandboxTests(unittest.TestCase):
    def test_plugin_cannot_read_host_environment(self):
        with tempfile.TemporaryDirectory() as t:
            source=Path(t)/"extension.py"
            source.write_text(
                "import json,os\n"
                "assert os.path.exists('/etc/passwd') is False\n"
                "print(json.dumps({'schema_version':1,'module_id':'example_1',"
                "'actions':[{'action':'view','arguments':{}}]}))\n")
            # Sobald das Linux-System die Sandbox gestattet, muss der reale
            # Kindprozess laufen. Ein fehlgeschlagener Test darf keine Freigabe sein.
            result=plugin_isolation.probe_plugin(source,approved=True)
            self.assertEqual(result["actions"][0]["action"],"view")
