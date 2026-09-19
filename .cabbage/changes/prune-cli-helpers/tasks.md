---
change: prune-cli-helpers
cabbage_stage: implementation
---
# Tasks

- [x] 删除无调用者的 core.run()。
- [x] core.workflow() 补存在性检查，scaffold 两处改用该封装。
- [x] 新增 changes_root/archive_root，收敛 cli.py 三处硬编码路径。
- [x] 删除 get_change_tasks_dag 的未使用变量。
- [x] 修复不可达判定分支，保持 [/] 与 [-] 的既有行为。
- [x] 新增两条契约测试并完成负向验证。
- [x] 实测友好错误消息与归档路径未变。
- [x] 同步 vendored CLI，运行全量测试与文档构建。

# Verification

- `python -m unittest discover tests`：59 项通过。
- `python -m cabbage_cli validate --all`：VALID。
- `python -m cabbage_cli ci --base HEAD`：CABBAGE CI PASSED。
- `pnpm --dir docs run build`：构建成功。
- `python scripts/sync-vendor.py`：副本已同步。
- `git diff --check`：无空白错误。

代码变化：6 个文件（含副本）46 增 38 减。
未覆盖：CI 正则与 exclude_prefixes 中的字面 `.cabbage` 有意保留，未改为常量。
