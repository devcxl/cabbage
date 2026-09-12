---
change: task-dag-honesty
cabbage_stage: requirement
---
# Goal

让任务派发工具对普通清单保持诚实：没有声明依赖时不要伪造派发计划。

# Scope

修复 `cabbage tasks --export-dag` 与文本输出在无结构化 DAG 时的误导行为。
在变更说明中补充任务分解与 DAG 的使用指引。清理一个全空的孤儿变更。
不新增 skill，不引入新的变更类型。

# Acceptance Criteria

- 普通 `# Tasks` 清单不再产生派发计划与假 `verification`。
- `--export-dag` 在无结构化分节时报错并说明原因，退出码非零。
- 文本输出不再显示 "No tasks currently ready" 这类误导信息。
- 结构化任务分节行为不变，`--json` 输出新增 `structured` 标志。
- 回归测试可在还原守卫时失败。
