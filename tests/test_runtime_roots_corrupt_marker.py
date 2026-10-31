"""Regressionsschutz: beschädigte externe Datenmarker führen zu einem klaren Abbruch."""
import json
import tempfile
import unittest
from pathlib import Path

from app.runtime_roots import MARKER, VARIABLE, runtime_root


class CorruptExternalDataMarkerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.code = root / "programm"
        self.code.mkdir()
        self.data = root / "benutzerdaten"
        (self.data / "daten").mkdir(parents=True)
        self.marker = self.data / MARKER
        self.environment = {VARIABLE: str(self.data)}

    def test_malformed_json_fails_with_clear_value_error(self):
        self.marker.write_text('{"schema_version":', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Prüfmarker.*beschädigt"):
            runtime_root(self.code, self.environment)

    def test_invalid_utf8_fails_with_clear_value_error(self):
        self.marker.write_bytes(b"\xff\xfe")
        with self.assertRaisesRegex(ValueError, "Prüfmarker.*beschädigt"):
            runtime_root(self.code, self.environment)

    def test_valid_marker_remains_accepted(self):
        self.marker.write_text(json.dumps({
            "schema_version": 1,
            "purpose": "provoware-managed-data",
            "activation_allowed": False,
        }), encoding="utf-8")
        self.assertEqual(runtime_root(self.code, self.environment), self.data)
        self.assertEqual(runtime_root(self.code, {}), self.code)


if __name__ == "__main__":
    unittest.main()
