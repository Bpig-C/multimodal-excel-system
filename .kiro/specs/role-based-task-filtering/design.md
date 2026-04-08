# Design Document

## Overview

本设计文档描述了基于角色的任务列表权限控制功能的技术实现方案。该功能包括：

1. **新增跨数据集任务列表API** (`GET /api/v1/annotations`)
2. **增强现有数据集任务列表API** (`GET /api/v1/datasets/{dataset_id}/tasks`)
3. **增强任务详情和编辑API的权限检查**
4. **创建任务列表前端页面** (`/annotations`)

核心设计原则：
- **复用现有逻辑**：充分利用 `DatasetAssignmentService` 的权限检查和任务范围过滤
- **统一权限控制**：创建可复用的权限装饰器和中间件
- **高效查询**：在数据库层面进行权限过滤，避免应用层过滤
- **向后兼容**：确保现有API的响应格式和行为不变

## Architecture

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ AnnotationList   │  │ DatasetDetail    │                │
│  │ (任务列表页面)    │  │ (数据集详情页)    │                │
│  └────────┬─────────┘  └────────┬─────────┘                │
│           │                     │                           │
└───────────┼─────────────────────┼───────────────────────────┘
            │                     │
            ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                         API Layer                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │  GET /api/v1/annotations (新增)                      │  │
│  │  - 跨数据集任务列表                                   │  │
│  │  - 权限过滤                                          │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  GET /api/v1/datasets/{id}/tasks (增强)             │  │
│  │  - 添加权限过滤                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  GET /api/v1/annotations/{id} (增强)                 │  │
│  │  - 添加权限检查                                       │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       Service Layer                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │  TaskQueryService (新增)                             │  │
│  │  - 统一任务查询逻辑                                   │  │
│  │  - 权限过滤                                          │  │
│  │  - 任务范围计算                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  DatasetAssignmentService (复用)                     │  │
│  │  - check_permission()                                │  │
│  │  - get_user_task_range()                             │  │
│  │  - _get_tasks_in_range()                             │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        Data Layer                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │AnnotationTask│  │DatasetAssign │  │    User      │     │
│  │              │  │    ment      │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. TaskQueryService (新增)

**职责**：封装任务查询逻辑，提供统一的权限过滤和任务范围计算

**接口**：
```python
class TaskQueryService:
    def __init__(self, db: Session):
        self.db = db
        self.assignment_service = DatasetAssignmentService(db)
    
    def get_user_tasks(
        self,
        user_id: int,
        user_role: str,
        dataset_id: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Tuple[List[AnnotationTask], int]:
        """
        获取用户可访问的任务列表
        
        Args:
            user_id: 用户ID
            user_role: 用户角色 (admin/annotator/viewer)
            dataset_id: 数据集ID筛选（可选）
            status: 状态筛选（可选）
            page: 页码
            page_size: 每页数量
            sort_by: 排序字段
            sort_order: 排序方向
        
        Returns:
            (任务列表, 总数)
        """
        pass
    
    def check_task_permission(
        self,
        user_id: int,
        user_role: str,
        task_id: int
    ) -> bool:
        """
        检查用户是否有权限访问指定任务
        
        Args:
            user_id: 用户ID
            user_role: 用户角色
            task_id: 任务ID
        
        Returns:
            是否有权限
        """
        pass
```


### 2. API端点设计

#### 2.1 跨数据集任务列表API (新增)

**端点**: `GET /api/v1/annotations`

**请求参数**:
```python
{
    "dataset_id": Optional[str],  # 数据集ID筛选
    "status": Optional[str],      # 状态筛选 (pending/processing/completed/failed)
    "page": int = 1,              # 页码
    "page_size": int = 20,        # 每页数量
    "sort_by": str = "created_at", # 排序字段
    "sort_order": str = "desc"    # 排序方向 (asc/desc)
}
```

**响应格式**:
```python
{
    "success": True,
    "message": "获取任务列表成功",
    "data": {
        "items": [
            {
                "id": int,
                "task_id": str,
                "dataset_id": str,
                "dataset_name": str,
                "corpus_id": int,
                "corpus_text": str,  # 语料文本预览（前100字符）
                "status": str,
                "annotation_type": str,
                "entity_count": int,
                "relation_count": int,
                "current_version": int,
                "created_at": str,
                "updated_at": str
            }
        ],
        "total": int,
        "page": int,
        "page_size": int
    }
}
```

**权限逻辑**:
- **管理员**: 返回所有任务（可选按数据集筛选）
- **标注员**: 返回分配给该用户的任务（基于 DatasetAssignment）
- **浏览员**: 返回403错误（浏览员不使用此端点）

#### 2.2 数据集任务列表API (增强)

**端点**: `GET /api/v1/datasets/{dataset_id}/tasks`

**现有参数**:
```python
{
    "page": int = 1,
    "page_size": int = 20,
    "status": Optional[str]
}
```

**增强内容**:
- 添加权限过滤逻辑
- 保持响应格式不变（向后兼容）

**权限逻辑**:
- **管理员**: 返回该数据集的所有任务
- **标注员**: 返回该数据集中分配给该用户的任务
- **浏览员**: 返回该数据集中状态为 completed 的任务

#### 2.3 任务详情API (增强)

**端点**: `GET /api/v1/annotations/{task_id}`

**增强内容**:
- 添加权限检查
- 保持响应格式不变

**权限逻辑**:
- **管理员**: 可以访问所有任务
- **标注员**: 只能访问分配给自己的任务
- **浏览员**: 只能访问状态为 completed 的任务

#### 2.4 任务更新API (增强)

**端点**: `PUT /api/v1/annotations/{task_id}`

**增强内容**:
- 添加权限检查

**权限逻辑**:
- **管理员**: 可以更新所有任务
- **标注员**: 只能更新分配给自己的任务
- **浏览员**: 禁止更新（返回403）

### 3. 权限装饰器设计

创建可复用的权限装饰器，避免在每个API中重复权限检查代码。

```python
from functools import wraps
from fastapi import HTTPException, Depends
from typing import Callable

def require_task_permission(
    allow_admin: bool = True,
    allow_annotator: bool = True,
    allow_viewer: bool = False,
    check_assignment: bool = True
):
    """
    任务权限装饰器
    
    Args:
        allow_admin: 是否允许管理员
        allow_annotator: 是否允许标注员
        allow_viewer: 是否允许浏览员
        check_assignment: 是否检查任务分配（标注员）
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取当前用户
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=401, detail="未认证")
            
            user_role = current_user['role']
            user_id = current_user['user_id']
            
            # 角色检查
            if user_role == 'admin' and not allow_admin:
                raise HTTPException(status_code=403, detail="管理员无权访问")
            elif user_role == 'annotator' and not allow_annotator:
                raise HTTPException(status_code=403, detail="标注员无权访问")
            elif user_role == 'viewer' and not allow_viewer:
                raise HTTPException(status_code=403, detail="浏览员无权访问")
            
            # 任务分配检查（仅标注员）
            if check_assignment and user_role == 'annotator':
                task_id = kwargs.get('task_id')
                if task_id:
                    db = kwargs.get('db')
                    service = TaskQueryService(db)
                    if not service.check_task_permission(user_id, user_role, task_id):
                        raise HTTPException(status_code=403, detail="无权访问该任务")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

**使用示例**:
```python
@router.get("/{task_id}")
@require_task_permission(allow_viewer=True, check_assignment=True)
async def get_annotation_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # API逻辑
    pass
```

## Data Models

### 现有模型（无需修改）

#### AnnotationTask
```python
class AnnotationTask(Base):
    __tablename__ = "annotation_tasks"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String(100), unique=True, nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    corpus_id = Column(Integer, ForeignKey("corpus.id"))
    status = Column(String(20), default='pending')
    annotation_type = Column(String(20), default='automatic')
    current_version = Column(Integer, default=1)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    # ...
```

#### DatasetAssignment
```python
class DatasetAssignment(Base):
    __tablename__ = "dataset_assignments"
    
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(20), nullable=False)  # 'annotator' 或 'reviewer'
    task_start_index = Column(Integer)  # 起始索引（从1开始）
    task_end_index = Column(Integer)    # 结束索引（包含）
    is_active = Column(Boolean, default=True)
    # ...
```

### 数据库查询策略

#### 管理员查询所有任务
```sql
SELECT * FROM annotation_tasks
WHERE (dataset_id = ? OR ? IS NULL)  -- 可选数据集筛选
  AND (status = ? OR ? IS NULL)      -- 可选状态筛选
ORDER BY created_at DESC
LIMIT ? OFFSET ?
```

#### 标注员查询分配的任务
```sql
-- 步骤1: 获取用户的所有分配
SELECT dataset_id, task_start_index, task_end_index
FROM dataset_assignments
WHERE user_id = ? AND role = 'annotator' AND is_active = TRUE

-- 步骤2: 对每个分配，获取任务范围
-- 如果 task_start_index 和 task_end_index 为 NULL，则获取该数据集的所有任务
-- 否则，按 ID 排序后取索引范围内的任务

-- 实现方式：使用 ROW_NUMBER() 窗口函数
WITH ranked_tasks AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY dataset_id ORDER BY id) as row_num
    FROM annotation_tasks
    WHERE dataset_id IN (
        SELECT dataset_id FROM dataset_assignments
        WHERE user_id = ? AND role = 'annotator' AND is_active = TRUE
    )
)
SELECT * FROM ranked_tasks
WHERE (
    -- 全部分配
    (dataset_id, NULL, NULL) IN (
        SELECT dataset_id, task_start_index, task_end_index
        FROM dataset_assignments
        WHERE user_id = ? AND role = 'annotator' AND is_active = TRUE
    )
    OR
    -- 范围分配
    EXISTS (
        SELECT 1 FROM dataset_assignments da
        WHERE da.user_id = ? 
          AND da.role = 'annotator' 
          AND da.is_active = TRUE
          AND da.dataset_id = ranked_tasks.dataset_id
          AND ranked_tasks.row_num BETWEEN da.task_start_index AND da.task_end_index
    )
)
ORDER BY created_at DESC
LIMIT ? OFFSET ?
```

#### 浏览员查询已完成任务
```sql
SELECT * FROM annotation_tasks
WHERE status = 'completed'
  AND (dataset_id = ? OR ? IS NULL)
ORDER BY created_at DESC
LIMIT ? OFFSET ?
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Admin全局访问
*For any* set of tasks across any datasets, when an admin user queries the task list, all tasks should be returned (subject to pagination and filtering parameters).
**Validates: Requirements 1.1**

### Property 2: 任务响应完整性
*For any* task returned in the API response, the response should contain all required fields: task_id, dataset_name, corpus_text, status, annotation_type, entity_count, relation_count, created_at, updated_at.
**Validates: Requirements 1.2**

### Property 3: Admin任务访问权限
*For any* task in the system, an admin user should be able to access and edit that task without permission errors.
**Validates: Requirements 1.3**

### Property 4: 筛选功能正确性
*For any* set of tasks and any filter criteria (dataset_id, status, assigned_user), the filtered results should only contain tasks matching all specified criteria.
**Validates: Requirements 1.4**

### Property 5: 分页功能正确性
*For any* task list with more than page_size tasks, requesting different pages should return non-overlapping subsets of tasks, and the union of all pages should equal the total task set.
**Validates: Requirements 1.5, 4.4**

### Property 6: 标注员权限过滤
*For any* annotator user, querying the task list should return only tasks from datasets where that user has an active assignment.
**Validates: Requirements 2.1, 5.1**

### Property 7: 任务范围过滤
*For any* annotator with a task range assignment (start_index, end_index), the returned tasks should only include tasks within that index range when ordered by task ID.
**Validates: Requirements 2.2**

### Property 8: 标注员任务访问权限
*For any* task, an annotator should be able to access it if and only if the task is within their assigned range in the task's dataset.
**Validates: Requirements 2.4**

### Property 9: 未授权访问拒绝
*For any* task not assigned to an annotator, attempting to access that task should return a 403 Forbidden error.
**Validates: Requirements 2.5, 5.5**

### Property 10: 浏览员状态过滤
*For any* viewer user querying a dataset's task list, only tasks with status='completed' should be returned.
**Validates: Requirements 3.2, 5.2**

### Property 11: 浏览员只读访问
*For any* completed task, a viewer should be able to GET the task details, but PUT/POST/DELETE operations should return 403 Forbidden.
**Validates: Requirements 3.3, 3.4**

### Property 12: 分页元数据完整性
*For any* paginated task list response, the response should include total count, current page number, and page size fields.
**Validates: Requirements 4.5**

### Property 13: 权限错误响应
*For any* unauthorized access attempt, the system should return a 403 status code with a clear error message.
**Validates: Requirements 6.5**

### Property 14: 数据集筛选应用
*For any* task list request with a dataset_id parameter, all returned tasks should belong to that dataset.
**Validates: Requirements 8.2**

### Property 15: 筛选清除行为
*For any* annotator, when querying without a dataset_id filter, all tasks from all assigned datasets should be returned.
**Validates: Requirements 8.4**

### Property 16: NULL范围解释
*For any* dataset assignment with NULL task_start_index and task_end_index, the annotator should have access to all tasks in that dataset.
**Validates: Requirements 9.2**

### Property 17: 用户隔离
*For any* two annotators with different task range assignments in the same dataset, each annotator should only see their own assigned tasks with no overlap.
**Validates: Requirements 9.4**

### Property 18: 排序功能正确性
*For any* task list request with a sort_by parameter, the returned tasks should be ordered according to the specified field and sort direction.
**Validates: Requirements 10.3**

### Property 19: 认证要求
*For any* unauthenticated request to the task list API, the system should return a 401 Unauthorized error.
**Validates: Requirements 10.5**

### Property 20: 响应格式向后兼容
*For any* request to the enhanced dataset task list API, the response structure should match the original API response format.
**Validates: Requirements 11.1**

### Property 21: Admin行为向后兼容
*For any* admin user querying a dataset's task list before and after the enhancement, the returned task set should be identical (same tasks, same order).
**Validates: Requirements 11.3**

## Error Handling

### 错误类型和响应

#### 1. 认证错误 (401 Unauthorized)
**触发条件**:
- 请求未包含有效的认证令牌
- 认证令牌已过期

**响应格式**:
```json
{
    "success": false,
    "message": "未认证",
    "error_code": "UNAUTHORIZED"
}
```

#### 2. 权限错误 (403 Forbidden)
**触发条件**:
- 标注员尝试访问未分配的任务
- 浏览员尝试编辑任务
- 浏览员访问未完成的任务

**响应格式**:
```json
{
    "success": false,
    "message": "无权访问该资源",
    "error_code": "FORBIDDEN",
    "details": "该任务未分配给您"
}
```

#### 3. 资源不存在 (404 Not Found)
**触发条件**:
- 请求的任务ID不存在
- 请求的数据集ID不存在

**响应格式**:
```json
{
    "success": false,
    "message": "资源不存在",
    "error_code": "NOT_FOUND",
    "resource_type": "task",
    "resource_id": "task-123"
}
```

#### 4. 参数错误 (400 Bad Request)
**触发条件**:
- 分页参数无效（page < 1, page_size > 100）
- 排序字段无效
- 筛选参数格式错误

**响应格式**:
```json
{
    "success": false,
    "message": "请求参数错误",
    "error_code": "BAD_REQUEST",
    "details": "page 参数必须大于0"
}
```

### 错误处理策略

1. **统一错误响应格式**: 所有API使用相同的错误响应结构
2. **详细错误信息**: 在开发环境提供详细错误信息，生产环境隐藏敏感信息
3. **错误日志**: 记录所有权限错误和系统错误到日志系统
4. **优雅降级**: 当权限检查失败时，返回空列表而不是抛出异常（对于列表API）

## Testing Strategy

### 单元测试

#### TaskQueryService 测试
```python
class TestTaskQueryService:
    def test_admin_gets_all_tasks(self):
        """测试管理员获取所有任务"""
        # 创建测试数据
        # 调用 get_user_tasks
        # 断言返回所有任务
        
    def test_annotator_gets_assigned_tasks_only(self):
        """测试标注员只获取分配的任务"""
        # 创建测试数据和分配
        # 调用 get_user_tasks
        # 断言只返回分配的任务
        
    def test_task_range_filtering(self):
        """测试任务范围过滤"""
        # 创建任务和范围分配
        # 调用 get_user_tasks
        # 断言只返回范围内的任务
        
    def test_viewer_gets_completed_tasks_only(self):
        """测试浏览员只获取已完成任务"""
        # 创建不同状态的任务
        # 调用 get_user_tasks
        # 断言只返回completed任务
```

#### 权限装饰器测试
```python
class TestPermissionDecorator:
    def test_admin_allowed(self):
        """测试管理员权限"""
        
    def test_annotator_with_assignment_allowed(self):
        """测试有分配的标注员权限"""
        
    def test_annotator_without_assignment_denied(self):
        """测试无分配的标注员被拒绝"""
        
    def test_viewer_edit_denied(self):
        """测试浏览员编辑被拒绝"""
```

### 集成测试

#### API端点测试
```python
class TestAnnotationListAPI:
    def test_get_tasks_as_admin(self):
        """测试管理员获取任务列表"""
        
    def test_get_tasks_as_annotator(self):
        """测试标注员获取任务列表"""
        
    def test_get_tasks_with_filters(self):
        """测试筛选功能"""
        
    def test_get_tasks_with_pagination(self):
        """测试分页功能"""
        
    def test_get_tasks_unauthorized(self):
        """测试未认证访问"""
```

#### 数据集任务列表API测试
```python
class TestDatasetTasksAPI:
    def test_backward_compatibility_for_admin(self):
        """测试管理员的向后兼容性"""
        
    def test_permission_filtering_for_annotator(self):
        """测试标注员的权限过滤"""
        
    def test_status_filtering_for_viewer(self):
        """测试浏览员的状态过滤"""
```

### 属性测试（Property-Based Testing）

使用 Hypothesis 库进行属性测试：

```python
from hypothesis import given, strategies as st

class TestTaskPermissionProperties:
    @given(
        tasks=st.lists(st.builds(AnnotationTask)),
        user_role=st.sampled_from(['admin', 'annotator', 'viewer'])
    )
    def test_permission_filtering_property(self, tasks, user_role):
        """
        **Feature: role-based-task-filtering, Property 6: 标注员权限过滤**
        **Validates: Requirements 2.1, 5.1**
        
        属性：对于任何任务集合和用户角色，权限过滤应该正确应用
        """
        # 测试逻辑
        
    @given(
        start_index=st.integers(min_value=1, max_value=100),
        end_index=st.integers(min_value=1, max_value=100),
        tasks=st.lists(st.builds(AnnotationTask), min_size=100)
    )
    def test_task_range_property(self, start_index, end_index, tasks):
        """
        **Feature: role-based-task-filtering, Property 7: 任务范围过滤**
        **Validates: Requirements 2.2**
        
        属性：对于任何任务范围，返回的任务应该在指定范围内
        """
        # 测试逻辑
```

### 测试覆盖率目标

- **单元测试覆盖率**: ≥ 90%
- **集成测试覆盖率**: ≥ 80%
- **关键路径覆盖**: 100%（权限检查、任务过滤）


## Implementation Plan

### Phase 1: 后端服务层实现

#### 1.1 创建 TaskQueryService
- 实现 `get_user_tasks()` 方法
- 实现 `check_task_permission()` 方法
- 复用 `DatasetAssignmentService` 的权限检查逻辑
- 编写单元测试

#### 1.2 创建权限装饰器
- 实现 `@require_task_permission` 装饰器
- 支持不同角色的权限配置
- 编写单元测试

### Phase 2: 后端API实现

#### 2.1 新增跨数据集任务列表API
- 创建 `GET /api/v1/annotations` 端点
- 集成 TaskQueryService
- 应用权限装饰器
- 实现筛选和排序
- 实现分页
- 编写集成测试

#### 2.2 增强数据集任务列表API
- 修改 `GET /api/v1/datasets/{dataset_id}/tasks`
- 添加权限过滤逻辑
- 保持响应格式不变
- 编写向后兼容性测试

#### 2.3 增强任务详情API
- 修改 `GET /api/v1/annotations/{task_id}`
- 添加权限检查
- 编写权限测试

#### 2.4 增强任务编辑API
- 修改 `PUT /api/v1/annotations/{task_id}`
- 添加权限检查
- 编写权限测试

### Phase 3: 前端实现

#### 3.1 创建任务列表页面组件
- 创建 `AnnotationList.vue` 组件
- 实现任务列表展示
- 实现筛选UI
- 实现分页UI
- 实现排序UI

#### 3.2 集成API调用
- 创建 API 服务函数
- 实现数据加载逻辑
- 实现错误处理
- 实现加载状态

#### 3.3 实现导航集成
- 从"我的数据集"页面传递 dataset_id 参数
- 实现面包屑导航
- 实现筛选状态管理

### Phase 4: 测试和优化

#### 4.1 端到端测试
- 测试管理员工作流
- 测试标注员工作流
- 测试浏览员工作流
- 测试权限边界情况

#### 4.2 性能优化
- 优化数据库查询
- 添加索引
- 实现查询缓存（如需要）
- 性能测试

#### 4.3 文档和部署
- 更新API文档
- 更新用户手册
- 部署到测试环境
- 部署到生产环境

## Performance Considerations

### 数据库优化

#### 1. 索引策略
```sql
-- 任务表索引
CREATE INDEX idx_annotation_tasks_dataset_status 
ON annotation_tasks(dataset_id, status);

CREATE INDEX idx_annotation_tasks_created_at 
ON annotation_tasks(created_at DESC);

-- 分配表索引（已存在）
CREATE INDEX idx_dataset_assignments_user_active 
ON dataset_assignments(user_id, is_active);

CREATE INDEX idx_dataset_assignments_dataset_active 
ON dataset_assignments(dataset_id, is_active);
```

#### 2. 查询优化
- 使用 `JOIN` 而不是多次查询
- 使用 `EXISTS` 而不是 `IN` 子查询（当数据量大时）
- 使用窗口函数 `ROW_NUMBER()` 进行任务范围过滤
- 避免 `SELECT *`，只查询需要的字段

#### 3. 分页优化
- 使用游标分页（cursor-based pagination）而不是偏移分页（offset-based）
- 缓存总数查询结果（短时间内）

### 缓存策略

#### 1. 用户权限缓存
```python
# 缓存用户的数据集分配信息（5分钟）
@cache(ttl=300)
def get_user_assignments(user_id: int) -> List[DatasetAssignment]:
    pass
```

#### 2. 任务列表缓存
- 对于管理员的全局任务列表，可以缓存1分钟
- 对于标注员的任务列表，缓存30秒
- 使用 Redis 作为缓存后端

### 性能目标

- **API响应时间**: < 200ms (P95)
- **数据库查询时间**: < 100ms (P95)
- **并发支持**: 100 req/s
- **任务列表加载时间**: < 500ms (前端)

## Security Considerations

### 1. 认证和授权
- 所有API端点都需要认证
- 使用JWT令牌进行身份验证
- 令牌过期时间：1小时
- 刷新令牌机制

### 2. 权限检查
- 在API层进行权限检查（不依赖前端）
- 使用装饰器统一权限检查逻辑
- 记录所有权限拒绝事件

### 3. 数据访问控制
- 标注员只能访问分配的任务
- 浏览员只能访问已完成的任务
- 防止通过修改请求参数绕过权限检查

### 4. SQL注入防护
- 使用参数化查询
- 使用ORM（SQLAlchemy）
- 验证所有用户输入

### 5. 敏感信息保护
- 不在错误消息中泄露系统信息
- 不在日志中记录敏感数据
- 使用HTTPS传输

## Deployment Strategy

### 1. 数据库迁移
```sql
-- 无需数据库结构变更
-- 只需添加索引
CREATE INDEX IF NOT EXISTS idx_annotation_tasks_dataset_status 
ON annotation_tasks(dataset_id, status);

CREATE INDEX IF NOT EXISTS idx_annotation_tasks_created_at 
ON annotation_tasks(created_at DESC);
```

### 2. 后端部署
- 使用蓝绿部署策略
- 先部署到测试环境验证
- 逐步部署到生产环境
- 监控错误率和响应时间

### 3. 前端部署
- 构建生产版本
- 部署到CDN
- 清除浏览器缓存

### 4. 回滚计划
- 保留上一版本的Docker镜像
- 准备回滚脚本
- 监控关键指标

## Monitoring and Logging

### 1. 关键指标
- API响应时间（P50, P95, P99）
- 错误率（按端点）
- 权限拒绝次数
- 数据库查询时间
- 并发用户数

### 2. 日志记录
```python
# 权限检查日志
logger.info(f"Permission check: user={user_id}, role={role}, task={task_id}, result={allowed}")

# API访问日志
logger.info(f"API call: endpoint={endpoint}, user={user_id}, duration={duration}ms")

# 错误日志
logger.error(f"Permission denied: user={user_id}, task={task_id}, reason={reason}")
```

### 3. 告警规则
- API错误率 > 5%
- API响应时间 > 1s (P95)
- 权限拒绝率突增 > 50%
- 数据库连接池耗尽

## Future Enhancements

### 1. 高级筛选
- 按标注类型筛选（automatic/manual）
- 按实体数量筛选
- 按关系数量筛选
- 按标注员筛选（管理员）

### 2. 批量操作
- 批量更新任务状态
- 批量重新分配任务
- 批量导出任务

### 3. 任务优先级
- 支持任务优先级设置
- 按优先级排序
- 优先级提醒

### 4. 实时更新
- 使用WebSocket推送任务状态更新
- 实时显示其他用户的标注进度

### 5. 任务统计
- 标注员工作量统计
- 任务完成率统计
- 标注质量统计

## Conclusion

本设计文档详细描述了基于角色的任务列表权限控制功能的技术实现方案。通过复用现有的 `DatasetAssignmentService`，创建统一的 `TaskQueryService` 和权限装饰器，我们可以高效地实现权限控制，同时保持代码的可维护性和可扩展性。

关键设计决策：
1. **复用现有逻辑**：避免重复实现权限检查
2. **数据库层过滤**：提高查询效率
3. **统一权限控制**：使用装饰器模式
4. **向后兼容**：保持现有API的行为不变
5. **浏览员使用数据集页面**：简化架构，避免冗余

通过21个correctness properties，我们确保了系统的正确性和可测试性。通过详细的测试策略，我们可以验证系统在各种场景下的行为。
