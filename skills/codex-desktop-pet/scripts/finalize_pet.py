#!/usr/bin/env python3
"""Run deterministic Codex pet processing, QA artifact creation, and packaging."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(script_dir: Path, name: str, *args: str) -> None:
    command = [sys.executable, str(script_dir / name), *args]
    subprocess.run(command, check=True)


def load_request(run_dir: Path) -> dict[str, object]:
    request_path = run_dir / "pet_request.json"
    if not request_path.is_file():
        raise SystemExit(f"missing pet request: {request_path}")
    request = json.loads(request_path.read_text(encoding="utf-8"))
    for key in ("pet_id", "display_name", "description"):
        if not isinstance(request.get(key), str) or not str(request[key]).strip():
            raise SystemExit(f"pet_request.json is missing a non-empty {key}")
    return request


def require_strips(run_dir: Path) -> None:
    states = (
        "idle",
        "running-right",
        "running-left",
        "waving",
        "jumping",
        "failed",
        "waiting",
        "running",
        "review",
    )
    missing = [state for state in states if not (run_dir / "decoded" / f"{state}.png").is_file()]
    if missing:
        raise SystemExit(f"missing decoded row strips: {', '.join(missing)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument(
        "--package-root",
        help="Destination containing pet-id folders. Defaults to $CODEX_HOME/pets or ~/.codex/pets.",
    )
    parser.add_argument(
        "--stable-slots",
        action="store_true",
        help="Preserve a shared row viewport after visually confirming source strips are stable.",
    )
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    script_dir = Path(__file__).resolve().parent
    request = load_request(run_dir)
    require_strips(run_dir)

    frames = run_dir / "frames"
    final = run_dir / "final"
    qa = run_dir / "qa"
    previews = qa / "previews"
    for directory in (frames, final, qa, previews):
        directory.mkdir(parents=True, exist_ok=True)

    extraction_method = "stable-slots" if args.stable_slots else "auto"
    run(
        script_dir,
        "extract_strip_frames.py",
        "--decoded-dir",
        str(run_dir / "decoded"),
        "--output-dir",
        str(frames),
        "--states",
        "all",
        "--method",
        extraction_method,
    )

    inspect_args = [
        "--frames-root",
        str(frames),
        "--json-out",
        str(qa / "review.json"),
        "--require-components",
    ]
    if args.stable_slots:
        inspect_args.append("--allow-stable-slots")
    run(script_dir, "inspect_frames.py", *inspect_args)

    run(
        script_dir,
        "compose_atlas.py",
        "--frames-root",
        str(frames),
        "--output",
        str(final / "spritesheet.png"),
        "--webp-output",
        str(final / "spritesheet.webp"),
    )
    run(
        script_dir,
        "validate_atlas.py",
        str(final / "spritesheet.webp"),
        "--json-out",
        str(final / "validation.json"),
    )
    run(
        script_dir,
        "make_contact_sheet.py",
        str(final / "spritesheet.webp"),
        "--output",
        str(qa / "contact-sheet.png"),
    )
    run(
        script_dir,
        "render_animation_previews.py",
        "--frames-root",
        str(frames),
        "--output-dir",
        str(previews),
    )

    package_root = (
        Path(args.package_root).expanduser().resolve()
        if args.package_root
        else Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "pets"
    )
    package_dir = package_root / str(request["pet_id"])
    package_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final / "spritesheet.webp", package_dir / "spritesheet.webp")
    pet_manifest = {
        "id": request["pet_id"],
        "displayName": request["display_name"],
        "description": request["description"],
        "spritesheetPath": "spritesheet.webp",
    }
    (package_dir / "pet.json").write_text(
        json.dumps(pet_manifest, indent=2) + "\n", encoding="utf-8"
    )

    summary = {
        "ok": True,
        "run_dir": str(run_dir),
        "extraction_method": extraction_method,
        "spritesheet": str(final / "spritesheet.webp"),
        "validation": str(final / "validation.json"),
        "contact_sheet": str(qa / "contact-sheet.png"),
        "previews": str(previews),
        "package": str(package_dir),
        "visual_qa_required": True,
    }
    (qa / "run-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
