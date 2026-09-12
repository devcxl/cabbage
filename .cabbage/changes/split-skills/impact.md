---
change: split-skills
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Detail |
| --- | --- | --- |
| Product | Yes | 面向 agent 的分发形态从单 skill 变为五个场景 skill。 |
| Architecture | Yes | 说明书从仓库根迁移到 `skills/<name>/`，references 归属单个 skill 而非全局共享。 |
| Testing | Yes | 契约测试改为扫描 `skills/`，新增 frontmatter 与相对链接校验。 |
| API | No | CLI 子命令、参数与退出码不变。 |
| Database | No | 无持久化结构变更。 |
| Security | No | 不改变权限边界，仍依赖托管平台保护。 |
| Deployment | No | 不改变流水线与发布流程。 |

# Risks

拆分后 agent 可能只加载一个 skill，因此每个 skill 必须自包含，`cabbage-change` 尤其要能独立覆盖常见变更。
description 需互斥且可触发，否则会漏触发或重复触发。跨 skill 相对链接在独立安装后会失效，必须避免。
移除根 `SKILL.md` 是破坏性变更，已通过 README 与测试固定新入口。
