---
change: collapse-change-workflows
cabbage_stage: implementation
change_type: feature
---

# Tasks

## Task 1: 工作流收敛（8→2）
- **Builds**: 新项目 `change` / `incident` 两类工作流；impact 组合承接原专项场景
- **Blocked By**: None
- **Parallel Group**: G1
- **Verification**: `python -m unittest tests.test_lightweight_workflows`
- [x] 删除 7 份 assets 工作流，新增 change.yaml，incident 第三阶段改名 tasks
- [x] scaffold：IMPACT_FIELDS 增加 design/rfc、new_change 默认收敛（legacy 默认保留）、标签表更新

## Task 2: 命令面与核心泛化
- **Builds**: gate 目标泛化（阶段 id/merge/archive）；未知类型提示；移除 --export-dag
- **Blocked By**: None
- **Parallel Group**: G1
- **Verification**: `python -m unittest tests.test_cabbage tests.test_tasks_dag`
- [x] core.py：gate 泛化 + workflow() 报错附带可用类型
- [x] cli.py：gate choices 移除、cmd_tasks 移除导出分支并收敛视图提示

## Task 3: 模板与测试
- **Builds**: impact.md/change-record.md 更新；受影响的测试全部对齐新模型
- **Blocked By**: Task 1, Task 2
- **Parallel Group**: G2
- **Verification**: `python -m unittest discover tests`
- [x] 更新模板注释与矩阵行
- [x] 更新 test_lightweight_workflows / test_cli_output / test_repository_contracts / test_tasks_dag / test_templates

## Task 4: 文档与技能同步
- **Builds**: README、docs 概览、agent 契约、skills 全家与 references
- **Blocked By**: Task 1, Task 2
- **Parallel Group**: G2
- **Verification**: `python -m cabbage_cli validate --all` + `pnpm --dir docs run build`
- [x] 更新 README（快速开始/风险表/能力边界）与 docs/00-overview
- [x] 更新 skills（change/decision/research/incident/adopt/router/references）与 agent-contract
- [x] sync-vendor + 全量测试 + docs build + CI 预检

# Verification

- `python -m unittest discover tests`：72 项通过（含新项目 change/incident 全链路、README 示例可执行、未知类型提示）。
- `python -m cabbage_cli validate --all`：VALID。
- `pnpm --dir docs run build`：构建成功。
- `git diff --check`：无空白错误。
- legacy 兼容：`support.init_legacy_project`（冻结 fixture）全部用例通过，旧类型默认影响保持不变；
  本仓库自身 legacy 工作流与既有变更记录未受影响（`validate --all` 覆盖）。
- 新项目实际演练（测试内真实执行）：`new change` → `gate tasks` → `verify tasks` → `ci` → `archive`，
  以及 `impact --set api=true` 后 `api` 阶段门禁顺序。

未覆盖：docs/03-architecture/system-design 下历史同步文档中的 `--export-dag` 表述属历史设计记录，本次不重写；
新模型以本变更的同步文档与 skills 为准。
