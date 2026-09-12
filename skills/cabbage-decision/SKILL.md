---
name: cabbage-decision
description: Write architecture decision records and RFCs in a Cabbage project - ADR context/decision/consequences, alternatives considered, superseding older decisions, and RFC proposals for cross-team review. Use when recording a technical decision, technology choice, or design tradeoff, or when an architecture impact flag activates the adr stage.
---

# 架构决策记录

写 ADR 或 RFC 的内容标准。**流程**（创建变更、声明影响、门禁、验证、归档）由 `cabbage-change` 负责。

## 先确认是否需要决策记录

| 情况 | 处理 |
| --- | --- |
| 改变组件边界、拓扑、关键依赖或数据归属 | 写 ADR |
| 跨团队讨论、需要多方评审后才能定案 | 写 ADR，必要时先写 RFC |
| 仅实现细节、内部重构、无长期影响的选型 | 不写，记入变更记录即可 |
| 已有决策仍有效 | 不重复写；新决策显式取代旧的 |

不要为每个任务都产出 ADR，"有代码改动"不等于"有架构决策"。

## 在变更流程中启用

```bash
cabbage new architecture decide-storage-engine
cabbage impact decide-storage-engine --set architecture=true
cabbage next decide-storage-engine
# 填写 adr.md
cabbage verify decide-storage-engine adr
cabbage gate decide-storage-engine implementation
```

`cabbage new architecture` 使用专项工作流（含 `impact`、RFC、`tech-spec` 等阶段）；
普通 `feature` 变更声明 `architecture=true` 只增加 `adr` 阶段。两者都以 `next` 为准。
需要长期保留时通过 `cabbage sync` 复制到 `docs/03-architecture/adr/`，
默认文件名为 `<change-id>.md`，不是自动分配编号。

## ADR 必需标题

工作流要求 `Context`、`Decision`、`Consequences`。写具体内容，不要留模板提示。

```markdown
# Context

订单量增长后单体数据库写入成为瓶颈，需要在三个月内支持 5 倍写入。
现有约束：团队无分布式事务运维经验，可用预算有限。

# Decision

采用 PostgreSQL 分区表而非引入新数据库，理由是读写模式仍以单表点查为主。
备选方案：分库分表（运维成本高）、引入时序数据库（查询模式不匹配）。

# Consequences

写入吞吐提升依赖分区键选择，需要同步调整归档任务；
运维复杂度基本不变，但迁移窗口需停机 15 分钟。
```

要点：

- `Context` 写约束和现状，不写解决方案。
- `Decision` 写选了什么**以及为什么**，列出被否决的备选方案和否决理由。
- `Consequences` 同时写正面和负面影响，包括引入的运维负担和待办。

## RFC 与编号

- 需要跨团队评审、方案尚未定案时写 `rfc.md`，阶段 ID 同样以 `next` 为准。
- 历史文档命名保持 `ADR-<4位序号>-<标题>.md`，序号递增。
- **已合并的 ADR/RFC 不重命名、不改写**：用新记录显式取代，旧记录保留。

## 建议放 `adr.md` 之外的内容

ADR 是决策记录，不是设计文档。以下内容属于其他文档：

- 完整接口定义、字段级契约 → API 设计文档
- 表结构、迁移与回滚步骤 → 数据库设计文档
- 当前系统如何工作 → 当前状态架构文档（`docs/03-architecture/system-design/`）
- 测试策略与用例 → 变更记录的 Verification 部分

写完后用 `cabbage verify` 校验结构性错误，再回到 `cabbage-change` 继续流程。

## 同族 skill

- `cabbage-change`：创建变更、影响标记、门禁与验证流程。
- `cabbage-docs`：目录归属、命名、链接规则与 Mermaid 图表模板。
- `cabbage-incident`：事故时间线与复盘。
- `cabbage-adopt`：存量项目文档接入。

这些 skill 各自独立安装，不假设相对路径存在。
