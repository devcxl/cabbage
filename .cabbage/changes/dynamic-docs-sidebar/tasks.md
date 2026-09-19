---
change: dynamic-docs-sidebar
cabbage_stage: implementation
---
# Tasks

- [x] 定位死链：确认 4 个侧边栏链接与 1 个首页按钮指向无 index 的目录。
- [x] 侧边栏与导航改为按目录是否含 index 动态生成。
- [x] 修正资产首页 hero 按钮，改为同页锚点。
- [x] 双向验证：加 README 后目录出现；移除后消失。
- [x] 端到端验证：全新 init 项目（20 空目录）构建成功且无死链。
- [x] 同步 vendored CLI，运行全量测试与文档构建。

# Verification

- `python -m unittest discover tests`：54 项通过。
- `python -m cabbage_cli validate --all`：VALID。
- `pnpm --dir docs run build`：构建成功。
- `python scripts/sync-vendor.py`：副本已同步。
- `git diff --check`：无空白错误。
- 全新 init 项目端到端构建与首页链接检查通过。

未覆盖：站点为客户端渲染，未在真实浏览器中点击验证；已用构建产物 HTML 断言替代。
docs/ 下 5 个空目录保留（属 CLI 设计），侧边栏现已不引用它们。
