---
change: prepare-release-0-2-0
cabbage_stage: tests
change_type: feature
---

# Strategy

发布 PR 的验证重点是版本一致性、vendored 副本一致性、全量回归、构建产物和文档站点。
测试通过公开 CLI、包元数据和构建命令观察结果，不直接改内部状态。

| Level | Scope | Test seam | Owner |
|---|---|---|---|
| Unit | 全量 Python 测试 | `python -m unittest discover -s tests` | maintainer |
| Contract | vendored 副本与源码、版本断言 | `test_vendored_package_matches_source`、`test_cabbage_rename` | maintainer |
| Build | wheel、sdist、Debian 包 | `python -m build`、`scripts/build-deb.sh` | maintainer |
| E2E | 隔离安装 wheel 与安装脚本 | `cabbage --version`、`cabbage init --no-vendor-cli` | maintainer |
| Docs | VitePress 生产构建 | `pnpm --dir docs run build` | maintainer |

# Cases

| ID | Scenario | Level | Expected result | Priority |
|---|---|---|---|---|
| T-1 | 全量测试 | Unit | 73 项通过，退出码 0 | High |
| T-2 | 版本一致 | Contract | 代码、vendored 副本、PKGBUILD、断言均为 `0.2.0` | High |
| T-3 | 变更校验与 PR 门禁 | Contract | `validate --all` 为 VALID，`ci --base origin/master` 通过 | High |
| T-4 | 构建制品 | Build | wheel/sdist 与 `.deb` 文件名均为 `0.2.0` | High |
| T-5 | 隔离安装 | E2E | `cabbage --version` 为 `0.2.0`，`init --no-vendor-cli` 成功 | Medium |
| T-6 | 文档站点 | Docs | VitePress 构建成功 | Medium |

# Regression Coverage

全量 unittest 覆盖 CLI、工作流、模板、任务 DAG、仓库契约和 vendored 一致性；
构建与隔离安装覆盖发布路径。

# Entry and Exit Criteria

- Entry: 版本号和发布说明已提交，工作区干净。
- Exit: 所有测试、校验、构建和安装命令退出码为 0，结果写入发布说明和 PR 正文。
