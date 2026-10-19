"""Isolierte Ressourcenlimits, beschädigte Medien und Absturzschutz."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from app import media_retry, media_queue, plugin_isolation


class RegressionSecurity(unittest.TestCase):
    def test_plugin_timeout_and_cpu_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"plugin.py"
            p.write_text("while True: pass\n")
            with patch.object(plugin_isolation.shutil, "which", return_value="/usr/bin/bwrap"):
                import subprocess
                with patch.object(plugin_isolation.subprocess,"run",
                                  side_effect=subprocess.TimeoutExpired("bwrap", 1)) as runner:
                    with self.assertRaises(RuntimeError):
                        plugin_isolation.probe_plugin(p,approved=True,timeout=1)
                    self.assertIs(runner.call_args.kwargs["preexec_fn"],
                                  plugin_isolation._resource_limits)
    def test_bad_ffmpeg_job_is_not_requeued(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            source=root/"missing.png"
            output=root/"out.mp4"
            job=media_queue.enqueue(root,kind="slideshow",inputs=[str(source)],
                    output=str(output))
            media_queue.transition(root,job["id"],"running")
            media_queue.transition(root,job["id"],"failed")
            with self.assertRaises((ValueError,OSError)):
                media_retry.retry_failed(root,job["id"],approved=True)
            self.assertEqual(media_queue.load(root)["jobs"][0]["status"],"failed")
            self.assertFalse(output.exists())
    def test_invalid_completion_remains_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            job=media_queue.enqueue(root,kind="slideshow",inputs=["/tmp/a.png"],
                    output=str(root/"clip.mp4"))
            with self.assertRaises(ValueError):
                media_queue.transition(root,job["id"],"done")
