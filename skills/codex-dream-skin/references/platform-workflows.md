# Platform workflows

The commands below target the upstream `Fei-Away/Codex-Dream-Skin` checkout prepared by `scripts/prepare_upstream.py`. Run them from the indicated platform directory and read that directory's current README and `SKILL.md` first.

## macOS

Requirements:

- macOS with the official Codex Desktop app installed and launched at least once.
- `~/.codex/config.toml` exists.
- The upstream preflight accepts Codex's signed bundled Node runtime.

From `macos/`:

```bash
./tests/run-tests.sh
./scripts/doctor-macos.sh
./scripts/install-dream-skin-macos.sh --no-launch
./scripts/customize-theme-macos.sh --image "/absolute/path/to/image.png" --name "Theme name"
./scripts/start-dream-skin-macos.sh
./scripts/verify-dream-skin-macos.sh
./scripts/restore-dream-skin-macos.sh
```

### macOS signature-trust triage

Codex sandboxes can prevent `codesign` from reaching the macOS trust service. Before treating an app or bundled-Node signature error as real, verify a known system binary in the same execution context:

```bash
/usr/bin/codesign --verify --strict --verbose=4 /bin/ls
```

- If `/bin/ls` verifies, run the upstream tests and doctor normally. A Codex-only signature failure is a blocker.
- If `/bin/ls` fails with `CSSMERR_TP_NOT_TRUSTED`, `Authority=(unavailable)`, an internal Code Signing error, or another trust-service failure, the current context cannot adjudicate signatures. Do not report Codex as modified from that result.
- Request approval to rerun the exact `/usr/bin/codesign`, `./tests/run-tests.sh`, and `./scripts/doctor-macos.sh` checks outside the sandbox. Accept the signature only if `/bin/ls`, the Codex bundle, and its bundled Node all verify there.

This exception changes only where read-only verification runs. Installation, process control, configuration changes, and CDP launch remain subject to their normal approvals and guardrails.

The Finder-facing `.command` launchers are suitable when the user prefers interactive installation or image selection. Running them opens or restarts GUI processes, so obtain any required local approval and explicit authorization before restarting an already-open Codex instance.

Installed engine and state normally live at:

- `~/.codex/codex-dream-skin-studio`
- `~/Library/Application Support/CodexDreamSkinStudio`

macOS supports a personal image plus theme name and accent colors. Use the current upstream README for accepted image formats, size limits, and any new flags.

## Windows

Requirements:

- Windows with the official Store-installed Codex app.
- Node.js 22 or newer.
- Windows PowerShell capable of running the checked-out scripts.

From `windows/`:

```powershell
powershell -NoProfile -File tests\run-tests.ps1
node --check scripts\injector.mjs
node --check assets\renderer-inject.js
powershell -NoProfile -File scripts\install-dream-skin.ps1
powershell -NoProfile -File scripts\start-dream-skin.ps1
powershell -NoProfile -File scripts\verify-dream-skin.ps1 -ScreenshotPath C:\absolute\path\dream-skin.png
powershell -NoProfile -File scripts\restore-dream-skin.ps1
```

The CLI launcher requires `-RestartExisting` to restart an open Codex instance. Do not add it until the user explicitly authorizes the restart.

State normally lives under `%LOCALAPPDATA%\CodexDreamSkin`. Windows uses the bundled reference theme in the pinned upstream revision and does not have macOS's personal-image customization flow.

## Unsupported hosts

Do not attempt to run the renderer injection on Linux or unofficial Codex builds. You may inspect, stage, or explain the project there, but perform installation and live verification only on a supported host.
