---
name: codex-desktop-pet
description: Create, repair, validate, preview, and package animated desktop pets for the Codex app from a text concept, brand cue, or reference image. Use when a user asks for a Codex pet, desktop companion, animated pet spritesheet, pet.json package, 8x9 Codex animation atlas, or help fixing an existing Codex pet animation.
---

# Codex Desktop Pet

Create a Codex-compatible animated pet while separating creative image generation from deterministic atlas processing.

## Read the contract

Read these references before producing files:

- Read `references/codex-pet-contract.md` for package and atlas requirements.
- Read `references/animation-rows.md` for states, frame counts, and timing.
- Read `references/qa-rubric.md` before accepting or repairing output.

## Use the image generation skill

Load and follow the installed `$imagegen` skill before generating or editing any pet image. Use it as the only creative visual-generation layer. Do not synthesize missing animation rows with local drawing code.

Use the bundled Python scripts only for deterministic operations: prompt preparation, layout guides, chroma-key removal, frame extraction, safe mirroring, atlas composition, previews, validation, and packaging.

## Keep visible progress

Track these four steps and keep only one active at a time:

1. Define the pet.
2. Establish the canonical look.
3. Generate the animation rows.
4. Validate and package the pet.

## Workflow

### 1. Prepare the run

Choose or infer a short name, one-sentence description, stable identity notes, and style. If the request contains only a company or product name, research a few official sources and convert them into broad mascot-safe cues. Do not copy logos, readable marks, slogans, or UI.

Run:

```bash
python scripts/prepare_pet_run.py \
  --pet-name "<name>" \
  --description "<description>" \
  --pet-notes "<stable visual identity>" \
  --reference /absolute/path/to/reference.png \
  --style-preset auto \
  --output-dir /absolute/path/to/run
```

References are optional. Inspect `pet_request.json` and `imagegen-jobs.json` after preparation. A job is ready only when every job listed in `depends_on` is complete.

### 2. Generate the canonical base

Generate the `base` job from `prompts/base-pet.md` and every listed input image. Require one centered full-body character on the requested flat chroma background.

Copy the selected result to the job's `output_path`, copy it again to `references/canonical-base.png`, and only then mark `base` complete in `imagegen-jobs.json`.

Treat the canonical base as the identity source of truth for every row.

### 3. Generate one grounded strip per state

Generate `idle` and `running-right` first. Then generate the remaining ready jobs. For each row:

- Read its normal and retry prompt paths from the manifest.
- Attach every `input_images` entry, including the canonical base and layout guide.
- Produce exactly the requested number of separated full-body poses in one horizontal strip.
- Preserve face, silhouette, proportions, markings, palette, material, lighting, and props.
- Reject copied guide marks, scenery, text, shadows, glows, blur, dust, speed lines, detached effects, cropped poses, and overlapping slots.
- Copy the selected image to the declared `decoded/<state>.png` path before marking the job complete.

Use separate bounded generation workers only when the user has allowed delegation. Give each worker exactly one visual job and require it to return only the selected file path and a short QA note.

### 4. Handle the left-running row safely

Generate `running-left` normally when the pet has asymmetric markings, props, lighting, text, or direction-sensitive details.

Mirror an approved `running-right` strip only when flipping preserves identity and meaning:

```bash
python scripts/derive_running_left_from_running_right.py \
  --run-dir /absolute/path/to/run \
  --confirm-appropriate-mirror \
  --decision-note "<why framewise mirroring is safe>"
```

Never mirror the entire strip as one image; that reverses temporal order.

### 5. Finalize and package

After all nine decoded row strips exist, run the deterministic pipeline:

```bash
python scripts/finalize_pet.py \
  --run-dir /absolute/path/to/run
```

The command extracts frames, inspects them, composes PNG and lossless WebP atlases, validates the atlas, produces a contact sheet and GIF previews, and packages `pet.json` with `spritesheet.webp` under `${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/`.

If the generated strips are visually stable but extracted previews pop in size or baseline, rerun with:

```bash
python scripts/finalize_pet.py \
  --run-dir /absolute/path/to/run \
  --stable-slots
```

Use `--stable-slots` only after confirming the source strips themselves are stable and unclipped.

### 6. Perform visual QA

Inspect `qa/contact-sheet.png` and every GIF under `qa/previews/`. Deterministic validation is necessary but not sufficient.

Reject output when any row has identity drift, an incorrect state action, missing or inert motion, wrong direction, reversed cadence, size popping, a non-transparent background, artifacts, clipped poses, or detached components.

Repair the smallest failing scope. Prefer re-extraction for extraction-induced instability; regenerate only the affected row when its source imagery is wrong. Re-run finalization and visual QA after every repair.

## Acceptance

Accept only when:

- The atlas is `1536x1872`, transparent-capable PNG or WebP.
- Every used cell is non-empty and every unused cell is fully transparent.
- Fully transparent pixels contain no hidden RGB residue.
- `qa/review.json` and `final/validation.json` report no errors.
- All nine preview animations match the app states and preserve one pet identity.
- The package contains adjacent `pet.json` and `spritesheet.webp` files.
