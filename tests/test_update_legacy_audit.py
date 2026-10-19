from pathlib import Path
import tempfile,unittest,json
from app.update_legacy_audit import audit_legacy_install

class LegacyAuditTests(unittest.TestCase):
    def test_audit_refuses_unsafe_target_and_never_mutates(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            source=root/"old";source.mkdir()
            (source/"MANIFEST.json").write_text("{}")
            before=(source/"MANIFEST.json").read_bytes()
            result=audit_legacy_install(source,root)
            self.assertFalse(result["activation_allowed"])
            self.assertFalse(result["ready_for_migration"])
            self.assertTrue(result["blockers"])
            self.assertEqual(before,(source/"MANIFEST.json").read_bytes())
