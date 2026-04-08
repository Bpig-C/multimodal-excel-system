# 设计文档

## 概述

本系统是一个自动化实体关系标注工具,支持从品质失效案例Excel文件导入数据(包含文本和图片),通过LLM批量自动标注和人工编辑相结合的方式,生成高质量的实体关系标注数据集,用于模型训练。

系统采用 **Vue3 + FastAPI + LangChain v1.0 + SQLite** 技术栈,复用参考项目中的实体关系抽取和标注编辑器组件。

### 核心特性

- **Excel智能解析**: 支持WPS Excel内嵌图片提取,多字段文本分句处理
- **多模态标注**: 同时支持文本实体关系标注和图片实体标注
- **LLM自动标注**: 基于LangChain v1.0的Agent架构,实现批量自动标注
- **人工精修**: 提供可视化标注编辑器,支持实体和关系的创建、编辑、删除
- **质量保证**: 完整的复核流程和版本历史管理
- **本地优先**: 使用SQLite数据库和本地文件存储,便于快速部署

## 架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         前端层 (Vue3)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ 数据导入页面  │  │ 数据集管理   │  │ 标注编辑页面  │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                 │                 │                    │
│         └─────────────────┼─────────────────┘                    │
│                           ▼                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              API 调用层 (Axios)                            │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       后端层 (FastAPI)                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    API 路由层                              │  │
│  │  /corpus  /datasets  /annotations  /labels  /review       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│         ┌──────────────────┼──────────────────┐                  │
│         ▼                  ▼                  ▼                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Excel处理   │  │ 标注Agent   │  │ 业务逻辑层  │              │
│  │ 服务        │  │ (LangChain) │  │             │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   LLM (Qwen-Max)                           │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       数据层                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   SQLite     │  │  本地文件系统 │  │  图片存储    │           │
│  │   数据库     │  │  (JSON/JSONL)│  │  (imgs/)     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```


### 技术栈选型

#### 后端
- **FastAPI**: 高性能Web框架,支持异步处理和自动API文档
- **LangChain v1.0**: Agent框架,用于LLM调用和结构化输出
- **LangGraph**: 状态管理和工作流编排
- **SQLite**: 轻量级关系数据库,便于本地部署
- **SQLAlchemy**: ORM框架
- **Pydantic v2**: 数据验证和序列化
- **openpyxl**: Excel文件解析
- **Pillow**: 图片处理

#### 前端
- **Vue 3**: 前端框架(Composition API)
- **TypeScript**: 类型安全
- **Element Plus**: UI组件库
- **Pinia**: 状态管理
- **Axios**: HTTP客户端
- **Vite**: 构建工具

#### LLM
- **Qwen-Max**: 通义千问大模型(通过DashScope API)

### 部署架构

```
项目根目录/
├── backend/                    # 后端代码
│   ├── main.py                # FastAPI入口
│   ├── config.py              # 配置管理
│   ├── models/                # 数据模型
│   ├── services/              # 业务逻辑
│   ├── agents/                # LangChain Agents
│   ├── api/                   # API路由
│   └── utils/                 # 工具函数
├── frontend/                   # 前端代码
│   ├── src/
│   │   ├── views/            # 页面组件
│   │   ├── components/       # 通用组件
│   │   ├── stores/           # Pinia状态
│   │   ├── api/              # API封装
│   │   └── types/            # TypeScript类型
├── data/                      # 数据目录
│   ├── database.db           # SQLite数据库
│   ├── uploads/              # 上传的Excel文件
│   ├── images/               # 提取的图片
│   └── exports/              # 导出的数据集
└── requirements.txt           # Python依赖

```

## 组件和接口

### 后端核心组件

#### 1. Excel处理服务 (ExcelProcessingService)

**职责**: 解析Excel文件,提取文本和图片

**主要方法**:
- `process_excel_file(file_path: str) -> ProcessingResult`: 处理Excel文件
- `extract_images(xlsx_path: str, output_dir: str) -> List[str]`: 提取WPS内嵌图片
- `split_text_to_sentences(text: str) -> List[str]`: 文本分句
- `convert_dispimg_to_markdown(text: str) -> str`: 转换图片引用格式

**参考实现**: `参考项目代码/excel解析与图片处理项目示例/excel_tools.py`


#### 2. 实体标注Agent (EntityAnnotationAgent)

**职责**: 使用LLM自动抽取文本中的实体

**主要方法**:
- `extract_entities(text: str) -> List[Entity]`: 抽取实体
- `validate_offsets(entities: List[Entity], text: str) -> List[Entity]`: 验证和修正偏移量

**LangChain配置**:
```python
# 使用LangChain v1.0的create_agent
agent = create_agent(
    model=ChatOpenAI(model="qwen-max"),
    tools=[],
    system_prompt=entity_extraction_prompt,
    response_format=ToolStrategy(
        schema=EntityExtractionOutput,
        handle_errors=True
    )
)
```

**参考实现**: `参考项目代码/威胁情报实体关系抽取演示/backend/agents.py`

#### 3. 关系标注Agent (RelationAnnotationAgent)

**职责**: 基于已识别实体抽取关系

**主要方法**:
- `extract_relations(text: str, entities: List[Entity]) -> List[Relation]`: 抽取关系
- `validate_relation_ids(relations: List[Relation], entities: List[Entity]) -> List[Relation]`: 验证关系ID有效性

**参考实现**: `参考项目代码/威胁情报实体关系抽取演示/backend/agents.py`

#### 4. 图片实体标注服务 (ImageAnnotationService)

**职责**: 处理图片中的实体标注

**主要方法**:
- `create_image_entity(image_path: str, label: str, bbox: BoundingBox) -> ImageEntity`: 创建图片实体
- `get_image_entities(image_path: str) -> List[ImageEntity]`: 获取图片实体列表

**说明**: 由于缺陷图片类型单一,初期可以简化为单一标签"缺陷图片",后续可扩展为多类别

#### 5. 偏移量修正服务 (OffsetCorrectionService)

**职责**: 验证和修正实体偏移量

**主要方法**:
- `validate_offset(entity: Entity, text: str) -> bool`: 验证偏移量
- `correct_offset(entity: Entity, text: str) -> Entity`: 修正偏移量
- `find_closest_match(token: str, text: str, original_offset: int) -> Tuple[int, int]`: 查找最接近的匹配

**参考实现**: `参考项目代码/标注系统前端代码整理/composables/use-offset-correction.ts`

#### 6. 数据集管理服务 (DatasetService)

**职责**: 管理数据集的创建、查询、删除

**主要方法**:
- `create_dataset(name: str, description: str, corpus_ids: List[str]) -> Dataset`: 创建数据集
- `get_dataset(dataset_id: str) -> Dataset`: 获取数据集详情
- `delete_dataset(dataset_id: str) -> bool`: 删除数据集
- `export_dataset(dataset_id: str, format: str) -> str`: 导出数据集

#### 6.5. 标签定义生成服务 (LabelDefinitionGenerator)

**职责**: 使用LLM自动生成实体类型和关系类型的详细定义

**主要方法**:
- `generate_entity_type_definition(type_name: str, type_name_zh: str, description: str) -> EntityTypeDefinition`: 生成实体类型定义
- `generate_relation_type_definition(type_name: str, type_name_zh: str, description: str) -> RelationTypeDefinition`: 生成关系类型定义

**生成内容**:

实体类型定义包含:
- **标准定义** (definition): 详细说明该实体类型的含义和范围（100-200字）
- **示例列表** (examples): 至少5个典型示例
- **类别辨析** (disambiguation): 与相似类型的区别（50-100字）

关系类型定义包含:
- **标准定义** (definition): 详细说明该关系类型的含义（100-200字）
- **方向规则** (direction_rule): from和to实体的类型约束
- **示例列表** (examples): 至少5个典型示例（格式：实体A --[关系]--> 实体B）
- **类别辨析** (disambiguation): 与相似关系的区别（50-100字）

**工作流程**:
1. 用户在前端创建/修改标签时，提供基本信息（名称、简短描述）
2. 点击"生成定义"按钮，调用LLM生成详细定义
3. 系统展示生成结果，标记为"待审核"状态
4. 用户可以编辑生成的内容，确认后标记为"已审核"
5. 只有已审核的标签定义才会用于Agent的Prompt生成

**参考实现**: 新增Agent，使用LangChain结构化输出

#### 6.6. 标签体系版本管理服务 (LabelSchemaVersionService)

**职责**: 管理标签体系的版本历史和快照

**主要方法**:
- `create_version_snapshot(version_name: str, description: str) -> LabelSchemaVersion`: 创建版本快照
- `get_version_list() -> List[LabelSchemaVersion]`: 获取版本列表
- `get_version_detail(version_id: str) -> LabelSchemaVersion`: 获取版本详情
- `activate_version(version_id: str) -> bool`: 激活指定版本
- `compare_versions(from_version: str, to_version: str) -> VersionDiff`: 比较两个版本的差异
- `export_version(version_id: str) -> str`: 导出版本配置

**版本管理策略**:
- **增量修改**: 小幅度调整直接修改当前版本
- **版本快照**: 重大变更时创建新版本快照
- **数据集绑定**: 每个数据集绑定到特定版本，保证数据可追溯

**使用场景**:
- 标签体系演化（新增/删除标签类型）
- 多领域应用（不同项目使用不同标签体系）
- 历史数据兼容（旧数据集使用旧版本标签）

#### 7. 标注任务服务 (AnnotationTaskService)

**职责**: 管理标注任务的生命周期

**主要方法**:
- `create_task(dataset_id: str, sentence_id: str) -> AnnotationTask`: 创建标注任务
- `get_task(task_id: str) -> AnnotationTask`: 获取任务详情
- `update_task_status(task_id: str, status: TaskStatus) -> bool`: 更新任务状态
- `batch_annotate(dataset_id: str) -> BatchJob`: 批量自动标注


#### 8. 复核服务 (ReviewService)

**职责**: 管理标注数据的复核流程

**主要方法**:
- `submit_for_review(task_id: str) -> ReviewTask`: 提交复核
- `approve_task(task_id: str, reviewer_id: str) -> bool`: 批准任务
- `reject_task(task_id: str, reviewer_id: str, reason: str) -> bool`: 驳回任务
- `get_review_tasks(reviewer_id: str) -> List[ReviewTask]`: 获取复核任务列表

#### 9. 版本管理服务 (VersionService)

**职责**: 管理标注数据的版本历史

**主要方法**:
- `create_version(task_id: str, entities: List[Entity], relations: List[Relation]) -> Version`: 创建版本
- `get_version_history(task_id: str) -> List[Version]`: 获取版本历史
- `rollback_to_version(task_id: str, version_id: str) -> bool`: 回滚到指定版本
- `compare_versions(version_id_1: str, version_id_2: str) -> VersionDiff`: 比较版本差异

### 前端核心组件

#### 1. Excel导入页面 (CorpusImportView)

**功能**: 上传Excel文件,预览处理结果

**主要组件**:
- `FileUploader`: 文件上传组件
- `ProcessingProgress`: 处理进度显示
- `CorpusPreview`: 语料预览列表

#### 2. 数据集管理页面 (DatasetManagementView)

**功能**: 创建、查看、删除数据集

**主要组件**:
- `DatasetList`: 数据集列表
- `DatasetCard`: 数据集卡片
- `DatasetCreateDialog`: 创建数据集对话框
- `CorpusSelector`: 语料选择器

#### 3. 标注编辑页面 (AnnotationEditorView)

**功能**: 文本和图片的实体关系标注

**主要组件**:
- `TextAnnotationEditor`: 文本标注编辑器
  - `EntityHighlight`: 实体高亮显示
  - `LabelSelector`: 标签选择菜单
  - `RelationArrowLayer`: 关系箭头层(SVG)
- `ImageAnnotationEditor`: 图片标注编辑器
  - `ImageViewer`: 图片查看器
  - `BoundingBoxDrawer`: 边界框绘制工具
- `EntityList`: 实体列表面板
- `RelationList`: 关系列表面板

**参考实现**: `参考项目代码/标注系统前端代码整理/views/annotation/`

#### 4. 复核页面 (ReviewView)

**功能**: 审核标注数据,批准或驳回

**主要组件**:
- `ReviewTaskList`: 复核任务列表
- `AnnotationViewer`: 标注结果查看器(只读模式)
- `ReviewActionPanel`: 复核操作面板

#### 5. 标签配置页面 (LabelConfigView)

**功能**: 配置实体类型和关系类型，支持LLM自动生成定义

**主要组件**:
- `EntityTypeConfig`: 实体类型配置
  - `EntityTypeList`: 实体类型列表
  - `EntityTypeForm`: 实体类型编辑表单
  - `DefinitionGenerator`: 定义生成组件（调用LLM）
  - `DefinitionReview`: 定义审核组件（编辑和确认）
- `RelationTypeConfig`: 关系类型配置
  - `RelationTypeList`: 关系类型列表
  - `RelationTypeForm`: 关系类型编辑表单
  - `DefinitionGenerator`: 定义生成组件（调用LLM）
  - `DefinitionReview`: 定义审核组件（编辑和确认）
- `LabelImportExport`: 标签导入导出
- `PromptPreview`: Agent Prompt预览（展示当前标签配置生成的Prompt）

**工作流程**:
1. 用户创建新标签时，填写基本信息（名称、简短描述、颜色）
2. 点击"生成详细定义"按钮，系统调用LLM生成标准定义、示例、辨析等内容
3. 生成结果展示在审核面板，标记为"待审核"状态（黄色标识）
4. 用户可以编辑生成的内容，满意后点击"确认审核"
5. 审核通过后标记为"已审核"状态（绿色标识），该标签可用于标注
6. 可以点击"预览Prompt"查看当前标签配置生成的Agent Prompt


### API接口设计

#### 1. 语料管理接口

```
POST   /api/v1/corpus/upload          # 上传Excel文件
GET    /api/v1/corpus                 # 获取语料列表
GET    /api/v1/corpus/{id}            # 获取语料详情
DELETE /api/v1/corpus/{id}            # 删除语料
GET    /api/v1/corpus/{id}/images     # 获取语料关联图片
```

#### 2. 数据集管理接口

```
POST   /api/v1/datasets               # 创建数据集
GET    /api/v1/datasets               # 获取数据集列表
GET    /api/v1/datasets/{id}          # 获取数据集详情
PUT    /api/v1/datasets/{id}          # 更新数据集
DELETE /api/v1/datasets/{id}          # 删除数据集
POST   /api/v1/datasets/{id}/export   # 导出数据集
```

#### 3. 标注任务接口

```
POST   /api/v1/annotations/batch      # 批量自动标注
GET    /api/v1/annotations/{task_id}  # 获取标注任务详情
PUT    /api/v1/annotations/{task_id}  # 更新标注任务
POST   /api/v1/annotations/{task_id}/entities      # 添加实体
PUT    /api/v1/annotations/{task_id}/entities/{id} # 更新实体
DELETE /api/v1/annotations/{task_id}/entities/{id} # 删除实体
POST   /api/v1/annotations/{task_id}/relations      # 添加关系
PUT    /api/v1/annotations/{task_id}/relations/{id} # 更新关系
DELETE /api/v1/annotations/{task_id}/relations/{id} # 删除关系
```

#### 4. 图片标注接口

```
POST   /api/v1/images/{image_id}/entities      # 添加图片实体
GET    /api/v1/images/{image_id}/entities      # 获取图片实体列表
PUT    /api/v1/images/{image_id}/entities/{id} # 更新图片实体
DELETE /api/v1/images/{image_id}/entities/{id} # 删除图片实体
```

#### 5. 标签配置接口

```
GET    /api/v1/labels/entities        # 获取实体类型列表
POST   /api/v1/labels/entities        # 创建实体类型
PUT    /api/v1/labels/entities/{id}   # 更新实体类型
DELETE /api/v1/labels/entities/{id}   # 删除实体类型
POST   /api/v1/labels/entities/{id}/generate-definition  # 生成实体类型定义
POST   /api/v1/labels/entities/{id}/review  # 审核实体类型定义

GET    /api/v1/labels/relations       # 获取关系类型列表
POST   /api/v1/labels/relations       # 创建关系类型
PUT    /api/v1/labels/relations/{id}  # 更新关系类型
DELETE /api/v1/labels/relations/{id}  # 删除关系类型
POST   /api/v1/labels/relations/{id}/generate-definition  # 生成关系类型定义
POST   /api/v1/labels/relations/{id}/review  # 审核关系类型定义

POST   /api/v1/labels/import          # 导入标签配置
GET    /api/v1/labels/export          # 导出标签配置
GET    /api/v1/labels/prompt-preview  # 预览Agent Prompt（基于当前标签配置）

# 标签体系版本管理
GET    /api/v1/labels/versions        # 获取版本列表
POST   /api/v1/labels/versions/snapshot  # 创建版本快照
GET    /api/v1/labels/versions/{version_id}  # 获取版本详情
POST   /api/v1/labels/versions/{version_id}/activate  # 激活版本
GET    /api/v1/labels/versions/compare  # 比较版本差异
GET    /api/v1/labels/versions/{version_id}/export  # 导出版本配置
```

#### 6. 复核接口

```
POST   /api/v1/review/submit          # 提交复核
GET    /api/v1/review/tasks           # 获取复核任务列表
POST   /api/v1/review/{task_id}/approve  # 批准任务
POST   /api/v1/review/{task_id}/reject   # 驳回任务
```

#### 7. 版本管理接口

```
GET    /api/v1/versions/{task_id}     # 获取版本历史
POST   /api/v1/versions/{task_id}/rollback  # 回滚版本
GET    /api/v1/versions/compare       # 比较版本差异
```

#### 8. 用户管理接口

```
POST   /api/v1/users                  # 创建用户
GET    /api/v1/users                  # 获取用户列表
PUT    /api/v1/users/{id}             # 更新用户
DELETE /api/v1/users/{id}             # 删除用户
POST   /api/v1/auth/login             # 用户登录
POST   /api/v1/auth/logout            # 用户登出
```


## 数据模型

### 数据库表设计 (SQLite)

#### 1. 用户表 (users)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'admin', 'annotator', 'reviewer'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. 原始语料表 (corpus)

```sql
CREATE TABLE corpus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id VARCHAR(100) UNIQUE NOT NULL,
    text TEXT NOT NULL,
    source_file VARCHAR(255),
    source_row INTEGER,
    source_field VARCHAR(100),
    has_images BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. 图片表 (images)

```sql
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id VARCHAR(100) UNIQUE NOT NULL,
    corpus_id INTEGER,
    file_path VARCHAR(500) NOT NULL,
    original_name VARCHAR(255),
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (corpus_id) REFERENCES corpus(id) ON DELETE CASCADE
);
```

#### 4. 数据集表 (datasets)

```sql
CREATE TABLE datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

#### 5. 数据集-语料关联表 (dataset_corpus)

```sql
CREATE TABLE dataset_corpus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INTEGER NOT NULL,
    corpus_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
    FOREIGN KEY (corpus_id) REFERENCES corpus(id) ON DELETE CASCADE,
    UNIQUE(dataset_id, corpus_id)
);
```

#### 6. 标注任务表 (annotation_tasks)

```sql
CREATE TABLE annotation_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id VARCHAR(100) UNIQUE NOT NULL,
    dataset_id INTEGER NOT NULL,
    corpus_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'processing', 'completed', 'failed'
    annotation_type VARCHAR(20) DEFAULT 'automatic',  -- 'automatic', 'manual'
    current_version INTEGER DEFAULT 1,
    assigned_to INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
    FOREIGN KEY (corpus_id) REFERENCES corpus(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);
```


#### 7. 文本实体表 (text_entities)

```sql
CREATE TABLE text_entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,  -- 实体在任务内的ID
    task_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    token TEXT NOT NULL,
    label VARCHAR(50) NOT NULL,
    start_offset INTEGER NOT NULL,
    end_offset INTEGER NOT NULL,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES annotation_tasks(id) ON DELETE CASCADE
);
```

#### 8. 图片实体表 (image_entities)

```sql
CREATE TABLE image_entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,  -- 实体在任务内的ID
    task_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    label VARCHAR(50) NOT NULL,
    bbox_x INTEGER NOT NULL,
    bbox_y INTEGER NOT NULL,
    bbox_width INTEGER NOT NULL,
    bbox_height INTEGER NOT NULL,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES annotation_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
);
```

#### 9. 关系表 (relations)

```sql
CREATE TABLE relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relation_id INTEGER NOT NULL,  -- 关系在任务内的ID
    task_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    from_entity_id INTEGER NOT NULL,
    to_entity_id INTEGER NOT NULL,
    relation_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES annotation_tasks(id) ON DELETE CASCADE
);
```

#### 10. 实体类型配置表 (entity_types)

```sql
CREATE TABLE entity_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name VARCHAR(50) UNIQUE NOT NULL,
    type_name_zh VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 11. 关系类型配置表 (relation_types)

```sql
CREATE TABLE relation_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name VARCHAR(50) UNIQUE NOT NULL,
    type_name_zh VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 12. 复核任务表 (review_tasks)

```sql
CREATE TABLE review_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id VARCHAR(100) UNIQUE NOT NULL,
    task_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'approved', 'rejected'
    reviewer_id INTEGER,
    review_comment TEXT,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES annotation_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id)
);
```


#### 13. 版本历史表 (version_history)

```sql
CREATE TABLE version_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_id VARCHAR(100) UNIQUE NOT NULL,
    task_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    change_type VARCHAR(20) NOT NULL,  -- 'create', 'update', 'delete'
    change_description TEXT,
    changed_by INTEGER,
    snapshot_data TEXT,  -- JSON格式存储完整快照
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES annotation_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id)
);
```

#### 14. 批量任务表 (batch_jobs)

```sql
CREATE TABLE batch_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id VARCHAR(100) UNIQUE NOT NULL,
    dataset_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'running', 'completed', 'failed'
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    failed_tasks INTEGER DEFAULT 0,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
);
```

### Pydantic数据模型

#### 1. 实体模型

```python
class Entity(BaseModel):
    """文本实体模型"""
    id: int
    token: str
    label: str
    start_offset: int
    end_offset: int
    confidence: Optional[float] = None

class ImageEntity(BaseModel):
    """图片实体模型"""
    id: int
    image_id: str
    label: str
    bbox: BoundingBox
    confidence: Optional[float] = None

class BoundingBox(BaseModel):
    """边界框模型"""
    x: int
    y: int
    width: int
    height: int
```

#### 2. 关系模型

```python
class Relation(BaseModel):
    """关系模型"""
    id: int
    from_id: int
    to_id: int
    type: str
```

#### 3. 标注任务模型

```python
class AnnotationTask(BaseModel):
    """标注任务模型"""
    task_id: str
    dataset_id: str
    corpus_id: str
    text: str
    images: List[ImageInfo]
    status: TaskStatus
    annotation_type: AnnotationType
    current_version: int
    entities: List[Entity]
    image_entities: List[ImageEntity]
    relations: List[Relation]
    created_at: datetime
    updated_at: datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class AnnotationType(str, Enum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"
```


#### 4. 数据集模型

```python
class Dataset(BaseModel):
    """数据集模型"""
    dataset_id: str
    name: str
    description: Optional[str]
    total_tasks: int
    completed_tasks: int
    reviewed_tasks: int
    created_by: str
    created_at: datetime
    updated_at: datetime

class CorpusRecord(BaseModel):
    """语料记录模型"""
    text_id: str
    text: str
    source_file: Optional[str]
    source_row: Optional[int]
    source_field: Optional[str]
    has_images: bool
    images: List[ImageInfo]
    created_at: datetime
```

#### 5. 标签配置模型

```python
class EntityTypeConfig(BaseModel):
    """实体类型配置"""
    id: Optional[int]
    type_name: str
    type_name_zh: str
    color: str
    description: Optional[str]  # 简短描述
    definition: Optional[str]  # LLM生成的标准定义
    examples: Optional[List[str]]  # LLM生成的示例列表
    disambiguation: Optional[str]  # LLM生成的类别辨析
    supports_bbox: bool = False
    is_active: bool = True
    is_reviewed: bool = False  # 是否已人工审核
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]

class RelationTypeConfig(BaseModel):
    """关系类型配置"""
    id: Optional[int]
    type_name: str
    type_name_zh: str
    color: str
    description: Optional[str]  # 简短描述
    definition: Optional[str]  # LLM生成的标准定义
    direction_rule: Optional[str]  # LLM生成的方向规则
    examples: Optional[List[str]]  # LLM生成的示例列表
    disambiguation: Optional[str]  # LLM生成的类别辨析
    is_active: bool = True
    is_reviewed: bool = False  # 是否已人工审核
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]

class LabelSchema(BaseModel):
    """标签体系"""
    entity_types: List[EntityTypeConfig]
    relation_types: List[RelationTypeConfig]

class LabelDefinitionGenerateRequest(BaseModel):
    """标签定义生成请求"""
    type_name: str
    type_name_zh: str
    description: str

class LabelDefinitionGenerateResponse(BaseModel):
    """标签定义生成响应"""
    definition: str
    examples: List[str]
    disambiguation: str
    direction_rule: Optional[str] = None  # 仅关系类型有

class LabelReviewRequest(BaseModel):
    """标签审核请求"""
    definition: str
    examples: List[str]
    disambiguation: str
    direction_rule: Optional[str] = None  # 仅关系类型有
```

#### 6. 复核模型

```python
class ReviewTask(BaseModel):
    """复核任务模型"""
    review_id: str
    task_id: str
    status: ReviewStatus
    reviewer_id: Optional[str]
    review_comment: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime

class ReviewStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
```

#### 7. 版本模型

```python
class Version(BaseModel):
    """版本模型"""
    history_id: str
    task_id: str
    version: int
    change_type: ChangeType
    change_description: Optional[str]
    changed_by: str
    snapshot_data: Dict[str, Any]
    created_at: datetime

class ChangeType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class VersionDiff(BaseModel):
    """版本差异模型"""
    from_version: int
    to_version: int
    added_entities: List[Entity]
    deleted_entities: List[Entity]
    modified_entities: List[Dict[str, Any]]
    added_relations: List[Relation]
    deleted_relations: List[Relation]
    modified_relations: List[Dict[str, Any]]
```


## 正确性属性

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Excel文件验证完整性
*For any* Excel文件，如果文件格式为xlsx且包含所有必需列（问题分类、客户、质量问题、问题描述、问题处理、原因分析、采取措施、图片），则验证函数应返回true；否则应返回false并指出缺失的列
**Validates: Requirements 1.1**

### Property 2: 图片ID映射一致性
*For any* 包含WPS内嵌图片的Excel文件，提取的图片ID映射关系应满足：每个cellimages.xml中的图片名称都能在rels文件中找到对应的图片路径
**Validates: Requirements 1.2**

### Property 3: 图片文件导出完整性
*For any* 提取的图片映射关系，导出后的图片文件数量应等于映射关系中的图片数量，且每个文件名应保留原始ID
**Validates: Requirements 1.3**

### Property 4: DISPIMG转换正确性
*For any* 包含DISPIMG公式的文本，转换后的Markdown格式应能正确提取图片ID，且格式符合`![图片](imgs/ID.png)`模式
**Validates: Requirements 1.4**

### Property 5: 文本分句一致性
*For any* 长文本字段，按分隔符分割后的句子数量应大于等于1，且所有句子拼接后应能还原原始文本（忽略分隔符）
**Validates: Requirements 1.5**

### Property 6: 语料记录元数据完整性
*For any* 生成的语料记录，应包含text_id、text、source_file、source_row、source_field、text_type等所有必需字段
**Validates: Requirements 1.6, 1.7**

### Property 7: 处理统计准确性
*For any* Excel文件处理结果，统计信息中的总记录数应等于数据库中实际插入的记录数，提取图片数应等于导出的图片文件数
**Validates: Requirements 1.8**

### Property 8: 数据集任务创建一致性
*For any* 数据集创建操作，创建的标注任务数量应等于选中的语料记录数量
**Validates: Requirements 2.3**

### Property 9: 数据集统计准确性
*For any* 数据集，显示的总任务数、已标注数、已复核数应与数据库中实际的任务状态统计一致
**Validates: Requirements 2.4**

### Property 10: 级联删除完整性
*For any* 数据集删除操作，删除后该数据集关联的所有标注任务和复核任务都应不存在于数据库中
**Validates: Requirements 2.5**

### Property 11: 数据集导出格式正确性
*For any* 数据集导出操作，导出的JSONL文件中每一行都应是有效的JSON对象，且包含text、text_type、entities、relations、images、image_relations字段
**Validates: Requirements 2.6**

### Property 12: 标签配置序列化往返一致性
*For any* 标签配置，导出为JSON后再导入，应得到与原始配置完全相同的数据（包括所有字段值）
**Validates: Requirements 3.1, 3.2, 3.5**

### Property 13: 标签修改影响范围准确性
*For any* 标签类型修改操作，系统识别的受影响标注数量应等于数据库中使用该标签类型的实体数量
**Validates: Requirements 3.3**

### Property 14: 标签配置合并正确性
*For any* 两个标签配置，合并后的配置应包含两者的所有标签类型，且相同名称的标签应以导入的为准
**Validates: Requirements 3.6**


### Property 15: 批量标注任务创建完整性
*For any* 数据集的批量标注操作，创建的标注任务数量应等于数据集中待标注的句子数量
**Validates: Requirements 4.1**

### Property 16: LLM实体抽取输出格式正确性
*For any* LLM实体抽取结果，返回的每个实体都应包含token、label、start_offset、end_offset字段，且label应在预定义的实体类型列表中
**Validates: Requirements 4.2**

### Property 17: 多模态标注输出格式正确性
*For any* 包含图片的句子，LLM多模态标注结果应包含image_path和label字段，且label应在预定义的图片实体类型列表中
**Validates: Requirements 4.3**

### Property 18: 实体偏移量验证正确性
*For any* 文本实体，如果text[start_offset:end_offset]等于entity.token，则验证应通过；否则应失败
**Validates: Requirements 4.4, 10.1**

### Property 19: 关系实体ID有效性
*For any* 抽取的关系，其from_id和to_id都应在当前任务的实体列表中存在
**Validates: Requirements 4.5**

### Property 20: 批量标注进度计算准确性
*For any* 批量标注任务，显示的进度百分比应等于(已完成任务数/总任务数)*100
**Validates: Requirements 4.6**

### Property 21: 批量标注状态更新正确性
*For any* 批量标注任务，当所有子任务完成时，批量任务状态应更新为completed
**Validates: Requirements 4.7**

### Property 22: 标注失败错误记录完整性
*For any* 失败的标注任务，应在数据库中记录错误信息，且任务状态应标记为failed
**Validates: Requirements 4.8**

### Property 23: 文本选择偏移量计算正确性
*For any* 文本选择操作，计算的start_offset和end_offset应满足：text[start_offset:end_offset]等于选中的文本
**Validates: Requirements 5.2**

### Property 24: 关系创建有向性正确性
*For any* 关系创建操作，创建的关系应包含from_id和to_id，且from_id应对应第一个点击的实体，to_id应对应第二个点击的实体
**Validates: Requirements 5.6**

### Property 25: 版本历史递增性
*For any* 标注修改操作，修改后的版本号应等于修改前的版本号加1
**Validates: Requirements 5.7**

### Property 26: 版本回滚一致性
*For any* 版本回滚操作，回滚到版本N后的数据应与版本N的快照数据完全一致
**Validates: Requirements 5.8**

### Property 27: 复核任务创建正确性
*For any* 标注任务提交复核操作，应创建一个新的复核任务，且原任务状态应更新为pending_review
**Validates: Requirements 6.1**

### Property 28: 复核批准状态更新正确性
*For any* 复核批准操作，任务状态应更新为approved，且应记录reviewer_id和reviewed_at时间戳
**Validates: Requirements 6.3**

### Property 29: 复核驳回状态更新正确性
*For any* 复核驳回操作，任务状态应更新为rejected，且应记录reviewer_id、reviewed_at和review_comment
**Validates: Requirements 6.4**

### Property 30: 复核修改差异记录完整性
*For any* 复核过程中的修改，差异记录应包含所有变更的实体和关系，包括新增、删除和修改
**Validates: Requirements 6.6**

### Property 31: 质量统计计算准确性
*For any* 数据集，质量统计指标应基于实际的标注数据计算，且各项指标之和应等于总任务数
**Validates: Requirements 6.7**

### Property 32: 导出数据状态筛选正确性
*For any* 导出操作，如果指定筛选状态为approved，则导出的所有任务状态都应为approved
**Validates: Requirements 7.1**

### Property 33: 导出数据格式完整性
*For any* 导出的JSONL文件，每一行JSON对象都应包含text、text_type、entities、relations、images、image_relations字段
**Validates: Requirements 7.2**

### Property 34: JSONL格式有效性
*For any* 导出的JSONL文件，每一行都应是有效的JSON对象，且文件应能被标准JSONL解析器解析
**Validates: Requirements 7.3**

### Property 35: 数据集划分比例准确性
*For any* 训练集/测试集划分操作，如果指定比例为0.8，则训练集大小应约等于总数据量的80%（允许±1的误差）
**Validates: Requirements 7.4**

### Property 36: 句子分类筛选正确性
*For any* 按text_type筛选的导出操作，导出的所有记录的text_type都应等于指定的分类
**Validates: Requirements 7.5**

### Property 37: Reward数据集筛选正确性
*For any* Reward数据集生成操作，筛选的任务都应满足：存在人工修正（即原始标注与最终标注不同）
**Validates: Requirements 8.1**

### Property 38: 标注差异计算准确性
*For any* Reward数据集记录，差异描述应准确反映原始标注和修正标注之间的所有变更
**Validates: Requirements 8.2**

### Property 39: Reward数据格式完整性
*For any* Reward数据集JSONL文件，每一行都应包含original_annotation、corrected_annotation和diff字段
**Validates: Requirements 8.3**

### Property 40: 修正频率统计准确性
*For any* Reward数据集，统计的各类修正频率之和应等于总修正次数
**Validates: Requirements 8.4**

### Property 41: 用户角色分配正确性
*For any* 用户创建操作，创建的用户应包含role字段，且role应为admin或annotator之一
**Validates: Requirements 9.1**

### Property 42: 权限检查正确性
*For any* 用户访问操作，如果用户角色为annotator且访问管理功能，则权限检查应返回false
**Validates: Requirements 9.2, 9.3, 9.4**

### Property 43: 复核人员分配有效性
*For any* 数据集复核人员分配操作，分配的reviewer_id应与annotator_id不同
**Validates: Requirements 9.5**

### Property 44: 偏移量修正准确性
*For any* 偏移量验证失败的实体，修正后的偏移量应满足：text[new_start:new_end]等于entity.token
**Validates: Requirements 10.2**

### Property 45: 最近匹配选择正确性
*For any* 存在多个匹配位置的实体，选择的匹配位置应是与原始偏移量距离最小的那个
**Validates: Requirements 10.3**

### Property 46: 偏移量修正日志记录完整性
*For any* 偏移量修正操作，应在日志表中创建一条记录，包含原始偏移量、修正后偏移量和修正时间
**Validates: Requirements 10.4**

### Property 47: 无法修正实体标记正确性
*For any* 无法修正偏移量的实体，其状态应标记为needs_manual_review
**Validates: Requirements 10.5**

### Property 48: 标注数据序列化往返一致性
*For any* 标注任务，序列化为JSON后再反序列化，应得到与原始数据完全相同的实体和关系列表
**Validates: Requirements 11.1, 11.2, 11.7**

### Property 49: 文本实体序列化格式正确性
*For any* 文本实体，序列化后的JSON对象应包含id、start_offset、end_offset、label字段
**Validates: Requirements 11.3**

### Property 50: 整图实体序列化格式正确性
*For any* 整图实体，序列化后的JSON对象应包含id、image_path、label字段，且bbox字段应为null
**Validates: Requirements 11.4**

### Property 51: 区域实体序列化格式正确性
*For any* 区域实体，序列化后的JSON对象应包含id、image_path、label、bbox字段，且bbox应包含x、y、width、height子字段
**Validates: Requirements 11.5**

### Property 52: 关系序列化格式正确性
*For any* 关系，序列化后的JSON对象应包含from_id、to_id、type字段
**Validates: Requirements 11.6**

### Property 53: 图片坐标变换不变性
*For any* 图片缩放或平移操作，边界框在图片坐标系中的相对位置应保持不变（即bbox相对于图片尺寸的比例不变）
**Validates: Requirements 12.8**


## 错误处理

### 错误分类

#### 1. 用户输入错误
- **无效文件格式**: 上传的文件不是xlsx格式
- **缺失必需列**: Excel文件缺少必需的列
- **空文本输入**: 用户提交空的文本进行标注
- **无效偏移量**: 手动输入的偏移量超出文本范围

**处理策略**: 
- 在API层进行输入验证
- 返回400 Bad Request和详细错误信息
- 前端显示友好的错误提示

#### 2. 数据一致性错误
- **实体ID不存在**: 关系引用的实体ID在当前任务中不存在
- **偏移量不匹配**: 实体的偏移量与文本内容不对应
- **版本冲突**: 并发修改导致版本冲突

**处理策略**:
- 使用数据库事务保证原子性
- 实现乐观锁机制处理并发
- 自动修正偏移量，记录修正日志
- 无法自动修正时标记为待人工审核

#### 3. LLM调用错误
- **API超时**: LLM API调用超时
- **API限流**: 超过API调用频率限制
- **解析失败**: LLM返回的结果无法解析为结构化数据

**处理策略**:
- 实现重试机制（指数退避）
- 使用降级解析策略（结构化输出失败时使用正则提取）
- 记录失败任务，允许手动重试
- 显示详细错误信息给用户

#### 4. 文件系统错误
- **磁盘空间不足**: 上传或导出文件时磁盘空间不足
- **文件权限错误**: 无法读写文件
- **文件损坏**: Excel文件损坏无法解析

**处理策略**:
- 检查磁盘空间，提前警告
- 使用try-catch捕获IO异常
- 返回500 Internal Server Error和错误详情
- 记录错误日志用于排查

#### 5. 数据库错误
- **连接失败**: 无法连接到SQLite数据库
- **约束违反**: 违反唯一性约束或外键约束
- **查询超时**: 复杂查询执行超时

**处理策略**:
- 使用连接池管理数据库连接
- 捕获约束违反异常，返回友好错误信息
- 优化查询性能，添加必要索引
- 实现数据库备份和恢复机制

### 错误响应格式

```python
class ErrorResponse(BaseModel):
    """统一错误响应格式"""
    success: bool = False
    error_code: str
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    timestamp: datetime
```

### 日志记录

- **INFO**: 正常操作日志（文件上传、数据集创建等）
- **WARNING**: 可恢复的错误（偏移量自动修正、LLM重试等）
- **ERROR**: 需要人工介入的错误（文件损坏、数据库错误等）
- **DEBUG**: 调试信息（LLM请求/响应、SQL查询等）

日志格式:
```
[时间戳] [级别] [模块] [用户ID] [操作] - 消息
```


## 测试策略

### 测试方法

本系统采用**双重测试策略**，结合单元测试和基于属性的测试（Property-Based Testing, PBT），以确保系统的正确性和鲁棒性。

#### 单元测试
- 验证具体的功能点和边界情况
- 测试特定的输入输出示例
- 覆盖错误处理路径
- 测试组件间的集成

#### 基于属性的测试（PBT）
- 验证通用属性在大量随机输入下都成立
- 自动发现边界情况和异常输入
- 提供更高的测试覆盖率
- 每个属性测试运行至少100次迭代

### 测试框架

#### 后端测试
- **单元测试框架**: pytest
- **PBT框架**: Hypothesis
- **Mock框架**: pytest-mock
- **覆盖率工具**: pytest-cov

#### 前端测试
- **单元测试框架**: Vitest
- **组件测试**: @vue/test-utils
- **PBT框架**: fast-check
- **E2E测试**: Playwright（可选）

### 测试组织

#### 后端测试目录结构
```
backend/
├── tests/
│   ├── unit/                    # 单元测试
│   │   ├── test_excel_processing.py
│   │   ├── test_agents.py
│   │   ├── test_offset_correction.py
│   │   └── ...
│   ├── property/                # 属性测试
│   │   ├── test_properties_excel.py
│   │   ├── test_properties_serialization.py
│   │   ├── test_properties_offset.py
│   │   └── ...
│   ├── integration/             # 集成测试
│   │   ├── test_api_corpus.py
│   │   ├── test_api_annotation.py
│   │   └── ...
│   └── conftest.py              # pytest配置和fixtures
```

#### 前端测试目录结构
```
frontend/
├── src/
│   ├── components/
│   │   └── __tests__/
│   │       ├── AnnotationEditor.test.ts
│   │       └── ...
│   ├── composables/
│   │   └── __tests__/
│   │       ├── use-offset-correction.test.ts
│   │       └── ...
│   └── utils/
│       └── __tests__/
│           └── ...
```

### 属性测试标注规范

每个属性测试必须使用注释明确标注其对应的设计文档中的属性编号和需求编号：

```python
def test_property_1_excel_validation():
    """
    **Feature: entity-relation-annotation-tool, Property 1: Excel文件验证完整性**
    **Validates: Requirements 1.1**
    
    For any Excel文件，如果文件格式为xlsx且包含所有必需列，
    则验证函数应返回true；否则应返回false并指出缺失的列
    """
    @given(excel_file=excel_file_strategy())
    def property_test(excel_file):
        result = validate_excel_file(excel_file)
        # 验证逻辑
        ...
```

### 测试策略详解

#### 1. Excel处理测试

**单元测试**:
- 测试特定的Excel文件示例
- 测试空文件、单行文件等边界情况
- 测试包含特殊字符的文本

**属性测试**:
- Property 1: Excel文件验证完整性
- Property 2: 图片ID映射一致性
- Property 3: 图片文件导出完整性
- Property 4: DISPIMG转换正确性
- Property 5: 文本分句一致性

#### 2. 偏移量处理测试

**单元测试**:
- 测试简单的偏移量计算
- 测试中文、英文、混合文本
- 测试特殊字符和emoji

**属性测试**:
- Property 18: 实体偏移量验证正确性
- Property 23: 文本选择偏移量计算正确性
- Property 44: 偏移量修正准确性
- Property 45: 最近匹配选择正确性

#### 3. 序列化测试

**单元测试**:
- 测试特定的实体和关系示例
- 测试空列表、单个元素等边界情况

**属性测试**:
- Property 12: 标签配置序列化往返一致性
- Property 48: 标注数据序列化往返一致性
- Property 49-52: 各类实体和关系的序列化格式正确性

#### 4. LLM Agent测试

**单元测试**:
- 使用Mock模拟LLM响应
- 测试结构化输出解析
- 测试降级解析策略

**属性测试**:
- Property 16: LLM实体抽取输出格式正确性
- Property 17: 多模态标注输出格式正确性
- Property 19: 关系实体ID有效性

#### 5. 数据一致性测试

**单元测试**:
- 测试级联删除
- 测试事务回滚
- 测试并发修改

**属性测试**:
- Property 8: 数据集任务创建一致性
- Property 10: 级联删除完整性
- Property 26: 版本回滚一致性

### 测试数据生成策略

使用Hypothesis/fast-check的策略（Strategy）生成测试数据：

```python
from hypothesis import strategies as st

# 文本实体策略
@st.composite
def text_entity_strategy(draw):
    text = draw(st.text(min_size=10, max_size=100))
    start = draw(st.integers(min_value=0, max_value=len(text)-1))
    end = draw(st.integers(min_value=start+1, max_value=len(text)))
    label = draw(st.sampled_from(ENTITY_TYPES))
    return Entity(
        id=draw(st.integers(min_value=0)),
        token=text[start:end],
        label=label,
        start_offset=start,
        end_offset=end
    )

# Excel文件策略
@st.composite
def excel_file_strategy(draw):
    has_required_columns = draw(st.booleans())
    if has_required_columns:
        columns = REQUIRED_COLUMNS
    else:
        columns = draw(st.lists(st.text(), min_size=1, max_size=5))
    # 生成Excel文件内容
    ...
```

### 测试覆盖率目标

- **代码覆盖率**: ≥80%
- **分支覆盖率**: ≥70%
- **核心业务逻辑覆盖率**: ≥90%
- **属性测试迭代次数**: ≥100次/属性

### 持续集成

- 每次提交自动运行所有测试
- 测试失败阻止合并
- 生成测试覆盖率报告
- 定期运行长时间属性测试（1000+迭代）


## 性能考虑

### 性能目标

- **文件上传**: 支持最大100MB的Excel文件，处理时间<30秒
- **批量标注**: 1000条句子的批量标注完成时间<10分钟
- **页面加载**: 标注编辑页面首次加载时间<2秒
- **实时响应**: 用户交互响应时间<200ms
- **并发用户**: 支持10个并发用户同时标注

### 性能优化策略

#### 1. 数据库优化

**索引设计**:
```sql
-- 语料查询索引
CREATE INDEX idx_corpus_text_id ON corpus(text_id);
CREATE INDEX idx_corpus_source_field ON corpus(source_field);

-- 任务查询索引
CREATE INDEX idx_tasks_dataset_id ON annotation_tasks(dataset_id);
CREATE INDEX idx_tasks_status ON annotation_tasks(status);
CREATE INDEX idx_tasks_corpus_id ON annotation_tasks(corpus_id);

-- 实体查询索引
CREATE INDEX idx_entities_task_id ON text_entities(task_id);
CREATE INDEX idx_entities_version ON text_entities(task_id, version);

-- 关系查询索引
CREATE INDEX idx_relations_task_id ON relations(task_id);
CREATE INDEX idx_relations_version ON relations(task_id, version);
```

**查询优化**:
- 使用分页查询避免一次加载大量数据
- 使用JOIN减少多次查询
- 对频繁查询的统计数据使用缓存

#### 2. 文件处理优化

- **流式处理**: 使用流式读取Excel文件，避免一次性加载到内存
- **并行处理**: 使用多进程处理图片提取和文本分句
- **增量处理**: 支持断点续传，失败后可从中断处继续

#### 3. LLM调用优化

- **批量调用**: 将多个句子合并为一个批次调用LLM
- **异步处理**: 使用异步IO处理LLM API调用
- **结果缓存**: 对相同文本的标注结果进行缓存
- **限流控制**: 控制并发调用数量，避免超过API限制

#### 4. 前端性能优化

- **虚拟滚动**: 大量实体/关系列表使用虚拟滚动
- **懒加载**: 图片使用懒加载，按需加载
- **防抖节流**: 文本选择、搜索等操作使用防抖
- **组件缓存**: 使用keep-alive缓存页面组件

#### 5. 图片处理优化

- **缩略图生成**: 自动生成缩略图用于列表显示
- **图片压缩**: 对大图片进行压缩存储
- **CDN加速**: 生产环境使用CDN加速图片加载

### 监控指标

- **API响应时间**: 监控各API端点的平均响应时间
- **数据库查询时间**: 监控慢查询
- **LLM调用成功率**: 监控LLM API的成功率和平均响应时间
- **内存使用**: 监控服务器内存使用情况
- **磁盘使用**: 监控磁盘空间使用情况

## 安全考虑

### 认证和授权

- **JWT Token**: 使用JWT进行用户认证
- **Token过期**: Token有效期24小时，支持刷新
- **角色权限**: 基于角色的访问控制（RBAC）
- **API权限**: 每个API端点检查用户权限

### 数据安全

- **密码加密**: 使用bcrypt加密存储密码
- **SQL注入防护**: 使用参数化查询防止SQL注入
- **XSS防护**: 前端对用户输入进行转义
- **CSRF防护**: 使用CSRF Token防护

### 文件安全

- **文件类型验证**: 严格验证上传文件类型
- **文件大小限制**: 限制上传文件大小
- **文件名清理**: 清理文件名中的特殊字符
- **病毒扫描**: 可选的文件病毒扫描

### 数据备份

- **定期备份**: 每天自动备份SQLite数据库
- **增量备份**: 支持增量备份减少备份时间
- **备份验证**: 定期验证备份文件的完整性
- **灾难恢复**: 提供数据恢复工具和流程

## 扩展性设计

### 数据库迁移路径

当前使用SQLite作为初始数据库，未来可迁移到：

1. **MySQL**: 用于多用户并发场景
2. **Neo4j**: 用于复杂的图谱查询和分析
3. **MinIO**: 用于分布式图片存储

**迁移策略**:
- 使用SQLAlchemy ORM，便于切换数据库
- 提供数据导出/导入工具
- 保持API接口不变

### 功能扩展点

1. **多模态扩展**: 支持视频、音频等其他模态的标注
2. **协同标注**: 支持多人同时标注同一数据集
3. **主动学习**: 基于模型不确定性选择待标注样本
4. **标注质量评估**: 自动评估标注质量，识别低质量标注
5. **知识图谱可视化**: 将标注数据可视化为知识图谱

### 集成接口

- **模型训练接口**: 提供API供训练系统拉取标注数据
- **外部标注工具**: 支持导入/导出Label Studio等工具的格式
- **Webhook通知**: 支持标注完成、复核完成等事件的Webhook通知

## 部署方案

### 开发环境

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 前端
cd frontend
npm install
npm run dev
```

### 生产环境

**Docker部署**:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

**系统要求**:
- CPU: 4核心以上
- 内存: 8GB以上
- 磁盘: 100GB以上（根据数据量调整）
- 操作系统: Linux/Windows/macOS

