---
name: codex-dream-skin
description: Install, customize, launch, verify, repair, update, or restore a reversible decorative theme for the official Codex desktop app on macOS or Windows using the Fei-Away/Codex-Dream-Skin project. Use when a user asks to skin or theme Codex beyond official color settings, turn a personal image into a Codex banner or task background, reapply a theme after an app update, troubleshoot CDP injection, or safely return to the official appearance without modifying app.asar, WindowsApps, the signed app bundle, user tasks, authentication, or model-provider settings.
---

# Codex Dream Skin

Manage the upstream Dream Skin project as a reversible external theme. Keep Codex's native sidebar, cards, project selector, task content, menus, and composer interactive.

## Read before acting

- Read `references/platform-workflows.md` for the current platform before running commands.
- Read `references/security-boundaries.md` before installation, launch, repair, or restore.
- Read `references/qa-checklist.md` before accepting a live theme.

Use the bundled preparation script to obtain a known upstream revision or validate an existing checkout. The script never installs or launches the theme:

```bash
python scripts/prepare_upstream.py --destination /absolute/path/to/Codex-Dream-Skin
```

For an existing checkout:

```bash
python scripts/prepare_upstream.py --source /absolute/path/to/Codex-Dream-Skin
```

Report the resolved commit. Keep the pinned revision unless the user asks for the latest upstream version. Before executing downloaded code, inspect the platform `SKILL.md`, README, entry scripts, and repository status.

## Workflow

1. Identify macOS or Windows, the requested operation, the source image if any, and whether Codex is already open. Infer low-risk visual choices; do not restart a running Codex instance without explicit authorization.
2. Prepare or validate the upstream checkout. Stop if required files are missing, the checkout is unexpectedly dirty, or the platform is unsupported.
3. Run the platform's static tests and preflight checks before installation. On macOS, apply the signature-trust triage in `references/platform-workflows.md`; a sandbox that cannot validate a known system binary cannot adjudicate the Codex signature. Treat a failure reproduced in a working trust context, or any package identity, Node runtime, port ownership, config encoding, payload, or target-validation failure as a blocker.
4. Install only through the upstream platform entry point. Do not copy isolated CSS or JavaScript into Codex and do not modify official installation files.
5. Customize only when requested. On macOS, use the upstream customization command with the user's image and colors. Windows currently ships a fixed reference theme; explain that limitation instead of inventing unsupported flags.
6. Start or reapply the theme, then run the upstream verify command. Inspect both the home route and a normal task using `references/qa-checklist.md`; a successful command alone is insufficient visual proof.
7. Restore when requested or when safe verification cannot be completed. Confirm that the injector/debug session is stopped and that Codex opens normally.

## Image creation

If the user asks to generate or edit a theme image, load and follow `$imagegen` before creating it. Prefer a wide image at least 2000 px across, keep the left side calm for home titles, and avoid readable UI, logos, watermarks, or a fake full-window Codex screenshot. Treat user-provided people, characters, and brands as licensed only for the requested private use; flag redistribution risks.

## Repair discipline

- Diagnose before changing state: inspect the upstream status/doctor output, logs, recorded PID and port, current checkout commit, and Codex version.
- Reapply after normal navigation or app-update drift; reinstall only when upstream diagnostics require it.
- Never kill a process solely by a saved PID. Require the upstream identity checks to match executable, ownership, command line, and start time.
- Never overwrite all of `~/.codex/config.toml`. Preserve unrelated keys, UTF-8 encoding, authentication, pets, plugins, and model-provider settings.
- Prefer the smallest reversible action. Use the platform restore command rather than deleting state directories by hand.

## Completion report

State the platform, upstream commit, operation performed, test/preflight result, live verification result for home and task views, and whether restoration was tested or remains available. Distinguish command output from visual inspection and list any unverified item explicitly.
