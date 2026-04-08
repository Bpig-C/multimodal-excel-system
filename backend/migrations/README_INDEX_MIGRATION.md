# 数据库索引迁移指南

## 概述

本迁移为 `annotation_tasks` 表添加性能优化索引，以提升任务查询的性能。

## 迁移内容

### 新增索引

1. **复合索引**: `idx_annotation_tasks_dataset_status`
   - 列: `(dataset_id, status)`
   - 用途: 优化按数据集和状态组合筛选的查询
   - 场景: 标注员查看特定数据集的待处理任务

2. **时间索引**: `idx_annotation_tasks_created_at`
   - 列: `(created_at)`
   - 用途: 优化按创建时间排序的查询
   - 场景: 任务列表按时间倒序显示

## 执行步骤

### 方法一：使用 Python 脚本（推荐）

```bash
# 1. 应用迁移
python backend/scripts/apply_index_migration.py

# 2. 测试性能
python backend/scripts/test_index_performance.py
```

### 方法二：手动执行 SQL

```bash
# 使用 SQLite 命令行工具
sqlite3 backend/data/annotation.db < backend/migrations/add_task_query_indexes.sql
```

## 验证索引

### 检查索引是否创建成功

```sql
SELECT name, sql 
FROM sqlite_master 
WHERE type='index' AND tbl_name='annotation_tasks'
ORDER BY name;
```

预期输出应包含：
- `idx_annotation_tasks_dataset_status`
- `idx_annotation_tasks_created_at`

### 验证查询是否使用索引

```sql
EXPLAIN QUERY PLAN
SELECT * FROM annotation_tasks 
WHERE dataset_id = 1 AND status = 'pending'
ORDER BY created_at DESC;
```

输出中应该包含 `USING INDEX` 字样。

## 性能测试

### 运行性能测试脚本

```bash
python backend/scripts/test_index_performance.py
```

测试脚本会：
1. 验证索引是否存在
2. 执行多个查询并测量响应时间
3. 分析查询计划，确认索引被使用

### 预期性能提升

| 数据集规模 | 任务数量 | 预期提升 |
|-----------|---------|---------|
| 小型 | < 1,000 | 10-20% |
| 中型 | 1,000-10,000 | 50-80% |
| 大型 | > 10,000 | 80-95% |

## 回滚

如果需要删除索引：

```sql
DROP INDEX IF EXISTS idx_annotation_tasks_dataset_status;
DROP INDEX IF EXISTS idx_annotation_tasks_created_at;
```

## 注意事项

1. **执行时机**: 建议在低峰期执行，特别是对于大型数据库
2. **存储空间**: 索引会占用额外的存储空间（约为表大小的 10-20%）
3. **写入性能**: 插入/更新操作会有轻微影响（< 5%），但查询性能的提升远大于此
4. **统计信息**: 定期运行 `ANALYZE` 命令以更新统计信息

## 优化建议

### 更新统计信息

```sql
ANALYZE annotation_tasks;
```

### 监控查询性能

在应用日志中添加查询时间监控：

```python
import time

start = time.time()
results = db.query(AnnotationTask).filter(...).all()
elapsed = time.time() - start

if elapsed > 0.1:  # 超过 100ms
    logger.warning(f"Slow query detected: {elapsed:.2f}s")
```

### 进一步优化

如果查询性能仍不理想，可以考虑：

1. 添加更多复合索引
2. 使用查询缓存
3. 优化查询逻辑
4. 考虑数据库分区

## 相关文件

- 迁移脚本: `backend/migrations/add_task_query_indexes.sql`
- 应用脚本: `backend/scripts/apply_index_migration.py`
- 测试脚本: `backend/scripts/test_index_performance.py`

## 相关需求

- Requirement 4.2: 在数据库层面进行权限过滤
- Requirement 4.3: 使用数据集分配表的任务范围进行高效过滤

## 问题排查

### 索引未被使用

如果查询计划显示索引未被使用：

1. 检查查询条件是否匹配索引列
2. 运行 `ANALYZE` 更新统计信息
3. 检查数据分布是否适合使用索引

### 性能未提升

如果性能提升不明显：

1. 确认数据量是否足够大（< 1000 条时提升不明显）
2. 检查是否有其他性能瓶颈（网络、应用层等）
3. 使用 `EXPLAIN QUERY PLAN` 分析查询计划

## 联系支持

如有问题，请查看：
- 项目文档: `docs/`
- 任务规范: `.kiro/specs/role-based-task-filtering/`
