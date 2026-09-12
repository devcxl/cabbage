---
name: cabbage-change
description: Run Cabbage change records and gates in a project with .cabbage/ - create and classify changes, declare impact, pass implementation and merge gates, verify artifacts, sync and archive. Use for feature work, bug fixes, refactors, and any code change that needs a tracked change record.
---

# Cabbage 变更流程

在 `.cabbage/` 项目中做任何代码改动前，先确认变更记录、阶段和门禁。
阶段真相来自项目工作流文件，不是文档文件名。

## 先读项目实际工作流

```bash
cabbage status                    # 无参数：列出本仓库全部活动变更
cabbage status <change-id>        # 该变更的各阶段状态
cabbage next <change-id>          # 当前可做与被阻塞的阶段
```

`pending` 未验证；`done` 已验证；`stale` 验证后上游或内容变化，需重新审阅并验证；
`skipped` 当前影响未启用。以 `next` 输出为准，不要猜测阶段 ID。

## 默认路径：一次变更一份记录

新初始化项目的 `feature / bugfix / refactor` 只有一份 `tasks.md`，阶段 ID 为 `implementation`，
必须包含 `Goal`、`Design`、`Tasks`、`Verification`。

```bash
cabbage new bugfix fix-label
# 填写 tasks.md 的 Goal（含复现的问题）和 Design（最小修复方案）
cabbage gate fix-label implementation     # 无高风险前置时直接 ALLOWED
# 复现失败 → 最小修复 → 回归测试
# 完成任务清单并写入真实命令与结果
cabbage verify fix-label implementation
cabbage validate fix-label
cabbage gate fix-label merge
cabbage archive fix-label
```

不要为普通变更额外生成 PRD、测试计划、DAG 或多方案比较。
`change.yaml` 与 `state.json` 是 CLI 管理的元数据，不要手工编辑 `state.json`。

## 高风险才展开

实现前评估真实风险，用现有影响字段激活专项阶段：

```bash
cabbage new feature update-api
cabbage impact update-api --set api=true --set security=true
cabbage next update-api
```

| 影响标记 | 增加的阶段 / 文档 | 含义 |
| --- | --- | --- |
| `architecture=true` | `adr` / `adr.md` | 组件边界、拓扑或关键架构决策变化 |
| `api=true` | `api` / `api-design.md` | 外部接口契约、消息格式、兼容性变化 |
| `database=true` | `database` / `database-design.md` | 表结构、索引、迁移或数据安全变化 |
| `security=true` | `security` / `security-review.md` | 权限、认证、隐私、密钥或信任边界变化 |
| `deployment=true` | `release` / `release-plan.md` | 需要专项部署顺序、回滚或上线验证的发布 |

专项阶段位于 `implementation` 之前，必须逐一验证后才通过实现门禁。
专项文档写待执行的步骤与验证方法，真实执行结果写入 `tasks.md`，不要在实现前伪造测试证据。

风险由人或 Agent 判断，CLI 不会自动推断。不要为少写文档而隐瞒实际影响；
也只在确有风险时声明，普通发布不必标记 `deployment=true`。
`product` 与 `testing` 的证据留在单份记录中，不另建重复的当前文档。
写 ADR、RFC 的内容标准见 `cabbage-decision` skill；需要先做技术选型或方案对比时，
用 `cabbage-research` 得出结论再回来填写，调研本身不建变更记录。

## 其他变更类型

| 类型 | 用途 | 阶段来源 |
| --- | --- | --- |
| `architecture` | 影响多个模块的架构调整 | 含 `impact`、RFC、`tech-spec` 等专项阶段 |
| `migration` | 数据迁移，默认开启 database/deployment | 专项阶段 + 条件高风险阶段 |
| `integration` | 对接外部系统，默认开启 api | 含 `requirement` 等专项阶段 |
| `hotfix` | 生产紧急修复 | `impact` → `tests` → `implementation` → `release` |
| `incident` | 事故记录与复盘 | 见 `cabbage-incident` skill |

这些工作流的阶段与默认影响以 `.cabbage/workflows/<type>.yaml` 和 `next` 输出为准。
不要假设任意影响字段都能凭空新增一个工作流未定义的阶段。
纯文档更新可直接修改归属文档，写作用 `cabbage-docs` skill。

## 命令与退出码

```bash
cabbage new <type> <change-id>          # 创建变更工作区
cabbage impact <change-id> [--set k=v]  # 查看或更新影响矩阵
cabbage verify <change-id> <stage>      # 验证单个阶段并记录内容指纹
cabbage validate <change-id> | --all    # 校验结构、链接、占位符
cabbage gate <change-id> implementation|merge|archive
cabbage sync <change-id>                # 按映射复制专项文档到 docs/
cabbage archive <change-id>             # 先检查门禁，再同步并归档
cabbage ci --base origin/main           # 在 CI 中检查差异、门禁与文档规则
cabbage discard <change-id>             # 放弃活动变更
```

`verify` 失败返回 2；`validate`、`gate`、`ci` 报告错误返回 1。
`next` 在所有阶段完成或跳过时返回 0，仍有待办但无可执行阶段时返回 2。

## 任务分解与 DAG（按需）

普通清单已足够：`# Tasks` 下的 `- [ ]` 列表就是默认形式，不需要 Mermaid 图或依赖声明。
一套任务拆成两种粒度会失去意义，**只在真有并行或阻塞关系时才拆**。

需要声明依赖时，用结构化分节（字段名固定，解析器按字面匹配）：

```markdown
## Task 1: 数据库表结构
- **Builds**: 可观测的交付结果
- **Blocked By**: None
- **Parallel Group**: G1
- **Verification**: `pytest tests/test_schema.py`
- [ ] 建立表结构

## Task 2: 登录接口
- **Builds**: 登录能力
- **Blocked By**: Task 1
- **Parallel Group**: G2
- **Verification**: `pytest tests/test_api.py`
- [ ] 实现接口
```

要点：

- `Blocked By` 写任务 ID（`Task 1`）或 `None`，多个用逗号分隔；不要写任务标题。
- 只有写完整结构化分节才被识别为任务；否则按普通清单处理。
- `cabbage tasks <id>` 查看就绪与阻塞情况，`--json` 输出结构化结果。
- `--export-dag` 只在存在结构化分节时输出派发数据；普通清单会**报错并说明原因**，
  不会凭空生成依赖。它只导出数据，不执行任务。
- 派发数据中的 `verification` 来自任务自己的 `Verification` 字段；
  普通清单没有该字段，因此不会被当作可派发任务。

并行子代理与多方案比较按任务需要采用，不是所有变更的前置义务。
复杂任务可先做目标拆解（分层拆到可独立执行），再落成结构化分节。

## 约束与排错

- `verify` 检查结构、必需标题、占位符、未勾选清单、本地链接与 Mermaid 围栏，并记录内容指纹；
  不证明代码正确、文档语义正确或审批身份。
- 验证后修改上游材料会使依赖它的阶段变为 `stale`，需重新审阅并验证。
- `sync` 只按映射复制，不检查验证状态、不做语义合并；发布前先通过 `gate merge`。
- `archive` 不检查 Git 是否已合并，确认合并后再执行。
- 升级 CLI 不会迁移既有项目的工作流、配置或已验证状态。不要使用 `init --force` 升级，
  它会覆盖项目配置与工作流。旧流程的 `requirement`/`design`/`tests` 等阶段继续按 `next` 使用。

常见错误：

| 报错 | 处理 |
| --- | --- |
| `placeholder content remains` | 清除 `TODO`/`TBD`/`FIXME` 及模板提示文本 |
| `unchecked tasks remain` | 完成清单项后改为 `- [x]` |
| `gate implementation: BLOCKED` | 用 `next` 找到未完成的已启用前置阶段并验证 |
| `no structured DAG` | `--export-dag` 只接受结构化任务分节；普通清单无需导出 |
| 阶段 `stale` | 对照上游变化重新审阅，再 `cabbage verify` |
| `broken link` | 修正相对路径或锚点，见 `cabbage-docs` skill |

## 按需参考

- [命令与退出码](references/cli.md)
- [状态、门禁与归档](references/lifecycle.md)
- [验证规则与证据要求](references/validation.md)
- [记录格式与高风险文档](references/document-types.md)

## 同族 skill

- `cabbage`：总入口，选路与组合编排。
- `cabbage-research`：技术选型与方案调研（调研不建变更记录）。
- `cabbage-decision`：ADR/RFC 内容标准。
- `cabbage-incident`：事故复盘。
- `cabbage-docs`：文档写作与站点。
- `cabbage-adopt`：存量项目接入。

各自独立安装，不假设相对路径或其他 skill 已存在。
