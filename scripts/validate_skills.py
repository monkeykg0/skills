#!/usr/bin/env python3
"""Validate the minimal structure and metadata of every skill in this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        raw = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return ["missing SKILL.md"]
    try:
        metadata = frontmatter(skill_file)
    except ValueError as exc:
        return [str(exc)]
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != skill_dir.name:
        errors.append(f"frontmatter name {name!r} does not match folder name")
    if not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        errors.append("name must be <=64 characters of lowercase letters, digits, and hyphens")
    if not description:
        errors.append("description is required")
    if set(metadata) != {"name", "description"}:
        errors.append("frontmatter must contain only name and description")
    agent_file = skill_dir / "agents" / "openai.yaml"
    if not agent_file.is_file():
        errors.append("missing recommended agents/openai.yaml")
    else:
        agent_text = agent_file.read_text(encoding="utf-8")
        if f"$${name}" in agent_text:
            errors.append("default prompt contains an invalid double-dollar invocation")
        if f"${name}" not in agent_text:
            errors.append("default prompt must explicitly invoke the skill")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    skills_root = root / "skills"
    failed = False
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        errors = validate(skill_dir)
        if errors:
            failed = True
            print(f"FAIL {skill_dir.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {skill_dir.name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
