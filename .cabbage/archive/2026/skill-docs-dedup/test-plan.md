---
change: skill-docs-dedup
cabbage_stage: tests
---
# Strategy

把"内容只应出现在一个文件"变成可执行断言，而不是靠人工记忆。
每项新增测试都做负向验证，确认还原缺陷后测试会失败。

# Cases

- 退出码条目只出现在 `cli.md`。
- 治理路径 CODEOWNERS 只出现在 `enforcement.md`。
- release 指引存在，被 SKILL.md 链接，且包含四个关键标题。
- 全量测试与文档构建通过，既有七个 skill 结构校验继续通过。

# Evidence

`python -m unittest discover tests` 通过 53 项（新增 3 项）。

负向验证：
- 向 `ownership.md` 追加一行治理路径后，`test_governance_codeowners_block_has_one_copy` 失败。
- 向 `validation.md` 追加一条退出码后，`test_exit_codes_are_documented_in_one_place` 失败。
还原后两项均通过。

修复前事实：命令表 11/11 条与 cli.md 重复；退出码同一句在 SKILL.md 与 validation.md
逐字重复；CODEOWNERS 治理路径存在三个版本，其中 ownership.md 缺少 `**` 通配。
