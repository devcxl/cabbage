---
change: split-skills
cabbage_stage: implementation
---
# Tasks

- [x] 建立 `skills/` 骨架，把 13 篇 references 归入对应 skill，删除重复副本。
- [x] 编写 `cabbage-change`（流程主入口）并新增 `references/document-types.md`。
- [x] 编写 `cabbage-decision`、`cabbage-incident`、`cabbage-docs`、`cabbage-adopt`。
- [x] 修正 `lifecycle.md` 中与新轻量流程矛盾的阶段名断言。
- [x] 移除根 `SKILL.md` 与 `references/`，更新 README 与 CLI 输出提示。
- [x] 重写契约测试：扫描 `skills/`，校验 frontmatter、description、相对链接与阶段 ID。
- [x] 独立安装模拟验证 `cabbage-change` 自包含。
- [x] 同步 vendored CLI，运行全量测试与文档构建。
- [x] 补充专项工作流对照表，保留原 decision-tree 中对特殊类型与旧项目的说明。

# Verification

- `python scripts/sync-vendor.py`：副本已更新。
- `python -m unittest discover tests`：43 项通过。
- `python -m cabbage_cli validate --all`：VALID。
- `python -m cabbage_cli gate split-skills merge`：ALLOWED。
- `pnpm --dir docs run build`：构建成功（仍有既存的 chunk 体积提示）。
- `git diff --check`：无空白错误。

未覆盖：未在沙箱外执行真实 `npx skills add` 安装，仅以临时目录复制模拟独立安装；
多个 skill 同时安装后的触发优先级需实际使用后观察。
