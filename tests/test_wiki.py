"""Wiki-Logik: sichere Sammlungen, Versionen, Referenzen und Archivkopien."""
import json
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4
from unittest.mock import patch

from app import wiki_store as wiki, module_archive as archive


def article(title="Anfang", *, ident=None, base="Allgemein", links=None, content="Hallo"):
    return {"id": ident or uuid4().hex, "base": base, "title": title,
            "content": content, "tags": ["Gedanke"],
            "links": links or [], "revisions": []}


class WikiStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_create_edit_version_and_search(self):
        first = wiki.put(self.root, article())
        self.assertEqual(wiki.search(self.root, "gedanke")[0]["id"], first["id"])
        first["content"] = "Andere Fassung"
        saved = wiki.put(self.root, first)
        self.assertEqual(saved["revisions"][-1]["content"], "Hallo")
        self.assertEqual(len(saved["revisions"]), 1)
        self.assertEqual(wiki.search(self.root, "andere")[0]["content"], "Andere Fassung")
        wiki.put(self.root, saved)
        self.assertEqual(len(wiki.load(self.root)["articles"][0]["revisions"]), 1)

    def test_bases_links_and_delete_refusal(self):
        wiki.add_base(self.root, "Philosophie")
        a = wiki.put(self.root, article("Frage"))
        b = wiki.put(self.root, article("Antwort", base="Philosophie", links=[a["id"]]))
        self.assertEqual(wiki.search(self.root, base="Philosophie")[0]["id"], b["id"])
        with self.assertRaises(ValueError):
            wiki.remove(self.root, a["id"])
        wiki.remove(self.root, b["id"])
        wiki.remove(self.root, a["id"])
        self.assertEqual(wiki.load(self.root)["articles"], [])

    def test_import_remaps_links_and_never_overwrites(self):
        first = wiki.put(self.root, article())
        external = {"schema_version": 1, "bases": ["Allgemein"], "articles": [
            article("Anfang", ident="id1"), article("Weitere", ident="id2", links=["id1"])]}
        count = wiki.import_copies(self.root, external)
        self.assertEqual(count, 2)
        state = wiki.load(self.root)
        self.assertEqual(len(state["articles"]), 3)
        imported = next(a for a in state["articles"] if a["title"] == "Weitere")
        self.assertEqual(imported["links"], [next(a["id"] for a in state["articles"] if "Kopie" in a["title"])])
        self.assertEqual(next(a for a in state["articles"] if a["id"] == first["id"])["content"], "Hallo")

    def test_invalid_damaged_input_and_write_failure(self):
        original = wiki.put(self.root, article())
        path = archive.state_path(self.root, "wiki")
        before = path.read_bytes()
        bad = wiki.load(self.root)
        bad["articles"][0]["links"] = ["nicht_vorhanden"]
        with self.assertRaises(ValueError):
            wiki.validate(bad)
        with self.assertRaises(ValueError):
            wiki.put(self.root, article("Anfang"))
        with patch.object(archive, "atomic_write_json", side_effect=OSError("schreibgeschützt")):
            with self.assertRaises(OSError):
                wiki.put(self.root, article("Neu"))
        self.assertEqual(path.read_bytes(), before)
        path.write_text("{")
        with self.assertRaises(json.JSONDecodeError):
            wiki.load(self.root)
        self.assertEqual(path.read_text(), "{")
