---
change: prepare-release-0-2-0
cabbage_stage: requirement
change_type: feature
---

# Goal

把 `v0.1.1` 之后已合并的 51 个提交整理为 `v0.2.0` 发布候选：统一版本号、
补齐发布说明，并证明 wheel、Debian 包和文档站点可构建。之所以现在做，
是因为本版包含 `04-data` → `04-domain` 与新项目工作流收敛两处破坏性变更，
需要一份可评审的发布 PR，而不是直接打标签。

# Scope

## In Scope

- 将 `cabbage_cli.__version__`、AUR PKGBUILD、版本断言和发布索引统一为 `0.2.0`。
- 用 `scripts/sync-vendor.py` 同步仓库内 vendored CLI 副本。
- 新增 `docs/12-release/v0.2.0-release-notes.md`，列出亮点、破坏性变更、
  迁移方式、门禁结果、发版步骤、已知限制和回滚。
- 在 `RUNTIME.md` 顶部标注其为 `0.1.0` 时期的历史快照。

## Out of Scope

- 不重复评审 51 个已合并提交的实现；它们各自的变更记录已归档。
- 不打标签、不合并、不创建或发布 GitHub Release。
- 不处理 `v0.1.0` / `v0.1.1` 两个历史草稿 Release。

# Acceptance Criteria

### Scenario 1: 版本号一致

- **GIVEN**: 发布分支 `release/0.2.0` 检出后。
- **WHEN**: 读取 `cabbage_cli/__init__.py`、vendored 副本、PKGBUILD 和版本断言。
- **THEN**: 四处均为 `0.2.0`，且 `cabbage --version` 输出 `0.2.0`。
- [x] 版本号与 vendored 副本一致。

### Scenario 2: 发布门禁通过

- **GIVEN**: 版本和发布说明已提交。
- **WHEN**: 运行测试、compileall、validate、ci、Python 构建、Debian 包和文档构建。
- **THEN**: 全部命令退出码为 0，发布说明记录实际结果。
- [x] 所有发布门禁通过。

### Scenario 3: 发布动作保持未执行

- **GIVEN**: PR 已创建。
- **WHEN**: 检查仓库引用和 GitHub Release。
- **THEN**: 没有 `v0.2.0` 标签，也没有新 Release；PR 保持未合并。
- [x] 未打标签、未发布、未合并。
