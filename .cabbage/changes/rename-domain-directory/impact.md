---
change: rename-domain-directory
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Detail |
| --- | --- | --- |
| Product | Yes | 目录命名更准确；目录指南从 23 条无说明的树改为 21 行用途表。 |
| Architecture | Yes | 默认目录名与 sync 映射、CI 规则同步变更。 |
| Testing | Yes | 新增两条契约测试，断言指南与代码的 sync 映射、CI 规则一致。 |
| API | No | CLI 命令、参数与退出码不变；影响字段名不变。 |
| Database | Yes | 该目录本身就是数据设计目录，改名属其定义变更。 |
| Security | No | 不改变权限边界。 |
| Deployment | No | 流水线步骤不变。 |

# Risks

破坏性变更：磁盘上 3 个存量项目（LaseAI、fcitx5-voice-input、trading-web3-ai）的
config.yaml 仍指向 `docs/04-data/`，改名后它们的 sync 目标与 CI 检查将不一致，
需要手动迁移。用户已明确选择不引入兼容分支。
`trading-web3-ai` 的 `docs/04-data/README.md` 含真实内容，需随目录一起改名。
空目录不被 git 跟踪，改名在版本库中不产生 diff。
