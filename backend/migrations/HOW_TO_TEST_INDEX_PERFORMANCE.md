# 如何测试数据库索引性能

## 快速开始

### 1. 应用索引迁移（首次）

```bash
cd backend
python scripts/apply_index_migration.py
```

### 2. 运行性能测试

```bash
cd backend
python scripts/test_index_performance.py
```

## 详细测试步骤

### 步骤 1: 检查数据库状态

在应用迁移前，先检查数据库状态：

```bash
cd backend
python scripts/check_db_status.py
```

**预期输出**:
- 显示所有数据库表
- 显示 `annotation_tasks` 表的现有索引

### 步骤 2: 应用索引迁移

```bash
cd backend
python scripts/apply_index_migration.py
```

**预期输出**:
```
应用数据库索引迁移
迁移文件: .../add_task_query_indexes.sql
找到 6 条 SQL 语句

开始执行迁移...
  [1] 创建复合索引: idx_annotation_tasks_dataset_status
  [2] 创建时间索引: idx_annotation_tasks_created_at

✓ 迁移执行成功

验证索引创建:
  ✓ idx_annotation_tasks_created_at
  ✓ idx_annotation_tasks_dataset_status

迁移完成
```

### 步骤 3: 运行性能测试

```bash
cd backend
python scripts/test_index_performance.py
```

**测试内容**:

1. **索引验证测试**
   - 检查索引是否存在
   - 验证索引定义是否正确

2. **查询性能测试**
   - 测试按数据集和状态筛选
   - 测试按时间排序
   - 测试复合条件查询
   - 测量查询响应时间

3. **查询计划分析**
   - 使用 `EXPLAIN QUERY PLAN` 分析查询
   - 验证查询是否使用了索引

**预期输出**:
```
数据库索引性能测试

测试 1: 验证索引是否存在
找到的索引 (4):
  ✓ idx_annotation_tasks_created_at
  ✓ idx_annotation_tasks_dataset_status
  ✓ ix_annotation_tasks_status
  ✓ ix_annotation_tasks_task_id

✓ 所有必需的索引都已创建

测试 2: 查询性能测试
当前任务总数: 522

测试查询 1: 按数据集和状态筛选
  结果数量: 515
  查询时间: 4.97 ms

测试查询 2: 按创建时间排序（分页）
  结果数量: 20
  查询时间: 1.65 ms

测试查询 3: 复合条件查询
  结果数量: 20
  查询时间: 3.16 ms

性能评估:
  数据集规模: 小型 (522 条)
  预期查询时间: < 10 ms
  ✓ 查询性能优秀

测试 3: 查询计划分析（验证索引使用）
查询: 按数据集和状态筛选
  ✓ 使用了优化索引

查询: 按时间排序
  ✓ 使用了优化索引

查询: 复合查询
  ✓ 使用了优化索引

测试完成
```

## 性能基准

### 查询响应时间标准

| 数据集规模 | 任务数量 | 预期响应时间 | 性能评级 |
|-----------|---------|-------------|---------|
| 小型 | < 1,000 | < 10 ms | 优秀 |
| 中型 | 1,000-10,000 | < 50 ms | 良好 |
| 大型 | > 10,000 | < 100 ms | 可接受 |

### 性能评级标准

- **优秀**: 查询时间 < 10 ms
- **良好**: 查询时间 10-50 ms
- **一般**: 查询时间 50-100 ms
- **较差**: 查询时间 > 100 ms

## 手动测试查询

### 使用 SQLite 命令行

```bash
# 打开数据库
sqlite3 backend/data/annotation.db

# 查看所有索引
SELECT name, sql 
FROM sqlite_master 
WHERE type='index' AND tbl_name='annotation_tasks'
ORDER BY name;

# 分析查询计划
EXPLAIN QUERY PLAN
SELECT * FROM annotation_tasks 
WHERE dataset_id = 1 AND status = 'pending'
ORDER BY created_at DESC;

# 退出
.quit
```

### 使用 Python 脚本

创建测试脚本 `test_custom_query.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import engine
from sqlalchemy import text
import time

# 测试自定义查询
query = """
SELECT * FROM annotation_tasks 
WHERE dataset_id = 1 AND status = 'pending'
ORDER BY created_at DESC
LIMIT 20
"""

with engine.connect() as conn:
    # 测量查询时间
    start = time.time()
    result = conn.execute(text(query))
    rows = result.fetchall()
    elapsed = (time.time() - start) * 1000
    
    print(f"查询返回 {len(rows)} 条记录")
    print(f"查询时间: {elapsed:.2f} ms")
    
    # 查看查询计划
    plan = conn.execute(text(f"EXPLAIN QUERY PLAN {query}"))
    print("\n查询计划:")
    for row in plan:
        print(f"  {row}")
```

## 定期监控

### 建议监控频率

1. **数据量变化后**: 立即测试
2. **每月一次**: 定期性能检查
3. **性能问题时**: 立即诊断

### 监控脚本

创建定期监控脚本 `monitor_performance.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import SessionLocal
from models.db_models import AnnotationTask
import time
from datetime import datetime

db = SessionLocal()

try:
    # 获取任务总数
    total = db.query(AnnotationTask).count()
    
    # 测试查询性能
    start = time.time()
    tasks = db.query(AnnotationTask).filter(
        AnnotationTask.status == 'pending'
    ).order_by(
        AnnotationTask.created_at.desc()
    ).limit(20).all()
    elapsed = (time.time() - start) * 1000
    
    # 记录结果
    print(f"[{datetime.now()}] 性能监控")
    print(f"  任务总数: {total}")
    print(f"  查询时间: {elapsed:.2f} ms")
    
    if elapsed > 100:
        print(f"  ⚠️  警告: 查询时间超过 100ms")
    elif elapsed > 50:
        print(f"  ⚠️  注意: 查询时间超过 50ms")
    else:
        print(f"  ✓ 性能正常")
        
finally:
    db.close()
```

## 性能优化建议

### 如果查询性能不理想

1. **更新统计信息**
   ```sql
   ANALYZE annotation_tasks;
   ```

2. **检查索引使用情况**
   ```sql
   EXPLAIN QUERY PLAN <your_query>;
   ```

3. **考虑添加更多索引**
   - 分析慢查询日志
   - 识别常用查询模式
   - 添加针对性索引

4. **优化查询逻辑**
   - 减少不必要的 JOIN
   - 使用分页限制结果集
   - 避免 SELECT *

### 数据量增长后的优化

当任务数量超过 10,000 条时：

1. **评估索引效果**
   ```bash
   python scripts/test_index_performance.py
   ```

2. **考虑添加复合索引**
   ```sql
   -- 例如：按分配用户和状态查询
   CREATE INDEX idx_annotation_tasks_assigned_status 
   ON annotation_tasks(assigned_to, status);
   ```

3. **考虑数据归档**
   - 将旧的已完成任务归档
   - 保持活跃数据集较小

## 故障排查

### 问题: 索引未被使用

**症状**: 查询计划显示 `SCAN` 而不是 `SEARCH`

**解决方案**:
1. 运行 `ANALYZE` 更新统计信息
2. 检查查询条件是否匹配索引列
3. 确认数据量足够大（小数据集可能不使用索引）

### 问题: 查询性能未提升

**症状**: 添加索引后性能没有明显改善

**解决方案**:
1. 确认查询确实使用了索引（使用 EXPLAIN）
2. 检查是否有其他性能瓶颈（网络、应用层）
3. 考虑数据分布是否适合使用索引

### 问题: 写入性能下降

**症状**: 插入/更新操作变慢

**解决方案**:
1. 这是正常现象（索引需要维护）
2. 评估读写比例，确认索引收益大于成本
3. 考虑批量操作以减少索引维护开销

## 相关资源

- 迁移脚本: `backend/migrations/add_task_query_indexes.sql`
- 应用脚本: `backend/scripts/apply_index_migration.py`
- 测试脚本: `backend/scripts/test_index_performance.py`
- 检查脚本: `backend/scripts/check_db_status.py`
- 使用指南: `backend/migrations/README_INDEX_MIGRATION.md`
- 测试结果: `backend/migrations/INDEX_MIGRATION_TEST_RESULTS.md`

## 联系支持

如有问题或需要帮助，请参考：
- 项目文档: `docs/`
- 任务规范: `.kiro/specs/role-based-task-filtering/`
