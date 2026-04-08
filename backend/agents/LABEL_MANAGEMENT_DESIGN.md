# 标签管理系统设计文档

## 概述

本文档描述标签管理系统的完整设计，包括LLM自动生成标签定义、人工审核、动态Prompt生成等功能。

## 核心功能

### 1. 标签定义自动生成

**功能**: 使用LLM自动生成实体类型和关系类型的详细定义

**生成内容**:

#### 实体类型定义
- **标准定义** (definition): 详细说明该实体类型的含义和范围（100-200字）
- **示例列表** (examples): 至少5个典型示例
- **类别辨析** (disambiguation): 与相似类型的区别（50-100字）

#### 关系类型定义
- **标准定义** (definition): 详细说明该关系类型的含义（100-200字）
- **方向规则** (direction_rule): from和to实体的类型约束
- **示例列表** (examples): 至少5个典型示例（格式：实体A --[关系]--> 实体B）
- **类别辨析** (disambiguation): 与相似关系的区别（50-100字）

### 2. 人工审核机制

**审核状态**:
- **待审核** (is_reviewed=False): LLM生成后的初始状态，黄色标识
- **已审核** (is_reviewed=True): 人工确认后的状态，绿色标识

**审核流程**:
1. LLM生成定义后，标记为"待审核"
2. 用户在前端查看生成内容
3. 用户可以编辑修改生成的内容
4. 用户点击"确认审核"，标记为"已审核"
5. 只有已审核的标签才会用于Agent的Prompt生成

### 3. 动态Prompt生成

**核心机制**: Agent的Prompt根据数据库中的标签配置动态生成

**优点**:
- 用户可以自定义标签体系
- 修改标签配置后立即生效
- 支持领域定制化

**实现方式**:
- 标签配置缓存（提升性能）
- 版本号机制（检测配置变化）
- 降级策略（数据库不可用时使用默认配置）

## 数据库设计

### EntityType表扩展

```sql
ALTER TABLE entity_types ADD COLUMN definition TEXT;  -- LLM生成的标准定义
ALTER TABLE entity_types ADD COLUMN examples TEXT;  -- LLM生成的示例（JSON格式）
ALTER TABLE entity_types ADD COLUMN disambiguation TEXT;  -- LLM生成的类别辨析
ALTER TABLE entity_types ADD COLUMN prompt_template TEXT;  -- Prompt模板
ALTER TABLE entity_types ADD COLUMN is_reviewed BOOLEAN DEFAULT FALSE;  -- 是否已审核
ALTER TABLE entity_types ADD COLUMN reviewed_by INTEGER;  -- 审核人
ALTER TABLE entity_types ADD COLUMN reviewed_at TIMESTAMP;  -- 审核时间
ALTER TABLE entity_types ADD COLUMN updated_at TIMESTAMP;  -- 更新时间
```

### RelationType表扩展

```sql
ALTER TABLE relation_types ADD COLUMN definition TEXT;  -- LLM生成的标准定义
ALTER TABLE relation_types ADD COLUMN direction_rule TEXT;  -- LLM生成的方向规则
ALTER TABLE relation_types ADD COLUMN examples TEXT;  -- LLM生成的示例（JSON格式）
ALTER TABLE relation_types ADD COLUMN disambiguation TEXT;  -- LLM生成的类别辨析
ALTER TABLE relation_types ADD COLUMN prompt_template TEXT;  -- Prompt模板
ALTER TABLE relation_types ADD COLUMN is_reviewed BOOLEAN DEFAULT FALSE;  -- 是否已审核
ALTER TABLE relation_types ADD COLUMN reviewed_by INTEGER;  -- 审核人
ALTER TABLE relation_types ADD COLUMN reviewed_at TIMESTAMP;  -- 审核时间
ALTER TABLE relation_types ADD COLUMN updated_at TIMESTAMP;  -- 更新时间
```

## API设计

### 标签定义生成API

```
POST /api/v1/labels/entities/{id}/generate-definition
```

**请求体**:
```json
{
  "type_name": "Product",
  "type_name_zh": "产品",
  "description": "具体的产品名称、型号、部件"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "definition": "产品是指制造过程中的具体产出物，包括最终产品、半成品、零部件等...",
    "examples": ["电机", "控制器", "显示屏", "XX型号主板", "传感器"],
    "disambiguation": "产品与物料的区别：产品是制造的输出，物料是制造的输入..."
  }
}
```

### 标签审核API

```
POST /api/v1/labels/entities/{id}/review
```

**请求体**:
```json
{
  "definition": "用户编辑后的定义",
  "examples": ["示例1", "示例2", "示例3"],
  "disambiguation": "用户编辑后的辨析"
}
```

**响应**:
```json
{
  "success": true,
  "message": "审核完成",
  "data": {
    "is_reviewed": true,
    "reviewed_by": 1,
    "reviewed_at": "2024-01-19T10:30:00Z"
  }
}
```

### Prompt预览API

```
GET /api/v1/labels/prompt-preview?type=entity
```

**响应**:
```json
{
  "success": true,
  "data": {
    "prompt": "你是一个专业的品质失效案例实体抽取专家...\n\n## 实体类型定义\n\n1. **产品** (Product)\n   - 定义: 产品是指...\n   - 示例: 电机, 控制器...\n   - 辨析: 产品与物料的区别...\n\n2. **缺陷现象** (DefectPhenomenon)\n   ...",
    "entity_count": 16,
    "reviewed_count": 14,
    "pending_count": 2
  }
}
```

## 前端设计

### 标签配置页面布局

```
┌─────────────────────────────────────────────────────────┐
│  标签配置                                                │
├─────────────────────────────────────────────────────────┤
│  [实体类型] [关系类型] [导入/导出] [预览Prompt]          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  实体类型列表                                             │
│  ┌────────────────────────────────────────────────┐     │
│  │ ● 产品 (Product)                    [已审核✓]  │     │
│  │   简短描述: 具体的产品名称、型号、部件            │     │
│  │   [查看详情] [编辑] [生成定义] [删除]            │     │
│  ├────────────────────────────────────────────────┤     │
│  │ ● 缺陷现象 (DefectPhenomenon)       [待审核⚠]  │     │
│  │   简短描述: 具体的缺陷表现                       │     │
│  │   [查看详情] [编辑] [生成定义] [删除]            │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  [+ 添加实体类型]                                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 定义生成对话框

```
┌─────────────────────────────────────────────────────────┐
│  生成标签定义 - 产品 (Product)                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  正在调用LLM生成详细定义...                               │
│  [进度条 ████████░░ 80%]                                 │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  生成完成！请审核以下内容：                               │
│                                                          │
│  标准定义:                                                │
│  ┌────────────────────────────────────────────────┐     │
│  │ 产品是指制造过程中的具体产出物，包括最终产品、  │     │
│  │ 半成品、零部件等。产品是质量管理的核心对象...   │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  示例列表:                                                │
│  • 电机                                                  │
│  • 控制器                                                │
│  • 显示屏                                                │
│  • XX型号主板                                            │
│  • 传感器                                                │
│  [+ 添加示例]                                            │
│                                                          │
│  类别辨析:                                                │
│  ┌────────────────────────────────────────────────┐     │
│  │ 产品与物料的区别：产品是制造的输出，物料是制造  │     │
│  │ 的输入。产品与设备的区别：产品是被制造的对象... │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  [重新生成] [编辑] [确认审核] [取消]                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 工作流程

### 完整流程图

```
用户创建新标签
    ↓
填写基本信息（名称、描述、颜色）
    ↓
点击"生成定义"按钮
    ↓
调用LLM生成详细定义
    ↓
展示生成结果（标记为"待审核"）
    ↓
用户审核和编辑
    ↓
点击"确认审核"
    ↓
标记为"已审核"，保存到数据库
    ↓
清空标签配置缓存
    ↓
下次Agent调用时使用新配置
```

## 实现优先级

### Phase 1: 基础功能（当前任务）
- [x] 数据库模型扩展
- [x] LabelDefinitionGenerator Agent实现
- [ ] 标签管理服务实现
- [ ] 标签管理API实现

### Phase 2: 动态Prompt（Task 7-8优化）
- [ ] 标签配置缓存实现
- [ ] 动态Prompt生成器实现
- [ ] 更新EntityExtractionAgent支持动态Prompt
- [ ] 更新RelationExtractionAgent支持动态Prompt

### Phase 3: 前端界面（Task 32）
- [ ] 标签配置页面实现
- [ ] 定义生成组件实现
- [ ] 定义审核组件实现
- [ ] Prompt预览组件实现

## 测试策略

### 单元测试
- 测试LabelDefinitionGenerator生成质量
- 测试动态Prompt生成逻辑
- 测试缓存机制

### 集成测试
- 测试完整的标签配置→生成→审核→使用流程
- 测试缓存失效机制
- 测试降级策略

### 用户验收测试
- 测试生成的定义是否符合领域要求
- 测试审核流程是否顺畅
- 测试Prompt预览是否准确

## 注意事项

1. **LLM生成质量**: 需要精心设计Prompt模板，确保生成内容的专业性
2. **审核必要性**: 必须经过人工审核才能用于生产，避免LLM生成错误
3. **缓存一致性**: 标签配置更新后必须清空缓存
4. **向后兼容**: 保留默认硬编码配置作为降级方案
5. **性能优化**: 使用缓存减少数据库查询
