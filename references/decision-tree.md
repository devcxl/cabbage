# 变更类型与风险

## 普通变更

新初始化项目的 `feature`（功能）、`bugfix`（修复）、`refactor`（重构）使用同一轻量路径：
一份 `tasks.md`，记录目标或问题、方案、任务和实际验证结果。

- 功能：写清可观察的验收标准。
- 修复：先复现失败，再最小修复并验证回归。
- 重构：说明保持不变的行为及测试保护。

不要求单独 PRD、技术方案、测试计划、DAG 或多方案对比。纯文档调整可直接更新归属文档，
按项目策略检查链接和构建。

## 何时增加专项文档

实现前评估实际风险，使用现有影响标记，不新增复杂度档位：

```bash
cabbage impact <change-id> --set api=true --set security=true
cabbage next <change-id>
```

| 标记 | 适用情况 | 新轻量工作流增加的阶段 / 文档 |
| --- | --- | --- |
| `architecture` | 组件边界、拓扑、关键架构决策变化 | `adr` / `adr.md` |
| `api` | 外部接口契约、消息格式、兼容性变化 | `api` / `api-design.md` |
| `database` | 表结构、索引、迁移或数据安全变化 | `database` / `database-design.md` |
| `security` | 权限、认证、隐私、密钥或信任边界变化 | `security` / `security-review.md` |
| `deployment` | 需要专项部署顺序、回滚或上线验证的发布 | `release` / `release-plan.md` |

多个标记可同时启用。专项材料在实现前验证，`gate implementation` 通过后再开始实现。
计划中的验证方法写在专项文档，真实执行结果写在 `tasks.md`，不要在实现前伪造测试结果。

`product` 与 `testing` 的内容由单份记录承载，不触发重复的当前文档要求。
`operations / data / performance` 不自动生成新阶段，仍适用项目配置中的当前文档目录规则；
如果同时涉及数据库、安全等风险，应同时声明对应标记。CLI 不从代码自动推断风险。

## 保留的专项工作流

`architecture`、`migration`、`integration`、`hotfix`、`incident` 继续使用其专项流程，
阶段和默认影响以项目 `.cabbage/workflows/<type>.yaml` 和 `next` 输出为准。
不要假设任何影响字段都能凭空增加一个工作流未定义的阶段。

## 旧项目

升级 CLI 或重新生成副本不会更新项目工作流、配置、历史和已验证状态。
旧项目继续使用原阶段；迁移需另行评估活动变更和签名失效，不使用 `init --force` 自动切换。
