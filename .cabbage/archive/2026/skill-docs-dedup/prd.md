---
change: skill-docs-dedup
cabbage_stage: requirement
---
# Goal

补齐发布方案的编写指引，并消除说明书内部的重复与不一致。

# Scope

新增 release-plan 编写指引；收敛退出码与常见命令到单一事实源；
统一 CODEOWNERS 治理路径；新增契约测试防止重复回归。
不新增 skill，不改动 CLI 行为与 skill 结构。

# Acceptance Criteria

- `deployment=true` 有可遵循的编写指引：顺序、成功信号、可测回滚触发条件、数据处置。
- 退出码说明只在一处维护，其他位置链接引用。
- 治理路径 CODEOWNERS 只在一处维护。
- 三项内容均有契约测试覆盖，且测试可通过负向验证失败。
