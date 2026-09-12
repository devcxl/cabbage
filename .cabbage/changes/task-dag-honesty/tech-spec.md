---
change: task-dag-honesty
cabbage_stage: design
---
# Context

轻量工作流的 Tasks 是普通清单。解析器在找不到 `## Task <id>` 分节时回退为逐复选框扫描，
为每个条目生成 `blocked_by: []`、`verification: "N/A"`、`sop: []` 的任务，
并据此输出派发计划与执行提示，声称任务已就绪且无需依赖。

# Design

`parse_tasks_markdown` 新增 `structured` 标志：仅当存在结构化任务分节时为真。
派发计划只在结构化时生成，因为普通清单没有可派发的依赖与验证信息。

`cmd_tasks`：

- `--export-dag` 在非结构化时抛 `CabbageError`，说明需要什么样的分节，退出码非零；
- 文本输出在非结构化时给出说明，而不是 "No tasks currently ready"。

结构化路径的行为与输出保持不变。`--json` 原样输出解析结果，因此自动包含新标志。

# Failure Modes

- 破坏既有调用方：仅影响对普通清单执行 `--export-dag` 的场景，且旧行为本身是错的。
- 误判结构化：判定条件与既有的 `## Task` 提取共用同一分支，不存在第二套判定。
- 文档与实现再次漂移：`cli.md`、`document-types.md` 与 `cabbage-change` 同步更新，
  由既有契约测试保证阶段 ID 与链接有效。

# Rollout

仅改 CLI 与说明文件。删除 `.cabbage/changes/tasks-export-dag-versioned/`：
7 个文件零实质内容（去模板后正文 0 行），本变更覆盖其命名所暗示的方向。
