import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_DIRS = {".venv", "__pycache__", "logs", "berichte", "tmp", "backups", "release"}
FORBIDDEN_NAMES = {".DS_Store", "Thumbs.db"}
FORBIDDEN_SUFFIXES = (".pyc", ".pyo", ".log", ".tmp", ".bak", ".swp", ".zip", ".sha256")
FORBIDDEN_ROOT_PREFIXES = ("ChatGPT Image ", "Screenshot", "Bildschirmfoto")
MAX_ROOT_FILE_BYTES = 1_000_000


class RepositoryHygieneTests(unittest.TestCase):
    def test_no_tracked_runtime_or_local_artifacts(self):
        output = subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=ROOT
        ).decode("utf-8")
        tracked = [path for path in output.split("\0") if path]
        offenders = []

        for relative in tracked:
            path = Path(relative)
            if any(part in FORBIDDEN_DIRS for part in path.parts):
                offenders.append(relative)
                continue
            if path.name in FORBIDDEN_NAMES or path.name.endswith(FORBIDDEN_SUFFIXES):
                offenders.append(relative)
                continue
            if len(path.parts) == 1 and path.name.startswith(FORBIDDEN_ROOT_PREFIXES):
                offenders.append(relative)
                continue
            full_path = ROOT / path
            if len(path.parts) == 1 and full_path.is_file() and full_path.stat().st_size > MAX_ROOT_FILE_BYTES:
                offenders.append(relative)

        self.assertEqual([], offenders, f"Versionierte Repo-Artefakte gefunden: {offenders}")


if __name__ == "__main__":
    unittest.main()
