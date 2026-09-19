---
name: cabbage-docs
description: Write and organize long-lived project documentation in a Cabbage repository - place documents in the numbered docs tree, apply naming conventions, keep relative links and anchors valid, draw Mermaid diagrams, assign ownership, and preview or build the VitePress site. Use when authoring or moving current-state docs, fixing broken links, or running the documentation site.
---

# 文档写作与站点

面向长期存在的**当前状态文档**。变更流程与门禁由 `cabbage-change` 负责。

## 目录归属

文档写入 `docs/` 下的编号目录，只创建有实际内容的目录：

| 目录 | 内容 |
| --- | --- |
| `00-overview/` | 项目概览、范围、快速上手 |
| `01-product/` | 需求、用户故事、验收标准 |
| `02-design/` | 交互与视觉设计、原型说明 |
| `03-architecture/` | 系统设计、`adr/`、`rfc/` |
| `04-domain/` | 数据模型、数据库设计、迁移与回滚 |
| `05-api/` | 接口契约、事件、集成 |
| `06-development/` | 本地开发环境、构建与调试 |
| `07-standards/` | 编码规范、评审约定 |
| `08-testing/` | 测试策略与用例 |
| `09-security/` | 威胁模型、权限与合规控制 |
| `10-infrastructure/` | 部署拓扑、容量、环境配置 |
| `11-ci-cd/` | 流水线定义与门禁说明 |
| `12-release/` | 发布流程与版本策略 |
| `13-operations/` | 运行手册、监控、应急预案 |
| `14-performance/` | 性能基线与压测结果 |
| `15-incidents/` | 事故记录与复盘（不可改写的历史） |
| `16-dependencies/` | 外部依赖清单与升级策略 |
| `17-compliance/` | 合规要求与审计证据 |

其中 `01-product`、`03-architecture`（含 `adr`、`rfc`、`system-design`）、`04-domain`、`05-api`、
`08-testing`、`09-security`、`12-release`、`15-incidents` 同时是 `cabbage sync` 的写入目标；
`10-infrastructure`、`11-ci-cd`、`12-release` 是 `deployment` 影响可接受的目录。
完整映射与判定规则见 [目录布局](references/directory-structure.md)。
`.cabbage/changes/` 是变更历史，`docs/` 是当前状态，两者不互相复制内容。

## 写作原则

1. **单一事实来源**：一个事实只在一处定义，其他文档链接过去，不复制正文。
2. **当前状态 vs 决策历史**：当前状态文档原处更新；ADR/RFC/事故记录是不可改写的历史。
3. **稳定路径**：不使用 `spec-v2-final.md`、`_latest.md`、`_copy.md` 这类文件名，版本交给 Git。
4. **相对链接**：仓内链接一律用相对路径并带 `.md`，不写 `/docs/...` 绝对路径。
5. **不写占位内容**：`TODO`、`TBD`、`FIXME` 会导致验证失败。

命名、链接与反模式细节见
[命名规范](references/naming-conventions.md) 与 [链接规则](references/linking-rules.md)。

## 图表

仓库使用 Mermaid，写在 ```` ```mermaid ```` 围栏内。常用类型：流程图、时序图、状态图、ER 图。
围栏必须闭合，否则 `validate` 与站点构建都会失败。模板见 [图表指南](references/diagrams.md)。

图表只画难以用文字表达的关系；不要把流程描述强行画成图。

## 校验与构建

```bash
cabbage validate --all        # 结构和链接检查（不需要先建变更）
cabbage docs install          # 安装站点依赖
cabbage docs dev              # 本地预览
cabbage docs build            # 静态构建
```

`validate` 检查文件存在、标题锚点、相对路径是否越出项目根、Mermaid 围栏与图表类型。
它不是完整语义检查，站点构建也需单独执行。

站点配置、Mermaid 集成与构建排错见 [文档站点](references/documentation-site.md)。

## 归属与评审

关键长期文档应在 frontmatter 声明维护方：

```yaml
---
owner: team-billing
maintained-by: ["@alice"]
last-reviewed: 2026-03-01
---
```

用 `.github/CODEOWNERS` 让架构、安全等目录的改动必须由对应负责人评审。
细节见 [维护归属](references/ownership.md)。

**注意**：该 frontmatter 是约定，CLI 不校验也不强制；真正的强制来自代码托管平台的分支保护。

## 常见问题

| 现象 | 处理 |
| --- | --- |
| `broken link` | 修正相对路径层级或锚点 slug；确认目标文件存在 |
| 链接越出项目根 | 改用仓内相对路径，不要指向仓库外的文件 |
| `docs build` 失败 | 先 `cabbage validate --all` 定位死链，再检查围栏闭合与 HTML 标签 |
| 站点依赖缺失 | 重新执行 `cabbage docs install` |

## 同族 skill

- `cabbage`：总入口，选路与组合编排。
- `cabbage-change`：变更流程、门禁与验证。
- `cabbage-research`：技术选型与方案调研。
- `cabbage-decision`：ADR/RFC 内容标准。
- `cabbage-docs`：目录归属、命名、链接与站点构建。

各自独立安装，不假设相对路径或其他 skill 已存在。
