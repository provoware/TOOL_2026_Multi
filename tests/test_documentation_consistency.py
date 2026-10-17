"""Verhindert widersprüchliche oder fehlende Projektinformationen."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORTANT = (
    "README.md", "ANLEITUNG_LAIEN.md", "CHANGELOG.md",
    "TODO.md", "docs/README.md", "docs/AKTUELLER_STAND.md",
    "docs/ORDNERSTRUKTUR.md", "AGENTS.md",
)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class DocumentationConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))

    def test_project_version_matches_current_documentation(self):
        version = self.manifest["tool"]["version"]
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        status = (ROOT / "docs/AKTUELLER_STAND.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("**Version:** " + version, readme)
        self.assertIn("**Programmversion:** " + version, status)
        self.assertIn("## " + version, changelog)

    def test_required_information_files_exist(self):
        for relative in IMPORTANT:
            with self.subTest(file=relative):
                self.assertTrue((ROOT / relative).is_file(), f"Infodatei fehlt: {relative}")

    def test_internal_markdown_links_resolve(self):
        for relative in IMPORTANT:
            source = ROOT / relative
            text = source.read_text(encoding="utf-8")
            for target in LINK.findall(text):
                target = target.split("#", 1)[0].split("?", 1)[0]
                if not target or "://" in target or target.startswith(("mailto:", "#")):
                    continue
                file = (source.parent / target).resolve()
                with self.subTest(source=relative, link=target):
                    self.assertTrue(file.is_relative_to(ROOT.resolve()), "Link verlässt das Repository")
                    self.assertTrue(file.exists(), f"Linkziel fehlt: {relative} → {target}")

    def test_manifest_entrypoints_exist(self):
        for category in ("runtime",):
            for key, relative in self.manifest[category].items():
                if key in {"entrypoint", "launcher", "kubuntu_acceptance_launcher", "requirements", "watcher", "diagnostic_package"}:
                    with self.subTest(key=key):
                        self.assertTrue((ROOT / relative).is_file(), f"Datei fehlt: {relative}")

    def test_release_paths_in_manifest_exist(self):
        for entry in self.manifest["files"]:
            with self.subTest(file=entry["path"]):
                self.assertTrue((ROOT / entry["path"]).is_file(), f"Manifest-Datei fehlt: {entry['path']}")

    def test_capability_summary_marks_ideas_as_unfinished(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        status = (ROOT / "docs/AKTUELLER_STAND.md").read_text(encoding="utf-8")
        for topic in ("Genre-Zufall", "Reimfinder", "Dateisuche"):
            with self.subTest(feature=topic):
                self.assertIn(topic, readme)
                self.assertIn(topic, status)
        self.assertIn("**Noch nicht fertig", readme)
        self.assertIn("## Was ist noch nicht fertig?", status)


if __name__ == "__main__":
    unittest.main()
