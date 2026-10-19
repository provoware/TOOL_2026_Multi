"""Experimentelle Fremdcodeprobe nur im Linux-Bubblewrap-Namensraum.

KEINE Integration als produktiver Plugin-Loader. Keine Projektordner eingebunden,
kein Netz, keine Host-Privilegien. Fail closed ohne bwrap.
"""
from __future__ import annotations
import json
import os
import resource
from pathlib import Path
import shutil
import subprocess

MAX_PLUGIN = 64_000
MAX_STDOUT = 32_000
MAX_MEMORY = 256 * 1024 * 1024
MAX_CPU_SECONDS = 5
MAX_FILE_OUTPUT = 1024 * 1024


def _resource_limits():
    """Kernel-Limits gelten zusätzlich zum abgebrochenen Zeitlimit."""
    resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_SECONDS, MAX_CPU_SECONDS))
    resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_FILE_OUTPUT, MAX_FILE_OUTPUT))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))

def probe_plugin(plugin_file, *, approved=False, timeout=8):
    if approved is not True:
        raise PermissionError("Keine ausdrückliche Freigabe für Fremdcode.")
    executable=shutil.which("bwrap")
    if not executable or not Path("/usr/bin/python3").is_file():
        raise RuntimeError("Linux-Sandbox fehlt. Fremdcode bleibt gesperrt.")
    if type(timeout) not in (int, float) or not 1 <= timeout <= 15:
        raise ValueError("Zeitlimit muss zwischen 1 und 15 Sekunden liegen.")
    source=Path(plugin_file)
    if (source.is_symlink() or not source.is_file() or source.suffix!=".py"
            or source.stat().st_size>MAX_PLUGIN or source.stat().st_size==0):
        raise ValueError("Unzulässige Plugin-Datei.")
    source=source.resolve(strict=True)
    args=[executable,"--unshare-all","--die-with-parent","--new-session",
        "--cap-drop","ALL","--ro-bind","/usr","/usr"]
    for part in ("/lib","/lib64"):
        if Path(part).is_dir():
            args+=["--ro-bind",part,part]
    args+=["--proc","/proc","--dev","/dev","--tmpfs","/tmp",
           "--dir","/work","--ro-bind",str(source),"/work/extension.py",
           "--chdir","/work","--setenv","HOME","/tmp",
           "--setenv","PYTHONPATH","","--","/usr/bin/python3","-I",
           "/work/extension.py"]
    try:
        result=subprocess.run(args,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,check=False,timeout=timeout,
                              preexec_fn=_resource_limits,
                              env={"PATH":"/usr/bin:/bin"})
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise RuntimeError("Fremdcodeprobe fehlgeschlagen oder abgebrochen.") from exc
    if result.returncode or len(result.stdout)>MAX_STDOUT:
        raise RuntimeError("Fremdcodeprobe nicht bestanden.")
    try:
        response=json.loads(result.stdout.decode("utf-8"))
    except (UnicodeError,ValueError) as exc:
        raise ValueError("Fremdcode liefert keine erlaubte JSON-Antwort.") from exc
    from app.module_extension import validate_extension
    return validate_extension(response)
