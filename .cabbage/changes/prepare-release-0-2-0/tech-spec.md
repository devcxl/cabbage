---
change: prepare-release-0-2-0
cabbage_stage: design
change_type: feature
---

# Context

`pyproject.toml` 通过 `[tool.setuptools.dynamic]` 读取 `cabbage_cli.__version__`，
发布工作流再校验标签与 `__version__` 一致。当前代码版本是 `0.1.2`，最新标签是
`v0.1.1`，本版含破坏性变更，因此把版本统一提升到 `0.2.0`。

# Design

## Overview

版本号仍只维护一处：`cabbage_cli/__init__.py`。`scripts/sync-vendor.py` 把
`cabbage_cli/` 复制为 `.cabbage/tooling/cabbage_cli/`，本轮只产生 `__init__.py`
一处差异。AUR PKGBUILD 的静态 `pkgver`、测试里的版本断言和发布索引同步到 `0.2.0`。
构建工具从包属性读取版本，不需要改 `pyproject.toml`。

## Interfaces and Data

CLI 接口和 change 记录格式不变。发布工作流的输入仍是 `v*` 标签，输出仍是
wheel、sdist 和 `.deb` 草稿 Release。

## Failure Modes

| Failure mode | Detection | Handling | Recovery |
|---|---|---|---|
| 某处版本仍是 0.1.2 | `grep 0.1.2`、版本断言或 Release 标签校验 | 修正后重新跑门禁 | 重新构建 |
| vendored 副本未同步 | `test_vendored_package_matches_source` 失败 | 运行 `sync-vendor.py` | 重跑测试 |
| 文档站点构建失败 | `pnpm --dir docs run build` 非零退出 | 阻止 PR 合并 | 修复 Markdown 或配置 |

# Rollout

先合并发布 PR，再在合并后的 `master` 上打 `v0.2.0` 标签并推送。
发布工作流创建草稿 Release，人工核对制品版本后再发布。本次 PR 本身不执行任何发布动作。
