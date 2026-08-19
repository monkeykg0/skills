from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REQUIRED_FILES = (
    "README.md",
    "docs/platforms.md",
    "macos/SKILL.md",
    "macos/README.md",
    "macos/assets/theme.json",
    "macos/scripts/install-dream-skin-macos.sh",
    "macos/scripts/start-dream-skin-macos.sh",
    "macos/scripts/verify-dream-skin-macos.sh",
    "macos/scripts/restore-dream-skin-macos.sh",
    "macos/tests/run-tests.sh",
    "windows/SKILL.md",
    "windows/scripts/install-dream-skin.ps1",
    "windows/scripts/start-dream-skin.ps1",
    "windows/scripts/verify-dream-skin.ps1",
    "windows/scripts/restore-dream-skin.ps1",
    "windows/tests/run-tests.ps1",
)


class PrepareDreamSkinUpstreamTest(unittest.TestCase):
    @property
    def script(self) -> Path:
        repo = Path(__file__).resolve().parents[1]
        return repo / "skills" / "codex-dream-skin" / "scripts" / "prepare_upstream.py"

    def run_script(self, source: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.script), "--source", str(source)],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def make_complete_checkout(self, source: Path) -> None:
        for relative in REQUIRED_FILES:
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("placeholder\n", encoding="utf-8")
        assets = source / "macos" / "assets"
        (assets / "theme.json").write_text(
            json.dumps({"image": "portal-hero.png"}), encoding="utf-8"
        )
        (assets / "portal-hero.png").write_bytes(b"image")

    def test_validates_complete_existing_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            self.make_complete_checkout(source)

            completed = self.run_script(source)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["root"], str(source.resolve()))
            self.assertEqual(result["commit"], "unknown (not a Git checkout)")
            self.assertEqual(
                result["pinned_revision"],
                "2f038b5322702cfb248d9c7564b56470a389abc2",
            )
            self.assertFalse(result["dirty"])
            self.assertEqual(
                result["bundled_theme_image"],
                str((source / "macos/assets/portal-hero.png").resolve()),
            )
            self.assertEqual(result["platforms"]["macos"], str(source.resolve() / "macos"))
            self.assertEqual(result["platforms"]["windows"], str(source.resolve() / "windows"))

    def test_rejects_incomplete_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed = self.run_script(Path(temporary))

            self.assertEqual(completed.returncode, 1)
            self.assertIn("not a complete Codex-Dream-Skin checkout", completed.stderr)
            self.assertIn("README.md", completed.stderr)

    def test_rejects_missing_bundled_theme_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            self.make_complete_checkout(source)
            (source / "macos/assets/portal-hero.png").unlink()

            completed = self.run_script(source)

            self.assertEqual(completed.returncode, 1)
            self.assertIn("macOS bundled theme image is missing or empty", completed.stderr)


if __name__ == "__main__":
    unittest.main()
