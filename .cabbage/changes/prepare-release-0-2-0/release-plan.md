---
change: prepare-release-0-2-0
cabbage_stage: release
change_type: feature
---

# Deployment

| Order | Action | Owner | Success signal |
|---|---|---|---|
| 1 | 合并发布 PR，确认 `master` CI 通过 | maintainer | merge commit 的 CI 成功 |
| 2 | 在合并后的 `master` 上创建并推送 `v0.2.0` 标签 | maintainer | 标签指向包含 `__version__ = "0.2.0"` 的提交 |
| 3 | 等待 Draft Release 工作流完成 | maintainer | wheel/sdist 与 `.deb` 均以 `0.2.0` 命名 |
| 4 | 用发布说明替换自动生成正文，核对后发布 | maintainer | Release 页面版本与制品一致 |

本 PR 只准备发布元数据，不执行第 1 步之后的任何动作。

# Rollback

| 可测量触发条件 | 处置 |
|---|---|
| 标签与 `__version__` 不一致导致工作流失败 | 删除标签，修正版本后重新打标签 |
| 构建产物版本或内容错误 | 删除草稿 Release 和标签，重新构建 |
| 文档站点构建失败 | 阻止合并，修复后重跑 |
| 合并后发现版本错误 | 发布新的修复版本，不覆盖既有标签 |

# Verification

- 合并前：测试、compileall、validate、ci、Python 构建、Debian 包、wheel 隔离安装、
  安装脚本和文档构建全部通过。
- 发布后：从 Release 下载 wheel 和 `.deb`，在干净环境确认 `cabbage --version` 为 `0.2.0`；
  访问 GitHub Pages 确认发布说明可访问。
