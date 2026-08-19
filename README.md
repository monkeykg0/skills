# Codex Skills Collection

[English](README.md) | [简体中文](README.zh-CN.md)

A growing collection of production-oriented skills for Codex. Each skill is self-contained under `skills/` and includes concise agent instructions plus deterministic scripts and references where reliability matters.

## Included skills

| Skill | Purpose |
| --- | --- |
| `codex-desktop-pet` | Create, repair, validate, preview, and package animated pets for the Codex desktop app. |
| `codex-dream-skin` | Install, customize, verify, repair, and safely restore reversible Codex desktop themes. |
| `hand-drawn-illustration` | Turn articles and ideas into original, coherent hand-drawn editorial illustrations. |
| `ip-as-logo` | Generate highly simplified personified mascot logos with rounded, flat-first geometry. |

## Install a skill

Copy or symlink a skill directory into `${CODEX_HOME:-$HOME/.codex}/skills/`:

```bash
cp -R skills/codex-desktop-pet "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/codex-dream-skin "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/hand-drawn-illustration "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/ip-as-logo "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart or reload Codex so the skill catalog is refreshed. Invoke a skill explicitly with `$codex-desktop-pet`, `$codex-dream-skin`, `$hand-drawn-illustration`, or `$ip-as-logo`, or describe a matching task.

## Validate the repository

Install the single runtime dependency first:

```bash
python3 -m pip install -r requirements.txt
```

Then run:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

The desktop-pet integration test builds synthetic animation strips, runs the complete deterministic pipeline, validates the atlas, and verifies the packaged files.

## Add another skill

Create each new skill at `skills/<skill-name>/`. Keep its `SKILL.md` focused on execution, put detailed domain material in `references/`, and place repeatable or fragile transformations in `scripts/`.

This repository incorporates files derived from OpenAI's Apache-2.0-licensed `hatch-pet` skill. See `NOTICE` and the per-skill license.
