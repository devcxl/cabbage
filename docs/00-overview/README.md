# 项目概览

Cabbage 是本地文档与变更管理 CLI：**小变更一份记录，高风险才增加专项文档。**

## 新项目的最短路径

```bash
cabbage init
cabbage new bugfix fix-label
# 填写 tasks.md 的目标、方案，确认没有需要声明的专项风险
cabbage gate fix-label implementation
# 复现、修复、测试后，完成任务并写入实际验证结果
cabbage verify fix-label implementation
cabbage gate fix-label merge
# 提交后执行 CI；确认合并后归档
cabbage archive fix-label
```

新初始化项目的 `feature / bugfix / refactor` 只需一份人工填写的 `tasks.md`。
`change.yaml` 和 `state.json` 由 CLI 管理。不强制额外 PRD、测试计划、DAG 或多方案比较。

## 按风险展开

实现前用 `impact --set` 声明架构、外部 API、数据库、安全或高风险发布影响，
工具分别增加 ADR、API、数据库、安全和发布方案。相关阶段验证通过后才允许实现。
风险由使用者判断，不会从代码自动识别。已有文档失真时仍需修正。

`architecture / migration / integration / hotfix / incident` 保留专项流程。

## 旧项目保持原样

既有项目的 `.cabbage/workflows/`、配置、历史与验证状态不会自动迁移。本仓库也保留旧流程。
使用 `cabbage status` / `cabbage next <id>` 查看实际阶段，不将新项目示例直接套用到旧项目。
不要使用 `init --force` 升级 CLI，它会覆盖项目配置与工作流。

## 文档与技术边界

变更记录描述单次改动，当前文档描述系统现在的行为，历史决策保留背景和取舍。
`sync` 只复制有映射的文件，不做语义整合或验证状态检查；发布前先通过合并门禁。
轻量记录归档到 `.cabbage/archive/`，不额外复制到产品和测试目录。

运行时为 Python 3.10+、PyYAML；站点为 VitePress、Mermaid；CI 使用 GitHub Actions。
唯一 CLI 源码在 `cabbage_cli/`，`python scripts/sync-vendor.py` 生成仓库副本，测试检查一致性。

内容指纹用于识别验证后的变化，不证明文档质量、审批身份或记录不可篡改。
