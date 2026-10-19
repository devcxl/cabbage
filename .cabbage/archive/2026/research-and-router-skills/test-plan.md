---
change: research-and-router-skills
cabbage_stage: tests
---
# Strategy

用契约测试保证路由表与磁盘上的 skill 集合一致，并对该测试做负向验证，确认它真的能捕获遗漏。
其余沿用既有全量测试与文档构建，保证 CLI 行为未变。

# Cases

- 入口选路表覆盖全部同族 skill，且不指向不存在的 skill。
- 负向验证：从选路表删除一行后测试必须失败。
- 七个 skill 均通过结构校验，frontmatter 与 description 有效。
- 各 skill 内部相对链接在独立安装后可解析。
- `README.md` 与全部 skill 文档中的 `cabbage verify` 阶段 ID 真实存在。
- 全量单元测试与 VitePress 构建通过。

# Evidence

`python -m unittest discover tests` 通过 45 项。七个 skill 均通过结构校验。
新增路由测试做了负向验证：从选路表删除 `cabbage-research` 行后测试失败并指明
`routing table must name every sibling skill exactly once`，还原后通过。
初次实现负向验证未生效（测试仅检查 skill 名是否出现，组合表也含该名称），
已收紧为解析选路表并做集合相等比较。
