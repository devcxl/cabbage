---
change: close-loop-gaps
cabbage_stage: design
change_type: feature
---

# Context

2026-10 的闭环覆盖分析确认三处提示/契约缺口（见 prd.md 的 Goal）。当前实现：

- `cmd_status` 无参数时只输出 `done/total done N stale`，完成态与未完成态无法区分"可收尾"；
- CI 模板的测试步骤在无 `tests/` 时 `echo` 跳过，非 Python 项目拿到全绿 CI 但零测试执行；
- 评审责任与四项执行边界没有文字载体，只存在于设计者的意图中。

约束：不改门禁语义；不动 `--json` 既有字段；仓库 `.github/workflows/cabbage.yml` 与模板必须逐字节一致
（既有契约测试）；`.cabbage/tooling/cabbage_cli` 必须与源码一致（既有契约测试）。

# Design

- `cabbage_cli/cli.py` 的 `cmd_status`：聚合时计算
  `ready_to_archive = total > 0 and done == total and stale == 0`，加入行数据；
  文本模式在列表后追加提示（含 "After confirming the merge" 限定语）。单变更模式不变。
- CI 模板 `cabbage_cli/assets/integrations/cabbage.yml`：Run Test Suite 的 else 分支输出
  `::warning::` 注解（title 标注测试阶段被跳过），并更新文件头注释；`cp` 到仓库自身 workflow。
- 契约与技能：`integrations/agent-contract.md` 增"评审需平台保护""合并后归档"两条；
  router 边界节增四项外置职责；`cabbage-change` 的 archive 说明补"闭环终点"；
  `references/cli.md` 的 status 描述同步新增字段。
- README：影响表后补 `operations` / `performance` 说明；能力清单 `status` 条目补提示说明。
- 测试：`tests/test_cli_output.py` 新增可归档提示用例；`tests/test_repository_contracts.py`
  的 CI 模板用例新增 `::warning` 断言。

# Failure Modes

| Failure mode | Detection | Handling | Recovery |
|---|---|---|---|
| 含 stale 的变更被误判为可归档 | T-1 增补 stale 场景 | ready 条件要求 `stale == 0` | 修正条件并回归 |
| 提示被误解为可直接归档 | 文档评审 | 提示与文档均带确认合并限定语 | 文档澄清 |
| 模板与仓库 CI 副本漂移 | 既有契约测试（逐字节比较） | 同步复制两个文件 | 重新同步 |
| 非 Python 消费者忽略告警 | 注解出现在 PR 检查页 | 模板注释与 README 引导适配 | 后续做 `ci.test_command` 泛化 |

# Rollout

单 PR 合并，无迁移、无配置变更。成功标准：新增测试与全量回归通过，远端 CI 绿。
回滚 = revert 该 PR；`ready_to_archive` 为加性字段，无数据影响。
