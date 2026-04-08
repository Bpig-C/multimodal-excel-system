# 项目架构文档

> 最后更新：2026-04-02（索引同步更新：+57/-3837行，变更集中于排除test文件 + 新增content_hash迁移）

## 架构概览

**品质失效案例实体关系标注系统** - 一款面向品质失效案例的自动化实体关系标注工具

**技术栈**：
- 后端：FastAPI + LangChain + SQLAlchemy + SQLite
- 前端：Vue 3 + TypeScript + Element Plus + Pinia + Vite
- LLM：Qwen-Max（DashScope API）

**核心设计模式**：
- 分层架构（API / Service / Model）
- JWT 无状态认证
- 标签体系版本化管理（Schema Versioning）
- 处理器插件模式（BaseProcessor 抽象基类）
- 存储服务抽象（StorageService：本地 ↔ MinIO）

**数据流**：
```
Excel/文档导入 → 语料库(Corpus) → 数据集(Dataset) → 标注任务(AnnotationTask)
                                                    ↓
                                              LLM自动标注（Agent）
                                                    ↓
                                              人工复核(Review)
                                                    ↓
                                              导出(Export)
```

**扩展点**：
1. 新增标注类型：扩展 `EntityType`/`RelationType` 表 + Agent 实现
2. 新增导出格式：扩展 `ExportService`/`StructuredExportService`
3. 存储后端切换：本地文件系统 ↔ MinIO
4. 新处理器类型：实现 `BaseProcessor` 抽象基类

**对外接口**：
- RESTful API（FastAPI，自动生成 OpenAPI 文档）
- 轮询状态查询（无 WebSocket）
- 静态文件服务（图片、导出文件）

## 系统能力说明

**认证与授权**：
- 认证方式：JWT Token（HS256，24小时过期）
- 角色管理：有（admin / annotator / reviewer / browser）
- 权限粒度：路由级（基于角色的访问控制 RBAC）

**状态管理**（前端）：
- 方案：Pinia（多个 store：auth, corpus, dataset, annotation, label, review, document）
- 持久化：sessionStorage（token）

**缓存策略**：
- 后端缓存：Label 配置缓存（`LabelConfigCache`）
- 前端缓存：无

**任务队列 / 异步处理**：
- 方案：后台任务 + 轮询状态
- 批量标注：`BatchAnnotationService`
- 进度跟踪：`BatchJob` 模型

**多租户 / 数据隔离**：
- 方案：按数据集隔离（`dataset_id` 关联）
- 无独立数据库隔离

**国际化（i18n）**：
- 方案：硬编码中文（无 i18n 框架）

**日志与监控**：
- 日志：loguru（结构化日志）+ 自定义中间件
- 监控：无

**WebSocket / 实时通信**：
- 用途：无（轮询获取任务状态）

**文件存储**：
- 方案：本地磁盘 / MinIO（可配置，通过 `STORAGE_TYPE` 环境变量）
- 图片：`data/images/`
- 上传：`data/uploads/`
- 导出：`data/exports/`
- 处理后数据：`data/processed/{processor}/{data_source}/`

## 数据处理管线

### 管线A：表格解析骨架（`FailureCaseProcessor`）
**用途**：Excel 文件初步解析，提取表格结构和基本信息

**处理流程**：
```
Excel文件上传 → DocumentProcessor → FailureCaseProcessor.parse_excel()
                                            ↓
                                    输出 JSON 到 data/processed/
```

**输出**：表格元信息（sheet名称、记录数、列名），不创建语料记录

### 管线B：多模态数据转换与AI标注（`ExcelProcessingService` + Agents）
**用途**：WPS Excel 解析、图文多模态数据生成、LLM 自动标注

**处理流程**：
```
Excel文件上传 → ExcelProcessingService
    ├── extract_wps_excel_images() - 提取 WPS 内嵌图片
    ├── 读取 Excel DataFrame
    ├── _convert_dispimg_to_markdown() - DISPIMG公式→Markdown
    ├── 分句处理（按单元格，不进一步分句）
    ├── 创建 Corpus 记录 + Image 关联
    │
    ↓（可选）自动标注
EntityExtractionAgent - 实体抽取
RelationExtractionAgent - 关系抽取
ImageAnnotationAgent - 图片标注
```

**核心特性**：
- WPS Excel 特殊格式支持（`xl/cellimages.xml` + `xl/_rels/cellimages.xml.rels`）
- DISPIMG 公式转换：`=DISPIMG("ID_XXX", 数字)` → `![图片](ID_XXX)`
- 多模态语料：文本 + 图片引用关联
- 存储服务：`StorageService`（本地文件系统 / MinIO 可切换）

### 处理器插件（`/processors/`）
| 处理器 | 用途 | 适用场景 |
|--------|------|----------|
| `failure_case.py` | 品质失效案例骨架 | 管线A |
| `kf/` | 快反数据解析 | KF数据导入（快反事件表） |
| `qms/` | QMS数据解析 | QMS不合格品记录导入 |

**处理器基类**（`base.py`）：
- 抽象接口：`name`, `display_name`, `field_mapping`, `parse_excel()`, `get_export_config()`, `get_graph_config()`
- 默认实体的标准字段：event_id, occurrence_time, problem_analysis, images, data_source, short_term_measure, long_term_measure, classification, customer, product_model, product_category, industry_category, defect, root_cause_category, process_category, four_m_element, workshop, production_line, station, inspection_node, status, barcode, position

### KF/QMS 数据模型

**去重机制**：`content_hash` 字段（SHA256）用于 KF 快反事件和 QMS 不合格品记录的业务层去重兜底。

**快反数据**（`quick_response_events`）：
- 主键：id（VARCHAR，非自增）
- 关联：客户、产品、缺陷、原因、4M要素

**QMS数据**（`qms_defect_orders`）：
- 主键：id（VARCHAR，非自增）
- 关联：客户、车间、产线、岗位、质检节点、缺陷

## API 路由层（`/backend/api/`）

| 路由文件 | 核心职责 |
|----------|----------|
| `annotations.py` | 标注任务 CRUD + 提交复核 |
| `corpus.py` | 语料管理 |
| `corpus_grouped.py` | 按 source_field 分组的语料查询 |
| `dataset.py` | 数据集管理 |
| `dataset_assignment.py` | 数据集-用户分配（task_start_index / task_end_index 范围分配） |
| `document_import.py` | 文档上传/导入/图片上传/彻底删除 |
| `structured_export.py` | 结构化导出（Excel 格式） |
| `labels.py` | 标签配置（实体类型/关系类型） |
| `versions.py` | 标签体系版本管理 |
| `review.py` | 复核流程 |
| `images.py` | 图片管理 |
| `users.py` + `auth.py` | 用户认证 |
| `data_query.py` | KF/QMS 数据查询 |
| `config_api.py` | 系统配置 |
| `graph_api.py` | 实体关系图谱查询 |

## 服务层（`/backend/services/`）

| 服务文件 | 核心职责 |
|----------|----------|
| `batch_annotation_service.py` | 批量标注任务调度 + 进度跟踪 |
| `dataset_service.py` | 数据集操作 |
| `label_management_service.py` | 标签生命周期管理 |
| `label_config_cache.py` | 标签配置内存缓存（TTL） |
| `export_service.py` | JSONL 数据导出 + train/test 分割 |
| `structured_export_service.py` | 结构化 Excel 导出 |
| `review_service.py` | 复核流程逻辑 |
| `graph_builder.py` | 实体关系图构建 |
| `qms_graph_builder.py` | QMS 专用图构建 |
| `excel_processing.py` | WPS Excel 解析 + 图片提取 + DISPIMG 转换 |
| `document_processor.py` | 文档处理入口（管线A） |
| `data_parser.py` | 数据解析器 |
| `storage_service.py` | 存储抽象（本地/MinIO） |
| `version_management_service.py` | 标签体系版本管理 |
| `dataset_assignment_service.py` | 数据集分配逻辑 |
| `reward_dataset_service.py` | 奖励数据集服务 |
| `serialization_service.py` | 序列化服务 |
| `task_query_service.py` | 任务查询服务 |
| `query_engine.py` | KF/QMS 查询引擎 |
| `dynamic_prompt_builder.py` | 动态 Prompt 构建 |
| `offset_correction.py` | 实体偏移量校正 |

## Agent 层（`/backend/agents/`）

| Agent文件 | 核心职责 |
|-----------|----------|
| `entity_extraction.py` | 实体抽取（LangChain + Qwen-Max） |
| `relation_extraction.py` | 关系抽取（LangChain + Qwen-Max） |
| `image_annotation.py` | 图片标注（边界框） |
| `label_definition_generator.py` | 标签定义生成（LLM 辅助） |

**实体类型体系**（16类预定义）：
- 产品、问题类型、缺陷现象、原因分类、具体原因、工序、设备、物料、人员、客户、供应商、批次/编号、时间、地点/场所、纠正措施、相关文档

## 前端架构（`/frontend/src/`）

### 路由结构
```
/ (MainLayout)
├── /login - 登录
├── / - 首页
├── /corpus - 语料管理（admin/annotator）
├── /datasets - 数据集列表
├── /datasets/my - 我的数据集（annotator/reviewer）
├── /datasets/:id - 数据集详情
├── /datasets/:id/assign - 数据集分配（admin）
├── /labels - 标签配置（admin/annotator）
├── /annotations - 标注任务列表（admin/annotator）
├── /annotations/:taskId - 标注编辑器（核心）
├── /review - 复核列表（admin/annotator）
├── /review/:reviewId - 复核详情
├── /users - 用户管理（admin）
├── /document/import - 表格数据导入
├── /document/data-list - 数据列表
├── /document/statistics - 数据分析
└── /multimodal/export - 多模态语料导出
```

### Pinia Store
| Store | 核心职责 |
|-------|----------|
| `auth.ts` | 用户认证状态 |
| `corpus.ts` | 语料状态 |
| `dataset.ts` | 数据集状态 |
| `label.ts` | 标签状态 |
| `annotation.ts` | 标注任务状态 + 批量任务跟踪 |
| `review.ts` | 复核状态 |
| `document.ts` | 文档上传状态 |

### 核心组件
| 组件 | 核心职责 |
|------|----------|
| `TextAnnotationEditor.vue` | 文本标注编辑器（高亮 + 偏移量校正） |
| `ImageAnnotationEditor.vue` | 图片标注编辑器（边界框绘制） |
| `EntityHighlight.vue` | 实体高亮渲染 |
| `RelationArrowLayer.vue` | SVG 关系箭头层 |
| `CorpusSelector.vue` | 语料选择器 |
| `BatchAnnotationDialog.vue` | 批量标注对话框 |
| `VersionManager.vue` | 标签体系版本管理 |
| `DefinitionReview.vue` | 标签定义审核 |
| `CorpusGroupedView.vue` | 按字段分组的语料视图 |

### API 客户端（`/frontend/src/api/`）
- 基于 Axios 封装
- 请求拦截器：自动附加 JWT token
- 响应拦截器：统一错误处理（401跳转登录、403权限不足等）
- 上传超时：5分钟（文件上传单独设置）

## 数据库表结构

### 核心标注模块
- `users` - 用户表（admin/annotator/reviewer/browser）
- `corpus` - 原始语料表
- `images` - 图片表
- `datasets` - 数据集表
- `dataset_corpus` - 数据集-语料关联表
- `dataset_assignments` - 数据集分配表（支持范围分配 task_start_index/task_end_index）
- `annotation_tasks` - 标注任务表
- `text_entities` - 文本实体表
- `image_entities` - 图片实体表（支持边界框）
- `relations` - 关系表
- `entity_types` - 实体类型配置表
- `relation_types` - 关系类型配置表
- `review_tasks` - 复核任务表
- `version_history` - 版本历史表（快照存储）
- `batch_jobs` - 批量任务表（进度跟踪）
- `label_schema_versions` - 标签体系版本表

### KF/QMS 模块
- `customers` - 客户表（KF/QMS共用）
- `products` - 产品型号表
- `defects` - 缺陷类型表（KF/QMS共用）
- `root_causes` - 异常原因表
- `four_m_elements` - 4M要素表
- `quick_response_events` - 快反事件表（content_hash 去重）
- `qms_workshops` - QMS车间表
- `qms_production_lines` - QMS产线表
- `qms_stations` - QMS岗位表
- `qms_inspection_nodes` - QMS质检节点表
- `qms_defect_orders` - QMS不合格品记录表（content_hash 去重）

## 集成指南

### 如何添加新功能
1. **后端**：在对应 `services/` 添加业务逻辑，在 `api/` 添加路由
2. **前端**：在 `views/` 添加页面，在 `stores/` 添加状态，在 `api/` 添加调用
3. **数据库**：如需新表，在 `models/db_models.py` 添加模型

### 如何添加新标签类型
1. 在 `LabelManagement` 页面添加实体/关系类型
2. LLM 会根据 `EntityType.prompt_template` 生成 Prompt
3. 支持在标签管理页面配置定义、示例、辨析

### 如何导出数据
1. 使用 `ExportService`（JSONL）或 `StructuredExportService`（Excel）
2. 支持 train/test 分割
3. 支持按状态筛选（approved/completed等）

### 如何添加新处理器
1. 在 `processors/` 下创建新目录（如 `processors/my_processor/`）
2. 实现 `BaseProcessor` 抽象基类的所有接口
3. 在 `document_import.py` 中注册新处理器

## 关键配置

### 环境变量（`.env`）
```
DATABASE_URL=...                    # 数据库连接
DASHSCOPE_API_KEY=...               # 阿里云 DashScope API Key
LLM_MODEL=qwen-max                 # LLM 模型
LLM_TEMPERATURE=0.0                # LLM 温度
LLM_TIMEOUT_SECONDS=120            # LLM 超时
STORAGE_TYPE=local                  # 存储类型（local/minio）
UPLOAD_DIR, IMAGE_DIR, EXPORT_DIR  # 存储路径
MINIO_*                            # MinIO 配置（可选）
```

### 存储目录结构
```
data/
├── uploads/{processor_name}/      # 上传文件
├── images/{filename}/             # 提取的图片
├── exports/                       # 导出文件
├── processed/{processor}/{data_source}/
│   └── imgs/                      # 处理后的图片
└── database/                       # SQLite 数据库
```
