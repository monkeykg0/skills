# Live QA checklist

Verify both the home route and a normal task after every install, update, repair, or reapply.

## Functional checks

- Native sidebar navigation remains clickable and keyboard focus remains usable.
- Native suggestion cards, project selector, task content, menus, composer, attachments, and send controls remain real interactive controls.
- Decorative layers do not intercept pointer events or cover focus targets.
- Navigation, reload, window resize, and route changes do not duplicate injected elements or lose the theme unexpectedly.
- No horizontal overflow, clipped composer, blocked scrolling, or unusable contrast appears at the current window size.

## Visual checks

- The home banner/background is visible and intentionally cropped.
- The image is decorative, not a fake full-window screenshot of Codex controls.
- Home titles remain readable; the image's left side is sufficiently quiet.
- The task view has lower visual noise than the home hero and keeps code, diffs, and prose readable.
- No watermark, broken image, accidental personal information, or unlicensed redistributable asset appears.

## Runtime and restore checks

- The verify command reports the expected injection marker and renderer target.
- The CDP listener is loopback-only and belongs to the expected Codex process tree.
- Logs and state point to the current process/session rather than stale state.
- Restore removes the live decorative injection, stops the matching injector/debug session, and opens Codex normally without altering unrelated configuration.

Record command evidence separately from visual evidence. If screenshots or browser inspection are unavailable, say that visual QA remains pending rather than declaring a full pass.
