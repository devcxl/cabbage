---
change: skill-docs-dedup
cabbage_stage: implementation
---
# Tasks

- [x] 新增 release-plan 编写指引并链接到 deployment 影响说明。
- [x] 收敛退出码到 cli.md，删除 SKILL.md 与 validation.md 的重复。
- [x] 删除 SKILL.md 与 cli.md 重复的命令表，改为指向 cli.md。
- [x] 统一 CODEOWNERS 治理路径至 enforcement.md 单一位置。
- [x] 新增三项契约测试并完成负向验证。
- [x] 同步 vendored CLI，运行全量测试与文档构建。

# Verification

- `python -m unittest discover tests`：53 项通过。
- `python -m cabbage_cli validate --all`：VALID。
- `pnpm --dir docs run build`：构建成功。
- `git diff --check`：无空白错误。
- `cabbage-change/SKILL.md`：164 行（原 173），命令表已改为指向 cli.md。

未覆盖：release 指引的实际有效性需在真实发布变更中检验；本次仅验证结构与链接。
