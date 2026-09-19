# 当前状态目录布局

`docs/` 存放**当前状态文档**（系统现在如何工作）。`.cabbage/changes/` 是变更历史，两者不互相复制内容。

## 目录用途

`cabbage init` 会创建下列全部目录，但**只创建有实际内容的目录**才是规范；
空目录保留不影响使用，`validate` 也不会报错。

| 目录 | 用途 | 内容类型 |
| --- | --- | --- |
| `00-overview/` | 项目概览、范围、快速上手 | 手写 |
| `01-product/` | 需求、用户故事、验收标准 | 手写 + `sync` 目标（`requirement`） |
| `02-design/` | 交互与视觉设计、原型说明 | 手写 |
| `03-architecture/` | 系统设计、架构决策、跨切面约束 | 手写 |
| `03-architecture/adr/` | 架构决策记录（不可改写的历史） | 手写 + `sync` 目标（`adr`） |
| `03-architecture/rfc/` | 提案与评审记录（不可改写的历史） | 手写 + `sync` 目标（`rfc`） |
| `03-architecture/system-design/` | 当前系统结构与模块边界 | 手写 + `sync` 目标（`design`） |
| `04-domain/` | 数据模型、数据库设计、迁移与回滚 | 手写 + `sync` 目标（`database`） |
| `05-api/` | 接口契约、事件、集成 | 手写 + `sync` 目标（`api`） |
| `06-development/` | 本地开发环境、构建与调试说明 | 手写 |
| `07-standards/` | 编码规范、评审约定 | 手写 |
| `08-testing/` | 测试策略与用例 | 手写 + `sync` 目标（`tests`） |
| `09-security/` | 威胁模型、权限与合规控制 | 手写 + `sync` 目标（`security`） |
| `10-infrastructure/` | 部署拓扑、容量、环境配置 | 手写 |
| `11-ci-cd/` | 流水线定义与门禁说明 | 手写 |
| `12-release/` | 发布流程与版本策略 | 手写 + `sync` 目标（`release`） |
| `13-operations/` | 运行手册、监控、应急预案 | 手写 |
| `14-performance/` | 性能基线与压测结果 | 手写 |
| `15-incidents/` | 事故记录与复盘（不可改写的历史） | 手写 + `sync` 目标（`incident`、`postmortem`） |
| `16-dependencies/` | 外部依赖清单与升级策略 | 手写 |
| `17-compliance/` | 合规要求与审计证据 | 手写 |

`docs/README.md` 是站点首页；`docs/package.json`、`docs/.vitepress/` 是站点构建配置。

## `sync` 写入的目录

`cabbage sync` 按阶段映射复制已启用且存在的产物，目标固定为 `<目录>/<change-id>.md`：

| 阶段 | 写入 |
| --- | --- |
| `requirement` | `docs/01-product/` |
| `design` | `docs/03-architecture/system-design/` |
| `adr` | `docs/03-architecture/adr/` |
| `rfc` | `docs/03-architecture/rfc/` |
| `api` | `docs/05-api/` |
| `database` | `docs/04-domain/` |
| `security` | `docs/09-security/` |
| `tests` | `docs/08-testing/` |
| `release` | `docs/12-release/` |
| `incident` / `postmortem` | `docs/15-incidents/` |

映射可在项目 `.cabbage/config.yaml` 的 `docs.mapping` 中覆盖，不必与上表一致。
同步文件带 `origin_change` 等 frontmatter，说明它由哪个变更生成，不要手工改写。

## 门禁检查的目录

`ci` 按影响字段检查当前文档是否随代码更新，默认映射：

| 影响字段 | 接受的目录 |
| --- | --- |
| `product` | `docs/01-product/` |
| `architecture` | `docs/03-architecture/` |
| `api` | `docs/05-api/` |
| `database`、`data` | `docs/04-domain/` |
| `security` | `docs/09-security/` |
| `testing` | `docs/08-testing/` |
| `deployment` | `docs/10-infrastructure/`、`docs/11-ci-cd/`、`docs/12-release/` |
| `operations` | `docs/13-operations/` |
| `performance` | `docs/14-performance/` |

规则同样在 `.cabbage/config.yaml` 的 `ci.current_state_rules` 中配置。
新轻量工作流通过 `record_covers` 声明某些影响已由变更记录承载，这些字段不再要求目录改动。

## 放置原则

1. **只创建有内容的目录**，不要为凑齐编号建空目录。
2. **一个事实只放一处**，其他文档链接过去，不复制正文。
3. **当前状态与历史分开**：ADR、RFC、事故记录是不可改写的历史，当前状态文档原处更新。
4. **迁移时修正链接**：移动文件后用 `cabbage validate --all` 确认相对路径仍可解析。

## 与指南的差异

早期版本的本指南列出 `18-management`、`19-ownership`、`20-support`、`21-decisions`、`22-references`
五个目录，但 `cabbage init` 从未创建它们，也不在任何映射中。上表已按实际实现校正。
若需要这些类别，可直接创建目录并在 `docs.mapping` 或 `ci.current_state_rules` 中登记。
