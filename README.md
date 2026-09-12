# Cabbage

**小变更一份记录，高风险才增加专项文档。**

面向 AI Agent 和软件团队的本地文档与变更管理 CLI。使用 Markdown、Git、内容指纹和 CI 门禁，
不要求每个任务都编写 PRD、技术方案、测试计划和 DAG。

[在线文档](https://devcxl.github.io/cabbage/) · [CI 与部署](https://github.com/devcxl/cabbage/actions/workflows/cabbage.yml)

## 安装

需要 Python 3.10+ 和 PyYAML；文档站点使用 VitePress，构建需要 Node.js 和 pnpm。
本项目不发布至公共 PyPI。

### Linux / macOS

安装脚本创建独立虚拟环境并链接到 `~/.local/bin/cabbage`，无需 root：

```bash
curl -fsSL https://raw.githubusercontent.com/devcxl/cabbage/master/scripts/install.sh | bash
```

卸载：

```bash
curl -fsSL https://raw.githubusercontent.com/devcxl/cabbage/master/scripts/install.sh | bash -s -- --uninstall
```

### 系统包

Arch Linux：在 `packaging/aur` 执行 `makepkg -si`，或使用 `yay -S cabbage-git`。
Debian / Ubuntu：从 [Releases](https://github.com/devcxl/cabbage/releases) 下载 `.deb`，
执行 `sudo dpkg -i cabbage_*_all.deb`；缺少依赖时执行 `sudo apt-get install -f`。

## 快速开始：小变更

以下适用于**新初始化项目**。普通 `feature / bugfix / refactor` 默认只需一份 `tasks.md`：
目标或问题、改动方案、任务、实际验证结果。

```bash
cabbage init
cabbage new bugfix fix-label
# 填写 .cabbage/changes/fix-label/tasks.md 的 Goal 和 Design
cabbage gate fix-label implementation
# 复现失败 → 最小修复 → 回归测试；完成 Tasks 并填写 Verification 实际结果
cabbage verify fix-label implementation
cabbage gate fix-label merge
# 提交后，在 PR/CI 中检查（替换为实际基线分支）
cabbage ci --base origin/main
# 确认合并后再归档
cabbage archive fix-label
```

无需额外 PRD、测试计划、DAG 或多方案对比。`change.yaml` 和 `state.json` 是 CLI 管理的元数据，
“一份记录”指一份人工填写的 Markdown。归档保留该记录，不重复复制到产品和测试目录。

## 高风险才展开

在实现前声明实际影响。例如下面是一个独立的 API 变更：

```bash
cabbage new feature update-api
cabbage impact update-api --set api=true
# 填写 tasks.md 的目标与方案，以及新生成的 api-design.md
cabbage verify update-api api
cabbage gate update-api implementation
# 完成代码与测试，填写 tasks.md 实际结果后
cabbage verify update-api implementation
cabbage gate update-api merge
cabbage sync update-api
```

| 影响标记 | 增加的文档 | 实现前阶段 |
| --- | --- | --- |
| `architecture=true` | `adr.md` | `adr` |
| `api=true` | `api-design.md` | `api` |
| `database=true` | `database-design.md` | `database` |
| `security=true` | `security-review.md` | `security` |
| `deployment=true` | `release-plan.md` | `release` |

标记可组合。`deployment=true` 表示需要专项部署/回滚方案的发布，不是每次普通合并。
专项方案在实现前验证，实际测试和发布验证结果记在 `tasks.md`。
风险由人或 Agent 声明，CLI 不会从代码自动推断。高风险影响的 CI 当前文档目录规则继续生效；
已有当前文档失真时仍应修正，不应为凑文件数保留错误信息。

`architecture / migration / integration / hotfix / incident` 的独立专项工作流继续保留。

## 既有项目兼容

**既有 `.cabbage/workflows/`、配置和状态不自动迁移，本仓库也保留原工作流。**
升级 CLI 后，使用 `cabbage status <id>`、`cabbage next <id>` 查看实际阶段。
旧工作流中的 `requirement / impact / design / tests / implementation` 仍受支持；
不要把新项目示例直接套用到旧流程，不要使用 `init --force` 升级 CLI，它会覆盖配置与工作流。

本仓库唯一 CLI 源码是 `cabbage_cli/`。执行 `python scripts/sync-vendor.py` 生成
`.cabbage/tooling/cabbage_cli/`；完整测试与 CI 检查文件一致性，避免手工维护两份代码。

## 能力与边界

- `verify`：检查结构、占位符、清单、链接和 Mermaid 围栏，记录内容指纹。
- `status / next / gate`：显示状态、就绪阶段与门禁；验证后内容或依赖变化会使阶段 `stale`。
- `validate`：检查草稿结构与链接，不要求所有任务已经完成。
- `sync`：复制有映射的文档，不做语义合并，也不检查阶段验证状态；发布前先通过 `gate merge`。
- `archive`：先检查门禁，再同步和移动到 `.cabbage/archive/`；不检查 Git 合并状态。
- `ci`：检查提交差异中的变更绑定、门禁及适用的当前文档规则；不自行构建站点。
- `adopt`：盘点已有文档，确认迁移建议后再用 `--apply`。
- `docs dev / build`：预览和构建 VitePress 站点。
- `tasks --export-dag`：可选的任务派发数据导出，不执行任务，不是小变更的前置要求。

内容指纹不是身份签名，也不证明文档语义正确或记录不可篡改。
应在托管平台配置必要的分支保护、人工审批和策略文件所有权。

详细操作见 `skills/` 下的七个 skill。入口是 `cabbage`（选路与组合编排），
其余按任务类型选择：`cabbage-change`（变更流程与门禁）、`cabbage-research`（调研与选型）、
`cabbage-decision`（ADR/RFC）、`cabbage-incident`（事故复盘）、`cabbage-docs`（写作与站点）、
`cabbage-adopt`（存量接入与强制执行）。

## 验证

```bash
python scripts/sync-vendor.py
python -m unittest discover tests
python -m cabbage_cli validate --all
pnpm --dir docs run build
git diff --check
```

## License

MIT © devcxl
