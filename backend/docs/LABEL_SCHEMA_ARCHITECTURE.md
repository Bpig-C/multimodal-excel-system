# 标签配置体系架构说明

## 概述

本系统采用**全局标签配置 + 版本快照**的架构，确保数据集标注的一致性和可追溯性。

## 核心概念

### 1. 全局标签配置（Global Label Configuration）

系统维护一套**全局的**实体类型和关系类型配置：

- **实体类型表** (`entity_types`)：存储所有可用的实体类型定义
- **关系类型表** (`relation_types`)：存储所有可用的关系类型定义

这些配置是**动态的**，可以随时添加、修改、删除。

**表结构关键字段：**
```python
class EntityType:
    id: int                    # 主键
    type_name: str             # 英文名称（唯一）
    type_name_zh: str          # 中文名称
    color: str                 # 显示颜色
    description: str           # 描述
    definition: str            # LLM生成的标准定义
    examples: str              # 示例（JSON格式）
    disambiguation: str        # 类别辨析
    supports_bbox: bool        # 是否支持边界框
    is_active: bool            # 是否活跃
    is_reviewed: bool          # 是否已审核
```

### 2. 标签体系版本（Label Schema Version）

为了保证数据集标注的一致性，系统使用**版本快照机制**：

**表结构：**
```python
class LabelSchemaVersion:
    id: int                    # 主键
    version_id: str            # 版本ID（唯一）
    version_name: str          # 版本名称（如 "品质失效v1.0"）
    description: str           # 版本描述
    schema_data: str           # JSON格式的完整标签配置快照
    is_active: bool            # 是否为当前活跃版本
    created_by: int            # 创建人
    created_at: datetime       # 创建时间
```

**schema_data 内容示例：**
```json
{
  "entity_types": [
    {
      "id": 1,
      "type_name": "product_model",
      "type_name_zh": "产品型号",
      "color": "#FF5722",
      "description": "产品的型号标识",
      ...
    }
  ],
  "relation_types": [
    {
      "id": 1,
      "type_name": "causes",
      "type_name_zh": "导致",
      "color": "#2196F3",
      ...
    }
  ]
}
```

### 3. 数据集与版本绑定

每个数据集在**创建时**绑定一个标签体系版本：

```python
class Dataset:
    id: int
    dataset_id: str
    name: str
    description: str
    label_schema_version_id: int  # 绑定的标签版本ID
    created_by: int
    created_at: datetime
```

## 工作流程

### 创建数据集流程

```
1. 用户在标签管理页面配置实体类型和关系类型
   ↓
2. 用户创建版本快照（可选，或使用默认活跃版本）
   - 系统将当前所有活跃的标签配置保存为JSON快照
   ↓
3. 用户创建数据集
   - 选择要使用的标签体系版本
   - 系统将 label_schema_version_id 保存到数据集记录
   ↓
4. 数据集创建完成
   - 数据集永久绑定该版本的标签配置
```

### 标注任务流程

```
1. 用户进入标注页面
   ↓
2. 前端加载任务数据
   - 获取任务所属的 dataset_id
   ↓
3. 前端加载标签配置
   - 当前实现：加载全局活跃的标签配置
   - 理想实现：根据数据集的 label_schema_version_id 加载对应版本的配置
   ↓
4. 用户进行标注
   - 实体的 label 字段存储实体类型名称（type_name 或 type_name_zh）
   - 关系的 relation_type 字段存储关系类型名称
   ↓
5. 前端显示时匹配颜色
   - 根据 label 名称在 entityTypes 中查找对应的 color
```

## 关键问题解答

### Q1: 当前匹配的是数据集配置还是全局配置？

**当前实现：** 匹配的是**全局活跃配置**

```typescript
// frontend/src/views/annotation/AnnotationPage.vue
onMounted(async () => {
  // 加载全局活跃的标签配置
  await labelStore.fetchEntityTypes({ include_inactive: false })
  await labelStore.fetchRelationTypes({ include_inactive: false })
  
  // 加载任务数据
  await loadTaskData()
})
```

**问题：** 如果全局配置被修改（如修改颜色、删除类型），已有数据集的标注显示可能会出现问题。

### Q2: 每个数据集有自己的配置吗？

**是的，但是通过版本快照实现：**

- 每个数据集绑定一个 `label_schema_version_id`
- 该版本的 `schema_data` 字段存储了创建时的完整标签配置快照
- 这个快照是**不可变的**，保证了数据集标注的一致性

### Q3: 配置是创建数据集时使用的全局配置吗？

**是的：**

1. 创建数据集时，用户选择一个标签体系版本（或使用默认活跃版本）
2. 该版本的 `schema_data` 包含了创建版本快照时的全局配置
3. 数据集永久绑定该版本

### Q4: 创建数据集后还能修改配置吗？

**当前设计：不能直接修改**

- 数据集绑定的版本是固定的
- 如果需要使用新的标签配置，应该：
  1. 创建新的标签体系版本快照
  2. 创建新的数据集并绑定新版本

**原因：** 保证标注一致性，避免标注过程中配置变化导致的混乱

## 当前实现的问题

### 问题1: 前端未使用数据集的版本配置

**现状：**
- 前端加载的是全局活跃配置，而不是数据集绑定的版本配置
- 如果全局配置被修改，已有数据集的显示会受影响

**解决方案：**
```typescript
// 应该实现的逻辑
async function loadTaskData() {
  // 1. 获取任务信息（包含 dataset_id）
  const task = await getAnnotationTask(taskId)
  
  // 2. 获取数据集信息（包含 label_schema_version_id）
  const dataset = await getDataset(task.dataset_id)
  
  // 3. 获取版本的标签配置快照
  const version = await getVersion(dataset.label_schema_version_id)
  
  // 4. 使用版本快照中的配置
  entityTypes.value = version.schema_data.entity_types
  relationTypes.value = version.schema_data.relation_types
}
```

### 问题2: 后端API缺少按版本查询的接口

**需要添加的API：**
```python
@router.get("/versions/{version_id}")
async def get_version(version_id: str):
    """获取版本详情，包含完整的标签配置快照"""
    pass

@router.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: str):
    """获取数据集详情，包含 label_schema_version_id"""
    pass
```

## 推荐的改进方案

### 短期方案（快速修复）

保持当前使用全局配置的方式，但添加警告机制：
- 在标签管理页面修改配置时，提示"修改会影响所有使用该配置的数据集"
- 建议用户在修改前创建新版本快照

### 长期方案（完整实现）

1. **前端改造：**
   - 标注页面根据数据集的版本ID加载配置
   - 添加数据集详情API调用
   - 添加版本详情API调用

2. **后端改造：**
   - 完善版本查询API
   - 数据集详情API返回版本信息
   - 标注任务API返回数据集的版本信息

3. **版本管理增强：**
   - 版本对比功能
   - 版本迁移工具（将旧版本数据集迁移到新版本）
   - 版本使用统计

## 数据流图

```
┌─────────────────┐
│  全局标签配置    │
│  EntityTypes    │
│  RelationTypes  │
└────────┬────────┘
         │
         │ 创建快照
         ↓
┌─────────────────┐
│  标签体系版本    │
│  schema_data    │
│  (JSON快照)     │
└────────┬────────┘
         │
         │ 绑定
         ↓
┌─────────────────┐
│     数据集       │
│  label_schema_  │
│  version_id     │
└────────┬────────┘
         │
         │ 包含
         ↓
┌─────────────────┐
│    标注任务      │
│   entities      │
│   relations     │
└─────────────────┘
```

## 总结

1. **全局配置**：系统维护一套可动态修改的全局标签配置
2. **版本快照**：创建数据集时，将全局配置保存为不可变的版本快照
3. **数据集绑定**：每个数据集绑定一个版本，保证标注一致性
4. **当前问题**：前端使用全局配置而非数据集版本配置，需要改进
5. **改进方向**：实现基于版本的配置加载机制

## 相关文件

- 数据库模型：`backend/models/db_models.py`
- 数据集API：`backend/api/dataset.py`
- 标签API：`backend/api/labels.py`
- 前端标注页面：`frontend/src/views/annotation/AnnotationPage.vue`
- 标签Store：`frontend/src/stores/label.ts`
