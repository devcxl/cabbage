---
change: prune-dead-remnants
cabbage_stage: tests
change_type: refactor
---

# Strategy

本次为行为保持清理，回归由现有测试承担，不新增测试文件；
验证重点是清理前后的可观测行为一致。

# Cases

- `python -m unittest discover tests`：全部通过（数量以运行输出为准）。
- `parse_tasks_markdown`：ready/blocked 判定与完成计数不变（test_tasks_dag 既有断言）。
- `init_project`：普通与 `--force` 初始化行为不变（test_lightweight_workflows、test_cabbage_rename）。
- `cmd_adopt`：`--apply` 迁移路径不变（test_adopt、test_engine_enhancements）。
- cli 显式导入：`test_no_unused_imports_in_cli_package` 覆盖 cli.py 且通过。
- `python -m cabbage_cli validate --all`：VALID。
- `python -m cabbage_cli ci --base origin/master`：CABBAGE CI PASSED。
- `pnpm --dir docs run build`：构建成功。

# Regression Coverage

- 命令与输出契约：README 示例退出码（test_readme_command_examples_execute）。
- 副本一致性：test_vendored_package_matches_source。
- 文档引用：skills 链接、阶段名与目录映射契约测试。

# Risks

- 清理不改变行为，因此不新增测试；覆盖缺口维持在既有测试已暴露的范围。
- 若清理引入偏差，回退单文件改动，不扩大范围。
