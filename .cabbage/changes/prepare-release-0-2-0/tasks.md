---
change: prepare-release-0-2-0
cabbage_stage: implementation
change_type: feature
---

# Tasks

## Task 1: 同步版本号与 vendored 副本
- **Builds**: 代码、vendored CLI、PKGBUILD 和测试断言统一为 `0.2.0`。
- **Blocked By**: None
- **Parallel Group**: Group 1
- **Verification**: `python -m unittest tests.test_cabbage_rename`
- [x] 修改 `cabbage_cli/__init__.py` 并执行 `scripts/sync-vendor.py`
- [x] 更新 PKGBUILD、版本断言和发布索引

## Task 2: 整理发布说明与历史快照
- **Builds**: 评审者可以从 `docs/12-release/` 读到完整的 v0.2.0 发布说明。
- **Blocked By**: Task 1
- **Parallel Group**: Group 2
- **Verification**: `pnpm --dir docs run build`
- [x] 将发布说明状态改为发布评审稿并更新门禁结果
- [x] 更新发布索引链接，并标注 `RUNTIME.md` 为历史快照

## Task 3: 执行发布门禁
- **Builds**: 测试、校验、构建、安装和文档站点的可复现证据。
- **Blocked By**: Task 1, Task 2
- **Parallel Group**: Group 3
- **Verification**: `python -m unittest discover -s tests`
- [x] 运行测试、compileall、validate、ci 和 doctor
- [x] 运行 Python 构建、Debian 包、wheel 隔离安装和文档构建

# Verification

- `python -m unittest discover -s tests`：73 项通过。
- `python -m compileall -q cabbage_cli tests`：退出码 0。
- `python -m cabbage_cli validate --all`：VALID。
- `python -m cabbage_cli ci --base origin/master`：本次提交后通过。
- `python -m build`：生成 `0.2.0` 的 sdist 和 wheel。
- `./scripts/build-deb.sh v0.2.0`：生成 `cabbage_0.2.0_all.deb`。
- `pnpm --dir docs run build`：VitePress 构建成功。
- 隔离安装 wheel 和 `scripts/install.sh`：`cabbage --version` 为 `0.2.0`。
