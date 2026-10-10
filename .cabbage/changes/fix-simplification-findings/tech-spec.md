---
change: fix-simplification-findings
cabbage_stage: design
change_type: refactor
---

# Context

上一轮 find-simplifications 与代码整洁扫描确认 7 组待修问题：三个命令的非 JSON
输出破损（键名或 dict repr）；`cabbage init` 生成的 CI 模板在全新项目不可运行；
`adopt --apply` 吞掉 frontmatter 异常；incident/hotfix 的强制默认影响没有对应阶段；
skill 同族清单重复且漂移；workflow 元数据、版本号、LICENSE 与发布说明等小项缺口；
agent 侧文档存在会再次漂移的重复枚举。

# Design

按文件职责拆分为 6 个独立 worktree 并行实施，主分支统一合并：

1. emit 输出：`emit` 简化为仅 JSON；status/next/impact 增加人类可读文本；cli.md
   补充输出说明并把状态、门禁、校验枚举收敛到 lifecycle/validation 的权威位置；
   新增 `tests/test_cli_output.py`。
2. CI 模板：依赖、测试与文档站点步骤按文件存在性条件跳过；validate/ci 优先使用
   vendored CLI（回退已安装的 `cabbage`，否则明确失败）；权限下沉到部署 job；
   模板与仓库 CI 保持逐字节一致并新增契约测试；docs/11-ci-cd 补说明。
3. adopt 异常：收窄为 `(OSError, UnicodeDecodeError)`，收集 `warnings` 返回并打印，
   迁移继续完成，不再静默丢失元数据。
4. 默认影响：`new_change` 只声明工作流能产出证据的影响——incident 不再强制
   `testing`，hotfix 不再强制 `operations`；显式声明保持既有 CI 规则。
5. skills：7 个同族清单补全并新增契约测试；状态与门禁枚举收敛到 references 权威文件；
   document-types 显式化 `generic.md` 回退。
6. 打包发布：删除无消费者的 workflow `name`/`description`；版本单源为 0.1.2；
   新增 LICENSE；发布前校验 tag 与版本一致；README 补 agent-contract 入链与 .deb 说明。

# Failure Modes

| Failure mode | Detection | Handling | Recovery |
|---|---|---|---|
| 文本输出回归 | tests/test_cli_output.py | 修复对应命令分支 | 单文件回退 |
| CI 模板语法或语义错误 | 新增契约测试与远端 push CI | 修复后重推 | 单文件回退 |
| vendored 副本漂移 | test_vendored_package_matches_source | 运行 scripts/sync-vendor.py | 重新同步 |
| 版本与 tag 再次不一致 | release-draft 新增的校验步骤 | 打 tag 前先更新 `__version__` | 重新打 tag |

# Rollout

六个分支逐个审查后按序合并到 master；合并完成后统一 sync-vendor，运行全量测试、
`validate --all`、文档构建与 `ci --base origin/master` 自查，再推送并跟踪远端 CI
与 Pages 部署。
