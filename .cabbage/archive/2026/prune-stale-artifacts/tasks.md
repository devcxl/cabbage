---
change: prune-stale-artifacts
cabbage_stage: implementation
---
# Tasks

- [x] 删除 core.py / cli.py / scaffold.py 中的死导入与函数内重复导入。
- [x] 删除失真的 TEST_REPORT.md，把仍有效的现状并入 docs/08-testing/。
- [x] 删除零引用且使用失效阶段名的 examples/ 三个文件。
- [x] 新增死导入检测契约测试并完成负向验证。
- [x] 确认无残留引用（含 VitePress 配置）。
- [x] 同步 vendored CLI，运行全量测试与文档构建。

# Verification

- `python -m unittest discover tests`：54 项通过。
- `python -m cabbage_cli validate --all`：VALID。
- `pnpm --dir docs run build`：构建成功。
- `python scripts/sync-vendor.py`：副本已同步。
- `git diff --check`：无空白错误。
- 删除后搜索 examples/ 与 TEST_REPORT：无残留引用，VitePress 配置未引用。

未覆盖：docs/ 下 5 个空目录（04-data、09-security、13-operations、15-incidents、
03-architecture/rfc）经评估属 CLI 的 ALL_CONFORMING_DIRS 有意设计，本次保留。
