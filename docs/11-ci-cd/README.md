# CI/CD

`.github/workflows/cabbage.yml` 在 PR 与主分支推送上运行 `validate-and-test`（显示名 `Test & Validate`）。

## 检查和部署

1. 检出完整 Git 历史，安装 Python 依赖。
2. 执行完整 `unittest`，包括指南命令示例与副本一致性检查。
3. 执行 `python -m cabbage_cli validate --all`。
4. PR 上执行 `ci --base origin/<目标分支>`，检查变更绑定与合并门禁。
5. 使用 Node.js 22、pnpm 10、冻结锁文件构建 VitePress 文档。
6. 主分支推送成功后上传构建产物，由 `deploy-pages` 部署到 GitHub Pages。

`ci` 命令本身不运行测试或构建，这些由流水线独立步骤执行。
本仓库根目录的 `cabbage_cli/` 是唯一源码；生成的副本必须与其一致，避免不同入口行为漂移。

## 文档目录规则

- 代码变更需绑定本次差异中存在的活动变更记录。
- 本次差异中的活动变更需通过结构校验和合并门禁。
- 受影响的当前文档目录按项目配置检查。
- 新轻量工作流的 `record_covers: [product, testing]` 表明这两项已在单份记录中承载，不要求重复文档。
- 高风险及其他影响规则不变。本仓库仍使用旧工作流，因此原有目录要求继续生效。

## 本地复现

```bash
python scripts/sync-vendor.py
python -m unittest discover tests
python -m cabbage_cli validate --all
python -m cabbage_cli ci --base origin/master
pnpm --dir docs install --frozen-lockfile
pnpm --dir docs run build
```

CI 根据已提交的 `<base>...HEAD` 计算差异，不包含未提交的修改。

## 仓库保护

管理员需将实际测试检查设为 Required Status Check，并对工作流、配置、工具和 CI 文件要求人工审批。
流水线存在不代表分支保护已经配置。版本标签触发的草稿发布见发布说明。
