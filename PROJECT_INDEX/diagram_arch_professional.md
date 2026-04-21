# 系统架构图描述（专业级）

> 用途：供专业人士绘制技术架构图，模块级粒度，含技术栈标注
> 最后更新：2026-04-16

---

## 一、整体分层结构

图形建议采用**水平分层 + 垂直分组**布局，从上到下共五层：

```
[第1层] 用户端（浏览器）
[第2层] 前端应用（Vue 3 SPA）
[第3层] 后端服务（FastAPI）
[第4层] 数据持久层（SQLite）+ 文件存储
[第5层] 外部服务（DashScope LLM / MinIO）
```

---

## 二、各层节点描述

### 第1层：用户端
- **浏览器**（无需细分，单节点）
- 通过 HTTP/HTTPS 与前端交互

---

### 第2层：前端应用（Vue 3 + TypeScript + Vite）

**分为三个子模块组：**

**① 页面视图层（Views）**
- 登录页
- 数据导入页（Excel 上传 / KF 导入 / QMS 导入）
- 数据查询与统计页（数据列表 / 统计分析）
- 语料管理页（语料列表 / 分组视图）
- 数据集管理页（数据集列表 / 数据集详情 / 分配管理）
- 标注编辑器页（文本标注 + 图片标注）
- 复核页（复核列表 / 复核详情）
- 标签配置页（实体类型 / 关系类型 / 版本管理）
- 用户管理页
- 多模态导出页

**② 状态管理层（Pinia Store）**
- Auth Store（认证状态）
- Corpus Store（语料状态）
- Dataset Store（数据集状态）
- Annotation Store（标注任务 + 批量任务进度）
- Label Store（标签配置）
- Review Store（复核状态）
- Document Store（上传状态）

**③ API 客户端层（Axios）**
- 请求拦截器（自动附加 JWT Token）
- 响应拦截器（401 跳转登录 / 统一错误处理）
- 上传超时：5 分钟

**连接关系（前端内部）：**
- 页面视图层 → Pinia Store（读写状态）
- 页面视图层 → API 客户端层（发起请求）
- Pinia Store → API 客户端层（触发 API 调用）

---

### 第3层：后端服务（FastAPI + Python）

**分为四个子模块组：**

**① API 路由层（/backend/api/）**
- 认证路由（auth / users）
- 语料路由（corpus / corpus_grouped）
- 数据集路由（dataset / dataset_assignment）
- 标注路由（annotations）
- 复核路由（review）
- 标签路由（labels / versions）
- 文档导入路由（document_import）
- 图片路由（images）
- 数据查询路由（data_query）—— KF/QMS 数据查询
- 结构化导出路由（structured_export）
- 图谱查询路由（graph_api）
- 系统配置路由（config_api）

**② 业务服务层（/backend/services/）**
- 批量标注服务（BatchAnnotationService）—— 调度 + 进度跟踪
- 数据集服务（DatasetService）
- 标签管理服务（LabelManagementService + LabelConfigCache）
- 复核服务（ReviewService）
- 导出服务（ExportService —— JSONL / StructuredExportService —— Excel）
- Excel 处理服务（ExcelProcessingService）—— WPS 解析 + 图片提取 + DISPIMG 转换
- 文档处理器（DocumentProcessor）—— 管线A 骨架解析入口
- 存储服务（StorageService）—— 本地 / MinIO 可切换
- 图谱构建服务（GraphBuilder / QmsGraphBuilder）
- 版本管理服务（VersionManagementService）
- 数据集分配服务（DatasetAssignmentService）
- 查询引擎（QueryEngine）—— KF/QMS 结构化查询
- 动态 Prompt 构建（DynamicPromptBuilder）
- 实体偏移量校正（OffsetCorrectionService）

**③ AI Agent 层（/backend/agents/）**
- 实体抽取 Agent（EntityExtractionAgent）—— LangChain + Qwen-Max
- 关系抽取 Agent（RelationExtractionAgent）—— LangChain + Qwen-Max
- 图片标注 Agent（ImageAnnotationAgent）—— 边界框识别
- 标签定义生成 Agent（LabelDefinitionGenerator）—— LLM 辅助标签配置

**④ 数据处理管线（/backend/processors/）**
- BaseProcessor（抽象基类）
- FailureCaseProcessor —— 品质失效案例骨架（管线A）
- KF Processor —— 快反数据解析（管线B 变体）
- QMS Processor —— QMS 不合格品解析（管线B 变体）

**连接关系（后端内部）：**
- API 路由层 → 业务服务层（调用服务方法）
- 业务服务层 → AI Agent 层（触发 LLM 标注）
- 业务服务层 → 数据处理管线（解析文件）
- 业务服务层 → 存储服务（文件读写）
- AI Agent 层 → 外部 DashScope API（HTTP 调用）

---

### 第4层：数据持久层

**① SQLite 数据库（两大模块）**

核心标注模块（16张表）：
- users / corpus / images / datasets / dataset_corpus
- dataset_assignments / annotation_tasks
- text_entities / image_entities / relations
- entity_types / relation_types
- review_tasks / version_history
- batch_jobs / label_schema_versions

KF/QMS 数据模块（11张表）：
- customers / products / defects / root_causes / four_m_elements
- quick_response_events
- qms_workshops / qms_production_lines / qms_stations / qms_inspection_nodes / qms_defect_orders

**② 文件存储（本地目录 / MinIO）**
- data/uploads/{processor_name}/ —— 上传文件
- data/images/ —— 提取的图片
- data/exports/ —— 导出文件
- data/processed/{processor}/{data_source}/ —— 处理后中间数据

---

### 第5层：外部服务

- **DashScope API**（阿里云）：提供 Qwen-Max 大语言模型推理
- **MinIO**（可选）：对象存储，替代本地文件系统

---

## 三、跨层连接关系总览

| 来源 | 目标 | 协议/方式 |
|------|------|-----------|
| 浏览器 | 前端应用 | HTTP（静态资源加载） |
| 前端 API 客户端 | 后端 API 路由层 | RESTful HTTP（JWT 认证） |
| 后端业务服务层 | SQLite 数据库 | SQLAlchemy ORM |
| 后端存储服务 | 本地文件系统 / MinIO | 文件 I/O / MinIO SDK |
| AI Agent 层 | DashScope API | HTTPS（LangChain ChatOpenAI 兼容） |
| 前端（图片请求） | 后端静态文件服务 | HTTP |

---

## 四、关键横切关注点（可作为图注或附加图层）

- **认证体系**：JWT Token（HS256，24h 过期），RBAC 四角色（admin / annotator / reviewer / browser）
- **异步处理**：批量标注通过后台任务执行，前端轮询 batch_jobs 进度
- **版本化**：标签体系版本快照（label_schema_versions）+ 标注任务变更历史（version_history）
- **去重机制**：KF/QMS 导入数据使用 content_hash（SHA256）防止重复导入
- **标签缓存**：LabelConfigCache 内存缓存（带 TTL），减少数据库查询

---

## 五、绘图建议

- **推荐工具**：draw.io / Lucidchart / PlantUML C4 模型
- **建议分区**：按层次使用不同背景色，外部服务使用虚线框
- **可拆分为两张图**：
  1. 系统总览图（5层架构，不展开内部模块）
  2. 后端详细图（仅展开第3层，含所有服务和 Agent 节点）
