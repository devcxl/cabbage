---
change: drop-redundant-data-field
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Notes |
|---|---|---|
| Product | Yes | 影响字段从 10 个减为 9 个，消除一个误导性选项。 |
| Architecture | No | 模块结构不变。 |
| API | Yes | `impact --set` 不再接受 `data`，属破坏性变更。 |
| Database | No | 不涉及持久化结构；被删字段本就与 database 重复。 |
| Security | No | 不改变权限边界。 |
| Testing | Yes | 受影响测试改为从 IMPACT_FIELDS 派生，并新增分类目标完整性测试。 |
| Deployment | No | 流水线不变。 |
| Operations | No | 无运维影响。 |
| Performance | No | 无性能影响。 |

# Risks

破坏性：此前可用 `data=true` 的调用会报 unknown impact field。
已有变更记录中的 `data` 键被容忍（validate 只检查配置字段是否缺失，不禁止多余键），
不会使签名失效；历史记录不改。
最大风险是误删 adopt 的同名分类键（`data` 类别 -> `docs/04-domain`），
已用测试固化，且实测过该 bug 的表现（KeyError）。
