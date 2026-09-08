"""PySide6-Songbibliothek mit Suche, Filtern, Gruppierung und sicherem Restore."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QCheckBox,QComboBox,QDialog,QGridLayout,QHBoxLayout,QLabel,QLineEdit,QListWidget,QMessageBox,QPushButton,QTextEdit,QTreeWidget,QTreeWidgetItem,QVBoxLayout,QWidget)
from app.song_document import SONG_STATUSES, SongDocument, list_songs, list_versions, load_song, restore_version
from app.ui_standards import SPACING, apply_global_style
FILTER_ALL="Alle"
SORT_OPTIONS=("Zuletzt bearbeitet","Titel","Genre","Tags","Status")
GROUP_OPTIONS=("Keine","Genre","Tags","Status")
@dataclass(frozen=True)
class SongRow:
    path: Path; document: SongDocument; modified: float; versions: int
def _norm(value:str)->str: return value.strip().casefold()
def song_matches(row:SongRow, search:str="", *, genre:str=FILTER_ALL,mood:str=FILTER_ALL,style:str=FILTER_ALL,voice:str=FILTER_ALL,tag:str=FILTER_ALL,status:str=FILTER_ALL,favorites_only:bool=False)->bool:
    d=row.document; needle=_norm(search); searchable=" ".join((d.title,d.genre,d.mood,d.style,d.voice," ".join(d.tags))).casefold()
    if needle and needle not in searchable:return False
    fields=((genre,d.genre),(mood,d.mood),(style,d.style),(voice,d.voice),(status,d.status))
    if any(sel!=FILTER_ALL and _norm(sel)!=_norm(actual) for sel,actual in fields):return False
    if tag!=FILTER_ALL and _norm(tag) not in {_norm(x) for x in d.tags}:return False
    return not favorites_only or d.favorite
def sort_rows(rows:list[SongRow], sort_by:str)->list[SongRow]:
    if sort_by=="Titel": key,reverse=lambda r:_norm(r.document.title),False
    elif sort_by=="Genre": key,reverse=lambda r:(_norm(r.document.genre),_norm(r.document.title)),False
    elif sort_by=="Tags": key,reverse=lambda r:(_norm(", ".join(r.document.tags)),_norm(r.document.title)),False
    elif sort_by=="Status":
        order={s:i for i,s in enumerate(SONG_STATUSES)}; key,reverse=lambda r:(order.get(r.document.status,99),_norm(r.document.title)),False
    else:key,reverse=lambda r:r.modified,True
    return sorted(rows,key=key,reverse=reverse)
def row_group(row:SongRow, group_by:str)->str:
    if group_by=="Genre":return row.document.genre.strip() or "Ohne Genre"
    if group_by=="Tags":return ", ".join(row.document.tags) or "Ohne Tags"
    if group_by=="Status":return row.document.status or "Idee"
    return ""
class SongLibrary(QWidget):
    def __init__(self, project_root:Path, zoom_percent:int, open_song:Callable[[Path],None], parent:QWidget|None=None)->None:
        super().__init__(parent,Qt.Window); self.project_root=project_root; self.open_song_callback=open_song; self.zoom_percent=zoom_percent; self._rows=[]; self._path_by_item={}
        self.setWindowTitle("Songbibliothek"); self.resize(1180,720); self.setMinimumSize(920,580); self._build(); apply_global_style(self,zoom_percent); self.refresh()
    def _build(self):
        out=QVBoxLayout(self); out.setContentsMargins(15,15,15,15); out.setSpacing(8)
        h=QHBoxLayout(); t=QLabel("Songbibliothek"); t.setObjectName("sectionTitle"); h.addWidget(t); h.addStretch(); b=QPushButton("Aktualisieren"); b.clicked.connect(self.refresh); h.addWidget(b); out.addLayout(h)
        sr=QHBoxLayout(); sr.addWidget(QLabel("Suche:")); self.search_entry=QLineEdit(); self.search_entry.setPlaceholderText("Titel · Genre · Stimmung · Stil · Stimme · Tags"); self.search_entry.textChanged.connect(self.apply_view); sr.addWidget(self.search_entry,1); out.addLayout(sr)
        fl=QGridLayout(); self.filter_boxes={}
        for i,label in enumerate(("Genre","Stimmung","Stil","Stimme","Tags","Status")):
            fl.addWidget(QLabel(label),0,i); box=QComboBox(); box.addItem(FILTER_ALL); box.currentTextChanged.connect(self.apply_view); fl.addWidget(box,1,i); self.filter_boxes[label]=box
        self.favorite_check=QCheckBox("★ Nur Favoriten"); self.favorite_check.toggled.connect(self.apply_view); fl.addWidget(self.favorite_check,2,0,1,2)
        reset=QPushButton("Filter zurücksetzen"); reset.clicked.connect(self.reset_filters); fl.addWidget(reset,2,4,1,2); out.addLayout(fl)
        vr=QHBoxLayout(); vr.addWidget(QLabel("Sortierung:")); self.sort_box=QComboBox(); self.sort_box.addItems(SORT_OPTIONS); self.sort_box.currentTextChanged.connect(self.apply_view); vr.addWidget(self.sort_box); vr.addWidget(QLabel("Gruppierung:")); self.group_box=QComboBox(); self.group_box.addItems(GROUP_OPTIONS); self.group_box.currentTextChanged.connect(self.apply_view); vr.addWidget(self.group_box); vr.addStretch(); out.addLayout(vr)
        self.table=QTreeWidget(); self.table.setHeaderLabels(("Gruppe / Titel","★","Genre","Stimmung","Status","Tags","Zuletzt bearbeitet","Versionen")); self.table.setAlternatingRowColors(True); self.table.itemDoubleClicked.connect(lambda *_:self.open_selected()); out.addWidget(self.table,1)
        ar=QHBoxLayout(); op=QPushButton("Song öffnen"); op.clicked.connect(self.open_selected); ar.addWidget(op); vb=QPushButton("Versionsstände / Wiederherstellen"); vb.clicked.connect(self.show_versions); ar.addWidget(vb); ar.addStretch(); self.status_label=QLabel(); self.status_label.setObjectName("muted"); ar.addWidget(self.status_label); out.addLayout(ar)
    @staticmethod
    def _values(rows,attr):
        found=set()
        for r in rows:
            value=getattr(r.document,attr)
            if isinstance(value,list): found.update(x.strip() for x in value if x.strip())
            elif str(value).strip(): found.add(str(value).strip())
        return (FILTER_ALL,*sorted(found,key=str.casefold))
    def _set_values(self,box,values):
        current=box.currentText(); box.blockSignals(True); box.clear(); box.addItems(values); box.setCurrentText(current if current in values else FILTER_ALL); box.blockSignals(False)
    def _update_filter_values(self):
        for label,attr in {"Genre":"genre","Stimmung":"mood","Stil":"style","Stimme":"voice","Tags":"tags"}.items(): self._set_values(self.filter_boxes[label],self._values(self._rows,attr))
        self._set_values(self.filter_boxes["Status"],(FILTER_ALL,*SONG_STATUSES))
    def refresh(self):
        rows=[]
        for p in list_songs(self.project_root):
            try:
                d=load_song(p); rows.append(SongRow(p,d,p.stat().st_mtime,len(list_versions(self.project_root,d.title))))
            except (OSError,UnicodeError,ValueError): pass
        self._rows=rows; self._update_filter_values(); self.apply_view()
    def apply_view(self,*_):
        self.table.clear(); self._path_by_item.clear(); f=self.filter_boxes
        rows=[r for r in self._rows if song_matches(r,self.search_entry.text(),genre=f["Genre"].currentText(),mood=f["Stimmung"].currentText(),style=f["Stil"].currentText(),voice=f["Stimme"].currentText(),tag=f["Tags"].currentText(),status=f["Status"].currentText(),favorites_only=self.favorite_check.isChecked())]
        rows=sort_rows(rows,self.sort_box.currentText()); groups={}; group_by=self.group_box.currentText()
        for r in rows:
            parent=self.table.invisibleRootItem()
            if group_by!="Keine":
                g=row_group(r,group_by)
                if g not in groups:
                    groups[g]=QTreeWidgetItem([g]); self.table.addTopLevelItem(groups[g]); groups[g].setExpanded(True)
                parent=groups[g]
            d=r.document; item=QTreeWidgetItem((d.title,"★" if d.favorite else "",d.genre,d.mood,d.status,", ".join(d.tags),datetime.fromtimestamp(r.modified).strftime("%Y-%m-%d %H:%M"),str(r.versions))); parent.addChild(item) if parent is not self.table.invisibleRootItem() else self.table.addTopLevelItem(item); self._path_by_item[id(item)]=r.path
        self.table.resizeColumnToContents(0); self.status_label.setText(f"{len(rows)} von {len(self._rows)} Song(s)")
    def reset_filters(self):
        self.search_entry.clear(); [b.setCurrentText(FILTER_ALL) for b in self.filter_boxes.values()]; self.favorite_check.setChecked(False); self.apply_view(); self.search_entry.setFocus()
    def set_search(self,text): self.search_entry.setText(text); self.search_entry.setFocus()
    def selected_path(self):
        item=self.table.currentItem(); return self._path_by_item.get(id(item)) if item else None
    def open_selected(self):
        p=self.selected_path()
        if p:self.open_song_callback(p)
    def show_versions(self):
        path=self.selected_path()
        if not path:return
        d=load_song(path); versions=list_versions(self.project_root,d.title); dialog=QDialog(self); dialog.setWindowTitle(f"Versionsstände – {d.title}"); dialog.resize(820,600); l=QVBoxLayout(dialog)
        title=QLabel(f"Versionsstände · {d.title}"); title.setObjectName("sectionTitle"); l.addWidget(title); hint=QLabel("Erst Vorschau prüfen. Wiederherstellen sichert den aktuellen Stand automatisch als neue Version."); hint.setObjectName("muted"); hint.setWordWrap(True); l.addWidget(hint)
        listing=QListWidget(); [listing.addItem(v.stem) for v in versions]; l.addWidget(listing); preview=QTextEdit(); preview.setReadOnly(True); l.addWidget(preview,1); result=QLabel(); result.setObjectName("muted"); l.addWidget(result)
        def chosen():
            i=listing.currentRow(); return versions[i] if 0<=i<len(versions) else None
        def load_preview():
            v=chosen(); preview.setPlainText(v.read_text(encoding="utf-8") if v else "Noch keine älteren Versionsstände vorhanden.")
        listing.currentRowChanged.connect(lambda *_:load_preview())
        ar=QHBoxLayout(); restore=QPushButton("Diese Version wiederherstellen"); restore.setEnabled(bool(versions))
        def do_restore():
            v=chosen()
            if not v:return
            try:_target,backup=restore_version(self.project_root,path,v)
            except Exception as e: QMessageBox.critical(dialog,"Nicht wiederhergestellt",str(e)); return
            result.setText("Dieser Versionsstand entspricht bereits dem aktuellen Song." if backup is None else f"Wiederhergestellt · vorheriger Stand gesichert als {backup.name}"); self.refresh()
        restore.clicked.connect(do_restore); ar.addWidget(restore); ar.addStretch(); close=QPushButton("Schließen"); close.clicked.connect(dialog.accept); ar.addWidget(close); l.addLayout(ar)
        if versions: listing.setCurrentRow(0)
        else: load_preview()
        apply_global_style(dialog,self.zoom_percent); dialog.exec()
    def set_zoom(self,percent):
        self.zoom_percent=percent; apply_global_style(self,percent)
