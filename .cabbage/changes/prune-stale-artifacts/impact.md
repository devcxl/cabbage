---
change: prune-stale-artifacts
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Detail |
| --- | --- | --- |
| Product | Yes | 删除失真的测试报告与过期示例，文档不再指向已失效的阶段名。 |
| Testing | Yes | 新增死导入检测契约测试，并做负向验证。 |
| Architecture | No | 模块结构、导入图与依赖不变。 |
| API | No | CLI 命令、参数与退出码均未改变。 |
| Database | No | 无持久化结构变更。 |
| Security | No | 不改变权限边界。 |
| Deployment | No | 不改流水线；移除的文件不在打包与发布路径中。 |

# Risks

删除 TEST_REPORT.md 会丢失其独有信息（打包容器无 npm registry）：该情况已过时，
CI 现每天构建站点，相关信息已并入 docs/08-testing/。
删除 examples/ 会失去三份示例，但它们零引用且阶段名已失效，
README 中有受测试保护的可执行示例可替代。
空目录风险：仓库内 5 个空 docs 目录保留，避免与 CLI 的 ALL_CONFORMING_DIRS 设计冲突。
