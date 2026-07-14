# 手绘风格系统

选择一个预设并在同一组图片中保持一致。用户给出明确媒介或色板时，以用户要求为准。

## `airy-editorial`（默认）

适合文章、报告、产品观点和知识内容。

- 线条：粗细略有变化的石墨或墨水线，轻微抖动，局部不闭合。
- 背景：白色或浅暖灰，干净无纹理。
- 颜色：黑灰线稿为主；低饱和青绿色用于主要强调，暖赭色只用于少量焦点。
- 留白：主体占画面约 50–70%，至少保留 25% 连续空白。
- 气质：成熟、机智、编辑插画感；避免幼儿卡通和商业矢量图感。

提示词片段：

```text
airy hand-drawn editorial illustration, lively imperfect graphite-and-ink lines,
slightly open contours, mostly monochrome scene with restrained muted teal accents
and at most two warm ochre highlights, clean white or warm-gray background,
generous negative space, concrete recognizable objects, visual hierarchy through
scale and line weight, mature and thoughtful, not childish
```

## `warm-notebook`

适合个人成长、生活方式、旅行、复盘和温暖叙事。

- 线条：铅笔、蜡笔和少量干笔触，保留手工摩擦感。
- 背景：淡奶油纸色，不出现强噪点或仿旧污渍。
- 颜色：炭灰、陶土红、橄榄绿和淡米黄，最多三种强调色。
- 留白：主体占 55–75%，边缘保留呼吸空间。
- 气质：亲切、诚实、有日记感；避免过度可爱和剪贴簿堆叠。

提示词片段：

```text
warm hand-drawn notebook illustration, loose pencil and dry crayon marks,
subtle tactile strokes on a clean cream-paper background, charcoal gray with
restrained terracotta and olive accents, intimate and reflective, uncluttered,
clear visual metaphor, no scrapbook collage
```

## `monochrome-ink`

适合严肃观点、技术概念、封面和需要高对比度的内容。

- 线条：黑色钢笔或马克笔，粗细对比明显，允许少量排线。
- 背景：纯白。
- 颜色：仅黑、白、灰；用户明确指定时才能加入单一强调色。
- 留白：主体占 45–70%，用黑白面积和线密度建立层级。
- 气质：直接、克制、略带报刊漫画感；避免厚重漫画分镜和恐怖氛围。

提示词片段：

```text
monochrome hand-drawn ink editorial illustration, expressive black pen lines,
strong variation in line weight, sparse cross-hatching, pure white background,
bold readable silhouette, generous negative space, restrained newspaper-op-ed mood,
no color unless explicitly requested
```

## 系列一致性锁

生成第二张及后续图片时，在提示词中追加：

```text
Maintain the exact same illustration system across the series: line medium,
line weight range, background tone, accent palette, character proportions,
label style, and whitespace density. Change the scene and composition only.
```

## 通用禁项

- 不要光滑矢量轮廓、3D 渲染、摄影写实、渐变、发光、复杂阴影。
- 不要彩虹色、满版铺色、密集信息卡片、便利贴墙或模板化信息图。
- 不要水印、Logo、签名、伪造引用或无意义装饰文字。
- 不要在画面中写“对比构图”“流程图”等结构名称。
