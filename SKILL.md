---
name: project-docs-management
description: Manage Cabbage change records, document validation, workflow gates, and documentation sites in repositories using .cabbage.
---

# Cabbage 文档与变更管理

## 先确认项目实际工作流

读取项目 `.cabbage/config.yaml`、`.cabbage/workflows/<type>.yaml` 和相关当前文档。
工作流文件是阶段名称和依赖的依据，不用文档文件名代替阶段 ID。

```bash
cabbage status
cabbage next <change-id>
```

新初始化项目的 `feature / bugfix / refactor` 默认只有 `implementation` 阶段的一份
`tasks.md`，包含 Goal、Design、Tasks、Verification。先写目标与方案，实现后填实际验证结果，
再验证 `implementation`；不额外生成 PRD、测试计划、DAG 或重复 SOP。

实现前声明高风险影响：`architecture / api / database / security / deployment` 分别增加
`adr / api / database / security / release` 专项阶段及实现前门禁。普通发布不必标记 deployment，
需要专项部署/回滚方案时才启用。风险不会由 CLI 自动识别，不能为少写文档而隐瞒实际影响。

既有项目的工作流不会自动迁移。旧流程中 `requirement` 对应 `prd.md`，`design` 对应
`tech-spec.md`，`tests` 对应 `test-plan.md`，`implementation` 对应 `tasks.md`。
以当前项目 `status` / `next` 输出为准，不将旧阶段名套用到新轻量流程。

## 基本操作

```bash
cabbage init
cabbage new feature <change-id>
cabbage impact <change-id>
cabbage next <change-id>
```

已有项目不要重复初始化；尤其不要使用 `init --force` 更新 CLI，它会覆盖项目配置和工作流。
存量文档可先用 `cabbage adopt` 盘点，确认迁移清单后再 `adopt --apply`。

1. 确认目标、范围和风险；只向用户确认无法从代码判断的重要决策。
2. 通过 `impact --set` 声明相关影响，根据 `next` 顺序填写和验证已启用阶段。
3. 开始实现前运行 `gate implementation`，有阻塞时先处理缺失或失效的前置材料。
4. 完成任务并记录实际测试命令及结果，再验证 `implementation`；不要提前勾选任务。
5. 验证剩余阶段，检查合并门禁。新轻量流程的产品目标和测试证据留在记录中，不为这两项
   另建当前文档；高风险专项文档仍按 CI 规则发布，已有失真的当前文档仍需修正。

```bash
cabbage gate <change-id> implementation
# 实现与测试完成后：
cabbage verify <change-id> implementation
cabbage validate <change-id>
cabbage gate <change-id> merge
cabbage ci --base origin/main
cabbage docs build
# 确认合并后再归档；CLI 不检查 Git 合并状态。
cabbage archive <change-id>
```

基础引用中的分支名需换成项目实际基线，如 `origin/master`。
`sync` 会复制已启用且有映射的文档，不自行检查验证状态，也不做语义合并；需要发布时先通过
`gate merge` 再执行 `sync`。`archive` 会先检查门禁再自动同步。

## 不同类型

- `feature`：新增或调整功能。
- `bugfix`：先复现、确认失败，再最小修复和回归。
- `refactor`：保持行为，先确认测试保护。
- `architecture`、`migration`、`integration`：使用项目定义的专项工作流。
- `hotfix`、`incident`：记录处置、验证和适用的回滚或复盘材料。
- 纯文档更新：直接修改归属文档并验证链接与构建；遵循项目 CI 约束。

DAG、并行子代理和多方案比较按任务需要使用，不是所有变更的前置义务。
`cabbage tasks <change-id> --export-dag` 只导出派发数据，不执行任务。

## 约束与排错

- `verify` 检查结构、链接、占位符及清单，记录内容指纹；不证明代码正确或审批身份。
- `pending`：未验证；`stale`：内容或依赖变化后需重新审阅并验证；`skipped`：当前影响未启用。
- 不手工编辑 `state.json`，不为了通过门禁而伪造验证结果。
- 当前事实按功能维护；历史决策通过后续记录取代，不静默改写历史。
- 会话交接只记录恢复所需信息，不重复整个文档树。

## 按需参考

- [命令与退出码](references/cli.md)
- [变更类型和风险](references/decision-tree.md)
- [状态、门禁和归档](references/lifecycle.md)
- [文档类型](references/document-types.md)
- [验证规则](references/validation.md)
- [文档迁移](references/adoption.md)
- [目录布局](references/directory-structure.md)
- [站点构建](references/documentation-site.md)
- [权限和 CI](references/enforcement.md)
- [命名](references/naming-conventions.md)、[链接](references/linking-rules.md)、[维护归属](references/ownership.md)、[图表](references/diagrams.md)
