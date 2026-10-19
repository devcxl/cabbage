---
change: dynamic-docs-sidebar
cabbage_stage: requirement
---
# Goal

消除文档站点中指向空目录的死链，并让侧边栏与首页按钮随实际内容变化。

# Scope

把 VitePress 侧边栏与导航改为按目录是否含 index 页动态生成，同时应用于仓库自身与分发资产。
修正资产首页中指向尚未创建目录的按钮。不改 CLI 行为，不删除空目录。

# Acceptance Criteria

- 构建产物中不出现指向无 index 目录的链接。
- 给任一空目录添加 README 后，该目录自动出现在侧边栏与导航。
- 全新 init 项目（20 个空目录）构建成功且首页无死链。
- 全量测试、validate、文档构建通过。
