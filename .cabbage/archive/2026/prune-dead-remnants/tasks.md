---
change: prune-dead-remnants
cabbage_stage: implementation
change_type: refactor
---

# Tasks

- [x] 删除 `init_project` 中恒真的 config 写入条件（早退 raise 之后）。
- [x] 删除 `parse_tasks_markdown` 中与下游排除集合重复的 `completed_ids.update`。
- [x] `cmd_adopt` 改用解析器必然提供的 `a.apply`，去掉 `getattr` 兜底。
- [x] `cli.py` 通配导入改为显式导入 19 个 core 符号。
- [x] `sync_impact_document` 改用原子写入；`classify_adoption_doc` 去掉重复的 action/target 解析。
- [x] 删除测试死导入；将两份相同的 `fill_template` 收敛到 `tests/support.py`。
- [x] 修正 cli.md、lifecycle.md、docs README 中的失真引用。
- [x] 修正 install.sh 提示文案；.gitignore 忽略根目录构建产物 `/dist/`。
- [x] 同步 vendored 副本，运行全量测试、`validate --all`、文档构建与空白检查。

# Verification

- `python -m unittest discover tests`：59 项通过。
- `python -m cabbage_cli validate --all`：VALID。
- `pnpm --dir docs run build`：构建成功（11.39s）。
- `python scripts/sync-vendor.py`：副本已同步（test_vendored_package_matches_source 通过）。
- `git diff --check`：无空白错误。
- 行为抽查：临时项目中 `init` 后手工改写 `.cabbage/config.yaml`，再执行 `init --force`，
  配置按既有语义被覆盖刷新（与清理前一致，README 已声明该行为）。
- `ci --base origin/master` 绑定自查在提交后执行（diff 需要包含本次提交）。
