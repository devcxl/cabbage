---
change: research-and-router-skills
cabbage_stage: implementation
---
# Tasks

- [x] 编写入口 skill `cabbage`：项目识别、选路表、组合编排、边界约束。
- [x] 编写自包含调研 skill `cabbage-research`：启用判据、证据分级、强制纪律、产出与交接。
- [x] 更新既有五个 skill 的同族引用，补调研交接点，清理重复段落。
- [x] 新增路由覆盖契约测试，并通过负向验证确认其有效性。
- [x] 更新 README 与 docs 当前事实描述，修正章节编号。
- [x] 同步 vendored CLI，运行全量测试与文档构建。

# Verification

- `python scripts/sync-vendor.py`：副本已更新。
- `python -m unittest discover tests`：45 项通过。
- `python -m cabbage_cli validate --all`：VALID。
- `python -m cabbage_cli gate research-and-router-skills merge`：ALLOWED。
- `pnpm --dir docs run build`：构建成功。
- `git diff --check`：无空白错误。

未覆盖：未在沙箱外执行真实 `npx skills add`；旧 skill 与新 skill 同时安装时的触发优先级
需实际使用后观察。
