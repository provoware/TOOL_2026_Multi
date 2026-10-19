"""Kernel-Ressourcengrenzen der isolierten Fremdcodeprobe."""
import tempfile
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
import unittest
from app import plugin_isolation as isolation


class PluginResourceLimitsTests(unittest.TestCase):
    def test_limits_are_passed_to_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"test.py"
            p.write_text("print('{}')")
            raw=b'{"schema_version":1,"module_id":"example_1","actions":[{"action":"view","arguments":{}}]}'
            observed={}
            def runner(args, **kwargs):
                observed.update(kwargs)
                self.assertIn("--unshare-all",args)
                self.assertIn("--cap-drop",args)
                return SimpleNamespace(returncode=0,stdout=raw,stderr=b"")
            with patch.object(isolation.shutil,"which",return_value="/usr/bin/bwrap"), patch.object(
                    isolation.subprocess,"run",side_effect=runner):
                result=isolation.probe_plugin(p,approved=True)
            self.assertEqual(result["module_id"],"example_1")
            self.assertIs(observed["preexec_fn"],isolation._resource_limits)
            self.assertEqual(observed["timeout"],8)

    def test_invalid_timeout_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"safe.py"
            p.write_text("print('{}')")
            with patch.object(isolation.shutil,"which",return_value="/usr/bin/bwrap"):
                for timeout in (0,16,"ten",True):
                    with self.assertRaises(ValueError):
                        isolation.probe_plugin(p,approved=True,timeout=timeout)
