---
name: cabbage-adopt
description: Bring an existing project into Cabbage and enforce its gates - initialize without disturbing content, inventory and classify existing documentation, migrate current-state docs, import ADRs and incidents as immutable history, then enable branch protection, required status checks, and CODEOWNERS restrictions. Use when onboarding a repository that already has documentation or when setting up CI enforcement.
---

# 存量项目接入与强制执行

`cabbage init` 假设全新项目。已有文档的仓库走 `adopt` 流程：**CLI 只盘点，人和 Agent 决定并移动文件。**

## 接入前先看

```bash
cabbage init           # 只新增 .cabbage/、docs/ 骨架与 CI 模板，不改写已有文件
cabbage adopt          # 扫描 docs/ 树之外的 Markdown，写 .cabbage/adoption-report.md
cabbage adopt --json   # 结构化输出，便于脚本处理
```

`adopt` **不会移动任何文件**。若仓库已有 `docs/` 且内容不同，先逐个确认脚手架文件再接受。

## 分类与决策

每份文档得到四种动作之一：

| 动作 | 含义 | 处理 |
| --- | --- | --- |
| `keep` | 已在标准编号目录内 | 无需操作 |
| `migrate` | 当前状态文档 | 移入标准目录并修正链接 |
| `import` | 历史记录（ADR/RFC/事故） | 原样归档，**不改写内容** |
| `review` | 无法归类 | 由文档负责人人工判断 |

分类基于目录名和文件名推断（如 `adr/` → ADR、`runbooks/` → operations），
**始终需要人工确认**，不要直接批量 `--apply`。
逐行处理 `review`，确认后再执行 `cabbage adopt --apply`。

## 迁移要点

1. 用 `git mv` 保留历史，一个逻辑批次一个提交，便于评审。
2. 移动后立即修正相对链接；链接必须从新位置能解析。
3. 只创建有实际内容的目录，不要为了凑齐编号建空目录。
4. 每批之后执行 `cabbage docs build` 确认站点仍可构建。
5. 不把内容改写成 `final-v2.md` 风格，保持稳定路径。

历史记录（ADR/RFC/事故）导入后**不重写、不合并、不"现代化"措辞**；
新决策显式取代旧决策，旧记录保留可见。详见 [接入流程](references/adoption.md)。

## 基线变更记录

迁移本身也要可审计：

```bash
cabbage new feature adopt-existing-docs
# 填写记录并验证
cabbage validate adopt-existing-docs
cabbage docs build
```

合并后才启用强制检查。

## 启用强制执行

**关键前提：CI 通过不等于门禁被强制。** 托管平台必须配置保护，否则 Agent 或人都能绕过。

1. **分支保护**：禁止直接推送到默认分支；把 Cabbage 的 CI job 设为必需状态检查；
   对修改核心配置的 PR 要求人工审批。
2. **CODEOWNERS**：为治理路径指定负责人。

   ```text
   /.cabbage/config.yaml     @tech-lead
   /.cabbage/workflows/**    @tech-lead
   /.cabbage/tooling/**      @tech-lead
   /.github/workflows/cabbage.yml @tech-lead
   ```

3. **状态文件保护**：`.cabbage/changes/*/state.json` 由 CLI 生成，禁止手工编辑。

仓库自带的 CI 模板（`cabbage init` 写入 `.github/workflows/cabbage.yml`）依次执行：
单元测试、`validate --all`、PR 差异检查 `ci --base`、文档构建，主分支推送后再部署 Pages。

## 威胁模型

对拥有提交权限的 Agent，需要防住三类行为：

- 绕过门禁：直接改 `state.json` 而不运行 `verify`。
- 削弱策略：修改或删除 CI、工作流、配置让失败的 PR 通过。
- 无记录交付：改代码但不关联已验证的变更记录。

对策是上述分支保护、CODEOWNERS 与必需状态检查，而不是靠自觉。
细节见 [强制执行配置](references/enforcement.md)。

## 接入完成的判据

重新执行 `cabbage adopt` 后应当**全部报告 `keep`**；出现其他动作说明存在漂移。

## 同族 skill

- `cabbage-change`：变更流程、门禁与验证。
- `cabbage-docs`：目录归属、命名、链接与站点构建。
- `cabbage-decision`：ADR/RFC 内容标准。
- `cabbage-incident`：事故记录与复盘。

这些 skill 各自独立安装，不假设相对路径存在。
