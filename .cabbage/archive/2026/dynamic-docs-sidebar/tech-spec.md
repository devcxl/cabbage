---
change: dynamic-docs-sidebar
cabbage_stage: design
---
# Context

`cabbage init` 无条件创建 20 个标准目录，新项目绝大多数为空。侧边栏此前硬编码
9 个链接，其中 4 个（04-data、05-api、09-security、13-operations）在新项目中无页面，
构成死链。仓库自身也受同样影响。首页 hero 按钮同样指向可能为空的目录。

# Design

侧边栏与导航改为在配置加载时读取文件系统：`hasPage(dir)` 判断该目录是否存在
`README.md`（rewrites 会将其映射为 index.md）。分组仍保留全部候选目录，
但只渲染实际有页面的条目；分组为空时整组隐藏。

首页 hero 按钮改为指向同页锚点 `#工作流全景`，不依赖尚未创建的文档。
资产首页与仓库首页在此处有意不同：仓库的 00-overview 与 03-architecture 都有内容，
保留其跳转；资产首页面向新项目，改用锚点。

# Failure Modes

- 构建时文件缺失导致条目消失：降级为少显示一项，不产生死链。
- 两处 config 与首页漂移：两者都在测试与构建覆盖范围内，
  vendored 副本一致性由既有契约测试保证。
- 新增内容后忘记更新侧边栏：动态生成后不需要人工维护，加 README 即出现。

# Rollout

同时更新仓库配置与分发资产。已用全新 init 项目验证：20 个空目录下构建成功、
首页无死链；再给空目录加 README 后该目录自动出现。
