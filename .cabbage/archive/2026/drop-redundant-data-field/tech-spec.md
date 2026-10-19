---
change: drop-redundant-data-field
cabbage_stage: design
---
# Context

`database` 与 `data` 的 CI 规则指向同一目录，功能重复。但两者并不对称：
`database` 同时是阶段 ID（工作流 `when: impact.database` 激活 database-design.md 阶段），
`data` 从未被任何工作流引用。因此 `data=true` 只要求改文档目录却不触发任何文档阶段，
容易让人误以为已声明数据影响。

# Design

分四处移除 `data` 影响字段：IMPACT_FIELDS、默认 CI 规则、impact.md 模板的 Data 行、
sync_impact_document 的标签表；本仓库 config 同步去除字段与规则。

**关键区分**：adopt 子系统中的同名 `data` 是分类类别名
（`ADOPTION_CATEGORY_RULES` 中 database/schema/migration 等关键词的归类），
`ADOPTION_TARGET_BY_CATEGORY` 需保留 `"data":"docs/04-domain"` 映射。二者同名但用途无关。

顺带修复一处测试漂移：`test_impact_template_preserves_sync_rows` 硬编码了 10 个区域名，
与 IMPACT_FIELDS 脱节，改为从 IMPACT_FIELDS 派生标签表，并断言模板不含已删除的 Data 行。

# Failure Modes

- 误删 adopt 分类键导致 KeyError：已实测复现并修复，新增测试断言每个分类键都有目标。
- 测试硬编码再次漂移：改为从代码常量派生，字段增删时自动跟随。
- 历史记录失效：实测确认 validate 的 missing 判定只检查缺失，多余键被忽略。

# Rollout

不改 CLI 命令结构。存量项目若曾用 `data=true`，需改用 `database=true`；
其已有变更记录不受影响。历史记录中的 `data` 键无需清理。
