"""Atomare Programm-Slotumschaltung mit Rückkehr. Nur für vorbereitete Slot-Installationen.

Niemals bestehende Projektordner direkt überschreiben; persönliche Daten
dürfen nicht innerhalb der austauschbaren Slots liegen.
"""
from __future__ import annotations

import json
from contextlib import contextmanager
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import tempfile

from app.atomic_io import atomic_write_json
from app.update_checkpoint import _copy_regular, _released, verify_checkpoint
from app.update_sandbox import _sandbox_command, run_isolated, verify_candidate
from app.update_staging import identity, sha256

SLOT = re.compile(r"[A-Za-z0-9_-]{1,80}\Z")
JOURNAL = "switch-journal.json"


def _managed(root):
    """Nur eine explizite Slot-Installation; alte normale Ordner nie migrieren."""
    root = Path(root).resolve(strict=True)
    slots = root / "slots"
    current = root / "current"
    if (not slots.is_dir() or slots.is_symlink() or not current.is_symlink()
            or (root / "daten").exists()):
        raise ValueError("Keine abgeschirmte Slot-Installation (oder ungeprüfter Datenordner).")
    target = os.readlink(current)
    parts = Path(target).parts
    if (len(parts) != 2 or parts[0] != "slots" or
            not SLOT.fullmatch(parts[1]) or (slots / parts[1]).is_symlink()):
        raise ValueError("Aktiver Slot ist kein erlaubter relativer Verweis.")
    active = (slots / parts[1]).resolve(strict=True)
    if active.parent != slots.resolve() or not active.is_dir():
        raise ValueError("Aktiver Slot verlässt den verwalteten Ordner.")
    return root, slots, current, parts[1], active


def _atomic_pointer(root, slot):
    if not SLOT.fullmatch(slot):
        raise ValueError("Ungültiger Slot.")
    if not (root / "slots" / slot).is_dir() or (root / "slots" / slot).is_symlink():
        raise ValueError("Ziel-Slot fehlt.")
    temporary = root / (".current-" + secrets.token_hex(12))
    try:
        os.symlink("slots/" + slot, temporary)
        os.replace(temporary, root / "current")
    finally:
        temporary.unlink(missing_ok=True)


def _health_check(slot):
    """Headless-Start ausschließlich im isolierten Namensraum, nie auf dem Host."""
    import shutil as _shutil
    binary = _shutil.which("bwrap")
    if not binary or not Path("/usr/bin/python3").is_file():
        return False
    try:
        process = subprocess.run(
            _sandbox_command(binary, slot), stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            cwd="/", timeout=30, close_fds=True, check=False)
        return process.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def _checkpoint_matches(active, folder):
    receipt = verify_checkpoint(folder)
    manifest = active / "MANIFEST.json"
    if sha256(manifest) != receipt["basis_manifest_sha256"]:
        raise ValueError("Sicherung und aktiver Programmstand sind verschieden.")
    for path, item in receipt["files"].items():
        source = active / path
        if source.is_symlink() or not source.is_file() or sha256(source) != item["sha256"]:
            raise ValueError("Aktiver Slot wurde nach der Sicherung verändert.")
    if set(_released(json.loads(manifest.read_text(encoding="utf-8")))) != set(receipt["files"]):
        raise ValueError("Freigabeliste und Checkpoint unterscheiden sich.")
    return receipt


def _journal(root):
    path = root / JOURNAL
    if not path.exists():
        return None
    if path.is_symlink() or path.stat().st_size > 10_000:
        raise ValueError("Wechselprotokoll ist kein vertrauenswürdiger Bestand.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(data, dict) or set(data) != {"schema", "state", "old", "new"}
            or data["schema"] != 1
            or data["state"] not in {"SWITCH_PENDING", "ACTIVE_VERIFIED", "ROLLED_BACK"}
            or not all(isinstance(data[k], str) and SLOT.fullmatch(data[k]) for k in ("old", "new"))
            or data["old"] == data["new"]):
        raise ValueError("Wechselprotokoll ist beschädigt.")
    return data


def _recover_pending_locked(root):
    """Nach Stromausfall eine unbestätigte Umschaltung zurücknehmen."""
    root, _slots, _pointer, active_slot, _active = _managed(root)
    journal = _journal(root)
    if journal is None or journal["state"] != "SWITCH_PENDING":
        return False
    if active_slot not in (journal["new"], journal["old"]):
        raise ValueError("Aktiver Slot widerspricht dem offenen Wechselprotokoll.")
    _atomic_pointer(root, journal["old"])
    atomic_write_json(root / JOURNAL, {**journal, "state": "ROLLED_BACK"})
    return True


def _activate_managed_locked(root, staging, checkpoint):
    """Wechselt nur bei gültiger Sandboxprobe und gültiger Sicherung.

    Der Slot-Wechsel wird nach einem sicheren Headless-Nachtest bestätigt;
    bei jedem Fehler wird der unveränderte alte Slot wieder eingehängt.
    """
    root, slots, _pointer, old, active = _managed(root)
    if (_journal(root) or {}).get("state") == "SWITCH_PENDING":
        raise ValueError("Unvollendeter Wechsel: zuerst recover_pending ausführen.")
    personal = active / "daten"
    if personal.is_symlink() or (personal.is_dir() and any(personal.iterdir())) or (personal.exists() and not personal.is_dir()):
        raise ValueError("Persönliche Arbeitsdaten dürfen nicht im austauschbaren Slot liegen.")
    if Path(staging).resolve().is_relative_to(root) or Path(checkpoint).resolve().is_relative_to(root):
        raise ValueError("Sicherung und Kandidat müssen außerhalb der Installation liegen.")
    _active, _folder, candidate, stage = verify_candidate(active, staging)
    receipt = _checkpoint_matches(active, checkpoint)
    if receipt["basis_manifest_sha256"] != stage["basis_manifest_sha256"]:
        raise ValueError("Ausgangsstand des Updatepakets passt nicht zum Checkpoint.")

    probe = run_isolated(active, staging)
    if probe["runtime_tests"] != "PASS" or probe["status"] != "ISOLATED_PROBE_PASSED_NOT_ACTIVATABLE":
        raise ValueError("Kandidat hat die isolierte Startprobe nicht bestanden.")

    new = "release-" + secrets.token_hex(12)
    target = slots / new
    target.mkdir(mode=0o700)
    journal_written = False
    try:
        data = json.loads((candidate / "MANIFEST.json").read_text(encoding="utf-8"))
        for relative in _released(data):
            before = sha256(candidate / relative)
            copied = _copy_regular(candidate / relative, target / relative)
            if copied["sha256"] != before or before != stage["files"][relative]:
                raise ValueError("Kandidatenkopie wurde beim Installieren verändert.")
        if not _health_check(target):
            raise ValueError("Installierter Slot hat die abgeschirmte Startprüfung nicht bestanden.")
        atomic_write_json(root / JOURNAL, {
            "schema": 1, "state": "SWITCH_PENDING", "old": old, "new": new,
        })
        journal_written = True
        _atomic_pointer(root, new)
        if not _health_check(target):
            raise ValueError("Startnachprüfung nach Umschaltung fehlgeschlagen.")
        atomic_write_json(root / JOURNAL, {
            "schema": 1, "state": "ACTIVE_VERIFIED", "old": old, "new": new,
        })
        return {"status": "ACTIVE_VERIFIED", "old": old, "new": new,
                "version": identity(data)["version"], "rollback_slot_kept": True}
    except BaseException:
        if journal_written:
            try:
                _atomic_pointer(root, old)
                atomic_write_json(root / JOURNAL, {
                    "schema": 1, "state": "ROLLED_BACK", "old": old, "new": new,
                })
            except OSError:
                # Der persistente SWITCH_PENDING-Beleg bleibt für den
                # nächsten recover_pending-Durchlauf erhalten.
                pass
        else:
            shutil.rmtree(target)
        raise


@contextmanager
def _exclusive(root):
    """Parallele Wechsel sperren; eine verwaiste Sperre wird NIE automatisch gelöscht."""
    root = Path(root).resolve(strict=True)
    lock = root / ".update-lock"
    lock.mkdir(mode=0o700)
    try:
        yield
    finally:
        lock.rmdir()


def recover_pending(root):
    with _exclusive(root):
        return _recover_pending_locked(root)


def activate_managed(root, staging, checkpoint):
    with _exclusive(root):
        return _activate_managed_locked(root, staging, checkpoint)
