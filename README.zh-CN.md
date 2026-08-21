# Codex 技能合集

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个持续扩充、面向生产环境的 Codex 技能合集。每个技能都独立存放在 `skills/` 目录下，包含简洁的智能体指令；对于注重可靠性的任务，还提供确定性脚本和参考资料。

## 已包含的技能

| 技能 | 用途 |
| --- | --- |
| `baoyu-article-illustrator` | 分析文章结构并生成风格统一的辅助配图。 |
| `baoyu-cover-image` | 从类型、配色、渲染、文字和情绪等维度生成文章封面。 |
| `baoyu-post-to-wechat` | 通过 API 或 Chrome 将文章或图文内容发布到微信公众号。 |
| `codex-desktop-pet` | 为 Codex 桌面应用创建、修复、验证、预览和打包动画宠物。 |
| `codex-dream-skin` | 安装、定制、验证、修复并安全恢复可逆的 Codex 桌面主题。 |
| `hand-drawn-illustration` | 将文章和想法转化为原创、统一的手绘编辑插画。 |
| `ip-as-logo` | 使用圆润、扁平优先的几何造型生成高度简化的拟人 IP 吉祥物 Logo。 |
| `kid-papercraft` | 为儿童生成个性化三段式折纸定格动画生日祝福提示词。 |

## 安装技能

将技能目录复制或创建符号链接到 `${CODEX_HOME:-$HOME/.codex}/skills/`：

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

重启或重新加载 Codex，以刷新技能目录。你可以使用 `$<skill-name>` 显式调用任意技能，也可以直接描述匹配的任务。

微信公众号发布 skill 不包含可重建的 `node_modules` 和任何凭据。需要使用时，请先安装锁定的 JavaScript 依赖：

```bash
(cd "${CODEX_HOME:-$HOME/.codex}/skills/baoyu-post-to-wechat/scripts" && bun install --frozen-lockfile)
```

如果尚未安装 `bun`，可以将命令中的 `bun` 替换为 `npx -y bun`。微信公众号凭据应保存在用户级或项目级 `.baoyu-skills/.env` 中，切勿提交该文件。

## 验证仓库

首先安装 Python 校验依赖：

```bash
python3 -m pip install -r requirements.txt
```

然后运行：

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

桌面宠物集成测试会生成模拟动画条带，运行完整的确定性处理流程，验证图集，并检查打包后的文件。

## 添加新技能

请将每个新技能创建在 `skills/<skill-name>/` 下。保持 `SKILL.md` 专注于执行步骤，将详细的领域资料放在 `references/` 中，并将需要重复执行或容易出错的转换逻辑放在 `scripts/` 中。

本仓库包含以 Apache-2.0 和 MIT 许可证发布的第三方 skill 材料。详情请参阅 `NOTICE` 和各技能目录中的许可证。
