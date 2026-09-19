---
change: rename-domain-directory
cabbage_stage: implementation
---
# Tasks

- [x] 改名 9 个文件的 13 处引用，并重命名实际目录。
- [x] 补充 adopt 的 domain/domains 分类关键词。
- [x] 重写目录指南为用途表 + sync 映射表 + 门禁规则表 + 放置原则。
- [x] 更新 cabbage-docs 的目录表，补全 10/11/12 与 02-design。
- [x] 新增两条契约测试并完成负向验证。
- [x] 端到端验证：新项目 init 只创建 04-domain，sync 写入该目录。
- [x] 同步 vendored CLI，运行全量测试与文档构建。

# Verification

- `python -m unittest discover tests`：56 项通过。
- `python -m cabbage_cli validate --all`：VALID。
- `pnpm --dir docs run build`：构建成功。
- `python scripts/sync-vendor.py`：副本已同步。
- `git diff --check`：无空白错误。
- 全仓库搜索：无 `04-data` 残留（历史变更记录除外）。

未覆盖：3 个存量项目（LaseAI、fcitx5-voice-input、trading-web3-ai）的迁移未执行，
需手动改 config 与目录；本次不引入兼容分支是既定选择。
`docs/04-domain/` 为空目录，git 不跟踪，改名在版本库中无 diff。
