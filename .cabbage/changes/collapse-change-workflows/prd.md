---
change: collapse-change-workflows
cabbage_stage: requirement
change_type: feature
---

# Goal

收敛新项目的变更模型与命令面，为阶段二（插件内置 cabbage 能力）铺路：

1. 新项目工作流从 8 类收敛为 2 类：`change`（单一记录 + 按需专项文档）与 `incident`；其中 `feature / bugfix / refactor` 三份模板逐字节相同、`migration / integration / architecture / hotfix` 均可由 impact 组合表达。
2. 概念与命令面统一：新项目 stage id 与产物名对齐（`tasks` / tasks.md）；`gate` 目标泛化为「阶段 id / merge / archive」；移除 `--export-dag`（派发职责归编排侧）。
3. 生成体验对齐 OpenSpec 范式：一份变更 = 一个目录（tasks.md + 按风险展开的专项文档）+ 验证门禁 + 归档同步；既有项目工作流保持不变。

# Scope

## In Scope

- `cabbage_cli/assets/workflows/`：删除 7 份工作流，新增 `change.yaml`；`incident.yaml` 的第三阶段改名为 `tasks`。
- 新增可选 impact 字段 `design`（tech-spec.md）与 `rfc`（rfc.md），承接原专项工作流的高风险产物。
- `gate` 目标泛化：任意阶段 id 作为目标（校验其前置阶段），保留 merge/archive 全量语义。
- `new` 与 `impact`：默认影响收敛为 `change`；未知类型报错附带可用类型提示。
- 移除 `cabbage tasks --export-dag` 及配套导出逻辑（保留 `tasks` 只读视图）。
- 同步更新：skills（cabbage / cabbage-change / cabbage-decision / cabbage-research / cabbage-incident / cabbage-adopt 及 references）、README、docs 概览、agent 契约、模板注释、测试。

## Out of Scope

- 分发路径退役（install.sh / AUR / deb）：在阶段二随插件内置一并评估。
- cabbage 技能与 flow 技能的合并、插件内置引擎：阶段二执行。
- 旧项目工作流迁移：不做，既有 `.cabbage/workflows/` 原样保留。

# Acceptance Criteria

### Scenario 1: 新项目单记录闭环

- GIVEN 新初始化项目（`cabbage init`）
- WHEN 执行 `cabbage new change fix-label` 并完成记录
- THEN 工作区只有 tasks.md + 元数据；`gate fix-label tasks` / `verify fix-label tasks` / `gate fix-label merge` 全链路可用

### Scenario 2: 高风险按需展开

- GIVEN 新项目中的 change
- WHEN `cabbage impact <id> --set design=true --set rfc=true --set api=true`
- THEN 生成 tech-spec.md / rfc.md / api-design.md 三个专项文档，逐项验证后才允许通过 `tasks` 前置门禁

### Scenario 3: 既有项目不受影响

- GIVEN 使用旧版工作流的项目（fixture 与真实仓库自身）
- WHEN 升级 CLI 后继续使用
- THEN 旧工作流、既有 `gate <id> implementation` 用法与已验证状态全部保持有效

### Scenario 4: 概念与命令面统一

- GIVEN 任一使用 `cabbage --help` 的使用者
- WHEN 查看 `new` / `gate` / `tasks`
- THEN 新项目类型只有 change/incident；gate 目标接受阶段 id 或 merge/archive；`--export-dag` 不再出现
