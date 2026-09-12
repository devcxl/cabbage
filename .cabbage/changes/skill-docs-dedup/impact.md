---
change: skill-docs-dedup
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Detail |
| --- | --- | --- |
| Product | Yes | 补充发布/回滚指引，消除说明书重复与三处 CODEOWNERS 不一致。 |
| Testing | Yes | 新增 3 项契约测试，均通过负向验证。 |
| Architecture | No | skill 结构不变，仍为七个。 |
| API | No | CLI 行为、命令与退出码均未改变。 |
| Database | No | 无持久化结构变更。 |
| Security | No | 不改变权限边界。 |
| Deployment | No | 不改流水线；新增的是发布方案写作指引。 |

# Risks

指引可能与 `release-plan.md` 模板漂移：已加测试校验四个关键标题存在。
收敛退出码到 `cli.md` 后，若有人再在别处补一份，测试会失败。
CODEOWNERS 收敛为单份后，`ownership.md` 需要跨 skill 引用，已在文中指明位置。
