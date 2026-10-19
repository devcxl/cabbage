---
change: prune-cli-helpers
cabbage_stage: design
---
# Context

按 find-simplifications 方法审计 cabbage_cli 全部 1240 行，确认无大块死代码，
但发现四处具体问题：一个完全无调用者的 helper、两处绕过既有封装的路径拼接、
一个未使用变量、一个不可达判定分支。

# Design

- 删除 `core.run()`：全仓库无调用者，`cli.py` 中的 `run` 均为 `subprocess.run` 或
  `pnpm run` 字符串。
- `core.workflow()` 增加存在性检查并抛出 `unknown change type`，使 `scaffold.py` 的
  两处调用不再需要自行判断；`new_change` 改用该函数，错误消息文本保持不变。
  这是关键取舍：直接替换会把友好提示降级为 `missing file:`，因此在被复用处补足语义。
- `core` 新增 `changes_root()` 与 `archive_root()`，消除 `cli.py` 三处硬编码路径；
  9 处 `.cabbage` 字面值收敛为对 `CABBAGE_DIR` 的使用。
- `get_change_tasks_dag` 的 `meta` 改为 `parse_frontmatter(content)[1]`。
- 复选框判定 `x.strip() in {"", " "}` 中的 `""` 不可达（正则至少捕获一个字符），改为
  `== ""`。**不改变** `[/]` 与 `[-]` 的既有判定，行为保持原样。

保留的字面 `.cabbage`：CI 正则（`^\.cabbage/changes/`）与 `exclude_prefixes`，
它们匹配仓库真实路径，跟随常量改名反而会破坏功能。

# Failure Modes

- 错误消息退化：已实测 `new bogustype x` 仍输出 `unknown change type: bogustype`。
- 归档路径错误：实测 `archive` 写入 `.cabbage/archive/2026/<id>`。
- 死代码回归：新增测试断言每个模块级函数都有调用者，负向验证确认可捕获。
- 函数内 import 回归：新增测试，豁免 try/except 内的可选依赖探测。

# Rollout

纯内部重构，无行为变更。`cli.py:54` 的 `try/except ImportError` 内 `import yaml`
是有意的可选依赖探测，予以保留并由测试豁免。
