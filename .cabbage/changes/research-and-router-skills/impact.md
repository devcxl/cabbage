---
change: research-and-router-skills
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Detail |
| --- | --- | --- |
| Product | Yes | 说明书分发从五个 skill 增加为七个，新增入口与调研职责。 |
| Architecture | Yes | 引入"入口做选路、其余自包含"的结构，避免入口膨胀为新的全流程说明书。 |
| Testing | Yes | 新增路由覆盖校验，并对其做负向验证确认可捕获遗漏。 |
| API | No | CLI 子命令、参数与退出码不变，未新增变更类型。 |
| Database | No | 无持久化结构变更。 |
| Security | No | 不改变权限边界。 |
| Deployment | No | 不改变流水线与发布流程。 |

# Risks

入口 skill 有膨胀风险：一旦开始描述具体步骤就会与 `cabbage-change` 重复，边界已在文件中写死为三项职责。
调研结论若被直接写成 ADR 会跳过变更流程，已在两个 skill 中明确交接规则。
新增 skill 若不更新路由表会导致无法触达，已由契约测试覆盖。
