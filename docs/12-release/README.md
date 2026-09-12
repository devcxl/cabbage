# 发布说明

Cabbage 当前版本为 `0.1.0`。`.github/workflows/release-draft.yml` 在 `v*` 标签推送时运行测试、构建 Python 包和 Debian 包，并创建 GitHub 草稿 Release；不自动发布到公共 PyPI。

## 发布物

| 发布物 | 当前形式 |
| --- | --- |
| Python 包 | 项目名 `project-docs-cabbage`，包含 `cabbage_cli` 与内置 assets |
| 命令行入口 | `cabbage = cabbage_cli.cli:main` |
| 本地安装入口 | `scripts/install.sh` 在用户可执行目录创建 `cabbage` 启动脚本 |
| 项目内工具副本 | `cabbage init` 默认复制到 `.cabbage/tooling/cabbage_cli/` |
| 文档站点 | `docs/` 下的 VitePress 静态站点，主分支 CI 成功后部署到 GitHub Pages |

## 兼容性基线

- Python：3.10 及以上。
- 运行依赖：PyYAML 6.0 及以上。
- 当前包版本与 `cabbage --version`：`0.1.0`。
- 文档构建环境：Node.js 22、pnpm 10。

## 发布前检查

发布候选版本至少应通过：

```bash
python scripts/sync-vendor.py
python -m unittest discover -s tests -v
python -m compileall -q cabbage_cli tests
python -m build
cabbage docs build
```

还应在隔离环境安装生成的 wheel，并验证：

```bash
cabbage --version
cabbage init --no-vendor-cli
```

对于受 Cabbage 管理的发布变更，发布前还必须完成所有已激活阶段并通过：

```bash
cabbage validate <change-id>
cabbage gate <change-id> merge
```

## 版本与变更记录

版本号同时存在于 `pyproject.toml` 和 `cabbage_cli/__init__.py`，发布时必须保持一致。变更文档保存在 `.cabbage/changes/`，完成后通过 `cabbage archive <change-id>` 移入按年份组织的归档目录。

## 回滚原则

- 尚未发布的构建失败：修复后重新构建，不复用未验证产物。
- 已发布包存在缺陷：发布新的修复版本，不覆盖既有版本。
- workflow 或模板导致项目门禁异常：回退相关变更，用 `python scripts/sync-vendor.py` 重新生成本仓库 CLI 副本。
- 新轻量默认仅随新项目初始化提供，不自动迁移旧项目工作流或签名；不要用 `init --force` 升级 CLI。
- 文档站点构建失败：阻止合并或部署，不绕过 VitePress 构建检查。

## 当前边界

标签推送和草稿 Release 转正式发布仍需维护者决定；当前没有自动版本递增、制品签名或公共包仓库发布。不要把文档部署成功当作已发布新包版本。
