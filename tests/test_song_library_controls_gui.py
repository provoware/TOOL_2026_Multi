import os,tempfile,unittest
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.song_document import SongDocument,SongSection,save_song
from app.song_editor import SongEditor
from app.song_library import SongLibrary
class SongLibraryControlsGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.app=QApplication.instance() or QApplication([])
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root_path=Path(self.temp.name); self.opened=[]
        save_song(self.root_path,SongDocument(title="Favorit Song",genre="Rock",mood="Wild",style="Rau",voice="Tief",tags=["live","laut"],status="Entwurf",favorite=True,sections=[SongSection("Strophe","eins")]))
        save_song(self.root_path,SongDocument(title="Ruhiger Song",genre="Ambient",mood="Ruhig",style="Minimal",voice="Leise",tags=["nacht"],status="Fertig",favorite=False,sections=[SongSection("Strophe","zwei")]))
    def tearDown(self): self.temp.cleanup()
    def test_library_combined_filter_and_favorite_view(self):
        library=SongLibrary(self.root_path,100,self.opened.append); self.assertEqual(len(library._path_by_item),2); library.filter_boxes["Genre"].setCurrentText("Rock"); library.favorite_check.setChecked(True); library.apply_view(); self.assertEqual(len(library._path_by_item),1); selected=next(iter(library._path_by_item.values())); self.assertEqual(selected.name,"Favorit Song.txt"); library.close()
    def test_search_sort_and_group_controls_change_view_without_files(self):
        library=SongLibrary(self.root_path,100,self.opened.append); before=sorted(p.read_text(encoding="utf-8") for p in (self.root_path/"daten"/"songtexte").glob("*.txt")); library.search_entry.setText("nacht"); library.sort_box.setCurrentText("Status"); library.group_box.setCurrentText("Genre"); library.apply_view(); self.assertEqual(len(library._path_by_item),1); self.assertEqual(library.table.topLevelItemCount(),1); self.assertEqual(library.table.topLevelItem(0).text(0),"Ambient"); after=sorted(p.read_text(encoding="utf-8") for p in (self.root_path/"daten"/"songtexte").glob("*.txt")); self.assertEqual(before,after); library.close()
    def test_editor_exposes_status_and_favorite_and_saves_them(self):
        editor=SongEditor(self.root_path,document=SongDocument(title="Editor Song",sections=[SongSection("Strophe","Text")])); editor.status_song.setCurrentText("Überarbeitung"); editor.favorite_check.setChecked(True); path=editor.save(); content=path.read_text(encoding="utf-8"); self.assertIn("STATUS: Überarbeitung",content); self.assertIn("FAVORIT: Ja",content); self.assertTrue(editor.status_song.isEnabled()); self.assertTrue(editor.favorite_check.isEnabled()); editor.close_safely()
    def test_versions_exist_and_restore_is_available(self):
        path=self.root_path/"daten"/"songtexte"/"Favorit Song.txt"; save_song(self.root_path,SongDocument(title="Favorit Song",genre="Rock",status="Entwurf",favorite=True,sections=[SongSection("Strophe","geändert")])); library=SongLibrary(self.root_path,100,self.opened.append); self.assertGreaterEqual(len(__import__('app.song_document',fromlist=['list_versions']).list_versions(self.root_path,"Favorit Song")),1); item=next(i for i in library.table.findItems("Favorit Song",0) if id(i) in library._path_by_item); library.table.setCurrentItem(item); self.assertEqual(library.selected_path(),path); library.close()
if __name__=="__main__": unittest.main()
