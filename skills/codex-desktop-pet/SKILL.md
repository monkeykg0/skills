---
name: codex-desktop-pet
description: Create, repair, validate, preview, and package animated desktop pets for the Codex app from a text concept, brand cue, uploaded photograph, or one or more character reference images. Use when a user asks for a Codex pet, desktop companion, photo-to-pet conversion, reference-image-driven mascot, animated pet spritesheet, pet.json package, 8x9 Codex animation atlas, or help fixing an existing Codex pet animation.
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

## Interpret uploaded images

Inspect every available upload before preparing the run. Identify and record:

- The primary identity reference.
- Supporting front, side, back, expression, color, clothing, or accessory references.
- Stable anchors that must survive simplification: silhouette, face, proportions, markings, palette, clothing, accessories, and material.
- Details that are too small, text-like, fragile, or unsafe at `192x208` and should be simplified.
- Any left/right asymmetry that makes automatic mirroring unsafe.

When attachments have local paths, pass each path with a separate `--reference` flag. Put the primary identity reference first:

```bash
python scripts/prepare_pet_run.py \
  --pet-name "<name>" \
  --description "<description>" \
  --pet-notes "<stable identity anchors and asymmetry notes>" \
  --reference /absolute/path/to/front.png \
  --reference /absolute/path/to/side.png \
  --reference /absolute/path/to/detail.png \
  --style-preset auto \
  --output-dir /absolute/path/to/run
```

When an uploaded image is visible in the conversation but has no local path, prepare the run without `--reference`, then include the smallest number of recent conversation images that covers every requested reference when generating the canonical base. Save the selected result at the manifest's base `output_path` and at `references/canonical-base.png`. Record the upload roles and identity anchors in `pet_request.json` or an adjacent run note so later rows remain grounded in the canonical base.

Never claim to have used an uploaded reference unless the image was actually attached to the base generation call. Do not require the user to upload it again when it is already accessible in the current conversation.

## Complete user prompt examples

Treat the following blocks as user-facing examples that can be copied and customized. Infer omitted low-risk details; ask only when a missing choice would materially change identity, licensing, or output.

### Example 1: Quick pet from a text concept

```text
Use $codex-desktop-pet to create a Codex desktop pet named Mochi.

Mochi is a round pale-blue cloud spirit with tiny black eyes, a simple smile,
short arms and feet, and no clothing or props. Use a soft 3D toy style. Keep the
silhouette compact and readable at small size. Complete all nine animation rows,
run visual QA, and package the finished pet for Codex.
```

### Example 2: Detailed text-only art direction

```text
使用 $codex-desktop-pet 创建一个名叫 Byte 的 Codex 桌面宠物。

角色设定：
- 小型深蓝色机械水獭，头大身小，完整全身
- 圆形青色眼睛，银灰色腹部面板，短尾巴
- 左耳有一个固定的黄色小夹子，这是身份锚点
- 不要文字、Logo、屏幕 UI、武器或新增道具
- 风格是简洁的搪胶玩具，不要写实金属材质
- 所有动画中保持脸型、眼睛、耳夹、配色和身体比例一致

动画要求：
- idle 必须安静，只允许呼吸、眨眼和轻微身体起伏
- running-right 和 running-left 必须方向明确、步态交替
- running 表达“正在处理任务”，不能画成字面跑步
- review 不要添加放大镜、文件或界面
- 左耳夹具有方向性，因此 running-left 必须独立生成，禁止镜像

请生成完整九行动画，检查 contact sheet 和全部 GIF，修复不合格的最小范围，
最后生成 pet.json 和 spritesheet.webp。
```

### Example 3: One uploaded character image

```text
使用 $codex-desktop-pet，根据我上传的角色图片创建 Codex 桌面宠物。

请先检查图片，再提取并记录必须保持的身份锚点：
- 头部和身体轮廓
- 脸部比例与表情
- 主色、辅色和固定花纹
- 服装与关键配件
- 左右不对称细节

把复杂细节简化到适合 192×208 单格显示，但不要擅自改变角色身份。
不要添加图片中不存在的文字、Logo、衣服、道具或特效。

请以上传图片为基础建立 canonical base，然后用它生成全部九种状态。
完成透明背景处理、atlas 验证、contact sheet、九个 GIF 预览和 Codex 宠物打包。

工作目录：
/absolute/path/to/outputs/my-reference-pet
```

### Example 4: Multiple uploaded character sheets

```text
Use $codex-desktop-pet to build a pet from my three uploaded images.

Reference roles:
1. The first image is the primary front-view identity reference.
2. The second image defines the side silhouette and tail shape.
3. The third image defines the exact colors, face details, and accessory shape.

Preserve the same head-to-body ratio, eye spacing, ear shape, tail, clothing,
palette, and accessory placement. When references disagree, prioritize image 1
for identity, image 2 for side geometry, and image 3 only for close-up details.
Simplify details that disappear at 192x208, but list every simplification before
generation. Do not merge alternate costumes or expressions into the base design.

Generate a canonical full-body base for approval, then generate all nine rows.
Independently generate left-facing movement if any accessory changes sides under
mirroring. Finish the full deterministic validation and package the result.
```

### Example 5: Turn a real pet photograph into a mascot

```text
使用 $codex-desktop-pet，把我上传的猫咪照片设计成 Codex 桌面宠物。

必须保留：
- 灰白毛色分布
- 左眼旁边的深灰色斑块
- 绿色眼睛
- 短尾巴和圆脸轮廓

转换要求：
- 转成简洁的毛绒玩具吉祥物，不直接裁切或照搬照片
- 保持四足动物身份，但允许为了动画清晰度适度拟人化动作
- 不添加项圈、衣服、文字或新花纹
- 毛发细节要简化，轮廓必须适合透明背景和小尺寸显示
- 深灰眼斑具有方向性，左右跑动分别生成，不允许直接镜像

先生成 canonical base 并让我确认；确认后再生成九种状态、执行视觉质检并打包。
```

### Example 6: Turn a portrait into a non-identical stylized companion

```text
Use $codex-desktop-pet to create a stylized desktop companion inspired by my
uploaded portrait.

Use broad, non-sensitive visual cues only: short curly dark hair, round glasses,
a teal hoodie, warm friendly expression, and compact chibi proportions. Do not
attempt photorealistic identity reconstruction, infer sensitive traits, reproduce
background details, or add readable text. Make it an original toy-like mascot
rather than a realistic miniature person.

Keep hair silhouette, glasses, hoodie color, and proportions stable across every
row. Generate a canonical base first, then all nine animations, visual previews,
validation files, and the final Codex package.
```

### Example 7: Brand-inspired pet without copying a logo

```text
使用 $codex-desktop-pet，为我的产品设计一个品牌启发的 Codex 桌面宠物。

我会上传品牌色板和产品视觉参考。请只提取经过授权的宽泛特征，例如主色、
辅助色、圆角几何语言、亲和与高效的气质。不要复制 Logo、商标轮廓、标语、
产品 UI 或可读品牌文字。

角色方向：一只原创的小型工具精灵，主体为深紫色，青绿色点缀，圆角轮廓，
没有屏幕、键盘或文字。请先记录哪些视觉线索被采用、哪些因商标风险被排除，
再建立 canonical base。完成九种状态、一致性检查、透明图集和宠物包。
```

### Example 8: Asymmetric character with strict no-mirroring rule

```text
Use $codex-desktop-pet with my uploaded character sheet.

This character is asymmetric:
- red patch over the character's anatomical left eye
- satchel strap runs from anatomical right shoulder to left hip
- one small horn exists only on the anatomical right side
- tail tip bends toward the character's anatomical left

Preserve anatomical left/right identity in every frame. Generate running-left
and running-right independently. Do not mirror either row, do not swap the eye
patch, horn, strap, or tail direction, and do not simplify away these anchors.
Use the front and back references together when generating the canonical base.
Complete all nine rows and explicitly inspect asymmetry in the contact sheet and
both directional GIFs before packaging.
```

### Example 9: Repair an existing generated pet

```text
使用 $codex-desktop-pet 修复我现有的 Codex 宠物运行目录：
/absolute/path/to/existing-pet-run

已知问题：
- idle 第 4 帧身体突然变大
- running-left 的方向正确，但时间顺序反了
- waiting 错误地添加了问号
- review 的眼睛和 canonical base 不一致

请先检查现有 decoded strips、frames、contact sheet、GIF、qa/review.json 和
final/validation.json，判断问题来自生成、帧提取还是图集组装。

只修复最小失败范围：
- 提取问题优先重新提取，不要重生整行
- 源条带错误时只重新生成对应状态
- 不要修改已经合格的状态

修复后重新运行 finalization 和完整视觉 QA，并覆盖更新最终宠物包。
```

### Example 10: Plan and inspect before generating

```text
Use $codex-desktop-pet to plan a pet from my uploaded image, but do not generate
images yet.

Inspect the reference and return:
1. Proposed pet name and one-sentence description.
2. Stable identity anchors.
3. Details that should be simplified for 192x208 cells.
4. Left/right asymmetry and whether mirroring is safe.
5. Recommended style preset and chroma-key color.
6. Risks for each of the nine animation states.
7. The exact prepare_pet_run.py command you would run.

Stop after the plan and wait for my approval.
```

### Example 11: Full local smoke test with explicit acceptance criteria

```text
使用 $codex-desktop-pet 创建一个用于端到端验证的简单宠物。

名称：Sprout
设定：圆形绿色植物精灵，两片完全对称的叶子，小黑眼睛，没有衣服、文字、
花纹或道具。使用简洁贴纸风格。工作目录使用：
/absolute/path/to/outputs/sprout-smoke-test

必须完成：
- canonical base
- 九个 decoded 状态条带
- 1536×1872 透明 spritesheet.png 和 spritesheet.webp
- qa/contact-sheet.png
- qa/previews/ 下九个 GIF
- qa/review.json 和 final/validation.json 无错误
- `${CODEX_HOME:-$HOME/.codex}/pets/sprout/` 下相邻的 pet.json 与 spritesheet.webp

最后汇报每项验收结果，并列出仍需人工目视确认的问题。
```

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

When the user asks for planning only, prepare and report the proposed inputs or command, but stop before running image generation.

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
