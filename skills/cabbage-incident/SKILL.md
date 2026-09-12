---
name: cabbage-incident
description: Document production incidents and postmortems in a Cabbage project - incident timelines, impact quantification, containment and recovery, blameless root cause analysis, contributing factors, and corrective actions. Use for outages, severity events, live-service failures, or writing a postmortem retrospective.
---

# 事故与复盘

处置生产事故时，先止损、再取证、后复盘。**不要在事故进行中伪造完整时间线或结论。**

## 流程

```bash
cabbage new incident payment-timeout-2026-08-29
cabbage next payment-timeout-2026-08-29
# 1. 记录事实：填写 incident.md
cabbage verify payment-timeout-2026-08-29 incident
# 2. 分析根因：填写 postmortem.md
cabbage verify payment-timeout-2026-08-29 postmortem
# 3. 落实预防措施：完成 tasks.md 清单
cabbage verify payment-timeout-2026-08-29 implementation
cabbage gate payment-timeout-2026-08-29 merge
cabbage archive payment-timeout-2026-08-29
```

阶段 ID 以 `next` 输出为准：`incident` → `postmortem` → `implementation`。
前两个阶段是事实与分析，第三个阶段是实际修复与预防措施。

**分级降载**：正在处置的紧急故障不要为了走流程而拖延止血。
紧急修复可以用 `cabbage new hotfix <id>` 走轻量路径，事后另行新建 `incident` 记录复盘。
不要把两者混在同一个变更里。

## incident.md：先记事实

必需标题 `Impact`、`Timeline`、`Mitigation`。

- 时间戳统一用 UTC 或明确标注时区，事故期间先记原始观测，不追求措辞。
- `Impact` 量化受影响用户数、时长、区域、功能、数据与 SLO 影响；无法量化时写估计方法与误差。
- `Timeline` 记录事件、观测与采取的行动及其执行人，包括误判和无效尝试。
- `Mitigation` 区分 **Containment**（如何限制影响，如回滚、摘流量、限流）
  与 **Recovery**（如何恢复，及仍然降级的行为）。
- 恢复后补 `Recovery Verification`：证明恢复的指标、检查项与观察窗口。
- 不要写"疑似"当结论；不确定的内容标注为待确认。

## postmortem.md：对事不对人

必需标题 `Root Cause`、`Contributing Factors`、`Corrective Actions`。

- 区分 **触发点**（直接原因）与 **根因**（使其可能且未被拦截的系统条件）。
- 根因结论要有证据支撑：日志、指标、变更记录、复现步骤，而非推测。
- `Corrective Actions` 每项必须有单一责任人、期限、验证方式与状态；
  笼统的"加强监控""提高意识"不是可验证的措施。
- 保持无责文化：记录系统为何允许人为错误造成影响，不记录个人过失。

## tasks.md：预防措施落地

`postmortem.md` 中的措施要落到实际任务，完成并验证后才通过阶段。
只写计划不执行会阻塞合并门禁，这是刻意的：复盘结论必须兑现。

## 边界

- 事故记录与变更记录都属于决策历史，归档后不重写、不"现代化"措辞。
- 当前系统的运行方式写到 `docs/13-operations/`；事故报告本身是历史记录。
- 结构校验只检查标题、占位符与链接，不判断根因分析是否正确；
  复盘质量仍需人工评审。

## 同族 skill

- `cabbage-change`：变更流程、影响标记、门禁与验证、hotfix 工作流。
- `cabbage-decision`：ADR/RFC 决策记录。
- `cabbage-docs`：目录归属、命名、链接规则与 Mermaid 图表。
- `cabbage-adopt`：存量项目文档接入。

这些 skill 各自独立安装，不假设相对路径存在。
