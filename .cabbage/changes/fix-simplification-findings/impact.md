---
change: fix-simplification-findings
cabbage_stage: impact
change_type: refactor
---

# Impact Matrix

| Area | Impact | Notes |
|---|---|---|
| Product | No | 命令集合不变；status/next/impact 的文本输出为修复性变化，`--json` 结构不变。 |
| Architecture | No | 模块边界不变；仅清理默认值与打包元数据。 |
| API | No | CLI 参数与退出码不变；仅非 JSON 输出从破损的键名或 repr 变为可读文本。 |
| Database | No | 无持久化结构变更。 |
| Security | No | CI 权限收敛为按 job 最小化（pages/id-token 仅部署 job 持有），属收紧而非放宽。 |
| Testing | Yes | 新增 CLI 输出、CI 模板与默认影响的行为测试；docs/08-testing 覆盖列表同步更新。 |
| Deployment | Yes | CI 模板对缺失文件条件跳过并优先 vendored CLI；版本单源化与发布 tag 校验；docs/11-ci-cd 同步说明。 |
| Operations | No | 无运维影响。 |
| Performance | No | 无性能影响。 |

# Risks

- 文本输出是本次唯一的用户可见行为变化；`--json` 结构保持不变，测试同时覆盖文本与 JSON 两种形态。
- CI 模板泛化后仍与仓库自身 CI 逐字节一致，由新契约测试守护；推送后由远端 CI 实际验证。
- 版本从 0.1.0 提升到 0.1.2 并改为单源（pyproject 动态读取 `cabbage_cli.__version__`）；发布流程新增 tag 与版本一致性校验，防止再次漂移。
- incident/hotfix 默认影响收紧后，可被同步阶段满足的 testing 规则保持不变；只移除没有任何阶段能产出证据的强制默认，显式声明仍会触发既有 CI 规则。
