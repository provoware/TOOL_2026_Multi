import stat
import unittest
import zipfile
from pathlib import Path


class Iteration36AcceptanceLauncherTests(unittest.TestCase):
    def test_user_facing_shell_launchers_are_executable_in_repository(self):
        root = Path(__file__).resolve().parent.parent
        for relative in ("schnellstart.sh", "kubuntu_abnahme.sh"):
            path = root / relative
            mode = path.stat().st_mode
            self.assertTrue(
                mode & stat.S_IXUSR,
                f"{relative} ist nicht als ausführbar markiert. Klick-&-Start wäre nach dem Entpacken unnötig erschwert.",
            )

    def test_full_project_git_archive_contract_requires_executable_acceptance_launcher(self):
        root = Path(__file__).resolve().parent.parent
        mode = (root / "kubuntu_abnahme.sh").stat().st_mode
        self.assertTrue(mode & stat.S_IXUSR)

    def test_runtime_release_zip_preserves_executable_launcher_bits(self):
        root = Path(__file__).resolve().parent.parent
        archive = root / "release" / "_iteration36_permission_probe.zip"
        archive.parent.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as handle:
                handle.write(root / "kubuntu_abnahme.sh", arcname="kubuntu_abnahme.sh")
            with zipfile.ZipFile(archive, "r") as handle:
                info = handle.getinfo("kubuntu_abnahme.sh")
                archived_mode = (info.external_attr >> 16) & 0o777
            self.assertTrue(
                archived_mode & 0o100,
                f"ZIP hat kubuntu_abnahme.sh ohne Ausführungsrecht gespeichert: {oct(archived_mode)}",
            )
        finally:
            archive.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
