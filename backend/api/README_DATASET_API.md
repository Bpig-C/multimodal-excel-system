# 数据集管理API文档

## 概述

数据集管理API提供数据集的完整CRUD操作，包括创建、查询、更新、删除、统计和导出功能。

## API端点

### 1. 创建数据集

**端点**: `POST /api/v1/datasets`

**描述**: 创建新的数据集，关联语料，自动创建标注任务

**请求体**:
```json
{
  "name": "品质失效案例数据集v1",
  "description": "用于训练品质失效分析模型的数据集",
  "corpus_ids": [1, 2, 3, 4, 5],
  "created_by": 1,
  "label_schema_version_id": 1
}
```

**响应**:
```json
{
  "success": true,
  "message": "数据集创建成功",
  "data": {
    "id": 1,
    "dataset_id": "DS_20240119_001",
    "name": "品质失效案例数据集v1",
    "description": "用于训练品质失效分析模型的数据集",
    "label_schema_version_id": 1,
    "created_by": 1,
    "created_at": "2024-01-19T10:30:00Z",
    "updated_at": "2024-01-19T10:30:00Z"
  }
}
```

**功能说明**:
- 创建数据集记录
- 关联指定的语料（通过corpus_ids）
- 为每个语料自动创建标注任务（状态为pending）
- 绑定到指定的标签体系版本（可选）

---

### 2. 获取数据集列表

**端点**: `GET /api/v1/datasets`

**描述**: 获取数据集列表，支持分页和筛选

**查询参数**:
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20，最大100）
- `name`: 数据集名称筛选（可选）
- `created_by`: 创建人ID筛选（可选）

**示例请求**:
```
GET /api/v1/datasets?page=1&page_size=20&name=品质失效
```

**响应**:
```json
{
  "success": true,
  "message": "获取数据集列表成功",
  "data": {
    "items": [
      {
        "id": 1,
        "dataset_id": "DS_20240119_001",
        "name": "品质失效案例数据集v1",
        "description": "用于训练品质失效分析模型的数据集",
        "label_schema_version_id": 1,
        "created_by": 1,
        "created_at": "2024-01-19T10:30:00Z",
        "updated_at": "2024-01-19T10:30:00Z",
        "corpus_count": 5,
        "task_count": 5
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20
  }
}
```

---

### 3. 获取数据集详情

**端点**: `GET /api/v1/datasets/{dataset_id}`

**描述**: 获取指定数据集的详细信息，包括关联的语料和任务

**示例请求**:
```
GET /api/v1/datasets/DS_20240119_001
```

**响应**:
```json
{
  "success": true,
  "message": "获取数据集详情成功",
  "data": {
    "id": 1,
    "dataset_id": "DS_20240119_001",
    "name": "品质失效案例数据集v1",
    "description": "用于训练品质失效分析模型的数据集",
    "label_schema_version_id": 1,
    "created_by": 1,
    "created_at": "2024-01-19T10:30:00Z",
    "updated_at": "2024-01-19T10:30:00Z",
    "corpus_list": [
      {
        "id": 1,
        "text_id": "C_001",
        "text": "产品外观有划痕...",
        "text_type": "问题描述",
        "has_images": true
      }
    ],
    "task_list": [
      {
        "id": 1,
        "task_id": "T_001",
        "corpus_id": 1,
        "status": "pending",
        "annotation_type": "automatic",
        "current_version": 1
      }
    ]
  }
}
```

---

### 4. 更新数据集

**端点**: `PUT /api/v1/datasets/{dataset_id}`

**描述**: 更新数据集的名称和描述

**请求体**:
```json
{
  "name": "品质失效案例数据集v1.1",
  "description": "更新后的描述"
}
```

**响应**:
```json
{
  "success": true,
  "message": "数据集更新成功",
  "data": {
    "id": 1,
    "dataset_id": "DS_20240119_001",
    "name": "品质失效案例数据集v1.1",
    "description": "更新后的描述",
    "label_schema_version_id": 1,
    "created_by": 1,
    "created_at": "2024-01-19T10:30:00Z",
    "updated_at": "2024-01-19T11:00:00Z"
  }
}
```

---

### 5. 删除数据集

**端点**: `DELETE /api/v1/datasets/{dataset_id}`

**描述**: 删除数据集及其所有关联数据（级联删除）

**示例请求**:
```
DELETE /api/v1/datasets/DS_20240119_001
```

**响应**:
```json
{
  "success": true,
  "message": "数据集删除成功"
}
```

**级联删除内容**:
- 数据集记录
- 数据集-语料关联记录
- 所有标注任务
- 所有文本实体
- 所有图片实体
- 所有关系
- 所有版本历史
- 所有复核任务
- 所有批量任务

---

### 6. 获取数据集统计

**端点**: `GET /api/v1/datasets/{dataset_id}/statistics`

**描述**: 获取数据集的统计信息

**示例请求**:
```
GET /api/v1/datasets/DS_20240119_001/statistics
```

**响应**:
```json
{
  "success": true,
  "message": "获取统计信息成功",
  "data": {
    "dataset_id": "DS_20240119_001",
    "total_tasks": 5,
    "pending_tasks": 2,
    "processing_tasks": 0,
    "completed_tasks": 3,
    "failed_tasks": 0,
    "completion_rate": 0.6,
    "entity_count": 45,
    "relation_count": 38,
    "avg_entities_per_task": 9.0,
    "avg_relations_per_task": 7.6
  }
}
```

**统计指标说明**:
- `total_tasks`: 总任务数
- `pending_tasks`: 待处理任务数
- `processing_tasks`: 处理中任务数
- `completed_tasks`: 已完成任务数
- `failed_tasks`: 失败任务数
- `completion_rate`: 完成率（0-1）
- `entity_count`: 实体总数
- `relation_count`: 关系总数
- `avg_entities_per_task`: 平均每任务实体数
- `avg_relations_per_task`: 平均每任务关系数

---

### 7. 导出数据集

**端点**: `POST /api/v1/datasets/{dataset_id}/export`

**描述**: 导出数据集为JSONL格式

**请求体**:
```json
{
  "output_path": "./data/exports/dataset_001.jsonl",
  "status_filter": ["completed"]
}
```

**响应**:
```json
{
  "success": true,
  "message": "数据集导出成功",
  "data": {
    "export_path": "./data/exports/dataset_001.jsonl"
  }
}
```

**导出格式**:

每行一个JSON对象：
```json
{
  "text_id": "C_001",
  "text": "产品外观有划痕，经检查发现是焊接工序中操作不当导致。",
  "entities": [
    {"id": 0, "token": "产品", "label": "Product", "start_offset": 0, "end_offset": 2},
    {"id": 1, "token": "划痕", "label": "DefectPhenomenon", "start_offset": 5, "end_offset": 7}
  ],
  "relations": [
    {"id": 0, "from_id": 0, "to_id": 1, "type": "has_defect"}
  ]
}
```

**状态筛选**:
- `pending`: 待处理
- `processing`: 处理中
- `completed`: 已完成
- `failed`: 失败

---

## 错误处理

### 常见错误码

**400 Bad Request**:
- 请求参数验证失败
- 语料ID不存在
- 数据格式错误

```json
{
  "detail": "语料ID [999] 不存在"
}
```

**404 Not Found**:
- 数据集不存在

```json
{
  "detail": "数据集不存在"
}
```

**500 Internal Server Error**:
- 服务器内部错误
- 数据库操作失败

```json
{
  "detail": "创建数据集失败: 数据库连接错误"
}
```

---

## 使用示例

### Python示例

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. 创建数据集
response = requests.post(
    f"{BASE_URL}/api/v1/datasets",
    json={
        "name": "测试数据集",
        "description": "这是一个测试数据集",
        "corpus_ids": [1, 2, 3],
        "created_by": 1
    }
)
dataset = response.json()
dataset_id = dataset["data"]["dataset_id"]

# 2. 获取数据集列表
response = requests.get(f"{BASE_URL}/api/v1/datasets?page=1&page_size=10")
datasets = response.json()

# 3. 获取数据集详情
response = requests.get(f"{BASE_URL}/api/v1/datasets/{dataset_id}")
detail = response.json()

# 4. 获取统计信息
response = requests.get(f"{BASE_URL}/api/v1/datasets/{dataset_id}/statistics")
stats = response.json()

# 5. 导出数据集
response = requests.post(
    f"{BASE_URL}/api/v1/datasets/{dataset_id}/export",
    json={
        "output_path": "./export.jsonl",
        "status_filter": ["completed"]
    }
)
export_result = response.json()

# 6. 更新数据集
response = requests.put(
    f"{BASE_URL}/api/v1/datasets/{dataset_id}",
    json={
        "name": "更新后的名称",
        "description": "更新后的描述"
    }
)

# 7. 删除数据集
response = requests.delete(f"{BASE_URL}/api/v1/datasets/{dataset_id}")
```

### JavaScript示例

```javascript
const BASE_URL = "http://localhost:8000";

// 创建数据集
async function createDataset() {
  const response = await fetch(`${BASE_URL}/api/v1/datasets`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      name: "测试数据集",
      description: "这是一个测试数据集",
      corpus_ids: [1, 2, 3],
      created_by: 1
    })
  });
  
  const data = await response.json();
  return data.data.dataset_id;
}

// 获取数据集列表
async function listDatasets(page = 1, pageSize = 20) {
  const response = await fetch(
    `${BASE_URL}/api/v1/datasets?page=${page}&page_size=${pageSize}`
  );
  return await response.json();
}

// 获取数据集详情
async function getDataset(datasetId) {
  const response = await fetch(`${BASE_URL}/api/v1/datasets/${datasetId}`);
  return await response.json();
}

// 导出数据集
async function exportDataset(datasetId) {
  const response = await fetch(
    `${BASE_URL}/api/v1/datasets/${datasetId}/export`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        output_path: "./export.jsonl",
        status_filter: ["completed"]
      })
    }
  );
  return await response.json();
}
```

---

## 注意事项

1. **级联删除**: 删除数据集会级联删除所有关联数据，操作不可逆，请谨慎使用

2. **标签体系版本**: 创建数据集时可以指定标签体系版本，用于版本管理和数据追溯

3. **自动任务创建**: 创建数据集时会自动为每个语料创建标注任务，初始状态为pending

4. **分页限制**: 列表查询最大每页100条记录

5. **导出格式**: 导出的JSONL文件每行一个JSON对象，便于流式处理大数据集

6. **状态筛选**: 导出时可以按任务状态筛选，只导出特定状态的数据

---

## 相关文档

- [语料管理API](./README_CORPUS_API.md)
- [标注任务API](./README_ANNOTATION_API.md)
- [数据集服务](../services/dataset_service.py)
- [数据库模型](../models/db_models.py)
