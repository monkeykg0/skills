# 提示词配方

每张图独立组装提示词，使用明确描述，不使用只有作者自己理解的变量名。

## 组装顺序

```text
1. 任务和读者收获
2. 具体主体与物件分工
3. 构图和故事动线
4. 选定的手绘风格片段
5. 人物或参考图一致性
6. 文字、比例和留白
7. 负向约束
```

## 基础模板

```text
Create one original hand-drawn editorial illustration.

Reader takeaway: {TAKEAWAY}.

Draw these specific, recognizable objects: {OBJECTS}.
Information roles: {ROLES}.
Scene and metaphor: {SCENE}.
Composition: {COMPOSITION}.
Reading flow: {FLOW}; every arrow or path must have a clear start and destination.

{STYLE_PRESET}
{SERIES_LOCK}
{CHARACTER_LOCK}

Text: {TEXT_RULE}.
Framing: aspect ratio {RATIO}, {ORIENTATION}; main subject occupies roughly
50-70% of the frame with at least 25% clean negative space.

Avoid: smooth vector art, polished corporate infographic, formal flowchart,
3D render, photorealism, gradient, glow, heavy shadow, dense colored panels,
decorative sticky notes, generic symbols unrelated to the source, watermark,
logo, signature, gibberish text, cropped main subject, or duplicated objects.
```

## 人物规则

### 无固定人物

当物件足以表达内容时使用：

```text
No mascot or recurring character. Let concrete objects and their relationships
carry the message. Do not add a person merely as decoration.
```

### 通用人物

内容需要动作或情绪时使用：

```text
Use a simple original generic adult figure with neutral, non-branded clothing.
Keep facial detail minimal; communicate through pose and interaction with objects.
Do not resemble a known character, celebrity, or proprietary mascot.
```

### 用户参考角色

附上用户提供的所有参考图，并填写：

```text
Match the user-provided character reference for these identity anchors only:
{IDENTITY_ANCHORS}. Preserve silhouette, proportions, clothing, palette, and
distinctive accessories across the series. Adapt only the line medium to the
selected hand-drawn preset. Do not copy the reference background or composition.
```

## 文字规则

- 无文字：`no text, no letters, no numbers, no watermark`。
- 仅短标签：列出精确文字并写明 `0-4 short handwritten Chinese labels, black or dark-gray text, no label background boxes`。
- 有标题：列出精确标题，并要求顶部预留空间。标题和标签不得让画面变成教程页。
- 精确文字是硬需求时，优先生成无字底图，再用可靠的排版工具后期添加；不要反复依赖生图模型纠正长文本。

## 比例描述

| 比例 | 描述 |
| --- | --- |
| `16:9` | `wide horizontal editorial composition, not portrait or square` |
| `3:4` | `vertical social-media composition, not landscape` |
| `1:1` | `balanced square composition` |
| `9:16` | `tall mobile-story composition with safe space near top and bottom` |

## 定向修复句

- 留白不足：`Reduce secondary objects and restore one continuous clean empty area covering at least 25% of the frame.`
- 太像 PPT：`Replace boxes and equal-weight panels with one concrete scene and a natural visual path.`
- 物件太泛：`Replace generic icons with these named source objects: {OBJECTS}.`
- 系列漂移：`Match the approved reference image's line medium, palette, background tone, and character proportions exactly; change scene content only.`
- 文字乱码：`Remove all generated text and preserve blank space for later typography.`
- 箭头错误：`Draw the path explicitly from {START} to {END}; remove all other arrows.`
