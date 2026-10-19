---
change: prune-stale-artifacts
cabbage_stage: requirement
---
# Goal

清理仓库中已失真且无消费者的内容：死导入、陈旧的测试报告、与当前流程矛盾的示例。

# Scope

删除 4 处死导入与 1 处函数内重复导入；删除已失真的 TEST_REPORT.md 与零引用且过期的
examples/；把仍有效的测试现状信息并入 docs/08-testing/；新增死导入检测防止回归。
不改 CLI 行为，不删空目录，不动有意设计（vendored 副本、旧工作流、冻结 fixture）。

# Acceptance Criteria

- 无未使用的导入，且由契约测试断言。
- 不再存在指引使用已失效阶段名或已被移除命令的文档。
- 删除的文件零引用、不在打包范围。
- 全量测试、validate、文档构建通过。
