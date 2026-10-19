---
change: close-loop-gaps
cabbage_stage: implementation
change_type: feature
---

# Tasks

## Task 1: status 可归档提示
- **Builds**: `cabbage status` 对全部验证通过的变更给出归档提示；JSON 暴露 `ready_to_archive`。
- **Blocked By**: None
- **Parallel Group**: G1
- **Verification**: `python -m unittest tests.test_cli_output`
- [x] 先写失败测试（T-1/T-2），确认 RED
- [x] 实现 `cmd_status` 聚合与提示，测试转 GREEN

## Task 2: CI 模板显式告警
- **Builds**: 模板测试跳过分支输出 `::warning::` 注解；仓库 CI 副本逐字节同步。
- **Blocked By**: None
- **Parallel Group**: G1
- **Verification**: `python -m unittest tests.test_repository_contracts`
- [x] 先写模板断言（T-3），确认 RED
- [x] 修改模板并同步 `.github/workflows/cabbage.yml`，测试转 GREEN

## Task 3: 契约与文档补齐
- **Builds**: agent-contract、router 边界、cabbage-change、cli.md、README 五处更新；
  vendored CLI 同步；全量回归与站点构建通过。
- **Blocked By**: None
- **Parallel Group**: G2
- **Verification**: `python -m unittest discover tests`
- [x] 更新五处契约/技能/README 文档
- [x] `python scripts/sync-vendor.py` 并跑全量测试、`validate --all`、`docs build`

# Verification

- 新增测试先 RED（`ready to archive` 缺失、`::warning` 缺失），实现后 GREEN。
- `python -m unittest discover tests`：73 项通过（71 旧 + 2 新）。
- `python -m cabbage_cli validate --all`：VALID。
- `pnpm --dir docs run build`：构建成功（9.79s）。
- `git diff --check`：无空白错误。
- 本仓库 `cabbage status`：出现 `16 change(s) fully verified and ready to archive` 提示，
  `--json` 输出含 `ready_to_archive` 字段（既有字段不变）。

未覆盖：GitHub Actions 注解的实际渲染效果需在远端 CI 上确认（本地无法渲染注解）。
