# 项目文档

- **架构文档**：`PROJECT_INDEX/architecture.md`
- **数据库表结构**：`PROJECT_INDEX/database_schema.md`
- **代码签名索引**：`PROJECT_INDEX/history/`（repomix 自动生成）

## 更新索引

运行以下命令更新代码签名索引：

```bash
bash update_index.sh
```

或直接运行 repomix（需手动替换 `{datetime}`）：

```bash
npx repomix@latest --config repomix.config.json --compress
```

## 项目概述

**品质失效案例实体关系标注系统** - 一款自动化实体关系标注工具

- 后端：FastAPI + LangChain + SQLAlchemy + SQLite
- 前端：Vue 3 + TypeScript + Element Plus + Pinia + Vite
- LLM：Qwen-Max（DashScope API）

**核心进度**：16/46 核心任务完成 (35%)
