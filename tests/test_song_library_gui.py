import os,tempfile,unittest
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
from pathlib import Path
from PySide6.QtWidgets import QApplication,QPushButton
from app.song_document import SongDocument,SongSection,save_song
from app.song_editor import SongEditor
from app.song_library import SongLibrary
from app.ui import Dashboard
class FakeTexts:
    def get(self,_key,default=""): return default
class FakeLogger:
    def recent(self,_limit=100): return []
    @staticmethod
    def human_report(event): return str(event)
class SongLibraryGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.app=QApplication.instance() or QApplication([])
    def setUp(self): self.temp=tempfile.TemporaryDirectory(); self.project_root=Path(self.temp.name); self.dashboard=Dashboard(FakeTexts(),FakeLogger(),self.project_root); self.dashboard.show(); self.app.processEvents()
    def tearDown(self): self.dashboard._closing_after_save=True; self.dashboard.close(); self.app.processEvents(); self.temp.cleanup()
    def test_recent_song_tiles_are_created_and_open_existing_song(self):
        path=save_song(self.project_root,SongDocument(title="Letzter Song",genre="Soul",mood="warm",sections=[SongSection("Strophe","Text")])); self.dashboard.refresh_recent_songs(); self.app.processEvents(); buttons=[self.dashboard.recent_layout.itemAt(i).widget() for i in range(self.dashboard.recent_layout.count())]; buttons=[b for b in buttons if isinstance(b,QPushButton)]; self.assertEqual(len(buttons),1); self.assertIn("Letzter Song",buttons[0].text()); self.dashboard.open_song_path(path); self.assertEqual(len(self.dashboard._song_editors),1); editor=self.dashboard._song_editors[0]; self.assertEqual(editor.title_entry.text(),"Letzter Song"); self.assertEqual(editor.mood_entry.text(),"warm"); editor.close_safely()
    def test_library_lists_saved_song_and_can_open_selected(self):
        save_song(self.project_root,SongDocument(title="Bibliothek Song",sections=[SongSection("Refrain","Hook")])); opened=[]; library=SongLibrary(self.project_root,100,opened.append); library.show(); self.app.processEvents(); self.assertEqual(len(library._path_by_item),1); item=next(i for i in library.table.findItems("Bibliothek Song",0)); library.table.setCurrentItem(item); library.open_selected(); self.assertEqual(len(opened),1); library.close()
    def test_metadata_fields_and_export_menu_exist(self):
        editor=SongEditor(self.project_root); self.assertGreaterEqual(len(editor.meta_entries),7); editor.mood_entry.setText("dunkel"); editor.style_entry.setText("minimal"); editor.voice_entry.setText("rau"); editor.special_entry.setText("Pause vor Hook"); editor.tags_entry.setText("nacht, bass"); editor._update_preview(); preview=editor.preview.toPlainText(); self.assertIn("STIMMUNG: dunkel",preview); self.assertIn("STIL: minimal",preview); self.assertIn("STIMME: rau",preview); self.assertIn("TAGS: nacht, bass",preview); self.assertIsNotNone(editor.export("json")); self.assertIsNotNone(editor.export("txt",lyrics_only=True)); editor.close_safely()
if __name__=="__main__": unittest.main()
