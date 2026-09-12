---
change: research-and-router-skills
cabbage_stage: requirement
---
# Goal

补齐拆分后丢失的调研场景，并提供一个统一的入口 skill 引导多个 skill 的选择与组合使用。

# Scope

新增 `cabbage`（入口，只做选路与组合编排）与 `cabbage-research`（自包含的调研与选型流程）。
更新既有 skill 的同族引用与调研交接点。调研本身不建变更记录，结论需要落地时交给变更流程。
不新增变更类型，不修改 CLI 行为。

# Acceptance Criteria

- 入口 skill 能识别非 cabbage 项目并拒绝触发。
- 选路表覆盖全部同族 skill，且不指向不存在的 skill；契约测试可在遗漏时失败。
- 调研 skill 自包含，独立安装即可使用，不依赖 `technical-research` 或 `deep-research`。
- 调研 skill 明确"调研不建变更记录"以及结论的交接路径。
- 全部 skill 通过结构校验，全量测试与文档构建通过。
