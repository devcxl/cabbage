---
change: fix-simplification-findings
cabbage_stage: tests
change_type: refactor
---

# Strategy

以行为测试为主：每个修复项都有对应的可观察断言；合并后在主分支执行全量回归与
真实链路验证，不依赖单一分支的自测结论。

# Cases

- CLI 输出：status（无 id）/ next / impact 的文本输出可读且无 dict repr；`--json` 结构不变。
- CI 模板：仓库 CI 与生成模板逐字节一致；模板对缺失文件条件跳过；全新项目可经
  vendored CLI 运行 `validate --all`。
- adopt：非 UTF-8 文档迁移不抛异常，文件移动完成，warnings 被报告。
- 默认影响：incident 不再默认 testing、hotfix 不再默认 operations；显式声明仍触发规则。
- skills：7 个同族清单与目录集合一致且不含自身，由契约测试守护。
- 打包：pyproject 动态版本与包内 `__version__` 一致；LICENSE 存在；发布 tag 校验步骤存在。
- 全量：`python -m unittest discover tests`、`validate --all`、`pnpm --dir docs run build`、
  `ci --base origin/master`、`git diff --check`。

# Regression Coverage

- 既有 59 项测试全部保持通过；README 示例命令、vendored 副本一致性、目录映射契约不变。
- 合并后重新运行全部检查，任一分支的局部通过不能替代主分支的完整回归。

# Risks

- 各分支独立通过后仍可能在合并处产生交互问题（同一函数的小范围重叠）；合并后全量回归负责兜底。
- CI 模板的实际行为最终由远端 push 流水线验证；本地只覆盖可离线执行的步骤。
