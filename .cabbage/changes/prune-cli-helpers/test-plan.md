---
change: prune-cli-helpers
cabbage_stage: tests
---
# Strategy

重构的主要风险是行为漂移，因此不只跑测试套件，还实测三个可观测行为：
未知类型的错误消息、归档写入路径、复选框三种状态的判定。

# Cases

- `cabbage new bogustype x` 输出 `unknown change type: bogustype`。
- `cabbage archive` 写入 `.cabbage/archive/<year>/<id>`。
- `verify` 对未勾选任务返回 2 且报 unchecked 错误。
- `[/]` 与 `[-]` 仍被视为已完成（行为未变）。
- `status`、`validate --all` 等使用 changes_root 的命令正常。
- 新增测试：无函数内 import（豁免 try/except 可选依赖）、无死代码函数。
- 全量测试、validate、CI 自查、文档构建通过。

# Evidence

`python -m unittest discover tests` 通过 59 项（新增 2 项）。

实测行为（临时项目）：
- `cabbage new bogustype x` -> `cabbage: unknown change type: bogustype`
  （改用 core.workflow 后未降级为 `missing file:`）
- `cabbage archive a` -> `archived to .cabbage/archive/2026/a`
- 未勾选任务 -> `implementation: unchecked implementation tasks remain`，退出码 2
- `[/]` 与 `[-]` -> verify 通过（既有行为保持不变）
- `status` 与 `validate --all` 输出正常

负向验证：
- 追加一个无调用者函数后，`test_no_dead_module_level_functions` 失败。
- 在 new_change() 内加入 `import json` 后，`test_no_function_level_imports` 失败。
还原后均通过。

审计过程：逐一核对 core.py 的 39 个符号，确认仅 run() 无调用者；
其余看似"只被测试引用"的符号（如 validate_change 的 verification 参数）
实际经 validate_markdown 向下传递，非死代码。
