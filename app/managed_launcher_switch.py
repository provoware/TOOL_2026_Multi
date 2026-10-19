"""Atomarer Launcher-Wechsel ausschließlich für bereits verwaltete Links.

Normale Schnellstart-Skripte werden niemals umbenannt oder überschrieben.
Ein dauerhafter Journalbeleg macht eine unterbrochene Probe reversibel.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import secrets
import stat

from app.atomic_io import atomic_write_json

RECORD = "launcher-switch.json"


def _roots(directory):
    root = Path(directory).resolve(strict=True)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Launcher-Verzeichnis fehlt.")
    current = root / "start"
    old = root / "legacy_start.sh"
    new = root / "managed_start.sh"
    if (not current.is_symlink() or old.is_symlink() or new.is_symlink()
            or not old.is_file() or not new.is_file()):
        raise ValueError("Nur vorbereitete Launcher-Links sind austauschbar.")
    if not stat.S_ISREG(old.stat().st_mode) or not stat.S_ISREG(new.stat().st_mode):
        raise ValueError("Starter müssen reguläre Dateien sein.")
    if os.readlink(current) not in ("legacy_start.sh", "managed_start.sh"):
        raise ValueError("Unbekanntes Launcher-Ziel.")
    return root, current, old, new


def _set_pointer(root, name):
    if name not in ("legacy_start.sh", "managed_start.sh"):
        raise ValueError("Ungültiges Zeigerziel.")
    tmp = root / (".start-" + secrets.token_hex(12))
    try:
        tmp.symlink_to(name)
        os.replace(tmp, root / "start")
    finally:
        tmp.unlink(missing_ok=True)


def _record(root):
    path = root / RECORD
    if not path.exists():
        return None
    if path.is_symlink() or path.stat().st_size > 2048:
        raise ValueError("Unzuverlässiges Wechselprotokoll.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(data, dict) or set(data) != {"schema", "state"}
            or data["schema"] != 1
            or data["state"] not in ("PENDING", "VERIFIED", "ROLLED_BACK")):
        raise ValueError("Wechselprotokoll beschädigt.")
    return data


def recover_launcher(directory):
    """Bei jedem unbestätigten Wechsel den Altstart wiederherstellen."""
    root, _pointer, _old, _new = _roots(directory)
    record = _record(root)
    if record is None or record["state"] != "PENDING":
        return False
    _set_pointer(root, "legacy_start.sh")
    atomic_write_json(root / RECORD, {"schema": 1, "state": "ROLLED_BACK"})
    return True


def switch_managed_launcher(directory, *, approved=False, verify=None):
    """Wechsel nur für einen vom Programm *zuvor* erstellten Wrapper.

    Verwendet niemals bestehende reguläre Altstart-Skripte als Ziel für replace.
    Ein Crash nach dem Wechsel muss per recover_launcher zurückgeführt werden.
    """
    if approved is not True:
        raise PermissionError("Ausdrückliche Freigabe erforderlich.")
    root, current, _old, _new = _roots(directory)
    if os.readlink(current) != "legacy_start.sh":
        raise ValueError("Launcher wurde bereits umgestellt.")
    if (_record(root) or {}).get("state") == "PENDING":
        raise ValueError("Ausstehende Umschaltung zuerst zurücksetzen.")
    if not callable(verify):
        raise ValueError("Ein unabhängiger Startprüfer fehlt.")
    if verify("managed_start.sh") is not True:
        raise RuntimeError("Vorprüfung des neuen Schnellstarts fehlgeschlagen.")
    atomic_write_json(root / RECORD, {"schema": 1, "state": "PENDING"})
    try:
        _set_pointer(root, "managed_start.sh")
        if verify("managed_start.sh") is not True:
            raise RuntimeError("Nachprüfung des neuen Schnellstarts fehlgeschlagen.")
        atomic_write_json(root / RECORD, {"schema": 1, "state": "VERIFIED"})
        return True
    except BaseException:
        # Bei einem Fehler vor oder nach dem Zeigertausch bleibt die Altdatei erhalten.
        recover_launcher(root)
        raise


def launch_checked(directory, *, runner):
    """Rückkehr bei unbestätigtem Wechsel und bei Fehler des neuen Starters.

    Der Aufrufer liefert einen kontrollierten Prozessstarter, statt beliebige
    Shellbefehle aus JSON oder Dateinamen zu übernehmen.
    """
    if not callable(runner):
        raise ValueError("Ein geprüfter Prozessstarter fehlt.")
    root, pointer, old, new = _roots(directory)
    recover_launcher(root)
    target = os.readlink(pointer)
    status = runner(root / target)
    if type(status) is not int:
        raise ValueError("Startvorgang lieferte keinen gültigen Status.")
    if status != 0 and target == "managed_start.sh":
        _set_pointer(root, "legacy_start.sh")
        atomic_write_json(root / RECORD, {"schema": 1, "state": "ROLLED_BACK"})
    return status
