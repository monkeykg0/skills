# Security boundaries

## Preserve the official application

- Keep the official Codex app bundle, `app.asar`, `WindowsApps`, package identity, signature, and executable unchanged.
- Use only the complete upstream platform package. Do not transplant standalone CSS or injection payloads from screenshots, forks, or chat messages.
- Keep theme state separate from Codex authentication, tasks, pets, plugins, and provider configuration.

## Treat CDP as privileged local access

- Bind Chromium DevTools Protocol only to `127.0.0.1`.
- Accept a listener only when the upstream checks prove it belongs to the launched official Codex process or a legitimate child.
- Require expected `app://` renderer markers and a same-port loopback WebSocket target.
- Warn that loopback CDP has no same-user authentication. Recommend restoring the official appearance when theming is no longer needed and avoiding untrusted local programs while it is active.

## Control process changes

- Ask before restarting an already-running Codex instance.
- Do not kill a saved PID unless executable, ownership, command line, and start time all match the recorded process.
- Do not reuse an occupied explicit port. Let the upstream launcher choose a free port when supported.

## Protect configuration

- Preserve `config.toml` as strict UTF-8 and change only documented appearance keys.
- Refuse ambiguous TOML structures or concurrent file changes instead of attempting a best-effort rewrite.
- Never add, remove, print, or rewrite API keys, auth files, base URLs, or model-provider settings as part of theming.

## Pin and inspect upstream code

The bundled preparation script defaults to commit `2f038b5322702cfb248d9c7564b56470a389abc2`, inspected on 2026-07-16. This revision restores the bundled macOS theme asset and fixes configuration round-trip behavior. A different revision may change commands or security behavior. When the user requests latest upstream:

1. Resolve and report the new commit.
2. Inspect its README, platform `SKILL.md`, entry scripts, tests, and relevant diff from the pinned revision.
3. Reconfirm signature checks, loopback binding, process identity, target validation, configuration preservation, and restore behavior before executing it.
