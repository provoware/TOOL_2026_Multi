"""Die Modulinstanz verarbeitet ausschließlich geprüfte Formulardaten."""
from pathlib import Path
import tempfile
import unittest
from app import module_blueprints as b, module_runtime as r

class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.blueprint = {"id":"my_module", "title":"Eigene Sammlung",
                          "description":"", "capabilities":["view","edit","search"],
                          "fields":[{"id":"field_1","label":"Text","type":"text"},
                                    {"id":"field_2","label":"Tag","type":"date"}]}
        b.put(self.root, self.blueprint)

    def test_save_search_roundtrip(self):
        values={"field_1":"Hallo","field_2":"2026-10-19"}
        one=r.save_record(self.root,"my_module",values)
        self.assertEqual(r.query(self.root,"my_module","hallo")[0]["id"],one["id"])
        r.save_record(self.root,"my_module",{**values,"field_1":"Geändert"},one["id"])
        self.assertEqual(len(r.load(self.root,"my_module")["records"]),1)

    def test_no_code_fields_unknown_ids_or_ungranted_capabilities(self):
        with self.assertRaises(ValueError):
            r.save_record(self.root,"my_module",{"__import__":"os"})
        with self.assertRaises(ValueError):
            r.save_record(self.root,"my_module",{"field_1":"x","field_2":"2026-99-99"})
        with self.assertRaises(ValueError):
            r.load(self.root,"../../outside")
        b.put(self.root,{**self.blueprint,"capabilities":["view"]})
        with self.assertRaises(ValueError):
            r.save_record(self.root,"my_module",{"field_1":"x","field_2":""})
