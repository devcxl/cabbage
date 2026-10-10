---
change: prune-dead-remnants
cabbage_stage: impact
change_type: refactor
---

# Impact Matrix

| Area | Impact | Notes |
|---|---|---|
| Product | No | 命令、参数与输出不变；顺带修正 docs/01-product/README.md 中 `data` 影响字段的失真引用。 |
| Architecture | No | 模块边界与依赖方向不变；顺带修正 docs/03-architecture/README.md 的影响字段计数。 |
| API | No | CLI 人类输出与 `--json` 输出均未改变。 |
| Database | No | `state.json`、`change.yaml` 等持久化格式不变。 |
| Security | No | 不改变输入信任模型与权限边界。 |
| Testing | No | 仅删除测试死导入、收敛重复 helper；测试验证的行为不变，当前测试文档无需更新。 |
| Deployment | No | 不改变流水线；仅修正 install.sh 的提示文案。 |
| Operations | No | 无运维影响。 |
| Performance | No | 无性能影响。 |

# Risks

- 误删被依赖的代码：`completed_ids.update({...})` 的四个值都能被下游 `d.lower() in {"none","preparation",""}` 覆盖，删除不改变 ready/blocked 判定；由 test_tasks_dag 的既有断言与全量回归覆盖。
- `init_project` 恒真条件删除后行为一致：早退 raise 保证执行到写入时只可能是「config 不存在」或 `force=True`；由 test_lightweight_workflows 与 test_cabbage_rename 的初始化用例覆盖。
- 通配导入改显式导入若遗漏符号会立即在测试中失败；`test_no_unused_imports_in_cli_package` 从此开始覆盖 cli.py，防止再次引入未用导入。
