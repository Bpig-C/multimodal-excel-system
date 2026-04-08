# 数据库迁移管理指南

## 概述

本项目使用版本化的数据库迁移系统，确保数据库结构的变更可追踪、可回滚。

## 目录结构

```
backend/migrations/
├── versions.json           # 迁移版本记录
├── MIGRATION_GUIDE.md      # 本文档
├── v001_*.sql             # 版本1迁移脚本
├── v002_*.sql             # 版本2迁移脚本
└── ...
```

## 迁移版本命名规范

格式：`v{版本号}_{描述}.sql`

示例：
- `v001_initial_schema.sql` - 初始数据库结构
- `v002_add_batch_jobs.sql` - 添加批量任务表
- `v003_add_dataset_assignment.sql` - 添加数据集分配表

## 迁移脚本编写规范

### 1. 文件头部注释

```sql
-- 迁移版本: v001
-- 描述: 初始数据库结构
-- 作者: [作者名]
-- 日期: 2026-02-04
-- 依赖: 无
```

### 2. 向前迁移 (UP)

```sql
-- ============================================
-- 向前迁移 (UP)
-- ============================================

CREATE TABLE IF NOT EXISTS example_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
```

### 3. 向后迁移 (DOWN) - 可选

```sql
-- ============================================
-- 向后迁移 (DOWN) - 回滚用
-- ============================================

-- DROP TABLE IF EXISTS example_table;
```

### 4. 数据迁移

如果需要迁移数据，在结构变更后添加：

```sql
-- ============================================
-- 数据迁移
-- ============================================

-- 示例：更新现有数据
-- UPDATE users SET role = 'user' WHERE role IS NULL;
```

## 使用方法

### 1. 检查当前数据库版本

```bash
python backend/scripts/db_migrate.py status
```

### 2. 应用所有待执行的迁移

```bash
python backend/scripts/db_migrate.py upgrade
```

### 3. 应用到指定版本

```bash
python backend/scripts/db_migrate.py upgrade --target 5
```

### 4. 回滚到指定版本

```bash
python backend/scripts/db_migrate.py downgrade --target 3
```

### 5. 创建新的迁移

```bash
python backend/scripts/db_migrate.py create "add_user_profile"
```

这会创建一个新的迁移文件模板。

## 迁移历史

### v001 - 初始数据库结构 (2026-02-04)
- 创建所有基础表
- 包含：users, datasets, corpus, annotation_tasks, text_entities, relations等

### v002 - 添加批量任务表 (2026-02-04)
- 添加 batch_jobs 表
- 支持批量自动标注功能

### v003 - 添加数据集分配表 (2026-02-04)
- 添加 dataset_assignments 表
- 支持任务分配和权限控制

### v004 - 添加任务查询索引 (2026-02-04)
- 添加 idx_annotation_tasks_dataset_status 索引
- 添加 idx_annotation_tasks_created_at 索引
- 优化任务列表查询性能

## 注意事项

1. **永远不要直接修改已应用的迁移文件**
   - 如果需要修改，创建新的迁移文件

2. **测试迁移**
   - 在开发环境测试迁移
   - 确保向前和向后迁移都能正常工作

3. **备份数据**
   - 在生产环境应用迁移前，务必备份数据库

4. **版本控制**
   - 所有迁移文件都应纳入版本控制
   - versions.json 也应纳入版本控制

5. **团队协作**
   - 多人开发时，注意迁移版本号的冲突
   - 建议在合并代码前同步迁移版本

## 故障排除

### 迁移失败

如果迁移失败：

1. 检查错误信息
2. 查看数据库当前状态
3. 手动修复问题
4. 更新 versions.json 中的版本号

### 版本不一致

如果本地版本与数据库版本不一致：

```bash
# 查看状态
python backend/scripts/db_migrate.py status

# 强制设置版本（谨慎使用）
python backend/scripts/db_migrate.py set-version 3
```

## 最佳实践

1. **小步迁移**：每次迁移只做一件事
2. **可逆性**：尽量提供回滚脚本
3. **测试数据**：在迁移中包含测试数据的处理
4. **文档化**：在迁移文件中详细注释
5. **代码审查**：迁移脚本也需要代码审查
