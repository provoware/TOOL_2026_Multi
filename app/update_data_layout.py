"""Konservative Trennung von Laufzeitcode und Datenpfad ohne Bestandsmigration."""
from pathlib import Path

def inspect_external_data_layout(install_root,data_root):
    program=Path(install_root).resolve(strict=True)
    data=Path(data_root).expanduser().resolve(strict=True)
    if not program.is_dir() or not data.is_dir() or data.is_symlink():
        raise ValueError("Programm- und Datenordner müssen bestehende Verzeichnisse sein.")
    if data==program or data.is_relative_to(program) or program.is_relative_to(data):
        raise ValueError("Daten- und Programmordner müssen voneinander unabhängig sein.")
    if (program/"daten").exists() or (program/"daten").is_symlink():
        raise ValueError("Programmordner enthält noch eigene Daten; Migration gesperrt.")
    return {"code_root":str(program),"data_root":str(data),
            "separation_verified":True,"migration_performed":False}
