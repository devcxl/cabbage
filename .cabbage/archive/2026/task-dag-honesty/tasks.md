---
change: task-dag-honesty
cabbage_stage: implementation
---
# Tasks

- [x] 解析器新增 `structured` 标志，非结构化时不生成派发计划。
- [x] `--export-dag` 在无结构化分节时报错并说明所需格式。
- [x] 文本输出修正误导信息。
- [x] 新增回归测试，并验证还原守卫后测试会失败。
- [x] 更新 `cli.md`、`document-types.md` 与 `cabbage-change` 的 DAG 指引。
- [x] 删除零内容的孤儿变更 `tasks-export-dag-versioned`。
- [x] 同步 vendored CLI，运行全量测试与文档构建。

# Verification

- `python -m unittest discover tests`：50 项通过。
- `python -m cabbage_cli validate --all`：VALID。
- `python -m cabbage_cli tasks <id> --export-dag`（普通清单）：按预期报错并说明原因。
- 删除孤儿变更后 `cabbage status` 不再列出 `tasks-export-dag-versioned`。
- `pnpm --dir docs run build`：构建成功。
- `git diff --check`：无空白错误。

未覆盖：`--export-dag` 行为变更对仓库外既有调用方的影响无法在本仓库验证。
