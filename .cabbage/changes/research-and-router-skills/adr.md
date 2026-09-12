---
change: research-and-router-skills
cabbage_stage: adr
---
# Context

拆分后的五个 skill 各自自包含，但没有统一入口，多步任务缺少组合指引；
且原单 skill 中的 Technical Research 场景在拆分时丢失，调研与选型无落点。

# Decision

新增入口 skill `cabbage` 与调研 skill `cabbage-research`。
入口只做选路与组合编排，不承载流程；调研 skill 自包含核心证据纪律，
不依赖已有的 `technical-research` / `deep-research`。

否决的方案：让入口同时承载常用流程（会退化为新的全流程说明书，重新引入上下文成本）；
把调研并入 `cabbage-decision`（调研阶段尚未定案，与决策记录的性质不同）；
依赖外部调研 skill（无法保证已安装，削弱独立可用性）。

# Consequences

正面：单次任务仍只加载一个目标 skill；多步任务有明确的顺序与交接点；调研场景恢复。
代价：存在七个 description 常驻上下文；调研方法与既有 `technical-research` 存在内容重叠，
需要人工保持两者不矛盾；入口本身成为必须维护的路由表，遗漏可由契约测试发现。
