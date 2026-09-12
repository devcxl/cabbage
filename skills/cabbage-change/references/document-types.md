# 文档类型与记录格式

## 默认：一份变更记录

新项目的 `feature / bugfix / refactor` 使用 `change-record.md` 模板生成 `tasks.md`，
阶段 ID 为 `implementation`。必需标题：

| 标题 | 内容 |
| --- | --- |
| `Goal` | 目标或已复现问题、范围、验收标准 |
| `Design` | 最小改动方案和风险，必要时声明专项影响 |
| `Tasks` | 实际任务清单，实现完成后才勾选 |
| `Verification` | 真实执行命令与结果，修复需包含失败复现与通过回归 |

开始实现前写目标和方案，实现后补验证结果。门禁不会审查自然语言是否正确。
不需要单独 PRD、测试计划或每个任务重复四步 SOP。
记录保留在 `.cabbage/changes/<id>/`，归档后位于 `.cabbage/archive/<year>/<id>/`，
不重复复制进产品和测试目录。`change.yaml` 和 `state.json` 是机器管理的元数据。

## 高风险文档

按影响激活，不为凑齐目录而创建文件：

| 阶段 ID | 文件 | 新轻量流程必需标题 | 默认同步目录 |
| --- | --- | --- | --- |
| `adr` | `adr.md` | Context, Decision, Consequences | `docs/03-architecture/adr/` |
| `api` | `api-design.md` | Contract, Compatibility | `docs/05-api/` |
| `database` | `database-design.md` | Schema, Migration, Rollback | `docs/04-data/` |
| `security` | `security-review.md` | Threats, Controls | `docs/09-security/` |
| `release` | `release-plan.md` | Deployment, Rollback, Verification | `docs/12-release/` |

这些阶段在新轻量流程中位于 `implementation` 之前。发布方案写待执行的步骤与验证方法，
不要提前宣称执行成功；真实结果记入变更记录。
默认同步文件名为 `<change-id>.md`，不是自动分配 ADR 编号。

## 旧项目和专项工作流

原有 `prd.md`、`impact.md`、`tech-spec.md`、`test-plan.md`、`tasks.md`、RFC、事故与复盘
模板继续保留。实际必需标题取自项目工作流的 `required_headings`，不是一份全局标题清单。
旧项目默认流程不随 CLI 升级改变。

## 可选 DAG

普通 `# Tasks` 下的 `- [ ]` 清单是默认形式，不需要 DAG 或 Mermaid 图。
仅在多任务确有依赖或需要派发时使用 `## Task <id>: <title>` 分节，以及
`Builds`、`Blocked By`、`Parallel Group`、`Verification` 字段（字段名需完全匹配）。
`Blocked By` 写任务 ID 或 `None`，多个用逗号分隔。

`cabbage tasks <id>` 查看就绪与阻塞；`--export-dag` 输出派发数据，不调度执行任务。
无结构化分节时 `--export-dag` 会报错而非伪造依赖，因为普通清单没有可派发的依赖信息。

## 当前事实与历史

变更记录解释这次改动，当前文档解释系统现在的行为，二者不能靠文件复制实现语义整合。
当前文档失真时按模块更新；历史决策通过后续记录明确替代，不静默改写。
`sync` 按映射复制文档，不检查验证状态；发布前先通过合并门禁。
