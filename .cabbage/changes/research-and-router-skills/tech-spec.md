---
change: research-and-router-skills
cabbage_stage: design
---
# Context

上一次拆分把说明书按任务场景拆为五个 skill，但丢失了原单 skill 中的 "Technical Research" 场景，
`skills/` 中无任何调研相关内容。同时缺少统一入口，多 skill 场景只能靠各文件末尾一句话提示。

# Design

新增两个 skill，不新增变更类型，不改动 CLI：

- `cabbage`：入口。职责写死为三项——识别是否 cabbage 项目、按任务选路、给出多 skill 的组合顺序与交接点。
  不描述任何具体流程，避免长成新的全流程说明书。
- `cabbage-research`：自包含的调研流程。包含何时启用与不启用、证据分级、强制纪律、
  调研步骤、产出格式与交接。按用户选择内置核心方法，不依赖外部调研 skill 是否安装。

调研不建变更记录：调研阶段尚未定案，产物是报告；只有结论需要落地代码时才由 `cabbage-change`
创建变更。入口的选路表必须覆盖全部同族 skill，否则新增 skill 将无法被触达。

# Failure Modes

- 入口膨胀：以"只做选路与编排"约束，并在边界章节明示不得把新流程写入本文件。
- 路由遗漏：契约测试解析选路表，要求与磁盘上的 skill 目录集合完全一致，并做负向验证。
- 调研与决策职责混淆：调研产出报告，ADR 由 `cabbage-decision` 负责，交接规则写在两个 skill 中。
- 与既有外部调研 skill 重复：接受该重叠，换取独立安装可用；不复制其模板文件。

# Rollout

仅新增与更新 `skills/` 下的说明文件，并同步更新 README 与 docs 当前事实描述。
用户需重新安装或新增安装这两个 skill；旧单文件 skill 的卸载提示写入入口 skill。
