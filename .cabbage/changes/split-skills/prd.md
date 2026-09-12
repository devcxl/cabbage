---
change: split-skills
cabbage_stage: requirement
---
# Goal

把单个 `project-docs-management` skill 拆成按任务场景划分的多个 skill，让 agent 按需加载而不是一次读入全流程说明书。

# Scope

产出 `skills/` 目录下的五个 skill：`cabbage-change`、`cabbage-decision`、`cabbage-incident`、`cabbage-docs`、`cabbage-adopt`。
每个 skill 携带自己需要的 references，且单独安装后仍可独立工作。移除根目录 `SKILL.md` 与 `references/`。
不改变 CLI 行为，不迁移既有项目工作流。

# Acceptance Criteria

- 五个 skill 各自通过结构校验，frontmatter 含 `name` 与可触发语义的 `description`。
- 单个 skill 被独立安装时，其内部相对链接全部可解析，不依赖兄弟 skill 的相对路径。
- `cabbage-change` 单独安装即可覆盖 feature/bugfix/refactor 的完整流程。
- 测试自动校验 frontmatter、description 与相对链接，并拒绝根目录重新出现 `SKILL.md` 或 `references/`。
- 文档中出现的 `cabbage verify` 阶段 ID 均存在于当前随包工作流或仓库工作流中。
