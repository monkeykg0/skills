# Codex 技能合集

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个持续扩充、面向生产环境的 Codex 技能合集。每个技能都独立存放在 `skills/` 目录下，包含简洁的智能体指令；对于注重可靠性的任务，还提供确定性脚本和参考资料。

## 已包含的技能

| 技能 | 用途 |
| --- | --- |
| `codex-desktop-pet` | 为 Codex 桌面应用创建、修复、验证、预览和打包动画宠物。 |
| `hand-drawn-illustration` | 将文章和想法转化为原创、统一的手绘编辑插画。 |

## 安装技能

将技能目录复制或创建符号链接到 `${CODEX_HOME:-$HOME/.codex}/skills/`：

```bash
cp -R skills/codex-desktop-pet "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/hand-drawn-illustration "${CODEX_HOME:-$HOME/.codex}/skills/"
```

重启或重新加载 Codex，以刷新技能目录。你可以使用 `$codex-desktop-pet` 或 `$hand-drawn-illustration` 显式调用技能，也可以直接描述匹配的任务。

## 验证仓库

首先安装唯一的运行时依赖：

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

本仓库包含基于 OpenAI 以 Apache-2.0 许可证发布的 `hatch-pet` 技能所衍生的文件。详情请参阅 `NOTICE` 和各技能目录中的许可证。
