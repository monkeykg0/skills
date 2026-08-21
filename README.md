# Codex Skills Collection

[English](README.md) | [简体中文](README.zh-CN.md)

A growing collection of production-oriented skills for Codex. Each skill is self-contained under `skills/` and includes concise agent instructions plus deterministic scripts and references where reliability matters.

## Included skills

| Skill | Purpose |
| --- | --- |
| `baoyu-article-illustrator` | Analyze articles and generate coherent supporting illustrations. |
| `baoyu-cover-image` | Generate configurable article covers across type, palette, rendering, text, and mood. |
| `baoyu-post-to-wechat` | Publish articles or image-text posts to a WeChat Official Account via API or Chrome. |
| `codex-desktop-pet` | Create, repair, validate, preview, and package animated pets for the Codex desktop app. |
| `codex-dream-skin` | Install, customize, verify, repair, and safely restore reversible Codex desktop themes. |
| `hand-drawn-illustration` | Turn articles and ideas into original, coherent hand-drawn editorial illustrations. |
| `ip-as-logo` | Generate highly simplified personified mascot logos with rounded, flat-first geometry. |
| `kid-papercraft` | Create personalized three-part papercraft stop-motion birthday video prompts for children. |

## Install a skill

Copy or symlink a skill directory into `${CODEX_HOME:-$HOME/.codex}/skills/`:

```bash
cp -R skills/baoyu-article-illustrator "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/baoyu-cover-image "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/baoyu-post-to-wechat "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/codex-desktop-pet "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/codex-dream-skin "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/hand-drawn-illustration "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/ip-as-logo "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/kid-papercraft "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart or reload Codex so the skill catalog is refreshed. Invoke any skill explicitly with `$<skill-name>`, or describe a matching task.

The WeChat publishing skill intentionally excludes installed `node_modules` and credentials. Install its locked JavaScript dependencies when needed:

```bash
(cd "${CODEX_HOME:-$HOME/.codex}/skills/baoyu-post-to-wechat/scripts" && bun install --frozen-lockfile)
```

If `bun` is not installed, use `npx -y bun` in its place. Store WeChat credentials in a user- or project-level `.baoyu-skills/.env`; never commit that file.

## Validate the repository

Install the Python validation dependency first:

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

This repository incorporates third-party skill material under Apache-2.0 and MIT licenses. See `NOTICE` and the per-skill licenses.
