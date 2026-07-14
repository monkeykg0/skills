from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


FRAME_COUNTS = {
    "idle": 6,
    "running-right": 8,
    "running-left": 8,
    "waving": 4,
    "jumping": 5,
    "failed": 8,
    "waiting": 6,
    "running": 6,
    "review": 6,
}


class DesktopPetPipelineTest(unittest.TestCase):
    def test_synthetic_pet_pipeline(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        scripts = repo / "skills" / "codex-desktop-pet" / "scripts"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_dir = root / "run"
            decoded = run_dir / "decoded"
            decoded.mkdir(parents=True)
            request = {
                "pet_id": "test-pet",
                "display_name": "Test Pet",
                "description": "A synthetic validation pet.",
                "chroma_key": {"hex": "#FF00FF", "rgb": [255, 0, 255]},
            }
            (run_dir / "pet_request.json").write_text(
                json.dumps(request), encoding="utf-8"
            )

            colors = [
                (35, 99, 235),
                (22, 163, 74),
                (234, 88, 12),
                (20, 150, 70),
                (20, 130, 180),
                (8, 145, 178),
                (202, 138, 4),
                (220, 38, 38),
                (71, 85, 105),
            ]
            for row, (state, count) in enumerate(FRAME_COUNTS.items()):
                strip = Image.new("RGB", (count * 192, 208), "#FF00FF")
                draw = ImageDraw.Draw(strip)
                for frame in range(count):
                    left = frame * 192 + 57
                    top = 45 + (frame % 2) * 3
                    draw.rounded_rectangle(
                        (left, top, left + 78, top + 116),
                        radius=24,
                        fill=colors[row],
                    )
                    draw.ellipse((left + 19, top + 28, left + 29, top + 38), fill="white")
                    draw.ellipse((left + 49, top + 28, left + 59, top + 38), fill="white")
                strip.save(decoded / f"{state}.png")

            result = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "finalize_pet.py"),
                    "--run-dir",
                    str(run_dir),
                    "--package-root",
                    str(root / "packages"),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode:
                self.fail(
                    "finalize_pet.py failed\n"
                    f"stdout:\n{result.stdout}\n"
                    f"stderr:\n{result.stderr}"
                )
            self.assertIn('"ok": true', result.stdout)

            atlas_path = run_dir / "final" / "spritesheet.webp"
            with Image.open(atlas_path) as atlas:
                self.assertEqual(atlas.size, (1536, 1872))
                self.assertIn("A", atlas.mode)

            validation = json.loads(
                (run_dir / "final" / "validation.json").read_text(encoding="utf-8")
            )
            self.assertTrue(validation["ok"])
            self.assertEqual(validation["transparent_rgb_residue_pixels"], 0)
            self.assertTrue((run_dir / "qa" / "contact-sheet.png").is_file())
            self.assertEqual(len(list((run_dir / "qa" / "previews").glob("*.gif"))), 9)
            self.assertTrue((root / "packages" / "test-pet" / "pet.json").is_file())
            self.assertTrue(
                (root / "packages" / "test-pet" / "spritesheet.webp").is_file()
            )


if __name__ == "__main__":
    unittest.main()
