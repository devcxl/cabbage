---
change: close-loop-gaps
cabbage_stage: tests
change_type: feature
---

# Strategy

单元/契约层。CLI 行为用子进程集成测试（沿用 `test_cli_output.py` 的临时项目夹具），
CI 模板用 YAML 结构 + 字符串断言（沿用 `test_repository_contracts.py` 模式）。
公开测试缝：`cabbage status` 文本与 JSON 输出；模板 `Run Test Suite` 步骤的 run 脚本。

# Cases

| ID | Scenario | Level | Expected result | Priority |
|---|---|---|---|---|
| T-1 | 全部阶段验证通过后执行 status | 集成（子进程） | 输出含 "ready to archive" 提示；`--json` 行含 `ready_to_archive: true` | High |
| T-2 | 未完成变更执行 status | 集成（子进程） | 无提示、`ready_to_archive: false` | High |
| T-3 | 模板 Run Test Suite 跳过分支 | 契约（字符串） | 含 `::warning` 注解，且保留 `[ -d tests ]` 守卫 | High |
| T-4 | 既有测试全量回归 | 回归 | 全部通过（含 vendored 一致性与 CI 逐字节一致） | High |

# Entry and Exit Criteria

- Entry：前置阶段验证通过；`cabbage gate close-loop-gaps implementation` 输出 ALLOWED。
- Exit：T-1..T-4 通过；`validate --all`、`docs build`、`git diff --check` 通过；远端 CI 绿。

# Risks

- 本仓库 16 条已完成变更会让 status 每次输出提示——预期行为，作为收尾信号，不视为缺陷。
- JSON 消费方依赖严格 schema 的风险低：字段为加性；测试同时断言旧字段不变。
