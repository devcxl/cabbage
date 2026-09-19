---
change: prune-stale-artifacts
cabbage_stage: tests
---
# Strategy

清理类变更的主要风险是"删了还在用的东西"，因此每条候选都要有零引用的搜索证据，
并新增契约测试防止死代码重新引入。

# Cases

- 死导入检测：重新引入 `shutil` 后测试必须失败。
- 全量测试、validate、文档构建通过。
- 删除后 `rg` 确认无残留引用（README、docs、skills、CI、打包脚本）。
- vendored 副本与源码一致。

# Evidence

`python -m unittest discover tests` 通过 54 项（原 53，新增死导入检测 1 项）。

负向验证：重新加入 `import shutil` 后，
`test_no_unused_imports_in_cli_package` 以 `+ ['shutil'] : unused imports in core.py` 失败；
还原后通过。

清理前证据：
- `dataclass`、`Any`、`shutil`、`os` 在各自文件中除导入行外零使用。
- `scaffold.py:142` 的 `import re` 与第 5 行顶层导入重复。
- `TEST_REPORT.md` 零引用；声称的 `complete` 命令在 CLI 中不存在；3 处 VuePress 已过时。
- `examples/` 三文件零入链，`new-feature.md` 使用 `requirement`/`impact` 等新流程不存在的阶段名。
