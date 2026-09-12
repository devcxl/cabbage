---
change: split-skills
cabbage_stage: adr
---
# Context

原方案把全部场景、SOP、参考文档集中在一个 skill 中。随着流程收缩为"轻量单记录 + 高风险专项"，
集中式说明书的剩余价值只在少数专项场景，却仍对每次任务全量占context。

# Decision

按任务场景拆分说明书，而不是按流程阶段拆分；并让每个 skill 自包含其最小闭环。
流程知识集中在 `cabbage-change`，内容标准分给 `cabbage-decision`、`cabbage-incident`、
`cabbage-docs`、`cabbage-adopt`。

否决的备选方案：按流程阶段（初始化/影响/编写/验证/实现/归档）拆分会让单次任务加载多个 skill
并重复状态机知识；继续维持单 skill 只做精简无法解决"按任务定位"的问题。

# Consequences

优点是 agent 按任务加载，context 占用显著下降，且每个 skill 的触发条件清晰。
代价是存在五个 description 常驻上下文（约 1700 字符），且 `cabbage-change` 与
`cabbage-decision`/`cabbage-docs` 存在边缘重叠，需要以"流程 vs 内容"分工约束。
跨 skill 引用不再使用相对路径，改为按 skill 名引用，牺牲了一点可点击性换取独立安装后的可用性。
