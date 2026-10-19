import tempfile,unittest,zipfile,json
from pathlib import Path
from app import development_pool as pool, development_pool_import as importer
class ImportTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name)
        pool.put(self.root,{"id":"old","name":"Beispiel","description":"","status":"offen"})
        (pool.workspace(self.root,"old")/"notiz.txt").write_text("wichtig")
        self.archive=self.root/"project.zip"
        pool.archive_workspace(self.root,"old",self.archive)
    def test_import_adds_copy_without_modifying_existing(self):
        result=importer.import_project_copy(self.root,self.archive)
        self.assertNotEqual(result["id"],"old")
        self.assertIn("Import",result["name"])
        self.assertEqual((pool.workspace(self.root,result["id"])/"notiz.txt").read_text(),"wichtig")
        self.assertEqual((pool.workspace(self.root,"old")/"notiz.txt").read_text(),"wichtig")
    def test_zip_traversal_refused_without_changes(self):
        bad=self.root/"bad.zip"
        with zipfile.ZipFile(bad,"w") as z:
            z.writestr("projekt.json",json.dumps({"id":"old","name":"B","description":"","status":"offen"}))
            z.writestr("arbeit/../../evil.txt","evil")
        with self.assertRaises(ValueError):
            importer.import_project_copy(self.root,bad)
        self.assertEqual(len(pool.load(self.root)["projects"]),1)
