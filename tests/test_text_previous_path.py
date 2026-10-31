"""Rückfalltests: Umbenennen darf keine fremden Dateien verschieben."""
import tempfile
import unittest
from pathlib import Path

from app.text_editor_store import TextDocument, save_text_document, text_path


class TextPreviousPathTests(unittest.TestCase):
    def test_external_previous_path_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "projekt"
            root.mkdir()
            external = Path(tmp) / "fremd.json"
            external.write_bytes(b"fremde Daten bleiben hier")
            with self.assertRaisesRegex(ValueError, "Textordner"):
                save_text_document(root, TextDocument(title="Neuer Titel"), previous_path=external)
            self.assertEqual(external.read_bytes(), b"fremde Daten bleiben hier")
            self.assertFalse(text_path(root, "Neuer Titel").exists())

    def test_link_to_external_previous_path_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "projekt"
            folder = root / "daten" / "texte"
            folder.mkdir(parents=True)
            external = Path(tmp) / "fremd.json"
            external.write_bytes(b"unveraendert")
            alias = folder / "alt.json"
            alias.symlink_to(external)
            with self.assertRaisesRegex(ValueError, "Textordner"):
                save_text_document(root, TextDocument(title="Neuer Titel"), previous_path=alias)
            self.assertEqual(external.read_bytes(), b"unveraendert")
            self.assertTrue(alias.is_symlink())
            self.assertFalse(text_path(root, "Neuer Titel").exists())

    def test_ordinary_rename_preserves_old_document_in_versions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = save_text_document(root, TextDocument(title="Alter Titel", text="Original"))
            new = save_text_document(root, TextDocument(title="Neuer Titel", text="Neu"), previous_path=old)
            self.assertTrue(new.is_file())
            self.assertFalse(old.exists())
            self.assertEqual(len(list((root / "daten" / "texte" / ".versionen" / "Alter Titel").glob("*.json"))), 1)


if __name__ == "__main__":
    unittest.main()
