---
change: collapse-change-workflows
cabbage_stage: design
change_type: feature
---

# Context

当前新初始化项目带 8 类工作流；`feature / bugfix / refactor` 三份 YAML 逐字节相同（仅类型名不同），`architecture / migration / integration / hotfix` 的独特产物可由 impact 条件表达，唯 `incident` 结构独有。命令面 16 个，`--export-dag` 服务于已由编排侧接管的派发场景。约束：既有项目工作流与已验证状态不得受影响（兼容策略已文档化）；本变更自身走仓库既有 legacy 工作流。

# Design

## change.yaml（新默认）

```
record_covers: [product, testing]
stages:
  design   → tech-spec.md        when impact.design
  rfc      → rfc.md              when impact.rfc
  adr      → adr.md              when impact.architecture
  api      → api-design.md       when impact.api
  database → database-design.md  when impact.database
  security → security-review.md  when impact.security
  release  → release-plan.md     when impact.deployment
  tasks    → tasks.md            depends_on: [design, rfc, adr, api, database, security, release]
                                validator: checklist, required_headings: [Goal, Design, Tasks, Verification]
```

专项阶段与其产物名一一对应（概念统一）；顺序即门禁顺序。

## 其他设计点

- `incident.yaml`：第三阶段 `implementation` → `tasks`（同产物 tasks.md），其余不变。
- `scaffold.IMPACT_FIELDS` 增加 `design`、`rfc`（插在语义相邻位置）；`new_change` 默认：`change` → product+testing，`incident` → 均 false；legacy 类型（feature/architecture/migration/integration）的既有默认保持不变，旧项目行为与升级前完全一致。
- `gate` 泛化：目标为 merge/archive 时要求全量；目标为任一阶段 id 时要求其前置阶段；未知目标返回带说明的错误。旧用法 `gate <id> implementation` 在 legacy 工作流下语义不变。
- `core.workflow()` 未知类型报错附带可用类型列表（从 workflows 目录扫描）。
- 移除 `tasks --export-dag` 分支与 argparse 标志；保留 `tasks` 只读视图与结构化解析（仍用于视图展示）。
- 同步更新：`sync_impact_document` 标签表、impact.md 模板行、change-record.md 注释。

# Failure Modes

| Failure mode | Detection | Handling | Recovery |
|---|---|---|---|
| 旧用类型名在新项目执行 | `new` 报错信息 | 提示可用类型 change/incident | 用户改用新类型 |
| gate 目标拼写错误 | gate 返回错误列表 | 错误信息说明可选形态（阶段 id / merge / archive） | 修正目标名 |
| 存量项目 impact.md 与新字段表不一致 | 模板测试 | 存量项目不迁移；仅新配置启用新字段 | 无需处理 |

# Rollout

随 CLI 版本发布；新初始化项目生效，既有项目不变。回滚 = revert 该变更（工作流资产随版本恢复）。
