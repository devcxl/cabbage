---
change: collapse-change-workflows
cabbage_stage: impact
change_type: feature
---

# Impact Matrix

| Area | Impact | Notes |
|---|---|---|
| Product | Yes | 新项目的变更类型、阶段命名、gate 目标与 help 输出变化；`--export-dag` 移除。 |
| Design | No | 本变更自身不需要专项技术方案；新增 `design` 字段供其他变更选用。 |
| Architecture | No | 模块边界不变（cli/core/scaffold 职责维持）。 |
| RFC | No | 无跨团队评审需求；新增 `rfc` 字段供其他变更选用。 |
| API | No | CLI 命令集合不变；新增类型 `change`、gate 目标泛化、移除 `--export-dag` 标志，均在新项目/新用法层面生效。 |
| Database | No | 无持久化结构变更；change.yaml 字段集合向后兼容（新增字段仅新配置启用）。 |
| Security | No | 无权限、密钥或信任边界变化。 |
| Testing | Yes | 轻量流程、CLI 输出、README 可执行示例、模板一致性等测试全面更新。 |
| Deployment | No | 无部署流程变化；随 CLI 版本发布生效。 |
| Operations | No | 无运维影响。 |
| Performance | No | 无性能影响。 |

# Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| 存量新项目（已用旧 8 类模板初始化）继续 `new feature` 报错 | Medium | Low | 报错信息附带可用类型提示；既有项目工作流文件仍在，`new` 仍按其自身 workflows 解析 | maintainer |
| `--export-dag` 有既有使用方 | Low | Medium | 该能力面向本仓库自用的子代理派发；阶段二由插件侧接管派发职责，README 同步说明 | maintainer |
| 新增 impact 字段被误解为必填 | Low | Low | 字段为显式 opt-in，默认 false；文档与模板注释说明用途 | maintainer |
| gate 目标泛化引入回归 | Low | Medium | 保留 merge/archive 分支原语义；新增阶段 id 分支仅在前置阶段校验处泛化，全量测试覆盖 | maintainer |

# Documentation Updates

- README（快速开始 / 高风险表 / 能力与边界）、docs/00-overview
- skills 全家（cabbage-change / cabbage-decision / cabbage-research / cabbage-incident / cabbage-adopt / references）
- integrations/agent-contract.md、模板注释（change-record.md、impact.md）
