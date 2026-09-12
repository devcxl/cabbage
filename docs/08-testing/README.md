# 测试说明

测试使用 Python `unittest`，主要在临时目录验证真实文件系统和 CLI 行为，不依赖外部服务。
测试数量以实际运行输出为准，不手工维护容易失效的计数表。

## 执行方式

```bash
python -m unittest discover tests
python -m cabbage_cli validate --all
pnpm --dir docs run build
git diff --check
```

## 覆盖范围

- `test_cabbage.py`：模板校验、依赖门禁、失效传播、同步与归档。
- `test_cabbage_rename.py`：包入口、初始化、站点依赖、vendored CLI。
- `test_engine_enhancements.py`：依赖环、Markdown、清单、迁移、文档映射和 Git CI。
- `test_adopt.py`：文档盘点和分类。
- `test_templates.py`：模板标题契约。
- `test_tasks_dag.py`：可选 DAG 解析与派发数据。
- `test_repository_contracts.py`：指南使用真实阶段 ID；副本所有文件与主实现一致。

修改 `cabbage_cli/` 后执行 `python scripts/sync-vendor.py`，不要手动修改
`.cabbage/tooling/cabbage_cli/`。完整测试套件与 CI 会检查副本漂移。

## 验证记录与边界

指南和副本修复前，新增检查复现了无效阶段名称与七个文件差异；修复后完整
Python 测试与 VitePress 构建通过。构建仍提示部分 chunk 大于 500 kB，不影响成功。

自动检查不证明文档语义与代码一致，也不验证 GitHub 的分支保护设置。
CLI 的单元测试不能替代真实文档站点构建及远程 CI/部署检查。
