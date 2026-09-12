---
name: cabbage
description: Entry point for Cabbage-based documentation and change management - decide which cabbage skill applies, and how to combine them for multi-step work such as research into a decision, an incident into follow-up changes, or adopting an existing repository. Use at the start of any task in a repository containing a .cabbage directory, or when unsure which cabbage skill to load.
---

# Cabbage 总入口

本 skill 只做**选路与编排**，不描述具体流程。确定目标 skill 后加载它，按其中的步骤执行。

## 1. 是否是 Cabbage 项目

```bash
test -d .cabbage && echo "cabbage project"
```

- 没有 `.cabbage/`：本族 skill 不适用。不要为一次性任务执行 `cabbage init`；
  只有用户明确要求接入时才加载 `cabbage-adopt`。
- 有 `.cabbage/`：读取 `.cabbage/config.yaml` 确认真实配置，继续第 2 步。

项目已有工作流时不要执行 `cabbage init`，也不要用 `init --force` 升级，它会覆盖配置与工作流。

## 2. 选路

| 任务 | 加载 |
| --- | --- |
| 改代码、修 bug、重构、新增功能 | `cabbage-change` |
| 技术选型、方案评估、开源项目成熟度、PoC | `cabbage-research` |
| 写 ADR / RFC、记录架构决策 | `cabbage-decision` |
| 线上故障、写事故报告与复盘 | `cabbage-incident` |
| 整理文档、修链接、目录归属、建站点 | `cabbage-docs` |
| 接入存量项目、配分支保护与 CI 强制 | `cabbage-adopt` |

一次只加载一个 skill。目标不明确时先读 `.cabbage/config.yaml` 与
`.cabbage/status`（`cabbage status`）确认真实状态，再决定。

**含代码改动就一定先从 `cabbage-change` 开始**，其他 skill 在其流程内部按需加载。

## 3. 组合

多步任务的顺序与交接点如下。只按顺序加载，不要一次加载全部。

| 场景 | 顺序与交接点 |
| --- | --- |
| 调研后落地 | `cabbage-research` → 结论需要长期保留时 `cabbage-decision` → 开始改代码时 `cabbage-change` |
| 事故后需架构调整 | `cabbage-incident`（先复盘定性）→ 需要重新选型才 `cabbage-research` → `cabbage-decision` → `cabbage-change` |
| 存量项目接入后的首个变更 | `cabbage-adopt`（迁移与基线）→ `cabbage-change` |
| 高风险变更且要改文档 | `cabbage-change` 管流程，`cabbage-docs` 管内容与站点 |
| 紧急故障止血 | `cabbage-incident` 说明为何先用 `hotfix`，事后再补 `incident` 记录 |

交接原则：

- 前一个 skill 的产物是后一个的输入，不要跳过中间环节；
- 调研与复盘本身**不建变更记录**，需要落地代码时由 `cabbage-change` 创建；
- 交接时把已确认的事实、被否决的方案和未决问题一并带入，不要重新调研。

## 4. 与 CLI 的关系

各 skill 用同一套 CLI，阶段真相始终来自项目内的工作流文件：

```bash
cabbage status                 # 列出活动变更
cabbage next <change-id>       # 当前可做与被阻塞的阶段
cabbage --version              # 确认版本，便于排查行为差异
```

不要凭记忆套用阶段 ID；`.cabbage/workflows/<type>.yaml` 与 `next` 才是依据。

## 5. 安装与旧版本冲突

本族 skill 替代旧的单文件 `project-docs-management` skill。两者同时安装会重复触发，
安装后应先卸载旧版：

```bash
npx skills remove project-docs-management   # 具体命令以你所用的安装器为准
npx skills add <本仓库地址>/skills/cabbage
```

至少安装入口 `cabbage` 与其路由到的目标 skill；其余按需安装。
入口自包含选路表，但具体流程在目标 skill 中，缺少目标 skill 时无法完成对应任务。

## 6. 边界

本 skill 不包含：变更门禁细节、文档写作规范、证据分级方法、迁移步骤——
这些分别属于上面路由到的 skill。若发现某个任务在本表找不到落点，
先确认是否属于 Cabbage 的职责范围，而不是把新流程塞进本文件。

## 同族 skill

`cabbage-change`、`cabbage-research`、`cabbage-decision`、`cabbage-incident`、
`cabbage-docs`、`cabbage-adopt`。

各自独立安装，不假设相对路径或其他 skill 已存在。
