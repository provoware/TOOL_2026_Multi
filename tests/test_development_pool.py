"""Projektpool: sichere Arbeitsordner, Kopien, Datenerhalt und ZIP."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from app import development_pool as pool, module_archive as archive


def item(id="projekt_1", name="Musik"):
    return {"id": id, "name": name, "description": "Ideen sammeln", "status": "offen"}


class DevelopmentPoolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_create_edit_search_copy_archive(self):
        pool.put(self.root, item())
        self.assertEqual(pool.load(self.root)["projects"][0]["name"], "Musik")
        source = pool.workspace(self.root, "projekt_1")
        (source / "Notiz.txt").write_text("unverändert")
        pool.put(self.root, {**item(), "status": "aktiv"})
        copied = pool.copy_workspace(self.root, "projekt_1")
        self.assertEqual((copied / "Notiz.txt").read_text(), "unverändert")
        self.assertEqual(pool.list_files(self.root, "projekt_1"), ["Notiz.txt"])
        output = self.root / "extern.zip"
        pool.archive_workspace(self.root, "projekt_1", output)
        with zipfile.ZipFile(output) as z:
            self.assertEqual(z.read("arbeit/Notiz.txt"), b"unver\xc3\xa4ndert")
        self.assertEqual((source / "Notiz.txt").read_text(), "unverändert")

    def test_duplicate_name_and_unsafe_special_links_rejected(self):
        pool.put(self.root, item())
        with self.assertRaises(ValueError):
            pool.put(self.root, item("projekt_2", "MUSIK"))
        path = pool.workspace(self.root, "projekt_1")
        (path / "link").symlink_to(self.root)
        with self.assertRaisesRegex(ValueError, "Links"):
            pool.copy_workspace(self.root, "projekt_1")
        with self.assertRaisesRegex(ValueError, "Links"):
            pool.archive_workspace(self.root, "projekt_1", self.root / "a.zip")

    def test_atomic_failure_keeps_old_project_state(self):
        pool.put(self.root, item())
        file = archive.state_path(self.root, pool.MODULE)
        before = file.read_bytes()
        with patch.object(archive, "atomic_write_json", side_effect=OSError("voll")):
            with self.assertRaises(OSError):
                pool.put(self.root, {**item(), "status": "fertig"})
        self.assertEqual(file.read_bytes(), before)

    def test_archives_cannot_overwrite_data_or_existing_exports(self):
        pool.put(self.root, item())
        with self.assertRaises(ValueError):
            pool.archive_workspace(self.root, "projekt_1", pool.workspace(self.root, "projekt_1") / "x.zip")
        target = self.root / "external.zip"
        target.write_bytes(b"bleibt")
        with self.assertRaises(ValueError):
            pool.archive_workspace(self.root, "projekt_1", target)
        self.assertEqual(target.read_bytes(), b"bleibt")
