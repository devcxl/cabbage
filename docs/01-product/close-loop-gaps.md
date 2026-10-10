---
origin_change: close-loop-gaps
change_type: feature
cabbage_stage: requirement
synced_at: '2026-10-10T06:36:08.943842+00:00'
---

# Goal

2026-10 的闭环覆盖分析确认"收尾与诚实性"上有三个缺口：

1. 全部阶段验证通过的变更没有任何归档提示，活动台账会无限膨胀（本仓库自身已有 16 条已完成变更未归档）；
2. 生成的 CI 模板在非 Python 项目中对测试阶段静默跳过，验证在 CI 层落空；
3. 代码评审与执行边界（需求池、监控、部署自动化）在 agent 契约与路由器中不可见。

本次变更补齐提示层与契约层，使"创建 → 实现 → 验证 → 合并 → 归档"的闭环完整可循。
门禁语义、`gate` 行为与 `--json` 既有字段不变。

# Scope

## In Scope

- `cabbage status`：全部阶段验证通过的变更标记 `ready_to_archive`（JSON 加字段），文本输出追加归档提示。
- CI 模板：测试跳过分支输出 `::warning::` 注解；文件头注释说明需按技术栈适配测试步骤。
- `integrations/agent-contract.md`：增加代码评审与合并后归档两条规则。
- `skills/cabbage/SKILL.md`：边界节声明四项外置职责（需求池与排期、监控与告警、部署自动化、代码评审执行）。
- README：补充 `operations` / `performance` 影响字段语义；`status` 条目说明归档提示。
- 测试固定以上行为；vendored CLI 与仓库 CI 副本同步。

## Out of Scope

- `ci.test_command` 配置化：等第二个真实非 Python 消费方出现再做。
- 内建代码评审流程、监控与部署自动化：维持边界外置，仅补声明。
- 归档强制：CLI 不检查 Git 合并状态，保持"确认合并后再归档"的人工确认。

# Acceptance Criteria

### Scenario 1: 可归档提示（T-1/T-2）

- GIVEN 一个全部阶段均验证通过的变更
- WHEN 执行 `cabbage status` 或 `cabbage status --json`
- THEN 文本出现 "ready to archive" 提示；JSON 行含 `ready_to_archive: true`；含 pending/stale 的变更不受影响

### Scenario 2: 测试跳过不再静默（T-3）

- GIVEN 使用生成模板且无 `tests/` 目录的项目
- WHEN CI 运行 Run Test Suite 步骤
- THEN 输出 `::warning::` 注解且退出码为 0（fresh 项目仍绿）

### Scenario 3: 契约与边界可查

- GIVEN 消费者项目或 agent 阅读文档
- WHEN 查看 agent-contract、router 边界、README 与 `status` 描述
- THEN 评审/归档责任与四项外置边界均有明确文字
