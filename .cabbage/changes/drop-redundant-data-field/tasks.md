---
change: drop-redundant-data-field
cabbage_stage: implementation
---
# Tasks

- [x] 从 IMPACT_FIELDS、CI 规则、模板、同步标签中移除 data 影响字段。
- [x] 同步清理本仓库 config 的字段与规则。
- [x] 保留并验证 adopt 的同名分类键与目标映射。
- [x] 修复硬编码区域名的测试，改为从 IMPACT_FIELDS 派生。
- [x] 新增 adopt 分类目标完整性测试并完成负向验证。
- [x] 实测确认已有变更记录与新项目均不受影响。
- [x] 同步 vendored CLI，运行全量测试与文档构建。

# Verification

- `python -m unittest discover tests`：57 项通过。
- `python -m cabbage_cli validate --all`：VALID（含 12 个含 data 键的历史变更）。
- `pnpm --dir docs run build`：构建成功。
- `python scripts/sync-vendor.py`：副本已同步。
- `git diff --check`：无空白错误。
- 命令行拒绝 `data=true`；新项目与模板均不含该字段。

未覆盖：未检查 3 个存量项目是否有脚本仍传 `data=true`；若有会立即报错，属刻意的破坏性变更。
