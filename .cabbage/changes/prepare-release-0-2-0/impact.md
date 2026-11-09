---
change: prepare-release-0-2-0
cabbage_stage: impact
change_type: feature
---

# Change Summary

只改发布元数据与发布说明：版本号从 `0.1.2` 提到 `0.2.0`，同步 vendored CLI 副本，
更新 AUR 包版本和版本断言，新增 `v0.2.0` 发布评审稿。CLI 行为、工作流定义和
运行时依赖均不变。

# Impact Matrix

| Area | Impact | Notes |
|---|---|---|
| Product | No | 面向用户的变化已由 `v0.1.1..HEAD` 的 51 个提交交付。 |
| Architecture | No | 模块边界不变。 |
| API | No | 命令、参数、退出码和 JSON 字段不变。 |
| Database | No | 无持久化结构变化。 |
| Security | No | 不改变权限、密钥或信任边界。 |
| Testing | No | 只改版本断言；全量回归照常执行。 |
| Deployment | Yes | 发布标签、制品和 GitHub 草稿 Release 的版本号变化。 |
| Operations | No | 无运维流程变化。 |
| Performance | No | 无性能影响。 |

# Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| 标签与代码版本不一致导致 Release 工作流失败 | Low | Medium | 发布工作流会校验 `v${__version__}`；本地先跑全量门禁 | maintainer |
| vendored 副本与源码版本漂移 | Low | Medium | 执行 `sync-vendor.py`，并由 `test_vendored_package_matches_source` 守护 | maintainer |
| 旧草稿 Release 被误发布 | Low | High | 发布说明明确标注两个旧草稿不要发布 | maintainer |

# Documentation Updates

- `docs/12-release/README.md`：当前版本与发布记录入口。
- `docs/12-release/v0.2.0-release-notes.md`：发布评审稿。
- `RUNTIME.md`：标注历史快照。
