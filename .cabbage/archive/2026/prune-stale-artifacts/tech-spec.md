---
change: prune-stale-artifacts
cabbage_stage: design
---
# Context

按 find-simplifications 的方法对仓库做只读审计，发现四类候选：死导入、
失真的 TEST_REPORT.md、过期示例、空目录。前两类与第三类有充分证据，空目录属有意设计。

# Design

- 删除导入：`core.py` 的 `dataclass`、`Any`、`shutil`；`cli.py` 的 `os`；`scaffold.py:142` 函数内
  重复的 `import re`（第 5 行已有顶层导入）。
- 删除 `TEST_REPORT.md`：零引用、不在 pyproject 打包范围、不被 CI 或打包脚本读取；
  内容已失真（声称的 `complete` 命令不存在，VuePress 已迁 VitePress，列 15 项而实际 54 项）。
- 删除 `examples/`：三文件零入链，`new-feature.md` 使用新轻量流程中不存在的阶段名。
- 新增 `test_no_unused_imports_in_cli_package`：用 `ast` 解析，跳过 `__init__.py`（重导出）
  与 `__future__` 导入。

# Failure Modes

- 误报未使用导入：`__future__` 与 `__init__` 重导出已排除；属性访问（`os.path`）
  通过 Attribute 基名识别，避免把模块方法调用误判为未使用。
- 误删有用的独有信息：先对比 docs/08-testing/ 的覆盖范围，再把仍有效的信息并入。
- 阶段名回归：既有 `test_documented_verify_stages_exist` 已断言阶段 ID 真实存在，
  不重复实现第二套判定。

# Rollout

纯清理，无行为变更。删除后确认无残留引用（含 VitePress 侧边栏配置）。
