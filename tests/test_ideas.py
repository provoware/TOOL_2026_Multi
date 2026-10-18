from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from app import idea_store as store
from app.module_archive import export_archive, read_archive


def record():
    return {'id':'idea_1','title':'Regen','content':'Ein Vers\nZweiter Vers','tags':['Wetter'],'origin':'Eigene Idee'}


class IdeaStoreTests(unittest.TestCase):
    def test_roundtrip_searchable_fields_and_import_copies(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            store.put(root,record())
            original=store.load(root)
            exported=root/'export.json'
            export_archive(exported,'ideen',original,store.validate,root=root)
            loaded=read_archive(exported,'ideen',store.validate)
            store.import_copies(root,loaded)
            records=store.load(root)['ideas']
            self.assertEqual(len(records),2)
            self.assertNotEqual(records[0]['id'],records[1]['id'])
            self.assertEqual(records[0]['content'],records[1]['content'])

    def test_invalid_import_and_failed_write_preserve_original(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);store.put(root,record())
            before=store.load(root)
            bad=record();bad['content']=''
            with self.assertRaises(ValueError):store.put(root,bad)
            with patch('app.module_archive.atomic_write_json',side_effect=OSError('voll')):
                with self.assertRaises(OSError):store.put(root,{**record(),'title':'Neu'})
            self.assertEqual(store.load(root),before)
