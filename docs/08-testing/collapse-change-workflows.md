---
origin_change: collapse-change-workflows
change_type: feature
cabbage_stage: tests
synced_at: '2026-10-10T09:09:38.926394+00:00'
---

# Strategy

单元与端到端脚本测试并行：核心流程用 `test_lightweight_workflows` 的临时项目夹具（真实 init + new + gate + verify + ci），CLI 输出用子进程夹具，README 示例由既有可执行测试守护；legacy 兼容由冻结 fixture 继续覆盖。

# Cases

| ID | Scenario | Level | Expected result | Priority |
|---|---|---|---|---|
| T-1 | 新项目 `new change` 单记录闭环（gate tasks / verify tasks / merge） | 集成 | 全部通过，产物仅 tasks.md | High |
| T-2 | 逐个 impact（design/rfc/architecture/api/database/security/deployment）展开专项文档并验证 | 集成 | 每个风险只增加对应文档；验证后前置门禁放开 | High |
| T-3 | `new incident` 三阶段与默认影响 | 集成 | incident/postmortem/tasks 可验证，testing=false | High |
| T-4 | legacy 项目（fixture）行为不变 | 集成 | 既有测试全绿（requirement/design/tests/implementation 流程） | High |
| T-5 | README 命令示例可执行 | 端到端 | 测试内实际执行全部示例并返回 0 | High |
| T-6 | gate 目标泛化 | 单元 | 阶段 id 目标校验前置、merge/archive 全量、未知目标报错 | High |
| T-7 | 未知类型报错提示 | 单元 | 报错包含可用类型清单 | Medium |

# Entry and Exit Criteria

- Entry：前置阶段验证通过；`cabbage gate collapse-change-workflows implementation` 输出 ALLOWED。
- Exit：全部测试通过；`validate --all`、`docs build`、vendored 一致性通过；远端 CI 绿。

# Risks

- README 示例测试真实执行命令序列，任何示例改动都需保持顺序自洽。
- 旧类型相关测试如误改为新类型会丢兼容覆盖；保留 fixture 路径不动即可规避。
