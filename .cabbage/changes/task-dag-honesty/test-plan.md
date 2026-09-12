---
change: task-dag-honesty
cabbage_stage: tests
---
# Strategy

先复现误导输出，再修实现。回归测试调用真实的 `cmd_tasks` 而非复制守卫逻辑，
避免测试与实现各写一份判断而同时出错。

# Cases

- 普通清单：`structured` 为假，派发计划为空，无 Mermaid。
- 结构化分节：`structured` 为真，字段照常解析。
- `--export-dag` 对普通清单报错；对结构化任务通过。
- 还原 `--export-dag` 守卫后，对应用例必须失败。

# Evidence

`python -m unittest discover tests` 通过 50 项（新增 4 项针对本修复）。
负向验证：临时移除 `--export-dag` 守卫后，
`test_export_dag_refuses_plain_checklist` 以
`AssertionError: unexpectedly None : plain checklists must not produce a dispatch plan` 失败；
还原后通过。修复前 `tasks --export-dag` 对普通清单输出
`verification: "N/A"`、`sop: []` 的派发提示，属已复现的误导行为。
