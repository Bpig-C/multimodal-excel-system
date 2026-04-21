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

**核心进度**：42/47 核心任务完成 (~89%)

- 后端全部完成（Tasks 1-26）
- 前端核心完成（Tasks 27-38, 41-43, 47）
- 跳过：Task 39（数据导出前端）、Task 40（Reward数据集前端）
- 待完成：Task 44（系统集成测试）、Task 45（文档/部署）、Task 46（最终检查）
