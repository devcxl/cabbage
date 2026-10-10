---
change: fix-simplification-findings
cabbage_stage: implementation
change_type: refactor
---

# Tasks

- [x] 修复 status（无 id）/ next / impact 的非 JSON 输出，`emit` 简化为仅 JSON，新增 `tests/test_cli_output.py`。
- [x] cli.md 补输出说明并把状态、门禁、校验枚举收敛到 lifecycle/validation 权威位置。
- [x] CI 模板条件化（requirements/tests/文档站点）、validate 与 ci 优先 vendored CLI、权限最小化，并保持模板与仓库 CI 逐字节一致。
- [x] 新增 CI 模板契约测试（一致性、守卫断言、全新项目经 vendored CLI 跑通 validate）。
- [x] adopt 迁移收窄异常并报告 frontmatter 写入失败，新增回归测试。
- [x] incident 不再默认 testing、hotfix 不再默认 operations；新增默认值与 CI 行为测试。
- [x] 7 个同族 skill 清单补全并新增契约测试；状态与门禁枚举收敛；显式化 generic.md 回退。
- [x] 删除 asset workflow 无消费者元数据；版本单源为 0.1.2；新增 LICENSE 与发布 tag 校验。
- [x] README 补 agent-contract 入链与 .deb 说明，docs/12-release 版本说明同步。
- [x] 六分支合并后统一 sync-vendor，跑全量测试、validate、文档构建、ci 自查与空白检查。

# Verification

- `python -m unittest discover tests`：71 项通过（基线 59 + 新增 12）。
- `python -m cabbage_cli validate --all`：VALID。
- `pnpm --dir docs run build`：构建成功（10.25s）。
- `python scripts/sync-vendor.py`：副本已同步（test_vendored_package_matches_source 通过）。
- 冒烟实测：`status` 输出 `demo  0/1 done  0 stale`；空项目输出 `no active changes`；
  `next` 输出 `ready:` 段；`impact --set api=true` 输出矩阵且 `--json` 结构不变。
- `git diff --check`：无空白错误。
- `ci --base origin/master` 绑定自查在记录提交后执行（diff 需要包含本次提交）。
