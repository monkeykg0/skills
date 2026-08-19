#!/usr/bin/env python3
"""Fetch a pinned Codex Dream Skin checkout or validate an existing one."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_REPOSITORY = "https://github.com/Fei-Away/Codex-Dream-Skin.git"
DEFAULT_REVISION = "2f038b5322702cfb248d9c7564b56470a389abc2"

REQUIRED = {
    "common": ("README.md", "docs/platforms.md"),
    "macos": (
        "macos/SKILL.md",
        "macos/README.md",
        "macos/assets/theme.json",
        "macos/scripts/install-dream-skin-macos.sh",
        "macos/scripts/start-dream-skin-macos.sh",
        "macos/scripts/verify-dream-skin-macos.sh",
        "macos/scripts/restore-dream-skin-macos.sh",
        "macos/tests/run-tests.sh",
    ),
    "windows": (
        "windows/SKILL.md",
        "windows/scripts/install-dream-skin.ps1",
        "windows/scripts/start-dream-skin.ps1",
        "windows/scripts/verify-dream-skin.ps1",
        "windows/scripts/restore-dream-skin.ps1",
        "windows/tests/run-tests.ps1",
    ),
}


def validate_macos_theme(root: Path) -> str:
    theme_path = root / "macos/assets/theme.json"
    try:
        theme = json.loads(theme_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid macOS bundled theme metadata: {error}") from error

    image = theme.get("image")
    if not isinstance(image, str) or not image or Path(image).name != image:
        raise ValueError("invalid macOS bundled theme image name")
    image_path = theme_path.parent / image
    if not image_path.is_file() or image_path.stat().st_size < 1:
        raise ValueError(f"macOS bundled theme image is missing or empty: {image}")
    return str(image_path.resolve())


def run(command: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{detail}")
    return completed.stdout.strip()


def fetch(repository: str, revision: str, destination: Path) -> Path:
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f"destination must not exist or must be empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "--quiet"], destination)
    run(["git", "remote", "add", "origin", repository], destination)
    run(["git", "fetch", "--depth", "1", "origin", revision], destination)
    run(["git", "checkout", "--quiet", "--detach", "FETCH_HEAD"], destination)
    return destination


def git_value(root: Path, *arguments: str) -> str | None:
    try:
        return run(["git", *arguments], root)
    except RuntimeError:
        return None


def validate(root: Path) -> dict[str, object]:
    root = root.resolve()
    missing = [
        relative
        for group in REQUIRED.values()
        for relative in group
        if not (root / relative).is_file()
    ]
    if missing:
        raise ValueError("not a complete Codex-Dream-Skin checkout; missing: " + ", ".join(missing))

    bundled_theme_image = validate_macos_theme(root)

    commit = git_value(root, "rev-parse", "HEAD")
    dirty_output = git_value(root, "status", "--short")
    return {
        "root": str(root),
        "commit": commit or "unknown (not a Git checkout)",
        "pinned_revision": DEFAULT_REVISION,
        "matches_pinned_revision": commit == DEFAULT_REVISION,
        "dirty": bool(dirty_output),
        "changed_paths": dirty_output.splitlines() if dirty_output else [],
        "bundled_theme_image": bundled_theme_image,
        "platforms": {
            "macos": str(root / "macos"),
            "windows": str(root / "windows"),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    location = parser.add_mutually_exclusive_group(required=True)
    location.add_argument("--source", type=Path, help="validate an existing checkout")
    location.add_argument("--destination", type=Path, help="fetch into an empty directory")
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--revision", default=DEFAULT_REVISION)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = args.source.resolve() if args.source else fetch(
            args.repository, args.revision, args.destination.resolve()
        )
        result = validate(root)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
