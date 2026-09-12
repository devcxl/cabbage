---
name: cabbage-research
description: Run evidence-driven technical research before committing to a direction - technology selection, framework or database comparison, vendor and open-source maturity assessment, PoC scoping, and recording conclusions as evidence-backed findings with explicit unknowns. Use when comparing options, evaluating whether something is production-ready, or deciding what to build before writing a change record.
---

# 技术调研与选型

把"了解某项技术"变成"基于证据的技术决策"。本 skill 自包含，不依赖其他 skill 是否安装。

## 何时启用

- 技术选型、方案对比、架构评估。
- 框架、中间件、数据库、云服务、API、协议或模型调研。
- 开源项目成熟度、维护状态、安全性、生产可用性评估。
- 性能、稳定性、扩展性、成本或迁移风险评估。

**不启用**：查询一个明确事实、解释基础概念、用户已定方案只要实现代码、纯代码 bug 调试。

**关键判断**：如果结论不会改变任何决策，就不要调研，直接实现。

## 调研不建变更记录

调研阶段尚未定案，不要创建变更记录，也不要为调研填写 `tasks.md`。

```text
调研（产出报告）→ 结论 → 需要落地时才交给变更流程
```

只有结论需要长期保留或需要落地代码时，才交接给 `cabbage-change` 或 `cabbage-decision`。

## 强制纪律

1. **先定义决策，后收集资料**。开始前写下"要回答什么问题"和"什么条件下选哪个方案"。
2. **硬性约束优先于加权评分**。不满足硬性约束的方案直接淘汰，不进入评分表。
3. **事实、推断、未知项必须分开**。不得把推断写成事实。
4. **每个关键结论必须可追溯到证据**：来源、时间、版本、支撑的具体结论。
5. **优先验证失败路径**，不只验证正常路径。
6. **无法验证就写"待验证"**，禁止补全式猜测。
7. **推荐必须包含适用边界、代价和退出条件**（什么情况下需要重新评估）。

## 证据分级

按可信度从高到低使用，低等级证据只能作为线索：

| 等级 | 来源 | 用途 |
| --- | --- | --- |
| A | 官方文档、规范、源码、Release Notes、官方安全公告 | 核心事实与行为确认 |
| B | 官方 Benchmark、官方示例、维护者 Issue/Discussion | 实现细节与限制确认 |
| C | 独立实测、生产案例、论文 | 性能与生产经验交叉验证 |
| D | 高质量社区讨论、技术文章 | 发现问题的线索 |
| E | 聚合文章、营销材料、无原始数据的结论 | 仅作线索，不作单独依据 |

版本与时间必须记录：某特性在 v2.0 加入，不代表你评估的 v1.x 有它。

## 调研步骤

1. **明确决策**：要选什么、硬性约束是什么、什么算可接受。
2. **列出候选**：通常 3-5 个，含现状（"不改变"也是候选）。
3. **逐项取证**：按证据分级记录，标注未知项。
4. **验证高风险假设**：用最小 PoC、源码阅读或故障注入，不必写完整系统。
5. **对比与结论**：先按硬性约束淘汰，再对比剩余项的成本与风险。
6. **记录退出条件**：什么信号出现时需要重新评估。

PoC 的边界：只验证会导致方案被否决的那个假设，不开发完整系统。

## 产出格式

调研报告至少包含：

```markdown
# 决策问题
要决定什么，硬性约束是什么。

# 候选方案
| 方案 | 满足硬性约束 | 关键证据（含等级与版本） | 成本与风险 |

# 事实
| 结论 | 证据来源 | 等级 | 时间/版本 |

# 推断与未知项
明确标注哪些是从证据推导的，哪些尚未验证及验证方法。

# 推荐
推荐哪个、适用边界、代价、退出条件。
```

## 交接

| 结论形态 | 交给 |
| --- | --- |
| 需要长期保留的架构决策 | `cabbage-decision`（写 ADR/RFC） |
| 需要落地代码 | `cabbage-change`（创建变更并声明影响） |
| 需要跨团队评审后才定案 | `cabbage-decision`，用 RFC 阶段 |

交接时带上：已确认的事实、被否决的方案及否决理由、未决问题。
不要让下一个环节重新调研。

**常见误区**：把调研结论直接写成 ADR，跳过 `cabbage-change` 的影响声明；
或反过来，为了让调研"入库"而创建只包含调研内容的变更记录。两者都不要。

如果同时涉及要在生产落地的架构变更，先看 `cabbage-change` 的 `architecture` 变更类型
（含 `impact` → `rfc` → `design` → `adr` 阶段），不要自行拼装流程。

## 同族 skill

`cabbage`（选路与组合编排）、`cabbage-change`、`cabbage-decision`、
`cabbage-incident`、`cabbage-docs`、`cabbage-adopt`。

各自独立安装，不假设相对路径或其他 skill 已存在。
