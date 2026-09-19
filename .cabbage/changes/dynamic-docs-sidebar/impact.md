---
change: dynamic-docs-sidebar
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Detail |
| --- | --- | --- |
| Product | Yes | 站点导航不再指向空白页；首次访问不再遇到 404。 |
| Testing | Yes | 以构建产物断言替代人工点击检查，并做双向动态验证。 |
| Architecture | No | 仅改站点配置与首页资产，CLI 逻辑与目录创建行为不变。 |
| API | No | 无接口变化。 |
| Database | No | 无持久化结构变更。 |
| Security | No | 不改变权限边界。 |
| Deployment | No | 流水线步骤不变，构建仍由同一命令完成。 |

# Risks

动态生成依赖构建时文件系统状态：若 CI 缓存导致文件缺失，侧边栏会少条目而不是报错，
属可接受的降级。不删除空目录是刻意决定，避免与 CLI 的 ALL_CONFORMING_DIRS 设计冲突，
也避免下次 init 重建。
