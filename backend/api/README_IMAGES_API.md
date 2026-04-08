# 图片标注API文档

## 概述

图片标注API提供了对图片实体的完整CRUD操作,支持两种标注模式:
1. **整图标注**: 对整张图片进行分类标注
2. **区域标注**: 使用边界框(Bounding Box)标注图片中的特定区域

## API端点列表

### 1. 添加图片实体

**端点**: `POST /api/v1/images/{image_id}/entities`

**描述**: 为指定图片添加实体标注

**路径参数**:
- `image_id` (string): 图片ID

**请求体参数**:
- `task_id` (string, 必需): 标注任务ID
- `label` (string, 必需): 实体标签
- `bbox_x` (integer, 可选): 边界框X坐标
- `bbox_y` (integer, 可选): 边界框Y坐标
- `bbox_width` (integer, 可选): 边界框宽度
- `bbox_height` (integer, 可选): 边界框高度
- `confidence` (float, 可选): 置信度(0-1)

**标注模式**:
- **整图标注**: 不提供任何边界框参数
- **区域标注**: 必须提供完整的边界框参数(x, y, width, height)

**请求示例 - 整图标注**:
```json
{
  "task_id": "task-abc123",
  "label": "产品图片"
}
```

**请求示例 - 区域标注**:
```json
{
  "task_id": "task-abc123",
  "label": "缺陷区域",
  "bbox_x": 100,
  "bbox_y": 150,
  "bbox_width": 200,
  "bbox_height": 180
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "图片实体添加成功",
  "data": {
    "id": 1,
    "entity_id": "img-entity-a1b2c3d4",
    "image_id": "img-001",
    "label": "缺陷区域",
    "annotation_type": "region",
    "bbox": {
      "x": 100,
      "y": 150,
      "width": 200,
      "height": 180
    },
    "confidence": null
  }
}
```

**错误响应**:
- `400`: 边界框参数不完整或超出图片范围
- `404`: 图片或任务不存在
- `500`: 服务器内部错误

---

### 2. 获取图片实体列表

**端点**: `GET /api/v1/images/{image_id}/entities`

**描述**: 获取指定图片的所有实体标注

**路径参数**:
- `image_id` (string): 图片ID

**查询参数**:
- `task_id` (string, 可选): 筛选特定任务的图片实体

**响应示例**:
```json
{
  "success": true,
  "message": "获取图片实体列表成功",
  "data": {
    "image_id": "img-001",
    "image_info": {
      "file_path": "/data/images/img-001.jpg",
      "width": 1920,
      "height": 1080
    },
    "total": 2,
    "entities": [
      {
        "id": 1,
        "entity_id": "img-entity-a1b2c3d4",
        "task_id": "task-abc123",
        "label": "缺陷区域",
        "annotation_type": "region",
        "bbox": {
          "x": 100,
          "y": 150,
          "width": 200,
          "height": 180
        },
        "confidence": 0.95,
        "version": 1,
        "created_at": "2024-01-19T10:30:00"
      },
      {
        "id": 2,
        "entity_id": "img-entity-e5f6g7h8",
        "task_id": "task-abc123",
        "label": "产品图片",
        "annotation_type": "whole_image",
        "bbox": null,
        "confidence": null,
        "version": 1,
        "created_at": "2024-01-19T10:31:00"
      }
    ]
  }
}
```

**错误响应**:
- `404`: 图片不存在
- `500`: 服务器内部错误

---

### 3. 更新图片实体

**端点**: `PUT /api/v1/images/{image_id}/entities/{entity_id}`

**描述**: 更新指定的图片实体标注

**路径参数**:
- `image_id` (string): 图片ID
- `entity_id` (integer): 实体ID

**请求体参数** (所有参数可选):
- `label` (string): 实体标签
- `bbox_x` (integer): 边界框X坐标
- `bbox_y` (integer): 边界框Y坐标
- `bbox_width` (integer): 边界框宽度
- `bbox_height` (integer): 边界框高度
- `confidence` (float): 置信度

**注意事项**:
- 如果要更新边界框,必须提供完整的边界框参数(x, y, width, height)
- 边界框必须在图片范围内
- 更新操作会自动将任务标记为手动标注

**请求示例**:
```json
{
  "label": "严重缺陷",
  "bbox_x": 120,
  "bbox_y": 160,
  "bbox_width": 220,
  "bbox_height": 200,
  "confidence": 0.98
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "图片实体更新成功",
  "data": {
    "id": 1,
    "entity_id": "img-entity-a1b2c3d4",
    "image_id": "img-001",
    "label": "严重缺陷",
    "annotation_type": "region",
    "bbox": {
      "x": 120,
      "y": 160,
      "width": 220,
      "height": 200
    },
    "confidence": 0.98
  }
}
```

**错误响应**:
- `400`: 边界框参数不完整或超出图片范围
- `404`: 图片或实体不存在
- `500`: 服务器内部错误

---

### 4. 删除图片实体

**端点**: `DELETE /api/v1/images/{image_id}/entities/{entity_id}`

**描述**: 删除指定的图片实体标注

**路径参数**:
- `image_id` (string): 图片ID
- `entity_id` (integer): 实体ID

**响应示例**:
```json
{
  "success": true,
  "message": "图片实体删除成功"
}
```

**错误响应**:
- `404`: 图片或实体不存在
- `500`: 服务器内部错误

---

## 数据模型

### ImageEntity (图片实体)

```python
{
  "id": int,                    # 数据库主键
  "entity_id": str,             # 实体唯一标识
  "task_id": int,               # 关联的标注任务ID
  "image_id": int,              # 关联的图片ID
  "label": str,                 # 实体标签
  "bbox_x": int | null,         # 边界框X坐标(整图标注时为null)
  "bbox_y": int | null,         # 边界框Y坐标
  "bbox_width": int | null,     # 边界框宽度
  "bbox_height": int | null,    # 边界框高度
  "confidence": float | null,   # 置信度(0-1)
  "version": int,               # 版本号
  "created_at": datetime        # 创建时间
}
```

### 标注类型

- `whole_image`: 整图标注 - bbox参数全部为null
- `region`: 区域标注 - 包含完整的bbox参数

---

## 使用场景

### 场景1: 整图分类标注

对整张图片进行分类,例如判断图片类型、质量等级等。

```python
# 添加整图标注
POST /api/v1/images/img-001/entities
{
  "task_id": "task-abc123",
  "label": "合格产品"
}
```

### 场景2: 缺陷区域标注

使用边界框标注图片中的缺陷区域。

```python
# 添加区域标注
POST /api/v1/images/img-001/entities
{
  "task_id": "task-abc123",
  "label": "划痕",
  "bbox_x": 100,
  "bbox_y": 150,
  "bbox_width": 200,
  "bbox_height": 180
}
```

### 场景3: 多区域标注

一张图片可以包含多个标注区域。

```python
# 标注第一个缺陷
POST /api/v1/images/img-001/entities
{
  "task_id": "task-abc123",
  "label": "划痕",
  "bbox_x": 100,
  "bbox_y": 150,
  "bbox_width": 200,
  "bbox_height": 180
}

# 标注第二个缺陷
POST /api/v1/images/img-001/entities
{
  "task_id": "task-abc123",
  "label": "污渍",
  "bbox_x": 500,
  "bbox_y": 300,
  "bbox_width": 150,
  "bbox_height": 120
}
```

---

## 边界框坐标系统

边界框使用标准的图片坐标系统:
- 原点(0, 0)位于图片左上角
- X轴向右递增
- Y轴向下递增
- 边界框由左上角坐标(x, y)和尺寸(width, height)定义

```
(0,0) ────────────────> X
  │
  │    (x,y)
  │      ┌─────────┐
  │      │         │ height
  │      │         │
  │      └─────────┘
  │         width
  │
  v Y
```

---

## 验证规则

### 边界框验证

1. **完整性验证**: 区域标注必须提供完整的边界框参数(x, y, width, height)
2. **范围验证**: 边界框必须在图片范围内
   - `bbox_x >= 0`
   - `bbox_y >= 0`
   - `bbox_x + bbox_width <= image.width`
   - `bbox_y + bbox_height <= image.height`

### 标签验证

- 标签必须是非空字符串
- 建议使用标签配置系统中定义的标签

---

## 错误处理

所有API端点遵循统一的错误响应格式:

```json
{
  "detail": "错误描述信息"
}
```

常见错误码:
- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误

---

## 最佳实践

1. **边界框精度**: 使用整数像素坐标,确保边界框准确框选目标区域
2. **标签一致性**: 使用标签配置系统中定义的标签,保持标注一致性
3. **版本管理**: 图片实体支持版本控制,修改会创建新版本
4. **批量操作**: 对于大量图片标注,建议使用批处理方式
5. **坐标验证**: 在前端绘制边界框时,实时验证坐标是否在图片范围内

---

## 集成示例

### 前端集成示例 (Vue3 + TypeScript)

```typescript
// 添加区域标注
async function addRegionAnnotation(
  imageId: string,
  taskId: string,
  label: string,
  bbox: { x: number; y: number; width: number; height: number }
) {
  const response = await fetch(`/api/v1/images/${imageId}/entities`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      task_id: taskId,
      label: label,
      bbox_x: bbox.x,
      bbox_y: bbox.y,
      bbox_width: bbox.width,
      bbox_height: bbox.height
    })
  });
  
  return await response.json();
}

// 获取图片所有标注
async function getImageAnnotations(imageId: string, taskId?: string) {
  const url = new URL(`/api/v1/images/${imageId}/entities`);
  if (taskId) {
    url.searchParams.append('task_id', taskId);
  }
  
  const response = await fetch(url.toString());
  return await response.json();
}
```

---

## 相关需求

本API实现满足以下需求:
- Requirements 5.4: 图片实体标注
- Requirements 5.5: 边界框标注
- Requirements 12.3: 整图标注
- Requirements 12.5: 区域标注
- Requirements 12.6: 边界框编辑
- Requirements 12.7: 边界框删除
