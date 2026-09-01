# Cabbage

一个面向 AI Agent / 软件团队的项目文档管理 Skill，并附带可执行的 `cabbage` CLI。

核心目标不是“提醒 Agent 写文档”，而是把需求、架构、API、数据库、测试、发布和事故文档变成可验证的工作流门禁。

## 安装方式

本项目不发布至 PyPI，推荐通过以下三种方式进行安装：

### 1. 远程一键安装（通用 Linux / macOS，推荐）

自动创建独立隔离环境并安装至 `~/.local/bin/cabbage`（无需 root 权限，不污染系统 Python 环境）：

```bash
curl -fsSL https://raw.githubusercontent.com/devcxl/cabbage/master/scripts/install.sh | bash
```

> **卸载方式**：
> ```bash
> curl -fsSL https://raw.githubusercontent.com/devcxl/cabbage/master/scripts/install.sh | bash -s -- --uninstall
> ```

### 2. Arch Linux 原生包（AUR / PKGBUILD）

```bash
# 从仓库 PKGBUILD 本地构建并安装
cd packaging/aur && makepkg -si

# 或通过 AUR helper 安装
yay -S cabbage-git
```

### 3. Debian / Ubuntu (.deb 包)

直接从 [GitHub Releases](https://github.com/devcxl/cabbage/releases) 页面下载最新 `.deb` 安装包：

```bash
sudo dpkg -i cabbage_*_all.deb
# 如缺少依赖可执行：sudo apt-get install -f
```

---

## 快速开始

```bash
cd your-project
cabbage init
cabbage new feature add-user-login
cabbage status add-user-login
cabbage next add-user-login
cabbage verify add-user-login requirement
cabbage gate add-user-login implementation
cabbage validate add-user-login
cabbage sync add-user-login
cabbage archive add-user-login
cabbage docs dev
```

已有项目接入（存量文档迁移）：`cabbage init` 后运行 `cabbage adopt`，它会清点现有文档并生成 `.cabbage/adoption-report.md`（不动任何文件），按 `references/adoption.md` 的七个阶段完成迁移后再开启 CI 门禁。

## 关键约束

- 文档验收状态由 CLI 生成，不能只靠文件存在判断。
- 验证阶段（`verify`）记录内容签名；上游文档、影响范围或 workflow 变化后，下游自动变为 `stale`。
- `gate implementation` 在实现前检查所有前置文档。
- `verify` 会拒绝仍含 `TODO`、`TBD`、`FIXME` 或 `CABBAGE` 占位提示的文档。
- `sync` / `archive` 自动将变更中的需求与设计规范沉淀到 `docs/` 全局文档中，避免手动重复搬运。
- `ci` 使用 Git diff 检查代码变更是否绑定 `.cabbage/changes/<change>`。
- `gate merge` 要求当前 change 的所有激活阶段均已验证完成。
- VitePress 构建作为 CI 文档门禁；Mermaid 由 `vitepress-plugin-mermaid` 插件渲染。

## 真正形成门禁

将生成的 GitHub Actions `cabbage` job 设为受保护分支的 Required Status Check，并对 `.cabbage/workflows/**`、`.cabbage/tooling/**` 与 CI 配置要求人工审核。详见 `references/enforcement.md`。
