# 品质数据平台合并迁移计划

> 版本：v1.1 | 日期：2026-03-30 | 状态：待执行（已根据现有代码审核修正）

---

## 一、项目背景与目标

### 1.1 现有两个系统

**KFSystem（快反问题知识图谱系统）**
- 技术栈：FastAPI + 原生SQLite + Vue 3 + Element Plus
- 核心能力：KF/QMS两种Excel表格解析、知识图谱化、三种多模态语料导出（entity_text/CLIP/Q&A）
- 架构亮点：Processor插件模式（BaseProcessor → KF/QMS），ExportConfig驱动的导出框架
- 不足：无认证、无ORM、无迁移管理、前端TypeScript不严格

**实体关系标注系统（品质失效案例实体关系标注系统）**
- 技术栈：FastAPI + SQLAlchemy + LangChain + Vue 3 + TypeScript + Pinia
- 核心能力：语料管理、AI实体关系标注（Qwen-Max）、人工审核、标签版本管理、标注结果导出
- 架构亮点：JWT认证+角色权限、SQLAlchemy ORM+Alembic迁移、完整TypeScript类型系统、AI Agent模式
- 不足：无多模态语料导出、无Processor插件框架

### 1.2 合并目标

将两个系统合并为一个统一的**品质数据平台**，实现：

1. 统一文档解析入口：支持KF表格、QMS表格、品质失控案例三种文件的上传和解析
2. 统一多模态语料导出：三种文件均支持entity_text/CLIP/Q&A格式导出（管线A，规则转换，不需要AI）
3. 品质失控案例专属标注：仅品质失控案例支持AI实体关系标注→人工审核→JSONL导出（管线B）
4. 图谱功能暂时搁置：代码保留但前端入口隐藏，后续恢复
5. 未来视频标注集成预留：前端路由级集成，后端完全独立

### 1.3 合并原则

- **主体选择**：以标注系统为主体（基础设施全面领先），将KFSystem模块迁入
- **不做架构重构**：利用标注系统现有的分层架构，KFSystem代码做局部适配即可
- **两条管线独立**：多模态语料导出（管线A）和实体关系标注导出（管线B）完全解耦

---

## 二、核心架构决策

### 2.1 两条导出管线设计

这是整个合并方案的核心设计决策。两条管线服务于不同目的、使用不同数据源、在不同时间点可用。

**管线A：多模态语料导出（规则转换，即时可用）**

```
Excel上传 → Processor.parse_excel() → JSON/结构化数据
                                          │
                                          ▼
                                    CorpusExporter
                                    （改名为 StructuredExportService）
                                          │
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                         entity_text   CLIP对齐    Q&A对齐
```

- 适用文件：KF表格、QMS表格、品质失控案例（三种都支持）
- 数据源：Processor解析出的JSON/结构化字段
- 核心逻辑：字段映射 + 模板填充，纯数据转换
- 特点：上传后立即可导出，不需要等AI处理
- 每种Processor通过`get_export_config()`定义自己的字段映射、CLIP字段顺序、Q&A模板

**管线B：实体关系标注导出（需要AI+人工，周期性）**

```
Excel上传 → FailureCaseProcessor.build_corpus_records()
                → corpus表 → 创建dataset → 创建annotation_tasks
                    → AI Agent标注（实体提取 + 关系提取）
                        → 人工审核
                            → ExportService.export_jsonl()
```

- 适用文件：仅品质失控案例
- 数据源：标注结果（text_entities + relations + image_entities）
- 核心逻辑：AI提取 → 人工校验 → 结构化导出
- 特点：需要完整的标注和审核流程，导出的是高质量的实体关系数据

**两条管线的关系**：完全独立，互不依赖。用户导入品质失控案例后，可以立即通过管线A导出多模态语料，同时可以发起管线B的标注流程。两者不冲突。

### 2.2 Processor插件框架扩展

在KFSystem原有BaseProcessor基础上，新增对语料生成的支持：

```python
class BaseProcessor(ABC):
    """表格处理器基类"""
    
    # ===== 原有接口（管线A需要）=====
    @abstractmethod
    def parse_excel(self, file_path: str, output_dir: str) -> dict: ...
    
    @abstractmethod
    def get_export_config(self) -> ExportConfig: ...
    
    @abstractmethod
    def get_graph_config(self) -> GraphConfig: ...
    
    def extract_entities(self, record: Dict, data_source: str = None) -> Dict: ...
    
    def build_entity_text(self, record: Dict, data_source: str = None) -> str: ...
    
    @property
    @abstractmethod
    def field_mapping(self) -> Dict[str, str]: ...
    
    @property
    @abstractmethod
    def default_values(self) -> Dict[str, str]: ...
    
    @property
    @abstractmethod
    def column_mappings(self) -> Dict[str, str]: ...
    
    # ===== 管线B接口（已废弃，见下方修正说明）=====
    # ⚠️ v1.1修正：build_corpus_records()不在Processor层实现。
    # 管线B直接复用标注系统的ExcelProcessingService.process_excel_file()，
    # 该服务已完整实现WPS图片提取、DISPIMG转换、文本清洗、corpus写库全流程。
    # BaseProcessor无需扩展任何管线B相关接口。
```

三种Processor的职责分工：

| Processor | parse_excel | 管线A（多模态导出） | 管线B（语料→标注） | 图谱化 |
|-----------|------------|-------------------|-------------------|--------|
| KFProcessor | HTML表格解析 | ✅ 支持 | ❌ 不支持 | ✅ GraphBuilder |
| QMSProcessor | pandas直读 | ✅ 支持 | ❌ 不支持 | ✅ QMSGraphBuilder |
| FailureCaseProcessor（新增） | pandas直读 | ✅ 支持 | ✅ 支持（由ExcelProcessingService处理，Processor层不介入） | ❌ 不需要 |

> ⚠️ **v1.1重要修正**：管线B的语料生成不经过Processor框架。标注系统已有
> `services/excel_processing.py` → `ExcelProcessingService.process_excel_file()`，
> 完整实现了WPS图片提取（`extract_wps_excel_images`）、DISPIMG公式转换、
> 文本清洗、corpus+image写库全流程。上传品质失控案例时，直接调用此服务即可，
> **无需在BaseProcessor中新增任何接口**。

### 2.3 数据存储边界

```
合并后的数据库（annotation.db 扩展）
│
├── 原标注系统的表（保持不变）
│   ├── users                    用户和认证
│   ├── corpus                   语料（仅品质失控案例的文本）
│   ├── images                   图片
│   ├── datasets                 数据集
│   ├── dataset_corpus           数据集-语料关联
│   ├── dataset_assignments      数据集分配
│   ├── annotation_tasks         标注任务
│   ├── text_entities            文本实体
│   ├── image_entities           图片实体
│   ├── relations                关系
│   ├── entity_types             实体类型配置
│   ├── relation_types           关系类型配置
│   ├── review_tasks             审核任务
│   ├── version_history          版本历史
│   ├── batch_jobs               批量任务
│   └── label_schema_versions    标签版本
│
└── 从KFSystem迁入的表（新增）
    ├── customers                客户（KF+QMS共用）
    ├── products                 产品型号（KF）
    ├── defects                  缺陷类型（KF+QMS共用）
    ├── root_causes              异常原因（KF）
    ├── four_m_elements          4M要素（KF）
    ├── quick_response_events    快反事件（KF）
    ├── qms_workshops            QMS车间
    ├── qms_production_lines     QMS产线
    ├── qms_stations             QMS岗位
    ├── qms_inspection_nodes     QMS质检节点
    └── qms_defect_orders        QMS不合格品记录
```

关键边界：
- corpus表**仅存品质失控案例**的文本片段，不存KF/QMS数据
- KF/QMS的结构化数据存入各自的关系表
- 两类表之间**无外键关联**，通过Processor层区分

### 2.4 API路由规划

```
/api/v1/
│
├── /auth/                        认证（原标注系统，统一入口）
│   ├── POST /login
│   └── GET  /me
│
├── /users/                       用户管理（原标注系统）
│
├── /config/                      处理器配置（从KFSystem迁入）
│   ├── GET /processors                    处理器列表
│   ├── GET /processors/{name}/graph-config 图谱配置
│   └── GET /processors/{name}/field-mapping 字段映射
│
├── /documents/                   文档解析（新建，整合两个系统的上传逻辑）
│   ├── POST /upload              Excel上传+解析（三种文件通用）
│   ├── POST /import              JSON数据导入到结构化表
│   ├── POST /images              图片ZIP包上传
│   └── GET  /processed-files     已处理文件列表
│
├── /export/                      导出（分两个子路由）
│   ├── /corpus/{processor}/      管线A：多模态语料导出
│   │   ├── POST /entity-text
│   │   ├── POST /clip-alignment
│   │   ├── POST /qa-alignment
│   │   └── POST /batch           批量打包导出
│   │
│   └── /annotation/{dataset_id}/ 管线B：标注结果导出
│       └── POST /jsonl
│
├── /graph/                       图谱查询（从KFSystem迁入，暂时隐藏前端入口）
│   ├── GET /data
│   ├── GET /events/{id}
│   └── GET /statistics
│
├── /data/                        数据列表查询（从KFSystem迁入）
│   ├── GET /list                 KF/QMS数据浏览
│   └── GET /statistics           统计分析
│
├── /corpus/                      语料管理（原标注系统，仅品质失控案例）
│   ├── POST /upload
│   ├── GET  /
│   └── GET  /grouped
│
├── /datasets/                    数据集管理（原标注系统）
├── /annotations/                 标注管理（原标注系统）
├── /labels/                      标签管理（原标注系统）
├── /review/                      审核管理（原标注系统）
└── /versions/                    版本管理（原标注系统）
```

### 2.5 前端导航结构

```
┌─────────────────────────────────────────────────────┐
│  品质数据平台                                         │
│                                                       │
│  ┌─ 数据管理 ─────────────────────────────────────┐  │
│  │  文档导入    数据列表    多模态导出    统计分析   │  │
│  │  （三种文件）（KF/QMS浏览）（管线A）              │  │
│  └─────────────────────────────────────────────────┘  │
│                                                       │
│  ┌─ 标注工作台 ───────────────────────────────────┐  │
│  │  语料管理    数据集     标注任务     审核列表   │  │
│  │  标签管理    标注导出（管线B）                   │  │
│  │  （仅品质失控案例）                              │  │
│  └─────────────────────────────────────────────────┘  │
│                                                       │
│  ┌─ 系统管理 ─────────────────────────────────────┐  │
│  │  用户管理    （图谱可视化 - 暂时隐藏）          │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### 2.6 认证策略

- 统一使用标注系统的JWT + 角色认证
- KFSystem迁入的API全部走认证中间件
- 第一阶段使用默认admin账户（admin/admin123）
- 角色权限保留但不强制分配：
  - admin：全部功能
  - annotator：标注相关 + 数据管理（只读）
  - reviewer：审核相关 + 数据管理（只读）

---

## 三、合并后目标目录结构

```
project-root/
├── backend/
│   ├── __init__.py
│   ├── main.py                          FastAPI应用入口（原标注系统，新增路由注册）
│   ├── config.py                        配置管理（原标注系统）
│   ├── database.py                      SQLAlchemy引擎和会话（原标注系统）
│   ├── init_db.py                       数据库初始化（原标注系统，新增KF/QMS表）
│   │
│   ├── api/                             API路由层
│   │   ├── __init__.py
│   │   ├── annotations.py              标注API（原标注系统）
│   │   ├── corpus.py                   语料API（原标注系统）
│   │   ├── corpus_by_row.py            按行查询语料（原标注系统）
│   │   ├── corpus_grouped.py           分组查询语料（原标注系统）
│   │   ├── dataset.py                  数据集API（原标注系统）
│   │   ├── dataset_assignment.py       数据集分配API（原标注系统）
│   │   ├── images.py                   图片API（原标注系统）
│   │   ├── labels.py                   标签API（原标注系统）
│   │   ├── review.py                   审核API（原标注系统）
│   │   ├── users.py                    用户API（原标注系统）
│   │   ├── versions.py                 版本API（原标注系统）
│   │   ├── config_api.py              【迁入】处理器配置API
│   │   ├── document_import.py         【新建】统一文档上传/导入API
│   │   ├── structured_export.py       【迁入】管线A多模态语料导出API
│   │   ├── data_query.py             【迁入】数据列表查询API
│   │   └── graph_api.py              【迁入】图谱查询API（暂时不注册路由）
│   │
│   ├── models/                          数据模型层
│   │   ├── __init__.py
│   │   ├── db_models.py                SQLAlchemy模型（原标注系统，新增KF/QMS表模型）
│   │   └── schemas.py                  Pydantic Schema（原标注系统）
│   │
│   ├── services/                        业务服务层
│   │   ├── __init__.py
│   │   ├── batch_annotation_service.py 批量标注服务（原标注系统）
│   │   ├── dataset_service.py          数据集服务（原标注系统）
│   │   ├── dataset_assignment_service.py 数据集分配服务（原标注系统）
│   │   ├── excel_processing.py         Excel处理服务（原标注系统）
│   │   ├── export_service.py           管线B标注结果导出（原标注系统）
│   │   ├── label_management_service.py 标签管理服务（原标注系统）
│   │   ├── review_service.py           审核服务（原标注系统）
│   │   ├── storage_service.py          存储服务（原标注系统）
│   │   ├── user_service.py             用户服务（原标注系统）
│   │   ├── version_management_service.py 版本管理服务（原标注系统）
│   │   ├── structured_export_service.py【迁入】管线A CorpusExporter改名
│   │   ├── data_parser.py             【迁入】JSON数据解析
│   │   ├── document_processor.py      【迁入】Excel处理+重复检测
│   │   ├── graph_builder.py           【迁入】KF图谱构建器
│   │   └── qms_graph_builder.py       【迁入】QMS图谱构建器
│   │
│   ├── processors/                     【整体迁入】处理器插件
│   │   ├── __init__.py                 处理器注册表
│   │   ├── base.py                     BaseProcessor（扩展supports_corpus接口）
│   │   ├── kf/
│   │   │   ├── __init__.py             KFProcessor
│   │   │   ├── config.py              KF配置常量
│   │   │   ├── excel_tools.py         WPS/MS图片提取
│   │   │   ├── node.py                HTML表格解析
│   │   │   └── parser.py              KF Excel解析
│   │   ├── qms/
│   │   │   ├── __init__.py             QMSProcessor
│   │   │   ├── config.py              QMS配置常量
│   │   │   └── parser.py              QMS Excel解析
│   │   └── failure_case/              【新建】品质失控案例处理器
│   │       ├── __init__.py             FailureCaseProcessor
│   │       └── config.py              品质失控配置常量
│   │
│   ├── agents/                          AI Agent模块（原标注系统，不改动）
│   │   ├── __init__.py
│   │   ├── entity_extraction.py
│   │   ├── relation_extraction.py
│   │   ├── image_annotation.py
│   │   └── label_definition_generator.py
│   │
│   ├── middleware/                       中间件（原标注系统，不改动）
│   │   ├── __init__.py
│   │   ├── error_handler.py
│   │   └── logging_config.py
│   │
│   ├── migrations/                      数据库迁移
│   │   ├── v001_initial_schema.sql     原标注系统初始Schema
│   │   ├── v002_add_batch_jobs.sql
│   │   ├── v003_add_dataset_assignment.sql
│   │   ├── v004_add_task_query_indexes.sql
│   │   └── v005_add_kf_qms_tables.sql 【新建】KF/QMS表迁移脚本
│   │
│   ├── utils/                           工具函数
│   │   ├── __init__.py
│   │   └── file_utils.py              【迁入】文件名规范化
│   │
│   ├── scripts/                         维护脚本
│   │   └── db_migrate.py              数据库迁移执行器
│   │
│   └── tests/                           测试（原标注系统，后续补充）
│
├── frontend/
│   ├── src/
│   │   ├── api/                         API客户端
│   │   │   ├── request.ts              统一请求封装（原标注系统）
│   │   │   ├── auth.ts                 认证API（原标注系统）
│   │   │   ├── annotation.ts           标注API（原标注系统）
│   │   │   ├── corpus.ts              语料API（原标注系统）
│   │   │   ├── dataset.ts             数据集API（原标注系统）
│   │   │   ├── label.ts               标签API（原标注系统）
│   │   │   ├── review.ts              审核API（原标注系统）
│   │   │   ├── user.ts                用户API（原标注系统）
│   │   │   ├── version.ts             版本API（原标注系统）
│   │   │   ├── image.ts               图片API（原标注系统）
│   │   │   └── document.ts           【新建】文档导入/导出/查询API
│   │   │
│   │   ├── types/
│   │   │   ├── index.ts               类型定义（原标注系统，新增KF/QMS类型）
│   │   │   └── assignment.ts          分配类型（原标注系统）
│   │   │
│   │   ├── stores/                     Pinia状态管理
│   │   │   ├── annotation.ts          标注状态（原标注系统）
│   │   │   ├── auth.ts                认证状态（原标注系统）
│   │   │   ├── corpus.ts             语料状态（原标注系统）
│   │   │   ├── dataset.ts            数据集状态（原标注系统）
│   │   │   ├── label.ts              标签状态（原标注系统）
│   │   │   ├── review.ts             审核状态（原标注系统）
│   │   │   ├── user.ts               用户状态（原标注系统）
│   │   │   └── document.ts          【新建】文档管理状态
│   │   │
│   │   ├── views/
│   │   │   ├── Login.vue              登录（原标注系统）
│   │   │   ├── Home.vue               首页（原标注系统，改造为平台首页）
│   │   │   ├── NotFound.vue           404（原标注系统）
│   │   │   │
│   │   │   ├── annotation/            标注相关（原标注系统，不改动）
│   │   │   │   ├── AnnotationPage.vue
│   │   │   │   ├── AnnotationEditor.vue
│   │   │   │   └── AnnotationList.vue
│   │   │   │
│   │   │   ├── dataset/               数据集相关（原标注系统，不改动）
│   │   │   │   ├── DatasetManagement.vue
│   │   │   │   ├── DatasetDetail.vue
│   │   │   │   ├── DatasetAssignment.vue
│   │   │   │   └── MyDatasets.vue
│   │   │   │
│   │   │   ├── corpus/                语料管理（原标注系统，不改动）
│   │   │   │   └── CorpusManagement.vue
│   │   │   │
│   │   │   ├── label/                 标签管理（原标注系统，不改动）
│   │   │   │   ├── LabelManagement.vue
│   │   │   │   └── LabelConfig.vue
│   │   │   │
│   │   │   ├── review/                审核相关（原标注系统，不改动）
│   │   │   │   ├── ReviewList.vue
│   │   │   │   └── ReviewDetail.vue
│   │   │   │
│   │   │   ├── user/                  用户管理（原标注系统，不改动）
│   │   │   │   └── UserManagement.vue
│   │   │   │
│   │   │   └── document/             【新建】数据管理模块
│   │   │       ├── DocumentImport.vue   文档导入页面
│   │   │       ├── DataList.vue         数据列表浏览页面
│   │   │       ├── DataStatistics.vue   统计分析页面
│   │   │       └── GraphVisualization.vue 图谱可视化（暂时隐藏路由）
│   │   │
│   │   ├── components/
│   │   │   ├── annotation/            标注组件（原标注系统，不改动）
│   │   │   ├── dataset/               数据集组件（原标注系统，不改动）
│   │   │   ├── corpus/                语料组件（原标注系统，不改动）
│   │   │   ├── label/                 标签组件（原标注系统，不改动）
│   │   │   └── document/            【新建】数据管理组件
│   │   │       ├── ExportDialog.vue     单文件导出对话框
│   │   │       └── BatchExportDialog.vue 批量导出对话框
│   │   │
│   │   ├── layouts/
│   │   │   └── MainLayout.vue         主布局（原标注系统，修改导航结构）
│   │   │
│   │   ├── router/
│   │   │   └── index.ts               路由配置（原标注系统，新增数据管理路由）
│   │   │
│   │   └── App.vue                    根组件
│   │
│   ├── index.html
│   └── vite.config.ts
│
├── data/                               数据目录
│   ├── database/
│   │   └── annotation.db              统一数据库
│   ├── uploads/                        上传文件暂存
│   ├── images/                         图片存储
│   ├── exports/                        导出文件暂存
│   └── processed/                     【新增】Excel解析后的JSON文件存储
│       └── {processor}/{data_source}/  按处理器和数据源分目录
│
└── scripts/                            维护脚本
    ├── maintenance/                   【迁入】数据清理脚本
    ├── tests/                         【迁入】测试脚本
    └── utils/                         【迁入】检查工具
```

---

## 四、分阶段实施计划

### 阶段一：后端基座迁移（P0，预计5个任务）

本阶段目标：将KFSystem的核心后端模块迁入标注系统，通过API可用但不连接前端。

#### 任务 1.1：迁移Processor插件框架

**目标**：在标注系统后端建立processors/目录，KF和QMS处理器可实例化

> ⚠️ **v1.1修正**：原计划要扩展BaseProcessor新增`supports_corpus`和`build_corpus_records()`接口，
> 经审核后**取消此扩展**。管线B语料生成由`ExcelProcessingService`直接负责，与Processor框架无关。
> BaseProcessor原样迁移即可。

**操作步骤**：
1. 在`backend/`下创建`processors/`目录
2. 从`参考项目代码/kfandQMS/KFsystem_2026-03-30_11-48-38.md`中提取以下文件内容，复制到目标位置：
   - `backend/app/processors/base.py` → `backend/processors/base.py`
   - `backend/app/processors/__init__.py` → `backend/processors/__init__.py`
   - `backend/app/processors/kf/__init__.py` → `backend/processors/kf/__init__.py`
   - `backend/app/processors/kf/config.py` → `backend/processors/kf/config.py`
   - `backend/app/processors/kf/excel_tools.py` → `backend/processors/kf/excel_tools.py`
   - `backend/app/processors/kf/node.py` → `backend/processors/kf/node.py`
   - `backend/app/processors/kf/parser.py` → `backend/processors/kf/parser.py`
   - `backend/app/processors/qms/__init__.py` → `backend/processors/qms/__init__.py`
   - `backend/app/processors/qms/config.py` → `backend/processors/qms/config.py`
   - `backend/app/processors/qms/parser.py` → `backend/processors/qms/parser.py`
3. 调整所有文件内的import路径：将`from backend.app.processors`或`from app.processors`改为`from processors`（以能在`backend/`目录下正常运行为准）
4. **不对BaseProcessor做任何额外扩展**

**适配要点**：
- KFProcessor和QMSProcessor的`parse_excel()`是纯文件操作（读Excel→输出JSON），不需要改数据库调用
- `extract_entities()`和`build_entity_text()`也是纯内存操作，不需要改
- `get_graph_config()`保留原样，后续图谱恢复时可直接用
- **不需要**新增`supports_corpus`或`build_corpus_records()`，BaseProcessor原样迁移

**验证标准**：
```python
from processors import get_processor, list_processors
kf = get_processor('kf')
qms = get_processor('qms')
assert kf.name == 'kf'
assert qms.name == 'qms'
print("All OK!")
```

**需要给MiniMax的文件**：
- KFSystem的`processors/`目录下全部文件（从repomix中提取完整代码）
- 标注系统的`backend/`目录树（仅结构，不需要代码）
- BaseProcessor扩展接口定义（本文档2.2节的代码片段）

**预计工作量**：1个任务

---

#### 任务 1.2：迁移KF/QMS数据库Schema

**目标**：在标注系统的SQLAlchemy模型中新增11张KF/QMS表

**操作步骤**：
1. 在`backend/models/db_models.py`末尾新增以下SQLAlchemy模型：
   - `Customer`（customers表）：id, name(UNIQUE)
   - `Product`（products表）：id, model(UNIQUE), product_category, industry_category
   - `Defect`（defects表）：id, name(UNIQUE)
   - `RootCause`（root_causes表）：id, category, process_category
   - `FourMElement`（four_m_elements表）：id, element(UNIQUE)
   - `QuickResponseEvent`（quick_response_events表）：id(TEXT PK), occurrence_time, problem_analysis, short_term_measure, long_term_measure, images, data_source, classification, 5个外键（customer_id, product_id, defect_id, root_cause_id, four_m_id）
   - `QMSWorkshop`（qms_workshops表）：id, name(UNIQUE)
   - `QMSProductionLine`（qms_production_lines表）：id, name, workshop_id(FK), UNIQUE(name, workshop_id)
   - `QMSStation`（qms_stations表）：id, name(UNIQUE)
   - `QMSInspectionNode`（qms_inspection_nodes表）：id, name(UNIQUE)
   - `QMSDefectOrder`（qms_defect_orders表）：id(TEXT PK), entry_time, model, barcode, position, photo_path, status, data_source, 6个外键
2. 为每个模型添加relationship定义
3. 创建迁移脚本`backend/migrations/v005_add_kf_qms_tables.sql`
4. 修改`backend/init_db.py`，在`main()`中确保新表也被创建

**适配要点**：
- KFSystem原来用`sqlite3.connect()`直接建表，这里改为SQLAlchemy声明式模型
- QuickResponseEvent的id是TEXT类型（不是自增INTEGER），需要`Column(String, primary_key=True)`
- QMSDefectOrder的id也是TEXT类型
- customers和defects是KF/QMS共用表，只建一份模型

**验证标准**：
```python
from database import init_db
init_db()  # 应该成功创建所有表包括新增的11张
```

**需要给MiniMax的文件**：
- `KFsystem_database_schema.md`（完整，作为源表定义）
- 标注系统的`models/db_models.py`（作为写法参考，展示现有模型的风格）
- 标注系统的`database.py`（了解Base和engine的定义方式）

**预计工作量**：1个任务

---

#### 任务 1.3：迁移数据导入服务和API

**目标**：实现统一的文档上传和数据导入接口

**操作步骤**：
1. 将KFSystem的`excel_processor.py`迁移为`backend/services/document_processor.py`
   - 核心功能：Excel文件上传 → 调用Processor.parse_excel() → 输出JSON
   - 文件哈希计算和重复检测逻辑保留
   - 文件保存路径改为`data/processed/{processor}/{data_source}/`
   - 去掉原来的`sqlite3`调用，改为SQLAlchemy session
2. 将KFSystem的`data_parser.py`迁移为`backend/services/data_parser.py`
   - JSON解析和版本检测逻辑保留
   - `extract_entities()`委托给Processor保持不变
3. 将KFSystem的`graph_builder.py`和`qms_graph_builder.py`迁移到`backend/services/`
   - **所有`sqlite3.connect()`改为接收SQLAlchemy `Session`参数**
   - 所有`cursor.execute()`改为`db.execute(text(...))`
   - 所有`conn.commit()`改为`db.commit()`
4. 新建`backend/api/document_import.py`路由：
   - `POST /api/v1/documents/upload` —— 接收Excel文件+processor_name参数，调用DocumentProcessor
   - `POST /api/v1/documents/import` —— 接收JSON文件路径+processor_name，调用DataParser+GraphBuilder导入
   - `POST /api/v1/documents/images` —— 接收图片ZIP包，解压到对应目录
   - `GET /api/v1/documents/processed-files` —— 获取已处理文件列表
   - 所有路由需要JWT认证
5. 在`backend/main.py`中注册新路由

**适配要点**：
- KFSystem的upload_api和import_api合并为一个document_import.py
- 原来的`DATABASE_PATH`硬编码路径改为通过`get_db()`依赖注入获取session
- GraphBuilder的`build_graph(self, entities)`签名改为`build_graph(self, db: Session, entities)`
- QMSGraphBuilder同理
- 品质失控案例的导入除了调GraphBuilder外，还需要额外调用`build_corpus_records()`写入corpus表（当`supports_corpus=True`时）

**导入流程（分支逻辑）**：
```python
async def upload_excel(file, processor_name: str, db: Session):
    processor = get_processor(processor_name)
    
    # 1. Excel解析（三种文件通用）
    result = document_processor.process_excel(file, processor)
    
    # 2. 数据导入到结构化表（KF/QMS走这个分支）
    if processor_name in ('kf', 'qms'):
        parser = DataParser(processor_name)
        for json_file in result['json_files']:
            records = parser.parse_json_file(json_file)
            for record in records:
                entities = parser.extract_entities(record)
                graph_builder.build_graph(db, entities)
    
    # 3. 语料生成（品质失控案例走这个分支）
    if processor.supports_corpus:
        corpus_records = processor.build_corpus_records(
            parsed_data, source_file=file.filename
        )
        for cr in corpus_records:
            # 写入corpus表（复用标注系统的ExcelProcessingService逻辑）
            ...
    
    return result
```

**验证标准**：
- 上传KF Excel → JSON文件生成在data/processed/kf/下 → 数据写入quick_response_events表
- 上传QMS Excel → JSON文件生成在data/processed/qms/下 → 数据写入qms_defect_orders表
- 重复上传同一文件 → 返回"已处理"提示

**需要给MiniMax的文件**：
- KFSystem的`upload_api.py` + `import_api.py`（原始API逻辑）
- KFSystem的`excel_processor.py`（重复检测逻辑）
- KFSystem的`data_parser.py`（JSON解析逻辑）
- KFSystem的`graph_builder.py` + `qms_graph_builder.py`（写入逻辑）
- 标注系统的`api/corpus.py`或任意一个API文件（了解路由写法和get_db()用法）
- 标注系统的`database.py`（了解Session用法）
- 任务1.1的产出：`processors/`目录代码
- 任务1.2的产出：新增的SQLAlchemy模型

**预计工作量**：2个任务（可拆分为1.3a导入服务+1.3b导入API）

---

#### 任务 1.4：迁移多模态语料导出服务和API（管线A）

**目标**：三种Processor都支持entity_text/CLIP/Q&A格式的多模态语料导出

**操作步骤**：
1. 将KFSystem的`corpus_exporter.py`迁移为`backend/services/structured_export_service.py`
   - 类名改为`StructuredExportService`
   - 构造函数接收`processor_name`参数
   - 内部通过`get_processor()`获取Processor实例
   - 三个导出方法保持不变：`export_entity_text()`, `export_clip_alignment()`, `export_qa_alignment()`
   - 数据源：从data/processed/{processor}/目录读取JSON文件（不涉及数据库查询）
2. 新建`backend/api/structured_export.py`路由：
   - `POST /api/v1/export/corpus/{processor}/entity-text` —— 实体文本格式导出
   - `POST /api/v1/export/corpus/{processor}/clip-alignment` —— CLIP格式导出
   - `POST /api/v1/export/corpus/{processor}/qa-alignment` —— Q&A格式导出
   - `POST /api/v1/export/corpus/{processor}/batch` —— 批量打包导出（多文件+多格式+图片→ZIP）
   - 所有路由需要JWT认证
3. 在`backend/main.py`中注册新路由

**适配要点**：
- CorpusExporter原来通过文件路径读取JSON数据，这个逻辑保持不变
- 批量导出的ZIP打包逻辑（图片收集、临时文件创建、流式下载）完整保留
- processor参数通过路由路径传入，内部通过`get_processor(processor)`获取配置
- 品质失控案例的ExportConfig需要在任务3.1中定义，但导出框架先搭好

**验证标准**：
- `POST /api/v1/export/corpus/kf/entity-text` → 返回KF的实体文本JSON
- `POST /api/v1/export/corpus/qms/clip-alignment` → 返回QMS的CLIP对齐JSON
- 批量导出 → 返回ZIP文件（含多格式JSON + 图片）

**需要给MiniMax的文件**：
- KFSystem的`corpus_exporter.py`（完整代码）
- KFSystem的`export_api.py`（API路由逻辑）
- KFSystem的`kf/config.py`和`qms/config.py`（ExportConfig配置参考）
- 标注系统的`api/`目录中任意一个文件（路由写法参考）

**预计工作量**：1个任务

---

#### 任务 1.5：迁移处理器配置API和数据查询API

**目标**：前端能获取处理器列表、字段映射配置，能查询KF/QMS数据和统计信息

**操作步骤**：
1. 将KFSystem的`config_api.py`迁移到`backend/api/config_api.py`
   - 三个端点保持不变：`/processors`、`/processors/{name}/graph-config`、`/processors/{name}/field-mapping`
   - 添加JWT认证
2. 将KFSystem的`graph_api.py`中的数据查询和统计部分迁移到`backend/api/data_query.py`
   - 数据列表查询：根据processor_name查询对应的表
   - 统计分析：缺陷分布、客户排行等
   - `QueryEngine`的`sqlite3.connect()`改为接收SQLAlchemy Session
3. 图谱查询API（`graph_api.py`）迁移到`backend/api/graph_api.py`但**暂时不在main.py中注册路由**
4. 在`backend/main.py`中注册config_api和data_query路由

**适配要点**：
- KFSystem的QueryEngine整体迁移，但所有`sqlite3.connect()`改为SQLAlchemy
- 统计查询的SQL保持不变（SQLAlchemy的`db.execute(text("SELECT..."))`可以直接执行原始SQL）
- 图谱相关的API代码搬过来但不激活，需要时取消注释即可

**验证标准**：
- `GET /api/v1/config/processors` → 返回['kf', 'qms']
- `GET /api/v1/config/processors/kf/field-mapping` → 返回KF的字段映射
- 数据查询API能返回quick_response_events和qms_defect_orders的记录

**需要给MiniMax的文件**：
- KFSystem的`config_api.py`（完整代码）
- KFSystem的`graph_api.py`（完整代码，说明只迁移数据查询和统计部分）
- KFSystem的`query_engine.py`（完整代码）
- 标注系统的`database.py`（Session用法参考）

**预计工作量**：1个任务

---

### 阶段一完成检查点

完成阶段一后，后端应该能通过以下API验证：

```
POST /api/v1/auth/login                    ✅ 登录获取JWT
GET  /api/v1/config/processors             ✅ 返回处理器列表
POST /api/v1/documents/upload              ✅ 上传Excel并解析
GET  /api/v1/documents/processed-files     ✅ 查看已处理文件
POST /api/v1/export/corpus/kf/entity-text  ✅ KF多模态导出
POST /api/v1/export/corpus/qms/qa-alignment ✅ QMS多模态导出

原标注系统的所有API                           ✅ 全部正常（未被改动）
```

**Claude介入点**：阶段一完成后，审核SQLAlchemy适配是否正确、API路由注册是否完整。

---

### 阶段二：前端整合（P0，预计4个任务）

本阶段目标：将KFSystem的前端页面迁入标注系统前端，统一导航。

#### 任务 2.1：新建前端API客户端和类型定义

**目标**：为新增的后端API创建前端调用封装和TypeScript类型

**操作步骤**：
1. 新建`frontend/src/api/document.ts`
   - `uploadExcel(file, processorName)` → `POST /documents/upload`
   - `importJsonData(source, filePath, processorName)` → `POST /documents/import`
   - `uploadImagesZip(file, dataSource)` → `POST /documents/images`
   - `getProcessedFiles()` → `GET /documents/processed-files`
   - `getProcessors()` → `GET /config/processors`
   - `getFieldMapping(processorName)` → `GET /config/processors/{name}/field-mapping`
   - `exportEntityText(processor, params)` → `POST /export/corpus/{processor}/entity-text`
   - `exportClipAlignment(processor, params)` → `POST /export/corpus/{processor}/clip-alignment`
   - `exportQaAlignment(processor, params)` → `POST /export/corpus/{processor}/qa-alignment`
   - `batchExport(processor, params)` → `POST /export/corpus/{processor}/batch`
   - `getDataList(processor, params)` → `GET /data/list`
   - `getStatistics(processor)` → `GET /data/statistics`
2. 在`frontend/src/types/index.ts`中新增类型定义：
   - `ProcessorInfo { name, display_name }`
   - `ProcessedFile { filename, data_source, record_count, ... }`
   - `QuickResponseEvent { id, occurrence_time, customer, product, defect, ... }`
   - `QMSDefectOrder { id, entry_time, model, workshop, defect, ... }`
   - `ExportFormat = 'entity_text' | 'clip_alignment' | 'qa_alignment'`
   - `StatisticsData { total_events, defect_distribution, customer_ranking, ... }`
3. 新建`frontend/src/stores/document.ts`
   - 管理processor选择状态
   - 管理已处理文件列表
   - 管理导出状态

**适配要点**：
- 所有API调用使用标注系统的`request.ts`封装（自带JWT token注入）
- 所有类型严格TypeScript定义
- Store使用Pinia的组合式API风格（与标注系统现有store保持一致）

**需要给MiniMax的文件**：
- 标注系统的`api/request.ts`（了解请求封装方式）
- 标注系统的`api/annotation.ts`（任意一个API文件作为写法参考）
- 标注系统的`types/index.ts`（了解类型定义风格）
- 标注系统的`stores/annotation.ts`（了解store风格）
- 任务1.3-1.5产出的API路由定义（知道端点路径和参数）

**预计工作量**：1个任务

---

#### 任务 2.2：迁移文档导入页面

**目标**：创建统一的文档导入页面，支持KF/QMS/品质失控案例三种文件上传

**操作步骤**：
1. 新建`frontend/src/views/document/DocumentImport.vue`
   - 参考KFSystem的`DataImport.vue`但改写为TypeScript + Pinia
   - 顶部：处理器选择下拉框（el-select，选项来自`getProcessors()` API）
   - 主区域：Excel文件拖拽上传（el-upload），显示上传进度
   - 下方：已处理文件列表（el-table），每行显示文件名、数据源、记录数
   - 每个已处理文件提供"导出"按钮（打开ExportDialog）
2. 迁移`ExportDialog.vue`到`frontend/src/components/document/ExportDialog.vue`
   - 改写为TypeScript
   - 三种导出格式的radio选择
   - 使用document.ts中的API调用
3. 迁移`BatchExportDialog.vue`到`frontend/src/components/document/BatchExportDialog.vue`
   - 改写为TypeScript
   - 支持多文件+多格式批量导出
   - 下载进度显示

**适配要点**：
- KFSystem的`DataImport.vue`使用的是Options API，需要改为Composition API + `<script setup lang="ts">`
- 原来直接使用axios，改为使用`document.ts`中封装的API函数
- 处理器切换时要清空文件列表并重新加载
- 样式保持Element Plus风格，与标注系统视觉统一

**需要给MiniMax的文件**：
- KFSystem的`DataImport.vue`（完整代码）
- KFSystem的`ExportDialog.vue`（完整代码）
- KFSystem的`BatchExportDialog.vue`（完整代码）
- 任务2.1产出的`api/document.ts`和`stores/document.ts`
- 标注系统的`views/corpus/CorpusManagement.vue`（Vue页面写法参考）

**预计工作量**：1个任务

---

#### 任务 2.3：迁移数据列表和统计页面

**目标**：创建KF/QMS数据浏览页面和统计分析页面

**操作步骤**：
1. 新建`frontend/src/views/document/DataList.vue`
   - 参考KFSystem的`DataList.vue`改写为TypeScript
   - 顶部处理器选择（切换KF/QMS查看不同数据）
   - KF模式：显示快反事件列表（发生时间、客户、产品、缺陷、措施等列）
   - QMS模式：显示不合格品记录列表（入库时间、型号、车间、缺陷等列）
   - 支持分页、搜索、筛选
   - 点击行可查看详情
2. 新建`frontend/src/views/document/DataStatistics.vue`
   - 参考KFSystem的`Statistics.vue`改写为TypeScript
   - 总览统计卡片（总记录数、客户数、缺陷类型数等）
   - 图表：缺陷类型分布（柱状图）、4M要素分布（饼图）、客户问题排行（横向柱状图）
   - QMS模式下显示不同的统计维度（车间分布、产线分布等）

**需要给MiniMax的文件**：
- KFSystem的`DataList.vue`（完整代码）
- KFSystem的`Statistics.vue`（完整代码）
- 任务2.1产出的`api/document.ts`中的数据查询和统计API
- 标注系统的任意一个list/table页面（写法参考）

**预计工作量**：1个任务

---

#### 任务 2.4：统一导航和路由注册

**目标**：将所有新页面整合到统一导航结构中

**操作步骤**：
1. 修改`frontend/src/router/index.ts`新增路由：
   ```typescript
   // 数据管理路由组
   { path: '/document/import', component: DocumentImport, meta: { title: '文档导入' } },
   { path: '/document/list', component: DataList, meta: { title: '数据列表' } },
   { path: '/document/statistics', component: DataStatistics, meta: { title: '统计分析' } },
   // 图谱路由（暂时注释或设 meta.hidden = true）
   // { path: '/document/graph', component: GraphVisualization },
   ```
2. 修改`frontend/src/layouts/MainLayout.vue`的导航菜单：
   - 添加"数据管理"菜单组，包含：文档导入、数据列表、多模态导出、统计分析
   - 原有"标注工作台"菜单保持不变
   - 根据用户角色控制菜单可见性
3. 修改`frontend/src/views/Home.vue`首页：
   - 添加"数据管理"快捷入口卡片
   - 显示系统总览统计（两个模块的数据量汇总）

**适配要点**：
- 路由守卫确保未登录用户跳转到登录页
- 新增路由的meta.requiresAuth = true
- 导航菜单使用el-menu + el-sub-menu分组
- 移动端响应式处理

**需要给MiniMax的文件**：
- 标注系统的`router/index.ts`（当前路由配置）
- 标注系统的`layouts/MainLayout.vue`（当前导航结构）
- 标注系统的`views/Home.vue`（当前首页）
- 本文档2.5节的前端导航结构设计

**预计工作量**：1个任务

---

### 阶段二完成检查点

完成阶段二后，用户应该能：

```
1. 登录系统                                    ✅
2. 在导航栏看到"数据管理"和"标注工作台"两个区域  ✅
3. 进入"文档导入"页面，选择KF/QMS处理器上传Excel  ✅
4. 查看已导入的数据列表和统计分析                 ✅
5. 对已处理文件进行多模态语料导出                 ✅
6. 原有标注系统的所有功能正常使用                 ✅
```

**Claude介入点**：阶段二开始前审核路由设计和导航结构；阶段二完成后审核前端整合是否完整。

---

### 阶段三：品质失控案例处理器（P1，预计3个任务）

本阶段目标：新增FailureCaseProcessor，打通品质失控案例的两条管线。

#### 任务 3.1：实现FailureCaseProcessor

**目标**：品质失控案例可通过统一框架上传和解析，管线A（多模态导出）可用

> ⚠️ **v1.1修正**：原计划中`FailureCaseProcessor`需实现`supports_corpus=True`和
> `build_corpus_records()`。经审核，**这两个接口全部取消**。管线B（语料写库）
> 直接由`ExcelProcessingService.process_excel_file()`负责，与Processor无关。
> 本任务的FailureCaseProcessor仅需实现管线A所需接口。

**品质失控案例Excel格式**（已确认，来自`参考项目代码/品质失效案例-2022年-客户端质量问题.xlsx`）：

| 列名 | 字段用途 | 管线A导出 |
|------|---------|----------|
| 问题分类 | 分类标签 | 结构化字段 |
| 客户/发生工程/供应商 | 主体信息 | 结构化字段 |
| 质量问题 | 问题标题 | entity_text标题 |
| 问题描述 | 事件描述 | ✅ 核心文本字段 |
| 问题处理 | 处置措施 | ✅ 文本字段 |
| 原因分析 | 失效原因 | ✅ 核心文本字段 |
| 采取措施 | 纠正预防 | ✅ 核心文本字段 |
| 图片 | DISPIMG公式 | CLIP图文对 |

**操作步骤**：
1. 新建`backend/processors/failure_case/config.py`
   - 定义`COLUMN_MAPPINGS`（Excel列名→内部字段名）
   - 定义`FIELD_MAPPING`（内部字段名→中文标签）
   - 定义`ENTITY_FIELDS`（参与entity_text的字段列表：问题描述、原因分析、采取措施）
   - 定义`CLIP_FIELDS`（CLIP导出字段顺序：图片字段 + 对应文本字段）
   - 定义`QA_QUERY`（如"该品质失控案例描述的问题是什么？根本原因是什么？采取了哪些措施？"）
2. 新建`backend/processors/failure_case/__init__.py`
   - 实现`FailureCaseProcessor(BaseProcessor)`
   - `name` = `'failure_case'`
   - `display_name` = `'品质失控案例'`
   - `parse_excel()` —— 使用pandas直读（类似QMSProcessor），输出JSON到`data/processed/failure_case/`
   - `get_export_config()` —— 返回品质失控案例的ExportConfig
   - `build_entity_text()` —— 拼接各文本字段构建实体文本描述
   - `get_graph_config()` —— 返回空配置（不需要图谱化）
   - **不实现`supports_corpus`和`build_corpus_records()`**
3. 在`backend/processors/__init__.py`注册表中添加`FailureCaseProcessor`

**需要给MiniMax的文件**：
- 任务1.1产出的`processors/base.py`（写法参考）
- 任务1.1产出的`processors/qms/config.py`和`processors/qms/__init__.py`（QMSProcessor实现参考，因为parse_excel同为pandas直读）
- 本文档"品质失控案例Excel格式"表格（列名定义）

**预计工作量**：1个任务

---

#### 任务 3.2：打通品质失控案例的管线B入口

**目标**：品质失控案例上传后，其文本自动进入corpus表，可创建dataset并触发AI标注

> ⚠️ **v1.1修正**：原计划在`document_import.py`中调用`processor.build_corpus_records()`。
> 经审核，**改为直接调用`ExcelProcessingService.process_excel_file()`**。
> 该服务已完整实现：WPS图片提取、DISPIMG转换、文本清洗、corpus+image写库，
> 无需在Processor层重复实现任何语料生成逻辑。

**操作步骤**：
1. 修改`backend/api/document_import.py`的upload逻辑：
   - 当`processor_name == 'failure_case'`时，除了正常的Excel解析（管线A）外，额外执行：
     ```python
     excel_service = ExcelProcessingService(db)
     corpus_result = excel_service.process_excel_file(xlsx_path, file.filename)
     ```
   - 返回结果中增加`corpus_count`字段（取自`corpus_result['corpus_count']`）
2. `ExcelProcessingService`已处理的内容（**无需额外实现**）：
   - WPS图片提取并保存到`data/images/`
   - DISPIMG公式转换为Markdown图片引用
   - 文本清洗（去除多余空白）
   - corpus记录写入（含text_id、text_type=列名、source_file、source_row、source_field）
   - Image记录写入并关联corpus_id
3. 测试完整流程：上传品质失控案例Excel → corpus表中出现记录 → 在标注系统的"语料管理"页面可以看到 → 可以创建dataset并发起批量标注

**导入流程（分支逻辑）**：
```python
async def upload_excel(file, processor_name: str, db: Session):
    processor = get_processor(processor_name)

    # 1. Excel解析（三种文件通用，管线A）
    result = document_processor.process_excel(file, processor)

    # 2. 数据导入到结构化表（KF/QMS）
    if processor_name in ('kf', 'qms'):
        parser = DataParser(processor_name)
        for json_file in result['json_files']:
            records = parser.parse_json_file(json_file)
            for record in records:
                entities = parser.extract_entities(record)
                graph_builder.build_graph(db, entities)

    # 3. 语料生成（品质失控案例，管线B入口）
    # 直接复用ExcelProcessingService，无需经过Processor框架
    if processor_name == 'failure_case':
        excel_service = ExcelProcessingService(db)
        corpus_result = excel_service.process_excel_file(
            xlsx_path=uploaded_file_path,
            source_filename=file.filename
        )
        result['corpus_count'] = corpus_result['corpus_count']

    return result
```

**需要给MiniMax的文件**：
- 任务1.3的产出：`api/document_import.py`（当前导入逻辑）
- 任务3.1的产出：`processors/failure_case/__init__.py`
- 标注系统的`services/excel_processing.py`（corpus记录创建逻辑参考）
- 标注系统的`models/db_models.py`中Corpus和Image模型定义
- 标注系统的`services/storage_service.py`（图片存储逻辑参考）

**预计工作量**：1个任务

---

#### 任务 3.3：前端处理器选项更新

**目标**：前端的文档导入页面支持选择品质失控案例处理器

**操作步骤**：
1. 由于`getProcessors()` API是动态返回的，注册新Processor后前端自动能看到
2. 但需要确认前端的处理器选择下拉框展示正确
3. 品质失控案例上传后，在"语料管理"页面应该自动可见
4. 如果DocumentImport页面有处理器特定的UI（比如QMS有图片ZIP上传），需要为品质失控案例增加对应的条件判断
5. 在"文档导入"页面的上传结果区域，品质失控案例需要额外显示"已生成N条语料"信息

**需要给MiniMax的文件**：
- 任务2.2产出的`DocumentImport.vue`
- 任务3.2的API响应格式说明

**预计工作量**：1个任务（较轻量）

---

### 阶段三完成检查点

完成阶段三后，品质失控案例的完整工作流：

```
用户上传品质失控案例Excel
        │
        ├──→ 立即可用：在"多模态导出"中选择failure_case处理器导出
        │    entity_text / CLIP / Q&A 三种格式 ✅
        │
        └──→ 异步流程：
             1. 语料自动进入"语料管理"页面 ✅
             2. 创建数据集，添加语料 ✅
             3. 触发批量AI标注 ✅
             4. 人工审核标注结果 ✅
             5. 导出JSONL ✅
```

**Claude介入点**：审核FailureCaseProcessor的config定义是否合理（需要你提供Excel格式说明）。

---

### 阶段四：收尾优化（P2，预计2个任务）

#### 任务 4.1：数据库迁移脚本整合和测试

**操作步骤**：
1. 确保`v005_add_kf_qms_tables.sql`可以在已有数据库上干净执行
2. 编写一个完整的迁移执行脚本，按顺序执行v001-v005
3. 创建基本的冒烟测试脚本：
   - 测试认证流程：登录→获取token→带token访问API
   - 测试KF上传流程：上传Excel→解析→查询数据→导出
   - 测试QMS上传流程：同上
   - 测试标注系统原有流程：创建dataset→上传语料→标注→审核→导出
4. 检查requirements.txt是否合并了两个项目的所有依赖

**预计工作量**：1个任务

---

#### 任务 4.2：图谱模块保留（可选）

**操作步骤**：
1. 确认图谱查询API代码（`graph_api.py`）已迁移到位
2. 确认GraphVisualization.vue已迁移到`views/document/`
3. 路由中注册但设置`meta.hidden = true`或注释掉
4. 文档中标注"图谱功能已就绪，取消路由隐藏即可恢复"

**预计工作量**：0.5个任务

---

## 五、资源分配策略

### 5.1 Claude的使用节点（预计4-5次交互）

| 节点 | 时机 | 目的 |
|------|------|------|
| 节点0 | 现在 | 总体规划和架构决策（已完成） |
| 节点1 | 阶段一完成后 | 审核SQLAlchemy适配、API路由注册、数据库Schema |
| 节点2 | 阶段二开始前 | 审核前端路由设计、导航结构、TypeScript类型定义 |
| 节点3 | 任务3.1之前 | 审核FailureCaseProcessor的config设计（需要你提供Excel格式） |
| 节点4 | 全部完成后 | 集成问题排查、最终审核 |

### 5.2 MiniMax的任务分配（预计12-13个任务）

| 阶段 | 任务数 | 任务编号 |
|------|--------|---------|
| 阶段一：后端基座 | 5-6 | 1.1, 1.2, 1.3a, 1.3b, 1.4, 1.5 |
| 阶段二：前端整合 | 4 | 2.1, 2.2, 2.3, 2.4 |
| 阶段三：品质失控Processor | 3 | 3.1, 3.2, 3.3 |
| 阶段四：收尾 | 1-2 | 4.1, 4.2 |

### 5.3 给MiniMax下达任务的文档策略

**核心原则：每个任务只给3-5个文件，不超过上下文窗口的60%。**

每个任务使用以下固定格式：

```
## 任务目标
[一句话]

## 项目背景（简短）
这是一个品质数据平台，基于FastAPI+Vue 3+SQLAlchemy。
当前任务是将另一个系统的[具体模块]迁入本系统。

## 当前系统中相关文件
[列出2-3个现有文件路径，说明其作用]

## 需要迁入的代码
[粘贴完整的源代码]

## 具体步骤
1. [步骤1]
2. [步骤2]
...

## 适配要求
- [具体的改动点1]
- [具体的改动点2]

## 期望输出
- 输出文件路径和内容
- 不需要改动的文件

## 验证方式
- [如何确认任务完成]
```

---

## 六、风险和注意事项

### 6.1 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| SQLAlchemy适配遗漏 | 中 | 运行时数据库错误 | 每个任务完成后立即跑冒烟测试 |
| 前端TypeScript类型不匹配 | 中 | 编译错误 | 给MiniMax提供现有类型文件作为参考 |
| 两个系统的静态文件路径冲突 | 低 | 图片无法加载 | 统一使用data/images/目录，通过data_source子目录区分 |
| FailureCaseProcessor的Excel格式不确定 | 高 | 无法完成任务3.1 | 在开始阶段三前确定Excel格式 |

### 6.2 依赖关系

```
任务1.1 ──→ 任务1.3（依赖processors）
任务1.2 ──→ 任务1.3（依赖数据库模型）
任务1.1 ──→ 任务1.4（依赖processors的ExportConfig）
任务1.3+1.4+1.5 ──→ 任务2.1（依赖后端API接口定义）
任务2.1 ──→ 任务2.2+2.3（依赖前端API客户端）
任务2.2+2.3 ──→ 任务2.4（依赖页面组件）
任务1.1 ──→ 任务3.1（依赖BaseProcessor接口）
任务3.1 ──→ 任务3.2（依赖FailureCaseProcessor）
任务3.2 ──→ 任务3.3（依赖后端导入逻辑变更）
```

任务1.1和1.2可以并行执行（无依赖关系）。

### 6.3 未来扩展预留

- **视频标注集成**：在router中预留`/video/`路由前缀，MainLayout导航预留"视频标注"菜单项（设为hidden）。后端完全独立部署，前端通过iframe或micro-frontend方式挂载。
- **新增Processor**：只需在`processors/`目录下新建子目录，实现BaseProcessor接口，注册到注册表即可。无需修改任何其他文件。
- **新增导出格式**：在StructuredExportService中新增方法，在structured_export.py中新增路由端点。
- **图谱功能恢复**：取消main.py中graph_api路由的注释，取消前端路由的hidden标记。

---

## 七、术语对照表

| 本文档用语 | KFSystem中的对应概念 | 标注系统中的对应概念 |
|-----------|--------------------|--------------------|
| 管线A | CorpusExporter导出 | 无（新增能力） |
| 管线B | 无 | ExportService.export_jsonl() |
| Processor | BaseProcessor插件 | 无（新增框架） |
| 文档导入 | upload_api + import_api | corpus.py上传 |
| 结构化表 | knowledge_graph.db中的表 | 无（新增表） |
| 语料 | 无 | corpus表中的记录 |
| 多模态语料 | entity_text/CLIP/Q&A | 无（新增能力） |
| 标注结果 | 无 | text_entities + relations |
