# API 影响分析

## 现有API分析

### 1. 数据集任务列表API（已存在）
**端点**: `GET /api/v1/datasets/{dataset_id}/tasks`
**文件**: `backend/api/dataset.py:318`

**当前功能**:
- 获取指定数据集的任务列表
- 支持分页（page, page_size）
- 支持按状态筛选（status）
- 返回任务详情（语料文本、实体数、关系数）

**缺少的功能**:
- ❌ 没有权限过滤（任何人都能看到所有任务）
- ❌ 没有基于 DatasetAssignment 的任务范围过滤
- ❌ 没有角色检查

**需要增强**:
- ✅ 添加权限检查（基于用户角色和 DatasetAssignment）
- ✅ 标注员只能看到分配给他的任务范围
- ✅ 浏览员只能看到已完成的任务
- ✅ 管理员可以看到所有任务

---

### 2. 单个任务详情API（已存在）
**端点**: `GET /api/v1/annotations/{task_id}`
**文件**: `backend/api/annotations.py:98`

**当前功能**:
- 获取单个任务的详细信息
- 包含语料、实体、关系

**缺少的功能**:
- ❌ 没有权限检查

**需要增强**:
- ✅ 添加权限检查
- ✅ 标注员只能访问分配给他的任务
- ✅ 浏览员只能访问已完成的任务

---

### 3. 任务更新API（已存在）
**端点**: `PUT /api/v1/annotations/{task_id}`
**文件**: `backend/api/annotations.py:145`

**当前功能**:
- 更新任务状态

**缺少的功能**:
- ❌ 没有权限检查

**需要增强**:
- ✅ 添加权限检查
- ✅ 标注员只能更新分配给他的任务
- ✅ 浏览员不能更新任何任务

---

## 需要新增的API

### 1. 跨数据集任务列表API（新增）
**端点**: `GET /api/v1/annotations`
**用途**: 标注员和管理员的工作台

**功能**:
- 获取用户可访问的所有任务（跨数据集）
- 支持分页
- 支持筛选（数据集、状态、分配人）
- 支持排序
- 自动根据角色过滤：
  - 管理员：所有任务
  - 标注员：分配给自己的任务

**查询参数**:
- `page`: 页码
- `page_size`: 每页数量
- `dataset_id`: 数据集筛选（可选）
- `status`: 状态筛选（可选）
- `sort_by`: 排序字段（可选）
- `sort_order`: 排序方向（可选）

---

## 数据集分配服务（已存在）

**文件**: `backend/services/dataset_assignment_service.py`

**已有功能**:
- ✅ `check_permission()`: 检查用户权限
- ✅ `get_user_task_range()`: 获取用户的任务范围
- ✅ `get_user_datasets()`: 获取用户的数据集列表
- ✅ `_get_tasks_in_range()`: 获取范围内的任务

**可以复用**:
- 权限检查逻辑
- 任务范围过滤逻辑

---

## 实施策略

### 阶段1：增强现有API
1. 在 `GET /api/v1/datasets/{dataset_id}/tasks` 添加权限过滤
2. 在 `GET /api/v1/annotations/{task_id}` 添加权限检查
3. 在 `PUT /api/v1/annotations/{task_id}` 添加权限检查

### 阶段2：新增跨数据集API
1. 创建 `GET /api/v1/annotations` 端点
2. 实现基于角色的任务查询逻辑
3. 支持筛选和排序

### 阶段3：前端实现
1. 创建任务列表页面组件
2. 集成API调用
3. 实现筛选和排序UI

---

## 权限矩阵

| API端点 | 管理员 | 标注员 | 浏览员 |
|---------|--------|--------|--------|
| `GET /api/v1/annotations` | 所有任务 | 分配的任务 | ❌ 不使用 |
| `GET /api/v1/datasets/{id}/tasks` | 所有任务 | 分配的任务 | 已完成任务 |
| `GET /api/v1/annotations/{id}` | 所有任务 | 分配的任务 | 已完成任务 |
| `PUT /api/v1/annotations/{id}` | 所有任务 | 分配的任务 | ❌ 禁止 |
| `POST /api/v1/annotations/{id}/entities` | 所有任务 | 分配的任务 | ❌ 禁止 |
| `PUT /api/v1/annotations/{id}/entities/{eid}` | 所有任务 | 分配的任务 | ❌ 禁止 |
| `DELETE /api/v1/annotations/{id}/entities/{eid}` | 所有任务 | 分配的任务 | ❌ 禁止 |

---

## 避免冗余的策略

1. **复用 DatasetAssignmentService**
   - 不重复实现权限检查逻辑
   - 使用现有的 `check_permission()` 和 `get_user_task_range()`

2. **统一权限装饰器**
   - 创建 `@require_task_permission` 装饰器
   - 在所有任务相关API中复用

3. **统一任务查询逻辑**
   - 创建 `TaskQueryService` 封装任务查询逻辑
   - 避免在多个API中重复相同的查询代码
