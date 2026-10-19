---
change: close-loop-gaps
cabbage_stage: impact
change_type: feature
---

# Impact Matrix

| Area | Impact | Notes |
|---|---|---|
| Product | Yes | `status` 文本新增归档提示；`--json` 行新增 `ready_to_archive` 加性字段。 |
| Architecture | No | 模块边界不变；仅 `cmd_status` 内聚合逻辑微调。 |
| API | No | CLI 参数与退出码不变；JSON 为加字段，无破坏性变更。 |
| Database | No | 无持久化结构变更。 |
| Security | No | 无权限、密钥或信任边界变化。 |
| Testing | Yes | 新增 CLI 输出与 CI 模板行为测试；全量回归。 |
| Deployment | No | 模板告警不改变条件跳过语义；仓库 CI 副本与模板保持逐字节一致。 |
| Operations | No | 无运维影响；本次显式声明其边界。 |
| Performance | No | 无性能影响。 |

# Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| 归档提示被误读为"无需确认即可归档" | Medium | Low | 提示与文档均带"确认合并后再归档"限定语 | maintainer |
| 文本新增行破坏依赖精确输出的脚本 | Low | Low | 仅在全部完成时追加两行；`--json` 为加字段 | maintainer |
| 非 Python 项目仍不跑测试且无人适配 | Medium | Medium | `::warning::` 注解在 PR 检查页可见；模板注释与文档引导适配 | maintainer |
