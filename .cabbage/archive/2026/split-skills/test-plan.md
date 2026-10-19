---
change: split-skills
cabbage_stage: tests
---
# Strategy

用结构契约测试替代人工检查：五个 skill 必须能独立安装并通过校验，文档中的命令必须指向真实阶段。
同时保证 CLI 行为未变，全量既有测试继续通过。

# Cases

- 五个 skill 均通过 `skill-creator` 的结构校验，frontmatter 含 `name` 与足够具体的 `description`。
- 每个 skill 内部 Markdown 的相对链接在独立安装后仍可解析（忽略代码块与行内代码中的示例）。
- 仅复制 `cabbage-change` 到独立目录时，其 SKILL.md 的四个 references 引用全部存在。
- 根目录不再存在 `SKILL.md` 与 `references/`，防止旧入口回归。
- `README.md` 与全部 skill 文档中出现的 `cabbage verify <stage>` 阶段 ID 存在于随包或仓库工作流。
- 全量单元测试与 VitePress 构建通过。

# Evidence

`python -m unittest discover tests` 通过 43 项（新增 skill 结构与链接契约检查）。
五个 skill 分别通过 `skill-creator/scripts/quick_validate.py` 结构校验。
把 `cabbage-change` 单独复制到临时目录后，其 SKILL.md 引用的四个 references 全部存在。
新增检查在修复前复现了失败：示例链接误报（代码块与行内代码未剥离）以及
`lifecycle.md` 中断言旧阶段名的描述与新轻量流程矛盾。
