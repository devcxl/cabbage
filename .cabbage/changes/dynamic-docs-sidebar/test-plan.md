---
change: dynamic-docs-sidebar
cabbage_stage: tests
---
# Strategy

死链无法靠阅读配置发现，只能以构建产物为准：检查渲染后的 HTML 含哪些目录链接，
并对动态逻辑做双向验证，避免"删掉链接"式的假修复。

# Cases

- 构建产物中不含 04-data、05-api、09-security、13-operations 的链接。
- 给 04-data 添加 README 后构建，该链接出现；移除后消失。
- 全新 init 项目（20 空目录）构建成功；首页 href 仅含 /、#工作流全景、#VPContent。
- 全量测试、validate、仓库自身构建通过。

# Evidence

构建产物检查（仓库自身 `docs/.vitepress/dist/index.html`）：
有内容目录 00-overview/01-product/03-architecture/08-testing/11-ci-cd/12-release 各出现 3-4 次；
空目录 04-data/09-security/13-operations/05-api 均出现 0 次。

双向动态验证：给 `docs/04-data/` 添加 README.md 后构建，`/04-data/` 出现 1 次；
移除后重新构建，出现 0 次。

端到端验证：`cabbage init` 生成新项目（20 个空目录），`pnpm run build` 成功；
首页渲染后 href 仅含 `/`、`#工作流全景`、`#VPContent`；
00-overview/01-product/04-data/09-security/13-operations 均未出现在侧边栏。

修复前：侧边栏硬编码 4 个死链，首页 hero 有 1 个指向空目录的按钮。
