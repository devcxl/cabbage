---
change: task-dag-honesty
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Detail |
| --- | --- | --- |
| Product | Yes | 修正 `tasks --export-dag` 的误导输出，并补充 DAG 使用指引。 |
| Testing | Yes | 新增 4 个回归测试，含对真实 CLI 命令的端到端调用。 |
| Architecture | No | 解析器结构未变，仅新增 `structured` 标志并在调用处使用。 |
| API | No | 子命令与参数不变；`--export-dag` 在无 DAG 时改为报错属行为修正。 |
| Database | No | 无持久化结构变更。 |
| Security | No | 不改变权限边界。 |
| Deployment | No | 不改变流水线与发布流程。 |

# Risks

行为变更为破坏性：此前对普通清单调用 `--export-dag` 会成功返回，现在会报错。
这是刻意的，因为旧输出包含 `verification: "N/A"` 与空 SOP，会诱导错误派发。
`--json` 输出新增字段，对已有消费者是向后兼容的增量。
