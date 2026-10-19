"""Import lokaler Projekt-ZIPs: vollständige Prüfung, niemals Überschreiben."""
from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
import zipfile
from uuid import uuid4

from app import development_pool as pool
from app import module_archive as archive

MAX_JSON = 16 * 1024


def import_project_copy(root, source):
    root=Path(root)
    file=Path(source)
    if file.is_symlink() or not file.is_file() or file.stat().st_size > pool.MAX_TOTAL + 4*1024*1024:
        raise ValueError("Ungültiges oder zu großes Projektarchiv.")
    with zipfile.ZipFile(file) as z:
        infos=z.infolist()
        if not infos or len(infos)>pool.MAX_FILES+1:
            raise ValueError("Zu viele Archivdateien.")
        names=[i.filename for i in infos]
        if len(names)!=len(set(names)) or names.count("projekt.json")!=1:
            raise ValueError("Mehrdeutiger Archivinhalt.")
        if z.getinfo("projekt.json").file_size>MAX_JSON:
            raise ValueError("Projektbeschreibung zu groß.")
        metadata=json.loads(z.read("projekt.json").decode("utf-8"))
        item=pool.validate_project(metadata)
        total=0
        for info in infos:
            name=info.filename
            parts=PurePosixPath(name).parts
            if (name=="projekt.json"):
                continue
            if (info.is_dir() or len(parts)<2 or parts[0]!="arbeit"
                    or any(p in ("..",".","") for p in parts)
                    or name.startswith("/") or "\\" in name
                    or stat.S_IFMT(info.external_attr>>16) not in (0,stat.S_IFREG)):
                raise ValueError("Archiv enthält unsichere Pfade oder Dateitypen.")
            if info.file_size>pool.MAX_FILE:
                raise ValueError("Projektdatei zu groß.")
            total+=info.file_size
            if total>pool.MAX_TOTAL:
                raise ValueError("Projektarchiv zu groß.")
        state=pool.load(root)
        new_id=uuid4().hex
        existing={p["name"].casefold() for p in state["projects"]}
        title=item["name"]
        index=2
        while item["name"].casefold() in existing:
            suffix=f" (Import {index})"
            item["name"]=title[:150-len(suffix)]+suffix
            index+=1
        item["id"]=new_id
        destination=pool.workspace(root,new_id)
        if destination.exists() or destination.is_symlink():
            raise ValueError("Arbeitsordner ist bereits belegt.")
        destination.mkdir(parents=True)
        try:
            for info in infos:
                if info.filename=="projekt.json":
                    continue
                target=destination.joinpath(*PurePosixPath(info.filename).parts[1:])
                target.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info) as inp, target.open("xb") as out:
                    count=0
                    while block:=inp.read(1024*1024):
                        count+=len(block)
                        if count>pool.MAX_FILE or count>info.file_size:
                            raise ValueError("Dateigröße weicht ab.")
                        out.write(block)
                    if count!=info.file_size:
                        raise ValueError("Archivinhalt unvollständig.")
            state["projects"].append(item)
            archive.save(root,pool.MODULE,state,pool.validate)
        except BaseException:
            shutil.rmtree(destination)
            raise
    return item
