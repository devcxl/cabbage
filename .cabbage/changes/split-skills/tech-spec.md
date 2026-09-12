---
change: split-skills
cabbage_stage: design
---
# Context

原单 skill 有 377 行，包含 10 类场景分派矩阵与 6 个 SOP。agent 每次只能整体加载，
难以按任务定位，且指南与实际工作流脱节（阶段 ID 与产物文件名混用）。

# Design

按任务场景而非流程阶段拆分。理由是 skill 触发依赖 description 语义匹配，
按阶段拆会让同一任务连续加载多个 skill，并各自重复状态机知识。

- `cabbage-change`：唯一流程主入口，含 feature/bugfix/refactor、影响标记、门禁、验证、归档。
- `cabbage-decision`：ADR/RFC 的内容标准，不重复流程。
- `cabbage-incident`：事故时间线、复盘、预防措施落地。
- `cabbage-docs`：当前状态文档的目录归属、命名、链接、图表与站点构建。
- `cabbage-adopt`：存量文档盘点迁移与强制执行配置。

关键约束是 skill 之间不能互相 require。因此每个 SKILL.md 自包含该类任务的最小闭环，
references 只作为可选深读。同一份参考文档只归属一个 skill，其他 skill 以名称引用，不复制正文。

阶段真相保持在项目内（`.cabbage/workflows/*.yaml` 与 `cabbage next`），skill 不复制工作流定义，
从根上避免指南再次漂移。

# Failure Modes

- 单个 skill 缺少关键步骤：以独立安装模拟验证链接与自包含性。
- description 无法区分触发：明确"流程 vs 内容"分工，并在改动时更新。
- references 重复导致再次漂移：同一文档只保留一份，由测试保证相对链接可解析。
- 删除根 `SKILL.md` 影响既有引用：README 指向新入口，测试阻止旧入口回归。

# Rollout

仓库内一次性替换说明书布局，不涉及项目脚手架与运行时代码路径。
`cli.py` 与 `scaffold.py` 中指向已删除 `references/` 的提示改为指向 skill 名称。
用户通过既有方式（如 npx skills add）分别安装所需 skill。
