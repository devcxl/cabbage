---
change: drop-redundant-data-field
cabbage_stage: tests
---
# Strategy

删除字段的主要风险是连带删除同名但无关的 adopt 分类键。因此既验证删除生效，
也验证 adopt 仍能处理数据库类文档，并对"分类键都有目标"加断言。

# Cases

- `impact --set data=true` 被拒绝，提示 unknown impact field。
- 新项目 config 的 impact_fields 与 current_state_rules 均无 data。
- impact.md 模板无 Data 行，且模板行与 IMPACT_FIELDS 完全对应。
- adopt 分类：database/schema/migration/domain 均归类为 data -> docs/04-domain。
- 每个 adopt 分类键都有目标目录。
- 已有变更记录（含 data 键）validate 与 gate 仍通过。

# Evidence

`python -m unittest discover tests` 通过 57 项（新增 adopt 分类完整性 1 项）。
本次为 `refactor` 类型，工作流阶段为 impact/design/tests/implementation，无 requirement。

实测确认：
- `impact --set data=true` 报 `unknown impact field: data`。
- 新项目 config 的 impact_fields 为 9 个字段，无 data；current_state_rules 无 data。
- 本仓库旧工作流新建变更的 impact.md 生成 9 行表格，无 Data 行。
- adopt 分类：`database/schema.md`、`migrations/001.md`、`domain/model.md`
  均归为 category=data、target=docs/04-domain。
- 既有 12 个变更的 change.yaml 仍含 data 键，`validate --all` 与 `gate merge` 均通过
  （validate 只检查配置字段是否缺失，多余键被忽略）。

修复过程中真实复现过一次 bug：删除 impact 字段时连带删除了 adopt 的
`"data":"docs/04-domain"` 目标键，`classify_adoption_doc(Path("database/schema.md"))`
抛出 `KeyError: 'data'`。恢复后新增
`test_every_adoption_category_has_a_target` 固化，负向验证确认删掉该键测试会失败。
