---
change: prune-dead-remnants
cabbage_stage: design
change_type: refactor
---

# Context

find-simplifications 扫描（并行子代理 + 逐条代码复核）确认无需改动架构，
但存在一批零散死代码与失真引用：

- `scaffold.init_project` 的 config 写入条件位于早退 raise 之后，恒为真。
- `core.parse_tasks_markdown` 的 `completed_ids.update({...})` 与下游大小写不敏感排除集合重复。
- `cli.cmd_adopt` 用 `getattr` 兜底解析器必然提供的 `--apply`。
- `cli.py` 使用 `from .core import *`，使 `test_no_unused_imports_in_cli_package` 跳过该文件。
- `scaffold.sync_impact_document` 对既有文件使用非原子写入；`classify_adoption_doc` 复制两份相同的 action/target 解析。
- 测试内存在死导入与两份完全相同的 `fill_template`。
- 文档失真：cli.md 仍列已删除的 `data` 影响字段并称 adopt 使用 Git；lifecycle.md 的同步目标清单不全；两份 docs README 的字段计数与 `data` 引用过期。

# Design

- 删除恒真条件与冗余集合更新，行为不变（论证见 impact.md 的 Risks）。
- `cli.py` 改为显式导入 19 个 core 符号，纳入既有未用导入契约；不改变任何调用。
- `fill_template` 收敛到 `tests/support.py`，两份相同实现删除；test_lightweight_workflows 的 `complete` 语义不同（替换文案并自动勾选），保持独立。
- lifecycle.md 不再重述同步映射表，改为指向 `cabbage-docs` skill 的目录指南，避免再次漂移。
- 不改变命令、输出、退出码、错误消息与持久化格式。

# Failure Modes

| Failure mode | Detection | Handling | Recovery |
|---|---|---|---|
| 显式导入遗漏符号 | unittest 立即 NameError | 补齐导入后重跑 | 单文件回退 |
| 行为漂移 | test_tasks_dag、test_lightweight_workflows 回归失败 | 回退对应小改 | 单文件回退 |
| vendored 副本漂移 | test_vendored_package_matches_source | 运行 scripts/sync-vendor.py | 重新同步 |

# Rollout

纯内部清理，单次提交，无部署步骤。完成后执行 sync-vendor、全量测试、
`validate --all`、文档构建与 `ci --base origin/master` 自查。
