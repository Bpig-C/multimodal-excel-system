# 标签管理API文档

## 概述

标签管理API提供实体类型、关系类型的CRUD操作,以及标签定义生成、审核、导入导出、版本管理等功能。

**Base URL**: `/api/v1/labels`

---

## 实体类型管理

### 1. 获取实体类型列表

**接口**: `GET /entities`

**查询参数**:
- `include_inactive` (boolean, 可选): 是否包含不活跃的类型,默认false
- `include_unreviewed` (boolean, 可选): 是否包含未审核的类型,默认true

**响应示例**:
```json
{
  "success": true,
  "message": "获取实体类型列表成功",
  "data": {
    "items": [
      {
        "id": 1,
        "type_name": "Product",
        "type_name_zh": "产品",
        "color": "#1f77b4",
        "description": "具体的产品名称、型号、部件",
        "definition": "产品是指制造过程中的具体产出物...",
        "examples": "[\"电机\", \"控制器\", \"显示屏\"]",
        "disambiguation": "产品与物料的区别...",
        "supports_bbox": false,
        "is_active": true,
        "is_reviewed": true,
        "reviewed_by": 1,
        "reviewed_at": "2024-01-19T10:30:00Z",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-19T10:30:00Z"
      }
    ],
    "total": 16
  }
}
```

### 2. 创建实体类型

**接口**: `POST /entities`

**请求体**:
```json
{
  "type_name": "Product",
  "type_name_zh": "产品",
  "color": "#1f77b4",
  "description": "具体的产品名称、型号、部件",
  "supports_bbox": false
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "实体类型创建成功",
  "data": {
    "id": 1,
    "type_name": "Product",
    "type_name_zh": "产品",
    "color": "#1f77b4",
    "is_reviewed": false
  }
}
```

### 3. 更新实体类型

**接口**: `PUT /entities/{entity_type_id}`

**请求体** (所有字段可选):
```json
{
  "type_name": "Product",
  "type_name_zh": "产品型号",
  "color": "#2f87c4",
  "description": "更新后的描述",
  "supports_bbox": true
}
```

### 4. 删除实体类型

**接口**: `DELETE /entities/{entity_type_id}`

**说明**: 软删除,将`is_active`设置为false

### 5. 生成实体类型定义

**接口**: `POST /entities/{entity_type_id}/generate-definition`

**说明**: 调用LLM自动生成详细定义、示例和类别辨析

**响应示例**:
```json
{
  "success": true,
  "message": "定义生成成功",
  "data": {
    "definition": "产品是指制造过程中的具体产出物,包括最终产品、半成品、零部件等...",
    "examples": ["电机", "控制器", "显示屏", "XX型号主板", "传感器"],
    "disambiguation": "产品与物料的区别:产品是制造的输出,物料是制造的输入..."
  }
}
```

### 6. 审核实体类型定义

**接口**: `POST /entities/{entity_type_id}/review`

**请求体**:
```json
{
  "reviewed_by": 1,
  "definition": "用户编辑后的定义",
  "examples": ["示例1", "示例2", "示例3"],
  "disambiguation": "用户编辑后的辨析"
}
```

**说明**: 
- 用户可以编辑LLM生成的内容
- 审核后`is_reviewed`设置为true
- 只有已审核的标签才会用于Agent的Prompt生成

---

## 关系类型管理

### 7. 获取关系类型列表

**接口**: `GET /relations`

**查询参数**: 同实体类型

### 8. 创建关系类型

**接口**: `POST /relations`

**请求体**:
```json
{
  "type_name": "has_defect",
  "type_name_zh": "有缺陷",
  "color": "#3498db",
  "description": "产品/部件存在某种缺陷"
}
```

### 9. 更新关系类型

**接口**: `PUT /relations/{relation_type_id}`

### 10. 删除关系类型

**接口**: `DELETE /relations/{relation_type_id}`

### 11. 生成关系类型定义

**接口**: `POST /relations/{relation_type_id}/generate-definition`

**响应示例**:
```json
{
  "success": true,
  "message": "定义生成成功",
  "data": {
    "definition": "has_defect关系表示产品或部件存在某种缺陷现象...",
    "direction_rule": "Product/Material -> DefectPhenomenon",
    "examples": ["显示屏 --[has_defect]--> 裂纹", "电机 --[has_defect]--> 异响"],
    "disambiguation": "与caused_by的区别:has_defect描述缺陷的存在..."
  }
}
```

### 12. 审核关系类型定义

**接口**: `POST /relations/{relation_type_id}/review`

**请求体**:
```json
{
  "reviewed_by": 1,
  "definition": "用户编辑后的定义",
  "direction_rule": "Product -> DefectPhenomenon",
  "examples": ["示例1", "示例2"],
  "disambiguation": "用户编辑后的辨析"
}
```

---

## 导入导出

### 13. 导入标签配置

**接口**: `POST /import`

**请求体**:
```json
{
  "schema_data": {
    "entity_types": [...],
    "relation_types": [...],
    "metadata": {...}
  },
  "merge": false
}
```

**参数说明**:
- `merge`: 
  - `false`: 替换模式,禁用所有现有标签,导入新标签
  - `true`: 合并模式,保留现有标签,更新或新增

**响应示例**:
```json
{
  "success": true,
  "message": "导入成功",
  "data": {
    "entity_types_created": 5,
    "entity_types_updated": 11,
    "relation_types_created": 2,
    "relation_types_updated": 6
  }
}
```

### 14. 导出标签配置

**接口**: `GET /export`

**响应示例**:
```json
{
  "success": true,
  "message": "导出成功",
  "data": {
    "entity_types": [...],
    "relation_types": [...],
    "metadata": {
      "exported_at": "2024-01-19T10:00:00Z",
      "total_entity_types": 16,
      "total_relation_types": 8
    }
  }
}
```

### 15. 预览Agent Prompt

**接口**: `GET /prompt-preview`

**查询参数**:
- `prompt_type` (string): Prompt类型,可选值: `entity`或`relation`

**响应示例**:
```json
{
  "success": true,
  "message": "获取Prompt预览成功",
  "data": {
    "prompt": "你是一个专业的品质失效案例实体抽取专家...",
    "entity_count": 16,
    "entity_reviewed_count": 14,
    "entity_pending_count": 2,
    "relation_count": 8,
    "relation_reviewed_count": 8,
    "relation_pending_count": 0,
    "total_reviewed": 22,
    "total_pending": 2
  }
}
```

---

## 版本管理

### 16. 获取版本列表

**接口**: `GET /versions`

**响应示例**:
```json
{
  "success": true,
  "message": "获取版本列表成功",
  "data": {
    "versions": [
      {
        "id": 1,
        "version_id": "schema-abc123",
        "version_name": "品质失效v2.0",
        "description": "新增供应商相关实体类型",
        "is_active": true,
        "datasets_count": 5,
        "created_by": 1,
        "created_at": "2024-03-15T10:00:00Z"
      },
      {
        "id": 2,
        "version_id": "schema-def456",
        "version_name": "品质失效v1.0",
        "description": "初始版本",
        "is_active": false,
        "datasets_count": 100,
        "created_by": 1,
        "created_at": "2024-01-01T10:00:00Z"
      }
    ],
    "active_version": "schema-abc123"
  }
}
```

### 17. 创建版本快照

**接口**: `POST /versions/snapshot`

**请求体**:
```json
{
  "version_name": "品质失效v2.0",
  "description": "新增供应商相关实体类型,优化关系定义",
  "created_by": 1
}
```

**说明**: 
- 保存当前标签配置的完整快照
- 新版本默认不活跃,需要手动激活

### 18. 获取版本详情

**接口**: `GET /versions/{version_id}`

**响应示例**:
```json
{
  "success": true,
  "message": "获取版本详情成功",
  "data": {
    "version_id": "schema-abc123",
    "version_name": "品质失效v2.0",
    "description": "新增供应商相关实体类型",
    "is_active": true,
    "entity_types": [...],
    "relation_types": [...],
    "datasets": [
      {"dataset_id": "ds-001", "name": "2024年1月数据"},
      {"dataset_id": "ds-002", "name": "2024年2月数据"}
    ],
    "created_at": "2024-03-15T10:00:00Z"
  }
}
```

### 19. 激活版本

**接口**: `POST /versions/{version_id}/activate`

**说明**: 
- 将指定版本设置为活跃版本
- 新建数据集将使用该版本的标签配置
- 已有数据集不受影响

### 20. 比较版本差异

**接口**: `GET /versions/compare`

**查询参数**:
- `from_version` (string, 必需): 源版本ID
- `to_version` (string, 必需): 目标版本ID

**响应示例**:
```json
{
  "success": true,
  "message": "版本比较成功",
  "data": {
    "from_version": "schema-def456",
    "to_version": "schema-abc123",
    "changes": {
      "entity_types": {
        "added": [
          {"type_name": "Supplier", "type_name_zh": "供应商"}
        ],
        "removed": [
          {"type_name": "OldType", "type_name_zh": "旧类型"}
        ],
        "modified": [
          {
            "type_name": "Product",
            "changes": ["definition", "examples"]
          }
        ]
      },
      "relation_types": {
        "added": [],
        "removed": [],
        "modified": []
      }
    }
  }
}
```

---

## 工作流程

### 完整的标签配置流程

```
1. 创建标签类型
   POST /entities 或 POST /relations
   ↓
2. 生成详细定义(调用LLM)
   POST /entities/{id}/generate-definition
   ↓
3. 人工审核和编辑
   POST /entities/{id}/review
   ↓
4. 预览Prompt效果
   GET /prompt-preview
   ↓
5. 创建版本快照(可选)
   POST /versions/snapshot
   ↓
6. Agent使用新配置进行标注
```

### 版本管理流程

```
1. 创建版本快照
   POST /versions/snapshot
   ↓
2. 在新版本上修改标签
   PUT /entities/{id}
   ↓
3. 激活新版本
   POST /versions/{version_id}/activate
   ↓
4. 新数据集使用新版本
   旧数据集仍使用旧版本
```

---

## 注意事项

1. **审核状态**: 只有`is_reviewed=true`的标签才会用于Agent的Prompt生成
2. **活跃状态**: 只有`is_active=true`的标签才会被使用
3. **缓存机制**: 标签配置更新后会自动清空缓存
4. **版本绑定**: 每个数据集绑定到特定的标签体系版本
5. **软删除**: 删除操作只是将`is_active`设置为false,不会真正删除数据

---

## 错误码

- `404`: 资源不存在
- `500`: 服务器内部错误

所有错误响应格式:
```json
{
  "detail": "错误信息"
}
```
