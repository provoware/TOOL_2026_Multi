import tempfile
from pathlib import Path
import unittest

from app import module_blueprints, module_extension

class ExtensionContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        module_blueprints.put(self.root,{
            "id":"example_1", "title":"Notizen", "description":"",
            "fields":[{"id":"field_1","label":"Notiz","type":"text"}],
            "capabilities":["view","search","edit"]})

    def doc(self,kind="edit",args=None):
        if args is None:
            args={"values":{"field_1":"Test"}}
        return {"schema_version":1,"module_id":"example_1",
                "actions":[{"action":kind,"arguments":args}]}

    def test_explicit_permission_and_safe_builtin_operation(self):
        with self.assertRaises(PermissionError):
            module_extension.execute_approved(self.root,self.doc())
        item=module_extension.execute_approved(self.root,self.doc(),approved=True)
        self.assertEqual(item["values"]["field_1"],"Test")
        matches=module_extension.execute_approved(self.root,
                self.doc("search",{"needle":"Test"}),approved=True)
        self.assertEqual(len(matches),1)

    def test_no_unknown_callbacks_network_or_python(self):
        for bad in ("execute","python","shell","network","delete"):
            with self.assertRaises(PermissionError):
                module_extension.validate_extension(self.doc(bad,{}))
        with self.assertRaises(ValueError):
            module_extension.validate_extension({**self.doc(), "entrypoint":"os.system"})
        with self.assertRaises(PermissionError):
            module_extension.execute_approved(self.root,
                {**self.doc(),"actions":self.doc()["actions"]*2},approved=True)

    def test_refuses_symlinked_document(self):
        original=self.root/"ext.json"
        original.write_text('{"schema_version":1,"module_id":"example_1","actions":[]}')
        link=self.root/"ext-link.json"
        link.symlink_to(original)
        with self.assertRaises(ValueError):
            module_extension.load_extension(link)
