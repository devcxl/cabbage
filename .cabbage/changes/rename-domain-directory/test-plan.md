---
change: rename-domain-directory
cabbage_stage: tests
---
# Strategy

改名的风险是遗漏引用导致两处不一致。用全仓库搜索确认覆盖，再用契约测试把
"指南描述"与"代码常量"绑定，避免重写后的表格再次失真。

# Cases

- 全仓库 rg 无 `04-data` 残留（排除历史变更记录与副本）。
- 新项目 init 只创建 `docs/04-domain`，无 `docs/04-data`。
- `sync` 的 database 阶段写入 `docs/04-domain/<id>.md`，端到端验证。
- 指南中的 sync 映射与 `DEFAULT_STAGE_DOCS_MAPPING` 一致。
- 指南列出 `current_state_rules` 中的每个目录。
- 篡改指南映射或删除某目录后，对应测试必须失败。

# Evidence

`python -m unittest discover tests` 通过 56 项（新增 2 项）。

负向验证：
- 把指南中 `database` 的映射篡改为 `docs/99-wrong/` 后，
  `test_directory_guide_matches_sync_mapping` 失败。
- 从指南删掉 `docs/11-ci-cd/` 后，`test_directory_guide_matches_ci_rules` 失败。
还原后均通过。

端到端验证（临时项目）：`cabbage init` 只创建 `docs/04-domain`，无 `docs/04-data`；
`database` 阶段 verify 后 `cabbage sync` 输出
`synced 1 document(s): docs/04-domain/add-orders.md`。

覆盖检查：全仓库 rg 确认 13 处引用已改，无 `04-data` 残留。
