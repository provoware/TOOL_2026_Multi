from pathlib import Path
import tempfile
import unittest
from app import account_store as store
from app.module_archive import export_archive,read_archive


def record():
    return {'id':'account_1','url':'https://example.org/login','name':'Privat','email':'name@example.org',
            'hint':'Passwortmanager verwenden','notes':'Kein Geheimnis','group':'Kreativ','custom':{'Kundennummer':'123'}}


class AccountStoreTests(unittest.TestCase):
    def test_metadata_roundtrip_and_import_copies(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);store.put(root,record());saved=store.load(root)
            export_archive(root/'konten.json','konten',saved,store.validate,root=root)
            imported=read_archive(root/'konten.json','konten',store.validate)
            store.import_copies(root,imported)
            result=store.load(root)['accounts']
            self.assertEqual(len(result),2);self.assertNotEqual(result[0]['id'],result[1]['id'])
            self.assertNotIn('password',result[0]);self.assertEqual(result[0]['custom'],{'Kundennummer':'123'})

    def test_personal_backup_restores_accounts_and_ideas_as_separate_copy(self):
        from scripts.datensicherung import create, restore
        from app import idea_store
        from tests.test_ideas import record as idea
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'active';root.mkdir()
            store.put(root,record());idea_store.put(root,idea())
            package=create(root/'daten',Path(folder)/'backups')
            dest=Path(folder)/'restore'
            restore(package,dest)
            self.assertEqual(store.load(dest),store.load(root))
            self.assertEqual(idea_store.load(dest),idea_store.load(root))

    def test_secret_fields_and_urls_are_rejected(self):
        for field in ('password','Passwort','api_key','Token','PIN','recovery_code'):
            raw=record();raw['custom']={field:'secret'}
            with self.subTest(field=field), self.assertRaises(ValueError):store.validate_record(raw)
        raw=record();raw['password']='secret'
        with self.assertRaises(ValueError):store.validate_record(raw)
        for url in ('javascript:alert(1)','file:///tmp/a','https://u:secret@example.org',
                    'https://example.org/?token=abc','https://example.org/#access_token=abc','https://example.org/\n','https://example.org:bad'):
            with self.subTest(url=url),self.assertRaises(ValueError):store.validate_url(url)

    def test_invalid_import_does_not_change_existing_data(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);store.put(root,record());before=store.load(root)
            raw=record();raw['email']='invalid'
            with self.assertRaises(ValueError):store.import_copies(root,{'schema_version':1,'accounts':[raw]})
            self.assertEqual(store.load(root),before)
