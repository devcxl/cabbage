---
change: rename-domain-directory
cabbage_stage: design
---
# Context

`04-data` 语义偏窄，实际承载数据模型、数据库设计、迁移与回滚。同时 `directory-structure.md`
存在问题：列出 23 个目录但 `init` 只创建 18 个，且除树形结构外没有任何用途说明，
`11-ci-cd/` 与 `12-release/` 挤在同一格。

# Design

改名覆盖 9 个文件的 13 处引用：`core.py` 的 sync 映射、`scaffold.py` 的 adopt 目标/目录列表/
CI 规则两处、本仓库 config 两处、三个 skills 文件、两份站点配置。同时把 adopt 分类关键词
`domain`/`domains` 补入 data 类，使新目录名能被正确归类。

`directory-structure.md` 重写为四部分：目录用途表（21 行）、sync 写入目录表、
门禁检查目录表、放置原则，并在末节说明与旧指南的差异（那 5 个从未被创建的目录）。

两条契约测试解析指南中的表格并与代码常量比较：
`test_directory_guide_matches_sync_mapping` 比对 `DEFAULT_STAGE_DOCS_MAPPING`，
`test_directory_guide_matches_ci_rules` 比对 config 的 `current_state_rules`。

# Failure Modes

- 指南与代码再次漂移：两条测试固定二者关系，缺失目录或写错路径都会失败。
- 改名遗漏：以全仓库 rg 确认无残留，并端到端验证新项目 init 与 sync 路径。
- 存量项目门禁失效：已在风险中记录，由用户承担迁移。

# Rollout

不改 CLI 行为。存量项目需手动把 `docs/04-data/` 改名为 `docs/04-domain/`
并更新 `.cabbage/config.yaml` 中 `current_state_rules` 的两处路径。
