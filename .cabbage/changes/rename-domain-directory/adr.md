---
change: rename-domain-directory
cabbage_stage: adr
---
# Context

目录 `04-data` 的名称只体现"数据"，但它实际承载数据模型、数据库设计与迁移回滚。
扩展名 `-domain` 更贴合其内容范围，且与 `ADOPTION_CATEGORY_RULES` 中
`database`/`schema`/`migration` 等关键词所归类的领域概念一致。

# Decision

把默认目录名改为 `04-domain`，并同步代码默认值、CI 规则、skills 指南与站点配置。

权衡过的替代方案：保留 `04-data` 只改文档描述（不动代码，但名称仍偏窄）；
同时保留两个目录名做兼容（引入分支逻辑，且需长期维护两套映射，用户明确否决）；
改影响字段名 `data` -> `domain`（影响面更大且字段已稳定，本次不做）。

# Consequences

命名更准确，且目录指南补充了用途、sync 目标与门禁规则三类信息。

代价是破坏性变更：不提供向后兼容。磁盘上 3 个存量项目的 config 仍指向 `docs/04-data/`，
改名后其 `sync` 新路径与 CI 检查路径不一致，必须手动迁移配置与目录。
空目录不被 git 跟踪，版本库中不产生 diff，改名只在磁盘与代码默认值上生效。

遗留一处既有重复未被处理：`database` 与 `data` 两个影响字段指向完全相同的目录，
本次只改名不改字段，该重复仍存在。
