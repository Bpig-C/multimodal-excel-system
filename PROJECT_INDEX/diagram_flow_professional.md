# 业务流程图描述（专业级）

> 用途：供专业人士绘制技术业务流程图，模块级粒度，含角色泳道和状态机
> 最后更新：2026-04-16

---

## 一、总体流程概述

系统包含三条相对独立但有关联的主流程：

1. **主流程：标注生产流程**（核心）
2. **支撑流程A：数据接入流程**（为主流程提供语料）
3. **支撑流程B：标签体系管理流程**（为主流程提供配置）

---

## 二、主流程：标注生产流程

### 泳道角色
- admin（管理员）
- annotator（标注员）
- reviewer（复核员）
- LLM Agent（AI 自动标注）

### 流程步骤

```
[admin] 创建数据集
    ↓ 关联语料（corpus → dataset_corpus）
    ↓ 绑定标签体系版本（label_schema_version_id）
    ↓
[admin] 分配标注任务
    ↓ 创建 dataset_assignments（task_start_index ~ task_end_index 范围）
    ↓ 每条语料生成一个 annotation_task（status=pending）
    ↓
━━━━━ 分支：自动标注 / 手工标注 ━━━━━

分支A：LLM 自动标注（BatchAnnotationService）
    [admin/annotator] 触发批量标注
    ↓ 创建 BatchJob（status=pending）
    ↓
    [LLM Agent] 循环处理每个 annotation_task
        ├── EntityExtractionAgent → 写入 text_entities
        ├── RelationExtractionAgent → 写入 relations
        └── ImageAnnotationAgent（如有图片）→ 写入 image_entities
    ↓ annotation_task.status → completed
    ↓ BatchJob.progress 实时更新（前端轮询）
    ↓

分支B：手工标注
    [annotator] 打开标注编辑器（/annotations/:taskId）
    ↓ 加载 corpus 文本 + 关联 images
    ↓ 操作文本高亮 → 创建/修改 text_entities
    ↓ 操作关系连线 → 创建/修改 relations
    ↓（如有图片）绘制边界框 → 创建/修改 image_entities
    ↓ 保存 → 写入数据库，版本号 +1，写入 version_history
    ↓

━━━━━ 汇合：提交复核 ━━━━━

    [annotator] 提交复核
    ↓ annotation_task.status → processing（待复核）
    ↓ 创建 review_task（status=pending）
    ↓
    [reviewer] 进入复核工作台（/review/:reviewId）
    ↓ 查看标注结果，对比标签定义
    ↓
    ├── 通过 → review_task.status=approved
    │         annotation_task.status=completed
    │
    └── 退回 → review_task.status=rejected + 填写 review_comment
              annotation_task.status=pending（返回标注员）
              ↑（循环至手工标注步骤）
    ↓
[admin] 数据导出
    ├── ExportService → JSONL 格式（train/test 分割）
    └── StructuredExportService → Excel 格式
```

### 关键状态机：annotation_task.status
```
pending → processing → completed
pending → processing → failed
completed → （可被管理员重置）
```

### 关键状态机：review_task.status
```
pending → approved
pending → rejected → （触发 annotation_task 回到 pending）
```

---

## 三、支撑流程A：数据接入流程

### 管线A：骨架解析（FailureCaseProcessor）

```
[admin] 上传 Excel 文件（/document/import）
    ↓ DocumentProcessor → FailureCaseProcessor.parse_excel()
    ↓ 输出：表格元信息（sheet名称、记录数、列名）→ data/processed/
    ↓ 不创建 corpus 记录（仅预览/验证）
```

### 管线B：多模态语料生成（ExcelProcessingService）

```
[admin] 上传 WPS Excel 文件
    ↓ ExcelProcessingService.process()
    ├── extract_wps_excel_images()
    │       → 解析 xl/cellimages.xml + xl/_rels/cellimages.xml.rels
    │       → 提取图片 → 写入 data/images/ → 创建 Image 记录
    ├── 读取 DataFrame（pandas）
    ├── _convert_dispimg_to_markdown()
    │       → DISPIMG 公式 → ![图片](image_id) Markdown 引用
    ├── 按单元格拆分句子
    └── 创建 Corpus 记录 + 关联 Image（corpus.has_images=True）
    ↓ 语料入库完成 → 可进入主流程
```

### 管线C：KF 快反数据导入（KFProcessor）

```
[admin] 上传 KF Excel 文件
    ↓ KFProcessor.parse_excel()
    ↓ 结构化解析 → 写入 quick_response_events
    ↓ content_hash 去重（SHA256，跳过已存在记录）
    ↓ 关联维度表（customers / products / defects / root_causes / four_m_elements）
    ↓ 数据入库 → 可通过 data_query 接口查询
```

### 管线D：QMS 不合格品数据导入（QMSProcessor）

```
[admin] 上传 QMS Excel 文件
    ↓ QMSProcessor.parse_excel()
    ↓ 结构化解析 → 写入 qms_defect_orders
    ↓ content_hash 去重（SHA256，跳过已存在记录）
    ↓ 关联维度表（customers / qms_workshops / qms_production_lines /
    │              qms_stations / qms_inspection_nodes / defects）
    ↓ 数据入库 → 可通过 data_query 接口查询
```

---

## 四、支撑流程B：标签体系管理流程

```
[admin] 进入标签配置页（/labels）
    ↓
    ├── 手动创建实体类型（EntityType）/ 关系类型（RelationType）
    │
    └── AI 辅助生成标签定义
            [admin] 选择类型，触发 LabelDefinitionGenerator
            ↓ LLM 生成：definition / examples / disambiguation
            ↓ 写入 entity_types / relation_types
            ↓ is_reviewed=false（待审核状态）
            ↓
            [admin] 在 DefinitionReview 组件中审核
            ↓ 通过 → is_reviewed=true，recorded reviewer_id / reviewed_at
    ↓
[admin] 保存标签体系版本快照
    ↓ VersionManagementService.create_version()
    ↓ 写入 label_schema_versions（schema_data = 完整 JSON 快照）
    ↓ is_active 切换到新版本
    ↓ 创建数据集时可绑定指定版本
```

---

## 五、图谱查询流程（独立功能）

```
[用户] 访问图谱查询页
    ↓ 选择数据集 / 过滤条件
    ↓ 调用 graph_api 接口
    ↓ GraphBuilder（普通标注）/ QmsGraphBuilder（QMS 数据）
    ↓ 从 annotation_tasks + text_entities + relations 构建图结构
    ↓ 返回节点 + 边列表 → 前端图可视化渲染
```

---

## 六、关键横切流程

### 认证流程
```
用户提交用户名/密码 → auth 路由验证 → 生成 JWT Token（24h）
→ 存入 sessionStorage → 后续请求 Axios 拦截器自动附加 Authorization 头
→ FastAPI 依赖注入验证 Token → 解析角色 → RBAC 路由守卫
```

### 前端状态轮询（批量任务进度）
```
触发批量标注 → 获取 job_id → 前端定时轮询 /batch_jobs/{job_id}
→ BatchJob.progress（0.0~1.0）+ completed_tasks / total_tasks
→ 进度条更新 → progress=1.0 时停止轮询
```

---

## 七、绘图建议

- **推荐格式**：泳道流程图（Swimlane Diagram）
- **泳道划分**：admin / annotator / reviewer / LLM Agent / System（系统自动）
- **状态机**：annotation_task 和 review_task 的状态机可单独绘制为状态图（State Diagram）
- **管线图**：数据接入四条管线可单独绘制为数据流图（DFD）
- **可拆分**：主流程 + 支撑流程分开绘制，总览图仅展示三条流程的关系
