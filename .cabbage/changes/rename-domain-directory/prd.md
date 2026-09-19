---
change: rename-domain-directory
cabbage_stage: requirement
---
# Goal

把数据目录从 `04-data` 改名为 `04-domain`，并在目录指南中补充每个目录的用途。

# Scope

改名覆盖代码默认值、CI 规则、本仓库配置、skills 指南与两份站点配置。
重写 `directory-structure.md`，用表格说明用途、sync 目标与门禁规则。
按用户决定不做向后兼容：存量项目需自行迁移配置与目录。
不改变 `data` / `database` 两个影响字段名。

# Acceptance Criteria

- 全仓库无 `04-data` 残留引用（历史变更记录除外）。
- `init` 只创建 `04-domain`，`sync` 的 `database` 阶段写入该目录。
- 目录指南列出全部目录用途，且与代码中的 sync 映射、CI 规则一致。
- 新增契约测试断言指南与代码一致，并可负向验证。
