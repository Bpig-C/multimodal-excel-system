# 自动化标注功能调研报告

## 调研日期
2026-02-04

## 调研目的
调研系统中自动化标注功能的实现状态，确定前端是否已接入后端API。

## 后端API现状

### ✅ 已实现的API

#### 1. 批量自动标注 API

**端点**: `POST /api/v1/annotations/batch`

**功能**: 触发批量自动标注，创建批量任务并在后台异步执行

**请求参数**:
```json
{
  "dataset_id": "string",  // 数据集ID（必填）
  "created_by": 1          // 创建人ID（可选）
}
```

**响应**:
```json
{
  "success": true,
  "message": "批量标注任务已创建",
  "data": {
    "job_id": "batch-xxxxxxxxxxxx",
    "dataset_id": "dataset_001",
    "total_tasks": 100,
    "status": "pending"
  }
}
```

#### 2. 查询批量任务状态 API

**端点**: `GET /api/v1/annotations/batch/{job_id}`

**功能**: 获取批量任务的状态和进度

**响应**:
```json
{
  "success": true,
  "message": "获取批量任务状态成功",
  "data": {
    "job_id": "batch-xxxxxxxxxxxx",
    "status": "processing",
    "total_tasks": 100,
    "completed_tasks": 50,
    "failed_tasks": 2,
    "pending_tasks": 48,
    "progress": 0.52,
    "duration_seconds": 120.5,
    "started_at": "2026-02-04T10:00:00",
    "completed_at": null,
    "error_message": null
  }
}
```

#### 3. 取消批量任务 API

**端点**: `POST /api/v1/annotations/batch/{job_id}/cancel`

**功能**: 取消正在执行的批量任务

**响应**:
```json
{
  "success": true,
  "message": "批量任务已取消"
}
```

### ❌ 未实现的API

#### 单条自动标注 API

**状态**: 未实现独立的API端点

**说明**: 
- 后端服务层有 `_annotate_single_task` 方法（私有方法）
- 该方法在批量标注中被调用
- 但没有暴露为独立的API端点

**建议**: 
如果需要单条自动标注功能，可以添加以下API：

```python
@router.post("/{task_id}/auto-annotate")
async def auto_annotate_single_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """触发单条任务的自动标注"""
    # 实现代码
```

## 后端服务实现

### BatchAnnotationService

**位置**: `backend/services/batch_annotation_service.py`

**核心功能**:

1. **create_batch_job()** - 创建批量标注任务
   - 验证数据集存在
   - 统计待标注任务数量
   - 创建批量任务记录

2. **execute_batch_annotation()** - 执行批量标注（异步）
   - 获取所有待标注任务
   - 逐个调用 `_annotate_single_task()`
   - 更新进度和状态

3. **_annotate_single_task()** - 标注单个任务（私有方法）
   - 调用实体抽取Agent
   - 调用关系抽取Agent
   - 保存标注结果到数据库
   - 更新任务状态

4. **get_batch_job_statistics()** - 获取批量任务统计
   - 返回任务进度、状态、耗时等信息

5. **cancel_batch_job()** - 取消批量任务
   - 只能取消 pending 或 processing 状态的任务

### 使用的AI Agent

1. **EntityExtractionAgent** - 实体抽取
   - 位置: `backend/agents/entity_extraction.py`
   - 功能: 从文本中提取命名实体

2. **RelationExtractionAgent** - 关系抽取
   - 位置: `backend/agents/relation_extraction.py`
   - 功能: 从实体中提取关系

## 前端接入状态

### ❌ 未接入

**当前状态**:
- 数据集详情页面有"批量标注"按钮
- 点击后显示"批量标注功能开发中..."
- 未调用后端API

**位置**: `frontend/src/views/dataset/DatasetDetail.vue`

```typescript
const handleBatchAnnotate = () => {
  // TODO: 触发批量标注
  ElMessage.info('批量标注功能开发中...')
}
```

### 需要实现的前端功能

#### 1. 批量标注功能

**步骤**:
1. 创建 API 客户端方法（`frontend/src/api/annotation.ts`）
2. 实现批量标注触发逻辑
3. 显示批量任务进度对话框
4. 轮询查询任务状态
5. 显示完成结果

**建议实现**:
```typescript
// API 客户端
export const annotationApi = {
  // 触发批量标注
  triggerBatchAnnotation: (datasetId: string) => {
    return request.post('/api/v1/annotations/batch', {
      dataset_id: datasetId
    })
  },
  
  // 查询批量任务状态
  getBatchJobStatus: (jobId: string) => {
    return request.get(`/api/v1/annotations/batch/${jobId}`)
  },
  
  // 取消批量任务
  cancelBatchJob: (jobId: string) => {
    return request.post(`/api/v1/annotations/batch/${jobId}/cancel`)
  }
}

// 组件实现
const handleBatchAnnotate = async () => {
  try {
    const response = await annotationApi.triggerBatchAnnotation(datasetId)
    const jobId = response.data.job_id
    
    // 显示进度对话框
    showBatchProgressDialog(jobId)
    
    // 开始轮询状态
    pollBatchJobStatus(jobId)
  } catch (error) {
    ElMessage.error('启动批量标注失败')
  }
}
```

#### 2. 单条自动标注功能

**状态**: 后端未实现独立API

**建议**:
1. 先实现后端API端点
2. 在标注编辑器中添加"自动标注"按钮
3. 调用API触发单条自动标注
4. 显示标注结果

## 实现优先级

### 高优先级
1. ✅ 统一复核列表界面样式（已完成）
2. 🔄 实现批量标注前端接入
   - 创建 API 客户端方法
   - 实现批量标注触发
   - 实现进度显示和轮询

### 中优先级
3. 实现单条自动标注
   - 后端添加API端点
   - 前端添加触发按钮
   - 集成到标注编辑器

### 低优先级
4. 优化用户体验
   - 添加批量标注历史记录
   - 支持批量任务管理
   - 添加标注质量评估

## 技术细节

### 批量标注流程

```
1. 用户点击"批量标注"按钮
   ↓
2. 前端调用 POST /api/v1/annotations/batch
   ↓
3. 后端创建 BatchJob 记录
   ↓
4. 后端在后台异步执行标注
   ├─ 获取所有 pending 状态的任务
   ├─ 逐个调用 _annotate_single_task()
   │   ├─ 调用 EntityExtractionAgent
   │   ├─ 保存实体到数据库
   │   ├─ 调用 RelationExtractionAgent
   │   └─ 保存关系到数据库
   └─ 更新 BatchJob 进度
   ↓
5. 前端轮询查询任务状态
   ↓
6. 显示完成结果
```

### 单条标注流程

```
1. 用户在标注编辑器点击"自动标注"
   ↓
2. 前端调用 POST /api/v1/annotations/{task_id}/auto-annotate
   ↓
3. 后端调用 _annotate_single_task()
   ├─ 调用 EntityExtractionAgent
   ├─ 保存实体
   ├─ 调用 RelationExtractionAgent
   └─ 保存关系
   ↓
4. 返回标注结果
   ↓
5. 前端显示标注结果
```

## 数据库表

### batch_jobs 表

```sql
CREATE TABLE batch_jobs (
    id INTEGER PRIMARY KEY,
    job_id VARCHAR(100) UNIQUE NOT NULL,
    dataset_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,  -- pending, processing, completed, failed, cancelled
    total_tasks INTEGER NOT NULL,
    completed_tasks INTEGER DEFAULT 0,
    failed_tasks INTEGER DEFAULT 0,
    progress FLOAT DEFAULT 0.0,
    error_message TEXT,
    created_by INTEGER,
    created_at DATETIME,
    started_at DATETIME,
    completed_at DATETIME,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

## 结论

### 后端状态
✅ **批量标注功能已完整实现**
- API端点完整
- 服务层实现完善
- 支持异步执行和进度跟踪

❌ **单条自动标注功能未实现**
- 服务层有私有方法
- 缺少独立的API端点

### 前端状态
❌ **批量标注未接入**
- 按钮存在但未实现
- 需要创建API客户端
- 需要实现进度显示

❌ **单条自动标注未接入**
- 功能不存在
- 需要先实现后端API

### 下一步行动
1. ✅ 统一复核列表界面（已完成）
2. 实现批量标注前端接入
3. 考虑是否需要单条自动标注功能
4. 测试自动标注的准确性

## 相关文件

**后端**:
- `backend/api/annotations.py` - API端点
- `backend/services/batch_annotation_service.py` - 批量标注服务
- `backend/agents/entity_extraction.py` - 实体抽取Agent
- `backend/agents/relation_extraction.py` - 关系抽取Agent

**前端**:
- `frontend/src/views/dataset/DatasetDetail.vue` - 数据集详情页面
- `frontend/src/api/annotation.ts` - API客户端（需要添加方法）

## 签名

- 调研人: Kiro AI Assistant
- 调研日期: 2026-02-04
- 状态: 完成 ✅
