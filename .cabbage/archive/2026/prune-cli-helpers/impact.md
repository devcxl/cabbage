---
change: prune-cli-helpers
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Notes |
|---|---|---|
| Product | Yes | 路径拼接收敛到单一实现，未知变更类型的报错得到保留并在所有入口一致。 |
| Architecture | No | 模块划分不变，仅消除重复实现。 |
| API | No | 命令、参数与退出码均未改变；错误消息文本保持兼容。 |
| Database | No | 无持久化结构变更。 |
| Security | No | 不改变权限边界。 |
| Testing | Yes | 新增两条契约测试，断言无函数内 import 与无死代码函数。 |
| Deployment | No | 流水线不变。 |
| Operations | No | 无运维影响。 |
| Performance | No | 无性能影响。 |

# Risks

`core.workflow()` 增加存在性检查后，所有调用方的报错从 `missing file:` 变为
`unknown change type:`，这是**错误质量提升**而非退化；已实测确认 `cabbage new bogustype x`
仍输出友好提示。CI 正则与 `exclude_prefixes` 中的 `.cabbage` 必须保持字面值，
因为要匹配仓库真实路径，不能改为跟随常量；已在实现中明确保留。
