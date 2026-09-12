---
change: skill-docs-dedup
cabbage_stage: design
---
# Context

`deployment=true` 只激活一个 release 阶段，但全部 skill 中相关指导仅两行，模板虽有九个标题
却无编写标准。同时 SKILL.md 的命令表与 `cli.md` 完全重复，退出码说明在 `SKILL.md` 与
`validation.md` 逐字重复，CODEOWNERS 治理路径在两个 skill 中出现三个不一致版本。
这些重复正是此前反复出现的指南漂移来源。

# Design

- 新增 `skills/cabbage-change/references/release-plan.md`：由 SKILL.md 按需链接，
  不进入常驻内容。内容覆盖何时声明 deployment、可勾选前置条件、带成功信号的步骤表、
  可测回滚触发条件与数据处置、上线后验证、观察窗口与沟通边界。
- 退出码与完整命令收敛到 `cli.md`；`SKILL.md` 只保留流程示例与 `next` 提示，
  `validation.md` 改为链接引用。
- CODEOWNERS 治理路径只保留在 `cabbage-adopt/references/enforcement.md`；
  `ownership.md` 只保留文档评审路径并注明权威位置。

# Failure Modes

- 指引膨胀：控制在按需加载的 reference 内，SKILL.md 不增加常驻体积。
- 再次漂移：三项各加一条契约测试，断言内容的唯一归属文件。
- 跨 skill 引用失效：`ownership.md` 用 skill 名而非相对路径指明位置，符合既有约定。

# Rollout

仅新增与修改说明文件与测试。不改 CLI，不改工作流，用户无需重新安装以外的操作。
