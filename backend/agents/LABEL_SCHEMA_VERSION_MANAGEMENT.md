# 标签体系版本管理设计

## 问题背景

### 核心问题
1. **标签配置演化**: 用户可能会修改、删除、新增标签类型
2. **数据可追溯性**: 需要知道某个数据集使用的是哪个版本的标签体系
3. **多项目支持**: 不同项目可能需要完全不同的标签体系
4. **历史数据兼容**: 旧数据集不应该因为标签配置变化而失效

### 典型场景

#### 场景1：标签体系演化
```
时间线:
2024-01: 创建标签体系v1.0（16个实体类型 + 8个关系类型）
2024-02: 标注了100个数据集
2024-03: 发现需要新增2个实体类型，删除1个不常用的类型
         → 创建标签体系v2.0
2024-04: 使用v2.0标注新数据

问题: 
- 2月标注的数据集使用的是v1.0，如何保证可追溯？
- 如何在v1.0和v2.0之间切换？
- 如何导出v1.0标注的数据？
```

#### 场景2：多领域应用
```
项目A: 品质失效案例分析
  - 标签体系: 品质失效v1.0
  - 实体类型: Product, DefectPhenomenon, Process...
  
项目B: 供应链风险分析
  - 标签体系: 供应链风险v1.0
  - 实体类型: Supplier, RiskEvent, Mitigation...

问题:
- 如何管理两套完全不同的标签体系？
- 如何避免混淆？
```

## 解决方案：标签体系版本管理

### 核心设计理念

1. **版本快照**: 每次重大修改时创建新版本，保存完整的标签配置快照
2. **数据集绑定**: 每个数据集绑定到特定的标签体系版本
3. **活跃版本**: 系统有一个"当前活跃版本"，新建数据集默认使用
4. **版本切换**: 可以切换活跃版本，但不影响已有数据集

### 数据库设计

#### 1. LabelSchemaVersion表（新增）

```sql
CREATE TABLE label_schema_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_id VARCHAR(100) UNIQUE NOT NULL,  -- 如: "quality-v1.0"
    version_name VARCHAR(255) NOT NULL,       -- 如: "品质失效v1.0"
    description TEXT,                         -- 版本说明
    schema_data TEXT NOT NULL,                -- JSON格式的完整标签配置快照
    is_active BOOLEAN DEFAULT FALSE,          -- 是否为当前活跃版本
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

**schema_data字段格式**:
```json
{
  "entity_types": [
    {
      "type_name": "Product",
      "type_name_zh": "产品",
      "color": "#1f77b4",
      "description": "具体的产品名称、型号、部件",
      "definition": "产品是指制造过程中的具体产出物...",
      "examples": ["电机", "控制器", "显示屏"],
      "disambiguation": "产品与物料的区别...",
      "supports_bbox": false
    }
    // ... 更多实体类型
  ],
  "relation_types": [
    {
      "type_name": "has_defect",
      "type_name_zh": "有缺陷",
      "color": "#3498db",
      "description": "产品/部件存在某种缺陷",
      "definition": "has_defect关系表示...",
      "direction_rule": "Product/Material -> DefectPhenomenon",
      "examples": ["显示屏 --[has_defect]--> 裂纹"],
      "disambiguation": "与caused_by的区别..."
    }
    // ... 更多关系类型
  ],
  "metadata": {
    "domain": "quality_defect",
    "language": "zh-CN",
    "total_entity_types": 16,
    "total_relation_types": 8
  }
}
```

#### 2. Dataset表扩展

```sql
ALTER TABLE datasets ADD COLUMN label_schema_version_id INTEGER;
ALTER TABLE datasets ADD FOREIGN KEY (label_schema_version_id) 
    REFERENCES label_schema_versions(id);
```

### 版本管理策略

#### 策略1：增量修改（推荐）

**适用场景**: 小幅度调整，如新增1-2个标签、修改描述

**操作方式**:
- 直接修改当前活跃版本的标签配置
- 不创建新版本
- 已有数据集继续使用当前版本

**优点**: 简单，不会产生大量版本
**缺点**: 无法回溯到修改前的状态

#### 策略2：版本快照（推荐用于重大变更）

**适用场景**: 重大调整，如删除标签、重构标签体系

**操作方式**:
1. 创建新版本（保存当前配置的完整快照）
2. 在新版本上进行修改
3. 设置新版本为活跃版本
4. 旧数据集仍然绑定到旧版本

**优点**: 完整的版本历史，数据可追溯
**缺点**: 可能产生较多版本

#### 策略3：混合策略（最佳实践）

```
小修改（描述、示例、辨析）
    → 直接修改当前版本
    → 不创建新版本

重大修改（新增/删除标签、修改类型名称）
    → 提示用户创建新版本
    → 保存快照
    → 切换到新版本
```

### API设计

#### 1. 创建版本快照

```
POST /api/v1/labels/versions/snapshot
```

**请求体**:
```json
{
  "version_name": "品质失效v2.0",
  "description": "新增供应商相关实体类型，优化关系定义",
  "based_on_current": true  // 基于当前配置创建快照
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "version_id": "quality-v2.0",
    "version_name": "品质失效v2.0",
    "entity_types_count": 18,
    "relation_types_count": 8,
    "created_at": "2024-03-15T10:00:00Z"
  }
}
```

#### 2. 获取版本列表

```
GET /api/v1/labels/versions
```

**响应**:
```json
{
  "success": true,
  "data": {
    "versions": [
      {
        "version_id": "quality-v2.0",
        "version_name": "品质失效v2.0",
        "description": "新增供应商相关实体类型",
        "is_active": true,
        "datasets_count": 5,
        "created_at": "2024-03-15T10:00:00Z"
      },
      {
        "version_id": "quality-v1.0",
        "version_name": "品质失效v1.0",
        "description": "初始版本",
        "is_active": false,
        "datasets_count": 100,
        "created_at": "2024-01-01T10:00:00Z"
      }
    ],
    "active_version": "quality-v2.0"
  }
}
```

#### 3. 切换活跃版本

```
POST /api/v1/labels/versions/{version_id}/activate
```

**响应**:
```json
{
  "success": true,
  "message": "已切换到版本: 品质失效v1.0",
  "data": {
    "version_id": "quality-v1.0",
    "is_active": true
  }
}
```

#### 4. 查看版本详情

```
GET /api/v1/labels/versions/{version_id}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "version_id": "quality-v1.0",
    "version_name": "品质失效v1.0",
    "description": "初始版本",
    "entity_types": [...],  // 完整的实体类型列表
    "relation_types": [...],  // 完整的关系类型列表
    "datasets": [
      {"dataset_id": "ds-001", "name": "2024年1月数据"},
      {"dataset_id": "ds-002", "name": "2024年2月数据"}
    ],
    "created_at": "2024-01-01T10:00:00Z"
  }
}
```

#### 5. 版本比较

```
GET /api/v1/labels/versions/compare?from=quality-v1.0&to=quality-v2.0
```

**响应**:
```json
{
  "success": true,
  "data": {
    "from_version": "quality-v1.0",
    "to_version": "quality-v2.0",
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

### 前端设计

#### 版本管理界面

```
┌─────────────────────────────────────────────────────────┐
│  标签体系版本管理                                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  当前活跃版本: 品质失效v2.0                               │
│  [切换版本 ▼]                                            │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  版本历史                                                 │
│  ┌────────────────────────────────────────────────┐     │
│  │ ✓ 品质失效v2.0 (活跃)              2024-03-15  │     │
│  │   新增供应商相关实体类型                        │     │
│  │   使用数据集: 5个                               │     │
│  │   [查看详情] [比较] [导出]                      │     │
│  ├────────────────────────────────────────────────┤     │
│  │   品质失效v1.0                     2024-01-01  │     │
│  │   初始版本                                      │     │
│  │   使用数据集: 100个                             │     │
│  │   [查看详情] [激活] [比较] [导出]               │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  [+ 创建新版本快照]                                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### 创建版本快照对话框

```
┌─────────────────────────────────────────────────────────┐
│  创建标签体系版本快照                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  版本名称: [品质失效v2.0                            ]    │
│                                                          │
│  版本说明:                                                │
│  ┌────────────────────────────────────────────────┐     │
│  │ 新增供应商相关实体类型                          │     │
│  │ 优化关系定义和示例                              │     │
│  │ 修正部分类别辨析                                │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  基于版本: [当前配置 ▼]                                  │
│                                                          │
│  快照内容预览:                                            │
│  • 实体类型: 18个                                        │
│  • 关系类型: 8个                                         │
│  • 已审核标签: 24个                                      │
│  • 待审核标签: 2个                                       │
│                                                          │
│  ⚠ 注意: 创建快照后，当前配置将被锁定为v2.0              │
│                                                          │
│  [创建并激活] [仅创建] [取消]                             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 工作流程

#### 流程1：正常演化（小修改）

```
用户修改标签描述/示例
    ↓
直接保存到当前版本
    ↓
清空缓存
    ↓
新标注任务使用更新后的配置
```

#### 流程2：重大变更（创建新版本）

```
用户准备删除/新增标签
    ↓
系统提示: "这是重大变更，建议创建新版本"
    ↓
用户点击"创建版本快照"
    ↓
填写版本名称和说明
    ↓
系统保存当前配置的完整快照
    ↓
创建新版本（基于快照）
    ↓
用户在新版本上进行修改
    ↓
激活新版本
    ↓
新数据集使用新版本，旧数据集仍使用旧版本
```

#### 流程3：版本切换

```
用户在版本列表中选择旧版本
    ↓
点击"激活"
    ↓
系统切换活跃版本
    ↓
清空缓存
    ↓
新数据集使用旧版本的标签配置
```

### 实现建议

#### 1. 何时创建新版本？

**自动提示创建新版本的场景**:
- 删除任何标签类型
- 修改标签类型的英文名称（type_name）
- 删除超过3个标签
- 修改超过50%的标签定义

**不需要创建新版本的场景**:
- 修改标签的中文名称
- 修改描述、定义、示例、辨析
- 新增标签类型（可选）
- 修改颜色

#### 2. 版本命名规范

建议格式: `{领域}-v{主版本}.{次版本}`

示例:
- `quality-v1.0`: 品质失效v1.0
- `quality-v1.1`: 品质失效v1.1（小修改）
- `quality-v2.0`: 品质失效v2.0（重大变更）
- `supply-chain-v1.0`: 供应链风险v1.0（新领域）

#### 3. 数据迁移

如果需要将旧版本的数据集迁移到新版本:

```python
def migrate_dataset_to_new_version(
    dataset_id: str,
    target_version_id: str,
    label_mapping: Dict[str, str]  # 旧标签 -> 新标签的映射
):
    """
    将数据集迁移到新版本
    
    Args:
        dataset_id: 数据集ID
        target_version_id: 目标版本ID
        label_mapping: 标签映射关系
    """
    # 1. 加载数据集的所有标注
    # 2. 根据映射关系转换标签
    # 3. 验证转换后的标签在新版本中存在
    # 4. 保存到新版本
    # 5. 更新数据集的版本绑定
```

### 优先级建议

#### Phase 1: 基础版本管理（必需）
- [x] 数据库模型设计
- [ ] 版本快照创建功能
- [ ] 版本列表查询功能
- [ ] 活跃版本切换功能
- [ ] 数据集绑定版本

#### Phase 2: 高级功能（可选）
- [ ] 版本比较功能
- [ ] 数据迁移功能
- [ ] 版本导入导出
- [ ] 版本回滚

#### Phase 3: 用户体验优化（可选）
- [ ] 自动提示创建新版本
- [ ] 版本影响分析
- [ ] 版本使用统计

## 总结

### 推荐方案

**混合策略 + 版本快照**:
1. 日常小修改直接更新当前版本
2. 重大变更时创建新版本快照
3. 每个数据集绑定到特定版本
4. 支持版本切换和比较

### 优点
- ✅ 数据可追溯
- ✅ 支持多领域应用
- ✅ 历史数据不受影响
- ✅ 灵活的版本管理

### 注意事项
- ⚠️ 避免创建过多版本（建议<10个）
- ⚠️ 版本命名要清晰
- ⚠️ 定期清理不再使用的旧版本
- ⚠️ 重要版本要有详细的说明文档
