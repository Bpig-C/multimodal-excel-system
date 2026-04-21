This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.
The content has been processed where content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: **/*.md, **/*.json, **/*.log, **/*.png, **/*.jpg, **/*.jpeg, **/*.db, **/*.xlsx, **/*.bat, htmlcov/**, logs/**, backend/logs/**, backend/htmlcov/**, backend/data/images/**, backend/data/database/**, data/**, frontend/node_modules/**, frontend/dist/**, frontend/pnpm-lock.yaml, frontend/package-lock.json, PROJECT_INDEX/**, 参考项目代码/**, **/test*/**, **/*_test.py, **/*_tests.py, **/__tests__/**, backend/test_*.py, backend/tmp*.txt, .*/**
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.doc-checklist
.gitignore
账户记录.txt
backend/__init__.py
backend/.gitignore
backend/agents/__init__.py
backend/agents/entity_extraction.py
backend/agents/image_annotation.py
backend/agents/label_definition_generator.py
backend/agents/relation_extraction.py
backend/alembic.ini
backend/api/__init__.py
backend/api/annotations.py
backend/api/config_api.py
backend/api/corpus_by_row.py
backend/api/corpus_grouped.py
backend/api/corpus.py
backend/api/data_query.py
backend/api/dataset_assignment.py
backend/api/dataset.py
backend/api/document_import.py
backend/api/graph_api.py
backend/api/images.py
backend/api/labels.py
backend/api/review.py
backend/api/structured_export.py
backend/api/users.py
backend/api/versions.py
backend/check_assignments.py
backend/config.py
backend/database.py
backend/init_db.py
backend/main.py
backend/middleware/__init__.py
backend/middleware/error_handler.py
backend/middleware/logging_config.py
backend/models/__init__.py
backend/models/db_models.py
backend/models/schemas.py
backend/processors/__init__.py
backend/processors/base.py
backend/processors/failure_case.py
backend/processors/kf/__init__.py
backend/processors/kf/config.py
backend/processors/kf/excel_tools.py
backend/processors/kf/node.py
backend/processors/kf/parser.py
backend/processors/qms/__init__.py
backend/processors/qms/config.py
backend/processors/qms/parser.py
backend/pytest.ini
backend/requirements.txt
backend/scripts/apply_batch_job_migration.py
backend/scripts/apply_index_migration.py
backend/scripts/check_db_status.py
backend/scripts/check_tables.py
backend/scripts/cleanup_test_files.py
backend/scripts/db_migrate.py
backend/scripts/extract_failures.py
backend/scripts/generate_test_report.py
backend/scripts/maintenance/clean_orphan_datasets.py
backend/scripts/maintenance/force_clean_db.py
backend/scripts/maintenance/migrate_batch_jobs_fields.py
backend/scripts/maintenance/reset_db.py
backend/scripts/migration/create_default_version.py
backend/scripts/migration/migrate_dataset_assignment.py
backend/scripts/run_test_summary.py
backend/scripts/test_db_connection.py
backend/scripts/test_index_performance.py
backend/services/__init__.py
backend/services/batch_annotation_service.py
backend/services/data_parser.py
backend/services/dataset_assignment_service.py
backend/services/dataset_service.py
backend/services/document_processor.py
backend/services/dynamic_prompt_builder.py
backend/services/excel_processing.py
backend/services/export_service.py
backend/services/graph_builder.py
backend/services/label_config_cache.py
backend/services/label_management_service.py
backend/services/offset_correction.py
backend/services/qms_graph_builder.py
backend/services/query_engine.py
backend/services/review_service.py
backend/services/reward_dataset_service.py
backend/services/serialization_service.py
backend/services/storage_service.py
backend/services/structured_export_service.py
backend/services/task_query_service.py
backend/services/user_service.py
backend/services/version_management_service.py
backend/utils/__init__.py
backend/utils/file_utils.py
frontend/.env.development
frontend/.env.production
frontend/index.html
frontend/src/api/annotation.ts
frontend/src/api/auth.ts
frontend/src/api/corpus.ts
frontend/src/api/dataset.ts
frontend/src/api/document.ts
frontend/src/api/image.ts
frontend/src/api/index.ts
frontend/src/api/label.ts
frontend/src/api/request.ts
frontend/src/api/review.ts
frontend/src/api/user.ts
frontend/src/api/version.ts
frontend/src/App.vue
frontend/src/components/annotation/EntityHighlight.vue
frontend/src/components/annotation/EntityList.vue
frontend/src/components/annotation/ImageAnnotationEditor.vue
frontend/src/components/annotation/LabelSelector.vue
frontend/src/components/annotation/RelationArrowLayer.vue
frontend/src/components/annotation/RelationList.vue
frontend/src/components/annotation/RelationTypeSelector.vue
frontend/src/components/annotation/TextAnnotationEditor.vue
frontend/src/components/charts/SimplePieChart.vue
frontend/src/components/corpus/CorpusGroupedView.vue
frontend/src/components/corpus/CorpusPreview.vue
frontend/src/components/corpus/FileUploader.vue
frontend/src/components/dataset/BatchAnnotationDialog.vue
frontend/src/components/dataset/CorpusSelector.vue
frontend/src/components/dataset/DatasetCard.vue
frontend/src/components/dataset/DatasetCreateDialog.vue
frontend/src/components/dataset/DatasetEditDialog.vue
frontend/src/components/label/DefinitionReview.vue
frontend/src/components/label/EntityTypeConfig.vue
frontend/src/components/label/LabelImportExport.vue
frontend/src/components/label/PromptPreview.vue
frontend/src/components/label/RelationTypeConfig.vue
frontend/src/components/label/VersionCompare.vue
frontend/src/components/label/VersionManager.vue
frontend/src/components/label/VersionSnapshotDialog.vue
frontend/src/composables/useRelationCreation.ts
frontend/src/composables/useTextSelection.ts
frontend/src/constants/taskStatus.ts
frontend/src/layouts/MainLayout.vue
frontend/src/main.ts
frontend/src/router/index.ts
frontend/src/stores/annotation.ts
frontend/src/stores/auth.ts
frontend/src/stores/corpus.ts
frontend/src/stores/dataset.ts
frontend/src/stores/document.ts
frontend/src/stores/index.ts
frontend/src/stores/label.ts
frontend/src/stores/review.ts
frontend/src/stores/user.ts
frontend/src/types/assignment.ts
frontend/src/types/index.ts
frontend/src/utils/backendUrl.ts
frontend/src/utils/datetime.ts
frontend/src/views/annotation/AnnotationEditor.vue
frontend/src/views/annotation/AnnotationList.vue
frontend/src/views/annotation/AnnotationPage.vue
frontend/src/views/annotation/ImageAnnotationDemo.vue
frontend/src/views/corpus/CorpusManagement.vue
frontend/src/views/dataset/DatasetAssignment.vue
frontend/src/views/dataset/DatasetDetail.vue
frontend/src/views/dataset/DatasetManagement.vue
frontend/src/views/dataset/MyDatasets.vue
frontend/src/views/document/DataList.vue
frontend/src/views/document/DataStatistics.vue
frontend/src/views/document/DocumentImport.vue
frontend/src/views/Home.vue
frontend/src/views/label/LabelConfig.vue
frontend/src/views/label/LabelManagement.vue
frontend/src/views/Login.vue
frontend/src/views/multimodal/MultimodalExport.vue
frontend/src/views/NotFound.vue
frontend/src/views/review/ReviewDetail.vue
frontend/src/views/review/ReviewList.vue
frontend/src/views/user/UserManagement.vue
frontend/src/vite-env.d.ts
frontend/vite.config.ts
init_index.sh
update_index.sh
```

# Files

## File: 账户记录.txt
````
管理员：
admin/admin123 (ID: 1)

浏览员：
browser/browser123 (ID: 2)

标注员：
annotationer/annotationer123 (ID: 4)

注意：所有账号都在 backend/data/database/annotation.db 数据库中
````

## File: frontend/src/utils/backendUrl.ts
````typescript
function stripTrailingSlash(value: string): string
⋮----
function normalizePath(path: string): string
⋮----
function isAbsoluteUrl(value: string): boolean
⋮----
function getExplicitBackendOrigin(): string
⋮----
export function getApiBaseUrl(): string
⋮----
export function buildApiUrl(path: string): string
⋮----
export function buildBackendUrl(path: string): string
````

## File: .doc-checklist
````
# 文档创建检查清单

## 创建文档前必须检查：

□ 已阅读 DOC_QUICK_REF.md
□ 可以更新现有文档吗？
□ 这是临时文档吗？（如果是，命名为 TEMP_YYYYMMDD_*）
□ 会长期保留吗？（如果不是，不要创建）
□ 命名符合规范吗？
□ docs/ 目录文件数 < 15 吗？

## 如果有任何一项不确定，不要创建新文档！

## 完成任务后必须：

□ 删除所有 TEMP_*.md
□ 删除所有 *_COMPLETE.md
□ 删除所有 *_FIX.md
□ 整合临时文档到最终文档
□ 更新 PROJECT_STATUS.md

---

详细规则: DOCUMENTATION_RULES.md
快速参考: DOC_QUICK_REF.md
````

## File: .gitignore
````
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/
dist/
build/

# Node
*/node_modules/
dist/
.DS_Store

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Database
*.db
*.sqlite
*.sqlite3

# Data
data/uploads/*
data/images/*
data/exports/*
!data/uploads/.gitkeep
!data/images/.gitkeep
!data/exports/.gitkeep
*.png
*.jpg
*.jpeg
*.sql
参考项目代码/
# Logs
*.log
logs/

# Test
.pytest_cache/
.coverage
htmlcov/
.vitest/

# OS
Thumbs.db
.DS_Store
````

## File: backend/__init__.py
````python
"""
Backend package
"""
````

## File: backend/.gitignore
````
# 测试数据库
test_*.db
*.db-journal

# 测试产物
tests/test_artifacts/databases/*.db
tests/test_artifacts/reports/*.txt

# 日志文件
logs/
*.log

# Python缓存
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# 测试覆盖率
.coverage
.pytest_cache/
htmlcov/

# 虚拟环境
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 临时文件
*.tmp
*.bak
*~

# 数据文件
data/uploads/
data/exports/
*.jsonl

# 配置文件（包含敏感信息）
.env
.env.local
````

## File: backend/agents/__init__.py
````python
"""
Agent模块
"""
⋮----
__all__ = [
````

## File: backend/agents/entity_extraction.py
````python
"""
实体抽取Agent
使用LangChain v1.0 + Qwen-Max进行自动化实体标注
"""
⋮----
logger = logging.getLogger(__name__)
⋮----
# ============================================================================
# 输出模型定义
⋮----
class ExtractedEntity(BaseModel)
⋮----
"""提取的实体"""
id: int = Field(..., description="实体ID，从0开始")
token: str = Field(..., description="实体文本")
label: str = Field(..., description="实体类型标签")
start_offset: int = Field(..., description="起始偏移量")
end_offset: int = Field(..., description="结束偏移量")
confidence: Optional[float] = Field(None, description="置信度(0-1)，可选")
⋮----
class EntityExtractionOutput(BaseModel)
⋮----
"""实体抽取输出"""
text_id: str = Field(..., description="文本ID")
entities: List[ExtractedEntity] = Field(default_factory=list, description="提取的实体列表")
⋮----
# Prompt模板
⋮----
ENTITY_EXTRACTION_PROMPT = """你是一个专业的品质失效案例实体抽取专家。请从给定的文本中精准抽取实体。
⋮----
# Agent类
⋮----
class EntityExtractionAgent
⋮----
"""实体抽取Agent"""
⋮----
def __init__(self)
⋮----
"""初始化Agent"""
# 创建LLM
⋮----
# 创建偏移量修正服务
⋮----
"""
        提取实体
        
        Args:
            text_id: 文本ID
            text: 原始文本
            
        Returns:
            EntityExtractionOutput
        """
# 构建prompt（优先使用动态标签体系）
⋮----
prompt = DynamicPromptBuilder.build_entity_extraction_prompt(
⋮----
prompt = f"{ENTITY_EXTRACTION_PROMPT}\n文本ID: {text_id}\n文本内容: {text}"
⋮----
# 直接调用LLM获取原始文本输出（兼容DashScope/Qwen）
raw_response = self.llm.invoke(prompt)
raw_text = raw_response.content if hasattr(raw_response, 'content') else str(raw_response)
⋮----
# 从响应中提取JSON
json_text = self._extract_json(raw_text)
data = json.loads(json_text)
⋮----
entities = [
⋮----
# 验证和修正偏移量
corrected_entities = []
⋮----
@staticmethod
    def _extract_json(text: str) -> str
⋮----
"""从LLM响应中提取JSON块。"""
# 优先提取 ```json ... ``` 代码块
match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
⋮----
# 尝试直接找到第一个 { ... } 大块
match = re.search(r'(\{[\s\S]*\})', text)
⋮----
def get_correction_stats(self)
⋮----
"""获取偏移量修正统计"""
⋮----
def clear_correction_logs(self)
⋮----
"""清空修正日志"""
⋮----
# 全局单例
⋮----
_entity_agent: Optional[EntityExtractionAgent] = None
⋮----
def get_entity_agent() -> EntityExtractionAgent
⋮----
"""获取实体抽取Agent实例（单例模式）"""
⋮----
_entity_agent = EntityExtractionAgent()
````

## File: backend/agents/image_annotation.py
````python
"""
图片标注Agent（简化版）
使用多模态LLM对图片进行分类标注
"""
⋮----
class ImageAnnotationOutput(BaseModel)
⋮----
"""图片标注输出模型"""
image_path: str = Field(description="图片路径")
label: str = Field(description="图片分类标签")
confidence: Optional[float] = Field(None, description="置信度(0-1)")
description: Optional[str] = Field(None, description="图片描述")
⋮----
class ImageAnnotationAgent
⋮----
"""
    图片标注Agent（简化版）
    
    简化实现：
    1. 不调用真实的多模态LLM（Qwen-VL）
    2. 使用规则或默认标签进行分类
    3. 为后续扩展预留接口
    """
⋮----
def __init__(self)
⋮----
"""初始化Agent"""
# 预定义的图片实体类型
⋮----
"缺陷图片",  # 整图标注的默认标签
"缺陷区域"   # 区域标注的默认标签
⋮----
"""
        对图片进行分类标注（简化版）
        
        Args:
            image_path: 图片路径
            context_text: 上下文文本（可选）
            available_labels: 可用的标签列表（可选）
        
        Returns:
            ImageAnnotationOutput: 标注结果
        """
# 简化实现：使用默认标签
# 实际应用中，这里应该调用多模态LLM（如Qwen-VL）
⋮----
# 如果提供了可用标签列表，使用第一个
⋮----
label = available_labels[0]
⋮----
# 否则使用默认标签
label = self.default_labels[0]
⋮----
confidence=0.85,  # 简化版给一个固定置信度
⋮----
"""
        批量标注图片
        
        Args:
            image_paths: 图片路径列表
            context_text: 上下文文本（可选）
            available_labels: 可用的标签列表（可选）
        
        Returns:
            list[ImageAnnotationOutput]: 标注结果列表
        """
results = []
⋮----
result = self.annotate_image(
⋮----
# ============================================================================
# 多模态LLM集成（预留接口）
⋮----
class MultimodalLLMAgent
⋮----
"""
    多模态LLM Agent（完整版 - 预留接口）
    
    完整实现应该：
    1. 调用Qwen-VL或其他多模态LLM
    2. 支持图片理解和描述生成
    3. 支持基于上下文的图片分类
    4. 支持缺陷检测和定位
    """
⋮----
def __init__(self, model_name: str = "qwen-vl-max")
⋮----
"""
        初始化多模态LLM Agent
        
        Args:
            model_name: 模型名称
        """
⋮----
# TODO: 初始化模型连接
# from dashscope import MultiModalConversation
# self.client = MultiModalConversation()
⋮----
"""
        使用多模态LLM对图片进行分类
        
        Args:
            image_path: 图片路径
            context: 上下文文本
            candidate_labels: 候选标签列表
        
        Returns:
            Dict: 分类结果
        """
# TODO: 实现真实的多模态LLM调用
# 示例Prompt:
# """
# 请根据以下上下文和图片内容，从候选标签中选择最合适的标签对图片进行分类。
#
# 上下文: {context}
# 候选标签: {candidate_labels}
⋮----
# 请返回JSON格式:
# {
#     "label": "选择的标签",
#     "confidence": 0.95,
#     "reasoning": "选择理由"
# }
⋮----
"""
        检测图片中的缺陷
        
        Args:
            image_path: 图片路径
            defect_types: 缺陷类型列表
        
        Returns:
            list[Dict]: 检测到的缺陷列表，包含位置和类型
        """
# TODO: 实现缺陷检测
# 可以返回边界框坐标，用于区域标注
⋮----
# 使用示例
⋮----
def example_usage()
⋮----
"""使用示例"""
# 简化版Agent
agent = ImageAnnotationAgent()
⋮----
# 单张图片标注
result = agent.annotate_image(
⋮----
# 批量标注
results = agent.annotate_images_batch(
````

## File: backend/agents/label_definition_generator.py
````python
"""
标签定义生成Agent
使用LLM自动生成实体类型和关系类型的详细定义
"""
⋮----
# ============================================================================
# 输出模型定义
⋮----
class EntityTypeDefinition(BaseModel)
⋮----
"""实体类型定义"""
type_name: str = Field(..., description="实体类型英文名")
type_name_zh: str = Field(..., description="实体类型中文名")
definition: str = Field(..., description="标准定义（详细说明该实体类型的含义和范围）")
examples: List[str] = Field(..., description="示例列表（至少3个典型示例）")
disambiguation: str = Field(..., description="类别辨析（与相似类型的区别）")
⋮----
class RelationTypeDefinition(BaseModel)
⋮----
"""关系类型定义"""
type_name: str = Field(..., description="关系类型英文名")
type_name_zh: str = Field(..., description="关系类型中文名")
definition: str = Field(..., description="标准定义（详细说明该关系类型的含义）")
direction_rule: str = Field(..., description="方向规则（说明from和to的实体类型约束）")
examples: List[str] = Field(..., description="示例列表（格式：实体A --[关系]--> 实体B）")
disambiguation: str = Field(..., description="类别辨析（与相似关系的区别）")
⋮----
# Prompt模板
⋮----
ENTITY_TYPE_DEFINITION_PROMPT = """你是一个专业的品质失效案例领域专家。请为给定的实体类型生成详细的标准定义。
⋮----
RELATION_TYPE_DEFINITION_PROMPT = """你是一个专业的品质失效案例领域专家。请为给定的关系类型生成详细的标准定义。
⋮----
# Agent类
⋮----
class LabelDefinitionGenerator
⋮----
"""标签定义生成Agent"""
⋮----
def __init__(self)
⋮----
"""初始化Agent"""
⋮----
temperature=0.3,  # 稍高的温度以获得更丰富的内容
⋮----
"""
        生成实体类型定义
        
        Args:
            type_name: 实体类型英文名
            type_name_zh: 实体类型中文名
            description: 简短描述
            
        Returns:
            EntityTypeDefinition
        """
# 构建prompt
prompt = ENTITY_TYPE_DEFINITION_PROMPT.format(
⋮----
# 使用结构化输出
structured_llm = self.llm.with_structured_output(EntityTypeDefinition)
⋮----
result = structured_llm.invoke(prompt)
⋮----
# 返回基础定义
⋮----
"""
        生成关系类型定义
        
        Args:
            type_name: 关系类型英文名
            type_name_zh: 关系类型中文名
            description: 简短描述
            
        Returns:
            RelationTypeDefinition
        """
⋮----
prompt = RELATION_TYPE_DEFINITION_PROMPT.format(
⋮----
structured_llm = self.llm.with_structured_output(RelationTypeDefinition)
⋮----
# 全局单例
⋮----
_label_generator: Optional[LabelDefinitionGenerator] = None
⋮----
def get_label_generator() -> LabelDefinitionGenerator
⋮----
"""获取标签定义生成器实例（单例模式）"""
⋮----
_label_generator = LabelDefinitionGenerator()
````

## File: backend/agents/relation_extraction.py
````python
"""
关系抽取Agent
基于已提取的实体识别它们之间的关系
"""
⋮----
logger = logging.getLogger(__name__)
⋮----
# ============================================================================
# 输出模型定义
⋮----
class ExtractedRelation(BaseModel)
⋮----
"""提取的关系"""
id: int = Field(..., description="关系ID，从0开始")
from_id: int = Field(..., description="源实体ID")
to_id: int = Field(..., description="目标实体ID")
type: str = Field(..., description="关系类型")
⋮----
class RelationExtractionOutput(BaseModel)
⋮----
"""关系抽取输出"""
text_id: str = Field(..., description="文本ID")
relations: List[ExtractedRelation] = Field(default_factory=list, description="提取的关系列表")
⋮----
# Prompt模板
⋮----
RELATION_EXTRACTION_PROMPT = """你是一个专业的品质失效案例关系抽取专家。请基于给定的文本和已标注的实体，识别实体之间的关系。
⋮----
# Agent类
⋮----
class RelationExtractionAgent
⋮----
"""关系抽取Agent"""
⋮----
def __init__(self)
⋮----
"""初始化Agent"""
# 创建LLM
⋮----
"""
        提取关系
        
        Args:
            text_id: 文本ID
            text: 原始文本
            entities: 已提取的实体列表
            
        Returns:
            RelationExtractionOutput
        """
# 如果实体少于2个，无法建立关系
⋮----
# 构建prompt（优先使用动态标签体系）
⋮----
entities_for_prompt = [
prompt = DynamicPromptBuilder.build_relation_extraction_prompt(
⋮----
entities_str = "[\n"
⋮----
prompt = f"""{RELATION_EXTRACTION_PROMPT}
⋮----
# 直接调用LLM获取原始文本输出（兼容DashScope/Qwen）
structured_llm = self.llm
⋮----
# 调用LLM
raw_response = structured_llm.invoke(prompt)
raw_text = raw_response.content if hasattr(raw_response, 'content') else str(raw_response)
⋮----
# 从响应中提取JSON
json_text = self._extract_json(raw_text)
data = json.loads(json_text)
⋮----
relations = [
⋮----
# 验证实体ID有效性
valid_entity_ids = {entity.id for entity in entities}
validated_relations = []
⋮----
# 重新编号关系ID
⋮----
@staticmethod
    def _extract_json(text: str) -> str
⋮----
"""从LLM响应中提取JSON块。"""
match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
⋮----
match = re.search(r'(\{[\s\S]*\})', text)
⋮----
# 全局单例
⋮----
_relation_agent: Optional[RelationExtractionAgent] = None
⋮----
def get_relation_agent() -> RelationExtractionAgent
⋮----
"""获取关系抽取Agent实例（单例模式）"""
⋮----
_relation_agent = RelationExtractionAgent()
````

## File: backend/alembic.ini
````ini
# Alembic配置文件

[alembic]
script_location = alembic
prepend_sys_path = .
# Placeholder only. The active business database is configured via DATABASE_URL in .env.
sqlalchemy.url = driver://user:pass@localhost/dbname

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
````

## File: backend/api/__init__.py
````python
"""
API路由包
"""
⋮----
__all__ = ['corpus_router', 'dataset_router', 'labels_router', 'annotations_router', 'images_router', 'versions_router', 'review_router', 'users_router', 'auth_router']
````

## File: backend/api/annotations.py
````python
"""
标注任务API
提供批量自动标注、标注任务管理、实体和关系的CRUD操作
"""
⋮----
router = APIRouter(prefix="/api/v1/annotations", tags=["annotations"])
⋮----
"""后台执行批量标注（使用独立数据库会话，避免请求会话关闭后失效）"""
db = SessionLocal()
⋮----
service = BatchAnnotationService(db)
⋮----
# ============================================================================
# 跨数据集任务列表API
⋮----
"""
    获取跨数据集任务列表
    
    根据用户角色返回相应的任务：
    - 管理员：返回所有任务（可选按数据集筛选）
    - 标注员：返回分配给该用户的任务（基于 DatasetAssignment）
    - 浏览员：返回403错误（浏览员不使用此端点）
    
    Args:
        dataset_id: 数据集ID筛选（可选）
        status: 状态筛选（可选）
        page: 页码
        page_size: 每页数量
        sort_by: 排序字段
        sort_order: 排序方向
        db: 数据库会话
        current_user: 当前用户
    
    Returns:
        任务列表响应
    """
⋮----
user_id = current_user.get('user_id')
user_role = current_user.get('role')
⋮----
# 浏览员不能使用此端点
⋮----
# 创建任务查询服务
task_service = TaskQueryService(db)
⋮----
# 获取任务列表
⋮----
# 构建响应数据
items = []
⋮----
# 获取数据集信息
dataset = db.query(Dataset).filter(Dataset.id == task.dataset_id).first()
dataset_name = dataset.name if dataset else "未知数据集"
⋮----
# 获取语料信息
corpus = db.query(Corpus).filter(Corpus.id == task.corpus_id).first()
corpus_text = corpus.text[:100] if corpus and corpus.text else ""
⋮----
# 统计实体和关系数量
entity_count = db.query(TextEntity).filter(
⋮----
relation_count = db.query(Relation).filter(
⋮----
# 批量标注API
⋮----
"""
    触发批量自动标注
    
    创建批量任务并在后台异步执行
    
    权限要求：
    - 管理员：可以批量标注任何数据集的任务
    - 标注员：只能批量标注分配给自己的任务
    - 浏览员：无权限
    
    参数：
    - dataset_id: 数据集ID（必填）
    - task_ids: 指定要标注的任务ID列表（可选）
      - 如果提供，只标注指定的任务
      - 如果不提供，标注所有符合权限的pending任务
    """
user_id = current_user['user_id']
user_role = current_user['role']
⋮----
# 1. 检查角色权限
⋮----
# 2. 检查数据集访问权限（标注员）
⋮----
# 查询数据集
dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
⋮----
# 检查是否有分配
⋮----
assignment = db.query(DatasetAssignment).filter(
⋮----
# 创建批量任务（传递用户信息和任务ID列表）
batch_job = service.create_batch_job(
⋮----
# 在后台执行批量标注（独立会话，避免阻塞主请求和会话生命周期问题）
⋮----
"""获取批量任务状态和进度"""
⋮----
stats = service.get_batch_job_statistics(job_id)
⋮----
"""取消批量任务"""
⋮----
success = service.cancel_batch_job(job_id)
⋮----
# 标注任务管理API
⋮----
"""
    获取标注任务详情
    
    权限规则：
    - 管理员：允许访问所有任务
    - 标注员：只允许访问分配的任务
    - 浏览员：只允许访问已完成任务
    """
⋮----
# 查询任务
task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
⋮----
# 权限检查
⋮----
has_permission = task_service.check_task_permission(
⋮----
# 查询语料
⋮----
# 查询实体
entities = db.query(TextEntity)\
⋮----
# 查询关系
relations = db.query(Relation)\
⋮----
"""获取任务运行时使用的实体/关系Prompt文本（用于版本核对）"""
⋮----
entity_types = LabelConfigCache.get_entity_types(db)
relation_types = LabelConfigCache.get_relation_types(db)
⋮----
entity_prompt = DynamicPromptBuilder.build_entity_extraction_prompt(
⋮----
existing_entities = db.query(TextEntity)\
⋮----
entities_for_relation = [
⋮----
relation_prompt = DynamicPromptBuilder.build_relation_extraction_prompt(
⋮----
"""
    更新标注任务
    
    权限规则：
    - 管理员：允许编辑所有任务
    - 标注员：只允许编辑分配的任务
    - 浏览员：禁止编辑（返回403）
    """
⋮----
# 浏览员禁止编辑
⋮----
# 标注员和管理员需要检查权限
⋮----
# 更新状态
status = request_body.get('status')
⋮----
# 实体管理API
⋮----
"""添加文本实体"""
⋮----
# 从请求体中提取参数
token = request_body.get('token')
label = request_body.get('label')
start_offset = request_body.get('start_offset')
end_offset = request_body.get('end_offset')
⋮----
# 创建实体
entity = TextEntity(
⋮----
# 更新任务为手动标注
⋮----
"""更新文本实体"""
⋮----
entity = db.query(TextEntity)\
⋮----
# 更新字段
⋮----
"""删除文本实体"""
⋮----
# 删除关联的关系
⋮----
# 删除实体
⋮----
# 关系管理API
⋮----
"""添加关系"""
⋮----
from_entity_id = request_body.get('from_entity_id')
to_entity_id = request_body.get('to_entity_id')
relation_type = request_body.get('relation_type', 'relates_to')
⋮----
# 验证实体存在
from_entity = db.query(TextEntity)\
⋮----
to_entity = db.query(TextEntity)\
⋮----
# 创建关系
relation = Relation(
⋮----
"""更新关系"""
⋮----
relation_type = request_body.get('relation_type')
⋮----
relation = db.query(Relation)\
⋮----
"""删除关系"""
⋮----
# 删除关系
````

## File: backend/api/config_api.py
````python
"""处理器配置API - 提供处理器列表和前端配置"""
⋮----
router = APIRouter(prefix="/api/v1/config", tags=["config"])
⋮----
@router.get("/processors")
async def get_processors(current_user: dict = Depends(get_current_user))
⋮----
"""获取所有可用的处理器列表"""
⋮----
"""获取指定处理器的图谱可视化配置"""
⋮----
processor = get_processor(name)
⋮----
config = processor.get_graph_config()
⋮----
"""获取指定处理器的字段映射配置"""
````

## File: backend/api/corpus_by_row.py
````python
"""
获取同行语料API - 用于标注任务详情中显示上下文
"""
⋮----
router = APIRouter(prefix="/api/v1", tags=["corpus"])
⋮----
"""
    获取指定Excel行的所有语料记录
    用于在标注任务详情中显示上下文（同行的其他字段）
    
    Args:
        source_file: 源文件名
        source_row: 行号
        db: 数据库会话
    
    Returns:
        该行的所有语料记录列表
    """
# 查询该行的所有语料
corpus_list = db.query(Corpus).filter(
⋮----
# 构建响应
result = []
⋮----
# 获取关联的图片
images = db.query(Image).filter(Image.corpus_id == corpus.id).all()
image_infos = [
````

## File: backend/api/corpus_grouped.py
````python
"""
语料分组API - 按Excel行分组显示
"""
⋮----
# 定义分组语料模型
class GroupedCorpusItem(BaseModel)
⋮----
"""单个语料项"""
text_id: str
text: str
text_type: str
source_field: str
has_images: bool
images: List[ImageInfo] = []
⋮----
class GroupedCorpusRow(BaseModel)
⋮----
"""按行分组的语料"""
source_file: str
source_row: int
items: List[GroupedCorpusItem]
total_images: int
created_at: str
⋮----
class GroupedCorpusListResponse(BaseModel)
⋮----
"""分组语料列表响应"""
total: int
items: List[GroupedCorpusRow]
⋮----
router = APIRouter(prefix="/api/v1", tags=["corpus"])
⋮----
"""
    获取按Excel行分组的语料列表
    
    - 同一行的多个字段内容会合并显示
    - 支持分页（按行分页）
    - 支持筛选
    """
# 构建查询
query = db.query(Corpus)
⋮----
# 应用筛选条件
⋮----
query = query.filter(Corpus.source_file.like(f"%{source_file}%"))
⋮----
query = query.filter(Corpus.source_field == source_field)
⋮----
query = query.filter(Corpus.has_images == has_images)
⋮----
# 获取所有语料（先不分页，因为需要按行分组）
all_corpus = query.order_by(
⋮----
# 按 (source_file, source_row) 分组
grouped_data = defaultdict(list)
⋮----
key = (corpus.source_file, corpus.source_row)
⋮----
# 转换为列表并排序
grouped_rows = []
⋮----
# 获取该行的所有图片
total_images = 0
items = []
⋮----
# 获取关联的图片
images = db.query(Image).filter(Image.corpus_id == corpus.id).all()
image_infos = [
⋮----
# 按文件名和行号排序
⋮----
# 分页
total = len(grouped_rows)
offset = (page - 1) * page_size
paginated_rows = grouped_rows[offset:offset + page_size]
````

## File: backend/api/corpus.py
````python
"""
语料管理API路由
提供语料上传、查询、删除等功能
"""
⋮----
router = APIRouter(prefix="/api/v1/corpus", tags=["corpus"])
⋮----
def _delete_corpus_records(db: Session, corpus_list: list) -> SuccessResponse
⋮----
"""
    通用删除逻辑：阻止删除已被数据集引用的语料。
    """
⋮----
corpus_ids = [c.id for c in corpus_list]
text_id_map = {c.id: c.text_id for c in corpus_list}
⋮----
used_ids = {
deletable_ids = [cid for cid in corpus_ids if cid not in used_ids]
⋮----
# 删除物理图片文件
image_paths = [
⋮----
"""
    上传Excel文件并处理
    
    - 验证文件格式
    - 提取WPS内嵌图片
    - 解析表格数据
    - 生成语料记录
    """
# 验证文件类型
⋮----
# 保存上传的文件
upload_id = uuid.uuid4().hex[:16]
file_path = settings.UPLOAD_DIR / f"{upload_id}_{file.filename}"
⋮----
# 创建Excel处理服务
excel_service = ExcelProcessingService(db)
⋮----
# 验证Excel文件
validation_result = excel_service.validate_excel_file(str(file_path))
⋮----
# 处理Excel文件
result = excel_service.process_excel_file(
⋮----
# 统计各字段的句子分布
field_distribution = {}
⋮----
corpus = db.query(Corpus).filter(Corpus.text_id == corpus_id).first()
⋮----
# 清理上传的临时文件
⋮----
page_size: int = Query(20, ge=1, le=1000, description="每页数量"),  # 提高到1000
⋮----
"""
    获取语料列表
    
    - 支持分页
    - 支持按文件名筛选
    - 支持按字段分类筛选
    - 支持按是否包含图片筛选
    """
# 构建查询
query = db.query(Corpus)
⋮----
# 应用筛选条件
⋮----
query = query.filter(Corpus.source_file.like(f"%{source_file}%"))
⋮----
query = query.filter(Corpus.source_field == source_field)
⋮----
query = query.filter(Corpus.has_images == has_images)
⋮----
# 获取总数
total = query.count()
⋮----
# 分页查询
offset = (page - 1) * page_size
corpus_list = query.order_by(Corpus.created_at.desc()).offset(offset).limit(page_size).all()
⋮----
# 构建响应
items = []
⋮----
# 获取关联的图片
images = db.query(Image).filter(Image.corpus_id == corpus.id).all()
image_infos = [
⋮----
id=corpus.id,  # 添加数据库ID
⋮----
"""
    获取语料详情
    
    - 返回完整的语料信息
    - 包含关联的图片列表
    """
# 查询语料
⋮----
# 阻止删除已被数据集引用的语料
used = db.query(DatasetCorpus).filter(DatasetCorpus.corpus_id == corpus.id).first()
⋮----
"""
    Delete all corpus records under a file. Records referenced by datasets are skipped and reported.
    """
corpus_list = db.query(Corpus).filter(Corpus.source_file == source_file).all()
⋮----
"""
    Delete all corpus records in a specific file row. Records referenced by datasets are skipped and reported.
    """
corpus_list = db.query(Corpus).filter(
⋮----
"""
    删除语料
    
    - 删除语料记录
    - 级联删除关联的图片记录
    - 注意：不会删除物理图片文件
    """
⋮----
image_paths = [img.file_path for img in db.query(Image).filter(Image.corpus_id == corpus.id).all()]
⋮----
# 删除语料（级联删除会自动删除关联的图片记录）
⋮----
"""
    获取语料关联的图片列表
    
    - 返回该语料的所有关联图片
    """
````

## File: backend/api/data_query.py
````python
"""数据查询 API - KF/QMS/品质案例列表与统计。"""
⋮----
router = APIRouter(prefix="/api/v1/data", tags=["data"])
⋮----
"""获取 KF/QMS/品质失效案例数据列表（支持分页）。"""
⋮----
engine = QueryEngine(processor_name=processor_name)
⋮----
resolved_page_size = page_size or limit
resolved_page = page or (offset // resolved_page_size + 1)
resolved_offset = (resolved_page - 1) * resolved_page_size
⋮----
resolved_page_size = limit
resolved_offset = offset
resolved_page = (resolved_offset // resolved_page_size) + 1
⋮----
data = engine.get_data_list(db, processor_name, resolved_page_size, resolved_offset)
total_count = engine.get_data_total_count(db, processor_name)
⋮----
"""获取统计分析数据。"""
⋮----
stats = engine.get_statistics(db)
````

## File: backend/api/dataset_assignment.py
````python
"""
数据集分配API
提供数据集级别的任务分配功能
"""
⋮----
router = APIRouter(prefix="/api/v1/datasets", tags=["dataset-assignment"])
⋮----
# ============================================================================
# 辅助函数
⋮----
def get_assignment_service(db: Session = Depends(get_db)) -> DatasetAssignmentService
⋮----
"""获取数据集分配服务实例"""
⋮----
def format_task_range(start: Optional[int], end: Optional[int]) -> str
⋮----
"""格式化任务范围"""
⋮----
def get_assignment_info(assignment, db: Session)
⋮----
"""构建分配信息"""
# 获取用户信息
user = db.query(User).filter(User.id == assignment.user_id).first()
⋮----
# 获取数据集信息
dataset = db.query(Dataset).filter(Dataset.id == assignment.dataset_id).first()
⋮----
# 统计任务进度
service = DatasetAssignmentService(db)
tasks = service._get_tasks_in_range(
⋮----
completed_count = sum(1 for t in tasks if t.status == 'completed')
in_review_count = sum(1 for t in tasks if t.status == 'in_review')
⋮----
# 获取转移目标用户信息
transferred_to_username = None
⋮----
transferred_user = db.query(User).filter(User.id == assignment.transferred_to).first()
⋮----
transferred_to_username = transferred_user.username
⋮----
# API端点
⋮----
"""
    分配数据集（整体或范围）
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        request: 分配请求
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        AssignmentResponse: 分配响应
    """
⋮----
# 获取数据集
dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
⋮----
# 根据模式执行分配
⋮----
assignment = service.assign_full(
⋮----
assignment = service.assign_range(
⋮----
# 构建响应
assignment_info = get_assignment_info(assignment, db)
⋮----
"""
    自动平均分配数据集
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        request: 自动分配请求
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        AutoAssignmentResponse: 自动分配响应
    """
⋮----
# 执行自动分配
assignments = service.assign_auto(
⋮----
assignment_list = []
total_tasks = 0
⋮----
task_count = service._count_tasks_in_range(
⋮----
"""
    取消分配（带条件检查）
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        user_id: 用户ID
        role: 角色
        force: 强制取消
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        SuccessResponse: 成功响应
    
    Raises:
        HTTPException: 如果不能取消（有已完成任务）
    """
⋮----
# 尝试取消分配
⋮----
error_msg = str(e)
⋮----
# 检查是否是因为有已完成任务而无法取消
⋮----
# 解析错误信息和统计数据
parts = error_msg.split("|")
reason = parts[0]
⋮----
# 返回特殊错误，提示使用转移功能
⋮----
"""
    批量分配数据集
    
    权限：仅管理员
    
    用于两阶段分配：前端规划完成后，批量提交所有分配
    
    Args:
        dataset_id: 数据集ID
        request: 批量分配请求
        force: 强制分配（跳过已完成任务检查）
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        SuccessResponse: 成功响应
    """
⋮----
# 清空现有分配（使用删除而不是更新，避免唯一约束冲突）
⋮----
query = db.query(DatasetAssignment)\
⋮----
query = query.filter(DatasetAssignment.role == request.role_filter.value)
⋮----
existing_assignments = query.all()
⋮----
# 检查是否有已完成的任务（除非强制）
⋮----
assignments_with_progress = []
⋮----
# 构建详细错误信息
details = []
for item in assignments_with_progress[:3]:  # 最多显示3个
⋮----
error_msg = (
⋮----
# 删除分配
⋮----
# 批量创建分配
created_count = 0
⋮----
# 验证用户存在
user = db.query(User).filter(User.id == item.user_id).first()
⋮----
# 创建分配
assignment = DatasetAssignment(
⋮----
"""
    批量清空数据集的所有分配
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        role: 角色筛选（可选）
        force: 强制清空
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        SuccessResponse: 成功响应，包含清空数量
    """
⋮----
# 获取要清空的分配
⋮----
query = query.filter(DatasetAssignment.role == role)
⋮----
count = len(existing_assignments)
⋮----
# 直接删除而不是更新is_active（避免唯一约束冲突）
⋮----
"""
    转移分配
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        request: 转移请求
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        TransferAssignmentResponse: 转移响应
    """
⋮----
# 执行转移
result = service.transfer_assignment(
⋮----
"""
    获取数据集分配情况
    
    权限：管理员或已分配用户
    
    Args:
        dataset_id: 数据集ID
        include_inactive: 是否包含不活跃的分配
        db: 数据库会话
        current_user: 当前用户
        service: 分配服务
    
    Returns:
        AssignmentListResponse: 分配列表响应
    """
⋮----
# 权限检查：管理员或已分配用户
user_id = current_user['user_id']
user_role = current_user['role']
⋮----
# 检查是否有分配
has_assignment = service.check_permission(user_id, dataset.id, 'annotator') or \
⋮----
# 获取分配列表
assignments = service.get_dataset_assignments(dataset.id, include_inactive)
⋮----
# 统计信息
total_tasks = db.query(Dataset).filter(Dataset.id == dataset.id).first()
task_count = len(total_tasks.annotation_tasks) if total_tasks else 0
⋮----
assigned_tasks = sum(
unassigned_count = task_count - assigned_tasks
⋮----
annotator_count = len([a for a in assignment_list if a['role'] == 'annotator' and a['is_active']])
reviewer_count = len([a for a in assignment_list if a['role'] == 'reviewer' and a['is_active']])
⋮----
# 注意：这个路由必须在 /{dataset_id} 之前注册！
⋮----
"""
    获取我的数据集
    
    权限：标注员、复核员
    
    Args:
        role: 角色筛选
        page: 页码
        page_size: 每页数量
        db: 数据库会话
        current_user: 当前用户
        service: 分配服务
    
    Returns:
        MyDatasetsResponse: 我的数据集列表响应
    """
⋮----
# 管理员和浏览员不使用此接口
⋮----
# 获取用户的数据集
datasets = service.get_user_datasets(user_id, role)
⋮----
items = []
⋮----
# 获取用户在该数据集的分配信息
⋮----
assignment = query.first()
⋮----
# 优化：使用SQL COUNT查询而不是加载所有任务
task_query = db.query(AnnotationTask)\
⋮----
# 如果指定了范围，进行过滤
⋮----
# 获取所有任务ID，然后按索引切片
all_task_ids = [t.id for t in task_query.order_by(AnnotationTask.id).all()]
# 索引从1开始，所以需要减1
task_ids_in_range = all_task_ids[assignment.task_start_index-1:assignment.task_end_index]
⋮----
# 统计任务数和完成数
my_task_count = len(task_ids_in_range)
my_completed_count = db.query(AnnotationTask)\
⋮----
# 全部任务
my_task_count = task_query.count()
my_completed_count = task_query.filter(AnnotationTask.status == 'completed').count()
⋮----
# 分页
total = len(items)
start = (page - 1) * page_size
end = start + page_size
paginated_items = items[start:end]
````

## File: backend/api/dataset.py
````python
"""
数据集管理API
提供数据集的CRUD操作和导出功能
"""
⋮----
router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])
⋮----
class AddTasksRequest(BaseModel)
⋮----
"""向数据集添加语料的请求体"""
corpus_ids: List[int]
⋮----
"""
    创建数据集
    
    - 创建数据集记录
    - 关联语料
    - 自动创建标注任务
    - 绑定标签体系版本
    """
⋮----
service = DatasetService(db)
dataset = service.create_dataset(
⋮----
"""
    获取数据集列表
    
    权限：
    - 管理员：查看所有数据集
    - 标注员/复核员：只能查看分配给自己的数据集（应使用 /datasets/my 接口）
    - 浏览员：查看所有数据集（只读）
    
    - 支持分页
    - 支持按名称筛选
    - 支持按创建人筛选
    """
⋮----
user_role = current_user['role']
user_id = current_user['user_id']
⋮----
# 标注员和复核员应该使用 /datasets/my 接口
⋮----
# 管理员和浏览员可以查看所有数据集
⋮----
# 构建响应数据
items = []
⋮----
# 内联计算统计信息（复用已加载的 annotation_tasks 关系）
status_counts = Counter(task.status for task in dataset.annotation_tasks)
total_tasks = len(dataset.annotation_tasks)
statistics = {
⋮----
"""
    获取数据集详情
    
    - 返回数据集基本信息
    - 返回关联的语料列表
    - 返回标注任务列表
    """
⋮----
dataset = service.get_dataset(dataset_id)
⋮----
# 构建语料列表
corpus_list = []
⋮----
corpus = assoc.corpus
⋮----
# 构建任务列表
task_list = []
⋮----
# 内联计算统计信息
⋮----
"""
    更新数据集
    
    - 更新数据集名称和描述
    """
⋮----
# 更新字段
⋮----
"""
    删除数据集
    
    - 级联删除所有关联数据
    - 删除标注任务
    - 删除实体和关系
    """
⋮----
success = service.delete_dataset(dataset_id)
⋮----
"""
    获取数据集统计信息
    
    - 任务数量统计
    - 完成率统计
    - 实体和关系数量统计
    """
⋮----
stats = service.get_dataset_statistics(dataset_id)
⋮----
"""
    获取数据集的标注任务列表
    
    权限：
    - 管理员：返回该数据集的所有任务
    - 标注员：返回该数据集中分配给该标注员的任务
    - 浏览员：返回该数据集中状态为已完成的任务
    
    - 支持分页
    - 支持按状态筛选
    - 返回任务详情包括语料文本、实体数、关系数等
    """
⋮----
# 验证数据集是否存在
dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
⋮----
# 获取当前用户信息
⋮----
# 使用 TaskQueryService 进行权限过滤
task_query_service = TaskQueryService(db)
⋮----
# 获取用户可访问的任务列表（传入数据集ID进行筛选）
⋮----
# 获取语料文本
corpus = db.query(Corpus).filter(Corpus.id == task.corpus_id).first()
corpus_text = corpus.text if corpus else ""
⋮----
"""
    向已有数据集添加语料（自动创建标注任务，重复添加自动跳过）
    
    - 检测重复语料（已在数据集中的跳过）
    - 自动为新增语料创建 pending 状态的标注任务
    """
⋮----
result = service.add_tasks_to_dataset(dataset_id, request.corpus_ids)
⋮----
"""
    从数据集中删除一个标注任务及其关联语料绑定和全部标注数据
    仅管理员可操作
    """
# 权限检查：仅管理员可删除任务
⋮----
success = service.remove_task(dataset_id, task_id)
⋮----
"""
    导出数据集
    
    - 导出为JSONL格式
    - 支持按状态筛选
    - 返回导出文件路径
    """
⋮----
# 默认只导出已完成和已复核的任务
status_filter = None
⋮----
status_filter = request.status_filter
⋮----
status_filter = ["completed", "reviewed"]
export_path = service.export_dataset(
⋮----
# 确保路径存在并返回文件以触发浏览器下载（带 Content-Disposition: attachment）
⋮----
file_path = Path(export_path)
⋮----
# 有时候 service 返回相对路径，从项目根尝试解析
file_path = Path(os.getcwd()) / export_path
````

## File: backend/api/document_import.py
````python
"""
统一文档导入API
提供Excel上传、处理、导入图谱的统一入口
"""
⋮----
router = APIRouter(prefix="/api/v1/documents", tags=["documents"])
logger = logging.getLogger(__name__)
⋮----
def _count_imported_records_by_source(db: Session, processor_name: str, data_source: str) -> int
⋮----
"""Count imported records for one processor/data_source pair."""
⋮----
def _build_graph_importer(processor_name: str)
⋮----
"""Get parser and graph builder for graph-style processors."""
parser = DataParser(processor_name=processor_name)
⋮----
"""Import processed JSON records into the workflow database."""
json_dir = settings.PROCESSED_DIR / processor_name / data_source
⋮----
json_files = list(json_dir.glob("*.json"))
⋮----
total_records = 0
inserted_records = 0
skipped_records = 0
failed_records = 0
error_samples = []
⋮----
records = parser.parse_json_file(str(json_file))
⋮----
entities = parser.extract_entities(record, data_source=data_source)
record_id = (
⋮----
success = graph_builder.build_graph(db, entities, skip_if_exists=True)
⋮----
database_records = _count_imported_records_by_source(db, processor_name, data_source)
⋮----
"""
    上传Excel文件并处理

    - 将上传文件保存到 data/uploads/ 临时目录
    - 实例化 DocumentProcessor 解析Excel
    - 如果是重复文件，返回提示信息
    - 如果 processor_name == 'failure_case'，额外调用 ExcelProcessingService
    """
⋮----
# 临时文件按处理器隔离到子目录，避免不同处理器同名文件冲突
upload_subdir = settings.UPLOAD_DIR / processor_name
⋮----
file_path = upload_subdir / file.filename
⋮----
doc_processor = DocumentProcessor(processor_name=processor_name)
result = doc_processor.process_excel(str(file_path), file.filename)
⋮----
corpus_count = 0
auto_import_result = None
⋮----
excel_service = ExcelProcessingService(db)
corpus_result = excel_service.process_excel_file(str(file_path), file.filename)
corpus_count = corpus_result.get('corpus_count', 0)
⋮----
auto_import_result = _import_processed_records(db, processor_name, result['data_source'])
⋮----
response = {
⋮----
"""
    将处理好的JSON文件导入图谱数据库

    - 找到 data/processed/{processor_name}/{data_source}/ 目录下的所有JSON文件
    - 使用 DataParser 解析每条记录
    - 使用 GraphBuilder 或 QMSGraphBuilder 写入数据库
    """
⋮----
import_result = _import_processed_records(db, processor_name, data_source)
⋮----
"""
    上传图片ZIP文件并解压到 data/images/{data_source}/ 目录。
    仅限 QMS 处理器使用：KF 图片内嵌于 Excel，无需外部上传；
    品质案例处理器使用独立图片目录，不走此接口。
    """
⋮----
# 图片解压到 parser 实际查找的目录：data/processed/qms/{data_source}/imgs/
images_dir = settings.PROCESSED_DIR / 'qms' / data_source / 'imgs'
⋮----
zip_path = images_dir / f"{data_source}_upload.zip"
⋮----
extracted_count = len(list(images_dir.glob("**/*.*")))
⋮----
"""
    查询指定数据源的已上传图片数量
    """
⋮----
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
count = sum(
⋮----
"""
    获取已处理文件列表
    """
⋮----
files = doc_processor.get_processed_files()
⋮----
"""
    彻底删除指定数据源的所有数据：
    - 从 file_hashes.json 中移除记录
    - 删除 data/processed/{processor_name}/{data_source}/ 目录
    - 从数据库中删除该数据源的所有相关记录
    """
⋮----
# 从哈希记录中找到原始文件名（failure_case 需要）并移除条目
original_filename = None
removed = False
⋮----
original_filename = record.get('original_filename', '')
⋮----
removed = True
⋮----
# 删除处理结果目录
output_dir = settings.PROCESSED_DIR / processor_name / data_source
⋮----
# 删除数据库记录
db_deleted = 0
⋮----
result = db.query(QuickResponseEvent).filter(
db_deleted = result
⋮----
result = db.query(QMSDefectOrder).filter(
⋮----
# 与语料管理对齐：跳过已被数据集引用的语料，只删除可删除的
corpus_records = db.query(Corpus).filter(
⋮----
corpus_ids = [c.id for c in corpus_records]
used_ids = {
deletable = [c for c in corpus_records if c.id not in used_ids]
skipped = len(used_ids)
⋮----
# 先删物理图片文件
⋮----
deletable_ids = [c.id for c in deletable]
image_paths = [
⋮----
db_deleted = len(deletable)
````

## File: backend/api/graph_api.py
````python
"""图谱查询API - 知识图谱数据查询接口（暂不注册）"""
⋮----
router = APIRouter(prefix="/api/v1/graph", tags=["graph"])
⋮----
"""获取知识图谱的节点和边数据"""
⋮----
filters = {}
⋮----
engine = QueryEngine(processor_name=processor)
graph_data = engine.get_graph_data(db, filters if filters else None, limit)
⋮----
"""获取单个快反事件的详细信息"""
⋮----
engine = QueryEngine(processor_name='kf')
event = engine.get_event_detail(db, event_id)
⋮----
"""获取统计数据"""
⋮----
stats = engine.get_statistics(db)
````

## File: backend/api/images.py
````python
"""
图片标注API
提供图片实体的CRUD操作,支持整图标注和区域标注(边界框)
"""
⋮----
router = APIRouter(prefix="/api/v1/images", tags=["images"])
⋮----
# ============================================================================
# 图片实体管理API
⋮----
"""
    添加图片实体
    
    支持两种标注模式:
    1. 整图标注: 不提供边界框参数
    2. 区域标注: 提供完整的边界框参数(x, y, width, height)
    """
⋮----
# 查询图片
image = db.query(Image).filter(Image.image_id == image_id).first()
⋮----
# 查询任务
task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
⋮----
# 验证边界框参数
has_bbox = any([bbox_x is not None, bbox_y is not None,
⋮----
# 如果提供了任何边界框参数,则必须全部提供
⋮----
# 验证边界框在图片范围内
⋮----
# 生成实体ID
entity_id_str = f"img-entity-{uuid.uuid4().hex[:8]}"
⋮----
# 创建图片实体
image_entity = ImageEntity(
⋮----
# 更新任务为手动标注
⋮----
"""
    获取图片实体列表
    
    可选参数:
    - task_id: 筛选特定任务的图片实体
    """
⋮----
# 构建查询
query = db.query(ImageEntity).filter(ImageEntity.image_id == image.id)
⋮----
# 如果指定了任务ID,则筛选
⋮----
query = query.filter(ImageEntity.task_id == task.id)
⋮----
# 执行查询
entities = query.all()
⋮----
# 格式化返回数据
result = []
⋮----
has_bbox = entity.bbox_x is not None
⋮----
"""
    更新图片实体
    
    注意:
    - 如果要更新边界框,必须提供完整的边界框参数
    - 可以通过将所有边界框参数设为null来转换为整图标注
    """
⋮----
# 查询实体
entity = db.query(ImageEntity)\
⋮----
# 更新标签
⋮----
# 更新置信度
⋮----
# 更新边界框
bbox_params = [bbox_x, bbox_y, bbox_width, bbox_height]
bbox_provided = [p is not None for p in bbox_params]
⋮----
task = entity.task
⋮----
"""
    删除图片实体
    """
⋮----
# 删除实体
````

## File: backend/api/labels.py
````python
"""
标签管理API
提供实体类型、关系类型、标签定义生成、审核、导入导出、版本管理等功能
"""
⋮----
router = APIRouter(prefix="/api/v1/labels", tags=["labels"])
⋮----
# ============================================================================
# 实体类型管理API
⋮----
"""获取实体类型列表"""
⋮----
service = LabelManagementService(db)
entity_types = service.list_entity_types(
⋮----
"""创建实体类型"""
⋮----
entity_type = service.create_entity_type(
⋮----
"""更新实体类型"""
⋮----
# 构建更新字段
update_data = {}
⋮----
entity_type = service.update_entity_type(entity_type_id, **update_data)
⋮----
"""删除实体类型(软删除)"""
⋮----
success = service.delete_entity_type(entity_type_id)
⋮----
"""生成实体类型定义(调用LLM)"""
⋮----
entity_type = service.get_entity_type(entity_type_id)
⋮----
# 调用LLM生成定义
generator = LabelDefinitionGenerator()
result = generator.generate_entity_definition(
⋮----
# 更新实体类型
entity_type = service.update_entity_type(
⋮----
"""审核实体类型定义"""
⋮----
entity_type = service.review_entity_type(
⋮----
# 关系类型管理API
⋮----
"""获取关系类型列表"""
⋮----
relation_types = service.list_relation_types(
⋮----
"""创建关系类型"""
⋮----
relation_type = service.create_relation_type(
⋮----
"""更新关系类型"""
⋮----
relation_type = service.update_relation_type(relation_type_id, **update_data)
⋮----
"""删除关系类型(软删除)"""
⋮----
success = service.delete_relation_type(relation_type_id)
⋮----
"""生成关系类型定义(调用LLM)"""
⋮----
relation_type = service.get_relation_type(relation_type_id)
⋮----
result = generator.generate_relation_definition(
⋮----
# 更新关系类型
relation_type = service.update_relation_type(
⋮----
"""审核关系类型定义"""
⋮----
relation_type = service.review_relation_type(
⋮----
# 导入导出API
⋮----
"""导入标签配置"""
⋮----
stats = service.import_label_schema(schema_data, merge=merge)
⋮----
"""导出标签配置"""
⋮----
schema_data = service.export_label_schema()
⋮----
"""预览Agent Prompt"""
⋮----
# 获取标签配置
entity_types = LabelConfigCache.get_entity_types(db)
relation_types = LabelConfigCache.get_relation_types(db)
⋮----
# 构建Prompt预览
preview = DynamicPromptBuilder.build_prompt_preview(entity_types, relation_types)
⋮----
prompt_text = f"""你是一个专业的品质失效案例实体抽取专家。
⋮----
prompt_text = f"""你是一个专业的品质失效案例关系抽取专家。
⋮----
# 版本管理API
⋮----
"""获取版本列表"""
⋮----
versions = service.list_versions()
⋮----
# 统计每个版本使用的数据集数量，并解析schema_data获取实体和关系类型
⋮----
version_data = []
⋮----
datasets_count = db.query(func.count(Dataset.id))\
⋮----
# 解析schema_data获取实体和关系类型
schema_data = json.loads(version.schema_data)
⋮----
"""创建版本快照"""
⋮----
version = service.create_version_snapshot(
⋮----
# 解析schema_data获取统计信息
⋮----
"""获取版本详情"""
⋮----
version = service.get_version(version_id)
⋮----
# 解析schema_data
⋮----
# 获取使用该版本的数据集列表
⋮----
datasets = db.query(Dataset)\
⋮----
"""激活版本"""
⋮----
version = service.activate_version(version_id)
⋮----
"""比较版本差异"""
⋮----
# 获取两个版本
from_ver = service.get_version(from_version)
to_ver = service.get_version(to_version)
⋮----
from_schema = json.loads(from_ver.schema_data)
to_schema = json.loads(to_ver.schema_data)
⋮----
# 比较实体类型
from_entities = {et['type_name']: et for et in from_schema['entity_types']}
to_entities = {et['type_name']: et for et in to_schema['entity_types']}
⋮----
entity_changes = {
⋮----
# 检查修改的实体类型
⋮----
changes = []
⋮----
# 比较关系类型(类似逻辑)
from_relations = {rt['type_name']: rt for rt in from_schema['relation_types']}
to_relations = {rt['type_name']: rt for rt in to_schema['relation_types']}
⋮----
relation_changes = {
````

## File: backend/api/review.py
````python
"""
复核API
提供复核任务的REST API接口
"""
⋮----
from api.users import get_current_user  # 添加导入
⋮----
router = APIRouter(prefix="/api/v1/review", tags=["review"])
⋮----
"""
    提交标注任务进行复核
    
    Args:
        task_id: 标注任务ID
        request_body: 请求体，可包含reviewer_id
    
    Returns:
        ReviewTaskResponse: 创建的复核任务
    """
reviewer_id = request_body.get('reviewer_id') if request_body else None
⋮----
# 查询标注任务
task = db.query(AnnotationTask).filter(
⋮----
# 创建复核服务
service = ReviewService(db)
⋮----
review = service.submit_for_review(task.id, reviewer_id)
⋮----
"""
    获取复核任务列表
    
    权限：管理员和标注员可以访问
    - 管理员：可以看到所有复核任务
    - 标注员：只能看到他人标注的任务的复核
    
    Args:
        status: 复核状态筛选（pending/approved/rejected）
        reviewer_id: 复核人员ID筛选
        skip: 跳过记录数
        limit: 返回记录数
        current_user: 当前用户信息
    
    Returns:
        List[ReviewTaskResponse]: 复核任务列表
    """
# 检查权限：只有管理员和标注员可以访问
⋮----
# 构建响应
result = []
⋮----
# 查询关联的标注任务
⋮----
# 如果是标注员，过滤掉自己标注的任务
⋮----
user_id = current_user.get('user_id')
⋮----
continue  # 跳过自己标注的任务
⋮----
"""
    获取复核任务详情
    
    Args:
        review_id: 复核任务ID
    
    Returns:
        Dict: 复核任务详情，包含完整的标注数据
    """
⋮----
detail = service.get_review_task_detail(review_id)
⋮----
"""
    批准复核任务
    
    Args:
        review_id: 复核任务ID
        request: 复核操作请求（包含复核意见和复核人员ID）
    
    Returns:
        ReviewTaskResponse: 更新后的复核任务
    """
# 从请求体中获取 reviewer_id，默认为 1
reviewer_id = getattr(request, 'reviewer_id', 1)
⋮----
review = service.approve_task(
⋮----
"""
    驳回复核任务
    
    Args:
        review_id: 复核任务ID
        request: 复核操作请求（必须包含驳回原因和复核人员ID）
    
    Returns:
        ReviewTaskResponse: 更新后的复核任务
    """
⋮----
review = service.reject_task(
⋮----
"""
    获取数据集的质量统计
    
    Args:
        dataset_id: 数据集ID
    
    Returns:
        Dict: 质量统计指标
    """
⋮----
stats = service.calculate_quality_statistics(dataset_id)
⋮----
"""
    获取数据集的复核摘要
    
    Args:
        dataset_id: 数据集ID
    
    Returns:
        Dict: 复核摘要信息
    """
⋮----
summary = service.get_dataset_review_summary(dataset_id)
````

## File: backend/api/structured_export.py
````python
"""
Structured export API.
"""
⋮----
router = APIRouter(prefix="/api/v1/export/corpus", tags=["export"])
logger = logging.getLogger(__name__)
⋮----
def _get_json_files_for_data_source(processor_name: str, data_source: str | None = None) -> list[Path]
⋮----
json_dir = settings.PROCESSED_DIR / processor_name / data_source
⋮----
json_dir = settings.PROCESSED_DIR / processor_name
⋮----
json_files = sorted(json_dir.glob("page_*.json"))
⋮----
engine = QueryEngine(processor_name="failure_case")
grouped_records = engine._get_failure_case_list(db, limit=1_000_000, offset=0)
selected_sources = {str(item).strip() for item in (data_sources or []) if str(item).strip()}
⋮----
export_records: list[dict] = []
⋮----
source_file = (grouped.get("source_file") or "").strip()
data_source = sanitize_filename(Path(source_file).stem or source_file)
⋮----
image_paths = [str(path).strip() for path in (grouped.get("image_paths") or []) if str(path).strip()]
record = {
⋮----
json_files: list[Path] = []
⋮----
json_files = _get_json_files_for_data_source(processor_name)
⋮----
parser = DataParser(processor_name=processor_name)
all_records: list[dict] = []
⋮----
records = parser.parse_json_file(str(json_file))
data_source = json_file.parent.name
⋮----
class ExportRequest(BaseModel)
⋮----
data_sources: list[str] = []
⋮----
class BatchExportRequest(BaseModel)
⋮----
formats: list[str] = ["entity_text", "clip_alignment", "qa_alignment"]
include_images: bool = True
⋮----
start_time = time.time()
⋮----
all_records = _load_export_records(processor_name, request.data_sources, db)
⋮----
exporter = StructuredExportService(processor_name=processor_name)
results = exporter.export_entity_text(all_records)
⋮----
results = exporter.export_clip_alignment(all_records)
⋮----
results = exporter.export_qa_alignment(all_records)
⋮----
temp_file_path: str | None = None
⋮----
results = exporter.batch_export(all_records, request.formats, request.include_images)
⋮----
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
temp_file_path = temp_file.name
⋮----
json_str = json.dumps(results[fmt], ensure_ascii=False, indent=2)
⋮----
file_size = os.path.getsize(temp_file_path)
⋮----
zip_filename = f"corpus_export_{processor_name}_{timestamp}.zip"
````

## File: backend/api/users.py
````python
"""
用户管理和认证API
实现用户CRUD、登录登出和JWT认证
"""
⋮----
router = APIRouter(prefix="/api/v1/users", tags=["users"])
auth_router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
⋮----
# HTTPBearer 安全方案（Swagger UI 🔒 Authorize 按钮使用）
_bearer_scheme = HTTPBearer(auto_error=False)
⋮----
# ============================================================================
# 依赖注入
⋮----
def get_user_service(db: Session = Depends(get_db)) -> UserService
⋮----
"""获取用户服务实例"""
⋮----
"""
    从JWT令牌获取当前用户（支持 Swagger UI Authorize 按钮）
    
    Args:
        credentials: HTTPBearer 自动解析的 Bearer 令牌
        user_service: 用户服务
    
    Returns:
        dict: 用户信息
    
    Raises:
        HTTPException: 认证失败
    """
⋮----
token = credentials.credentials
⋮----
# 验证令牌
payload = user_service.verify_token(token)
⋮----
def require_admin(current_user: dict = Depends(get_current_user)) -> dict
⋮----
"""
    要求管理员权限
    
    Args:
        current_user: 当前用户
    
    Returns:
        dict: 用户信息
    
    Raises:
        HTTPException: 权限不足
    """
⋮----
# 认证API
⋮----
"""
    用户登录
    
    Args:
        request: 登录请求
        user_service: 用户服务
    
    Returns:
        LoginResponse: 登录响应（包含JWT令牌）
    
    Raises:
        HTTPException: 用户名或密码错误
    """
# 认证用户
user = user_service.authenticate(request.username, request.password)
⋮----
# 生成JWT令牌
access_token = user_service.create_access_token(
⋮----
@auth_router.post("/logout", response_model=SuccessResponse)
def logout(current_user: dict = Depends(get_current_user))
⋮----
"""
    用户登出
    
    Note: JWT是无状态的，登出主要由前端处理（删除token）
    此接口主要用于记录登出日志或执行其他清理操作
    
    Args:
        current_user: 当前用户
    
    Returns:
        SuccessResponse: 成功响应
    """
⋮----
"""
    获取当前用户信息
    
    Args:
        current_user: 当前用户
        user_service: 用户服务
    
    Returns:
        UserResponse: 用户信息
    
    Raises:
        HTTPException: 用户不存在
    """
user = user_service.get_user_by_id(current_user["user_id"])
⋮----
# 用户管理API
⋮----
"""
    创建用户（需要管理员权限）
    
    Args:
        request: 创建用户请求
        user_service: 用户服务
        admin: 管理员用户
    
    Returns:
        UserResponse: 创建的用户
    
    Raises:
        HTTPException: 用户名已存在或角色无效
    """
⋮----
user = user_service.create_user(
⋮----
"""
    获取用户列表
    
    Args:
        role: 角色筛选（可选）
        skip: 跳过记录数
        limit: 返回记录数
        user_service: 用户服务
        current_user: 当前用户
    
    Returns:
        List[UserResponse]: 用户列表
    """
⋮----
"""
    获取用户详情
    
    Args:
        user_id: 用户ID
        user_service: 用户服务
        current_user: 当前用户
    
    Returns:
        UserResponse: 用户信息
    
    Raises:
        HTTPException: 用户不存在
    """
user = user_service.get_user_by_id(user_id)
⋮----
"""
    更新用户信息（需要管理员权限）
    
    Args:
        user_id: 用户ID
        request: 更新用户请求
        user_service: 用户服务
        admin: 管理员用户
    
    Returns:
        UserResponse: 更新后的用户
    
    Raises:
        HTTPException: 用户不存在或用户名已被占用
    """
⋮----
user = user_service.update_user(
⋮----
"""
    删除用户（需要管理员权限）
    
    Args:
        user_id: 用户ID
        user_service: 用户服务
        admin: 管理员用户
    
    Returns:
        SuccessResponse: 成功响应
    
    Raises:
        HTTPException: 用户不存在
    """
⋮----
"""
    获取用户统计信息（需要管理员权限）
    
    Args:
        user_service: 用户服务
        admin: 管理员用户
    
    Returns:
        dict: 统计信息
    """
stats = user_service.get_user_statistics()
````

## File: backend/api/versions.py
````python
"""
版本管理API
提供标注任务的版本历史查询、回滚和比较功能
"""
⋮----
router = APIRouter(prefix="/api/v1/versions", tags=["versions"])
⋮----
# ============================================================================
# 版本比较API（必须在 /{task_id} 之前注册，否则被动态路由拦截）
⋮----
"""
    比较两个版本的差异

    返回两个版本之间的详细差异信息,包括:
    - 新增的实体、图片实体、关系
    - 删除的实体、图片实体、关系
    - 修改的实体、图片实体、关系
    """
⋮----
service = VersionManagementService(db)
diff = service.compare_versions(
⋮----
# 版本历史API
⋮----
"""
    获取标注任务的版本历史

    返回按时间倒序排列的版本历史列表
    """
⋮----
history = service.get_version_history(task_id, limit)
⋮----
# 版本回滚API
⋮----
"""
    回滚到指定版本

    注意:
    - 回滚前会自动创建当前版本的备份
    - 回滚后会创建新的版本记录
    - 回滚操作不可撤销,请谨慎操作
    """
⋮----
success = service.rollback_to_version(
⋮----
# 版本详情API
⋮----
"""
    获取指定版本的详细信息

    返回该版本的完整快照数据
    """
⋮----
# 查询任务
task = db.query(AnnotationTask).filter(
⋮----
# 查询版本
version_history = db.query(VersionHistory)\
⋮----
# 解析快照数据
snapshot_data = json.loads(version_history.snapshot_data)
⋮----
# 创建版本快照API
⋮----
"""
    手动创建版本快照

    用于在重要操作前手动保存当前状态
    """
⋮----
version_history = service.create_version(
````

## File: backend/check_assignments.py
````python
"""
检查数据库中的分配记录
"""
⋮----
def resolve_sqlite_path() -> Path
⋮----
"""Resolve the current SQLite database path from DATABASE_URL."""
db_url = settings.DATABASE_URL
⋮----
raw_path = Path(db_url.replace("sqlite:///", "", 1))
⋮----
DB_PATH = resolve_sqlite_path()
⋮----
def check_database()
⋮----
"""检查数据库中的分配记录"""
conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()
⋮----
users = cursor.fetchall()
⋮----
datasets = cursor.fetchall()
⋮----
assignments = cursor.fetchall()
⋮----
all_assignments = cursor.fetchall()
⋮----
status = "✓ 活跃" if assign[4] else "✗ 不活跃"
````

## File: backend/config.py
````python
"""Configuration module for the backend settings."""
⋮----
# Load .env file
⋮----
# Backend directory (used to resolve relative paths)
BACKEND_DIR = Path(__file__).resolve().parent
# Project root (multimodal_excel_system/), one level above backend/
PROJECT_DIR = BACKEND_DIR.parent
# All data files live under PROJECT_DIR/data/
_DATA_DIR = PROJECT_DIR / "data"
⋮----
def normalize_database_url(raw_value: str | None) -> str
⋮----
"""Normalize DATABASE_URL into a SQLAlchemy-compatible URL."""
⋮----
value = raw_value.strip().strip('"').strip("'")
⋮----
# Already a full URL
⋮----
# Support relative/absolute filesystem paths
path = Path(value)
⋮----
path = (BACKEND_DIR / value).resolve()
⋮----
class Settings
⋮----
"""Application settings."""
⋮----
# Application
APP_NAME: str = "面向离散型电子信息制造业的多模态语料库构建平台"
APP_VERSION: str = "1.0.0"
DEBUG: bool = True
⋮----
# Server
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "18080"))
⋮----
# CORS
CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
⋮----
# Database
DATABASE_URL: str = normalize_database_url(os.getenv("DATABASE_URL"))
⋮----
# LLM
DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
DASHSCOPE_BASE_URL: str = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
LLM_MODEL: str = "qwen-max"
LLM_TEMPERATURE: float = 0.0
LLM_TIMEOUT_SECONDS: int = int(os.getenv("LLM_TIMEOUT_SECONDS", "120"))
LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "1"))
⋮----
# Storage — all paths are absolute, anchored to PROJECT_DIR/data/
STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")  # 'local' or 'minio'
UPLOAD_DIR: Path = _DATA_DIR / "uploads"
IMAGE_DIR: Path = _DATA_DIR / "images"
EXPORT_DIR: Path = _DATA_DIR / "exports"
PROCESSED_DIR: Path = _DATA_DIR / "processed"
DATABASE_DIR: Path = _DATA_DIR / "database"
MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
⋮----
# MinIO (when STORAGE_TYPE='minio')
MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "annotation-images")
MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
MINIO_PUBLIC_URL: str = os.getenv("MINIO_PUBLIC_URL", "")  # Optional public URL
⋮----
# JWT
SECRET_KEY: str = "your-secret-key-change-in-production"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
⋮----
# Batch tasks
BATCH_SIZE: int = 10
MAX_CONCURRENT_TASKS: int = 5
⋮----
# Global settings instance
settings = Settings()
⋮----
# Ensure required directories exist
````

## File: backend/database.py
````python
"""
数据库连接和会话管理
"""
⋮----
# 创建数据库引擎
engine = create_engine(
⋮----
connect_args={"check_same_thread": False},  # SQLite需要
⋮----
# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
⋮----
# 创建Base类
Base = declarative_base()
⋮----
def get_db()
⋮----
"""
    获取数据库会话
    用于FastAPI依赖注入
    """
db = SessionLocal()
⋮----
def run_migration_v005()
⋮----
"""执行 v005 迁移：新增 KF/QMS 相关表"""
migration_path = Path(__file__).parent / "migrations" / "v005_add_kf_qms_tables.sql"
⋮----
sql = migration_path.read_text(encoding="utf-8")
⋮----
stmt = statement.strip()
⋮----
def init_db()
⋮----
"""
    初始化数据库
    创建所有表并执行迁移
    """
# 导入所有模型以确保它们被注册
from models import db_models  # noqa
⋮----
def drop_db()
⋮----
"""
    删除所有表（仅用于开发/测试）
    """
````

## File: backend/init_db.py
````python
"""
数据库初始化脚本
创建所有表并插入初始数据
"""
⋮----
# 添加backend目录到Python路径
⋮----
def create_default_entity_types(db)
⋮----
"""创建默认实体类型（品质失效案例领域本体）"""
⋮----
# 检查是否已存在实体类型
existing_count = db.query(EntityType).count()
⋮----
# 文本实体类型
text_entity_types = [
⋮----
# 图片实体类型
image_entity_types = [
⋮----
all_types = text_entity_types + image_entity_types
⋮----
entity_type = EntityType(**et)
⋮----
def create_default_relation_types(db)
⋮----
"""创建默认关系类型"""
⋮----
# 检查是否已存在关系类型
existing_count = db.query(RelationType).count()
⋮----
relation_types = [
⋮----
relation_type = RelationType(**rt)
⋮----
def create_default_admin(db)
⋮----
"""创建默认管理员账户"""
⋮----
# 检查是否已存在管理员
existing_admin = db.query(User).filter(User.username == "admin").first()
⋮----
# 使用bcrypt加密密码
password = "admin123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
password_hash = hashed.decode('utf-8')
⋮----
# 更新现有管理员的密码
⋮----
# 创建新的管理员
admin = User(
⋮----
def main()
⋮----
"""主函数"""
⋮----
# 创建所有表
⋮----
# 创建数据库会话
db = SessionLocal()
⋮----
# 插入初始数据
````

## File: backend/main.py
````python
"""FastAPI application entrypoint."""
⋮----
# middlewares
⋮----
logger = get_logger(__name__)
⋮----
IMAGE_MEDIA_TYPES = {
⋮----
@asynccontextmanager
async def lifespan(app: FastAPI)
⋮----
"""Manage startup and shutdown logs."""
⋮----
app = FastAPI(
⋮----
# Middlewares
⋮----
# Routers (order matters for grouped corpus)
⋮----
# CORS
⋮----
# Static or delegated file serving
⋮----
@app.get("/images/{file_path:path}")
    async def get_image(file_path: str)
⋮----
"""Fetch image from object storage."""
image_data = storage_service.get_image(file_path)
⋮----
ext = file_path.split('.')[-1].lower()
content_type_map = {
content_type = content_type_map.get(ext, 'image/png')
⋮----
"""Resolve processed image path and prevent path traversal."""
⋮----
base_dir = settings.PROCESSED_DIR.resolve()
candidate = (base_dir / processor_name / data_source / image_path).resolve()
⋮----
@app.get("/processed-images/{processor_name}/{data_source}/{image_path:path}")
async def get_processed_image(processor_name: str, data_source: str, image_path: str)
⋮----
"""
    Serve KF/QMS processed image files.

    These images are stored under data/processed/{processor}/{data_source}/imgs/*
    and are separate from storage_service-managed /images files.
    """
resolved = _safe_resolve_processed_image_path(processor_name, data_source, image_path)
⋮----
ext = resolved.suffix.lower()
media_type = IMAGE_MEDIA_TYPES.get(ext)
⋮----
@app.get("/")
async def root()
⋮----
"""Root service metadata."""
⋮----
@app.get("/health")
async def health_check()
⋮----
"""Health check endpoint."""
⋮----
@app.exception_handler(Exception)
async def global_exception_handler(request, exc)
⋮----
"""Catch-all exception handler returning JSON."""
````

## File: backend/middleware/__init__.py
````python
"""
中间件模块
提供错误处理、日志记录等中间件功能
"""
⋮----
__all__ = [
````

## File: backend/middleware/error_handler.py
````python
"""
统一错误处理中间件
提供标准化的错误响应格式和日志记录
"""
⋮----
# 确保logs目录存在
log_dir = Path('logs')
⋮----
# 配置日志
⋮----
logger = logging.getLogger(__name__)
⋮----
class ErrorResponse
⋮----
"""标准错误响应格式"""
⋮----
"""
        格式化错误响应
        
        Args:
            error_code: 错误代码
            message: 错误消息
            details: 错误详情
            status_code: HTTP状态码
        
        Returns:
            dict: 标准化的错误响应
        """
response = {
⋮----
async def error_handler_middleware(request: Request, call_next)
⋮----
"""
    全局错误处理中间件
    
    捕获所有未处理的异常并返回标准化的错误响应
    """
⋮----
response = await call_next(request)
⋮----
# 请求验证错误
⋮----
error_details = []
⋮----
# 数据库错误
⋮----
# 值错误（通常是业务逻辑错误）
⋮----
# 权限错误
⋮----
# 文件未找到
⋮----
# 未知错误
⋮----
class APIException(Exception)
⋮----
"""自定义API异常基类"""
⋮----
class NotFoundException(APIException)
⋮----
"""资源未找到异常"""
⋮----
def __init__(self, resource: str, identifier: str = None)
⋮----
message = f"{resource}不存在"
⋮----
class ValidationException(APIException)
⋮----
"""验证异常"""
⋮----
def __init__(self, message: str, details: Union[dict, list] = None)
⋮----
class AuthenticationException(APIException)
⋮----
"""认证异常"""
⋮----
def __init__(self, message: str = "认证失败")
⋮----
class AuthorizationException(APIException)
⋮----
"""授权异常"""
⋮----
def __init__(self, message: str = "没有权限执行此操作")
⋮----
# 日志工具函数
⋮----
def log_request(request: Request)
⋮----
"""记录请求日志"""
⋮----
def log_response(response, duration: float)
⋮----
"""记录响应日志"""
⋮----
def log_error(error: Exception, context: str = "")
⋮----
"""记录错误日志"""
````

## File: backend/middleware/logging_config.py
````python
"""
日志配置
提供统一的日志配置和管理
"""
⋮----
# 创建logs目录
LOGS_DIR = Path(__file__).parent.parent / "logs"
⋮----
class LogConfig
⋮----
"""日志配置类"""
⋮----
# 日志级别
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
⋮----
# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
⋮----
# 日志文件配置
APP_LOG_FILE = LOGS_DIR / "app.log"
ERROR_LOG_FILE = LOGS_DIR / "error.log"
ACCESS_LOG_FILE = LOGS_DIR / "access.log"
⋮----
# 文件大小限制（10MB）
MAX_BYTES = 10 * 1024 * 1024
⋮----
# 备份文件数量
BACKUP_COUNT = 5
⋮----
def setup_logging()
⋮----
"""设置日志配置"""
⋮----
# 创建根日志器
root_logger = logging.getLogger()
⋮----
# 清除现有的处理器
⋮----
# 创建格式化器
formatter = logging.Formatter(
⋮----
# 1. 控制台处理器
console_handler = logging.StreamHandler()
⋮----
# 2. 应用日志文件处理器（所有日志）
app_handler = RotatingFileHandler(
⋮----
# 3. 错误日志文件处理器（仅ERROR及以上）
error_handler = RotatingFileHandler(
⋮----
# 4. 访问日志处理器（按天轮转）
access_handler = TimedRotatingFileHandler(
⋮----
# 创建访问日志器
access_logger = logging.getLogger('access')
⋮----
def get_logger(name: str) -> logging.Logger
⋮----
"""
    获取日志器
    
    Args:
        name: 日志器名称（通常使用__name__）
    
    Returns:
        logging.Logger: 日志器实例
    """
⋮----
# 日志装饰器
⋮----
def log_function_call(func)
⋮----
"""记录函数调用的装饰器"""
⋮----
@functools.wraps(func)
    def wrapper(*args, **kwargs)
⋮----
logger = get_logger(func.__module__)
⋮----
result = func(*args, **kwargs)
⋮----
def log_execution_time(func)
⋮----
"""记录函数执行时间的装饰器"""
⋮----
start_time = time.time()
⋮----
duration = time.time() - start_time
⋮----
# 初始化日志系统
````

## File: backend/models/__init__.py
````python
"""
数据模型包
"""
# SQLAlchemy数据库模型
⋮----
# Pydantic数据模型
⋮----
# 枚举
⋮----
# 基础模型
⋮----
# 用户模型
⋮----
# 语料模型
⋮----
# 数据集模型
⋮----
# 标注任务模型
⋮----
# 批量标注模型
⋮----
# 标签配置模型
⋮----
# 复核模型
⋮----
# 版本模型
⋮----
# 导出模型
⋮----
# 通用响应
⋮----
__all__ = [
⋮----
# 数据库模型
⋮----
# Pydantic模型
````

## File: backend/models/db_models.py
````python
"""
SQLAlchemy数据库模型
定义所有数据库表结构
"""
⋮----
class User(Base)
⋮----
"""用户表"""
__tablename__ = "users"
⋮----
id = Column(Integer, primary_key=True, autoincrement=True)
username = Column(String(50), unique=True, nullable=False, index=True)
password_hash = Column(String(255), nullable=False)
role = Column(String(20), nullable=False)  # 'admin', 'annotator', 'reviewer'
created_at = Column(DateTime, default=datetime.utcnow)
updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
⋮----
# 关系
datasets = relationship("Dataset", back_populates="creator")
annotation_tasks = relationship("AnnotationTask", back_populates="assignee")
dataset_assignments = relationship("DatasetAssignment", foreign_keys="DatasetAssignment.user_id", back_populates="user")
⋮----
class Corpus(Base)
⋮----
"""原始语料表"""
__tablename__ = "corpus"
⋮----
text_id = Column(String(100), unique=True, nullable=False, index=True)
text = Column(Text, nullable=False)
text_type = Column(String(100))  # 句子分类（字段来源）
source_file = Column(String(255))
source_row = Column(Integer)
source_field = Column(String(100), index=True)
has_images = Column(Boolean, default=False)
⋮----
images = relationship("Image", back_populates="corpus", cascade="all, delete-orphan")
dataset_associations = relationship("DatasetCorpus", back_populates="corpus")
⋮----
class Image(Base)
⋮----
"""图片表"""
__tablename__ = "images"
⋮----
image_id = Column(String(100), unique=True, nullable=False, index=True)
corpus_id = Column(Integer, ForeignKey("corpus.id", ondelete="CASCADE"))
file_path = Column(String(500), nullable=False)
original_name = Column(String(255))
width = Column(Integer)
height = Column(Integer)
⋮----
corpus = relationship("Corpus", back_populates="images")
image_entities = relationship("ImageEntity", back_populates="image", cascade="all, delete-orphan")
⋮----
class Dataset(Base)
⋮----
"""数据集表"""
__tablename__ = "datasets"
⋮----
dataset_id = Column(String(100), unique=True, nullable=False, index=True)
name = Column(String(255), nullable=False)
description = Column(Text)
label_schema_version_id = Column(Integer, ForeignKey("label_schema_versions.id"))  # 使用的标签体系版本
created_by = Column(Integer, ForeignKey("users.id"))
⋮----
creator = relationship("User", back_populates="datasets")
label_schema_version = relationship("LabelSchemaVersion", back_populates="datasets")
corpus_associations = relationship("DatasetCorpus", back_populates="dataset", cascade="all, delete-orphan")
annotation_tasks = relationship("AnnotationTask", back_populates="dataset", cascade="all, delete-orphan")
batch_jobs = relationship("BatchJob", back_populates="dataset", cascade="all, delete-orphan")
assignments = relationship("DatasetAssignment", back_populates="dataset", cascade="all, delete-orphan")
⋮----
class DatasetCorpus(Base)
⋮----
"""数据集-语料关联表"""
__tablename__ = "dataset_corpus"
⋮----
dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
corpus_id = Column(Integer, ForeignKey("corpus.id", ondelete="CASCADE"), nullable=False)
⋮----
# 唯一约束
__table_args__ = (UniqueConstraint('dataset_id', 'corpus_id', name='uix_dataset_corpus'),)
⋮----
dataset = relationship("Dataset", back_populates="corpus_associations")
corpus = relationship("Corpus", back_populates="dataset_associations")
⋮----
class DatasetAssignment(Base)
⋮----
"""数据集分配表"""
__tablename__ = "dataset_assignments"
⋮----
dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
role = Column(String(20), nullable=False, index=True)  # 'annotator' 或 'reviewer'
⋮----
# 任务范围（可选，NULL表示分配所有任务）
task_start_index = Column(Integer)  # 起始索引（从1开始，包含）
task_end_index = Column(Integer)    # 结束索引（包含）
⋮----
# 分配状态
is_active = Column(Boolean, default=True, nullable=False, index=True)  # 是否激活
⋮----
# 转移信息
transferred_to = Column(Integer, ForeignKey("users.id"))  # 转移给谁
transferred_at = Column(DateTime)  # 转移时间
transfer_reason = Column(Text)  # 转移原因
⋮----
# 分配信息
assigned_by = Column(Integer, ForeignKey("users.id"))  # 分配人
assigned_at = Column(DateTime, default=datetime.utcnow)
⋮----
dataset = relationship("Dataset", back_populates="assignments")
user = relationship("User", foreign_keys=[user_id], back_populates="dataset_assignments")
assigner = relationship("User", foreign_keys=[assigned_by])
transferred_to_user = relationship("User", foreign_keys=[transferred_to])
⋮----
# 索引
__table_args__ = (
⋮----
class AnnotationTask(Base)
⋮----
"""标注任务表"""
__tablename__ = "annotation_tasks"
⋮----
task_id = Column(String(100), unique=True, nullable=False, index=True)
⋮----
status = Column(String(20), default='pending', index=True)  # 'pending', 'processing', 'completed', 'failed'
annotation_type = Column(String(20))  # 'automatic', 'manual'，为空表示未选择
current_version = Column(Integer, default=1)
assigned_to = Column(Integer, ForeignKey("users.id"))
error_message = Column(Text)
⋮----
dataset = relationship("Dataset", back_populates="annotation_tasks")
assignee = relationship("User", back_populates="annotation_tasks")
text_entities = relationship("TextEntity", back_populates="task", cascade="all, delete-orphan")
image_entities = relationship("ImageEntity", back_populates="task", cascade="all, delete-orphan")
relations = relationship("Relation", back_populates="task", cascade="all, delete-orphan")
review_tasks = relationship("ReviewTask", back_populates="task", cascade="all, delete-orphan")
version_history = relationship("VersionHistory", back_populates="task", cascade="all, delete-orphan")
⋮----
class TextEntity(Base)
⋮----
"""文本实体表"""
__tablename__ = "text_entities"
⋮----
entity_id = Column(Integer, nullable=False)  # 实体在任务内的ID
task_id = Column(Integer, ForeignKey("annotation_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
version = Column(Integer, nullable=False, index=True)
token = Column(Text, nullable=False)
label = Column(String(50), nullable=False)
start_offset = Column(Integer, nullable=False)
end_offset = Column(Integer, nullable=False)
confidence = Column(Float)
⋮----
task = relationship("AnnotationTask", back_populates="text_entities")
⋮----
class ImageEntity(Base)
⋮----
"""图片实体表"""
__tablename__ = "image_entities"
⋮----
image_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
⋮----
bbox_x = Column(Integer)
bbox_y = Column(Integer)
bbox_width = Column(Integer)
bbox_height = Column(Integer)
⋮----
task = relationship("AnnotationTask", back_populates="image_entities")
image = relationship("Image", back_populates="image_entities")
⋮----
class Relation(Base)
⋮----
"""关系表"""
__tablename__ = "relations"
⋮----
relation_id = Column(Integer, nullable=False)  # 关系在任务内的ID
⋮----
from_entity_id = Column(Integer, nullable=False)
to_entity_id = Column(Integer, nullable=False)
relation_type = Column(String(50), nullable=False)
⋮----
task = relationship("AnnotationTask", back_populates="relations")
⋮----
class EntityType(Base)
⋮----
"""实体类型配置表"""
__tablename__ = "entity_types"
⋮----
type_name = Column(String(50), unique=True, nullable=False)
type_name_zh = Column(String(50), nullable=False)
color = Column(String(20), nullable=False)
description = Column(Text)  # 简短描述
definition = Column(Text)  # LLM生成的标准定义
examples = Column(Text)  # LLM生成的示例（JSON格式存储列表）
disambiguation = Column(Text)  # LLM生成的类别辨析
prompt_template = Column(Text)  # 用于生成该实体类型的Prompt模板
supports_bbox = Column(Boolean, default=False)  # 是否支持边界框（图片实体）
is_active = Column(Boolean, default=True)
is_reviewed = Column(Boolean, default=False)  # 是否已人工审核
reviewed_by = Column(Integer, ForeignKey("users.id"))  # 审核人
reviewed_at = Column(DateTime)  # 审核时间
⋮----
class RelationType(Base)
⋮----
"""关系类型配置表"""
__tablename__ = "relation_types"
⋮----
direction_rule = Column(Text)  # LLM生成的方向规则
⋮----
prompt_template = Column(Text)  # 用于生成该关系类型的Prompt模板
⋮----
class ReviewTask(Base)
⋮----
"""复核任务表"""
__tablename__ = "review_tasks"
⋮----
review_id = Column(String(100), unique=True, nullable=False, index=True)
task_id = Column(Integer, ForeignKey("annotation_tasks.id", ondelete="CASCADE"), nullable=False)
status = Column(String(20), default='pending')  # 'pending', 'approved', 'rejected'
reviewer_id = Column(Integer, ForeignKey("users.id"))
review_comment = Column(Text)
reviewed_at = Column(DateTime)
⋮----
task = relationship("AnnotationTask", back_populates="review_tasks")
⋮----
class VersionHistory(Base)
⋮----
"""版本历史表"""
__tablename__ = "version_history"
⋮----
history_id = Column(String(100), unique=True, nullable=False, index=True)
⋮----
version = Column(Integer, nullable=False)
change_type = Column(String(20), nullable=False)  # 'create', 'update', 'delete'
change_description = Column(Text)
changed_by = Column(Integer, ForeignKey("users.id"))
snapshot_data = Column(Text)  # JSON格式存储完整快照
⋮----
task = relationship("AnnotationTask", back_populates="version_history")
⋮----
class BatchJob(Base)
⋮----
"""批量任务表"""
__tablename__ = "batch_jobs"
⋮----
job_id = Column(String(100), unique=True, nullable=False, index=True)
⋮----
status = Column(String(20), default='pending')  # 'pending', 'processing', 'completed', 'completed_with_errors', 'failed', 'cancelled'
total_tasks = Column(Integer, default=0)
completed_tasks = Column(Integer, default=0)
failed_tasks = Column(Integer, default=0)
progress = Column(Float, default=0.0)  # 进度 0.0-1.0
error_message = Column(Text)  # 错误信息
created_by = Column(Integer, ForeignKey("users.id"))  # 创建人
started_at = Column(DateTime)
completed_at = Column(DateTime)
⋮----
dataset = relationship("Dataset", back_populates="batch_jobs")
creator = relationship("User", foreign_keys=[created_by])
⋮----
class LabelSchemaVersion(Base)
⋮----
"""标签体系版本表"""
__tablename__ = "label_schema_versions"
⋮----
version_id = Column(String(100), unique=True, nullable=False, index=True)
version_name = Column(String(255), nullable=False)  # 如: "品质失效v1.0", "供应链风险v1.0"
⋮----
schema_data = Column(Text, nullable=False)  # JSON格式存储完整的标签配置快照
is_active = Column(Boolean, default=False)  # 是否为当前活跃版本
⋮----
datasets = relationship("Dataset", back_populates="label_schema_version")
⋮----
# ============================================
# KF/QMS 处理器相关模型
⋮----
class Customer(Base)
⋮----
"""客户表（KF和QMS共用）"""
__tablename__ = "customers"
⋮----
name = Column(String(255), unique=True, nullable=False)
⋮----
quick_response_events = relationship("QuickResponseEvent", back_populates="customer")
qms_defect_orders = relationship("QMSDefectOrder", back_populates="customer")
⋮----
class Product(Base)
⋮----
"""产品型号表"""
__tablename__ = "products"
⋮----
model = Column(String(255), unique=True, nullable=False)
product_category = Column(String(255))
industry_category = Column(String(255))
⋮----
quick_response_events = relationship("QuickResponseEvent", back_populates="product")
⋮----
class Defect(Base)
⋮----
"""缺陷类型表（KF和QMS共用）"""
__tablename__ = "defects"
⋮----
quick_response_events = relationship("QuickResponseEvent", back_populates="defect")
qms_defect_orders = relationship("QMSDefectOrder", back_populates="defect")
⋮----
class RootCause(Base)
⋮----
"""异常原因表"""
__tablename__ = "root_causes"
⋮----
category = Column(String(255))
process_category = Column(String(255))
⋮----
quick_response_events = relationship("QuickResponseEvent", back_populates="root_cause")
⋮----
class FourMElement(Base)
⋮----
"""4M要素表"""
__tablename__ = "four_m_elements"
⋮----
element = Column(String(255), unique=True, nullable=False)
⋮----
quick_response_events = relationship("QuickResponseEvent", back_populates="four_m_element")
⋮----
class QuickResponseEvent(Base)
⋮----
"""快反事件表"""
__tablename__ = "quick_response_events"
⋮----
id = Column(String(100), primary_key=True)  # 主键为String类型（非自增）
content_hash = Column(String(64), unique=True, nullable=True)  # 内容哈希，用于去重兜底
occurrence_time = Column(DateTime)
problem_analysis = Column(Text)
short_term_measure = Column(Text)
long_term_measure = Column(Text)
images = Column(Text)
data_source = Column(String(255))
classification = Column(String(255))
customer_id = Column(Integer, ForeignKey("customers.id"))
product_id = Column(Integer, ForeignKey("products.id"))
defect_id = Column(Integer, ForeignKey("defects.id"))
root_cause_id = Column(Integer, ForeignKey("root_causes.id"))
four_m_id = Column(Integer, ForeignKey("four_m_elements.id"))
⋮----
customer = relationship("Customer", back_populates="quick_response_events")
product = relationship("Product", back_populates="quick_response_events")
defect = relationship("Defect", back_populates="quick_response_events")
root_cause = relationship("RootCause", back_populates="quick_response_events")
four_m_element = relationship("FourMElement", back_populates="quick_response_events")
⋮----
class QMSWorkshop(Base)
⋮----
"""QMS车间表"""
__tablename__ = "qms_workshops"
⋮----
production_lines = relationship("QMSProductionLine", back_populates="workshop")
defect_orders = relationship("QMSDefectOrder", back_populates="workshop")
⋮----
class QMSProductionLine(Base)
⋮----
"""QMS产线表"""
__tablename__ = "qms_production_lines"
⋮----
workshop_id = Column(Integer, ForeignKey("qms_workshops.id"))
⋮----
__table_args__ = (UniqueConstraint('name', 'workshop_id', name='uix_line_name_workshop'),)
⋮----
workshop = relationship("QMSWorkshop", back_populates="production_lines")
defect_orders = relationship("QMSDefectOrder", back_populates="production_line")
⋮----
class QMSStation(Base)
⋮----
"""QMS岗位表"""
__tablename__ = "qms_stations"
⋮----
defect_orders = relationship("QMSDefectOrder", back_populates="station")
⋮----
class QMSInspectionNode(Base)
⋮----
"""QMS质检节点表"""
__tablename__ = "qms_inspection_nodes"
⋮----
defect_orders = relationship("QMSDefectOrder", back_populates="inspection_node")
⋮----
class QMSDefectOrder(Base)
⋮----
"""QMS不合格品记录表"""
__tablename__ = "qms_defect_orders"
⋮----
entry_time = Column(String(255))
model = Column(String(255))
barcode = Column(String(255))
position = Column(String(255))
photo_path = Column(Text)
status = Column(String(255))
⋮----
line_id = Column(Integer, ForeignKey("qms_production_lines.id"))
station_id = Column(Integer, ForeignKey("qms_stations.id"))
⋮----
inspection_node_id = Column(Integer, ForeignKey("qms_inspection_nodes.id"))
⋮----
customer = relationship("Customer", back_populates="qms_defect_orders")
workshop = relationship("QMSWorkshop", back_populates="defect_orders")
production_line = relationship("QMSProductionLine", back_populates="defect_orders")
station = relationship("QMSStation", back_populates="defect_orders")
defect = relationship("Defect", back_populates="qms_defect_orders")
inspection_node = relationship("QMSInspectionNode", back_populates="defect_orders")
````

## File: backend/models/schemas.py
````python
"""
Pydantic数据模型
用于API请求和响应的数据验证
"""
⋮----
# ============================================================================
# 枚举类型
⋮----
class TaskStatus(str, Enum)
⋮----
"""任务状态"""
PENDING = "pending"
PROCESSING = "processing"
COMPLETED = "completed"
FAILED = "failed"
⋮----
class AnnotationType(str, Enum)
⋮----
"""标注类型"""
AUTOMATIC = "automatic"
MANUAL = "manual"
⋮----
class ReviewStatus(str, Enum)
⋮----
"""复核状态"""
⋮----
APPROVED = "approved"
REJECTED = "rejected"
⋮----
class ChangeType(str, Enum)
⋮----
"""变更类型"""
CREATE = "create"
UPDATE = "update"
DELETE = "delete"
⋮----
class UserRole(str, Enum)
⋮----
"""用户角色"""
ADMIN = "admin"
ANNOTATOR = "annotator"
REVIEWER = "reviewer"  # Task 47: 新增复核员角色
VIEWER = "viewer"
⋮----
# 基础模型
⋮----
class BoundingBox(BaseModel)
⋮----
"""边界框模型"""
x: int = Field(..., description="X坐标")
y: int = Field(..., description="Y坐标")
width: int = Field(..., description="宽度")
height: int = Field(..., description="高度")
⋮----
class Entity(BaseModel)
⋮----
"""文本实体模型"""
id: int = Field(..., description="实体ID")
token: str = Field(..., description="实体文本")
label: str = Field(..., description="实体标签")
start_offset: int = Field(..., description="起始偏移量")
end_offset: int = Field(..., description="结束偏移量")
confidence: Optional[float] = Field(None, description="置信度")
⋮----
class ImageEntity(BaseModel)
⋮----
"""图片实体模型"""
⋮----
image_id: str = Field(..., description="图片ID")
⋮----
bbox: Optional[BoundingBox] = Field(None, description="边界框（区域实体）")
⋮----
class Relation(BaseModel)
⋮----
"""关系模型"""
id: int = Field(..., description="关系ID")
from_id: int = Field(..., description="源实体ID")
to_id: int = Field(..., description="目标实体ID")
type: str = Field(..., description="关系类型")
⋮----
# 用户相关模型
⋮----
class UserCreate(BaseModel)
⋮----
"""创建用户请求"""
username: str = Field(..., min_length=3, max_length=50, description="用户名")
password: str = Field(..., min_length=6, description="密码")
role: UserRole = Field(..., description="用户角色")
⋮----
class UserUpdate(BaseModel)
⋮----
"""更新用户请求"""
password: Optional[str] = Field(None, min_length=6, description="新密码")
role: Optional[UserRole] = Field(None, description="用户角色")
⋮----
class UserResponse(BaseModel)
⋮----
"""用户响应"""
id: int
username: str
role: str
created_at: datetime
⋮----
model_config = {"from_attributes": True}
⋮----
class LoginRequest(BaseModel)
⋮----
"""登录请求"""
username: str = Field(..., description="用户名")
password: str = Field(..., description="密码")
⋮----
class LoginResponse(BaseModel)
⋮----
"""登录响应"""
access_token: str = Field(..., description="访问令牌")
token_type: str = Field(default="bearer", description="令牌类型")
user: UserResponse
⋮----
# 语料相关模型
⋮----
class ImageInfo(BaseModel)
⋮----
"""图片信息"""
image_id: str
file_path: str
original_name: Optional[str] = None
width: Optional[int] = None
height: Optional[int] = None
⋮----
class CorpusRecord(BaseModel)
⋮----
"""语料记录"""
id: Optional[int] = None  # 数据库ID，用于创建数据集
text_id: str
text: str
text_type: Optional[str] = None  # 句子分类
source_file: Optional[str] = None
source_row: Optional[int] = None
source_field: Optional[str] = None
has_images: bool = False
images: List[ImageInfo] = []
⋮----
class CorpusListResponse(BaseModel)
⋮----
"""语料列表响应"""
total: int
items: List[CorpusRecord]
⋮----
class ExcelUploadResponse(BaseModel)
⋮----
"""Excel上传响应"""
success: bool
message: str
total_records: int
total_sentences: int
total_images: int
field_distribution: Dict[str, int]  # 各字段句子分布
⋮----
# 数据集相关模型
⋮----
class DatasetCreateRequest(BaseModel)
⋮----
"""创建数据集请求"""
name: str = Field(..., min_length=1, max_length=255, description="数据集名称")
description: Optional[str] = Field(None, description="数据集描述")
corpus_ids: List[int] = Field(..., min_length=1, description="语料ID列表")
created_by: int = Field(..., description="创建人ID")
label_schema_version_id: Optional[int] = Field(None, description="标签体系版本ID")
⋮----
class DatasetUpdateRequest(BaseModel)
⋮----
"""更新数据集请求"""
name: Optional[str] = Field(None, min_length=1, max_length=255, description="数据集名称")
⋮----
class DatasetResponse(BaseModel)
⋮----
"""数据集响应"""
success: bool = True
⋮----
data: Dict[str, Any]
⋮----
class DatasetListResponse(BaseModel)
⋮----
"""数据集列表响应"""
⋮----
class DatasetStatisticsResponse(BaseModel)
⋮----
"""数据集统计响应"""
⋮----
class DatasetExportRequest(BaseModel)
⋮----
"""数据集导出请求"""
output_path: Optional[str] = Field(None, description="导出路径")
status_filter: Optional[List[str]] = Field(None, description="状态筛选")
⋮----
# 标注任务相关模型
⋮----
class AnnotationTask(BaseModel)
⋮----
"""标注任务"""
task_id: str
dataset_id: str
corpus_id: str
⋮----
text_type: Optional[str] = None
⋮----
status: TaskStatus
annotation_type: AnnotationType
current_version: int
entities: List[Entity] = []
image_entities: List[ImageEntity] = []
relations: List[Relation] = []
error_message: Optional[str] = None
⋮----
updated_at: datetime
⋮----
class AddEntityRequest(BaseModel)
⋮----
"""添加实体请求"""
⋮----
class UpdateEntityRequest(BaseModel)
⋮----
"""更新实体请求"""
token: Optional[str] = None
label: Optional[str] = None
start_offset: Optional[int] = None
end_offset: Optional[int] = None
⋮----
class AddImageEntityRequest(BaseModel)
⋮----
"""添加图片实体请求"""
⋮----
bbox: Optional[BoundingBox] = Field(None, description="边界框（可选）")
⋮----
class AddRelationRequest(BaseModel)
⋮----
"""添加关系请求"""
⋮----
type: str = Field(default="relates_to", description="关系类型")
⋮----
class UpdateRelationRequest(BaseModel)
⋮----
"""更新关系请求"""
from_id: Optional[int] = None
to_id: Optional[int] = None
type: Optional[str] = None
⋮----
# 批量标注相关模型
⋮----
class BatchAnnotationRequest(BaseModel)
⋮----
"""批量标注请求"""
dataset_id: str = Field(..., description="数据集ID")
⋮----
class BatchJobResponse(BaseModel)
⋮----
"""批量任务响应"""
job_id: str
⋮----
status: str
total_tasks: int
completed_tasks: int
failed_tasks: int
progress: float  # 进度百分比
started_at: Optional[datetime]
completed_at: Optional[datetime]
⋮----
# 标签配置相关模型
⋮----
class EntityTypeConfig(BaseModel)
⋮----
"""实体类型配置"""
type_name: str = Field(..., description="类型名称")
type_name_zh: str = Field(..., description="中文名称")
color: str = Field(..., description="颜色代码")
description: Optional[str] = Field(None, description="描述")
supports_bbox: bool = Field(default=False, description="是否支持边界框")
is_active: bool = Field(default=True, description="是否激活")
⋮----
class RelationTypeConfig(BaseModel)
⋮----
"""关系类型配置"""
⋮----
class LabelSchema(BaseModel)
⋮----
"""标签体系"""
entity_types: List[EntityTypeConfig]
relation_types: List[RelationTypeConfig]
⋮----
# 复核相关模型
⋮----
class SubmitReviewRequest(BaseModel)
⋮----
"""提交复核请求"""
task_id: str = Field(..., description="任务ID")
⋮----
class ReviewActionRequest(BaseModel)
⋮----
"""复核操作请求"""
reviewer_id: Optional[int] = Field(1, description="复核人员ID")
review_comment: Optional[str] = Field(None, description="复核意见")
⋮----
class ReviewTaskResponse(BaseModel)
⋮----
"""复核任务响应"""
review_id: str
⋮----
status: ReviewStatus
reviewer_id: Optional[int]  # 改为 int 类型
review_comment: Optional[str]
reviewed_at: Optional[datetime]
⋮----
# 版本管理相关模型
⋮----
class VersionResponse(BaseModel)
⋮----
"""版本响应"""
history_id: str
⋮----
version: int
change_type: ChangeType
change_description: Optional[str]
changed_by: str
⋮----
class VersionDiff(BaseModel)
⋮----
"""版本差异"""
from_version: int
to_version: int
added_entities: List[Entity] = []
deleted_entities: List[Entity] = []
modified_entities: List[Dict[str, Any]] = []
added_relations: List[Relation] = []
deleted_relations: List[Relation] = []
modified_relations: List[Dict[str, Any]] = []
⋮----
# 导出相关模型
⋮----
class ExportRequest(BaseModel)
⋮----
"""导出请求"""
⋮----
text_type_filter: Optional[List[str]] = Field(None, description="句子分类筛选")
train_test_split: Optional[float] = Field(None, ge=0, le=1, description="训练集比例")
⋮----
class ExportResponse(BaseModel)
⋮----
"""导出响应"""
⋮----
# 通用响应模型
⋮----
class SuccessResponse(BaseModel)
⋮----
"""成功响应"""
⋮----
data: Optional[Any] = None
⋮----
class ErrorResponse(BaseModel)
⋮----
"""错误响应"""
success: bool = False
error_code: str
error_message: str
error_details: Optional[Dict[str, Any]] = None
timestamp: datetime = Field(default_factory=datetime.utcnow)
⋮----
# 数据集分配相关模型 (Task 47)
⋮----
class AssignmentMode(str, Enum)
⋮----
"""分配模式"""
FULL = "full"  # 整体分配
RANGE = "range"  # 范围分配
⋮----
class TransferMode(str, Enum)
⋮----
"""转移模式"""
ALL = "all"  # 转移所有任务
REMAINING = "remaining"  # 只转移未完成的任务
COMPLETED = "completed"  # 只转移已完成的任务
⋮----
class AssignmentRole(str, Enum)
⋮----
"""分配角色"""
⋮----
REVIEWER = "reviewer"
⋮----
class AssignmentRequest(BaseModel)
⋮----
"""分配数据集请求"""
user_id: int = Field(..., description="用户ID")
role: AssignmentRole = Field(..., description="分配角色")
mode: AssignmentMode = Field(AssignmentMode.FULL, description="分配模式")
start_index: Optional[int] = Field(None, description="起始任务索引（范围模式必需）")
end_index: Optional[int] = Field(None, description="结束任务索引（范围模式必需）")
⋮----
class Config
⋮----
json_schema_extra = {
⋮----
class AutoAssignmentRequest(BaseModel)
⋮----
"""自动分配数据集请求"""
user_ids: List[int] = Field(..., min_length=1, description="用户ID列表")
⋮----
class BatchAssignmentItem(BaseModel)
⋮----
"""批量分配项"""
⋮----
class BatchAssignmentRequest(BaseModel)
⋮----
"""批量分配请求"""
assignments: List[BatchAssignmentItem] = Field(..., min_length=1, description="分配列表")
clear_existing: bool = Field(True, description="是否清空现有分配")
role_filter: Optional[AssignmentRole] = Field(None, description="清空时的角色筛选")
⋮----
class TransferAssignmentRequest(BaseModel)
⋮----
"""转移分配请求"""
old_user_id: int = Field(..., description="原用户ID")
new_user_id: int = Field(..., description="新用户ID")
role: AssignmentRole = Field(..., description="角色")
transfer_mode: TransferMode = Field(TransferMode.ALL, description="转移模式")
transfer_reason: Optional[str] = Field(None, description="转移原因")
⋮----
class AssignmentInfo(BaseModel)
⋮----
"""分配信息"""
assignment_id: int = Field(..., description="分配ID")
⋮----
role: str = Field(..., description="角色")
task_range: Optional[str] = Field(None, description="任务范围（如：1-200）")
task_count: int = Field(..., description="任务数量")
completed_count: int = Field(0, description="已完成数量")
in_review_count: int = Field(0, description="复核中数量")
is_active: bool = Field(True, description="是否激活")
transferred_to: Optional[int] = Field(None, description="转移给谁")
transferred_to_username: Optional[str] = Field(None, description="转移给谁（用户名）")
transferred_at: Optional[datetime] = Field(None, description="转移时间")
⋮----
assigned_by: Optional[int] = Field(None, description="分配人ID")
assigned_at: datetime = Field(..., description="分配时间")
⋮----
class AssignmentResponse(BaseModel)
⋮----
"""分配响应"""
⋮----
data: AssignmentInfo
⋮----
class AutoAssignmentInfo(BaseModel)
⋮----
"""自动分配信息"""
user_id: int
⋮----
task_range: str
task_count: int
⋮----
class AutoAssignmentResponse(BaseModel)
⋮----
"""自动分配响应"""
⋮----
data: Dict[str, Any] = Field(..., description="包含 assignments 和 total_tasks")
⋮----
class AssignmentListResponse(BaseModel)
⋮----
"""分配列表响应"""
⋮----
message: str = "获取分配列表成功"
data: Dict[str, Any] = Field(..., description="包含 dataset_id, assignments, unassigned_count 等")
⋮----
class MyDatasetInfo(BaseModel)
⋮----
"""我的数据集信息"""
⋮----
name: str
description: Optional[str]
my_role: str
my_task_range: Optional[str]
my_task_count: int
my_completed_count: int
⋮----
assigned_at: datetime
⋮----
class MyDatasetsResponse(BaseModel)
⋮----
"""我的数据集列表响应"""
⋮----
message: str = "获取我的数据集成功"
data: Dict[str, Any] = Field(..., description="包含 items, total, page, page_size")
⋮----
class TransferAssignmentResponse(BaseModel)
⋮----
"""转移分配响应"""
⋮----
data: Dict[str, Any] = Field(..., description="包含转移详情")
⋮----
class CancelAssignmentCheckResponse(BaseModel)
⋮----
"""取消分配检查响应"""
can_cancel: bool
reason: str
stats: Dict[str, int]
action: Optional[str] = None  # 'transfer' 表示需要使用转移功能
````

## File: backend/processors/__init__.py
````python
"""处理器注册表"""
⋮----
_PROCESSORS = {
⋮----
def get_processor(name: str = 'kf')
⋮----
"""获取处理器实例"""
cls = _PROCESSORS.get(name)
⋮----
available = list(_PROCESSORS.keys())
⋮----
def list_processors()
⋮----
"""列出所有可用处理器"""
````

## File: backend/processors/base.py
````python
"""处理器抽象基类"""
⋮----
@dataclass
class ExportConfig
⋮----
"""导出配置"""
# 字段名映射 {标准键: 源字段名}
field_names: Dict[str, str]
# 实体字段列表 [(源字段名, 实体标签)]
entity_fields: List[Tuple[str, str]]
# 关系映射 [(源字段名, 关系类型)]
relation_mappings: List[Tuple[str, str]]
# Q&A 查询模板
qa_query: str
# CLIP 导出字段顺序
clip_fields: List[str]
# 事件ID字段名
event_id_field: str
⋮----
@dataclass
class GraphConfig
⋮----
"""前端图谱可视化配置"""
# 节点类型 {类型名: {label, color}}
node_types: Dict[str, dict]
# 边标签 {边类型: 显示标签}
edge_labels: Dict[str, str]
⋮----
class BaseProcessor(ABC)
⋮----
"""表格处理器基类，定义处理器插件接口"""
⋮----
@property
@abstractmethod
    def name(self) -> str
⋮----
"""处理器唯一标识"""
⋮----
@property
@abstractmethod
    def display_name(self) -> str
⋮----
"""显示名称"""
⋮----
@property
@abstractmethod
    def field_mapping(self) -> Dict[str, str]
⋮----
"""
        源字段名 → 标准实体字段名映射

        标准字段:
        - event_id, occurrence_time, problem_analysis, images, data_source
        - short_term_measure, long_term_measure, classification
        - customer, product_model, product_category, industry_category
        - defect, root_cause_category, process_category, four_m_element
        - workshop, production_line, station, inspection_node, status, barcode, position
        """
⋮----
@property
@abstractmethod
    def default_values(self) -> Dict[str, str]
⋮----
"""缺失字段默认值，键为源字段名"""
⋮----
@property
@abstractmethod
    def column_mappings(self) -> Dict[str, str]
⋮----
"""Excel 列名重映射（旧列名 → 标准列名）"""
⋮----
@abstractmethod
    def parse_excel(self, file_path: str, output_dir: str) -> dict
⋮----
"""解析 Excel 文件，输出 JSON"""
⋮----
@abstractmethod
    def get_export_config(self) -> ExportConfig
⋮----
"""返回导出配置"""
⋮----
@abstractmethod
    def get_graph_config(self) -> GraphConfig
⋮----
"""返回图谱可视化配置"""
⋮----
def extract_entities(self, record: Dict, data_source: str = None) -> Dict
⋮----
"""
        从解析后的记录中提取标准实体，默认实现使用 field_mapping。
        子类可覆写以实现自定义逻辑。
        """
fm = self.field_mapping
dv = self.default_values
⋮----
def _extract_images(self, image_text: str) -> List[str]
⋮----
"""从 Markdown 格式提取图片路径"""
⋮----
def build_entity_text(self, record: Dict, data_source: str = None) -> str
⋮----
"""
        构建实体文本描述，供 corpus_exporter 使用。
        子类可覆写以提供处理器特定的文本模板。
        默认实现返回空字符串（由 corpus_exporter 自行构建）。
        """
````

## File: backend/processors/failure_case.py
````python
"""品质失效案例处理器 - 管线A骨架（真正的AI标注走管线B的ExcelProcessingService）"""
⋮----
CANONICAL_SECOND_FIELD = '客户/发生工程/供应商'
SECOND_FIELD_ALIASES = [
⋮----
def _normalize_header_name(name: Any) -> str
⋮----
"""统一表头比较口径：去首尾空白并移除中间空白。"""
⋮----
text = str(name).strip()
⋮----
NORMALIZED_SECOND_FIELD_ALIASES = {_normalize_header_name(c) for c in SECOND_FIELD_ALIASES}
⋮----
# 源字段名 → 标准实体字段名
FIELD_MAPPING = {
⋮----
# 缺失字段默认值
DEFAULT_VALUES = {
⋮----
# Excel 列名重映射（别名 → 标准名）
COLUMN_MAPPINGS = {
⋮----
# 实体标注字段 [(源字段名, 实体标签)]
ENTITY_FIELDS = [
⋮----
# 关系映射 [(源字段名, 关系类型)]
RELATION_MAPPINGS = [
⋮----
# Q&A 查询模板
QA_QUERY = "这个品质失效案例的问题分类是什么？原因分析是什么？采取了什么措施？"
⋮----
# CLIP 导出字段顺序
CLIP_FIELDS = [
⋮----
class FailureCaseProcessor(BaseProcessor)
⋮----
"""品质失效案例处理器（管线A骨架）"""
⋮----
@property
    def name(self) -> str
⋮----
@property
    def display_name(self) -> str
⋮----
@property
    def field_mapping(self)
⋮----
@property
    def default_values(self)
⋮----
@property
    def column_mappings(self)
⋮----
def parse_excel(self, file_path: str, output_dir: str) -> dict
⋮----
"""
        解析品质失效案例 Excel，返回基本信息。
        output_dir 由 DocumentProcessor 传入用于写 JSON，骨架实现不使用。
        深度处理由管线B的 ExcelProcessingService 负责。
        """
REQUIRED_COLUMNS = [
normalized_required = {_normalize_header_name(col) for col in REQUIRED_COLUMNS}
⋮----
file_path = Path(file_path)
wb = openpyxl.load_workbook(file_path, data_only=True)
⋮----
all_tables: list[dict] = []
found_header = False
⋮----
ws = wb[sheet_name]
rows = list(ws.iter_rows(values_only=True))
⋮----
# 找到表头行（含所有必要列的行）
header = None
header_row_idx = None
⋮----
row_strs = [str(c).strip() if c is not None else "" for c in row]
normalized_row = {_normalize_header_name(c) for c in row_strs if c}
has_required = normalized_required.issubset(normalized_row)
has_second_field = bool(normalized_row & NORMALIZED_SECOND_FIELD_ALIASES)
⋮----
header_row_idx = i
header = [
found_header = True
⋮----
# 统计数据行数（跳过空行）
record_count = 0
⋮----
def get_export_config(self) -> ExportConfig
⋮----
def get_graph_config(self) -> GraphConfig
⋮----
"""品质案例不使用知识图谱（管线B负责实体关系标注）"""
⋮----
def build_entity_text(self, record: dict, data_source: str = None) -> str
⋮----
"""
        管线A骨架：品质案例的语料生成由管线B负责，
        此处返回简单的纯文本拼接，仅用于兼容接口。
        """
parts = []
⋮----
val = record.get(en_key) or record.get(cn_key, "")
````

## File: backend/processors/kf/__init__.py
````python
"""KF（快反问题记录）处理器"""
⋮----
class KFProcessor(BaseProcessor)
⋮----
"""快反问题记录处理器"""
⋮----
@property
    def name(self) -> str
⋮----
@property
    def display_name(self) -> str
⋮----
@property
    def field_mapping(self)
⋮----
@property
    def default_values(self)
⋮----
@property
    def column_mappings(self)
⋮----
def parse_excel(self, file_path, output_dir)
⋮----
def get_export_config(self)
⋮----
def get_graph_config(self)
````

## File: backend/processors/kf/config.py
````python
"""KF（快反问题记录）处理器配置 - 所有 KF 特有常量集中在此"""
⋮----
# 源字段名 → 标准实体字段名
FIELD_MAPPING = {
⋮----
# 老版本 Excel 缺失字段默认值
DEFAULT_VALUES = {
⋮----
# Excel 列名重映射（旧/别名 → 标准名）
COLUMN_MAPPINGS = {
⋮----
# --- 导出配置 ---
⋮----
# 实体标注字段 [(源字段名, 实体标签)]
ENTITY_FIELDS = [
⋮----
# 关系映射 [(源字段名, 关系类型)]
RELATION_MAPPINGS = [
⋮----
# Q&A 查询模板
QA_QUERY = "当前缺陷是什么？是什么原因导致的？如何解决？"
⋮----
# CLIP 导出字段顺序
CLIP_FIELDS = [
⋮----
# --- 图谱可视化配置 ---
⋮----
NODE_TYPES = {
⋮----
EDGE_LABELS = {
````

## File: backend/processors/kf/excel_tools.py
````python
"""KF Excel 工具函数 - 图片提取、列名映射等"""
⋮----
def detect_excel_type(xlsx_path)
⋮----
"""
    检测Excel文件类型（WPS或Microsoft）

    Returns:
        'wps': WPS Excel格式
        'microsoft': Microsoft Excel格式
        'unknown': 无法确定或没有图片
    """
⋮----
file_list = z.namelist()
⋮----
def extract_wps_excel_images(xlsx_path, out_dir='images')
⋮----
"""从WPS Excel中提取图片"""
⋮----
root = ET.fromstring(z.read('xl/cellimages.xml'))
ns = {'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
name2rid = {p.find('.//xdr:cNvPr', ns).get('name'):
⋮----
rel_root = ET.fromstring(z.read('xl/_rels/cellimages.xml.rels'))
rid2path = {c.get('Id'): c.get('Target') for c in rel_root}
⋮----
image_count = 0
⋮----
img_path = 'xl/' + rid2path[rid]
ext = os.path.splitext(img_path)[1] or '.png'
⋮----
def extract_microsoft_excel_images(xlsx_path, out_dir='images')
⋮----
"""从Microsoft Excel格式中提取图片，并使用UUID重命名"""
⋮----
image_mapping = {}
⋮----
drawing_files = [f for f in file_list
⋮----
drawing_xml = z.read(drawing_file)
drawing_root = ET.fromstring(drawing_xml)
⋮----
rel_file = drawing_file.replace('xl/drawings/', 'xl/drawings/_rels/') + '.rels'
⋮----
rel_xml = z.read(rel_file)
rel_root = ET.fromstring(rel_xml)
⋮----
ns_rel = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}
⋮----
rel_type = rel.get('Type', '')
target = rel.get('Target', '')
⋮----
image_path = 'xl/media/' + target.split('/')[-1]
⋮----
image_path = 'xl/' + target
⋮----
image_path = 'xl/drawings/' + target
⋮----
image_data = z.read(image_path)
original_name = os.path.basename(image_path)
⋮----
file_ext = os.path.splitext(original_name)[1]
uuid_name = f"ID_{uuid.uuid4().hex.upper()}{file_ext}"
⋮----
output_path = os.path.join(out_dir, uuid_name)
⋮----
def extract_excel_images(xlsx_path, out_dir='images')
⋮----
"""统一的Excel图片提取接口，自动检测类型"""
excel_type = detect_excel_type(xlsx_path)
⋮----
def table_str_wps_image_name_2_markdown_img_name(table_str: str, image_files_map: dict = None)
⋮----
"""将WPS Excel的DISPIMG格式转换为Markdown格式"""
# 先处理带扩展名的格式
out = re.sub(
⋮----
# 再处理不带扩展名的格式
⋮----
def replace_with_map(match)
⋮----
uuid = match.group(1)
⋮----
full_name = image_files_map[uuid]
⋮----
def extract_image_paths(text)
⋮----
"""从文本中提取图片路径"""
pattern = r'!\[图片\]\((imgs/[A-Za-z0-9_]+\.(png|jpeg|jpg))\)'
matches = re.findall(pattern, text, flags=re.I)
⋮----
def update_column_names(json_file_path, column_mappings=None)
⋮----
"""
    更新JSON文件中的列名

    Args:
        json_file_path: JSON文件路径
        column_mappings: 列名映射字典，如果为None则使用KF默认映射
    """
⋮----
column_mappings = COLUMN_MAPPINGS
⋮----
data = json.load(f)
table_data = data['table_data']
⋮----
keys_to_modify = list(item.keys())
````

## File: backend/processors/kf/node.py
````python
class Node
⋮----
def __init__(self)
⋮----
def add_table(self, html_content)
⋮----
"""将HTML表格内容解析并存储到table_data"""
⋮----
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find('table')
⋮----
rows = table.find_all('tr')
⋮----
headers = self._parse_table_headers(rows)
⋮----
def _parse_table_headers(self, rows)
⋮----
first_row = rows[0].find_all(['th', 'td'])
head_depth = max(int(c.get('rowspan', 1)) for c in first_row) if first_row else 1
canvas = []
col_cnt = 0
⋮----
c_idx = 0
⋮----
txt = cell.get_text(strip=True)
⋮----
flat = []
⋮----
def _parse_table_data(self, rows, headers)
⋮----
"""解析表格数据，支持单元格合并"""
data_rows = rows[self._get_header_rows(rows):]
⋮----
rowspan_tracker = {}
is_header_row = False
⋮----
cells = row.find_all(['th', 'td'])
row_data = {}
col_idx = 0
⋮----
is_header_row = True
⋮----
text_content = cell.get_text(separator=' ', strip=True)
⋮----
images = cell.find_all('img')
⋮----
img_list = [{'src': img.get('src', '')} for img in images]
cell_value = {
⋮----
cell_value = text_content
⋮----
rowspan = int(cell.get('rowspan', 1))
⋮----
next_row = row_idx + i
⋮----
colspan = int(cell.get('colspan', 1))
⋮----
def _get_header_rows(self, rows)
⋮----
"""识别表头行数"""
⋮----
max_span = 1
min_span = 100
⋮----
first_row_cells = rows[0].find_all(['th', 'td'])
⋮----
max_span = rowspan
⋮----
max_span = colspan
⋮----
min_span = rowspan
⋮----
min_span = colspan
⋮----
def to_dict(self)
⋮----
"""将节点数据转换为字典格式"""
````

## File: backend/processors/kf/parser.py
````python
"""KF Excel 解析器 - 使用 pandas + openpyxl"""
⋮----
def get_microsoft_excel_image_positions(xlsx_path)
⋮----
"""获取Microsoft Excel中图片所在的行号"""
⋮----
wb = load_workbook(xlsx_path)
ws = wb.active
⋮----
image_positions = {}
⋮----
row = img.anchor._from.row
⋮----
img_filename = os.path.basename(img.path)
⋮----
img_filename = f"image{row}.png"
⋮----
def insert_image_references_to_dataframe(df, image_mapping, image_column='问题图片')
⋮----
"""将图片引用插入到DataFrame的指定列"""
⋮----
sorted_images = sorted(
⋮----
def excel_to_html_table(excel_path: str, sheet_name=None, image_mapping=None) -> str
⋮----
"""使用 pandas 将 Excel 转换为 HTML 表格"""
⋮----
df = pd.read_excel(excel_path, sheet_name=sheet_name)
⋮----
df = insert_image_references_to_dataframe(df, image_mapping)
⋮----
html = df.to_html(index=False, na_rep='', border=1)
⋮----
def process_excel_file(src_file_path: str, output_dir: str = None)
⋮----
"""
    处理Excel文件，提取表格和图片信息并保存为JSON格式
    """
⋮----
# KF 必要列（排除 DEFAULT_VALUES 中允许缺失的可选字段）
REQUIRED_COLUMNS = [
⋮----
src_file = Path(src_file_path)
filename = src_file.stem
⋮----
out_root_dir = './Datas/tree_from_excel/' + filename
⋮----
out_root_dir = output_dir
⋮----
# 提取图片
out_img_dir = out_root_dir + '/imgs'
image_result = extract_excel_images(src_file, out_img_dir)
⋮----
image_mapping = None
image_files_map = {}
⋮----
image_mapping = image_result
⋮----
uuid = os.path.splitext(fname)[0]
⋮----
# 读取所有工作表
⋮----
sheet_names = excel_file.sheet_names
⋮----
# 校验必要列（先读第一个工作表做列名检查，支持别名重映射）
df_check = pd.read_excel(src_file_path, sheet_name=sheet_names[0], nrows=0)
actual_columns = {COLUMN_MAPPINGS.get(c, c) for c in df_check.columns}
missing = [col for col in REQUIRED_COLUMNS if col not in actual_columns]
⋮----
node_list = []
⋮----
html_table = excel_to_html_table(src_file_path, sheet_name, image_mapping)
table_str = table_str_wps_image_name_2_markdown_img_name(html_table, image_files_map)
imgs = extract_image_paths(table_str)
⋮----
node = Node()
⋮----
html_table = excel_to_html_table(src_file_path, None, image_mapping)
⋮----
node_list = [node]
⋮----
# 保存为 JSON
⋮----
json_path = out_root_dir + '/' + f'page_{i}.json'
````

## File: backend/processors/qms/__init__.py
````python
"""QMS（不合格品记录）处理器"""
⋮----
class QMSProcessor(BaseProcessor)
⋮----
"""不合格品记录处理器"""
⋮----
@property
    def name(self) -> str
⋮----
@property
    def display_name(self) -> str
⋮----
@property
    def field_mapping(self)
⋮----
@property
    def default_values(self)
⋮----
@property
    def column_mappings(self)
⋮----
def parse_excel(self, file_path, output_dir)
⋮----
def get_export_config(self)
⋮----
def get_graph_config(self)
⋮----
def extract_entities(self, record: dict, data_source: str = None) -> dict
⋮----
"""QMS 特有实体结构"""
fm = self.field_mapping
⋮----
def build_entity_text(self, record: dict, data_source: str = None) -> str
⋮----
"""构建 QMS 实体文本（用于语料导出）"""
⋮----
parts = [
⋮----
customer = record.get(fm.get('customer', ''), '')
model = record.get(fm.get('product_model', ''), '')
⋮----
barcode = record.get(fm.get('barcode', ''), '')
position = record.get(fm.get('position', ''), '')
⋮----
workshop = record.get(fm.get('workshop', ''), '')
line = record.get(fm.get('production_line', ''), '')
station = record.get(fm.get('station', ''), '')
prod_parts = []
⋮----
defect = record.get(fm.get('defect', ''), '')
⋮----
inspection_node = record.get(fm.get('inspection_node', ''), '')
status = record.get(fm.get('status', ''), '')
````

## File: backend/processors/qms/config.py
````python
"""QMS（不合格品记录）处理器配置 - 所有 QMS 特有常量集中在此"""
⋮----
# 源字段名 → 标准实体字段名
FIELD_MAPPING = {
⋮----
# QMS 无可选字段
DEFAULT_VALUES = {}
⋮----
# QMS 列名固定，无需重映射
COLUMN_MAPPINGS = {}
⋮----
# --- 导出配置 ---
⋮----
# 实体标注字段 [(源字段名, 实体标签)]
ENTITY_FIELDS = [
⋮----
# 关系映射 [(源字段名, 关系类型)]
RELATION_MAPPINGS = [
⋮----
# Q&A 查询模板
QA_QUERY = "这是什么不良现象？发生在哪个工位？如何处理？"
⋮----
# CLIP 导出字段顺序
CLIP_FIELDS = [
⋮----
# --- 图谱可视化配置 ---
⋮----
NODE_TYPES = {
⋮----
EDGE_LABELS = {
````

## File: backend/processors/qms/parser.py
````python
"""QMS Excel 解析器 - 使用 pandas 直读"""
⋮----
# QMS Excel 必须包含的列
REQUIRED_COLUMNS = [
⋮----
def _extract_filename_from_url(url_text: str) -> str
⋮----
"""从 URL 中提取文件名（name= 参数或路径最后一段）"""
⋮----
# 尝试提取 name= 参数
match = re.search(r'[?&]name=([^&]+)', url_text)
⋮----
# 尝试提取 URL 最后路径段
match = re.search(r'/([^/?]+)\??', url_text)
⋮----
def _find_image_file(filename: str, image_dirs: list) -> str
⋮----
"""在候选目录中查找匹配的图片文件，返回相对路径或空"""
⋮----
candidate = Path(img_dir) / filename
⋮----
def process_qms_excel(file_path: str, output_dir: str = None) -> dict
⋮----
"""
    处理 QMS Excel 文件，输出标准 JSON 格式。

    输出格式与 KF parser 一致：
    {
        "table_count": 1,
        "output_directory": str,
        "status": "success"
    }
    同时将每行数据保存为 page_0.json，键名保持原始中文列名。
    """
src_file = Path(file_path)
filename = src_file.stem
⋮----
out_root_dir = './Datas/tree_from_excel/' + filename
⋮----
out_root_dir = output_dir
⋮----
out_img_dir = os.path.join(out_root_dir, 'imgs')
⋮----
# 先只读表头做列名校验，避免大文件全量读取后才报错
⋮----
df_header = pd.read_excel(file_path, dtype=str, nrows=0)
⋮----
missing = [col for col in REQUIRED_COLUMNS if col not in df_header.columns]
⋮----
# 校验通过后读取全量数据
⋮----
df = pd.read_excel(file_path, dtype=str)
⋮----
# 处理每行数据
records = []
⋮----
record = {}
⋮----
val = row[col]
# 将 NaN/nan 转为空字符串
⋮----
# 处理照片字段：从 URL 提取文件名，尝试匹配本地图片
photo_url = record.get('照片', '')
⋮----
img_filename = _extract_filename_from_url(photo_url)
⋮----
local_path = _find_image_file(img_filename, [out_img_dir])
⋮----
# 保留文件名引用（图片尚未下载）
⋮----
# 若无法提取文件名，保持 URL 原文
⋮----
# 保存为 JSON
json_path = os.path.join(out_root_dir, 'page_0.json')
result_data = {
````

## File: backend/pytest.ini
````ini
[pytest]
# Pytest configuration file

# Test directories
testpaths = tests

# Ignore directories (manual test scripts are not pytest tests)
norecursedirs = manual test_artifacts __pycache__ .git

# Python file patterns
python_files = test_*.py

# Python class patterns
python_classes = Test*

# Python function patterns
python_functions = test_*

# Output options
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings

# Markers
markers =
    unit: Unit tests
    api: API tests
    integration: Integration tests
    agents: Agent tests
    slow: Slow tests

# Minimum version
minversion = 7.0
````

## File: backend/requirements.txt
````
# Web框架
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# LangChain和LLM
langchain==0.1.0
langchain-openai==0.0.2
langgraph==0.0.20

# 数据库
sqlalchemy==2.0.25
alembic==1.13.1

# 数据验证和序列化
pydantic==2.5.3
pydantic-settings==2.1.0

# Excel处理
openpyxl==3.1.2
pandas==2.1.4
beautifulsoup4==4.12.2

# 图片处理
Pillow==10.2.0

# 工具库
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dateutil==2.8.2

# 测试
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
hypothesis==6.92.2
````

## File: backend/scripts/apply_batch_job_migration.py
````python
"""
应用批量任务表字段迁移
添加 progress, error_message, created_by 字段
"""
⋮----
# 添加项目根目录到路径
⋮----
def apply_migration()
⋮----
"""应用迁移"""
settings = Settings()
# 从 DATABASE_URL 提取数据库文件路径
db_path = settings.DATABASE_URL.replace('sqlite:///', '')
⋮----
# 读取迁移SQL
migration_file = os.path.join(
⋮----
migration_sql = f.read()
⋮----
# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
⋮----
# 检查字段是否已存在
⋮----
columns = [row[1] for row in cursor.fetchall()]
⋮----
fields_to_add = ['progress', 'error_message', 'created_by']
missing_fields = [f for f in fields_to_add if f not in columns]
⋮----
# 执行迁移
# 分割SQL语句并逐个执行
statements = [s.strip() for s in migration_sql.split(';') if s.strip() and not s.strip().startswith('--')]
⋮----
# 验证迁移
⋮----
columns_after = [row[1] for row in cursor.fetchall()]
⋮----
# 检查所有字段是否都存在
all_present = all(f in columns_after for f in fields_to_add)
⋮----
success = apply_migration()
````

## File: backend/scripts/apply_index_migration.py
````python
"""
应用数据库索引迁移脚本

使用方法：
    python backend/scripts/apply_index_migration.py
"""
⋮----
# 添加项目根目录到 Python 路径
⋮----
def apply_migration()
⋮----
"""应用索引迁移"""
migration_file = Path(__file__).parent.parent / "migrations" / "add_task_query_indexes.sql"
⋮----
# 读取 SQL 文件
⋮----
sql_content = f.read()
⋮----
# 分割 SQL 语句（按分号分割，但跳过注释）
statements = []
current_statement = []
⋮----
# 跳过纯注释行
stripped = line.strip()
⋮----
# 如果行以分号结尾，这是一个完整的语句
⋮----
# 添加最后一个语句（如果有）
⋮----
# 执行迁移
⋮----
# 跳过空语句
⋮----
# 只显示 CREATE INDEX 语句
⋮----
# 提取索引名称
⋮----
# 如果索引已存在，继续执行
⋮----
# 验证索引
⋮----
result = conn.execute(text("""
⋮----
indexes = result.fetchall()
⋮----
def main()
⋮----
"""主函数"""
success = apply_migration()
````

## File: backend/scripts/check_db_status.py
````python
"""检查数据库状态"""
⋮----
# 检查所有表
result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
tables = [row[0] for row in result.fetchall()]
⋮----
# 检查 annotation_tasks 表是否存在
⋮----
# 检查现有索引
result = conn.execute(text("""
indexes = [row[0] for row in result.fetchall() if row[0]]
````

## File: backend/scripts/check_tables.py
````python
settings = Settings()
db_path = settings.DATABASE_URL.replace('sqlite:///', '')
⋮----
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
⋮----
tables = [row[0] for row in cursor.fetchall()]
⋮----
# 检查 batch_jobs 表
⋮----
columns = cursor.fetchall()
````

## File: backend/scripts/cleanup_test_files.py
````python
"""
清理测试生成的临时文件
"""
⋮----
def cleanup()
⋮----
"""清理测试文件"""
backend_dir = Path(__file__).parent.parent
⋮----
# 要清理的文件模式
patterns = [
⋮----
cleaned = []
⋮----
# 清理 __pycache__
````

## File: backend/scripts/db_migrate.py
````python
"""
数据库迁移管理工具
支持版本化的数据库迁移
"""
⋮----
# 添加项目根目录到路径
⋮----
class DatabaseMigrator
⋮----
"""数据库迁移管理器"""
⋮----
def __init__(self)
⋮----
def get_db_connection(self)
⋮----
"""获取数据库连接"""
⋮----
def get_current_version(self)
⋮----
"""获取当前数据库版本"""
conn = self.get_db_connection()
cursor = conn.cursor()
⋮----
# 尝试从 schema_version 表读取
⋮----
result = cursor.fetchone()
⋮----
# 表不存在，返回0
⋮----
def set_version(self, version, description="")
⋮----
"""设置数据库版本"""
⋮----
# 创建版本表（如果不存在）
⋮----
# 插入版本记录
⋮----
def get_migration_files(self)
⋮----
"""获取所有迁移文件"""
migrations = []
⋮----
# 解析文件名: v001_description.sql
filename = file.stem
parts = filename.split('_', 1)
⋮----
version_str = parts[0][1:]  # 去掉 'v' 前缀
⋮----
version = int(version_str)
description = parts[1].replace('_', ' ')
⋮----
def apply_migration(self, migration)
⋮----
"""应用单个迁移"""
⋮----
# 读取迁移文件
⋮----
sql_content = f.read()
⋮----
# 分割SQL语句
statements = []
current_statement = []
in_up_section = False
⋮----
stripped = line.strip()
⋮----
# 检测UP部分开始
⋮----
in_up_section = True
⋮----
# 检测DOWN部分开始（停止处理）
⋮----
# 跳过注释和空行
⋮----
# 如果遇到分号，表示语句结束
⋮----
statement = '\n'.join(current_statement)
⋮----
# 处理最后一个语句
⋮----
# 执行所有语句
⋮----
error_msg = str(e).lower()
⋮----
# 记录版本
⋮----
def upgrade(self, target_version=None)
⋮----
"""升级数据库到指定版本（或最新版本）"""
current_version = self.get_current_version()
migrations = self.get_migration_files()
⋮----
# 确定目标版本
⋮----
target_version = migrations[-1]['version']
⋮----
# 找到需要应用的迁移
pending_migrations = [
⋮----
# 应用迁移
success = True
⋮----
success = False
⋮----
def status(self)
⋮----
"""显示迁移状态"""
⋮----
latest_version = migrations[-1]['version']
⋮----
# 显示所有迁移
⋮----
version = migration['version']
status = "✅ 已应用" if version <= current_version else "⏳ 待应用"
⋮----
# 显示待应用的迁移
pending = [m for m in migrations if m['version'] > current_version]
⋮----
def create_migration(self, description)
⋮----
"""创建新的迁移文件"""
⋮----
# 确定新版本号
⋮----
next_version = migrations[-1]['version'] + 1
⋮----
next_version = 1
⋮----
# 生成文件名
filename = f"v{next_version:03d}_{description.replace(' ', '_')}.sql"
filepath = self.migrations_dir / filename
⋮----
# 创建迁移文件模板
template = f"""-- 迁移版本: v{next_version:03d}
⋮----
def main()
⋮----
"""主函数"""
parser = argparse.ArgumentParser(description='数据库迁移管理工具')
subparsers = parser.add_subparsers(dest='command', help='命令')
⋮----
# status 命令
⋮----
# upgrade 命令
upgrade_parser = subparsers.add_parser('upgrade', help='升级数据库')
⋮----
# create 命令
create_parser = subparsers.add_parser('create', help='创建新的迁移文件')
⋮----
# set-version 命令（谨慎使用）
set_version_parser = subparsers.add_parser('set-version', help='强制设置版本号（谨慎使用）')
⋮----
args = parser.parse_args()
⋮----
migrator = DatabaseMigrator()
````

## File: backend/scripts/extract_failures.py
````python
"""
提取测试失败的详细信息
"""
⋮----
def extract_failures()
⋮----
"""运行测试并提取失败信息"""
⋮----
# 运行pytest
result = subprocess.run(
⋮----
[sys.executable, "-m", "pytest", "-v", "--tb=short", "-x"],  # -x: 遇到第一个失败就停止
⋮----
lines = result.stdout.split('\n')
⋮----
# 查找失败的测试
failures = []
current_failure = None
in_failure = False
⋮----
# 检测失败的测试
⋮----
current_failure = {
in_failure = True
⋮----
# 收集失败详情
⋮----
# 显示失败信息
⋮----
for detail in failure['details'][:20]:  # 只显示前20行
⋮----
# 显示汇总
````

## File: backend/scripts/generate_test_report.py
````python
"""
生成测试报告到文件
"""
⋮----
def generate_report()
⋮----
"""生成测试报告"""
⋮----
# 运行pytest
result = subprocess.run(
⋮----
# 生成报告文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_file = f"test_report_{timestamp}.txt"
⋮----
# 写入报告
⋮----
# 提取并显示汇总
lines = result.stdout.split('\n')
⋮----
report_file = generate_report()
````

## File: backend/scripts/maintenance/clean_orphan_datasets.py
````python
"""
清理孤立的数据集数据
删除数据库中存在但语料已被删除的数据集
"""
⋮----
# 添加backend目录到Python路径
BACKEND_ROOT = Path(__file__).resolve().parents[2]
⋮----
def get_database_display_path() -> str
⋮----
"""获取当前数据库的可读路径（优先显示SQLite绝对路径）"""
db_url = settings.DATABASE_URL
⋮----
sqlite_path = db_url.replace("sqlite:///", "", 1)
⋮----
def clean_orphan_datasets(db)
⋮----
"""清理孤立的数据集"""
⋮----
# 获取所有数据集
datasets = db.query(Dataset).all()
⋮----
cleaned_count = 0
⋮----
# 检查数据集关联的语料是否存在
corpus_count = db.query(Corpus).join(
⋮----
# 删除关联的标注任务
task_count = db.query(AnnotationTask).filter(
⋮----
# 删除数据集-语料关联
relation_count = db.query(DatasetCorpus).filter(
⋮----
# 删除数据集
⋮----
def main()
⋮----
"""主函数"""
⋮----
# 创建数据库会话
db = SessionLocal()
````

## File: backend/scripts/maintenance/force_clean_db.py
````python
"""
强制清理数据库
删除所有数据集、语料、图片等数据，保留用户和标签配置
"""
⋮----
# 添加backend目录到Python路径
BACKEND_ROOT = Path(__file__).resolve().parents[2]  # backend/
⋮----
def resolve_sqlite_path(db_url: str) -> Path | None
⋮----
"""Resolve the SQLite file path for the current DATABASE_URL."""
⋮----
raw_path = Path(db_url.replace("sqlite:///", "", 1))
⋮----
def get_database_display_path() -> str
⋮----
"""获取当前数据库的可读路径（优先显示SQLite绝对路径）"""
sqlite_path = resolve_sqlite_path(settings.DATABASE_URL)
⋮----
def force_clean_all_data(db)
⋮----
"""强制清理所有业务数据"""
⋮----
cleanup_plan = [
⋮----
exists = db.execute(
⋮----
count = db.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar() or 0
⋮----
def clean_extra_databases()
⋮----
"""清理项目内遗留的歧义数据库文件，保留当前活动主库。"""
main_db_path = resolve_sqlite_path(settings.DATABASE_URL)
candidate_dirs = [
⋮----
seen_dirs = set()
removed = 0
⋮----
file_path = f.resolve()
⋮----
def clean_file_storage()
⋮----
"""清空业务文件（图片、上传、导出、中间处理文件）。"""
dirs = [
⋮----
def main()
⋮----
"""主函数"""
⋮----
confirm = input("\n确定要继续吗？(输入 'yes' 确认): ")
⋮----
# 创建数据库会话
db = SessionLocal()
````

## File: backend/scripts/maintenance/migrate_batch_jobs_fields.py
````python
"""
Add missing columns to the batch_jobs table.

This script is idempotent and always follows DATABASE_URL from .env.
It no longer falls back to any repo-local annotation.db file.
"""
⋮----
BACKEND_ROOT = Path(__file__).resolve().parents[2]
⋮----
REQUIRED_COLUMNS = {
⋮----
def get_sqlite_path_from_url(database_url: str) -> Path
⋮----
"""Resolve the SQLite file path from DATABASE_URL."""
⋮----
raw_path = database_url.replace("sqlite:///", "", 1)
path = Path(raw_path)
⋮----
path = (BACKEND_ROOT / path).resolve()
⋮----
def get_table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]
⋮----
"""Return the column names of a table."""
cursor = conn.execute(f"PRAGMA table_info({table_name})")
⋮----
def table_exists(conn: sqlite3.Connection, table_name: str) -> bool
⋮----
"""Check whether a table exists."""
cursor = conn.execute(
⋮----
def migrate_batch_jobs_fields() -> int
⋮----
"""Apply the migration and return the number of added columns."""
db_path = get_sqlite_path_from_url(settings.DATABASE_URL)
⋮----
added_count = 0
⋮----
existing_columns = get_table_columns(conn, "batch_jobs")
⋮----
alter_sql = f"ALTER TABLE batch_jobs ADD COLUMN {column_name} {column_def}"
⋮----
def main() -> None
⋮----
added = migrate_batch_jobs_fields()
````

## File: backend/scripts/maintenance/reset_db.py
````python
"""
数据库和文件完全重置脚本
删除所有数据、图片和上传文件，然后重新初始化
⚠️ 警告：此操作会删除所有数据和文件，请谨慎使用！

使用方法：
    cd backend
    python reset_db.py
"""
⋮----
# 添加backend目录到Python路径
BACKEND_ROOT = Path(__file__).resolve().parents[2]  # backend/
⋮----
def resolve_sqlite_path(db_url: str) -> Path | None
⋮----
"""Resolve the SQLite file path for the current DATABASE_URL."""
⋮----
raw_path = Path(db_url.replace("sqlite:///", "", 1))
⋮----
def get_database_display_path() -> str
⋮----
"""获取当前数据库的可读路径（优先显示SQLite绝对路径）"""
sqlite_path = resolve_sqlite_path(settings.DATABASE_URL)
⋮----
def confirm_reset()
⋮----
"""确认是否重置数据库和文件"""
⋮----
response = input("确认要继续吗？(输入 'YES' 继续): ")
⋮----
def drop_all_tables()
⋮----
"""删除所有表"""
⋮----
# 获取所有表名
⋮----
# SQLite特定的查询
result = conn.execute(text(
tables = [row[0] for row in result]
⋮----
# 删除所有表
⋮----
def clean_directory(directory: Path, dir_name: str)
⋮----
"""清理目录中的所有文件"""
⋮----
file_count = sum(1 for _ in directory.rglob('*') if _.is_file())
⋮----
# 删除目录中的所有内容
⋮----
def clean_all_files()
⋮----
"""清理所有文件"""
⋮----
def clean_legacy_database_files()
⋮----
"""删除项目内遗留数据库文件，避免多库歧义。"""
active_db_path = resolve_sqlite_path(settings.DATABASE_URL)
candidate_dirs = [
⋮----
seen_dirs = set()
removed = 0
⋮----
file_path = f.resolve()
⋮----
def main()
⋮----
"""主函数"""
# 确认操作
⋮----
# 1. 删除所有表
⋮----
# 2. 清理所有文件（含 data/processed/ 中间文件）
⋮----
# 3. 清理项目内遗留数据库文件（init_db 会重建当前主库）
⋮----
# 4. 重新初始化数据库
````

## File: backend/scripts/migration/create_default_version.py
````python
"""
创建默认标签配置版本
将当前的默认配置保存为不可修改的默认版本
"""
⋮----
# 添加backend目录到Python路径
⋮----
def create_default_version(db)
⋮----
"""创建默认版本快照"""
⋮----
# 1. 检查是否已存在默认版本
existing_default = db.query(LabelSchemaVersion).filter(
⋮----
# 2. 获取当前所有实体类型
entity_types = db.query(EntityType).all()
entity_types_data = []
⋮----
# 3. 获取当前所有关系类型
relation_types = db.query(RelationType).all()
relation_types_data = []
⋮----
# 4. 构建版本快照数据
schema_data = {
⋮----
"is_default": True,  # 标记为默认版本
"is_readonly": True  # 标记为只读（不可修改）
⋮----
# 5. 获取管理员用户ID
admin_user = db.query(User).filter(User.username == "admin").first()
created_by = admin_user.id if admin_user else None
⋮----
# 6. 创建版本记录
version = LabelSchemaVersion(
⋮----
is_active=True,  # 设置为活跃版本
⋮----
# 7. 打印版本内容摘要
⋮----
bbox = "✓" if et["supports_bbox"] else " "
⋮----
def main()
⋮----
"""主函数"""
⋮----
# 创建数据库会话
db = SessionLocal()
⋮----
version = create_default_version(db)
````

## File: backend/scripts/migration/migrate_dataset_assignment.py
````python
"""
数据集分配功能 - 数据库迁移脚本
执行 dataset_assignments 表的创建和索引添加
"""
⋮----
def run_migration()
⋮----
"""执行数据库迁移"""
# 从 DATABASE_URL 提取数据库路径
db_url = settings.DATABASE_URL
db_path = db_url.replace("sqlite:///", "")
migration_file = Path(__file__).parent / "migrations" / "add_dataset_assignment.sql"
⋮----
# 读取迁移脚本
⋮----
migration_sql = f.read()
⋮----
# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
⋮----
# 执行迁移脚本
⋮----
# 验证表是否创建
⋮----
result = cursor.fetchone()
⋮----
# 显示表结构
⋮----
columns = cursor.fetchall()
⋮----
# 显示索引
⋮----
indexes = cursor.fetchall()
````

## File: backend/scripts/run_test_summary.py
````python

````

## File: backend/scripts/test_db_connection.py
````python
"""
测试数据库连接和用户创建
"""
⋮----
# 创建测试数据库
TEST_DATABASE_URL = "sqlite:///./test_connection.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
⋮----
# 创建表
⋮----
# 创建用户
db = TestingSessionLocal()
⋮----
user_service = UserService(db)
⋮----
admin = user_service.create_user(
⋮----
# 验证用户存在
found_user = db.query(User).filter(User.username == "admin").first()
⋮----
# 测试认证
auth_user = user_service.authenticate("admin", "admin123")
⋮----
# 测试错误密码
auth_user = user_service.authenticate("admin", "wrongpassword")
⋮----
# 清理
````

## File: backend/scripts/test_index_performance.py
````python
"""
测试数据库索引性能
用于验证 add_task_query_indexes.sql 迁移脚本的效果

使用方法：
1. 先运行迁移脚本创建索引
2. 运行此脚本测试性能
"""
⋮----
# 添加项目根目录到 Python 路径
⋮----
def test_index_exists()
⋮----
"""测试索引是否存在"""
⋮----
result = conn.execute(text("""
⋮----
indexes = result.fetchall()
⋮----
expected_indexes = [
⋮----
found_indexes = [idx[0] for idx in indexes if idx[0]]
⋮----
if idx[0]:  # 跳过 None（自动创建的索引）
⋮----
# 验证必需的索引
missing = []
⋮----
def test_query_performance()
⋮----
"""测试查询性能"""
⋮----
db = next(get_db())
⋮----
# 获取任务总数
total_tasks = db.query(AnnotationTask).count()
⋮----
# 获取一个存在的 dataset_id
sample_task = db.query(AnnotationTask).first()
⋮----
dataset_id = sample_task.dataset_id
⋮----
# 测试 1: 按数据集和状态筛选
⋮----
start_time = time.time()
results = db.query(AnnotationTask).filter(
elapsed = (time.time() - start_time) * 1000
⋮----
# 测试 2: 按时间排序
⋮----
results = db.query(AnnotationTask).order_by(
⋮----
# 测试 3: 复杂查询（数据集 + 状态 + 排序）
⋮----
# 性能评估
⋮----
def test_explain_query_plan()
⋮----
"""测试查询计划，验证是否使用了索引"""
⋮----
# 获取一个示例 dataset_id
result = conn.execute(text("SELECT dataset_id FROM annotation_tasks LIMIT 1"))
row = result.fetchone()
⋮----
dataset_id = row[0]
⋮----
# 测试查询计划
queries = [
⋮----
result = conn.execute(text(f"EXPLAIN QUERY PLAN {query['sql']}"))
plan = result.fetchall()
⋮----
uses_index = False
⋮----
# 检查是否使用了我们创建的索引
⋮----
uses_index = True
⋮----
def main()
⋮----
"""主测试函数"""
⋮----
# 测试 1: 验证索引存在
⋮----
# 测试 2: 查询性能测试
⋮----
# 测试 3: 查询计划分析
````

## File: backend/services/__init__.py
````python
"""
服务层模块
"""
⋮----
__all__ = ['ExcelProcessingService', 'OffsetCorrectionService', 'CorrectionLog', 'DatasetService', 'TaskQueryService']
````

## File: backend/services/batch_annotation_service.py
````python
"""
批量标注服务
提供批量自动标注功能,支持异步执行和进度跟踪
"""
⋮----
logger = logging.getLogger(__name__)
⋮----
class BatchAnnotationService
⋮----
"""批量标注服务"""
⋮----
def __init__(self, db: Session)
⋮----
"""
        初始化服务
        
        Args:
            db: 数据库会话
        """
⋮----
"""
        创建批量标注任务
        
        Args:
            dataset_id: 数据集ID
            created_by: 创建人ID
            user_role: 用户角色
            task_ids: 指定要标注的任务ID列表（可选）
            
        Returns:
            BatchJob: 批量任务对象
        """
# 查询数据集
dataset = self.db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
⋮----
# 构建基础查询
query = self.db.query(AnnotationTask)\
⋮----
# 如果指定了任务ID列表，只查询这些任务
⋮----
query = query.filter(AnnotationTask.task_id.in_(task_ids))
⋮----
# 应用权限过滤（标注员只能标注分配给自己的任务）
⋮----
# 查询用户的数据集分配
assignment = self.db.query(DatasetAssignment).filter(
⋮----
# 如果有任务范围限制
⋮----
# 获取任务范围内的任务ID
all_tasks = self.db.query(AnnotationTask)\
⋮----
# 计算范围内的任务
start_idx = assignment.task_start_index - 1  # 转换为0-based索引
end_idx = assignment.task_end_index
range_tasks = all_tasks[start_idx:end_idx]
range_task_ids = [t.id for t in range_tasks]
⋮----
# 应用范围过滤
query = query.filter(AnnotationTask.id.in_(range_task_ids))
# 如果没有范围限制，标注员可以标注该数据集的所有任务
⋮----
# 统计任务数量
total_tasks = query.count()
⋮----
# 生成任务ID
job_id = f"batch-{uuid.uuid4().hex[:12]}"
⋮----
# 创建批量任务记录
batch_job = BatchJob(
⋮----
def get_batch_job(self, job_id: str) -> Optional[BatchJob]
⋮----
"""
        获取批量任务详情
        
        Args:
            job_id: 任务ID
            
        Returns:
            Optional[BatchJob]: 批量任务对象
        """
⋮----
"""
        更新批量任务状态
        
        Args:
            job_id: 任务ID
            status: 状态
            completed_tasks: 完成任务数
            failed_tasks: 失败任务数
            error_message: 错误信息
            
        Returns:
            Optional[BatchJob]: 更新后的批量任务对象
        """
batch_job = self.get_batch_job(job_id)
⋮----
# 更新状态
⋮----
# 计算进度
⋮----
# 更新时间戳
⋮----
"""
        执行批量标注(异步)
        
        Args:
            job_id: 任务ID
            user_id: 用户ID
            user_role: 用户角色
        """
⋮----
# 更新状态为处理中
⋮----
# 构建查询 - 获取创建批量任务时确定的任务列表
⋮----
# 如果指定了任务ID列表（选中标注），只处理这些任务
⋮----
# 应用权限过滤（与create_batch_job保持一致）
⋮----
start_idx = assignment.task_start_index - 1
⋮----
# 获取任务列表
tasks = query.all()
⋮----
completed_count = 0
failed_count = 0
⋮----
# 逐个处理任务
⋮----
# 标注单个任务
⋮----
# 记录失败
⋮----
# 更新进度
⋮----
# 更新最终状态
final_status = 'completed' if failed_count == 0 else 'completed_with_errors'
⋮----
# 批量任务失败
⋮----
def _annotate_single_task(self, task: AnnotationTask)
⋮----
"""
        标注单个任务
        
        Args:
            task: 标注任务对象
        """
# 获取语料
corpus = self.db.query(Corpus).filter(Corpus.id == task.corpus_id).first()
⋮----
# 检测图片类语料（仅含图片 Markdown，如 ![图片](ID_...)）无法进行文本实体抽取
corpus_text_stripped = (corpus.text or '').strip()
⋮----
# 更新任务状态
⋮----
# 1. 实体抽取
active_entity_types = LabelConfigCache.get_entity_types(self.db)
⋮----
entity_result = self.entity_agent.extract_entities(
⋮----
# 基于当前生效标签体系（active+reviewed）构建中英文映射
entity_label_map = self._build_entity_label_map()
relation_label_map = self._build_relation_label_map()
allowed_entity_labels = self._get_allowed_entity_labels()
allowed_relation_labels = self._get_allowed_relation_labels()
⋮----
# 保存实体
entity_id_map = {}  # 临时ID -> 数据库ID的映射
saved_count = 0
⋮----
normalized_label = self._normalize_entity_label(entity.label, entity_label_map)
⋮----
entity_confidence = getattr(entity, 'confidence', None)
text_entity = TextEntity(
⋮----
# 记录映射关系
⋮----
# 2. 关系抽取
# 直接使用ExtractedEntity对象列表（relation_agent依赖实体属性访问）
entities_for_relation = entity_result.entities
⋮----
active_relation_types = LabelConfigCache.get_relation_types(self.db)
relation_result = self.relation_agent.extract_relations(
⋮----
# 保存关系
⋮----
# 映射临时ID到数据库ID
from_entity_id = entity_id_map.get(relation.from_id)
to_entity_id = entity_id_map.get(relation.to_id)
⋮----
normalized_relation_type = self._normalize_relation_label(
⋮----
text_relation = Relation(
⋮----
# 更新任务状态为完成
⋮----
# 标注失败
⋮----
def _build_entity_label_map(self) -> Dict[str, str]
⋮----
"""构建实体标签映射：英文名/中文名（大小写不敏感） -> 中文名。"""
entity_types = LabelConfigCache.get_entity_types(self.db)
label_map: Dict[str, str] = {}
⋮----
target_label = (entity_type.type_name_zh or '').strip()
⋮----
normalized_key = self._normalize_label_key(source_label)
⋮----
@staticmethod
    def _normalize_label_key(label: Optional[str]) -> Optional[str]
⋮----
"""标准化标签键（去空格+小写）用于匹配。"""
⋮----
normalized = label.strip()
⋮----
def _normalize_entity_label(self, label: str, label_map: Dict[str, str]) -> str
⋮----
"""将实体标签标准化为当前生效标签体系中的中文标签。"""
normalized_key = self._normalize_label_key(label)
⋮----
def _build_relation_label_map(self) -> Dict[str, str]
⋮----
"""构建关系标签映射：英文名/中文名（大小写不敏感） -> 中文名。"""
relation_types = LabelConfigCache.get_relation_types(self.db)
⋮----
target_label = (relation_type.type_name_zh or '').strip()
⋮----
def _normalize_relation_label(self, label: str, label_map: Dict[str, str]) -> str
⋮----
"""将关系标签标准化为当前生效标签体系中的中文标签。"""
⋮----
def _get_allowed_entity_labels(self) -> set[str]
⋮----
"""获取允许落库的实体中文标签集合。"""
⋮----
def _get_allowed_relation_labels(self) -> set[str]
⋮----
"""获取允许落库的关系中文标签集合。"""
⋮----
def cancel_batch_job(self, job_id: str) -> bool
⋮----
"""
        取消批量任务
        
        Args:
            job_id: 任务ID
            
        Returns:
            bool: 是否取消成功
        """
⋮----
# 只能取消pending或processing状态的任务
⋮----
# 更新状态为已取消
⋮----
def get_batch_job_statistics(self, job_id: str) -> Optional[Dict[str, Any]]
⋮----
"""
        获取批量任务统计信息
        
        Args:
            job_id: 任务ID
            
        Returns:
            Optional[Dict]: 统计信息
        """
⋮----
# 计算耗时
duration = None
⋮----
end_time = batch_job.completed_at or datetime.utcnow()
duration = (end_time - batch_job.started_at).total_seconds()
````

## File: backend/services/data_parser.py
````python
logger = logging.getLogger(__name__)
⋮----
class DataParser
⋮----
"""解析表格数据，通过处理器配置驱动字段映射"""
⋮----
def __init__(self, processor_name: str = 'kf')
⋮----
def parse_json_file(self, file_path: str) -> List[Dict]
⋮----
"""解析JSON文件"""
⋮----
data = json.load(f)
⋮----
table_data = data.get('table_data', [])
⋮----
def extract_entities(self, record: Dict, data_source: str = None) -> Dict
⋮----
"""从单条记录提取实体，委托给处理器"""
⋮----
def detect_data_version(self, record: Dict) -> str
⋮----
"""
        检测数据版本

        Returns:
            'v2': 新版本（包含所有字段）
            'v1': 老版本（缺少所有字段）
            'v1.5': 部分缺失
        """
required_fields = list(self.processor.default_values.keys())
missing_count = sum(1 for f in required_fields if not record.get(f))
⋮----
def batch_parse(self, file_paths: List[str]) -> List[Dict]
⋮----
"""批量解析多个JSON文件"""
all_entities = []
⋮----
records = self.parse_json_file(file_path)
⋮----
entities = self.extract_entities(record)
⋮----
def parse_with_report(self, file_path: str) -> tuple[List[Dict], Dict]
⋮----
"""解析JSON文件并生成版本统计报告"""
⋮----
stats = {
⋮----
version = self.detect_data_version(record)
````

## File: backend/services/dataset_assignment_service.py
````python
"""
数据集分配服务
处理数据集级别的任务分配逻辑
"""
⋮----
class DatasetAssignmentService
⋮----
"""数据集分配服务"""
⋮----
def __init__(self, db: Session)
⋮----
"""
        整体分配数据集
        
        Args:
            dataset_id: 数据集ID
            user_id: 用户ID
            role: 角色（annotator/reviewer）
            assigned_by: 分配人ID
        
        Returns:
            DatasetAssignment: 分配记录
        """
# 验证数据集存在
dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
⋮----
# 验证用户存在
user = self.db.query(User).filter(User.id == user_id).first()
⋮----
# 检查是否已经有活跃分配
existing = self.db.query(DatasetAssignment)\
⋮----
# 检查是否有其他用户的整体分配（同角色）
existing_full = self.db.query(DatasetAssignment)\
⋮----
existing_user = self.db.query(User).filter(User.id == existing_full.user_id).first()
⋮----
# 检查是否有任何范围分配（同角色）
existing_range = self.db.query(DatasetAssignment)\
⋮----
# 创建分配记录（task_start_index 和 task_end_index 为 NULL 表示全部）
assignment = DatasetAssignment(
⋮----
"""
        范围分配数据集
        
        Args:
            dataset_id: 数据集ID
            user_id: 用户ID
            role: 角色
            start_index: 起始任务索引（从1开始）
            end_index: 结束任务索引（包含）
            assigned_by: 分配人ID
        
        Returns:
            DatasetAssignment: 分配记录
        """
# 验证范围有效性
⋮----
# 获取数据集任务总数
total_tasks = self.db.query(AnnotationTask)\
⋮----
# 检查范围是否重叠
⋮----
# 创建分配记录
⋮----
"""
        检查任务范围是否与现有分配重叠
        
        Args:
            dataset_id: 数据集ID
            role: 角色
            start_index: 起始索引
            end_index: 结束索引
            exclude_assignment_id: 排除的分配ID（用于更新时）
        
        Raises:
            ValueError: 如果范围重叠
        """
query = self.db.query(DatasetAssignment)\
⋮----
query = query.filter(DatasetAssignment.id != exclude_assignment_id)
⋮----
# 查找重叠的分配
overlapping = query.filter(
⋮----
# 新范围的起始点在现有范围内
⋮----
# 新范围的结束点在现有范围内
⋮----
# 新范围包含现有范围
⋮----
# 整体分配（NULL范围）
⋮----
user = self.db.query(User).filter(User.id == overlapping.user_id).first()
⋮----
"""
        自动平均分配数据集
        
        Args:
            dataset_id: 数据集ID
            user_ids: 用户ID列表
            role: 角色
            assigned_by: 分配人ID
        
        Returns:
            List[DatasetAssignment]: 分配记录列表
        """
⋮----
# 验证所有用户存在
users = self.db.query(User).filter(User.id.in_(user_ids)).all()
⋮----
# 获取任务总数
⋮----
# 计算每人分配的任务数
num_users = len(user_ids)
tasks_per_user = total_tasks // num_users
remainder = total_tasks % num_users
⋮----
assignments = []
current_index = 1
⋮----
# 前面的用户多分配1个任务（处理余数）
count = tasks_per_user + (1 if i < remainder else 0)
end_index = current_index + count - 1
⋮----
assignment = self.assign_range(
⋮----
current_index = end_index + 1
⋮----
"""
        检查是否可以取消分配
        
        Args:
            assignment_id: 分配ID
        
        Returns:
            (是否可以取消, 原因说明, 统计信息)
        """
assignment = self.db.query(DatasetAssignment).filter(
⋮----
# 获取该分配范围内的任务
tasks = self._get_tasks_in_range(
⋮----
# 统计任务状态
completed_count = sum(1 for t in tasks if t.status == 'completed')
in_review_count = sum(1 for t in tasks if t.status == 'in_review')
processing_count = sum(1 for t in tasks if t.status == 'processing')
pending_count = sum(1 for t in tasks if t.status == 'pending')
⋮----
stats = {
⋮----
# 规则1：如果有任务已完成或在复核中，不能直接取消
⋮----
# 规则2：如果有任务正在处理中，给出警告但允许
⋮----
# 规则3：所有任务都是pending，可以安全取消
⋮----
"""
        取消分配
        
        Args:
            dataset_id: 数据集ID
            user_id: 用户ID
            role: 角色
            force: 强制取消（跳过检查）
        
        Returns:
            bool: 是否成功
        """
assignment = self.db.query(DatasetAssignment)\
⋮----
# 检查是否可以取消
⋮----
# 返回详细信息，让API层决定如何响应
⋮----
# 删除分配记录
⋮----
"""
        获取指定范围内的任务
        
        Args:
            dataset_id: 数据集ID
            start_index: 起始索引（None表示从头开始）
            end_index: 结束索引（None表示到末尾）
        
        Returns:
            List[AnnotationTask]: 任务列表
        """
query = self.db.query(AnnotationTask)\
⋮----
# 如果指定了范围，进行过滤
⋮----
# 获取所有任务，然后按索引切片
all_tasks = query.all()
# 索引从1开始，所以需要减1
⋮----
# 返回所有任务
⋮----
"""
        转移分配
        
        Args:
            dataset_id: 数据集ID
            old_user_id: 原用户ID
            new_user_id: 新用户ID
            role: 角色
            transfer_mode: 转移模式 ('all', 'remaining', 'completed')
            transfer_reason: 转移原因
            transferred_by: 转移操作人
        
        Returns:
            dict: 转移结果
        """
# 验证旧分配存在
old_assignment = self.db.query(DatasetAssignment)\
⋮----
# 验证新用户存在
new_user = self.db.query(User).filter(User.id == new_user_id).first()
⋮----
# 验证新旧用户不同
⋮----
# 根据转移模式执行不同的逻辑
⋮----
# 创建新分配，保持相同的任务范围
new_assignment = DatasetAssignment(
⋮----
# 禁用旧分配（不删除，保留历史）
⋮----
# 统计转移的任务数
transferred_tasks = self._count_tasks_in_range(
⋮----
# 获取旧用户信息
old_user = self.db.query(User).filter(User.id == old_user_id).first()
⋮----
# TODO: 实现部分转移逻辑
# 这需要更复杂的范围计算，暂时不实现
⋮----
"""
        统计指定范围内的任务数量
        
        Args:
            dataset_id: 数据集ID
            start_index: 起始索引
            end_index: 结束索引
        
        Returns:
            int: 任务数量
        """
⋮----
# 整体分配，返回所有任务数
⋮----
# 范围分配
⋮----
"""
        获取数据集的所有分配
        
        Args:
            dataset_id: 数据集ID
            include_inactive: 是否包含不活跃的分配
        
        Returns:
            List[DatasetAssignment]: 分配列表
        """
⋮----
query = query.filter(DatasetAssignment.is_active == True)
⋮----
"""
        获取用户分配的数据集列表
        
        Args:
            user_id: 用户ID
            role: 角色筛选（可选）
        
        Returns:
            List[Dataset]: 数据集列表
        """
query = self.db.query(Dataset)\
⋮----
query = query.filter(DatasetAssignment.role == role)
⋮----
"""
        检查用户是否有权限访问数据集
        
        Args:
            user_id: 用户ID
            dataset_id: 数据集ID
            required_role: 需要的角色 ('annotator', 'reviewer', 'view')
        
        Returns:
            bool: 是否有权限
        """
# 检查用户角色
⋮----
# 管理员有所有权限
⋮----
# 浏览员只能查看
⋮----
# 检查数据集分配
⋮----
"""
        获取用户在数据集中的任务范围
        
        Args:
            user_id: 用户ID
            dataset_id: 数据集ID
            role: 角色
        
        Returns:
            Optional[Tuple[start, end]]: 任务范围，None表示没有分配
        """
````

## File: backend/services/dataset_service.py
````python
"""
数据集管理服务
负责数据集的创建、查询、删除和导出
"""
⋮----
class DatasetService
⋮----
"""数据集管理服务"""
⋮----
def __init__(self, db: Session)
⋮----
"""
        初始化服务
        
        Args:
            db: 数据库会话
        """
⋮----
"""
        创建数据集
        
        Args:
            name: 数据集名称
            description: 数据集描述
            corpus_ids: 语料ID列表
            created_by: 创建人ID
            label_schema_version_id: 标签体系版本ID（可选，默认使用当前活跃版本）
            
        Returns:
            Dataset: 创建的数据集对象
        """
# 生成数据集ID
dataset_id = f"ds-{uuid.uuid4().hex[:12]}"
⋮----
# 如果未指定标签体系版本，使用当前活跃版本
⋮----
active_version = self.db.query(LabelSchemaVersion)\
⋮----
label_schema_version_id = active_version.id
⋮----
# 创建数据集
dataset = Dataset(
⋮----
self.db.flush()  # 获取dataset.id
⋮----
# 关联语料
⋮----
# 验证语料是否存在
corpus = self.db.query(Corpus).filter(Corpus.id == corpus_id).first()
⋮----
# 创建关联
association = DatasetCorpus(
⋮----
# 为每个语料创建标注任务
task_id = f"task-{uuid.uuid4().hex[:12]}"
task = AnnotationTask(
⋮----
def get_dataset(self, dataset_id: str) -> Optional[Dataset]
⋮----
"""
        获取数据集详情
        
        Args:
            dataset_id: 数据集ID
            
        Returns:
            Dataset: 数据集对象，如果不存在返回None
        """
dataset = self.db.query(Dataset)\
⋮----
"""
        获取数据集列表
        
        Args:
            page: 页码（从1开始）
            page_size: 每页数量
            name: 数据集名称筛选（可选）
            created_by: 创建人ID（可选，用于筛选）
            
        Returns:
            tuple[List[Dataset], int]: (数据集列表, 总数)
        """
query = self.db.query(Dataset)
⋮----
# 筛选条件
⋮----
query = query.filter(Dataset.name.like(f"%{name}%"))
⋮----
query = query.filter(Dataset.created_by == created_by)
⋮----
# 获取总数
total = query.count()
⋮----
# 分页
skip = (page - 1) * page_size
datasets = query.order_by(Dataset.created_at.desc())\
⋮----
def delete_dataset(self, dataset_id: str) -> bool
⋮----
"""
        删除数据集（级联删除关联的任务和标注）
        
        Args:
            dataset_id: 数据集ID
            
        Returns:
            bool: 是否删除成功
        """
⋮----
# SQLAlchemy会自动级联删除关联的记录（因为设置了cascade="all, delete-orphan"）
⋮----
"""
        向已有数据集添加语料并创建标注任务（自动去重）
        
        Args:
            dataset_id: 数据集ID（字符串形式）
            corpus_ids: 要添加的语料ID列表
            
        Returns:
            Dict: {"added": 新增任务数, "skipped": 重复跳过数}
        """
⋮----
# 查询已关联的语料ID集合（用于去重）
existing_corpus_ids: set = {
⋮----
added = 0
skipped = 0
⋮----
# 创建标注任务
⋮----
def remove_task(self, dataset_id: str, task_id: str) -> bool
⋮----
"""
        从数据集中删除一个标注任务及其关联语料绑定

        Args:
            dataset_id: 数据集ID（字符串形式）
            task_id: 任务ID（字符串形式，如 task-xxxx）

        Returns:
            bool: 成功则True，任务不存在则False
        """
⋮----
task = self.db.query(AnnotationTask)\
⋮----
corpus_id = task.corpus_id
⋮----
# 删除任务（cascade 会自动删除 text_entities / relations / image_entities）
⋮----
# 删除数据集-语料关联
assoc = self.db.query(DatasetCorpus)\
⋮----
def get_dataset_statistics(self, dataset_id: str) -> Dict[str, Any]
⋮----
"""
        获取数据集统计信息
        
        Args:
            dataset_id: 数据集ID
            
        Returns:
            Dict: 统计信息
        """
dataset = self.get_dataset(dataset_id)
⋮----
# 统计任务状态
task_stats = self.db.query(
⋮----
status_counts = {status: count for status, count in task_stats}
⋮----
# 统计总数
total_tasks = sum(status_counts.values())
completed_tasks = status_counts.get('completed', 0)
⋮----
# 统计实体和关系数量
entity_count = self.db.query(func.count(TextEntity.id))\
⋮----
relation_count = self.db.query(func.count(Relation.id))\
⋮----
"""
        导出数据集为JSONL格式
        
        Args:
            dataset_id: 数据集ID
            output_path: 导出路径（可选，默认为data/exports目录）
            status_filter: 状态筛选（可选，如['completed', 'reviewed']）
            
        Returns:
            Optional[str]: 导出文件路径，如果数据集不存在返回None
        """
⋮----
# 查询任务
query = self.db.query(AnnotationTask)\
⋮----
query = query.filter(AnnotationTask.status.in_(status_filter))
⋮----
tasks = query.all()
⋮----
# 生成JSONL内容
lines = []
⋮----
# 获取语料
corpus = self.db.query(Corpus)\
⋮----
# 获取实体
entities = self.db.query(TextEntity)\
⋮----
# 获取关系
relations = self.db.query(Relation)\
⋮----
# 仅导出文本实体与文本关系
sorted_entities = sorted(
⋮----
entity_id_map = {
⋮----
export_entities = []
⋮----
export_relations = []
⋮----
quick_response_id = self._extract_quick_response_id(corpus)
sample_id = f"entity_text_{quick_response_id}_{sample_index:03d}"
⋮----
# 构建文本导出记录
record = {
⋮----
# 确定输出路径
⋮----
output_path = str(settings.EXPORT_DIR / f"{dataset_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")
⋮----
# 确保目录存在
output_dir = Path(output_path).parent
⋮----
# 写入文件
⋮----
@staticmethod
    def _extract_quick_response_id(corpus: Corpus) -> str
⋮----
"""从语料中提取快反编号，提取失败时回退到text_id。"""
text_id = (corpus.text_id or "").strip()
⋮----
fr_match = re.search(r"FR\d+", text_id, re.IGNORECASE)
⋮----
@staticmethod
    def _build_data_source(corpus: Corpus) -> str
⋮----
"""优先使用来源文件名+行号构建数据来源标识。"""
source_file = (corpus.source_file or "").strip()
source_field = (corpus.source_field or "").strip()
⋮----
file_stem = Path(source_file).stem or source_file
````

## File: backend/services/document_processor.py
````python
"""
Excel文件处理服务
支持WPS Excel和Microsoft Excel格式的图片提取
"""
⋮----
logger = logging.getLogger(__name__)
⋮----
class DocumentProcessor
⋮----
"""Excel文件处理器"""
⋮----
def __init__(self, processor_name: str = 'kf')
⋮----
"""
        初始化文档处理器

        Args:
            processor_name: 处理器名称 ('kf' / 'qms' / 'failure_case')
        """
⋮----
# 目录已在 config.py 启动时创建，此处仅做保险
⋮----
# 加载已处理文件的哈希记录
⋮----
def _load_hashes(self) -> Dict[str, Dict]
⋮----
"""加载文件哈希记录，兼容旧版共用 file_hashes.json 的数据"""
⋮----
data = json.load(f)
⋮----
# 兼容旧版：尝试从根目录 file_hashes.json 迁移本处理器的记录
legacy_hash_file = settings.UPLOAD_DIR / "file_hashes.json"
⋮----
all_data = json.load(f)
migrated = {k: v for k, v in all_data.items()
⋮----
# 写入新位置，下次直接读
⋮----
def _save_hashes(self)
⋮----
"""保存文件哈希记录"""
⋮----
def calculate_file_hash(self, file_path: Path) -> str
⋮----
"""计算文件的SHA256哈希值"""
sha256_hash = hashlib.sha256()
⋮----
def check_duplicate(self, file_hash: str, filename: str) -> Optional[Dict]
⋮----
"""检查文件是否已处理过"""
⋮----
record = self.file_hashes[file_hash]
⋮----
def extract_data_source(self, filename: str) -> str
⋮----
"""从文件名提取数据源"""
base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
sanitized_name = sanitize_filename(base_name)
⋮----
def process_excel(self, file_path: Path, original_filename: str) -> Dict
⋮----
"""处理Excel文件"""
⋮----
# 1. 计算文件哈希
file_hash = self.calculate_file_hash(file_path)
⋮----
# 2. 检查是否重复
duplicate_record = self.check_duplicate(file_hash, original_filename)
⋮----
# 3. 规范化文件名
sanitized_name = sanitize_filename(original_filename)
base_name = sanitized_name.rsplit('.', 1)[0]
⋮----
# 4. 提取数据源
data_source = self.extract_data_source(original_filename)
⋮----
# 5. 设置输出目录: data/processed/{processor_name}/{data_source}/
output_dir = self.processed_dir / self.processor_name / data_source
⋮----
# 6. 通过处理器解析Excel文件
⋮----
result = self.processor.parse_excel(str(file_path), str(output_dir))
⋮----
# 7. 记录处理信息
⋮----
process_record = {
⋮----
# 8. 保存哈希记录
⋮----
def reload_hashes(self)
⋮----
"""重新加载哈希记录"""
⋮----
def _get_failure_case_record_count(self, record: Dict) -> int
⋮----
"""从语料库中统计品质案例的实际记录数。"""
source_file = (record.get('original_filename') or '').strip()
⋮----
db = SessionLocal()
⋮----
def get_processed_files(self) -> list
⋮----
"""获取已处理文件列表"""
result = []
⋮----
output_dir = Path(record['output_dir'])
record_count = 0
⋮----
record_count = self._get_failure_case_record_count(record)
⋮----
json_files = list(sorted(output_dir.glob('page_*.json')))
````

## File: backend/services/dynamic_prompt_builder.py
````python
"""
动态Prompt构建器
根据数据库中的标签配置动态生成Agent的Prompt
"""
⋮----
# 默认配置(降级使用)
DEFAULT_ENTITY_TYPES_PROMPT = """
⋮----
DEFAULT_RELATION_TYPES_PROMPT = """
⋮----
class DynamicPromptBuilder
⋮----
"""
    动态Prompt构建器
    
    根据数据库中的标签配置生成Agent的Prompt
    """
⋮----
@staticmethod
    def build_entity_types_section(entity_types: List[EntityType]) -> str
⋮----
"""
        构建实体类型定义部分
        
        Args:
            entity_types: 实体类型列表
            
        Returns:
            str: 实体类型定义的Prompt文本
        """
⋮----
sections = []
⋮----
# 标题行
section = f"{idx}. **{et.type_name_zh}** ({et.type_name})"
⋮----
# 添加标准定义(优先使用LLM生成的定义)
⋮----
# 添加示例
⋮----
examples = json.loads(et.examples) if isinstance(et.examples, str) else et.examples
⋮----
# 最多显示5个示例
example_str = ', '.join(examples[:5])
⋮----
# 添加类别辨析
⋮----
# 添加边界框支持说明
⋮----
@staticmethod
    def build_relation_types_section(relation_types: List[RelationType]) -> str
⋮----
"""
        构建关系类型定义部分
        
        Args:
            relation_types: 关系类型列表
            
        Returns:
            str: 关系类型定义的Prompt文本
        """
⋮----
section = f"{idx}. **{rt.type_name_zh}** ({rt.type_name})"
⋮----
# 添加方向规则
⋮----
examples = json.loads(rt.examples) if isinstance(rt.examples, str) else rt.examples
⋮----
# 显示第一个示例
⋮----
"""
        构建完整的实体抽取Prompt
        
        Args:
            text_id: 文本ID
            text: 文本内容
            entity_types: 实体类型列表
            
        Returns:
            str: 完整的实体抽取Prompt
        """
entity_types_section = DynamicPromptBuilder.build_entity_types_section(entity_types)
⋮----
prompt = f"""你是一个专业的品质失效案例实体抽取专家。请从给定文本中精准抽取实体。
⋮----
"""
        构建完整的关系抽取Prompt
        
        Args:
            text_id: 文本ID
            text: 文本内容
            entities: 已标注的实体列表
            relation_types: 关系类型列表
            
        Returns:
            str: 完整的关系抽取Prompt
        """
relation_types_section = DynamicPromptBuilder.build_relation_types_section(relation_types)
⋮----
entity_list_str = "\n".join([
⋮----
prompt = f"""你是一个专业的品质失效案例关系抽取专家。请基于文本与已标注实体识别关系。
⋮----
"""
        构建Prompt预览
        
        Args:
            entity_types: 实体类型列表
            relation_types: 关系类型列表
            
        Returns:
            dict: Prompt预览信息
        """
entity_section = DynamicPromptBuilder.build_entity_types_section(entity_types)
relation_section = DynamicPromptBuilder.build_relation_types_section(relation_types)
⋮----
# 统计审核状态
entity_reviewed = sum(1 for et in entity_types if et.is_reviewed)
entity_pending = len(entity_types) - entity_reviewed
⋮----
relation_reviewed = sum(1 for rt in relation_types if rt.is_reviewed)
relation_pending = len(relation_types) - relation_reviewed
````

## File: backend/services/excel_processing.py
````python
"""
Excel处理服务
提取WPS Excel内嵌图片、解析表格数据、生成语料记录
"""
⋮----
CANONICAL_SECOND_FIELD = '客户/发生工程/供应商'
SECOND_FIELD_ALIASES = [
⋮----
def _normalize_header_name(name: str) -> str
⋮----
"""统一列名比较口径：去首尾空白并移除中间空白。"""
⋮----
class ExcelProcessingService
⋮----
"""Excel文件处理服务"""
⋮----
def __init__(self, db: Session)
⋮----
"""
        处理Excel文件，提取图片和文本数据
        
        Args:
            xlsx_path: Excel文件路径
            source_filename: 原始文件名
            
        Returns:
            处理结果字典，包含语料ID列表、图片数量、统计信息
        """
# 1. 提取图片
image_mapping = self.extract_wps_excel_images(xlsx_path, source_filename)
⋮----
# 2. 读取Excel数据
df = pd.read_excel(xlsx_path, engine='openpyxl')
⋮----
df = self._normalize_failure_case_columns(df)
⋮----
# 3. 校验必要列，拒绝格式不符的文件
REQUIRED_COLUMNS = [
normalized_to_actual = {
missing = [
has_second_field = _normalize_header_name(CANONICAL_SECOND_FIELD) in normalized_to_actual
⋮----
detail = []
⋮----
# 4. 转换DISPIMG公式为Markdown格式
df = self._convert_dispimg_in_dataframe(df)
⋮----
# 4. 生成语料记录
corpus_ids = []
total_sentences = 0
⋮----
# 为每一行的每个字段生成语料
⋮----
text = str(cell_value)
⋮----
# 分句处理
sentences = self._split_text_to_sentences(text)
⋮----
# 提取图片引用
image_refs = self._extract_image_paths(sentence)
⋮----
# 创建语料记录
corpus = self._create_corpus_record(
⋮----
source_row=int(row_idx) + 2,  # Excel行号从1开始，加上表头
⋮----
def _normalize_failure_case_columns(self, df: pd.DataFrame) -> pd.DataFrame
⋮----
"""将品质案例表头中的同义字段统一为标准字段名。"""
alias_map = {
⋮----
rename_map = {}
second_field_candidates = []
⋮----
normalized = _normalize_header_name(col)
⋮----
df = df.rename(columns=rename_map)
⋮----
# 若多个同义列同时存在，按从左到右取第一个非空值进行合并。
⋮----
second_cols = [c for c in df.columns if c == CANONICAL_SECOND_FIELD]
merged = df[second_cols].bfill(axis=1).iloc[:, 0]
dedup = df.loc[:, df.columns != CANONICAL_SECOND_FIELD]
df = pd.concat([dedup, merged.rename(CANONICAL_SECOND_FIELD)], axis=1)
⋮----
"""
        从WPS Excel文件中提取内嵌图片
        
        WPS Excel使用特殊的cellimages.xml存储图片信息：
        1. cellimages.xml: 包含图片名称(如ID_XXX)和关系ID(rId)的映射
        2. cellimages.xml.rels: 包含关系ID和实际图片路径的映射
        
        Args:
            xlsx_path: Excel文件路径
            source_filename: 原始文件名（用于组织输出目录）
            
        Returns:
            图片名称到文件路径的映射字典 {image_name: file_path}
        """
# 创建输出目录
file_stem = Path(source_filename).stem
out_dir = settings.IMAGE_DIR / file_stem
⋮----
image_mapping = {}
⋮----
# 检查cellimages.xml是否存在
⋮----
# 1. 解析 cellimages.xml 得到 <name, rId>
root = ET.fromstring(z.read('xl/cellimages.xml'))
ns = {
⋮----
name2rid = {}
⋮----
cNvPr = pic.find('.//xdr:cNvPr', ns)
blip = pic.find('.//a:blip', ns)
⋮----
name = cNvPr.get('name')
rid = blip.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
⋮----
# 2. 解析 .rels 得到 <rId, 真实路径>
rel_root = ET.fromstring(z.read('xl/_rels/cellimages.xml.rels'))
rid2path = {c.get('Id'): c.get('Target') for c in rel_root}
⋮----
# 3. 合并映射并导出图片
⋮----
img_path = 'xl/' + rid2path[rid]
ext = os.path.splitext(img_path)[1] or '.png'
⋮----
# 读取图片数据
⋮----
img_data = z.read(img_path)
⋮----
# 使用存储服务保存图片（支持本地/MinIO）
relative_path = f"{file_stem}/{name}{ext}"
⋮----
content_type=f'image/{ext[1:]}'  # 去掉点号
⋮----
def _convert_dispimg_in_dataframe(self, df: pd.DataFrame) -> pd.DataFrame
⋮----
"""
        将DataFrame中的DISPIMG公式转换为Markdown图片格式
        
        WPS Excel中的图片显示为公式: =DISPIMG("ID_XXX",数字)
        转换为Markdown格式: ![图片](ID_XXX)
        
        Args:
            df: 原始DataFrame
            
        Returns:
            转换后的DataFrame
        """
⋮----
def _convert_dispimg_to_markdown(self, text: str) -> str
⋮----
"""
        将WPS图片函数转换为Markdown图片格式
        
        Args:
            text: 包含DISPIMG公式的文本
            
        Returns:
            转换后的文本
        """
# 匹配 =DISPIMG("ID_XXX",数字) 并替换成 ![图片](ID_XXX)
pattern = r'=DISPIMG\("([A-Za-z0-9_]+)",\d+\)'
result = re.sub(pattern, r'![图片](\1)', text, flags=re.I)
⋮----
def _extract_image_paths(self, text: str) -> List[str]
⋮----
"""
        从文本中提取Markdown格式的图片引用
        
        匹配格式: ![图片](ID_XXX)
        
        Args:
            text: 包含Markdown图片引用的文本
            
        Returns:
            图片名称列表，如 ['ID_XXX', ...]
        """
pattern = r'!\[图片\]\(([A-Za-z0-9_]+)\)'
⋮----
def _split_text_to_sentences(self, text: str) -> List[str]
⋮----
"""
        将单元格文本作为一个完整句子进行清洗

        处理规则：
        1. 删除换行符影响（按空白统一处理）
        2. 清理多余空格（保留单个空格，删除首尾空格和连续空格）
        3. 不再按标点或序号进一步分句
        
        Args:
            text: 原始文本
            
        Returns:
            句子列表
        """
cleaned_text = re.sub(r'\s+', ' ', text).strip()
⋮----
"""
        创建语料记录并关联图片
        
        Args:
            text: 文本内容
            source_file: 源文件名
            source_row: 源文件行号
            source_field: 源字段名
            text_type: 文本类型（字段分类）
            image_refs: 图片引用列表
            image_mapping: 图片名称到路径的映射
            
        Returns:
            创建的Corpus对象
        """
# 生成唯一ID
text_id = f"corpus_{uuid.uuid4().hex[:16]}"
⋮----
corpus = Corpus(
⋮----
self.db.flush()  # 获取corpus.id
⋮----
# 创建关联的图片记录
⋮----
image_id = f"img_{uuid.uuid4().hex[:16]}"
⋮----
# 获取图片文件路径
file_path = image_mapping[img_name]
full_path = settings.IMAGE_DIR / file_path
⋮----
# 获取图片尺寸（可选）
⋮----
image = Image(
⋮----
def _get_image_dimensions(self, image_path: Path) -> Tuple[Optional[int], Optional[int]]
⋮----
"""
        获取图片尺寸
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            (width, height) 元组，如果无法获取则返回 (None, None)
        """
⋮----
def validate_excel_file(self, xlsx_path: str, required_columns: List[str] = None) -> Dict
⋮----
"""
        验证Excel文件格式
        
        Args:
            xlsx_path: Excel文件路径
            required_columns: 必需的列名列表（可选）
            
        Returns:
            验证结果字典
        """
⋮----
# 检查文件是否存在
⋮----
# 检查文件扩展名
⋮----
# 尝试读取Excel文件
⋮----
# 检查是否为空
⋮----
# 检查必需列
⋮----
missing_columns = [col for col in required_columns if col not in df.columns]
````

## File: backend/services/export_service.py
````python
"""
数据导出服务
实现标注数据的导出功能
"""
⋮----
class ExportService
⋮----
"""数据导出服务类"""
⋮----
def __init__(self, db: Session)
⋮----
"""
        导出数据集为JSONL格式
        
        Args:
            dataset_id: 数据集ID
            status_filter: 状态筛选列表（如['approved', 'completed']）
            text_type_filter: 句子分类筛选列表
            train_test_split: 训练集比例（0-1之间），如0.8表示80%训练集，20%测试集
            random_seed: 随机种子
        
        Returns:
            Dict: 包含导出数据的字典
                - train_data: 训练集数据（如果指定了split）
                - test_data: 测试集数据（如果指定了split）
                - all_data: 所有数据（如果未指定split）
                - total_count: 总记录数
                - train_count: 训练集记录数
                - test_count: 测试集记录数
        """
# 查询数据集
dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
⋮----
# 查询标注任务
query = self.db.query(AnnotationTask).filter(
⋮----
# 状态筛选
⋮----
query = query.filter(AnnotationTask.status.in_(status_filter))
⋮----
tasks = query.all()
⋮----
# 构建导出数据
export_records = []
⋮----
# 查询语料
corpus = self.db.query(Corpus).filter(
⋮----
# 句子分类筛选
⋮----
# 查询当前版本的实体和关系
text_entities = self.db.query(TextEntity).filter(
⋮----
image_entities = self.db.query(ImageEntity).filter(
⋮----
relations = self.db.query(Relation).filter(
⋮----
# 构建记录
record = self._build_export_record(
⋮----
# 训练集/测试集划分
⋮----
# 设置随机种子
⋮----
# 随机打乱
⋮----
# 划分
split_index = int(len(export_records) * train_test_split)
train_data = export_records[:split_index]
test_data = export_records[split_index:]
⋮----
"""
        构建单条导出记录
        
        Args:
            corpus: 语料记录
            text_entities: 文本实体列表
            image_entities: 图片实体列表
            relations: 关系列表
        
        Returns:
            Dict: 导出记录
        """
# 构建文本实体
entities = []
⋮----
# 构建关系（仅文本实体之间的关系）
text_entity_ids = {e.entity_id for e in text_entities}
text_relations = []
⋮----
# 只包含文本实体之间的关系
⋮----
# 构建图片实体
images = []
image_entity_map = {}  # 映射图片实体ID到新ID
⋮----
# 查询图片信息
image = self.db.query(Image).filter(
⋮----
# 生成新的图片实体ID（从100开始，避免与文本实体ID冲突）
new_id = 100 + idx
⋮----
# 构建边界框
bbox = None
⋮----
bbox = {
⋮----
# 构建图片关系（文本实体到图片实体的关系）
image_entity_ids = {e.entity_id for e in image_entities}
image_relations = []
⋮----
# 文本实体 -> 图片实体
⋮----
# 图片实体 -> 文本实体
⋮----
# 构建完整记录
record = {
⋮----
"""
        将数据导出为JSONL文件
        
        Args:
            data: 导出数据列表
            output_path: 输出文件路径
        """
⋮----
"""
        获取导出统计信息
        
        Args:
            dataset_id: 数据集ID
            status_filter: 状态筛选列表
        
        Returns:
            Dict: 统计信息
        """
⋮----
# 统计
total_tasks = len(tasks)
total_entities = 0
total_relations = 0
total_images = 0
text_type_distribution = {}
⋮----
# 统计实体
entity_count = self.db.query(TextEntity).filter(
⋮----
# 统计关系
relation_count = self.db.query(Relation).filter(
⋮----
# 统计图片
image_count = self.db.query(ImageEntity).filter(
⋮----
# 统计句子分类分布
````

## File: backend/services/graph_builder.py
````python
"""KF knowledge graph builder."""
⋮----
def _compute_kf_content_hash(entities: Dict) -> str
⋮----
"""计算 KF 条目的内容哈希（排除 id/data_source/images 等非业务字段）。"""
event = entities.get("event", {})
product = entities.get("product", {})
root_cause = entities.get("root_cause", {})
parts = [
raw = "|".join(parts)
⋮----
class GraphBuilder
⋮----
"""Builds KF graph entities into relational tables."""
⋮----
def build_graph(self, db: Session, entities: Dict, skip_if_exists: bool = False) -> bool
⋮----
"""
        Build graph nodes and relationships.

        去重策略：
        1. 若 event_id 非空，以主键查重（唯一键优先）
        2. 以内容哈希兜底，防止相同内容用不同 id 重复写入

        Returns:
            True if inserted, False if skipped as duplicate.
        """
event_id = entities["event"]["id"]
content_hash = _compute_kf_content_hash(entities)
⋮----
# 唯一键优先
⋮----
existing = db.query(QuickResponseEvent).filter_by(id=event_id).first()
⋮----
# 内容哈希兜底
existing_by_hash = db.query(QuickResponseEvent).filter_by(
⋮----
customer_id = self._insert_customer(db, entities["customer"])
product_id = self._insert_product(db, entities["product"])
defect_id = self._insert_defect(db, entities["defect"])
root_cause_id = self._insert_root_cause(db, entities["root_cause"])
four_m_id = self._insert_four_m(db, entities["four_m"])
⋮----
def _insert_customer(self, db: Session, name: str) -> Optional[int]
⋮----
existing = db.query(Customer).filter_by(name=name).first()
⋮----
result = db.query(Customer).filter_by(name=name).first()
⋮----
def _insert_product(self, db: Session, product: Dict) -> Optional[int]
⋮----
existing = db.query(Product).filter_by(model=product["model"]).first()
⋮----
result = db.query(Product).filter_by(model=product["model"]).first()
⋮----
def _insert_defect(self, db: Session, name: str) -> Optional[int]
⋮----
existing = db.query(Defect).filter_by(name=name).first()
⋮----
result = db.query(Defect).filter_by(name=name).first()
⋮----
def _insert_root_cause(self, db: Session, root_cause: Dict) -> Optional[int]
⋮----
existing = db.query(RootCause).filter_by(
⋮----
result = db.query(RootCause).filter_by(
⋮----
def _insert_four_m(self, db: Session, element: str) -> Optional[int]
⋮----
existing = db.query(FourMElement).filter_by(element=element).first()
⋮----
result = db.query(FourMElement).filter_by(element=element).first()
⋮----
def _parse_occurrence_time(self, value: object) -> Optional[datetime]
⋮----
"""Normalize Excel/JSON date values to datetime for SQLAlchemy DateTime columns."""
⋮----
text = value.strip()
⋮----
iso_candidate = text[:-1] + "+00:00" if text.endswith("Z") else text
````

## File: backend/services/label_config_cache.py
````python
"""
标签配置缓存服务
提供标签配置的缓存机制,减少数据库查询
"""
⋮----
class LabelConfigCache
⋮----
"""
    标签配置缓存
    
    使用版本号机制检测配置变化,自动失效缓存
    线程安全的单例模式
    """
⋮----
_entity_types_cache: Optional[List[EntityType]] = None
_relation_types_cache: Optional[List[RelationType]] = None
_cache_version: int = 0
_cache_lock = threading.Lock()
⋮----
@classmethod
    def get_entity_types(cls, db_session: Session, version_id: Optional[int] = None) -> List[EntityType]
⋮----
"""
        获取实体类型配置(带缓存)
        
        Args:
            db_session: 数据库会话
            version_id: 标签体系版本ID(可选,默认使用活跃版本)
            
        Returns:
            List[EntityType]: 实体类型列表
        """
⋮----
current_version = cls._get_config_version(db_session)
⋮----
# 检查缓存是否有效
⋮----
# 重新加载配置
active_query = db_session.query(EntityType).filter(EntityType.is_active == True)
⋮----
# 优先使用已审核标签；若为空则回退到全部活跃标签（便于当前阶段直接投入使用）
reviewed_items = active_query.filter(EntityType.is_reviewed == True).order_by(EntityType.id).all()
⋮----
items = reviewed_items
⋮----
items = active_query.order_by(EntityType.id).all()
# 将对象从Session解绑，避免跨Session/commit后的DetachedInstanceError
⋮----
@classmethod
    def get_relation_types(cls, db_session: Session, version_id: Optional[int] = None) -> List[RelationType]
⋮----
"""
        获取关系类型配置(带缓存)
        
        Args:
            db_session: 数据库会话
            version_id: 标签体系版本ID(可选,默认使用活跃版本)
            
        Returns:
            List[RelationType]: 关系类型列表
        """
⋮----
active_query = db_session.query(RelationType).filter(RelationType.is_active == True)
⋮----
reviewed_items = active_query.filter(RelationType.is_reviewed == True).order_by(RelationType.id).all()
⋮----
items = active_query.order_by(RelationType.id).all()
⋮----
@classmethod
    def invalidate_cache(cls)
⋮----
"""
        清空缓存
        
        在标签配置更新时调用,强制下次查询时重新加载
        """
⋮----
@classmethod
    def _get_config_version(cls, db_session: Session) -> int
⋮----
"""
        获取配置版本号
        
        基于标签配置的最后更新时间生成版本号
        
        Args:
            db_session: 数据库会话
            
        Returns:
            int: 版本号(时间戳)
        """
⋮----
# 查询实体类型的最后更新时间
entity_max = db_session.query(func.max(EntityType.updated_at)).scalar()
⋮----
# 查询关系类型的最后更新时间
relation_max = db_session.query(func.max(RelationType.updated_at)).scalar()
⋮----
# 使用最新的时间戳作为版本号
⋮----
latest_time = max(entity_max, relation_max)
⋮----
# 如果查询失败,返回0(会触发重新加载)
⋮----
@classmethod
    def get_cache_stats(cls) -> dict
⋮----
"""
        获取缓存统计信息
        
        Returns:
            dict: 缓存统计信息
        """
````

## File: backend/services/label_management_service.py
````python
"""
标签管理服务
提供标签体系的CRUD、导入导出、版本管理等功能
"""
⋮----
class LabelManagementService
⋮----
"""标签管理服务"""
⋮----
def __init__(self, db: Session)
⋮----
"""
        初始化服务
        
        Args:
            db: 数据库会话
        """
⋮----
# ========================================================================
# 实体类型管理
⋮----
"""
        创建实体类型
        
        Args:
            type_name: 类型名称(英文)
            type_name_zh: 类型名称(中文)
            color: 颜色代码
            description: 描述
            supports_bbox: 是否支持边界框
            
        Returns:
            EntityType: 创建的实体类型
        """
entity_type = EntityType(
⋮----
is_reviewed=False  # 新创建的标签默认未审核
⋮----
# 清空缓存
⋮----
"""
        更新实体类型
        
        Args:
            entity_type_id: 实体类型ID
            **kwargs: 要更新的字段
            
        Returns:
            Optional[EntityType]: 更新后的实体类型
        """
entity_type = self.db.query(EntityType).filter(EntityType.id == entity_type_id).first()
⋮----
# 更新字段
⋮----
# 更新时间戳
⋮----
def delete_entity_type(self, entity_type_id: int) -> bool
⋮----
"""
        删除实体类型(软删除,设置为不活跃)
        
        Args:
            entity_type_id: 实体类型ID
            
        Returns:
            bool: 是否删除成功
        """
⋮----
# 软删除
⋮----
def get_entity_type(self, entity_type_id: int) -> Optional[EntityType]
⋮----
"""
        获取实体类型详情
        
        Args:
            entity_type_id: 实体类型ID
            
        Returns:
            Optional[EntityType]: 实体类型对象
        """
⋮----
"""
        获取实体类型列表
        
        Args:
            include_inactive: 是否包含不活跃的类型
            include_unreviewed: 是否包含未审核的类型
            
        Returns:
            List[EntityType]: 实体类型列表
        """
query = self.db.query(EntityType)
⋮----
query = query.filter(EntityType.is_active == True)
⋮----
query = query.filter(EntityType.is_reviewed == True)
⋮----
# 关系类型管理
⋮----
"""
        创建关系类型
        
        Args:
            type_name: 类型名称(英文)
            type_name_zh: 类型名称(中文)
            color: 颜色代码
            description: 描述
            
        Returns:
            RelationType: 创建的关系类型
        """
relation_type = RelationType(
⋮----
"""
        更新关系类型
        
        Args:
            relation_type_id: 关系类型ID
            **kwargs: 要更新的字段
            
        Returns:
            Optional[RelationType]: 更新后的关系类型
        """
relation_type = self.db.query(RelationType).filter(RelationType.id == relation_type_id).first()
⋮----
def delete_relation_type(self, relation_type_id: int) -> bool
⋮----
"""
        删除关系类型(软删除,设置为不活跃)
        
        Args:
            relation_type_id: 关系类型ID
            
        Returns:
            bool: 是否删除成功
        """
⋮----
def get_relation_type(self, relation_type_id: int) -> Optional[RelationType]
⋮----
"""
        获取关系类型详情
        
        Args:
            relation_type_id: 关系类型ID
            
        Returns:
            Optional[RelationType]: 关系类型对象
        """
⋮----
"""
        获取关系类型列表
        
        Args:
            include_inactive: 是否包含不活跃的类型
            include_unreviewed: 是否包含未审核的类型
            
        Returns:
            List[RelationType]: 关系类型列表
        """
query = self.db.query(RelationType)
⋮----
query = query.filter(RelationType.is_active == True)
⋮----
query = query.filter(RelationType.is_reviewed == True)
⋮----
# 标签定义审核
⋮----
"""
        审核实体类型定义
        
        Args:
            entity_type_id: 实体类型ID
            reviewed_by: 审核人ID
            definition: 定义(可选,用户可能编辑)
            examples: 示例列表(可选,用户可能编辑)
            disambiguation: 类别辨析(可选,用户可能编辑)
            
        Returns:
            Optional[EntityType]: 审核后的实体类型
        """
⋮----
# 更新定义(如果提供)
⋮----
# 标记为已审核
⋮----
"""
        审核关系类型定义
        
        Args:
            relation_type_id: 关系类型ID
            reviewed_by: 审核人ID
            definition: 定义(可选,用户可能编辑)
            direction_rule: 方向规则(可选,用户可能编辑)
            examples: 示例列表(可选,用户可能编辑)
            disambiguation: 类别辨析(可选,用户可能编辑)
            
        Returns:
            Optional[RelationType]: 审核后的关系类型
        """
⋮----
# 标签配置导入导出
⋮----
def export_label_schema(self) -> Dict[str, Any]
⋮----
"""
        导出标签配置
        
        Returns:
            Dict: 标签配置JSON
        """
entity_types = self.list_entity_types(include_inactive=False, include_unreviewed=True)
relation_types = self.list_relation_types(include_inactive=False, include_unreviewed=True)
⋮----
"""
        导入标签配置
        
        Args:
            schema_data: 标签配置JSON
            merge: 是否合并(True=合并, False=替换)
            
        Returns:
            Dict: 导入统计信息
        """
stats = {
⋮----
# 如果不是合并模式,先禁用所有现有标签
⋮----
# 导入实体类型
⋮----
existing = self.db.query(EntityType).filter(
⋮----
# 更新现有标签
⋮----
value = json.dumps(value, ensure_ascii=False)
⋮----
# 创建新标签
examples = et_data.get('examples', [])
⋮----
examples = json.dumps(examples, ensure_ascii=False)
⋮----
new_et = EntityType(
⋮----
# 导入关系类型
⋮----
existing = self.db.query(RelationType).filter(
⋮----
examples = rt_data.get('examples', [])
⋮----
new_rt = RelationType(
⋮----
# 版本管理
⋮----
"""
        创建标签体系版本快照
        
        Args:
            version_name: 版本名称
            description: 版本说明
            created_by: 创建人ID
            
        Returns:
            LabelSchemaVersion: 创建的版本对象
        """
# 生成版本ID
version_id = f"schema-{uuid.uuid4().hex[:12]}"
⋮----
# 导出当前配置
schema_data = self.export_label_schema()
⋮----
# 创建版本记录
version = LabelSchemaVersion(
⋮----
is_active=False,  # 新创建的版本默认不活跃
⋮----
def list_versions(self) -> List[LabelSchemaVersion]
⋮----
"""
        获取版本列表
        
        Returns:
            List[LabelSchemaVersion]: 版本列表
        """
⋮----
def get_version(self, version_id: str) -> Optional[LabelSchemaVersion]
⋮----
"""
        获取版本详情
        
        Args:
            version_id: 版本ID
            
        Returns:
            Optional[LabelSchemaVersion]: 版本对象
        """
⋮----
def activate_version(self, version_id: str) -> Optional[LabelSchemaVersion]
⋮----
"""
        激活版本
        
        Args:
            version_id: 版本ID
            
        Returns:
            Optional[LabelSchemaVersion]: 激活的版本对象
        """
version = self.get_version(version_id)
⋮----
# 取消其他版本的活跃状态
⋮----
# 激活当前版本
⋮----
def get_active_version(self) -> Optional[LabelSchemaVersion]
⋮----
"""
        获取当前活跃版本
        
        Returns:
            Optional[LabelSchemaVersion]: 活跃版本对象
        """
````

## File: backend/services/offset_correction.py
````python
"""
偏移量验证与修正服务
用于验证和修正LLM标注的实体偏移量
"""
⋮----
@dataclass
class CorrectionLog
⋮----
"""修正日志"""
entity_text: str
original_start: int
original_end: int
corrected_start: Optional[int]
corrected_end: Optional[int]
correction_type: str  # 'exact_match', 'fuzzy_match', 'failed'
message: str
⋮----
class OffsetCorrectionService
⋮----
"""偏移量验证与修正服务"""
⋮----
def __init__(self)
⋮----
"""
        验证偏移量是否正确
        
        Args:
            text: 原始文本
            entity_text: 实体文本
            start_offset: 起始偏移量
            end_offset: 结束偏移量
            
        Returns:
            偏移量是否正确
        """
# 检查偏移量范围
⋮----
# 检查偏移量对应的文本是否匹配
extracted_text = text[start_offset:end_offset]
⋮----
# 精确匹配
⋮----
# 去除空格后匹配
⋮----
"""
        修正偏移量
        
        Args:
            text: 原始文本
            entity_text: 实体文本
            start_offset: 原始起始偏移量
            end_offset: 原始结束偏移量
            max_search_distance: 最大搜索距离
            
        Returns:
            (修正后的起始偏移量, 修正后的结束偏移量, 修正日志)
        """
# 首先验证原始偏移量
⋮----
log = CorrectionLog(
⋮----
# 尝试查找最近匹配
⋮----
# 无法修正
⋮----
"""
        查找最近的匹配位置
        
        策略:
        1. 在hint_offset附近搜索精确匹配
        2. 尝试去除空格后匹配
        3. 尝试模糊匹配（忽略标点符号）
        
        Args:
            text: 原始文本
            entity_text: 实体文本
            hint_offset: 提示偏移量（搜索起点）
            max_distance: 最大搜索距离
            
        Returns:
            (起始偏移量, 结束偏移量) 或 (None, None)
        """
# 清理实体文本
entity_clean = entity_text.strip()
entity_len = len(entity_clean)
⋮----
# 定义搜索范围
search_start = max(0, hint_offset - max_distance)
search_end = min(len(text), hint_offset + max_distance + entity_len)
⋮----
# 策略1: 精确匹配
start_pos = text.find(entity_clean, search_start, search_end)
⋮----
# 策略2: 去除所有空格后匹配
entity_no_space = entity_clean.replace(' ', '')
text_no_space = text[search_start:search_end].replace(' ', '')
⋮----
pos_in_no_space = text_no_space.find(entity_no_space)
⋮----
# 需要映射回原始文本的位置
original_pos = self._map_position_with_spaces(
⋮----
# 策略3: 模糊匹配（忽略标点和空格）
entity_normalized = self._normalize_text(entity_clean)
⋮----
# 在搜索范围内滑动窗口查找
⋮----
window = text[i:i + entity_len]
window_normalized = self._normalize_text(window)
⋮----
# 策略4: 扩展窗口模糊匹配（允许长度差异）
⋮----
window = text[i:i + window_len]
⋮----
# 计算相似度
⋮----
"""
        将无空格文本的位置映射回原始文本位置
        
        Args:
            text: 原始文本
            pos_no_space: 无空格文本中的位置
            length_no_space: 无空格文本的长度
            
        Returns:
            (起始位置, 结束位置) 或 None
        """
char_count = 0
start_pos = None
⋮----
start_pos = i
⋮----
def _normalize_text(self, text: str) -> str
⋮----
"""
        标准化文本（去除空格和标点符号）
        
        Args:
            text: 原始文本
            
        Returns:
            标准化后的文本
        """
# 去除空格
text = text.replace(' ', '')
# 去除常见标点符号
text = re.sub(r'[，。！？、；：""''（）《》【】\\.,!?;:()\[\]{}]', '', text)
⋮----
def _text_similarity(self, text1: str, text2: str) -> float
⋮----
"""
        计算两个文本的相似度（简单的字符匹配率）
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度 (0-1)
        """
⋮----
# 使用最长公共子序列
⋮----
# 简化版：计算字符匹配率
matches = sum(1 for c1, c2 in zip(text1, text2) if c1 == c2)
max_len = max(len1, len2)
⋮----
def get_correction_logs(self) -> List[CorrectionLog]
⋮----
"""
        获取所有修正日志
        
        Returns:
            修正日志列表
        """
⋮----
def clear_logs(self)
⋮----
"""清空修正日志"""
⋮----
def get_correction_stats(self) -> Dict[str, int]
⋮----
"""
        获取修正统计信息
        
        Returns:
            统计信息字典
        """
stats = {
````

## File: backend/services/qms_graph_builder.py
````python
"""QMS不合格品知识图谱构建器"""
⋮----
def _compute_qms_content_hash(entities: Dict) -> str
⋮----
"""计算 QMS 条目的内容哈希（排除 id/data_source/photo_path 等非业务字段）。"""
event = entities.get("event", {})
product = entities.get("product", {})
production = entities.get("production", {})
inspection = entities.get("inspection", {})
parts = [
raw = "|".join(parts)
⋮----
class QMSGraphBuilder
⋮----
"""构建 QMS 不合格品知识图谱"""
⋮----
def build_graph(self, db: Session, entities: Dict, skip_if_exists: bool = False) -> bool
⋮----
"""
        构建 QMS 图谱节点和关系

        去重策略：
        1. 若制令单号非空，以主键查重（唯一键优先）
        2. 以内容哈希兜底，防止相同内容用不同制令单号重复写入

        Returns:
            True=新插入，False=已存在被跳过
        """
event_id = entities['event']['id']
⋮----
content_hash = _compute_qms_content_hash(entities)
⋮----
# 唯一键优先
existing = db.query(QMSDefectOrder).filter_by(id=event_id).first()
⋮----
# 内容哈希兜底
existing_by_hash = db.query(QMSDefectOrder).filter_by(
⋮----
customer_id = self._upsert_one(db, Customer, 'name', entities.get('customer'))
⋮----
prod = entities.get('product', {})
defect_id = self._upsert_one(db, Defect, 'name', entities.get('defect'))
⋮----
production = entities.get('production', {})
workshop_id = self._upsert_one(db, QMSWorkshop, 'name', production.get('workshop'))
line_id = self._upsert_line(db, production.get('line'), workshop_id)
station_id = self._upsert_one(db, QMSStation, 'name', production.get('station'))
⋮----
inspection = entities.get('inspection', {})
inspection_node_id = self._upsert_one(db, QMSInspectionNode, 'name', inspection.get('node'))
⋮----
event = entities['event']
images = event.get('images', [])
photo_path = images[0] if images else None
⋮----
def _upsert_one(self, db: Session, model_class, col: str, value: str) -> Optional[int]
⋮----
"""插入或忽略单列唯一值，返回 id"""
⋮----
existing = db.query(model_class).filter(getattr(model_class, col) == value).first()
⋮----
result = db.query(model_class).filter(getattr(model_class, col) == value).first()
⋮----
def _upsert_line(self, db: Session, name: str, workshop_id: Optional[int]) -> Optional[int]
⋮----
"""插入产线（name + workshop_id 联合唯一），返回 id"""
⋮----
existing = db.query(QMSProductionLine).filter(
⋮----
result = db.query(QMSProductionLine).filter(
````

## File: backend/services/query_engine.py
````python
"""鍥捐氨鏌ヨ寮曟搸"""
⋮----
class QueryEngine
⋮----
FAILURE_CASE_REQUIRED_FIELDS = [
⋮----
def __init__(self, processor_name: str = 'kf')
⋮----
def _clean_image_path(self, image_path: Optional[str]) -> str
⋮----
"""Normalize image path to forward-slash relative format."""
⋮----
def _to_storage_preview_url(self, image_path: Optional[str]) -> str
⋮----
"""Build preview URL for files managed by storage service (/images)."""
cleaned = self._clean_image_path(image_path)
⋮----
cleaned = cleaned[len('images/'):]
⋮----
"""Build preview URL for processed KF/QMS image folders."""
⋮----
encoded_ds = quote(ds, safe='')
encoded_path = quote(cleaned, safe='/')
⋮----
"""Normalize processed image relative path and datasource."""
⋮----
ds = (data_source or '').strip()
⋮----
# Some records may store "{data_source}/imgs/xxx.png".
prefix = f"{ds}/"
⋮----
cleaned = cleaned[len(prefix):]
⋮----
def _candidate_processed_data_sources(self, data_source: Optional[str]) -> List[str]
⋮----
"""Build possible directory names for one logical data_source."""
⋮----
candidates: List[str] = []
⋮----
normalized = (item or '').strip()
⋮----
def _strip_data_source_prefix(self, image_path: str, data_source_candidates: List[str]) -> str
⋮----
"""Strip optional '<data_source>/' prefix in stored image path."""
⋮----
def _safe_local_resolve(self, base_dir: Path, relative_path: str) -> Optional[Path]
⋮----
"""Resolve path under base_dir and reject traversal paths."""
⋮----
base = base_dir.resolve()
candidate = (base / relative_path).resolve()
⋮----
"""Whether KF/QMS processed image file exists on local filesystem."""
⋮----
"""
        Resolve the first existing processed image URL.

        Handles data_source naming drift such as '-' vs '_'.
        """
⋮----
# Processed images are local files; in non-local storage mode keep direct URL build.
⋮----
candidates = self._candidate_processed_data_sources(data_source)
⋮----
cleaned = self._strip_data_source_prefix(self._clean_image_path(image_path), candidates)
⋮----
relative = f"{processor_name}/{candidate_ds}/{cleaned}"
resolved = self._safe_local_resolve(settings.PROCESSED_DIR, relative)
⋮----
encoded_ds = quote(candidate_ds, safe='')
⋮----
def _storage_image_exists(self, image_path: Optional[str]) -> bool
⋮----
"""Whether storage-managed image exists (local check, MinIO optimistic)."""
⋮----
# MinIO does not have cheap local existence check here; keep preview enabled.
⋮----
resolved = self._safe_local_resolve(settings.IMAGE_DIR, cleaned)
⋮----
def _parse_image_paths(self, raw_value) -> List[str]
⋮----
"""Parse image path list from json/list/string/markdown values."""
⋮----
candidates = [str(v) for v in raw_value if str(v).strip()]
⋮----
text_value = str(raw_value).strip()
⋮----
# Markdown images: ![...](path)
markdown_paths = re.findall(r'!\[.*?\]\((.*?)\)', text_value)
⋮----
# JSON array or JSON string
⋮----
parsed = json.loads(text_value)
⋮----
# Common separators for multiple values
⋮----
normalized: List[str] = []
seen = set()
⋮----
cleaned = self._clean_image_path(item)
⋮----
def _build_kf_preview_urls(self, image_paths: List[str], data_source: Optional[str]) -> List[str]
⋮----
urls: List[str] = []
⋮----
# KF/QMS current data usually points to processed/{processor}/{data_source}/imgs/*
processed_url = self._resolve_processed_preview_url('kf', data_source, path)
⋮----
def _build_qms_preview_urls(self, image_paths: List[str], data_source: Optional[str]) -> List[str]
⋮----
processed_url = self._resolve_processed_preview_url('qms', data_source, path)
⋮----
def _get_failure_case_image_paths(self, db: Session, source_file: str, source_row: int) -> List[str]
⋮----
image_rows = db.query(Image.file_path).join(
image_paths = [self._clean_image_path(row[0]) for row in image_rows if row and row[0]]
⋮----
unique_paths: List[str] = []
⋮----
def get_graph_data(self, db: Session, filters: Optional[Dict] = None, limit: int = 100) -> Dict
⋮----
"""鑾峰彇鍥捐氨鏁版嵁"""
⋮----
def _get_kf_graph_data(self, db: Session, filters: Optional[Dict] = None, limit: int = 100) -> Dict
⋮----
nodes = []
edges = []
node_ids = set()
⋮----
# 鏋勫缓鏌ヨ
query = db.query(
⋮----
# 搴旂敤杩囨护
⋮----
query = query.filter(Customer.name == filters['customer'])
⋮----
query = query.filter(Product.model == filters['product'])
⋮----
query = query.filter(Defect.name == filters['defect'])
⋮----
query = query.filter(QuickResponseEvent.occurrence_time >= filters['start_date'])
⋮----
query = query.filter(QuickResponseEvent.occurrence_time <= filters['end_date'])
⋮----
query = query.limit(limit)
results = query.all()
⋮----
event_id = f"event_{event.id}"
⋮----
# 澶勭悊鍥剧墖璺緞
event_data = {
⋮----
images = json.loads(event.images) if isinstance(event.images, str) else event.images
data_source = event.data_source or ''
⋮----
# 瀹㈡埛鑺傜偣
⋮----
customer_id = f"customer_{customer.id}"
⋮----
# 浜у搧鑺傜偣
⋮----
product_id = f"product_{product.id}"
⋮----
# 缂洪櫡鑺傜偣
⋮----
defect_id = f"defect_{defect.id}"
⋮----
# 寮傚父鍘熷洜鑺傜偣
⋮----
rc_id = f"root_cause_{root_cause.id}"
⋮----
# 4M瑕佺礌鑺傜偣
⋮----
fm_id = f"four_m_{four_m.id}"
⋮----
def _get_qms_graph_data(self, db: Session, filters: Optional[Dict] = None, limit: int = 100) -> Dict
⋮----
query = db.query(QMSDefectOrder).outerjoin(
⋮----
query = query.filter(QMSWorkshop.name == filters['workshop'])
⋮----
query = query.filter(QMSDefectOrder.entry_time >= filters['start_date'])
⋮----
query = query.filter(QMSDefectOrder.entry_time <= filters['end_date'])
⋮----
order_id = f"order_{order.id}"
⋮----
order_data = {
⋮----
def get_event_detail(self, db: Session, event_id: str) -> Optional[Dict]
⋮----
"""鑾峰彇浜嬩欢璇︽儏"""
event = db.query(QuickResponseEvent).filter(QuickResponseEvent.id == event_id).first()
⋮----
result = {
⋮----
def get_statistics(self, db: Session) -> Dict
⋮----
"""鑾峰彇缁熻鏁版嵁"""
⋮----
def _get_kf_statistics(self, db: Session) -> Dict
⋮----
stats = {}
⋮----
# 鎬讳簨浠舵暟
⋮----
# 缂洪櫡绫诲瀷鍒嗗竷
defect_dist = db.query(
⋮----
# 4M瑕佺礌鍒嗗竷
four_m_dist = db.query(
⋮----
# 瀹㈡埛闂鎺掕
customer_rank = db.query(
⋮----
def _get_qms_statistics(self, db: Session) -> Dict
⋮----
# 缂洪櫡鍒嗗竷
⋮----
# 杞﹂棿鍒嗗竷
workshop_dist = db.query(
⋮----
# 浜х嚎鍒嗗竷
line_dist = db.query(
⋮----
# 璐ㄦ鑺傜偣鍒嗗竷
inspection_dist = db.query(
⋮----
# 鐘舵€佸垎甯?
status_dist = db.query(
⋮----
# 瀹㈡埛鎺掕
⋮----
def get_data_list(self, db: Session, processor_name: str = None, limit: int = 100, offset: int = 0) -> List[Dict]
⋮----
"""鑾峰彇鏁版嵁鍒楄〃"""
target = processor_name or self.processor_name
⋮----
def get_data_total_count(self, db: Session, processor_name: str = None) -> int
⋮----
"""Get total row count for pagination."""
⋮----
def _get_kf_list(self, db: Session, limit: int = 100, offset: int = 0) -> List[Dict]
⋮----
results = db.query(QuickResponseEvent).limit(limit).offset(offset).all()
response: List[Dict] = []
⋮----
image_paths = self._parse_image_paths(e.images)
image_preview_urls = self._build_kf_preview_urls(image_paths, e.data_source)
⋮----
def _get_qms_list(self, db: Session, limit: int = 100, offset: int = 0) -> List[Dict]
⋮----
results = db.query(QMSDefectOrder).limit(limit).offset(offset).all()
⋮----
image_paths = self._parse_image_paths(e.photo_path)
image_preview_urls = self._build_qms_preview_urls(image_paths, e.data_source)
⋮----
def _get_failure_case_list(self, db: Session, limit: int = 100, offset: int = 0) -> List[Dict]
⋮----
"""Group failure case records by source_file and source_row."""
grouped_rows = db.query(
⋮----
results: List[Dict] = []
⋮----
record = {
⋮----
field_rows = db.query(
⋮----
image_paths = self._get_failure_case_image_paths(db, source_file, source_row)
⋮----
image_preview_urls = [
⋮----
def _get_failure_case_statistics(self, db: Session) -> Dict
⋮----
"""Failure case statistics aggregated from corpus."""
stats: Dict = {}
⋮----
# 鎬讳簨浠舵暟锛氭寜 source_file + source_row 鍘婚噸
⋮----
# Backward compatibility for older imports that only kept coarse category.
⋮----
# 椤甸潰澶嶇敤瀛楁锛氬搧璐ㄦ渚嬫棤 4M 鍒嗗竷
````

## File: backend/services/review_service.py
````python
"""
复核服务
实现标注任务的复核流程管理
"""
⋮----
class ReviewService
⋮----
"""复核服务类"""
⋮----
def __init__(self, db: Session)
⋮----
def can_user_review_task(self, user_id: int, task_id: int) -> tuple[bool, str]
⋮----
"""
        检查用户是否可以复核指定任务
        
        Args:
            user_id: 用户ID
            task_id: 标注任务ID
        
        Returns:
            tuple: (是否可以复核, 原因说明)
        """
# 查询用户
user = self.db.query(User).filter(User.id == user_id).first()
⋮----
# 查询任务
task = self.db.query(AnnotationTask).filter(AnnotationTask.id == task_id).first()
⋮----
# 管理员可以复核所有任务
⋮----
# 标注员可以复核他人的任务
⋮----
# 检查任务是否是自己标注的
⋮----
# 浏览员不能复核
⋮----
"""
        提交标注任务进行复核
        
        Args:
            task_id: 标注任务ID
            reviewer_id: 指定的复核人员ID（可选）
        
        Returns:
            ReviewTask: 创建的复核任务
        
        Raises:
            ValueError: 任务不存在或状态不允许提交复核
        """
# 查询标注任务
task = self.db.query(AnnotationTask).filter(
⋮----
# 验证任务状态
⋮----
# 检查是否已有待处理的复核任务
existing_review = self.db.query(ReviewTask).filter(
⋮----
# 创建复核任务
review_id = f"REV_{uuid.uuid4().hex[:12].upper()}"
review_task = ReviewTask(
⋮----
# 更新标注任务状态为待复核
⋮----
"""
        查询复核任务列表
        
        Args:
            status: 复核状态筛选（pending/approved/rejected）
            reviewer_id: 复核人员ID筛选
            skip: 跳过记录数
            limit: 返回记录数
        
        Returns:
            tuple: (复核任务列表, 总数)
        """
query = self.db.query(ReviewTask)
⋮----
# 状态筛选
⋮----
query = query.filter(ReviewTask.status == status)
⋮----
# 复核人员筛选
⋮----
query = query.filter(ReviewTask.reviewer_id == reviewer_id)
⋮----
# 获取总数
total = query.count()
⋮----
# 分页查询
reviews = query.order_by(ReviewTask.created_at.desc()).offset(skip).limit(limit).all()
⋮----
"""
        批准标注任务
        
        Args:
            review_id: 复核任务ID
            reviewer_id: 复核人员ID
            comment: 复核意见（可选）
        
        Returns:
            ReviewTask: 更新后的复核任务
        
        Raises:
            ValueError: 复核任务不存在或状态不允许批准
        """
# 查询复核任务
review = self.db.query(ReviewTask).filter(
⋮----
# 更新复核任务
⋮----
# 更新标注任务状态
⋮----
"""
        驳回标注任务
        
        Args:
            review_id: 复核任务ID
            reviewer_id: 复核人员ID
            comment: 驳回原因（必填）
        
        Returns:
            ReviewTask: 更新后的复核任务
        
        Raises:
            ValueError: 复核任务不存在、状态不允许驳回或缺少驳回原因
        """
⋮----
# 更新标注任务状态为待修改
⋮----
def get_review_task_detail(self, review_id: str) -> Optional[Dict[str, Any]]
⋮----
"""
        获取复核任务详情（包含标注数据）
        
        Args:
            review_id: 复核任务ID
        
        Returns:
            Dict: 复核任务详情，包含标注任务和所有标注数据
        """
⋮----
# 查询当前版本的所有实体和关系
text_entities = self.db.query(TextEntity).filter(
⋮----
image_entities = self.db.query(ImageEntity).filter(
⋮----
relations = self.db.query(Relation).filter(
⋮----
# 组装返回数据
⋮----
"""
        记录复核过程中的修改差异
        
        Args:
            review_id: 复核任务ID
            modifications: 修改记录，包含added/removed/modified实体和关系
        
        Raises:
            ValueError: 复核任务不存在
        """
⋮----
# 将修改记录存储到review_comment字段（JSON格式）
⋮----
# 如果已有comment，追加修改记录
⋮----
existing_data = json.loads(review.review_comment)
⋮----
existing_data = {
⋮----
# 原有comment不是JSON，保留原comment并添加modifications
⋮----
"""
        计算数据集的质量统计指标
        
        Args:
            dataset_id: 数据集ID
        
        Returns:
            Dict: 质量统计指标
        """
# 查询数据集的所有标注任务
tasks = self.db.query(AnnotationTask).filter(
⋮----
total_tasks = len(tasks)
task_ids = [t.id for t in tasks]
⋮----
# 统计各状态任务数
completed_tasks = sum(1 for t in tasks if t.status == 'completed')
under_review_tasks = sum(1 for t in tasks if t.status == 'under_review')
approved_tasks = sum(1 for t in tasks if t.status == 'approved')
rejected_tasks = sum(1 for t in tasks if t.status == 'rejected')
⋮----
# 计算比率
completion_rate = (completed_tasks + under_review_tasks + approved_tasks) / total_tasks if total_tasks > 0 else 0.0
approval_rate = approved_tasks / total_tasks if total_tasks > 0 else 0.0
rejection_rate = rejected_tasks / total_tasks if total_tasks > 0 else 0.0
⋮----
# 统计实体和关系数量
total_entities = 0
total_relations = 0
⋮----
# 统计当前版本的实体数
text_entity_count = self.db.query(func.count(TextEntity.id)).filter(
⋮----
image_entity_count = self.db.query(func.count(ImageEntity.id)).filter(
⋮----
relation_count = self.db.query(func.count(Relation.id)).filter(
⋮----
# 计算平均值
avg_entities = total_entities / total_tasks if total_tasks > 0 else 0.0
avg_relations = total_relations / total_tasks if total_tasks > 0 else 0.0
⋮----
"""
        获取数据集的复核摘要信息
        
        Args:
            dataset_id: 数据集ID
        
        Returns:
            Dict: 复核摘要信息
        """
# 查询数据集的所有复核任务
reviews = self.db.query(ReviewTask).join(
⋮----
total_reviews = len(reviews)
pending_reviews = sum(1 for r in reviews if r.status == 'pending')
approved_reviews = sum(1 for r in reviews if r.status == 'approved')
rejected_reviews = sum(1 for r in reviews if r.status == 'rejected')
⋮----
# 计算平均复核时间（仅统计已完成的复核）
completed_reviews = [r for r in reviews if r.reviewed_at]
⋮----
total_hours = sum(
avg_review_time = total_hours / len(completed_reviews)
⋮----
avg_review_time = 0.0
````

## File: backend/services/reward_dataset_service.py
````python
"""
Reward数据集生成服务
用于生成LLM自动标注与人工修正之间的差异数据，用于模型微调
"""
⋮----
class RewardDatasetService
⋮----
"""Reward数据集生成服务类"""
⋮----
def __init__(self, db: Session)
⋮----
"""
        生成Reward数据集
        
        Args:
            dataset_id: 数据集ID
            output_path: 输出文件路径（可选）
        
        Returns:
            Dict: 包含Reward数据和统计信息
                - reward_data: Reward数据列表
                - statistics: 修正频率统计
                - total_count: 总记录数
        """
# 查询数据集
dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
⋮----
# 筛选存在人工修正的任务
corrected_tasks = self._filter_corrected_tasks(dataset_id)
⋮----
# 生成Reward数据
reward_records = []
statistics = {
⋮----
# 获取原始标注和修正标注
original_annotation = self._get_original_annotation(task)
corrected_annotation = self._get_current_annotation(task)
⋮----
# 计算差异
diff = self._calculate_diff(original_annotation, corrected_annotation)
⋮----
# 更新统计
⋮----
# 构建Reward记录
reward_record = {
⋮----
# 导出到文件
⋮----
def _filter_corrected_tasks(self, dataset_id: int) -> List[AnnotationTask]
⋮----
"""
        筛选存在人工修正的标注任务
        
        Args:
            dataset_id: 数据集ID
        
        Returns:
            List[AnnotationTask]: 存在修正的任务列表
        """
# 查询数据集中的所有任务
tasks = self.db.query(AnnotationTask).filter(
⋮----
corrected_tasks = []
⋮----
# 检查是否存在版本历史（版本号>1表示有修正）
⋮----
# 或者检查是否从automatic变为manual
⋮----
# 查询是否有版本1的记录
version1 = self.db.query(VersionHistory).filter(
⋮----
def _get_original_annotation(self, task: AnnotationTask) -> Dict[str, Any]
⋮----
"""
        获取原始标注（版本1）
        
        Args:
            task: 标注任务
        
        Returns:
            Dict: 原始标注数据
        """
# 查询版本1的历史记录
version1_history = self.db.query(VersionHistory).filter(
⋮----
# 从快照中恢复
snapshot = json.loads(version1_history.snapshot_data)
⋮----
# 如果没有快照，查询版本1的实体和关系
⋮----
def _get_current_annotation(self, task: AnnotationTask) -> Dict[str, Any]
⋮----
"""
        获取当前标注（最新版本）
        
        Args:
            task: 标注任务
        
        Returns:
            Dict: 当前标注数据
        """
⋮----
"""
        查询指定版本的标注数据
        
        Args:
            task: 标注任务
            version: 版本号
        
        Returns:
            Dict: 标注数据
        """
# 查询语料
corpus = self.db.query(Corpus).filter(
⋮----
# 查询文本实体
text_entities = self.db.query(TextEntity).filter(
⋮----
# 查询图片实体
image_entities = self.db.query(ImageEntity).filter(
⋮----
# 查询关系
relations = self.db.query(Relation).filter(
⋮----
"""
        从快照格式化标注数据
        
        Args:
            task: 标注任务
            snapshot: 快照数据
        
        Returns:
            Dict: 格式化的标注数据
        """
⋮----
# 格式化实体，将entity_id重命名为id以保持一致性
entities = []
⋮----
entity = e.copy()
⋮----
# 格式化图片实体
image_entities = []
⋮----
img_entity = ie.copy()
⋮----
"""
        计算原始标注和修正标注之间的差异
        
        Args:
            original: 原始标注
            corrected: 修正标注
        
        Returns:
            Dict: 差异描述
        """
def compare_entities(orig_list, corr_list)
⋮----
"""比较实体列表"""
orig_dict = {e['id']: e for e in orig_list}
corr_dict = {e['id']: e for e in corr_list}
⋮----
added = [e for eid, e in corr_dict.items() if eid not in orig_dict]
removed = [e for eid, e in orig_dict.items() if eid not in corr_dict]
modified = []
⋮----
orig_e = orig_dict[eid]
corr_e = corr_dict[eid]
⋮----
# 检查标签是否修改
⋮----
def compare_relations(orig_list, corr_list)
⋮----
"""比较关系列表"""
# 使用(from_id, to_id)作为关系的唯一标识
orig_set = {(r['from_id'], r['to_id']) for r in orig_list}
corr_set = {(r['from_id'], r['to_id']) for r in corr_list}
⋮----
orig_dict = {(r['from_id'], r['to_id']): r for r in orig_list}
corr_dict = {(r['from_id'], r['to_id']): r for r in corr_list}
⋮----
added = [corr_dict[k] for k in corr_set - orig_set]
removed = [orig_dict[k] for k in orig_set - corr_set]
⋮----
# 比较文本实体
entities_diff = compare_entities(
⋮----
# 比较图片实体
image_entities_diff = compare_entities(
⋮----
# 比较关系
relations_diff = compare_relations(
⋮----
"""
        更新修正频率统计
        
        Args:
            statistics: 统计字典
            diff: 差异数据
        """
# 文本实体统计
⋮----
# 图片实体统计
⋮----
# 关系统计
⋮----
"""
        导出Reward数据到JSONL文件
        
        Args:
            reward_data: Reward数据列表
            output_path: 输出文件路径
        """
⋮----
"""
        获取修正频率报告
        
        Args:
            dataset_id: 数据集ID
        
        Returns:
            Dict: 修正频率报告
        """
result = self.generate_reward_dataset(dataset_id)
⋮----
statistics = result['statistics']
total_corrections = sum(statistics.values())
⋮----
# 计算百分比
frequency_report = {}
⋮----
percentage = (count / total_corrections * 100) if total_corrections > 0 else 0
````

## File: backend/services/serialization_service.py
````python
"""
数据序列化服务（简化版）
提供标注数据的序列化和反序列化功能
"""
⋮----
class SerializationService
⋮----
"""数据序列化服务类"""
⋮----
def __init__(self, db: Session)
⋮----
# ========================================================================
# 文本实体序列化
⋮----
@staticmethod
    def serialize_text_entity(entity: TextEntity) -> Dict[str, Any]
⋮----
"""
        序列化文本实体
        
        Args:
            entity: 文本实体对象
        
        Returns:
            Dict: 序列化后的字典，包含id、start_offset、end_offset、label字段
        """
⋮----
"token": entity.token  # 额外包含token字段便于调试
⋮----
@staticmethod
    def deserialize_text_entity(data: Dict[str, Any], task_id: int, entity_id: int = 0, version: int = 1) -> TextEntity
⋮----
"""
        反序列化文本实体
        
        Args:
            data: 序列化的字典数据
            task_id: 关联的任务ID（整数）
            entity_id: 实体在任务内的ID
            version: 版本号
        
        Returns:
            TextEntity: 文本实体对象
        """
⋮----
# 图片实体序列化
⋮----
@staticmethod
    def serialize_image_entity(entity: ImageEntity) -> Dict[str, Any]
⋮----
"""
        序列化图片实体（支持整图和区域）
        
        Args:
            entity: 图片实体对象
        
        Returns:
            Dict: 序列化后的字典
            - 整图实体: id, image_path, label, bbox=null
            - 区域实体: id, image_path, label, bbox={x, y, width, height}
        """
result = {
⋮----
"image_path": entity.image_id,  # 使用image_id作为路径标识
⋮----
# 处理边界框
⋮----
# 区域实体
⋮----
# 整图实体
⋮----
@staticmethod
    def deserialize_image_entity(data: Dict[str, Any], task_id: int, entity_id: int = 0, version: int = 1) -> ImageEntity
⋮----
"""
        反序列化图片实体
        
        Args:
            data: 序列化的字典数据
            task_id: 关联的任务ID（整数）
            entity_id: 实体在任务内的ID
            version: 版本号
        
        Returns:
            ImageEntity: 图片实体对象
        """
bbox = data.get("bbox")
⋮----
# 注意：image_id 在数据库中是整数外键，这里简化处理
# 实际使用时需要先查找或创建对应的 Image 记录
⋮----
image_id=1,  # 简化：使用固定值，实际应该查找对应的图片ID
⋮----
# 关系序列化
⋮----
@staticmethod
    def serialize_relation(relation: Relation) -> Dict[str, Any]
⋮----
"""
        序列化关系
        
        Args:
            relation: 关系对象
        
        Returns:
            Dict: 序列化后的字典，包含from_id、to_id、type字段
        """
⋮----
@staticmethod
    def deserialize_relation(data: Dict[str, Any], task_id: int, relation_id: int = 0, version: int = 1) -> Relation
⋮----
"""
        反序列化关系
        
        Args:
            data: 序列化的字典数据
            task_id: 关联的任务ID（整数）
            relation_id: 关系在任务内的ID
            version: 版本号
        
        Returns:
            Relation: 关系对象
        """
⋮----
# 完整标注任务序列化
⋮----
"""
        序列化完整的标注任务
        
        Args:
            task: 标注任务对象
            include_metadata: 是否包含元数据（任务ID、状态等）
        
        Returns:
            Dict: 序列化后的完整数据
        """
# 获取语料信息
⋮----
corpus = self.db.query(Corpus).filter(
⋮----
# 获取所有实体和关系
text_entities = self.db.query(TextEntity).filter(
⋮----
image_entities = self.db.query(ImageEntity).filter(
⋮----
relations = self.db.query(Relation).filter(
⋮----
# 序列化数据
⋮----
# 可选的元数据
⋮----
"""
        反序列化标注任务数据
        
        Args:
            data: 序列化的字典数据
            task_id: 任务ID（整数）
            create_entities: 是否创建实体和关系对象（否则只返回数据）
        
        Returns:
            Dict: 包含entities、images、relations列表的字典
        """
⋮----
# 只返回原始数据
⋮----
# 创建实体对象
⋮----
entity = self.deserialize_text_entity(entity_data, task_id, entity_id=idx)
⋮----
entity = self.deserialize_image_entity(image_data, task_id, entity_id=idx)
⋮----
relation = self.deserialize_relation(relation_data, task_id, relation_id=idx)
⋮----
# 批量序列化
⋮----
"""
        批量序列化多个标注任务
        
        Args:
            task_ids: 任务ID列表
            include_metadata: 是否包含元数据
        
        Returns:
            List[Dict]: 序列化后的任务列表
        """
tasks = self.db.query(AnnotationTask).filter(
⋮----
# 工具方法
⋮----
@staticmethod
    def validate_serialized_data(data: Dict[str, Any]) -> bool
⋮----
"""
        验证序列化数据的格式是否正确
        
        Args:
            data: 序列化的数据
        
        Returns:
            bool: 数据格式是否有效
        """
# 检查必需字段
required_fields = ["text", "entities", "relations"]
⋮----
# 验证实体格式
⋮----
# 验证图片实体格式
⋮----
# 验证关系格式
````

## File: backend/services/storage_service.py
````python
"""
存储服务 - 支持本地文件系统和MinIO对象存储
提供统一的文件存储接口，可通过配置切换存储方式
"""
⋮----
class StorageService
⋮----
"""统一存储服务接口"""
⋮----
def __init__(self)
⋮----
self.storage_type = settings.STORAGE_TYPE  # 'local' or 'minio'
⋮----
# 确保bucket存在
⋮----
"""
        保存图片文件
        
        Args:
            file_data: 文件二进制数据
            relative_path: 相对路径，如 "文件名/ID_XXX.png"
            content_type: 文件MIME类型
            
        Returns:
            文件访问路径（相对路径）
        """
⋮----
def _save_to_local(self, file_data: bytes, relative_path: str) -> str
⋮----
"""保存到本地文件系统"""
full_path = settings.IMAGE_DIR / relative_path
⋮----
def _save_to_minio(self, file_data: bytes, relative_path: str, content_type: str) -> str
⋮----
"""保存到MinIO对象存储"""
# 将bytes转换为BytesIO对象
file_stream = io.BytesIO(file_data)
file_size = len(file_data)
⋮----
# 上传到MinIO
⋮----
def get_image(self, relative_path: str) -> Optional[bytes]
⋮----
"""
        获取图片文件
        
        Args:
            relative_path: 相对路径
            
        Returns:
            文件二进制数据，如果不存在返回None
        """
⋮----
def _get_from_local(self, relative_path: str) -> Optional[bytes]
⋮----
"""从本地文件系统获取"""
⋮----
def _get_from_minio(self, relative_path: str) -> Optional[bytes]
⋮----
"""从MinIO获取"""
⋮----
response = self.minio_client.get_object(
data = response.read()
⋮----
def delete_image(self, relative_path: str) -> bool
⋮----
"""
        删除图片文件
        
        Args:
            relative_path: 相对路径
            
        Returns:
            是否删除成功
        """
⋮----
def _delete_from_local(self, relative_path: str) -> bool
⋮----
"""从本地文件系统删除"""
⋮----
def _delete_from_minio(self, relative_path: str) -> bool
⋮----
"""从MinIO删除"""
⋮----
def get_public_url(self, relative_path: str) -> str
⋮----
"""
        获取文件的公开访问URL
        
        Args:
            relative_path: 相对路径
            
        Returns:
            完整的访问URL
        """
⋮----
# 如果配置了MinIO公开URL，直接返回
⋮----
# 否则通过后端代理访问
⋮----
# 创建全局存储服务实例
storage_service = StorageService()
````

## File: backend/services/structured_export_service.py
````python
"""
语料导出服务
将表格数据转换为机器学习训练格式，配置由处理器驱动
"""
⋮----
logger = logging.getLogger(__name__)
⋮----
class StructuredExportService
⋮----
"""语料导出器 - 支持三种导出格式，配置由处理器驱动"""
⋮----
def __init__(self, processor_name: str = 'kf')
⋮----
"""初始化导出器"""
⋮----
def _get_field_value(self, record: Dict, field_name: str, use_default: bool = False) -> str
⋮----
"""获取字段值"""
value = record.get(field_name, '')
⋮----
def _has_valid_value(self, record: Dict, field_name: str) -> bool
⋮----
"""检查字段是否有有效值（非空且非"未分类"）"""
⋮----
def _extract_image_path(self, markdown_img: str) -> Optional[str]
⋮----
"""从Markdown格式提取图片路径"""
⋮----
pattern = r'!\[.*?\]\((.*?)\)'
match = re.search(pattern, markdown_img)
⋮----
@staticmethod
    def _record_image_paths(record: Dict) -> List[str]
⋮----
"""Collect normalized image paths from export record metadata."""
raw_paths = record.get('_image_paths') or []
⋮----
def _generate_sample_id(self, record: Dict, index: int, format_type: str) -> str
⋮----
"""生成唯一样本ID"""
event_id_field = self.config.event_id_field
qr_id = record.get(event_id_field, 'unknown')
⋮----
@staticmethod
    def _build_space_map(text: str)
⋮----
"""
        预计算空格映射表，将无空格文本的索引映射回原文索引。
        返回 (text_clean, clean_to_orig) 其中 clean_to_orig[i] = 原文中第 i 个非空格字符的位置。
        一次构建，所有实体复用。
        """
clean_to_orig = []
chars = []
⋮----
"""
        在文本中查找实体的精确位置。
        space_map: 可选的预计算结果 (text_clean, clean_to_orig)，避免每次重建。
        """
⋮----
# 快速路径：精确匹配
index = text.find(entity_value, start_search)
⋮----
# 慢速路径：去空格模糊匹配，使用预计算映射表 O(1) 回映
entity_clean = entity_value.replace(' ', '')
⋮----
# 将 start_search 转换为 clean 索引
clean_start = 0
⋮----
# 二分查找第一个 >= start_search 的 clean 索引
⋮----
mid = (lo + hi) // 2
⋮----
lo = mid + 1
⋮----
hi = mid
clean_start = lo
⋮----
index_clean = text_clean.find(entity_clean, clean_start)
⋮----
orig_start = clean_to_orig[index_clean]
orig_end = clean_to_orig[index_clean + len(entity_clean) - 1] + 1
⋮----
def export_entity_text(self, json_data: List[Dict], data_source: str = None) -> List[Dict]
⋮----
"""导出实体标注文本格式"""
results = []
fm = self.field_mapping
images_field = fm.get('images', '')
event_id_field = fm.get('event_id', '')
classification_field = fm.get('classification', '')
problem_analysis_field = fm.get('problem_analysis', '')
customer_field = fm.get('customer', '')
product_model_field = fm.get('product_model', '')
defect_field = fm.get('defect', '')
short_term_field = fm.get('short_term_measure', '')
long_term_field = fm.get('long_term_measure', '')
four_m_field = fm.get('four_m_element', '')
industry_field = fm.get('industry_category', '')
product_cat_field = fm.get('product_category', '')
process_field = fm.get('process_category', '')
root_cause_field = fm.get('root_cause_category', '')
occurrence_field = fm.get('occurrence_time', '')
⋮----
record_data_source = record.get('_data_source', data_source or 'unknown')
⋮----
# 尝试由处理器构建文本
processor_text = self._processor.build_entity_text(record, record_data_source)
⋮----
text = processor_text
⋮----
# 回退：KF 原有文本构建逻辑
# 提取图片路径
image_path = self._extract_image_path(record.get(images_field, ''))
full_image_path = f"{record_data_source}/{image_path}" if image_path else None
⋮----
# 构建图片子句
⋮----
image_clause = f'问题图片已记录在路径"{full_image_path}"。'
⋮----
image_clause = ''
⋮----
# 构建分类子句
classification = record.get(classification_field)
⋮----
classification_clause = f'该产品所属分类为{classification}。'
⋮----
classification_clause = ''
⋮----
# 构建分类信息文本
classification_parts = []
⋮----
classification_text = '，'.join(classification_parts) + '。'
⋮----
classification_text = ''
⋮----
# 填充模板
text_parts = [
⋮----
problem_analysis = record.get(problem_analysis_field, '')
⋮----
customer = record.get(customer_field, '')
product_model = record.get(product_model_field, '')
⋮----
defect = record.get(defect_field, '')
⋮----
short_term = record.get(short_term_field, '')
long_term = record.get(long_term_field, '')
⋮----
text = '。'.join(text_parts) + '。'
⋮----
text = ' '.join(text.split())
⋮----
# 提取实体和关系
entities = []
relations = []
entity_id = 0
entity_map = {}
⋮----
# 预计算空格映射表，所有实体复用
space_map = self._build_space_map(text)
⋮----
search_pos = 0
⋮----
offset = self._find_entity_offset(text, value, search_pos, space_map=space_map)
⋮----
entity = {
⋮----
search_pos = offset[1]
⋮----
# 构建关系
relation_id = 0
event_id_entity = entity_map.get(event_id_field)
⋮----
target_id = entity_map.get(field_name)
⋮----
result = {
⋮----
def export_clip_alignment(self, json_data: List[Dict], data_source: str = None) -> List[Dict]
⋮----
"""导出CLIP风格的图文对齐格式"""
⋮----
images_field = self.field_mapping.get('images', '')
⋮----
record_paths = self._record_image_paths(record)
image_path = record_paths[0] if record_paths else None
⋮----
full_image_path = f"{record_data_source}/{image_path}"
⋮----
# 构建caption - 使用配置中的字段顺序
caption_parts = []
⋮----
value = record.get(field_key, '')
⋮----
caption = '，'.join(caption_parts)
⋮----
def export_qa_alignment(self, json_data: List[Dict], data_source: str = None) -> List[Dict]
⋮----
"""导出Q&A风格的多模态对齐格式"""
⋮----
# 构建assistant回答
answer_parts = []
⋮----
classification_info = []
⋮----
measures = []
⋮----
assistant_text = '。'.join(answer_parts) + '。'
⋮----
assistant_text = '暂无详细信息。'
⋮----
assistant_text = ' '.join(assistant_text.split())
⋮----
def batch_export(self, json_data: List[Dict], export_formats: List[str], include_images: bool = False) -> Dict
⋮----
"""
        批量导出多种格式

        Args:
            json_data: 解析后的JSON数据列表
            export_formats: 要导出的格式列表 ['entity_text', 'clip_alignment', 'qa_alignment']
            include_images: 是否在ZIP中包含图片文件

        Returns:
            包含各格式结果的字典，include_images=True 时额外包含 'image_files' 列表
            每项为 (zip内路径, 本地绝对路径)
        """
results = {}
⋮----
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
collected: Dict[str, Path] = {}  # zip内路径 → 本地路径，去重
⋮----
data_source = record.get('_data_source', '')
⋮----
raw_img = record.get(images_field, '')
image_rel_paths = self._record_image_paths(record)
img_rel = self._extract_image_path(raw_img)
⋮----
image_rel_paths = [img_rel, *[path for path in image_rel_paths if path != img_rel]]
⋮----
local_path = settings.IMAGE_DIR / rel_path
⋮----
normalized_rel_path = rel_path.replace('\\', '/')
zip_path = f"images/{normalized_rel_path}"
⋮----
local_path = settings.PROCESSED_DIR / self.processor_name / data_source / img_rel
⋮----
zip_path = f"images/{data_source}/{img_rel}"
⋮----
imgs_dir = settings.PROCESSED_DIR / self.processor_name / data_source / 'imgs'
⋮----
zip_path = f"images/{data_source}/imgs/{f.name}"
````

## File: backend/services/task_query_service.py
````python
"""
任务查询服务
提供基于角色的任务查询和权限检查功能
"""
⋮----
class TaskQueryService
⋮----
"""任务查询服务"""
⋮----
def __init__(self, db: Session)
⋮----
"""
        获取用户可访问的任务列表
        
        Args:
            user_id: 用户ID
            user_role: 用户角色 (admin/annotator/viewer)
            dataset_id: 数据集ID筛选（可选）
            status: 状态筛选（可选）
            page: 页码
            page_size: 每页数量
            sort_by: 排序字段
            sort_order: 排序方向
        
        Returns:
            (任务列表, 总数)
        """
# 构建基础查询
query = self._build_task_query(dataset_id, status)
⋮----
# 应用权限过滤
query = self._apply_permission_filter(query, user_id, user_role, dataset_id)
⋮----
# 获取总数
# 特殊排序：状态优先，本地排序以避免不同数据库的兼容性问题
⋮----
tasks_all = query.all()
total = len(tasks_all)
⋮----
def _priority(t: AnnotationTask)
⋮----
order = {
⋮----
offset = (page - 1) * page_size
tasks = tasks_all[offset:offset + page_size]
⋮----
total = query.count()
query = self._apply_sorting(query, sort_by, sort_order)
⋮----
tasks = query.offset(offset).limit(page_size).all()
⋮----
"""
        检查用户是否有权限访问指定任务
        
        Args:
            user_id: 用户ID
            user_role: 用户角色
            task_id: 任务ID
        
        Returns:
            是否有权限
        """
# 获取任务
task = self.db.query(AnnotationTask).filter(
⋮----
# 管理员有所有权限
⋮----
# 浏览员只能访问已完成的任务
⋮----
# 标注员需要检查分配
⋮----
"""
        构建基础任务查询
        
        Args:
            dataset_id: 数据集ID筛选
            status: 状态筛选
        
        Returns:
            Query对象
        """
query = self.db.query(AnnotationTask)
⋮----
# 数据集筛选
⋮----
query = query.filter(AnnotationTask.dataset_id == dataset_id)
⋮----
# 状态筛选
⋮----
query = query.filter(AnnotationTask.status == status)
⋮----
"""
        应用权限过滤
        
        Args:
            query: 查询对象
            user_id: 用户ID
            user_role: 用户角色
            dataset_id: 数据集ID（可选）
        
        Returns:
            过滤后的查询对象
        """
# 管理员可以访问所有任务
⋮----
# 标注员只能访问分配给他们的任务
⋮----
# 其他角色无权限，返回空查询
⋮----
"""
        应用标注员权限过滤
        
        Args:
            query: 查询对象
            user_id: 用户ID
            dataset_id: 数据集ID（可选）
        
        Returns:
            过滤后的查询对象
        """
# 获取用户的所有活跃分配
assignments_query = self.db.query(DatasetAssignment).filter(
⋮----
# 如果指定了数据集，只获取该数据集的分配
⋮----
assignments_query = assignments_query.filter(
⋮----
assignments = assignments_query.all()
⋮----
# 没有分配，返回空查询
⋮----
# 构建权限条件
permission_conditions = []
⋮----
# 如果是整体分配（task_start_index 和 task_end_index 为 NULL）
⋮----
# 该数据集的所有任务
⋮----
# 范围分配，需要使用子查询来计算任务索引
# 使用窗口函数 ROW_NUMBER() 来计算任务在数据集中的索引
⋮----
# 应用权限条件（OR关系）
⋮----
query = query.filter(or_(*permission_conditions))
⋮----
query = query.filter(False)
⋮----
"""
        创建任务范围条件
        
        Args:
            dataset_id: 数据集ID
            start_index: 起始索引
            end_index: 结束索引
        
        Returns:
            条件表达式
        """
# 获取该数据集中指定范围的任务ID列表
# 按ID排序后取指定范围
tasks_in_range = self.db.query(AnnotationTask.id)\
⋮----
task_ids = [task.id for task in tasks_in_range]
⋮----
"""
        检查标注员是否有权限访问指定任务
        
        Args:
            user_id: 用户ID
            task: 任务对象
        
        Returns:
            是否有权限
        """
# 获取用户在该数据集的分配
task_range = self.assignment_service.get_user_task_range(
⋮----
# 如果是整体分配
⋮----
# 如果是范围分配，需要计算任务在数据集中的索引
task_index = self._get_task_index_in_dataset(task.id, task.dataset_id)
⋮----
# 检查任务索引是否在分配范围内
⋮----
"""
        获取任务在数据集中的索引（从1开始）
        
        Args:
            task_id: 任务ID
            dataset_id: 数据集ID
        
        Returns:
            任务索引，如果任务不存在返回None
        """
# 获取该数据集的所有任务ID（按ID排序）
task_ids = self.db.query(AnnotationTask.id)\
⋮----
task_ids = [t.id for t in task_ids]
⋮----
# 索引从1开始
⋮----
"""
        应用排序
        
        Args:
            query: 查询对象
            sort_by: 排序字段
            sort_order: 排序方向
        
        Returns:
            排序后的查询对象
        """
# 自定义状态优先级排序：processing -> pending -> failed -> completed -> reviewed
⋮----
priority = case(
# 状态优先，次序按创建时间倒序
⋮----
# 若排序构造异常则降级为按创建时间倒序
⋮----
sort_by = 'created_at'
⋮----
# 验证排序字段
valid_sort_fields = ['created_at', 'updated_at', 'status', 'id']
⋮----
# 获取排序字段
sort_field = getattr(AnnotationTask, sort_by)
⋮----
# 应用排序方向
⋮----
query = query.order_by(sort_field.asc())
⋮----
query = query.order_by(sort_field.desc())
````

## File: backend/services/user_service.py
````python
"""
用户管理服务
实现用户CRUD、密码加密、JWT Token生成和权限检查
"""
⋮----
class UserService
⋮----
"""用户管理服务类"""
⋮----
# JWT配置
SECRET_KEY = settings.SECRET_KEY if hasattr(settings, 'SECRET_KEY') else "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时
⋮----
def __init__(self, db: Session)
⋮----
@staticmethod
    def hash_password(password: str) -> str
⋮----
"""
        密码加密
        
        Args:
            password: 明文密码
        
        Returns:
            str: 加密后的密码哈希
        """
# 使用bcrypt加密
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
⋮----
@staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool
⋮----
"""
        验证密码
        
        Args:
            plain_password: 明文密码
            hashed_password: 加密后的密码哈希
        
        Returns:
            bool: 密码是否匹配
        """
⋮----
"""
        创建用户
        
        Args:
            username: 用户名
            password: 密码
            role: 角色（admin/annotator/viewer）
        
        Returns:
            User: 创建的用户
        
        Raises:
            ValueError: 用户名已存在或角色无效
        """
# 验证角色（Task 47: 添加 reviewer 角色）
valid_roles = ['admin', 'annotator', 'reviewer', 'viewer']
⋮----
# 检查用户名是否已存在
existing_user = self.db.query(User).filter(
⋮----
# 创建用户
user = User(
⋮----
def get_user_by_id(self, user_id: int) -> Optional[User]
⋮----
"""
        根据ID获取用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 用户对象，不存在则返回None
        """
⋮----
def get_user_by_username(self, username: str) -> Optional[User]
⋮----
"""
        根据用户名获取用户
        
        Args:
            username: 用户名
        
        Returns:
            Optional[User]: 用户对象，不存在则返回None
        """
⋮----
"""
        获取用户列表
        
        Args:
            role: 角色筛选
            skip: 跳过记录数
            limit: 返回记录数
        
        Returns:
            tuple: (用户列表, 总数)
        """
query = self.db.query(User)
⋮----
# 角色筛选
⋮----
query = query.filter(User.role == role)
⋮----
# 获取总数
total = query.count()
⋮----
# 分页查询
users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
⋮----
"""
        更新用户信息
        
        Args:
            user_id: 用户ID
            username: 新用户名（可选）
            password: 新密码（可选）
            role: 新角色（可选）
        
        Returns:
            User: 更新后的用户
        
        Raises:
            ValueError: 用户不存在或用户名已被占用
        """
user = self.get_user_by_id(user_id)
⋮----
# 更新用户名
⋮----
# 检查新用户名是否已被占用
existing = self.db.query(User).filter(
⋮----
# 更新密码
⋮----
# 更新角色（Task 47: 添加 reviewer 角色）
⋮----
def delete_user(self, user_id: int) -> bool
⋮----
"""
        删除用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 是否删除成功
        
        Raises:
            ValueError: 用户不存在
        """
⋮----
def authenticate(self, username: str, password: str) -> Optional[User]
⋮----
"""
        用户认证
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            Optional[User]: 认证成功返回用户对象，失败返回None
        """
user = self.get_user_by_username(username)
⋮----
def authenticate_user(self, username: str, password: str) -> Optional[User]
⋮----
"""
        用户认证（别名方法，与authenticate相同）
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            Optional[User]: 认证成功返回用户对象，失败返回None
        """
⋮----
"""
        创建JWT访问令牌
        
        Args:
            user_id: 用户ID
            username: 用户名
            role: 角色
        
        Returns:
            str: JWT令牌
        """
expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
⋮----
payload = {
⋮----
token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
⋮----
def verify_token(self, token: str) -> Optional[Dict[str, Any]]
⋮----
"""
        验证JWT令牌
        
        Args:
            token: JWT令牌
        
        Returns:
            Optional[Dict]: 令牌有效返回payload，无效返回None
        """
⋮----
payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
⋮----
# 令牌已过期
⋮----
# 令牌无效
⋮----
"""
        检查用户权限
        
        Args:
            user_id: 用户ID
            required_role: 需要的角色
        
        Returns:
            bool: 是否有权限
        """
⋮----
# 管理员拥有所有权限
⋮----
# 检查角色匹配
⋮----
def can_review(self, user_id: int, task_assigned_to: Optional[int] = None) -> bool
⋮----
"""
        检查用户是否可以进行复核
        
        Args:
            user_id: 用户ID
            task_assigned_to: 任务分配给的用户ID（可选）
        
        Returns:
            bool: 是否可以复核
        """
⋮----
# 管理员可以复核所有任务
⋮----
# 标注员可以复核他人的任务
⋮----
# 如果提供了任务分配信息，检查是否是自己的任务
⋮----
# 如果没有提供任务分配信息，默认允许（在API层再做详细检查）
⋮----
# 浏览员不能复核
⋮----
def get_user_statistics(self) -> Dict[str, Any]
⋮----
"""
        获取用户统计信息
        
        Returns:
            Dict: 统计信息
        """
total_users = self.db.query(User).count()
admin_count = self.db.query(User).filter(User.role == 'admin').count()
annotator_count = self.db.query(User).filter(User.role == 'annotator').count()
reviewer_count = self.db.query(User).filter(User.role == 'reviewer').count()
````

## File: backend/services/version_management_service.py
````python
"""
版本管理服务
提供标注任务的版本控制功能,包括版本创建、历史查询、回滚和比较
"""
⋮----
class VersionManagementService
⋮----
"""版本管理服务"""
⋮----
def __init__(self, db: Session)
⋮----
"""
        初始化服务
        
        Args:
            db: 数据库会话
        """
⋮----
"""
        创建版本快照
        
        Args:
            task_id: 任务ID
            change_type: 变更类型 ('create', 'update', 'delete')
            change_description: 变更描述
            changed_by: 变更人ID
            
        Returns:
            VersionHistory: 版本历史对象
        """
# 查询任务
task = self.db.query(AnnotationTask).filter(
⋮----
# 生成版本ID
history_id = f"version-{uuid.uuid4().hex[:12]}"
⋮----
# 获取当前版本号
current_version = task.current_version
⋮----
# 创建快照数据
snapshot_data = self._create_snapshot(task, current_version)
⋮----
# 创建版本历史记录
version_history = VersionHistory(
⋮----
"""
        获取版本历史
        
        Args:
            task_id: 任务ID
            limit: 返回数量限制
            
        Returns:
            List[Dict]: 版本历史列表
        """
⋮----
# 查询版本历史
query = self.db.query(VersionHistory)\
⋮----
query = query.limit(limit)
⋮----
histories = query.all()
⋮----
# 格式化返回数据
result = []
⋮----
"""
        回滚到指定版本
        
        Args:
            task_id: 任务ID
            target_version: 目标版本号
            changed_by: 操作人ID
            
        Returns:
            bool: 是否回滚成功
        """
⋮----
# 查询目标版本
target_history = self.db.query(VersionHistory)\
⋮----
# 如果已经是当前版本,无需回滚
⋮----
# 先创建当前版本的快照(作为回滚前的备份)
⋮----
# 解析目标版本的快照数据
snapshot_data = json.loads(target_history.snapshot_data)
⋮----
# 恢复数据
⋮----
# 更新任务的当前版本号
⋮----
# 创建回滚记录
⋮----
"""
        比较两个版本的差异
        
        Args:
            task_id: 任务ID
            version1: 版本1
            version2: 版本2
            
        Returns:
            Dict: 版本差异信息
        """
⋮----
# 查询两个版本
history1 = self.db.query(VersionHistory)\
⋮----
history2 = self.db.query(VersionHistory)\
⋮----
# 解析快照数据
snapshot1 = json.loads(history1.snapshot_data)
snapshot2 = json.loads(history2.snapshot_data)
⋮----
# 计算差异
diff = self._calculate_diff(snapshot1, snapshot2)
⋮----
"""
        创建任务快照
        
        Args:
            task: 标注任务对象
            version: 版本号
            
        Returns:
            Dict: 快照数据
        """
# 查询文本实体
text_entities = self.db.query(TextEntity)\
⋮----
# 查询图片实体
image_entities = self.db.query(ImageEntity)\
⋮----
# 查询关系
relations = self.db.query(Relation)\
⋮----
# 构建快照数据
snapshot = {
⋮----
"""
        恢复快照数据
        
        Args:
            task: 标注任务对象
            snapshot_data: 快照数据
            target_version: 目标版本号
        """
# 删除当前版本的所有数据
⋮----
# 恢复文本实体
⋮----
entity = TextEntity(
⋮----
# 恢复图片实体
⋮----
image_entity = ImageEntity(
⋮----
# 恢复关系
⋮----
relation = Relation(
⋮----
# 更新任务信息
task_info = snapshot_data.get('task_info', {})
⋮----
"""
        计算两个快照的差异
        
        Args:
            snapshot1: 快照1
            snapshot2: 快照2
            
        Returns:
            Dict: 差异信息
        """
def compare_lists(list1, list2, id_key)
⋮----
"""比较两个列表的差异"""
dict1 = {item[id_key]: item for item in list1}
dict2 = {item[id_key]: item for item in list2}
⋮----
added = [dict2[k] for k in dict2 if k not in dict1]
removed = [dict1[k] for k in dict1 if k not in dict2]
modified = []
⋮----
# 比较实体
entities_diff = compare_lists(
⋮----
# 比较图片实体
image_entities_diff = compare_lists(
⋮----
# 比较关系
relations_diff = compare_lists(
````

## File: backend/utils/__init__.py
````python
"""
工具函数包
"""
````

## File: backend/utils/file_utils.py
````python
"""文件名规范化工具"""
⋮----
def sanitize_filename(filename: str) -> str
⋮----
"""
    规范化文件名，保留中文、英文、数字，其他字符替换为下划线
    """
⋮----
sanitized = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '_', name)
⋮----
def rename_all_files(root_path: str)
⋮----
"""遍历目录下所有文件并规范化文件名"""
⋮----
old_path = os.path.join(root, file)
new_name = sanitize_filename(file)
new_path = os.path.join(root, new_name)
````

## File: frontend/.env.development
````
# 开发环境配置
VITE_API_BASE_URL=/api/v1
VITE_DEV_PROXY_TARGET=http://127.0.0.1:18080
VITE_BACKEND_ORIGIN=
VITE_APP_TITLE=面向离散型电子信息制造业的多模态语料库构建平台
````

## File: frontend/.env.production
````
# 生产环境配置
VITE_API_BASE_URL=/api/v1
VITE_BACKEND_ORIGIN=
VITE_APP_TITLE=面向离散型电子信息制造业的多模态语料库构建平台
````

## File: frontend/index.html
````html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>面向离散型电子信息制造业的多模态语料库构建平台</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
````

## File: frontend/src/api/annotation.ts
````typescript
/**
 * 标注任务API
 */
import { request } from './request'
⋮----
export interface BatchAnnotationRequest {
  dataset_id: string
  task_ids?: string[]  // 可选：指定要标注的任务ID列表
}
⋮----
task_ids?: string[]  // 可选：指定要标注的任务ID列表
⋮----
export interface BatchJobResponse {
  job_id: string
  dataset_id: string
  status: string
  total_tasks: number
}
⋮----
export interface BatchJobStats {
  job_id: string
  dataset_id: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  total_tasks: number
  completed_tasks: number
  failed_tasks: number
  processing_tasks: number
  started_at?: string
  completed_at?: string
}
⋮----
/**
   * 获取任务列表（跨数据集）
   */
getTaskList(params?: {
    dataset_id?: string
    status?: string
    page?: number
    page_size?: number
    sort_by?: string
    sort_order?: string
})
⋮----
/**
   * 触发批量自动标注
   */
triggerBatchAnnotation(data: BatchAnnotationRequest)
⋮----
/**
   * 获取批量任务状态
   */
getBatchJobStatus(jobId: string)
⋮----
/**
   * 取消批量任务
   */
cancelBatchJob(jobId: string)
⋮----
/**
   * 获取标注任务详情
   */
getAnnotationTask(taskId: string)
⋮----
/**
   * 更新标注任务
   */
updateAnnotationTask(taskId: string, data: any)
⋮----
/**
   * 添加文本实体
   */
addTextEntity(taskId: string, data: any)
⋮----
/**
   * 更新文本实体
   */
updateTextEntity(taskId: string, entityId: number, data: any)
⋮----
/**
   * 删除文本实体
   */
deleteTextEntity(taskId: string, entityId: number)
⋮----
/**
   * 添加关系
   */
addRelation(taskId: string, data: any)
⋮----
/**
   * 更新关系
   */
updateRelation(taskId: string, relationId: number, data: any)
⋮----
/**
   * 删除关系
   */
deleteRelation(taskId: string, relationId: number)
````

## File: frontend/src/api/auth.ts
````typescript
import { request } from './request'
import type { LoginRequest, LoginResponse, User } from '@/types'
⋮----
// 登录
login(data: LoginRequest): Promise<LoginResponse>
⋮----
// 登出
logout(): Promise<void>
⋮----
// 获取当前用户信息
getCurrentUser(): Promise<User>
````

## File: frontend/src/api/corpus.ts
````typescript
/**
 * 语料管理API
 */
import { request } from './request'
import type { Corpus, PaginatedResponse } from '@/types'
⋮----
// Excel上传响应
export interface ExcelUploadResponse {
  success: boolean
  message: string
  total_records: number
  total_sentences: number
  total_images: number
  field_distribution: Record<string, number>
}
⋮----
/**
   * 上传Excel文件
   */
upload(file: File)
⋮----
/**
   * 获取语料列表
   */
list(params?: {
    page?: number
    page_size?: number
    source_file?: string
    source_field?: string  // 修改为 source_field 以匹配后端
    has_images?: boolean
})
⋮----
source_field?: string  // 修改为 source_field 以匹配后端
⋮----
/**
   * 获取语料详情
   */
get(id: number)
⋮----
/**
   * 删除语料（使用text_id）
   */
delete(textId: string)
⋮----
/**
   * 获取语料关联图片
   */
getImages(id: number)
````

## File: frontend/src/api/dataset.ts
````typescript
/**
 * 数据集管理API
 */
import { request } from './request'
import type { Dataset, PaginatedResponse } from '@/types'
import type {
  AssignmentRequest,
  AutoAssignmentRequest,
  TransferAssignmentRequest,
  AssignmentInfo,
  AutoAssignmentInfo,
  MyDatasetInfo,
  AssignmentListData,
  MyDatasetsData,
  TransferResult
} from '@/types/assignment'
⋮----
/**
   * 创建数据集
   */
create(data: {
    name: string
    description?: string
    corpus_ids: number[]
    created_by: number
    label_schema_version_id?: number
})
⋮----
/**
   * 获取数据集列表
   */
list(params?: {
    page?: number
    page_size?: number
    created_by?: number
})
⋮----
/**
   * 获取数据集详情
   */
get(id: string | number)
⋮----
/**
   * 更新数据集
   */
update(id: number, data: {
    name?: string
    description?: string
    label_schema_version_id?: number
})
⋮----
/**
   * 删除数据集
   */
delete(datasetId: string)
⋮----
/**
   * 导出数据集
   */
export(datasetId: string, params?: {
    output_path?: string
    status_filter?: string[]
})
⋮----
/**
   * 获取数据集的任务列表
   */
getTasks(datasetId: string, params?: {
    page?: number
    page_size?: number
    status?: string
})
⋮----
/**
   * 向数据集添加语料（创建新任务，自动去重）
   */
addTasks(datasetId: string, corpusIds: number[])
⋮----
/**
   * 从数据集删除一个任务（级联删除实体/关系）
   */
removeTask(datasetId: string, taskId: string)
⋮----
// ============================================================================
// 数据集分配相关API (Task 47)
// ============================================================================
⋮----
/**
   * 分配数据集（整体或范围）
   */
assign(datasetId: string, data: AssignmentRequest)
⋮----
/**
   * 自动平均分配数据集
   */
autoAssign(datasetId: string, data: AutoAssignmentRequest)
⋮----
/**
   * 批量分配
   */
batchAssign(datasetId: string, data: {
    assignments: Array<{
      user_id: number
      role: string
      mode: string
      start_index?: number
      end_index?: number
    }>
    clear_existing: boolean
    role_filter?: string
})
⋮----
/**
   * 取消分配
   */
cancelAssignment(datasetId: string, userId: number, role: string, force: boolean = false)
⋮----
/**
   * 批量清空分配
   */
clearAssignments(datasetId: string, role?: string, force: boolean = false)
⋮----
/**
   * 转移分配
   */
transferAssignment(datasetId: string, data: TransferAssignmentRequest)
⋮----
/**
   * 获取数据集分配情况
   */
getAssignments(datasetId: string, includeInactive: boolean = false)
⋮----
/**
   * 获取我的数据集
   */
getMyDatasets(params?: {
    role?: string
    page?: number
    page_size?: number
})
````

## File: frontend/src/api/document.ts
````typescript
/**
 * 文档管理 API - KF/QMS 文档上传、处理和导出
 */
import type { AxiosProgressEvent } from 'axios'
import { request } from './request'
import type {
  ProcessorInfo,
  ProcessedFile,
  UploadResult,
  ImportResult,
  ExportResult,
  ExportFormat,
  BatchExportParams,
  StatisticsData
} from '@/types'
⋮----
// 本文件内部使用的响应包装类型（不在全局 types 中）
export interface ProcessedFilesResult {
  success: boolean
  files: ProcessedFile[]
  total: number
}
⋮----
export interface ProcessorListResult {
  processors: ProcessorInfo[]
}
⋮----
export interface FieldMappingResult {
  processor: string
  display_name: string
  field_mapping: Record<string, string>
}
⋮----
export interface StatisticsResult {
  success: boolean
  data: StatisticsData
  processor: string
}
⋮----
export interface DataListResult {
  success: boolean
  data: any[]
  count: number
  total_count?: number
  page?: number
  page_size?: number
  processor: string
}
⋮----
export interface TransferProgress {
  loaded: number
  total?: number
  percentage: number
}
⋮----
export interface TransferProgressOptions {
  onUploadProgress?: (progress: TransferProgress) => void
  onDownloadProgress?: (progress: TransferProgress) => void
}
⋮----
// Re-export shared types so consumers can import from one place
⋮----
// ============ API函数 ============
⋮----
const toTransferProgress = (event: AxiosProgressEvent): TransferProgress =>
⋮----
/**
   * 上传Excel文件
   */
uploadExcel(file: File, processorName: string, options?: TransferProgressOptions): Promise<UploadResult>
⋮----
/**
   * 导入JSON数据
   */
importJsonData(processorName: string, dataSource: string): Promise<ImportResult>
⋮----
/**
   * 上传图片ZIP包
   */
uploadImagesZip(file: File, dataSource: string, processorName: string, options?: TransferProgressOptions): Promise<any>
⋮----
/**
   * 查询指定数据源已上传图片数量
   */
getImagesInfo(dataSource: string): Promise<any>
⋮----
/**
   * 删除已处理文件
   */
deleteProcessedFile(processorName: string, dataSource: string): Promise<any>
⋮----
/**
   * 获取已处理文件列表
   */
getProcessedFiles(processorName: string): Promise<ProcessedFilesResult>
⋮----
/**
   * 获取处理器列表
   */
getProcessors(): Promise<ProcessorListResult>
⋮----
/**
   * 获取字段映射
   */
getFieldMapping(processorName: string): Promise<FieldMappingResult>
⋮----
/**
   * 获取数据列表
   */
getDataList(
    processorName: string,
    params?: { page?: number; page_size?: number; limit?: number; offset?: number }
): Promise<DataListResult>
⋮----
/**
   * 获取统计数据
   */
getStatistics(processorName: string): Promise<StatisticsResult>
⋮----
/**
   * 导出实体文本格式
   */
exportEntityText(processorName: string, dataSources?: string[]): Promise<ExportResult>
⋮----
/**
   * 导出CLIP对齐格式
   */
exportClipAlignment(processorName: string, dataSources?: string[]): Promise<ExportResult>
⋮----
/**
   * 导出QA对齐格式
   */
exportQaAlignment(processorName: string, dataSources?: string[]): Promise<ExportResult>
⋮----
/**
   * 批量导出（返回ZIP文件流）
   */
batchExport(processorName: string, params: BatchExportParams, options?: TransferProgressOptions): Promise<Blob>
⋮----
timeout: 300000, // 大文件导出单独设 5 分钟超时
````

## File: frontend/src/api/image.ts
````typescript
/**
 * 图片标注API
 */
import { request } from './request'
import type { ImageEntity } from '@/types'
⋮----
/**
   * 添加图片实体
   */
addEntity(imageId: number, data: {
    label: string
    annotation_type: 'whole_image' | 'region'
    bbox?: {
      x: number
      y: number
      width: number
      height: number
    }
})
⋮----
/**
   * 获取图片实体列表
   */
getEntities(imageId: number)
⋮----
/**
   * 更新图片实体
   */
updateEntity(imageId: number, entityId: number, data: {
    label?: string
    annotation_type?: 'whole_image' | 'region'
    bbox?: {
      x: number
      y: number
      width: number
      height: number
    }
})
⋮----
/**
   * 删除图片实体
   */
deleteEntity(imageId: number, entityId: number)
````

## File: frontend/src/api/index.ts
````typescript
/**
 * API统一导出
 */
````

## File: frontend/src/api/label.ts
````typescript
/**
 * 标签管理API
 */
import { request } from './request'
⋮----
// 实体类型接口
export interface EntityType {
  id: number
  type_name: string
  type_name_zh: string
  color: string
  description?: string
  definition?: string
  examples?: string[]
  disambiguation?: string
  supports_bbox: boolean
  is_active: boolean
  is_reviewed: boolean
  reviewed_by?: number
  reviewed_at?: string
  created_at: string
  updated_at?: string
}
⋮----
// 关系类型接口
export interface RelationType {
  id: number
  type_name: string
  type_name_zh: string
  color: string
  description?: string
  definition?: string
  direction_rule?: string
  examples?: string[]
  disambiguation?: string
  is_active: boolean
  is_reviewed: boolean
  reviewed_by?: number
  reviewed_at?: string
  created_at: string
  updated_at?: string
}
⋮----
// 标签体系版本接口
export interface LabelSchemaVersion {
  id: number
  version_id: string
  version_name: string
  description: string
  is_active: boolean
  entity_types: EntityType[]
  relation_types: RelationType[]
  created_by: number
  created_at: string
}
⋮----
// ============================================================================
// 实体类型管理
// ============================================================================
⋮----
/**
   * 获取实体类型列表
   */
listEntityTypes(params?: {
    include_inactive?: boolean
    include_unreviewed?: boolean
})
⋮----
/**
   * 创建实体类型
   */
createEntityType(data: {
    type_name: string
    type_name_zh: string
    color: string
    description?: string
    supports_bbox?: boolean
})
⋮----
/**
   * 更新实体类型
   */
updateEntityType(id: number, data: {
    type_name?: string
    type_name_zh?: string
    color?: string
    description?: string
    supports_bbox?: boolean
    is_active?: boolean
})
⋮----
/**
   * 删除实体类型
   */
deleteEntityType(id: number)
⋮----
/**
   * 生成实体类型定义
   */
generateEntityDefinition(id: number)
⋮----
/**
   * 审核实体类型定义
   */
reviewEntityType(id: number, data: {
    approved: boolean
    definition?: string
    examples?: string[]
    disambiguation?: string
})
⋮----
// ============================================================================
// 关系类型管理
// ============================================================================
⋮----
/**
   * 获取关系类型列表
   */
listRelationTypes(params?: {
    include_inactive?: boolean
    include_unreviewed?: boolean
})
⋮----
/**
   * 创建关系类型
   */
createRelationType(data: {
    type_name: string
    type_name_zh: string
    color: string
    description?: string
})
⋮----
/**
   * 更新关系类型
   */
updateRelationType(id: number, data: {
    type_name?: string
    type_name_zh?: string
    color?: string
    description?: string
    is_active?: boolean
})
⋮----
/**
   * 删除关系类型
   */
deleteRelationType(id: number)
⋮----
/**
   * 生成关系类型定义
   */
generateRelationDefinition(id: number)
⋮----
/**
   * 审核关系类型定义
   */
reviewRelationType(id: number, data: {
    approved: boolean
    definition?: string
    direction_rule?: string
    examples?: string[]
    disambiguation?: string
})
⋮----
// ============================================================================
// 导入导出
// ============================================================================
⋮----
/**
   * 导入标签配置
   */
importLabels(data: {
    entity_types: Partial<EntityType>[]
    relation_types: Partial<RelationType>[]
})
⋮----
/**
   * 导出标签配置
   */
exportLabels()
⋮----
// ============================================================================
// Prompt预览
// ============================================================================
⋮----
/**
   * 预览Agent Prompt
   */
previewPrompt(params?: {
    prompt_type?: 'entity' | 'relation' | 'image'
})
⋮----
// ============================================================================
// 版本管理
// ============================================================================
⋮----
/**
   * 获取版本列表
   */
listVersions()
⋮----
/**
   * 创建版本快照
   */
createSnapshot(data: {
    version_name: string
    description: string
    created_by: number
})
⋮----
/**
   * 获取版本详情
   */
getVersion(versionId: string)
⋮----
/**
   * 激活版本
   */
activateVersion(versionId: string)
⋮----
/**
   * 比较版本差异
   */
compareVersions(params: {
    version1: string
    version2: string
})
````

## File: frontend/src/api/request.ts
````typescript
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'
import { getApiBaseUrl } from '@/utils/backendUrl'
⋮----
// 创建axios实例
⋮----
// 请求拦截器
⋮----
// 添加认证token
⋮----
// 响应拦截器
⋮----
// 对已在业务侧显示的提示不重复弹出全局错误
⋮----
// 未认证，跳转登录
⋮----
// 封装请求方法
⋮----
get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
⋮----
post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
⋮----
put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
⋮----
delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
⋮----
upload<T = any>(url: string, formData: FormData, config?: AxiosRequestConfig): Promise<T>
⋮----
timeout: 300000, // 文件上传单独设 5 分钟超时
⋮----
// 下载文件
download(url: string, filename: string, config?: AxiosRequestConfig): Promise<void>
````

## File: frontend/src/api/review.ts
````typescript
/**
 * 复核管理API
 */
import { request } from './request'
import type { ReviewTask, ReviewStatistics, PaginatedResponse } from '@/types'
⋮----
/**
   * 提交复核
   */
submit(taskId: string, reviewerId?: number)
⋮----
/**
   * 获取复核任务列表
   */
list(params?: {
    page?: number
    page_size?: number
    status?: string
    reviewer_id?: number
    skip?: number
    limit?: number
})
⋮----
// 转换参数格式
⋮----
/**
   * 获取复核任务详情
   */
get(reviewId: string)
⋮----
/**
   * 批准任务
   */
approve(reviewId: string, data?: {
    reviewer_id?: number
    review_comment?: string
})
⋮----
reviewer_id: data?.reviewer_id || 1, // 临时使用固定ID
⋮----
/**
   * 驳回任务
   */
reject(reviewId: string, data: {
    reviewer_id?: number
    comment: string
    suggestions?: string
})
⋮----
reviewer_id: data.reviewer_id || 1, // 临时使用固定ID
⋮----
/**
   * 获取数据集质量统计
   */
getStatistics(datasetId: number)
⋮----
/**
   * 获取数据集复核摘要
   */
getSummary(datasetId: number)
````

## File: frontend/src/api/user.ts
````typescript
/**
 * 用户管理API
 */
import { request } from './request'
import type { User, PaginatedResponse } from '@/types'
⋮----
/**
   * 创建用户
   */
create(data: {
    username: string
    password: string
    role: 'admin' | 'annotator' | 'viewer'
})
⋮----
/**
   * 获取用户列表
   */
list(params?: {
    role?: string
    skip?: number
    limit?: number
})
⋮----
/**
   * 获取用户详情
   */
get(id: number)
⋮----
/**
   * 更新用户
   */
update(id: number, data: {
    username?: string
    password?: string
    role?: 'admin' | 'annotator' | 'viewer'
})
⋮----
/**
   * 删除用户
   */
delete(id: number)
⋮----
/**
   * 获取用户统计
   */
getStatistics(id: number)
````

## File: frontend/src/api/version.ts
````typescript
/**
 * 版本管理API
 */
import { request } from './request'
import type { Version, VersionDiff } from '@/types'
⋮----
/**
   * 获取版本历史
   */
getHistory(taskId: string)
⋮----
/**
   * 回滚版本
   */
rollback(taskId: string, data: {
    version: number
})
⋮----
/**
   * 比较版本差异
   */
compare(params: {
    task_id: string
    version_1: number
    version_2: number
})
⋮----
/**
   * 获取版本详情
   */
get(taskId: string, version: number)
⋮----
/**
   * 创建版本快照
   */
createSnapshot(taskId: string, data?: {
    comment?: string
})
````

## File: frontend/src/App.vue
````vue
<template>
  <div id="app">
    <router-view />
  </div>
</template>
⋮----
<script setup lang="ts">
// App root component
</script>
⋮----
<style>
#app {
  width: 100%;
  height: 100vh;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
````

## File: frontend/src/components/annotation/EntityHighlight.vue
````vue
<template>
  <span
    class="entity-highlight"
    :class="{ selected: isSelected, hovered: isHovered }"
    :style="highlightStyle"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
    @click="handleClick"
  >
    <slot />
    <span v-if="showLabel" class="entity-label">{{ label }}</span>
  </span>
</template>
⋮----
<span v-if="showLabel" class="entity-label">{{ label }}</span>
⋮----
<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  color: string
  label?: string
  isSelected?: boolean
  showLabel?: boolean
}

interface Emits {
  (e: 'click'): void
}

const props = withDefaults(defineProps<Props>(), {
  isSelected: false,
  showLabel: false
})

const emit = defineEmits<Emits>()

const isHovered = ref(false)

const highlightStyle = computed(() => {
  const baseColor = props.color || '#2196f3'
  
  return {
    '--entity-color': baseColor,
    '--entity-bg': `${baseColor}20`, // 20% opacity
    '--entity-border': baseColor,
    '--entity-hover-bg': `${baseColor}40`, // 40% opacity
    '--entity-selected-bg': '#ffeb3b40' // Yellow with 40% opacity
  }
})

const handleClick = () => {
  emit('click')
}
</script>
⋮----
<style scoped>
.entity-highlight {
  position: relative;
  background-color: var(--entity-bg);
  border-bottom: 2px solid var(--entity-border);
  cursor: pointer;
  transition: all 0.2s;
  padding: 2px 0;
}

.entity-highlight:hover {
  background-color: var(--entity-hover-bg);
}

.entity-highlight.selected {
  background-color: var(--entity-selected-bg);
  border-bottom-color: #fbc02d;
}

.entity-label {
  position: absolute;
  top: -20px;
  left: 0;
  font-size: 11px;
  padding: 2px 6px;
  background-color: var(--entity-color);
  color: white;
  border-radius: 3px;
  white-space: nowrap;
  z-index: 10;
  opacity: 0;
  transition: opacity 0.2s;
}

.entity-highlight:hover .entity-label {
  opacity: 1;
}
</style>
````

## File: frontend/src/components/annotation/EntityList.vue
````vue
<template>
  <div class="entity-list">
    <div class="list-header">
      <h3>实体列表 ({{ entities.length }})</h3>
    </div>

    <el-scrollbar>
      <div class="entity-items">
        <div
          v-for="entity in sortedEntities"
          :key="entity.id"
          class="entity-item"
          :class="{ selected: selectedEntityId === entity.id }"
          @click="handleSelect(entity.id!)"
        >
          <div class="entity-header">
            <el-tag
              :color="entity.color"
              :style="{ backgroundColor: entity.color, color: '#fff', border: 'none' }"
              size="small"
            >
              {{ entity.entity_type_name }}
            </el-tag>
            <el-button
              type="danger"
              size="small"
              text
              @click.stop="handleDelete(entity.id!)"
            >
              删除
            </el-button>
          </div>

          <div class="entity-text">
            "{{ entity.text }}"
          </div>

          <div class="entity-meta">
            <span class="offset-info">
              偏移量: {{ entity.start_offset }} - {{ entity.end_offset }}
            </span>
          </div>
        </div>

        <el-empty
          v-if="entities.length === 0"
          description="暂无实体"
          :image-size="80"
        />
      </div>
    </el-scrollbar>
  </div>
</template>
⋮----
<h3>实体列表 ({{ entities.length }})</h3>
⋮----
{{ entity.entity_type_name }}
⋮----
"{{ entity.text }}"
⋮----
偏移量: {{ entity.start_offset }} - {{ entity.end_offset }}
⋮----
<script setup lang="ts">
import { ref, computed } from 'vue'

interface Entity {
  id?: number
  text: string
  start_offset: number
  end_offset: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Props {
  entities: Entity[]
  text: string
}

interface Emits {
  (e: 'select', entityId: number): void
  (e: 'delete', entityId: number): void
  (e: 'update', entityId: number, updates: Partial<Entity>): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const selectedEntityId = ref<number | null>(null)

// 按偏移量排序实体
const sortedEntities = computed(() => {
  return [...props.entities].sort((a, b) => a.start_offset - b.start_offset)
})

const handleSelect = (entityId: number) => {
  selectedEntityId.value = entityId
  emit('select', entityId)
}

const handleDelete = (entityId: number) => {
  emit('delete', entityId)
  if (selectedEntityId.value === entityId) {
    selectedEntityId.value = null
  }
}
</script>
⋮----
<style scoped>
.entity-list {
  display: flex;
  flex-direction: column;
  height: 50%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
}

.list-header {
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
}

.list-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.entity-items {
  padding: 8px;
}

.entity-item {
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.entity-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.entity-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.entity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.entity-text {
  font-size: 14px;
  color: #303133;
  margin-bottom: 8px;
  word-break: break-word;
  line-height: 1.5;
}

.entity-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.offset-info {
  font-size: 12px;
  color: #909399;
}
</style>
````

## File: frontend/src/components/annotation/ImageAnnotationEditor.vue
````vue
<template>
  <div class="image-annotation-editor">
    <!-- 工具栏 -->
    <div class="toolbar">
      <el-radio-group v-model="annotationMode" size="small" :disabled="props.readonly">
        <el-radio-button value="whole">整图标注</el-radio-button>
        <el-radio-button value="region">区域标注</el-radio-button>
      </el-radio-group>

      <el-divider direction="vertical" />

      <el-button-group size="small">
        <el-button @click="zoomIn">
          <el-icon><ZoomIn /></el-icon>
        </el-button>
        <el-button @click="zoomOut">
          <el-icon><ZoomOut /></el-icon>
        </el-button>
        <el-button @click="resetZoom">
          <el-icon><RefreshRight /></el-icon>
        </el-button>
      </el-button-group>

      <span class="zoom-info">{{ Math.round(scale * 100) }}%</span>

      <el-divider direction="vertical" />

      <el-button
        v-if="selectedBBox && !props.readonly"
        type="danger"
        size="small"
        @click="deleteSelectedBBox"
      >
        删除选中区域
      </el-button>
      
      <span v-if="props.readonly" class="toolbar-hint readonly-hint">
        <el-icon><View /></el-icon>
        只读模式：仅可查看标注，不可编辑
      </span>
    </div>

    <!-- 图片显示区域 -->
    <div class="image-display-area">
      <div
        ref="containerRef"
        class="image-container"
        :class="{ 'region-mode': annotationMode === 'region' }"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @wheel="handleWheel"
      >
        <img
          ref="imageRef"
          :src="imageUrl"
          :style="imageStyle"
          @load="handleImageLoad"
          @click="handleImageClick"
        />

        <!-- 边界框层 -->
        <svg
          v-if="annotationMode === 'region'"
          class="bbox-layer"
          :style="imageStyle"
        >
          <!-- 已标注的边界框 -->
          <g
            v-for="bbox in bboxes"
            :key="bbox.id"
            @click.stop="selectBBox(bbox.id!)"
          >
            <rect
              :x="bbox.x * scale"
              :y="bbox.y * scale"
              :width="bbox.width * scale"
              :height="bbox.height * scale"
              :stroke="bbox.color"
              :stroke-width="selectedBBox === bbox.id ? 3 : 2"
              fill="none"
              :class="{ 'bbox-rect': true, 'selected': selectedBBox === bbox.id }"
            />
            <text
              :x="bbox.x * scale + 5"
              :y="bbox.y * scale + 20"
              class="bbox-label"
              :fill="bbox.color"
            >
              {{ bbox.entity_type_name }}
            </text>
          </g>

          <!-- 正在绘制的边界框 -->
          <rect
            v-if="drawingBBox"
            :x="drawingBBox.x"
            :y="drawingBBox.y"
            :width="drawingBBox.width"
            :height="drawingBBox.height"
            stroke="#409eff"
            stroke-width="2"
            stroke-dasharray="5,5"
            fill="rgba(64, 158, 255, 0.1)"
          />
        </svg>
      </div>

      <!-- 整图标注标签选择 -->
      <LabelSelector
        v-if="showLabelSelector && annotationMode === 'whole'"
        :position="labelSelectorPosition"
        :entity-types="entityTypes"
        @select="handleWholeImageLabel"
        @close="closeLabelSelector"
      />

      <!-- 区域标注标签选择 -->
      <LabelSelector
        v-if="showBBoxLabelSelector"
        :position="bboxLabelSelectorPosition"
        :entity-types="bboxEntityTypes"
        @select="handleBBoxLabel"
        @close="closeBBoxLabelSelector"
      />
    </div>

    <!-- 侧边面板 -->
    <div class="side-panel">
      <!-- 整图标注列表 -->
      <div v-if="annotationMode === 'whole'" class="annotation-list">
        <div class="list-header">
          <h3>整图标注 ({{ wholeImageEntities.length }})</h3>
        </div>
        <el-scrollbar>
          <div class="entity-items">
            <div
              v-for="entity in wholeImageEntities"
              :key="entity.id"
              class="entity-item"
            >
              <el-tag
                :color="entity.color"
                :style="{ backgroundColor: entity.color, color: '#fff', border: 'none' }"
                size="small"
              >
                {{ entity.entity_type_name }}
              </el-tag>
              <el-button
                v-if="!props.readonly"
                type="danger"
                size="small"
                text
                @click="deleteWholeImageEntity(entity.id!)"
              >
                删除
              </el-button>
            </div>
          </div>
        </el-scrollbar>
      </div>

      <!-- 区域标注列表 -->
      <div v-if="annotationMode === 'region'" class="annotation-list">
        <div class="list-header">
          <h3>区域标注 ({{ bboxes.length }})</h3>
        </div>
        <el-scrollbar>
          <div class="bbox-items">
            <div
              v-for="bbox in bboxes"
              :key="bbox.id"
              class="bbox-item"
              :class="{ selected: selectedBBox === bbox.id }"
              @click="selectBBox(bbox.id!)"
            >
              <el-tag
                :color="bbox.color"
                :style="{ backgroundColor: bbox.color, color: '#fff', border: 'none' }"
                size="small"
              >
                {{ bbox.entity_type_name }}
              </el-tag>
              <div class="bbox-coords">
                {{ Math.round(bbox.x) }}, {{ Math.round(bbox.y) }}, 
                {{ Math.round(bbox.width) }}, {{ Math.round(bbox.height) }}
              </div>
              <el-button
                v-if="!props.readonly"
                type="danger"
                size="small"
                text
                @click.stop="deleteBBox(bbox.id!)"
              >
                删除
              </el-button>
            </div>
          </div>
        </el-scrollbar>
      </div>
    </div>
  </div>
</template>
⋮----
<!-- 工具栏 -->
⋮----
<span class="zoom-info">{{ Math.round(scale * 100) }}%</span>
⋮----
<!-- 图片显示区域 -->
⋮----
<!-- 边界框层 -->
⋮----
<!-- 已标注的边界框 -->
⋮----
{{ bbox.entity_type_name }}
⋮----
<!-- 正在绘制的边界框 -->
⋮----
<!-- 整图标注标签选择 -->
⋮----
<!-- 区域标注标签选择 -->
⋮----
<!-- 侧边面板 -->
⋮----
<!-- 整图标注列表 -->
⋮----
<h3>整图标注 ({{ wholeImageEntities.length }})</h3>
⋮----
{{ entity.entity_type_name }}
⋮----
<!-- 区域标注列表 -->
⋮----
<h3>区域标注 ({{ bboxes.length }})</h3>
⋮----
{{ bbox.entity_type_name }}
⋮----
{{ Math.round(bbox.x) }}, {{ Math.round(bbox.y) }},
{{ Math.round(bbox.width) }}, {{ Math.round(bbox.height) }}
⋮----
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ZoomIn, ZoomOut, RefreshRight, View } from '@element-plus/icons-vue'
import LabelSelector from './LabelSelector.vue'
import type { EntityType } from '@/api/label'

interface ImageEntity {
  id?: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface BoundingBox {
  id?: number
  x: number
  y: number
  width: number
  height: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Props {
  imageUrl: string
  wholeImageEntities: ImageEntity[]
  bboxes: BoundingBox[]
  entityTypes: EntityType[]
  readonly?: boolean  // 添加只读模式支持
}

interface Emits {
  (e: 'add-whole-image-entity', entity: Omit<ImageEntity, 'id'>): void
  (e: 'delete-whole-image-entity', id: number): void
  (e: 'add-bbox', bbox: Omit<BoundingBox, 'id'>): void
  (e: 'update-bbox', id: number, bbox: Partial<BoundingBox>): void
  (e: 'delete-bbox', id: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const containerRef = ref<HTMLElement>()
const imageRef = ref<HTMLImageElement>()
const annotationMode = ref<'whole' | 'region'>('whole')
const scale = ref(1)
const translateX = ref(0)
const translateY = ref(0)
const imageNaturalWidth = ref(0)
const imageNaturalHeight = ref(0)

// 整图标注
const showLabelSelector = ref(false)
const labelSelectorPosition = ref({ x: 0, y: 0 })

// 区域标注
const showBBoxLabelSelector = ref(false)
const bboxLabelSelectorPosition = ref({ x: 0, y: 0 })
const drawingBBox = ref<{ x: number; y: number; width: number; height: number } | null>(null)
const isDrawing = ref(false)
const drawStartX = ref(0)
const drawStartY = ref(0)
const selectedBBox = ref<number | null>(null)
const pendingBBox = ref<{ x: number; y: number; width: number; height: number } | null>(null)

// 拖拽平移
const isPanning = ref(false)
const panStartX = ref(0)
const panStartY = ref(0)

// 只支持边界框的实体类型
const bboxEntityTypes = computed(() => {
  return props.entityTypes.filter(et => et.supports_bbox)
})

// 图片样式
const imageStyle = computed(() => {
  return {
    transform: `translate(${translateX.value}px, ${translateY.value}px) scale(${scale.value})`,
    transformOrigin: '0 0'
  }
})

// 处理图片加载
const handleImageLoad = () => {
  if (imageRef.value) {
    imageNaturalWidth.value = imageRef.value.naturalWidth
    imageNaturalHeight.value = imageRef.value.naturalHeight
  }
}

// 缩放
const zoomIn = () => {
  scale.value = Math.min(scale.value * 1.2, 5)
}

const zoomOut = () => {
  scale.value = Math.max(scale.value / 1.2, 0.1)
}

const resetZoom = () => {
  scale.value = 1
  translateX.value = 0
  translateY.value = 0
}

// 鼠标滚轮缩放
const handleWheel = (e: WheelEvent) => {
  e.preventDefault()
  if (e.deltaY < 0) {
    zoomIn()
  } else {
    zoomOut()
  }
}

// 整图标注：点击图片
const handleImageClick = (e: MouseEvent) => {
  if (props.readonly) return  // 只读模式下不允许标注
  if (annotationMode.value !== 'whole') return
  if (isDrawing.value) return

  // 显示标签选择菜单
  labelSelectorPosition.value = {
    x: e.clientX,
    y: e.clientY
  }
  showLabelSelector.value = true
}

// 整图标注：选择标签
const handleWholeImageLabel = (entityType: EntityType) => {
  const newEntity: Omit<ImageEntity, 'id'> = {
    entity_type_id: entityType.id,
    entity_type_name: entityType.type_name_zh,
    color: entityType.color
  }
  emit('add-whole-image-entity', newEntity)
  closeLabelSelector()
  ElMessage.success('整图标注添加成功')
}

// 关闭整图标签选择
const closeLabelSelector = () => {
  showLabelSelector.value = false
}

// 删除整图标注
const deleteWholeImageEntity = (id: number) => {
  emit('delete-whole-image-entity', id)
}

// 区域标注：鼠标按下
const handleMouseDown = (e: MouseEvent) => {
  if (props.readonly) return  // 只读模式下不允许绘制
  if (annotationMode.value !== 'region') return
  if (!imageRef.value) return

  const rect = imageRef.value.getBoundingClientRect()
  const x = (e.clientX - rect.left) / scale.value
  const y = (e.clientY - rect.top) / scale.value

  // 检查是否在图片范围内
  if (x < 0 || y < 0 || x > imageNaturalWidth.value || y > imageNaturalHeight.value) {
    return
  }

  isDrawing.value = true
  drawStartX.value = x
  drawStartY.value = y
  drawingBBox.value = {
    x: x * scale.value,
    y: y * scale.value,
    width: 0,
    height: 0
  }
}

// 区域标注：鼠标移动
const handleMouseMove = (e: MouseEvent) => {
  if (!isDrawing.value || !imageRef.value) return

  const rect = imageRef.value.getBoundingClientRect()
  const x = (e.clientX - rect.left) / scale.value
  const y = (e.clientY - rect.top) / scale.value

  const width = x - drawStartX.value
  const height = y - drawStartY.value

  drawingBBox.value = {
    x: Math.min(drawStartX.value, x) * scale.value,
    y: Math.min(drawStartY.value, y) * scale.value,
    width: Math.abs(width) * scale.value,
    height: Math.abs(height) * scale.value
  }
}

// 区域标注：鼠标释放
const handleMouseUp = (e: MouseEvent) => {
  if (!isDrawing.value || !drawingBBox.value) return

  isDrawing.value = false

  // 检查边界框大小
  if (drawingBBox.value.width < 10 || drawingBBox.value.height < 10) {
    drawingBBox.value = null
    ElMessage.warning('边界框太小，请重新绘制')
    return
  }

  // 保存待标注的边界框（原始坐标）
  pendingBBox.value = {
    x: drawingBBox.value.x / scale.value,
    y: drawingBBox.value.y / scale.value,
    width: drawingBBox.value.width / scale.value,
    height: drawingBBox.value.height / scale.value
  }

  // 显示标签选择菜单
  bboxLabelSelectorPosition.value = {
    x: e.clientX,
    y: e.clientY
  }
  showBBoxLabelSelector.value = true
  drawingBBox.value = null
}

// 区域标注：选择标签
const handleBBoxLabel = (entityType: EntityType) => {
  if (!pendingBBox.value) return

  const newBBox: Omit<BoundingBox, 'id'> = {
    ...pendingBBox.value,
    entity_type_id: entityType.id,
    entity_type_name: entityType.type_name_zh,
    color: entityType.color
  }

  emit('add-bbox', newBBox)
  closeBBoxLabelSelector()
  pendingBBox.value = null
  ElMessage.success('区域标注添加成功')
}

// 关闭区域标签选择
const closeBBoxLabelSelector = () => {
  showBBoxLabelSelector.value = false
  drawingBBox.value = null
  pendingBBox.value = null
}

// 选择边界框
const selectBBox = (id: number) => {
  selectedBBox.value = id
}

// 删除边界框
const deleteBBox = (id: number) => {
  emit('delete-bbox', id)
  if (selectedBBox.value === id) {
    selectedBBox.value = null
  }
}

// 删除选中的边界框
const deleteSelectedBBox = () => {
  if (selectedBBox.value) {
    deleteBBox(selectedBBox.value)
  }
}
</script>
⋮----
<style scoped>
.image-annotation-editor {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.toolbar-hint {
  font-size: 13px;
  color: #909399;
  margin-left: auto;
}

.readonly-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #409eff;
  font-weight: 500;
}

.zoom-info {
  font-size: 14px;
  color: #606266;
  min-width: 50px;
}

.image-display-area {
  flex: 1;
  position: relative;
  overflow: hidden;
  display: flex;
  gap: 20px;
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.image-container {
  flex: 1;
  position: relative;
  overflow: auto;
  cursor: grab;
}

.image-container.region-mode {
  cursor: crosshair;
}

.image-container img {
  display: block;
  max-width: none;
  user-select: none;
}

.bbox-layer {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: all;
}

.bbox-rect {
  cursor: pointer;
  transition: stroke-width 0.2s;
}

.bbox-rect:hover {
  stroke-width: 3 !important;
}

.bbox-rect.selected {
  stroke-width: 4 !important;
}

.bbox-label {
  font-size: 14px;
  font-weight: 500;
  pointer-events: none;
  text-shadow: 0 0 3px white, 0 0 3px white;
}

.side-panel {
  width: 300px;
  display: flex;
  flex-direction: column;
}

.annotation-list {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.list-header {
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
}

.list-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
}

.entity-items,
.bbox-items {
  padding: 8px;
}

.entity-item,
.bbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  margin-bottom: 8px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.entity-item:hover,
.bbox-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.bbox-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.bbox-coords {
  flex: 1;
  font-size: 12px;
  color: #909399;
}
</style>
````

## File: frontend/src/components/annotation/LabelSelector.vue
````vue
<template>
  <teleport to="body">
    <div
      v-if="visible"
      class="label-selector"
      :style="{ left: `${position.x}px`, top: `${position.y}px` }"
      @click.stop
    >
      <div class="label-selector-header">
        <span>选择实体类型</span>
        <el-icon class="close-icon" @click="handleClose">
          <Close />
        </el-icon>
      </div>
      
      <el-scrollbar max-height="300px">
        <div class="label-list">
          <div
            v-for="entityType in entityTypes"
            :key="entityType.id"
            class="label-item"
            @click="handleSelect(entityType)"
          >
            <el-tag
              :color="entityType.color"
              :style="{ backgroundColor: entityType.color, color: '#fff', border: 'none' }"
            >
              {{ entityType.type_name_zh }}
            </el-tag>
            <span class="label-description">{{ entityType.description }}</span>
          </div>
        </div>
      </el-scrollbar>
    </div>
  </teleport>
</template>
⋮----
{{ entityType.type_name_zh }}
⋮----
<span class="label-description">{{ entityType.description }}</span>
⋮----
<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { Close } from '@element-plus/icons-vue'
import type { EntityType } from '@/api/label'

interface Props {
  position: { x: number; y: number }
  entityTypes: EntityType[]
}

interface Emits {
  (e: 'select', entityType: EntityType): void
  (e: 'close'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const visible = ref(true)

console.log('[LabelSelector] Created with props:', {
  position: props.position,
  entityTypesCount: props.entityTypes.length,
  entityTypes: props.entityTypes
})

const handleSelect = (entityType: EntityType) => {
  emit('select', entityType)
}

const handleClose = () => {
  visible.value = false
  emit('close')
}

// 点击外部关闭
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.label-selector')) {
    handleClose()
  }
}

onMounted(() => {
  // 延迟添加点击外部监听器，避免与触发选择的 mouseup 事件冲突
  setTimeout(() => {
    document.addEventListener('click', handleClickOutside)
  }, 100)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
⋮----
<style scoped>
.label-selector {
  position: fixed;
  z-index: 9999;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  min-width: 250px;
  max-width: 400px;
  transform: translateX(-50%);
}

.label-selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
  font-weight: 500;
}

.close-icon {
  cursor: pointer;
  font-size: 16px;
}

.close-icon:hover {
  color: #409eff;
}

.label-list {
  padding: 8px 0;
}

.label-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.label-item:hover {
  background-color: #f5f7fa;
}

.label-description {
  flex: 1;
  font-size: 13px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
````

## File: frontend/src/components/annotation/RelationArrowLayer.vue
````vue
<template>
  <svg
    class="relation-arrow-layer"
    :width="width"
    :height="height"
    preserveAspectRatio="xMinYMin meet"
    @click="handleLayerClick"
  >
    <!-- 箭头标记定义 -->
    <defs>
      <marker
        v-for="relation in relations"
        :key="`marker-${relation.id}`"
        :id="`arrow-${relation.id}`"
        markerWidth="10"
        markerHeight="10"
        refX="9"
        refY="3"
        orient="auto"
        markerUnits="strokeWidth"
      >
        <polygon
          points="0 0, 10 3, 0 6"
          :fill="getRelationColor(relation)"
        />
      </marker>
    </defs>

    <!-- 绘制关系箭头 -->
    <g v-for="relation in relations" :key="relation.id">
      <!-- 箭头路径 -->
      <path
        :d="getArrowPath(relation)"
        :stroke="getRelationColor(relation)"
        :stroke-width="isSelected(relation.id) ? 3 : 2"
        fill="none"
        stroke-linecap="round"
        stroke-linejoin="round"
        :marker-end="`url(#arrow-${relation.id})`"
        :class="{ 
          'relation-arrow': true, 
          'selected': isSelected(relation.id),
          'hovered': hoveredRelationId === relation.id
        }"
        @click.stop="handleArrowClick(relation)"
        @mouseenter="hoveredRelationId = relation.id"
        @mouseleave="hoveredRelationId = null"
      />

      <!-- 关系标签 -->
      <g v-if="showLabels">
        <rect
          :x="getLabelPosition(relation).x - 35"
          :y="getLabelPosition(relation).y - 14"
          width="70"
          height="28"
          rx="6"
          :fill="getRelationColor(relation)"
          opacity="0.95"
        />
        <text
          :x="getLabelPosition(relation).x"
          :y="getLabelPosition(relation).y"
          class="relation-label"
          text-anchor="middle"
          dominant-baseline="middle"
        >
          {{ relation.relation_type_name }}
        </text>
      </g>
    </g>

    <!-- 临时箭头（创建关系时） -->
    <path
      v-if="tempArrow"
      :d="tempArrow.path"
      stroke="#409eff"
      stroke-width="2"
      stroke-dasharray="5,5"
      fill="none"
      marker-end="url(#temp-arrow)"
    />
    <defs v-if="tempArrow">
      <marker
        id="temp-arrow"
        markerWidth="10"
        markerHeight="10"
        refX="9"
        refY="3"
        orient="auto"
        markerUnits="strokeWidth"
      >
        <path d="M0,0 L0,6 L9,3 z" fill="#409eff" />
      </marker>
    </defs>
  </svg>
</template>
⋮----
<!-- 箭头标记定义 -->
⋮----
<!-- 绘制关系箭头 -->
⋮----
<!-- 箭头路径 -->
⋮----
<!-- 关系标签 -->
⋮----
{{ relation.relation_type_name }}
⋮----
<!-- 临时箭头（创建关系时） -->
⋮----
<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface Entity {
  id?: number
  text: string
  start_offset: number
  end_offset: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Relation {
  id?: number
  source_entity_id: string  // 字符串格式的entity_id
  target_entity_id: string  // 字符串格式的entity_id
  relation_type_id: number
  relation_type_name: string
  color?: string
}

interface EntityPosition {
  x: number
  y: number
  width: number
  height: number
}

interface Props {
  relations: Relation[]
  entities: Entity[]
  entityPositions: Map<string, EntityPosition>  // 键改为字符串类型的entity_id
  selectedRelationId?: number | null
  showLabels?: boolean
  width?: number
  height?: number
}

interface Emits {
  (e: 'select', relationId: number): void
  (e: 'delete', relationId: number): void
}

const props = withDefaults(defineProps<Props>(), {
  selectedRelationId: null,
  showLabels: true,
  width: 0,
  height: 0
})

const emit = defineEmits<Emits>()

const hoveredRelationId = ref<number | null>(null)
const tempArrow = ref<{ path: string } | null>(null)

// 判断关系是否被选中
const isSelected = (relationId?: number) => {
  return relationId === props.selectedRelationId
}

// 获取关系颜色
const getRelationColor = (relation: Relation): string => {
  if (relation.color) return relation.color
  return '#409eff' // 默认蓝色
}

// 获取实体位置
const getEntityPosition = (entityId: string): EntityPosition | null => {
  return props.entityPositions.get(entityId) || null
}

/**
 * 计算箭头路径（优化方案：同行在上方，跨行从侧边）
 */
const getArrowPath = (relation: Relation): string => {
  const sourcePos = getEntityPosition(relation.source_entity_id)
  const targetPos = getEntityPosition(relation.target_entity_id)

  if (!sourcePos || !targetPos) {
    return ''
  }

  // 圆角半径
  const radius = 8

  // 计算中心点
  const sourceCenterX = sourcePos.x + sourcePos.width / 2
  const sourceCenterY = sourcePos.y + sourcePos.height / 2
  const targetCenterX = targetPos.x + targetPos.width / 2
  const targetCenterY = targetPos.y + targetPos.height / 2

  // 计算距离
  const dx = targetCenterX - sourceCenterX
  const dy = targetCenterY - sourceCenterY

  // 判断是否同行（垂直距离小于实体高度）
  const isSameLine = Math.abs(dy) < sourcePos.height

  let path = ''

  if (isSameLine) {
    // ========== 同一行：统一在上方绘制 ==========
    
    // 起点和终点：从实体上边缘中心出发
    const startX = sourceCenterX
    const startY = sourcePos.y
    const endX = targetCenterX
    const endY = targetPos.y

    // 计算箭头高度（根据关系ID分层，避免重叠）
    const layerIndex = (relation.id || 0) % 3
    const arcHeight = 40 + layerIndex * 30 // 40, 70, 100

    // 水平线的Y坐标（在实体上方）
    const horizontalY = Math.min(startY, endY) - arcHeight

    // 绘制路径
    path = `M ${startX} ${startY}`
    
    // 向上到水平线
    if (Math.abs(horizontalY - startY) > radius) {
      path += ` L ${startX} ${horizontalY + radius}`
      path += ` Q ${startX} ${horizontalY} ${startX + Math.sign(dx) * radius} ${horizontalY}`
    } else {
      path += ` L ${startX} ${horizontalY}`
    }

    // 水平线
    path += ` L ${endX - Math.sign(dx) * radius} ${horizontalY}`

    // 向下到终点
    path += ` Q ${endX} ${horizontalY} ${endX} ${horizontalY + radius}`
    path += ` L ${endX} ${endY}`

  } else {
    // ========== 跨行：从侧边连接 ==========
    
    let startX, startY, endX, endY

    // 判断方向
    const isDownward = dy > 0 // 从上到下
    const isRightward = dx > 0 // 从左到右

    if (isDownward) {
      // 从上到下
      if (isRightward) {
        // 右下方：从右边出发，到左边
        startX = sourcePos.x + sourcePos.width
        startY = sourceCenterY
        endX = targetPos.x
        endY = targetCenterY
      } else {
        // 左下方：从左边出发，到右边
        startX = sourcePos.x
        startY = sourceCenterY
        endX = targetPos.x + targetPos.width
        endY = targetCenterY
      }
    } else {
      // 从下到上
      if (isRightward) {
        // 右上方：从右边出发，到左边
        startX = sourcePos.x + sourcePos.width
        startY = sourceCenterY
        endX = targetPos.x
        endY = targetCenterY
      } else {
        // 左上方：从左边出发，到右边
        startX = sourcePos.x
        startY = sourceCenterY
        endX = targetPos.x + targetPos.width
        endY = targetCenterY
      }
    }

    // 计算中间转折点
    const midX = (startX + endX) / 2
    const midY = (startY + endY) / 2

    // 绘制Z字形路径
    path = `M ${startX} ${startY}`

    const horizontalLength = Math.abs(endX - startX)
    const verticalLength = Math.abs(endY - startY)

    if (horizontalLength > radius * 2 && verticalLength > radius * 2) {
      // 标准Z字形
      // 水平到中点
      path += ` L ${midX - Math.sign(dx) * radius} ${startY}`
      path += ` Q ${midX} ${startY} ${midX} ${startY + Math.sign(dy) * radius}`
      
      // 垂直到中点
      path += ` L ${midX} ${endY - Math.sign(dy) * radius}`
      path += ` Q ${midX} ${endY} ${midX + Math.sign(dx) * radius} ${endY}`
      
      // 水平到终点
      path += ` L ${endX} ${endY}`
    } else {
      // 距离太短，简化路径
      path += ` Q ${midX} ${startY} ${midX} ${midY}`
      path += ` Q ${midX} ${endY} ${endX} ${endY}`
    }
  }

  return path
}

// 获取标签位置（在箭头的水平段中点）
const getLabelPosition = (relation: Relation) => {
  const sourcePos = getEntityPosition(relation.source_entity_id)
  const targetPos = getEntityPosition(relation.target_entity_id)

  if (!sourcePos || !targetPos) {
    return { x: 0, y: 0 }
  }

  const sourceCenterX = sourcePos.x + sourcePos.width / 2
  const sourceCenterY = sourcePos.y + sourcePos.height / 2
  const targetCenterX = targetPos.x + targetPos.width / 2
  const targetCenterY = targetPos.y + targetPos.height / 2

  const dy = targetCenterY - sourceCenterY
  const isSameLine = Math.abs(dy) < sourcePos.height

  if (isSameLine) {
    // 同一行：标签在上方的水平线上
    const layerIndex = (relation.id || 0) % 3
    const arcHeight = 40 + layerIndex * 30
    const labelY = Math.min(sourcePos.y, targetPos.y) - arcHeight

    return {
      x: (sourceCenterX + targetCenterX) / 2,
      y: labelY
    }
  } else {
    // 跨行：标签在中间位置
    return {
      x: (sourceCenterX + targetCenterX) / 2,
      y: (sourceCenterY + targetCenterY) / 2
    }
  }
}

// 处理箭头点击
const handleArrowClick = (relation: Relation) => {
  if (relation.id) {
    emit('select', relation.id)
  }
}

// 处理图层点击（取消选择）
const handleLayerClick = () => {
  // 点击空白处取消选择
}

// 更新临时箭头（用于创建关系时的预览）
const updateTempArrow = (sourceEntityId: number, mouseX: number, mouseY: number) => {
  const sourcePos = getEntityPosition(sourceEntityId)
  if (!sourcePos) return

  const start = {
    x: sourcePos.x + sourcePos.width / 2,
    y: sourcePos.y + sourcePos.height / 2
  }

  tempArrow.value = {
    path: `M ${start.x} ${start.y} L ${mouseX} ${mouseY}`
  }
}

// 清除临时箭头
const clearTempArrow = () => {
  tempArrow.value = null
}

// 暴露方法给父组件
defineExpose({
  updateTempArrow,
  clearTempArrow
})
</script>
⋮----
<style scoped>
.relation-arrow-layer {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 10;
  overflow: visible;  /* 确保箭头不被裁剪 */
}

.relation-arrow {
  cursor: pointer;
  transition: all 0.2s ease;
  pointer-events: all;
}

.relation-arrow:hover {
  stroke-width: 3 !important;
  filter: brightness(1.2);
}

.relation-arrow.selected {
  stroke-width: 4 !important;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.relation-label {
  fill: white;
  font-size: 12px;
  font-weight: 600;
  pointer-events: none;
  user-select: none;
}
</style>
````

## File: frontend/src/components/annotation/RelationList.vue
````vue
<template>
  <div class="relation-list">
    <div class="list-header">
      <h3>关系列表 ({{ relations.length }})</h3>
    </div>

    <el-scrollbar>
      <div class="relation-items">
        <div
          v-for="relation in relations"
          :key="relation.id"
          class="relation-item"
          :class="{ selected: selectedRelationId === relation.id }"
          @click="handleSelect(relation.id!)"
        >
          <div class="relation-header">
            <el-tag type="info" size="small">
              {{ relation.relation_type_name }}
            </el-tag>
            <el-button
              type="danger"
              size="small"
              text
              @click.stop="handleDelete(relation.id!)"
            >
              删除
            </el-button>
          </div>

          <div class="relation-content">
            <div class="entity-box source">
              <span class="entity-label">源实体</span>
              <div class="entity-text">
                {{ getEntityText(relation.source_entity_id) }}
              </div>
            </div>

            <div class="arrow">
              <el-icon><Right /></el-icon>
            </div>

            <div class="entity-box target">
              <span class="entity-label">目标实体</span>
              <div class="entity-text">
                {{ getEntityText(relation.target_entity_id) }}
              </div>
            </div>
          </div>
        </div>

        <el-empty
          v-if="relations.length === 0"
          description="暂无关系"
          :image-size="80"
        />
      </div>
    </el-scrollbar>
  </div>
</template>
⋮----
<h3>关系列表 ({{ relations.length }})</h3>
⋮----
{{ relation.relation_type_name }}
⋮----
{{ getEntityText(relation.source_entity_id) }}
⋮----
{{ getEntityText(relation.target_entity_id) }}
⋮----
<script setup lang="ts">
import { ref } from 'vue'
import { Right } from '@element-plus/icons-vue'

interface Entity {
  id?: number
  text: string
  start_offset: number
  end_offset: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Relation {
  id?: number
  source_entity_id: number
  target_entity_id: number
  relation_type_id: number
  relation_type_name: string
}

interface Props {
  relations: Relation[]
  entities: Entity[]
}

interface Emits {
  (e: 'select', relationId: number): void
  (e: 'delete', relationId: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const selectedRelationId = ref<number | null>(null)

const getEntityText = (entityId: number): string => {
  const entity = props.entities.find(e => e.id === entityId)
  return entity ? entity.text : '未知实体'
}

const handleSelect = (relationId: number) => {
  selectedRelationId.value = relationId
  emit('select', relationId)
}

const handleDelete = (relationId: number) => {
  emit('delete', relationId)
  if (selectedRelationId.value === relationId) {
    selectedRelationId.value = null
  }
}
</script>
⋮----
<style scoped>
.relation-list {
  display: flex;
  flex-direction: column;
  height: 50%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
}

.list-header {
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
}

.list-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.relation-items {
  padding: 8px;
}

.relation-item {
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.relation-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.relation-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.relation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.relation-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.entity-box {
  flex: 1;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.entity-label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.entity-text {
  font-size: 13px;
  color: #303133;
  word-break: break-word;
  line-height: 1.4;
}

.arrow {
  font-size: 18px;
  color: #409eff;
}
</style>
````

## File: frontend/src/components/annotation/RelationTypeSelector.vue
````vue
<template>
  <el-dialog
    v-model="visible"
    title="选择关系类型"
    width="500px"
    @close="handleClose"
  >
    <div class="relation-info">
      <div class="entity-box">
        <span class="label">源实体</span>
        <div class="entity-text">{{ sourceEntity?.text }}</div>
      </div>
      <el-icon class="arrow-icon"><Right /></el-icon>
      <div class="entity-box">
        <span class="label">目标实体</span>
        <div class="entity-text">{{ targetEntity?.text }}</div>
      </div>
    </div>

    <el-divider />

    <div class="relation-types">
      <div
        v-for="relationType in relationTypes"
        :key="relationType.id"
        class="relation-type-item"
        @click="handleSelect(relationType)"
      >
        <el-tag
          :color="relationType.color"
          :style="{ backgroundColor: relationType.color, color: '#fff', border: 'none' }"
        >
          {{ relationType.type_name_zh }}
        </el-tag>
        <span class="description">{{ relationType.description }}</span>
      </div>
    </div>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
    </template>
  </el-dialog>
</template>
⋮----
<div class="entity-text">{{ sourceEntity?.text }}</div>
⋮----
<div class="entity-text">{{ targetEntity?.text }}</div>
⋮----
{{ relationType.type_name_zh }}
⋮----
<span class="description">{{ relationType.description }}</span>
⋮----
<template #footer>
      <el-button @click="handleClose">取消</el-button>
    </template>
⋮----
<script setup lang="ts">
import { ref, computed } from 'vue'
import { Right } from '@element-plus/icons-vue'
import type { RelationType } from '@/api/label'

interface Entity {
  id?: number
  text: string
  start_offset: number
  end_offset: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Props {
  modelValue: boolean
  sourceEntity: Entity | null
  targetEntity: Entity | null
  relationTypes: RelationType[]
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'select', relationType: RelationType): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleSelect = (relationType: RelationType) => {
  emit('select', relationType)
  visible.value = false
}

const handleClose = () => {
  visible.value = false
}
</script>
⋮----
<style scoped>
.relation-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.entity-box {
  flex: 1;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.entity-box .label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
}

.entity-box .entity-text {
  font-size: 14px;
  color: #303133;
  word-break: break-word;
  line-height: 1.5;
}

.arrow-icon {
  font-size: 24px;
  color: #409eff;
}

.relation-types {
  max-height: 400px;
  overflow-y: auto;
}

.relation-type-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.relation-type-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.description {
  flex: 1;
  font-size: 13px;
  color: #606266;
}
</style>
````

## File: frontend/src/components/annotation/TextAnnotationEditor.vue
````vue
<template>
  <div class="text-annotation-editor">
    <!-- 工具栏 -->
    <div class="toolbar">
      <el-alert
        v-if="relationCreation.state.value.isActive"
        :title="relationCreation.getHintMessage()"
        type="info"
        :closable="false"
      />
      <el-button
        v-if="relationCreation.state.value.isActive"
        size="small"
        @click="cancelRelationCreation"
      >
        取消关系创建
      </el-button>
      <span v-if="!relationCreation.state.value.isActive && !props.readonly" class="toolbar-hint">
        提示：选择文本创建实体，点击实体选中（Delete键删除），Ctrl+点击实体创建关系
      </span>
      <span v-if="props.readonly" class="toolbar-hint readonly-hint">
        <el-icon><View /></el-icon>
        只读模式：仅可查看标注，不可编辑
      </span>
    </div>

    <!-- 文本显示区域 -->
    <div class="text-display-area">
      <div
        ref="textContainerRef"
        class="text-container"
        v-html="renderedText"
      >
      </div>

      <!-- SVG箭头层 -->
      <RelationArrowLayer
        ref="arrowLayerRef"
        :relations="relations"
        :entities="entities"
        :entity-positions="entityPositions"
        :selected-relation-id="selectedRelationId"
        :width="containerWidth"
        :height="containerHeight"
        @select="handleRelationSelect"
      />

      <!-- 标签选择菜单 -->
      <LabelSelector
        v-if="showLabelSelector"
        :position="labelSelectorPosition"
        :entity-types="entityTypes"
        @select="handleLabelSelect"
        @close="closeLabelSelector"
      />
    </div>

    <!-- 侧边面板 -->
    <div class="side-panel">
      <!-- 实体列表 -->
      <EntityList
        :entities="entities"
        :text="text"
        @select="handleEntitySelect"
        @delete="handleEntityDelete"
        @update="handleEntityUpdate"
      />

      <!-- 关系列表 -->
      <RelationList
        :relations="relations"
        :entities="entities"
        @select="handleRelationSelect"
        @delete="handleRelationDelete"
      />
    </div>

    <!-- 关系类型选择对话框 -->
    <RelationTypeSelector
      v-model="showRelationTypeSelector"
      :source-entity="selectedSourceEntity"
      :target-entity="selectedTargetEntity"
      :relation-types="relationTypes"
      @select="handleRelationTypeSelect"
    />
  </div>
</template>
⋮----
<!-- 工具栏 -->
⋮----
<!-- 文本显示区域 -->
⋮----
<!-- SVG箭头层 -->
⋮----
<!-- 标签选择菜单 -->
⋮----
<!-- 侧边面板 -->
⋮----
<!-- 实体列表 -->
⋮----
<!-- 关系列表 -->
⋮----
<!-- 关系类型选择对话框 -->
⋮----
<script setup lang="ts">
import { ref, computed, onMounted, nextTick, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { View } from '@element-plus/icons-vue'
import LabelSelector from './LabelSelector.vue'
import EntityList from './EntityList.vue'
import RelationList from './RelationList.vue'
import RelationArrowLayer from './RelationArrowLayer.vue'
import RelationTypeSelector from './RelationTypeSelector.vue'
import { useTextSelection } from '@/composables/useTextSelection'
import { useRelationCreation } from '@/composables/useRelationCreation'
import type { EntityType, RelationType } from '@/api/label'

interface Entity {
  id?: number
  text: string
  start_offset: number
  end_offset: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Relation {
  id?: number
  source_entity_id: string  // 使用字符串格式的entity_id
  target_entity_id: string  // 使用字符串格式的entity_id
  relation_type_id: number
  relation_type_name: string
}

interface Props {
  text: string
  entities: Entity[]
  relations: Relation[]
  entityTypes: EntityType[]
  relationTypes: RelationType[]
  readonly?: boolean  // 添加只读模式支持
}

interface Emits {
  (e: 'add-entity', entity: Omit<Entity, 'id'>): void
  (e: 'update-entity', id: number, entity: Partial<Entity>): void
  (e: 'delete-entity', id: number): void
  (e: 'add-relation', relation: Omit<Relation, 'id'>): void
  (e: 'delete-relation', id: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const textContainerRef = ref<HTMLElement>()
const arrowLayerRef = ref<InstanceType<typeof RelationArrowLayer>>()
const showLabelSelector = ref(false)
const labelSelectorPosition = ref({ x: 0, y: 0 })
const selectedRange = ref<{ start: number; end: number } | null>(null)
const selectedEntityId = ref<number | null>(null)
const selectedRelationId = ref<number | null>(null)
const showRelationTypeSelector = ref(false)
const selectedSourceEntity = ref<Entity | null>(null)
const selectedTargetEntity = ref<Entity | null>(null)
const containerWidth = ref(0)
const containerHeight = ref(0)
const entityPositions = ref<Map<string, any>>(new Map())  // 键改为字符串类型

// 使用composables
const { getSelection, validateOffset } = useTextSelection()
const relationCreation = useRelationCreation()

// 计算文字颜色以确保对比度
const getContrastColor = (hexColor: string): string => {
  // 如果颜色未定义，返回黑色
  if (!hexColor) return '#000000'
  
  // 移除 # 号
  const hex = hexColor.replace('#', '')
  
  // 转换为 RGB
  const r = parseInt(hex.substr(0, 2), 16)
  const g = parseInt(hex.substr(2, 2), 16)
  const b = parseInt(hex.substr(4, 2), 16)
  
  // 计算亮度 (使用 YIQ 公式)
  const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000
  
  // 根据亮度返回黑色或白色
  return yiq >= 128 ? '#000000' : '#ffffff'
}

// 渲染带实体高亮的文本（使用v-html）
const renderedText = computed(() => {
  if (!props.text) return ''
  
  // 如果没有实体，直接返回转义后的纯文本
  if (props.entities.length === 0) {
    return escapeHtml(props.text)
  }
  
  // 按偏移量排序实体
  const sortedEntities = [...props.entities].sort((a, b) => a.start_offset - b.start_offset)
  
  let html = ''
  let lastOffset = 0
  
  sortedEntities.forEach(entity => {
    // 添加实体前的文本
    if (entity.start_offset > lastOffset) {
      html += escapeHtml(props.text.substring(lastOffset, entity.start_offset))
    }
    
    // 添加实体（带高亮）
    const entityText = props.text.substring(entity.start_offset, entity.end_offset)
    const textColor = getContrastColor(entity.color)
    const isSelected = selectedEntityId.value === entity.id
    const bgColor = isSelected ? '#ffeb3b' : entity.color
    const finalTextColor = isSelected ? '#000000' : textColor
    
    html += `<span class="entity-highlight" data-entity-id="${entity.id}" style="background-color: ${bgColor}; color: ${finalTextColor}; padding: 2px 4px; border-radius: 3px;">${escapeHtml(entityText)}</span>`
    
    lastOffset = entity.end_offset
  })
  
  // 添加最后的文本
  if (lastOffset < props.text.length) {
    html += escapeHtml(props.text.substring(lastOffset))
  }
  
  return html
})

// HTML转义函数
const escapeHtml = (text: string): string => {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

// 更新容器尺寸
const updateContainerSize = () => {
  if (textContainerRef.value) {
    containerWidth.value = textContainerRef.value.offsetWidth
    // 增加额外高度以容纳上方的箭头（120px padding + 100px 额外空间）
    containerHeight.value = textContainerRef.value.offsetHeight + 220
  }
}

// 更新实体位置
const updateEntityPositions = () => {
  if (!textContainerRef.value) return

  const positions = new Map()
  props.entities.forEach(entity => {
    if (!entity.entity_id) return

    // 查找实体的span元素（使用数字id作为data属性）
    const entitySpan = textContainerRef.value?.querySelector(
      `span[data-entity-id="${entity.id}"]`
    )

    if (entitySpan) {
      const rect = entitySpan.getBoundingClientRect()
      const containerRect = textContainerRef.value!.getBoundingClientRect()

      // 使用entity_id（字符串）作为键
      positions.set(entity.entity_id, {
        x: rect.left - containerRect.left,
        y: rect.top - containerRect.top, // 不加偏移，使用实际位置
        width: rect.width,
        height: rect.height
      })
    }
  })

  entityPositions.value = positions
}

// 处理鼠标松开事件（文本选择完成）
const handleMouseUp = () => {
  // 只读模式下不允许选择
  if (props.readonly) return
  
  // 延迟一小段时间，确保选择已完成
  setTimeout(() => {
    if (!textContainerRef.value) return
    
    const selection = getSelection(textContainerRef.value)
    
    // 只有当有有效选择且选择了文本时才显示标签选择器
    if (selection && selection.text && selection.text.trim().length > 0) {
      selectedRange.value = selection
      
      // 显示标签选择菜单
      const range = window.getSelection()?.getRangeAt(0)
      if (range) {
        const rect = range.getBoundingClientRect()
        labelSelectorPosition.value = {
          x: rect.left + rect.width / 2,
          y: rect.bottom + 10
        }
        showLabelSelector.value = true
      }
    }
  }, 10)
}

// 处理实体点击（使用事件委托）
const handleContainerClick = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  
  // 检查是否点击了实体
  if (target.classList.contains('entity-highlight')) {
    const entityId = parseInt(target.getAttribute('data-entity-id') || '0', 10)
    const entity = props.entities.find(e => e.id === entityId)
    
    if (entity && entity.id) {
      // Ctrl+点击实体：创建关系（只读模式下不允许）
      if (event.ctrlKey && !props.readonly) {
        event.preventDefault()
        event.stopPropagation()
        
        // 如果还没开始创建关系，自动开始
        if (!relationCreation.state.value.isActive) {
          relationCreation.startCreation()
        }
        
        const completed = relationCreation.selectEntity(entity.id)
        if (completed) {
          // 选择完成，显示关系类型选择对话框
          const { sourceEntityId, targetEntityId } = relationCreation.getSelectedEntities()
          selectedSourceEntity.value = props.entities.find(e => e.id === sourceEntityId) || null
          selectedTargetEntity.value = props.entities.find(e => e.id === targetEntityId) || null
          showRelationTypeSelector.value = true
        }
      } else {
        // 普通点击：选择/取消选择实体
        if (selectedEntityId.value === entity.id) {
          // 再次点击同一个实体，取消选择
          selectedEntityId.value = null
        } else {
          // 选择新实体
          selectedEntityId.value = entity.id
        }
      }
    }
  } else {
    // 点击空白处，取消所有选择
    selectedEntityId.value = null
    selectedRelationId.value = null
  }
}

// 处理标签选择
const handleLabelSelect = (entityType: EntityType) => {
  if (!selectedRange.value) return
  
  const { start, end } = selectedRange.value
  
  // 验证偏移量
  if (!validateOffset(props.text, start, end)) {
    ElMessage.error('选择的文本偏移量无效')
    return
  }
  
  // 检查是否与现有实体重叠
  const hasOverlap = props.entities.some(
    e => !(end <= e.start_offset || start >= e.end_offset)
  )
  
  if (hasOverlap) {
    ElMessage.warning('选择的文本与现有实体重叠')
    return
  }
  
  // 创建新实体
  const newEntity: Omit<Entity, 'id'> = {
    text: props.text.substring(start, end),
    start_offset: start,
    end_offset: end,
    entity_type_id: entityType.id,
    entity_type_name: entityType.type_name_zh,
    color: entityType.color
  }
  
  emit('add-entity', newEntity)
  closeLabelSelector()

  // 更新实体位置
  nextTick(() => {
    updateEntityPositions()
  })
}

// 关闭标签选择菜单
const closeLabelSelector = () => {
  showLabelSelector.value = false
  selectedRange.value = null
  window.getSelection()?.removeAllRanges()
}



// 取消创建关系
const cancelRelationCreation = () => {
  relationCreation.cancelCreation()
}

// 处理关系类型选择
const handleRelationTypeSelect = (relationType: RelationType) => {
  const { sourceEntityId, targetEntityId } = relationCreation.getSelectedEntities()
  
  if (!sourceEntityId || !targetEntityId) return

  // 查找实体对象以获取entity_id
  const sourceEntity = props.entities.find(e => e.id === sourceEntityId)
  const targetEntity = props.entities.find(e => e.id === targetEntityId)
  
  if (!sourceEntity || !targetEntity) {
    ElMessage.error('无法找到选中的实体')
    return
  }

  const newRelation: Omit<Relation, 'id'> = {
    source_entity_id: sourceEntity.entity_id,
    target_entity_id: targetEntity.entity_id,
    relation_type_id: relationType.id,
    relation_type_name: relationType.type_name_zh
  }

  emit('add-relation', newRelation)
  relationCreation.reset()
  ElMessage.success('关系创建成功')
}

// 处理实体选择
const handleEntitySelect = (entityId: number) => {
  selectedEntityId.value = entityId
}

// 处理实体删除
const handleEntityDelete = (entityId: number) => {
  emit('delete-entity', entityId)
  if (selectedEntityId.value === entityId) {
    selectedEntityId.value = null
  }

  // 清除选择，强制重新渲染
  window.getSelection()?.removeAllRanges()

  // 更新实体位置
  nextTick(() => {
    updateEntityPositions()
  })
}

// 处理键盘事件
const handleKeyDown = (event: KeyboardEvent) => {
  // 只读模式下不允许删除
  if (props.readonly) return
  
  // Delete 或 Backspace 键删除选中的实体
  if ((event.key === 'Delete' || event.key === 'Backspace') && selectedEntityId.value) {
    event.preventDefault()
    handleEntityDelete(selectedEntityId.value)
  }
  
  // Escape 键取消选择
  if (event.key === 'Escape') {
    selectedEntityId.value = null
    selectedRelationId.value = null
    if (relationCreation.state.value.isActive) {
      relationCreation.cancelCreation()
    }
  }
}

// 处理实体更新
const handleEntityUpdate = (entityId: number, updates: Partial<Entity>) => {
  emit('update-entity', entityId, updates)

  // 更新实体位置
  nextTick(() => {
    updateEntityPositions()
  })
}

// 处理关系选择
const handleRelationSelect = (relationId: number) => {
  // 如果点击的是已选中的关系，取消选择
  if (selectedRelationId.value === relationId) {
    selectedRelationId.value = null
  } else {
    selectedRelationId.value = relationId
  }
}

// 处理关系删除
const handleRelationDelete = (relationId: number) => {
  emit('delete-relation', relationId)
  if (selectedRelationId.value === relationId) {
    selectedRelationId.value = null
  }
}

// 初始化
onMounted(() => {
  console.log('[TextAnnotationEditor] Mounted with props:', {
    text: props.text?.substring(0, 50) + '...',
    entitiesCount: props.entities.length,
    relationsCount: props.relations.length,
    entityTypesCount: props.entityTypes.length,
    relationTypesCount: props.relationTypes.length,
    entityTypes: props.entityTypes
  })
  
  updateContainerSize()
  updateEntityPositions()

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    updateContainerSize()
    updateEntityPositions()
  })
  
  // 监听键盘事件
  document.addEventListener('keydown', handleKeyDown)
  
  // 监听鼠标松开事件（文本选择完成后显示标签选择器）
  if (textContainerRef.value) {
    textContainerRef.value.addEventListener('mouseup', handleMouseUp)
  }
  
  // 监听容器点击（用于实体点击）
  if (textContainerRef.value) {
    textContainerRef.value.addEventListener('click', handleContainerClick)
  }
})

// 清理
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
  if (textContainerRef.value) {
    textContainerRef.value.removeEventListener('mouseup', handleMouseUp)
    textContainerRef.value.removeEventListener('click', handleContainerClick)
  }
})
</script>
⋮----
<style scoped>
.text-annotation-editor {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.toolbar-hint {
  color: #909399;
  font-size: 14px;
}

.readonly-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e6a23c;
  font-weight: 500;
}

.text-display-area {
  flex: 1;
  position: relative;
  overflow: visible;  /* 改为 visible，让箭头可以超出容器 */
  display: flex;
  gap: 20px;
}

.text-container {
  flex: 1;
  padding: 20px;
  padding-top: 120px;  /* 增加顶部内边距，为上方的箭头留出空间 */
  line-height: 3;  /* 增加行间距到3倍，为跨行箭头留出空间 */
  font-size: 16px;
  white-space: pre-wrap;
  word-break: break-word;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: text;
  user-select: text;
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
  overflow-y: auto;  /* 添加垂直滚动 */
  max-height: calc(100vh - 400px);  /* 限制最大高度 */
}

/* 实体高亮样式 */
.text-container :deep(.entity-highlight) {
  cursor: text;
  user-select: text;
}

/* Ctrl 键按下时，实体显示为可点击 */
.text-container :deep(.entity-highlight:hover) {
  opacity: 0.9;
}

.side-panel {
  width: 350px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow: auto;
}
</style>
````

## File: frontend/src/components/charts/SimplePieChart.vue
````vue
<template>
  <div class="pie-chart">
    <div v-if="slices.length > 0" class="chart-wrap">
      <svg :viewBox="`0 0 ${size} ${size}`" class="chart-svg" role="img" aria-label="pie chart">
        <template v-if="slices.length === 1">
          <circle
            :cx="center"
            :cy="center"
            :r="radius"
            :fill="slices[0].color"
          />
        </template>
        <template v-else>
          <path
            v-for="slice in slices"
            :key="slice.name"
            :d="slice.path"
            :fill="slice.color"
          />
        </template>
        <circle
          :cx="center"
          :cy="center"
          :r="innerRadius"
          fill="#fff"
        />
        <text :x="center" :y="center - 6" text-anchor="middle" class="total-label">总计</text>
        <text :x="center" :y="center + 14" text-anchor="middle" class="total-value">{{ total }}</text>
      </svg>

      <div class="legend">
        <div
          v-for="slice in slices"
          :key="`${slice.name}-${slice.count}`"
          class="legend-item"
        >
          <span class="dot" :style="{ backgroundColor: slice.color }" />
          <span class="name" :title="slice.name">{{ slice.name }}</span>
          <span class="value">{{ slice.count }} ({{ formatPercent(slice.percent) }})</span>
        </div>
      </div>
    </div>

    <el-empty v-else description="暂无数据" :image-size="100" />
  </div>
</template>
⋮----
<template v-if="slices.length === 1">
          <circle
            :cx="center"
            :cy="center"
            :r="radius"
            :fill="slices[0].color"
          />
        </template>
<template v-else>
          <path
            v-for="slice in slices"
            :key="slice.name"
            :d="slice.path"
            :fill="slice.color"
          />
        </template>
⋮----
<text :x="center" :y="center + 14" text-anchor="middle" class="total-value">{{ total }}</text>
⋮----
<span class="name" :title="slice.name">{{ slice.name }}</span>
<span class="value">{{ slice.count }} ({{ formatPercent(slice.percent) }})</span>
⋮----
<script setup lang="ts">
import { computed } from 'vue'

interface PieItem {
  name: string
  count: number
}

const props = withDefaults(defineProps<{
  data: PieItem[]
  size?: number
  maxItems?: number
}>(), {
  size: 240,
  maxItems: 10
})

const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#2f4554']

const normalized = computed(() => {
  return (props.data || [])
    .filter((item) => item && Number(item.count) > 0)
    .slice(0, props.maxItems)
    .map((item) => ({
      name: String(item.name ?? ''),
      count: Number(item.count)
    }))
})

const total = computed(() => normalized.value.reduce((sum, item) => sum + item.count, 0))
const size = computed(() => props.size)
const center = computed(() => size.value / 2)
const radius = computed(() => Math.max(20, size.value * 0.42))
const innerRadius = computed(() => Math.max(12, radius.value * 0.55))

const slices = computed(() => {
  if (!normalized.value.length || total.value <= 0) return []

  let start = -Math.PI / 2
  return normalized.value.map((item, idx) => {
    const percent = item.count / total.value
    const end = start + percent * Math.PI * 2
    const path = buildSectorPath(center.value, center.value, radius.value, start, end)
    const slice = {
      ...item,
      percent,
      color: colors[idx % colors.length],
      path
    }
    start = end
    return slice
  })
})

function polarToCartesian(cx: number, cy: number, r: number, angle: number) {
  return {
    x: cx + r * Math.cos(angle),
    y: cy + r * Math.sin(angle)
  }
}

function buildSectorPath(cx: number, cy: number, r: number, start: number, end: number) {
  const diff = end - start
  if (diff >= Math.PI * 2 - 1e-6) {
    return `M ${cx} ${cy - r} A ${r} ${r} 0 1 1 ${cx - 0.01} ${cy - r} Z`
  }

  const startPoint = polarToCartesian(cx, cy, r, start)
  const endPoint = polarToCartesian(cx, cy, r, end)
  const largeArcFlag = diff > Math.PI ? 1 : 0

  return [
    `M ${cx} ${cy}`,
    `L ${startPoint.x} ${startPoint.y}`,
    `A ${r} ${r} 0 ${largeArcFlag} 1 ${endPoint.x} ${endPoint.y}`,
    'Z'
  ].join(' ')
}

function formatPercent(value: number) {
  return `${(value * 100).toFixed(1)}%`
}
</script>
⋮----
<style scoped lang="scss">
.pie-chart {
  width: 100%;

  .chart-wrap {
    display: flex;
    gap: 16px;
    align-items: center;
  }

  .chart-svg {
    width: 240px;
    height: 240px;
    flex-shrink: 0;
  }

  .total-label {
    fill: #909399;
    font-size: 12px;
  }

  .total-value {
    fill: #303133;
    font-size: 18px;
    font-weight: 600;
  }

  .legend {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    min-width: 0;
  }

  .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .name {
    color: #303133;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 220px;
  }

  .value {
    color: #606266;
    margin-left: auto;
    white-space: nowrap;
  }
}
</style>
````

## File: frontend/src/components/corpus/CorpusGroupedView.vue
````vue
<template>
  <div class="corpus-grouped-view">
    <!-- 筛选工具栏 -->
    <div class="filter-toolbar">
      <el-input
        v-model="searchFileName"
        placeholder="按文件名搜索"
        clearable
        style="width: 250px"
        @change="handleFilterChange"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="selectedType"
        placeholder="按字段分类筛选"
        clearable
        style="width: 200px"
        @change="handleFilterChange"
      >
        <el-option label="全部" value="" />
        <el-option label="问题描述" value="问题描述" />
        <el-option label="原因分析" value="原因分析" />
        <el-option label="采取措施" value="采取措施" />
      </el-select>

      <el-checkbox v-model="showOnlyWithImages" :disabled="showOnlyWithoutImages" @change="onShowWithImagesChange">
        仅显示包含图片的语料
      </el-checkbox>
      <el-checkbox v-model="showOnlyWithoutImages" :disabled="showOnlyWithImages" @change="onShowWithoutImagesChange">
        仅显示不包含图片的语料
      </el-checkbox>

      <div class="stats">
        <span>共 {{ total }} 行数据</span>
      </div>
    </div>

    <!-- 分组列表 -->
    <div v-loading="loading" class="grouped-list">
      <el-empty v-if="!loading && list.length === 0" description="暂无语料数据" />

      <!-- 每一行Excel数据作为一个卡片 -->
      <el-card
        v-for="row in list"
        :key="`${row.source_file}-${row.source_row}`"
        class="row-card"
        shadow="hover"
      >
        <!-- 卡片头部：文件信息 -->
        <template #header>
          <div class="card-header">
            <div class="file-info">
              <el-icon><Document /></el-icon>
              <span class="file-name">{{ row.source_file }}</span>
              <el-tag size="small" type="info">第 {{ row.source_row }} 行</el-tag>
              <el-tag v-if="row.total_images > 0" size="small" type="warning">
                <el-icon><Picture /></el-icon>
                {{ row.total_images }} 张图片
              </el-tag>
            </div>
            <div class="card-actions">
              <el-button size="small" @click="handleViewRow(row)">
                查看详情
              </el-button>
              <el-button
                size="small"
                type="danger"
                plain
                :loading="deletingKey === `${row.source_file}-${row.source_row}-row`"
                @click="handleDeleteRow(row)"
              >
                删除本行
              </el-button>
              <el-button
                size="small"
                type="danger"
                :loading="deletingKey === `${row.source_file}-file`"
                @click="handleDeleteFile(row)"
              >
                删除该文件
              </el-button>
            </div>
          </div>
        </template>

        <!-- 卡片内容：各字段内容 -->
        <div class="row-content">
          <div
            v-for="item in row.items"
            :key="item.text_id"
            class="field-item"
          >
            <div class="field-header">
              <el-tag size="small">{{ item.source_field }}</el-tag>
              <span class="text-id">{{ item.text_id }}</span>
            </div>
            <div class="field-text">{{ item.text }}</div>

            <!-- 该字段的图片 -->
            <div v-if="item.images && item.images.length > 0" class="field-images">
              <div
                v-for="image in item.images"
                :key="image.image_id"
                class="image-thumbnail"
                @click="handlePreviewImage(image)"
              >
                <el-image
                  :src="getImageUrl(image.file_path)"
                  :alt="image.original_name"
                  fit="cover"
                  lazy
                >
                  <template #error>
                    <div class="image-error">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </template>
                </el-image>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 图片预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="图片预览"
      width="800px"
    >
      <el-image
        v-if="previewImage"
        :src="getImageUrl(previewImage.file_path)"
        :alt="previewImage.original_name"
        fit="contain"
        style="width: 100%"
      />
    </el-dialog>
  </div>
</template>
⋮----
<!-- 筛选工具栏 -->
⋮----
<template #prefix>
          <el-icon><Search /></el-icon>
        </template>
⋮----
<span>共 {{ total }} 行数据</span>
⋮----
<!-- 分组列表 -->
⋮----
<!-- 每一行Excel数据作为一个卡片 -->
⋮----
<!-- 卡片头部：文件信息 -->
<template #header>
          <div class="card-header">
            <div class="file-info">
              <el-icon><Document /></el-icon>
              <span class="file-name">{{ row.source_file }}</span>
              <el-tag size="small" type="info">第 {{ row.source_row }} 行</el-tag>
              <el-tag v-if="row.total_images > 0" size="small" type="warning">
                <el-icon><Picture /></el-icon>
                {{ row.total_images }} 张图片
              </el-tag>
            </div>
            <div class="card-actions">
              <el-button size="small" @click="handleViewRow(row)">
                查看详情
              </el-button>
              <el-button
                size="small"
                type="danger"
                plain
                :loading="deletingKey === `${row.source_file}-${row.source_row}-row`"
                @click="handleDeleteRow(row)"
              >
                删除本行
              </el-button>
              <el-button
                size="small"
                type="danger"
                :loading="deletingKey === `${row.source_file}-file`"
                @click="handleDeleteFile(row)"
              >
                删除该文件
              </el-button>
            </div>
          </div>
        </template>
⋮----
<span class="file-name">{{ row.source_file }}</span>
<el-tag size="small" type="info">第 {{ row.source_row }} 行</el-tag>
⋮----
{{ row.total_images }} 张图片
⋮----
<!-- 卡片内容：各字段内容 -->
⋮----
<el-tag size="small">{{ item.source_field }}</el-tag>
<span class="text-id">{{ item.text_id }}</span>
⋮----
<div class="field-text">{{ item.text }}</div>
⋮----
<!-- 该字段的图片 -->
⋮----
<template #error>
                    <div class="image-error">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </template>
⋮----
<!-- 分页 -->
⋮----
<!-- 图片预览对话框 -->
⋮----
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Picture, Search } from '@element-plus/icons-vue'
import { request } from '@/api/request'
import type { Image } from '@/types'
import { buildBackendUrl } from '@/utils/backendUrl'

const getImageUrl = (filePath: string) => buildBackendUrl(`/images/${filePath}`)

interface GroupedCorpusItem {
  text_id: string
  text: string
  text_type: string
  source_field: string
  has_images: boolean
  images: Image[]
}

interface GroupedCorpusRow {
  source_file: string
  source_row: number
  items: GroupedCorpusItem[]
  total_images: number
  created_at: string
}

const loading = ref(false)
const list = ref<GroupedCorpusRow[]>([])
const total = ref(0)
const searchFileName = ref('')
const selectedType = ref('')
const showOnlyWithImages = ref(false)
const showOnlyWithoutImages = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const previewVisible = ref(false)
const previewImage = ref<Image | null>(null)
const deletingKey = ref<string | null>(null)

const fetchList = async () => {
  loading.value = true
  try {
    const response = await request.get<{
      total: number
      items: GroupedCorpusRow[]
    }>('/corpus/grouped', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        source_file: searchFileName.value || undefined,
        source_field: selectedType.value || undefined,
        has_images: showOnlyWithImages.value ? true : (showOnlyWithoutImages.value ? false : undefined)
      }
    })
    list.value = response.items
    total.value = response.total
  } catch (error: any) {
    ElMessage.error(error.message || '获取数据失败')
  } finally {
    loading.value = false
  }
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchList()
}

const onShowWithImagesChange = () => {
  if (showOnlyWithImages.value) showOnlyWithoutImages.value = false
  handleFilterChange()
}

const onShowWithoutImagesChange = () => {
  if (showOnlyWithoutImages.value) showOnlyWithImages.value = false
  handleFilterChange()
}

const handlePageChange = () => {
  fetchList()
}

const handleViewRow = (row: GroupedCorpusRow) => {
  console.log('查看行详情:', row)
}

const handleDeleteRow = async (row: GroupedCorpusRow) => {
  try {
    await ElMessageBox.confirm(
      `确认删除文件「${row.source_file}」第 ${row.source_row} 行的所有语料？已被数据集引用的语料会被跳过并提示。`,
      '删除确认',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
    )
  } catch {
    return
  }

  const key = `${row.source_file}-${row.source_row}-row`
  deletingKey.value = key
  try {
    const res = await request.delete<{
      success: boolean
      message: string
      data?: { deleted: number; skipped: number; skipped_text_ids?: string[] }
    }>('/corpus/by-row', {
      params: { source_file: row.source_file, source_row: row.source_row }
    })
    ElMessage.success(res.message || '删除成功')
    fetchList()
  } catch (error: any) {
    const msg = error?.response?.data?.detail || '删除失败'
    ElMessage.warning(msg)
  } finally {
    deletingKey.value = null
  }
}

const handleDeleteFile = async (row: GroupedCorpusRow) => {
  try {
    await ElMessageBox.confirm(
      `确认删除文件「${row.source_file}」下的所有语料？已被数据集引用的语料会被跳过并提示。`,
      '删除确认',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
    )
  } catch {
    return
  }

  const key = `${row.source_file}-file`
  deletingKey.value = key
  try {
    const res = await request.delete<{
      success: boolean
      message: string
      data?: { deleted: number; skipped: number; skipped_text_ids?: string[] }
    }>('/corpus/by-file', { params: { source_file: row.source_file } })
    ElMessage.success(res.message || '删除成功')
    fetchList()
  } catch (error: any) {
    const msg = error?.response?.data?.detail || '删除失败'
    ElMessage.warning(msg)
  } finally {
    deletingKey.value = null
  }
}

const handlePreviewImage = (image: Image) => {
  previewImage.value = image
  previewVisible.value = true
}

onMounted(() => {
  fetchList()
})

defineExpose({
  refresh: fetchList
})
</script>
⋮----
<style scoped lang="scss">
.corpus-grouped-view {
  .filter-toolbar {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 8px;

    .stats {
      margin-left: auto;
      font-size: 14px;
      color: #606266;
    }
  }

  .grouped-list {
    min-height: 400px;

    .row-card {
      margin-bottom: 20px;

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        .file-info {
          display: flex;
          align-items: center;
          gap: 12px;
          flex: 1;

          .el-icon {
            font-size: 18px;
            color: #409eff;
          }

          .file-name {
            font-weight: 600;
            color: #303133;
          }
        }

        .card-actions {
          display: flex;
          gap: 8px;
        }
      }

      .row-content {
        display: flex;
        flex-direction: column;
        gap: 16px;

        .field-item {
          padding: 12px;
          background: #f9fafc;
          border-radius: 6px;
          border-left: 3px solid #409eff;

          .field-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;

            .text-id {
              font-size: 12px;
              color: #909399;
            }
          }

          .field-text {
            font-size: 14px;
            line-height: 1.6;
            color: #303133;
            margin-bottom: 8px;
          }

          .field-images {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;

            .image-thumbnail {
              width: 100px;
              height: 100px;
              cursor: pointer;
              transition: all 0.3s;

              &:hover {
                transform: scale(1.05);
              }

              .el-image {
                width: 100%;
                height: 100%;
                border-radius: 4px;
                overflow: hidden;
                border: 1px solid #e4e7ed;
              }

              .image-error {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100%;
                color: #c0c4cc;

                .el-icon {
                  font-size: 24px;
                }
              }
            }
          }
        }
      }
    }
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}
</style>
````

## File: frontend/src/components/corpus/CorpusPreview.vue
````vue
<template>
  <div class="corpus-preview">
    <!-- 筛选工具栏 -->
    <div class="filter-toolbar">
      <el-input
        v-model="searchFileName"
        placeholder="按文件名搜索"
        clearable
        style="width: 250px"
        @change="handleFilterChange"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="selectedType"
        placeholder="按字段分类筛选"
        clearable
        style="width: 200px"
        @change="handleFilterChange"
      >
        <el-option label="全部" value="" />
        <el-option label="问题描述" value="问题描述" />
        <el-option label="原因分析" value="原因分析" />
        <el-option label="采取措施" value="采取措施" />
      </el-select>

      <el-checkbox v-model="showOnlyWithImages" @change="handleFilterChange">
        仅显示包含图片的语料
      </el-checkbox>

      <div class="stats">
        <span>共 {{ total }} 条语料</span>
        <span v-if="filteredCount !== total">（筛选后 {{ filteredCount }} 条）</span>
      </div>
    </div>

    <!-- 语料列表 -->
    <div v-loading="loading" class="corpus-list">
      <el-empty v-if="!loading && list.length === 0" description="暂无语料数据" />

      <div
        v-for="item in list"
        :key="item.text_id"
        class="corpus-item"
      >
        <div class="corpus-header">
          <div class="corpus-id">
            <el-tag size="small">{{ item.text_id }}</el-tag>
            <el-tag v-if="item.text_type" type="info" size="small">
              {{ item.text_type }}
            </el-tag>
          </div>
          <div class="corpus-meta">
            <span class="meta-item">
              <el-icon><Document /></el-icon>
              {{ item.source_file }}
            </span>
            <span class="meta-item">
              第 {{ item.source_row }} 行
            </span>
            <span v-if="item.has_images" class="meta-item">
              <el-icon><Picture /></el-icon>
              {{ item.images?.length || 0 }} 张图片
            </span>
          </div>
        </div>

        <div class="corpus-content">
          <p class="corpus-text">{{ item.text }}</p>
        </div>

        <!-- 图片缩略图 -->
        <div v-if="item.has_images && item.images && item.images.length > 0" class="corpus-images">
          <div
            v-for="image in item.images"
            :key="image.image_id"
            class="image-thumbnail"
            @click="handlePreviewImage(image)"
          >
            <el-image
              :src="getImageUrl(image.file_path)"
              :alt="image.original_name"
              fit="cover"
              lazy
            >
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                  <span>加载失败</span>
                </div>
              </template>
            </el-image>
            <div class="image-name">{{ image.original_name }}</div>
          </div>
        </div>

        <div class="corpus-actions">
          <el-button size="small" @click="handleView(item)">
            查看详情
          </el-button>
          <el-button
            size="small"
            type="danger"
            plain
            @click="handleDelete(item)"
          >
            删除
          </el-button>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 图片预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="图片预览"
      width="800px"
    >
      <el-image
        v-if="previewImage"
        :src="getImageUrl(previewImage.file_path)"
        :alt="previewImage.original_name"
        fit="contain"
        style="width: 100%"
      />
    </el-dialog>
  </div>
</template>
⋮----
<!-- 筛选工具栏 -->
⋮----
<template #prefix>
          <el-icon><Search /></el-icon>
        </template>
⋮----
<span>共 {{ total }} 条语料</span>
<span v-if="filteredCount !== total">（筛选后 {{ filteredCount }} 条）</span>
⋮----
<!-- 语料列表 -->
⋮----
<el-tag size="small">{{ item.text_id }}</el-tag>
⋮----
{{ item.text_type }}
⋮----
{{ item.source_file }}
⋮----
第 {{ item.source_row }} 行
⋮----
{{ item.images?.length || 0 }} 张图片
⋮----
<p class="corpus-text">{{ item.text }}</p>
⋮----
<!-- 图片缩略图 -->
⋮----
<template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                  <span>加载失败</span>
                </div>
              </template>
⋮----
<div class="image-name">{{ image.original_name }}</div>
⋮----
<!-- 分页 -->
⋮----
<!-- 图片预览对话框 -->
⋮----
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Picture, Search } from '@element-plus/icons-vue'
import { useCorpusStore } from '@/stores'
import type { Corpus, Image } from '@/types'
import { buildBackendUrl } from '@/utils/backendUrl'

const corpusStore = useCorpusStore()

const getImageUrl = (filePath: string) => buildBackendUrl(`/images/${filePath}`)

const searchFileName = ref('')
const selectedType = ref('')
const showOnlyWithImages = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const previewVisible = ref(false)
const previewImage = ref<Image | null>(null)

const loading = computed(() => corpusStore.loading)
const list = computed(() => corpusStore.corpusList)
const total = computed(() => corpusStore.total)
const filteredCount = computed(() => list.value.length)

const fetchList = async () => {
  await corpusStore.fetchList({
    page: currentPage.value,
    page_size: pageSize.value,
    source_file: searchFileName.value || undefined,
    text_type: selectedType.value || undefined,
    has_images: showOnlyWithImages.value || undefined
  })
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchList()
}

const handlePageChange = () => {
  fetchList()
}

const handleView = (item: Corpus) => {
  console.log('查看详情:', item)
}

const handleDelete = async (item: Corpus) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除语料 ${item.text_id} 吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await corpusStore.deleteCorpus(item.text_id)
    ElMessage.success('删除成功')

    if (list.value.length === 0 && currentPage.value > 1) {
      currentPage.value--
    }

    fetchList()
  } catch (error: any) {
    if (error !== 'cancel') {
      const msg = error?.response?.data?.detail || '删除失败'
      ElMessage.warning(msg)
    }
  }
}

const handlePreviewImage = (image: Image) => {
  previewImage.value = image
  previewVisible.value = true
}

onMounted(() => {
  fetchList()
})

defineExpose({
  refresh: fetchList
})
</script>
⋮----
<style scoped lang="scss">
.corpus-preview {
  .filter-toolbar {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 8px;

    .stats {
      margin-left: auto;
      font-size: 14px;
      color: #606266;

      span + span {
        margin-left: 8px;
        color: #909399;
      }
    }
  }

  .corpus-list {
    min-height: 400px;

    .corpus-item {
      margin-bottom: 16px;
      padding: 16px;
      background: #fff;
      border: 1px solid #e4e7ed;
      border-radius: 8px;
      transition: all 0.3s;

      &:hover {
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
      }

      .corpus-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;

        .corpus-id {
          display: flex;
          gap: 8px;
        }

        .corpus-meta {
          display: flex;
          gap: 16px;
          font-size: 13px;
          color: #909399;

          .meta-item {
            display: flex;
            align-items: center;
            gap: 4px;
          }
        }
      }

      .corpus-content {
        margin-bottom: 12px;

        .corpus-text {
          margin: 0;
          font-size: 14px;
          line-height: 1.6;
          color: #303133;
        }
      }

      .corpus-images {
        display: flex;
        gap: 12px;
        margin-bottom: 12px;
        flex-wrap: wrap;

        .image-thumbnail {
          width: 120px;
          cursor: pointer;
          transition: all 0.3s;

          &:hover {
            transform: scale(1.05);
          }

          .el-image {
            width: 120px;
            height: 120px;
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid #e4e7ed;
          }

          .image-error {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #c0c4cc;

            .el-icon {
              font-size: 32px;
              margin-bottom: 8px;
            }

            span {
              font-size: 12px;
            }
          }

          .image-name {
            margin-top: 4px;
            font-size: 12px;
            color: #909399;
            text-align: center;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }
        }
      }

      .corpus-actions {
        display: flex;
        gap: 8px;
        justify-content: flex-end;
      }
    }
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}
</style>
````

## File: frontend/src/components/corpus/FileUploader.vue
````vue
<template>
  <div class="file-uploader">
    <el-upload
      ref="uploadRef"
      class="upload-area"
      drag
      :before-upload="handleBeforeUpload"
      :http-request="handleUpload"
      :show-file-list="false"
      :disabled="uploading"
      accept=".xlsx,.xls"
    >
      <div class="upload-content">
        <el-icon v-if="!uploading" class="upload-icon">
          <UploadFilled />
        </el-icon>
        <el-icon v-else class="upload-icon uploading">
          <Loading />
        </el-icon>
        
        <div class="upload-text">
          <p v-if="!uploading" class="primary-text">
            将Excel文件拖到此处，或<em>点击上传</em>
          </p>
          <p v-else class="primary-text">上传中...</p>
          <p class="hint-text">支持 .xlsx 和 .xls 格式文件</p>
        </div>
      </div>
    </el-upload>

    <!-- 上传进度 -->
    <div v-if="uploading" class="upload-progress">
      <el-progress
        :percentage="uploadProgress"
        :status="uploadStatus"
        :stroke-width="8"
      />
      <p class="progress-text">{{ progressText }}</p>
    </div>

    <!-- 文件格式说明 -->
    <el-collapse v-if="!uploading" class="format-info">
      <el-collapse-item title="Excel文件格式说明" name="format">
        <div class="format-content">
          <div class="format-item">
            <h4>必需列</h4>
            <ul>
              <li><code>问题描述</code> - 问题的详细描述</li>
              <li><code>原因分析</code> - 问题原因分析</li>
              <li><code>采取措施</code> - 采取的解决措施</li>
            </ul>
          </div>
          
          <div class="format-item">
            <h4>图片支持</h4>
            <p>Excel中的内嵌图片会自动提取并关联到对应的语料记录</p>
            <p>支持WPS和Microsoft Excel格式</p>
          </div>

          <div class="format-item">
            <h4>文本处理</h4>
            <p>系统会自动：</p>
            <ul>
              <li>以单元格为单位处理文本（一个单元格生成一条语料）</li>
              <li>提取DISPIMG公式并转换为Markdown格式</li>
              <li>生成唯一的语料ID</li>
            </ul>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>
⋮----
<!-- 上传进度 -->
⋮----
<p class="progress-text">{{ progressText }}</p>
⋮----
<!-- 文件格式说明 -->
⋮----
<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, Loading } from '@element-plus/icons-vue'
import type { UploadRequestOptions } from 'element-plus'
import { useCorpusStore } from '@/stores'

const emit = defineEmits<{
  success: [response: any]
  error: [error: any]
}>()

const corpusStore = useCorpusStore()

// 状态
const uploadRef = ref()
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadStatus = ref<'success' | 'exception' | 'warning' | undefined>()
const progressText = ref('')

// 上传前验证
const handleBeforeUpload = (file: File) => {
  const fileName = file.name.toLowerCase()
  const isValidType = fileName.endsWith('.xlsx') || fileName.endsWith('.xls')
  
  if (!isValidType) {
    ElMessage.error('只支持 Excel 格式文件（.xlsx 或 .xls）')
    return false
  }

  const maxSize = 100 * 1024 * 1024 // 100MB
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过 100MB')
    return false
  }

  return true
}

// 处理上传
const handleUpload = async (options: UploadRequestOptions) => {
  const { file } = options

  uploading.value = true
  uploadProgress.value = 0
  uploadStatus.value = undefined
  progressText.value = '正在上传文件...'

  try {
    // 模拟进度
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10
      }
    }, 300)

    const result = await corpusStore.upload(file as File)

    clearInterval(progressInterval)

    uploadProgress.value = 100
    uploadStatus.value = 'success'
    progressText.value = result.message || `上传成功！共 ${result.total_sentences} 条语料`
    
    setTimeout(() => {
      uploading.value = false
      emit('success', result)
    }, 1500)
  } catch (error: any) {
    uploadProgress.value = 0
    uploadStatus.value = 'exception'
    progressText.value = '上传失败，请重试'
    
    setTimeout(() => {
      uploading.value = false
    }, 2000)

    emit('error', error)
    ElMessage.error(error.message || '上传失败')
  }
}
</script>
⋮----
<style scoped lang="scss">
.file-uploader {
  .upload-area {
    width: 100%;

    :deep(.el-upload) {
      width: 100%;
    }

    :deep(.el-upload-dragger) {
      width: 100%;
      height: 200px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2px dashed #d9d9d9;
      border-radius: 8px;
      transition: all 0.3s;

      &:hover {
        border-color: #409eff;
      }
    }
  }

  .upload-content {
    text-align: center;

    .upload-icon {
      font-size: 60px;
      color: #c0c4cc;
      margin-bottom: 16px;

      &.uploading {
        color: #409eff;
        animation: rotating 2s linear infinite;
      }
    }

    .upload-text {
      .primary-text {
        margin: 0 0 8px;
        font-size: 14px;
        color: #606266;

        em {
          color: #409eff;
          font-style: normal;
        }
      }

      .hint-text {
        margin: 0;
        font-size: 12px;
        color: #909399;
      }
    }
  }

  .upload-progress {
    margin-top: 20px;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 8px;

    .progress-text {
      margin: 12px 0 0;
      text-align: center;
      font-size: 13px;
      color: #606266;
    }
  }

  .format-info {
    margin-top: 20px;

    .format-content {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .format-item {
      h4 {
        margin: 0 0 8px;
        font-size: 14px;
        color: #303133;
        font-weight: 600;
      }

      p {
        margin: 0 0 8px;
        font-size: 13px;
        color: #606266;
      }

      ul {
        margin: 0;
        padding-left: 20px;
        font-size: 13px;
        color: #606266;

        li {
          margin-bottom: 4px;
        }
      }

      code {
        padding: 2px 6px;
        background: #f5f7fa;
        border: 1px solid #e4e7ed;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
        color: #e6a23c;
        font-size: 12px;
      }
    }
  }
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
````

## File: frontend/src/components/dataset/BatchAnnotationDialog.vue
````vue
<template>
  <el-dialog
    v-model="visible"
    title="批量自动标注"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-if="!jobStarted" class="dialog-content">
      <el-alert
        title="批量标注说明"
        type="info"
        :closable="false"
        show-icon
      >
        <p>将使用AI模型对数据集中的所有任务进行自动标注：</p>
        <ul>
          <li>自动识别文本中的实体</li>
          <li>自动抽取实体间的关系</li>
          <li>自动标注图片内容</li>
        </ul>
        <p style="margin-top: 10px; color: #e6a23c;">
          <el-icon><Warning /></el-icon>
          注意：批量标注可能需要较长时间，请耐心等待
        </p>
      </el-alert>

      <div class="dataset-info">
        <div class="info-item">
          <span class="label">数据集名称：</span>
          <span class="value">{{ dataset?.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">任务总数：</span>
          <span class="value">{{ dataset?.statistics?.total_tasks || 0 }}</span>
        </div>
        <div class="info-item">
          <span class="label">待标注任务：</span>
          <span class="value">{{ dataset?.statistics?.pending_tasks || 0 }}</span>
        </div>
      </div>
    </div>

    <div v-else class="progress-content">
      <div class="progress-header">
        <h3>正在执行批量标注...</h3>
        <el-tag :type="statusType">{{ statusText }}</el-tag>
      </div>

      <div class="progress-stats">
        <div class="stat-item">
          <div class="stat-label">总任务数</div>
          <div class="stat-value">{{ jobStats.total_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">已完成</div>
          <div class="stat-value success">{{ jobStats.completed_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">失败</div>
          <div class="stat-value danger">{{ jobStats.failed_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">进行中</div>
          <div class="stat-value warning">{{ jobStats.processing_tasks }}</div>
        </div>
      </div>

      <div class="progress-bar">
        <div class="progress-label">
          <span>完成进度</span>
          <span class="progress-percent">{{ progressPercent }}%</span>
        </div>
        <el-progress
          :percentage="progressPercent"
          :status="progressStatus"
        />
      </div>

      <div v-if="jobStats.failed_tasks > 0" class="error-section">
        <el-alert
          title="部分任务标注失败"
          type="warning"
          :closable="false"
          show-icon
        >
          <p>{{ jobStats.failed_tasks }} 个任务标注失败，请手动检查和标注</p>
        </el-alert>
      </div>

      <div class="time-info">
        <span>开始时间：{{ formatTime(jobStats.started_at) }}</span>
        <span v-if="jobStats.completed_at">
          完成时间：{{ formatTime(jobStats.completed_at) }}
        </span>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">
          {{ jobStarted && jobStats.status !== 'completed' ? '后台运行' : '关闭' }}
        </el-button>
        <el-button
          v-if="!jobStarted"
          type="primary"
          :loading="starting"
          @click="handleStart"
        >
          开始标注
        </el-button>
        <el-button
          v-else-if="jobStats.status === 'running'"
          type="danger"
          :loading="cancelling"
          @click="handleCancel"
        >
          取消任务
        </el-button>
        <el-button
          v-else-if="jobStats.status === 'completed'"
          type="primary"
          @click="handleViewResults"
        >
          查看结果
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>
⋮----
<span class="value">{{ dataset?.name }}</span>
⋮----
<span class="value">{{ dataset?.statistics?.total_tasks || 0 }}</span>
⋮----
<span class="value">{{ dataset?.statistics?.pending_tasks || 0 }}</span>
⋮----
<el-tag :type="statusType">{{ statusText }}</el-tag>
⋮----
<div class="stat-value">{{ jobStats.total_tasks }}</div>
⋮----
<div class="stat-value success">{{ jobStats.completed_tasks }}</div>
⋮----
<div class="stat-value danger">{{ jobStats.failed_tasks }}</div>
⋮----
<div class="stat-value warning">{{ jobStats.processing_tasks }}</div>
⋮----
<span class="progress-percent">{{ progressPercent }}%</span>
⋮----
<p>{{ jobStats.failed_tasks }} 个任务标注失败，请手动检查和标注</p>
⋮----
<span>开始时间：{{ formatTime(jobStats.started_at) }}</span>
⋮----
完成时间：{{ formatTime(jobStats.completed_at) }}
⋮----
<template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">
          {{ jobStarted && jobStats.status !== 'completed' ? '后台运行' : '关闭' }}
        </el-button>
        <el-button
          v-if="!jobStarted"
          type="primary"
          :loading="starting"
          @click="handleStart"
        >
          开始标注
        </el-button>
        <el-button
          v-else-if="jobStats.status === 'running'"
          type="danger"
          :loading="cancelling"
          @click="handleCancel"
        >
          取消任务
        </el-button>
        <el-button
          v-else-if="jobStats.status === 'completed'"
          type="primary"
          @click="handleViewResults"
        >
          查看结果
        </el-button>
      </div>
    </template>
⋮----
{{ jobStarted && jobStats.status !== 'completed' ? '后台运行' : '关闭' }}
⋮----
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Warning } from '@element-plus/icons-vue'
import { annotationApi } from '@/api/annotation'
import type { Dataset } from '@/types'
import { format } from 'date-fns'

interface Props {
  modelValue: boolean
  dataset: Dataset | null
}

interface JobStats {
  job_id: string
  dataset_id: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  total_tasks: number
  completed_tasks: number
  failed_tasks: number
  processing_tasks: number
  started_at?: string
  completed_at?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

// 状态
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const jobStarted = ref(false)
const starting = ref(false)
const cancelling = ref(false)
const jobId = ref<string>('')
const jobStats = ref<JobStats>({
  job_id: '',
  dataset_id: '',
  status: 'pending',
  total_tasks: 0,
  completed_tasks: 0,
  failed_tasks: 0,
  processing_tasks: 0
})

let pollingTimer: number | null = null

// 计算属性
const progressPercent = computed(() => {
  if (jobStats.value.total_tasks === 0) return 0
  return Math.round(
    (jobStats.value.completed_tasks / jobStats.value.total_tasks) * 100
  )
})

const progressStatus = computed(() => {
  if (jobStats.value.status === 'completed') return 'success'
  if (jobStats.value.status === 'failed') return 'exception'
  if (jobStats.value.status === 'cancelled') return 'exception'
  return undefined
})

const statusType = computed(() => {
  const typeMap = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
    cancelled: 'info'
  }
  return typeMap[jobStats.value.status]
})

const statusText = computed(() => {
  const textMap = {
    pending: '等待中',
    running: '进行中',
    completed: '已完成',
    failed: '失败',
    cancelled: '已取消'
  }
  return textMap[jobStats.value.status]
})

// 方法
const handleStart = async () => {
  if (!props.dataset) return

  try {
    starting.value = true

    const response = await annotationApi.triggerBatchAnnotation({
      dataset_id: props.dataset.dataset_id
    })

    jobId.value = response.data.job_id
    jobStats.value = {
      job_id: response.data.job_id,
      dataset_id: response.data.dataset_id,
      status: response.data.status,
      total_tasks: response.data.total_tasks,
      completed_tasks: 0,
      failed_tasks: 0,
      processing_tasks: 0
    }

    jobStarted.value = true
    ElMessage.success('批量标注任务已启动')

    // 开始轮询任务状态
    startPolling()
  } catch (error: any) {
    ElMessage.error(error.message || '启动批量标注失败')
  } finally {
    starting.value = false
  }
}

const handleCancel = async () => {
  try {
    cancelling.value = true

    await annotationApi.cancelBatchJob(jobId.value)

    jobStats.value.status = 'cancelled'
    stopPolling()

    ElMessage.success('批量标注任务已取消')
  } catch (error: any) {
    ElMessage.error(error.message || '取消任务失败')
  } finally {
    cancelling.value = false
  }
}

const handleViewResults = () => {
  emit('success')
  handleClose()
}

const handleClose = () => {
  if (jobStats.value.status === 'running') {
    ElMessage.info('任务将在后台继续运行')
  }
  
  stopPolling()
  resetState()
  visible.value = false
}

const startPolling = () => {
  // 每2秒轮询一次任务状态
  pollingTimer = window.setInterval(async () => {
    await fetchJobStatus()
  }, 2000)
}

const stopPolling = () => {
  if (pollingTimer) {
    clearInterval(pollingTimer)
    pollingTimer = null
  }
}

const fetchJobStatus = async () => {
  try {
    const response = await annotationApi.getBatchJobStatus(jobId.value)
    jobStats.value = response.data

    // 如果任务完成或失败，停止轮询
    if (['completed', 'failed', 'cancelled'].includes(jobStats.value.status)) {
      stopPolling()
      
      if (jobStats.value.status === 'completed') {
        ElMessage.success('批量标注任务已完成')
        emit('success')
      } else if (jobStats.value.status === 'failed') {
        ElMessage.error('批量标注任务失败')
      }
    }
  } catch (error: any) {
    console.error('获取任务状态失败:', error)
  }
}

const formatTime = (timeString?: string) => {
  if (!timeString) return '-'
  try {
    return format(new Date(timeString), 'yyyy-MM-dd HH:mm:ss')
  } catch {
    return timeString
  }
}

const resetState = () => {
  jobStarted.value = false
  starting.value = false
  cancelling.value = false
  jobId.value = ''
  jobStats.value = {
    job_id: '',
    dataset_id: '',
    status: 'pending',
    total_tasks: 0,
    completed_tasks: 0,
    failed_tasks: 0,
    processing_tasks: 0
  }
}

// 监听对话框关闭
watch(visible, (newVal) => {
  if (!newVal) {
    stopPolling()
  }
})
</script>
⋮----
<style scoped lang="scss">
.dialog-content {
  .dataset-info {
    margin-top: 20px;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 4px;

    .info-item {
      display: flex;
      align-items: center;
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }

      .label {
        font-size: 14px;
        color: #606266;
        min-width: 100px;
      }

      .value {
        font-size: 14px;
        color: #303133;
        font-weight: 600;
      }
    }
  }
}

.progress-content {
  .progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h3 {
      margin: 0;
      font-size: 16px;
      color: #303133;
    }
  }

  .progress-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;

    .stat-item {
      text-align: center;
      padding: 12px;
      background: #f5f7fa;
      border-radius: 4px;

      .stat-label {
        font-size: 12px;
        color: #909399;
        margin-bottom: 8px;
      }

      .stat-value {
        font-size: 24px;
        font-weight: 600;
        color: #303133;

        &.success {
          color: #67c23a;
        }

        &.danger {
          color: #f56c6c;
        }

        &.warning {
          color: #e6a23c;
        }
      }
    }
  }

  .progress-bar {
    margin-bottom: 20px;

    .progress-label {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      font-size: 14px;
      color: #606266;

      .progress-percent {
        font-weight: 600;
        color: #409eff;
      }
    }
  }

  .error-section {
    margin-bottom: 20px;
  }

  .time-info {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    color: #909399;
    padding-top: 16px;
    border-top: 1px solid #ebeef5;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
````

## File: frontend/src/components/dataset/CorpusSelector.vue
````vue
<template>
  <div class="corpus-selector">
    <!-- 选择模式切换 -->
    <div class="mode-selector">
      <el-radio-group v-model="selectionMode" @change="handleModeChange">
        <el-radio-button label="sentence">
          <el-icon><List /></el-icon>
          句子级选择
        </el-radio-button>
        <el-radio-button label="file">
          <el-icon><FolderOpened /></el-icon>
          按文件选择
        </el-radio-button>
        <el-radio-button label="row">
          <el-icon><Document /></el-icon>
          按行选择
        </el-radio-button>
      </el-radio-group>

      <!-- 通用筛选：是否包含图片 -->
      <el-checkbox v-model="showOnlyWithImages" @change="handleImageFilterChange('with')" style="margin-left: 16px">
        <el-icon><Picture /></el-icon>
        仅显示含图片
      </el-checkbox>
      <el-checkbox v-model="showOnlyWithoutImages" @change="handleImageFilterChange('without')" style="margin-left: 8px">
        仅显示非图片
      </el-checkbox>

      <el-button
        size="small"
        :icon="CloseBold"
        @click="handleClearSelection"
        style="margin-left: auto"
      >
        清空选择
      </el-button>
    </div>

    <!-- 句子级选择模式的筛选工具栏 -->
    <div v-if="selectionMode === 'sentence'" class="filter-toolbar">
      <el-input
        v-model="searchFileName"
        placeholder="按文件名搜索"
        clearable
        style="width: 200px"
        @change="handleFilterChange"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="selectedType"
        placeholder="按字段分类筛选"
        clearable
        style="width: 180px"
        @change="handleFilterChange"
      >
        <el-option label="全部" value="" />
        <el-option label="问题描述" value="问题描述" />
        <el-option label="原因分析" value="原因分析" />
        <el-option label="采取措施" value="采取措施" />
        <el-option label="问题处理" value="问题处理" />
        <el-option label="质量问题" value="质量问题" />
      </el-select>

      <el-input-number
        v-model="rowStart"
        placeholder="起始行"
        :min="1"
        :controls="false"
        style="width: 100px"
        @change="handleFilterChange"
      />
      <span style="margin: 0 4px">-</span>
      <el-input-number
        v-model="rowEnd"
        placeholder="结束行"
        :min="rowStart || 1"
        :controls="false"
        style="width: 100px"
        @change="handleFilterChange"
      />

      <el-button
        size="small"
        :icon="Select"
        @click="handleSelectAll"
      >
        全选当前页
      </el-button>
    </div>

    <!-- 内容区域 -->
    <div v-loading="loading" class="content-area">
      <!-- 模式1: 句子级列表 -->
      <div v-if="selectionMode === 'sentence'" class="corpus-table">
        <el-table
          ref="tableRef"
          :data="corpusList"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="text_id" label="ID" width="150" show-overflow-tooltip />
          <el-table-column prop="text_type" label="字段分类" width="120">
            <template #default="{ row }">
              <el-tag size="small" type="info">{{ row.text_type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="text" label="内容" min-width="300" show-overflow-tooltip />
          <el-table-column prop="source_file" label="来源文件" width="180" show-overflow-tooltip />
          <el-table-column prop="source_row" label="行号" width="80" align="center" />
          <el-table-column label="图片" width="80" align="center">
            <template #default="{ row }">
              <el-tag v-if="row.has_images" size="small" type="warning">
                <el-icon><Picture /></el-icon>
                {{ row.images?.length || 0 }}
              </el-tag>
              <span v-else class="no-image">-</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 模式2: 按文件选择 -->
      <div v-else-if="selectionMode === 'file'" class="file-selector">
        <el-empty v-if="fileGroups.length === 0" description="暂无文件" />
        <div v-else class="file-list">
          <div
            v-for="file in fileGroups"
            :key="file.name"
            class="file-item"
            :class="{ selected: isFileSelected(file.name) }"
            @click="handleSelectFile(file.name)"
          >
            <el-checkbox :model-value="isFileSelected(file.name)" @click.stop />
            <el-icon class="file-icon"><Document /></el-icon>
            <div class="file-info">
              <span class="file-name">{{ file.name }}</span>
              <span class="file-stats">
                <el-tag size="small" type="info">{{ file.count }} 条语料</el-tag>
                <el-tag v-if="file.imageCount > 0" size="small" type="warning">
                  <el-icon><Picture /></el-icon>
                  {{ file.imageCount }} 张图片
                </el-tag>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 模式3: 按行选择 -->
      <div v-else-if="selectionMode === 'row'" class="row-selector">
        <el-empty v-if="rowGroups.length === 0" description="暂无数据" />
        <div v-else class="row-list">
          <div
            v-for="row in rowGroups"
            :key="`${row.file}|||${row.row}`"
            class="row-item"
            :class="{ selected: isRowSelected(row.file, row.row) }"
            @click="handleSelectRow(row.file, row.row)"
          >
            <el-checkbox :model-value="isRowSelected(row.file, row.row)" @click.stop />
            <div class="row-info">
              <div class="row-header">
                <span class="row-title">{{ row.file }} - 第 {{ row.row }} 行</span>
                <span class="row-stats">
                  <el-tag size="small" type="info">{{ row.count }} 个字段</el-tag>
                  <el-tag v-if="row.imageCount > 0" size="small" type="warning">
                    <el-icon><Picture /></el-icon>
                    {{ row.imageCount }} 张图片
                  </el-tag>
                </span>
              </div>
              <div class="row-preview">
                <el-tag
                  v-for="field in row.fields"
                  :key="field.text_id"
                  size="small"
                  type="info"
                  style="margin-right: 8px"
                >
                  {{ field.text_type }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页（仅在句子级选择模式显示） -->
    <div v-if="selectionMode === 'sentence'" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 文件/行模式的数据提示 -->
    <div v-else class="mode-info">
      <el-alert
        type="info"
        :closable="false"
        show-icon
      >
        <template #title>
          <span v-if="selectionMode === 'file'">
            当前显示 {{ fileGroups.length }} 个文件，共 {{ total }} 条语料
          </span>
          <span v-else-if="selectionMode === 'row'">
            当前显示 {{ rowGroups.length }} 行，共 {{ total }} 条语料
          </span>
        </template>
      </el-alert>
    </div>

    <!-- 已选择统计 -->
    <div class="selection-summary">
      <div class="summary-title">
        <el-icon><Select /></el-icon>
        已选择 {{ selectedIds.length }} 条语料
      </div>
      <div v-if="selectedIds.length > 0" class="summary-details">
        <div class="detail-item">
          <span class="label">按文件:</span>
          <el-tag
            v-for="(count, file) in selectedByFile"
            :key="file"
            size="small"
            style="margin-right: 8px"
          >
            {{ file }}: {{ count }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">按分类:</span>
          <el-tag
            v-for="(count, type) in selectedByType"
            :key="type"
            size="small"
            type="info"
            style="margin-right: 8px"
          >
            {{ type }}: {{ count }}
          </el-tag>
        </div>
      </div>
    </div>
  </div>
</template>
⋮----
<!-- 选择模式切换 -->
⋮----
<!-- 通用筛选：是否包含图片 -->
⋮----
<!-- 句子级选择模式的筛选工具栏 -->
⋮----
<template #prefix>
          <el-icon><Search /></el-icon>
        </template>
⋮----
<!-- 内容区域 -->
⋮----
<!-- 模式1: 句子级列表 -->
⋮----
<template #default="{ row }">
              <el-tag size="small" type="info">{{ row.text_type }}</el-tag>
            </template>
⋮----
<el-tag size="small" type="info">{{ row.text_type }}</el-tag>
⋮----
<template #default="{ row }">
              <el-tag v-if="row.has_images" size="small" type="warning">
                <el-icon><Picture /></el-icon>
                {{ row.images?.length || 0 }}
              </el-tag>
              <span v-else class="no-image">-</span>
            </template>
⋮----
{{ row.images?.length || 0 }}
⋮----
<!-- 模式2: 按文件选择 -->
⋮----
<span class="file-name">{{ file.name }}</span>
⋮----
<el-tag size="small" type="info">{{ file.count }} 条语料</el-tag>
⋮----
{{ file.imageCount }} 张图片
⋮----
<!-- 模式3: 按行选择 -->
⋮----
<span class="row-title">{{ row.file }} - 第 {{ row.row }} 行</span>
⋮----
<el-tag size="small" type="info">{{ row.count }} 个字段</el-tag>
⋮----
{{ row.imageCount }} 张图片
⋮----
{{ field.text_type }}
⋮----
<!-- 分页（仅在句子级选择模式显示） -->
⋮----
<!-- 文件/行模式的数据提示 -->
⋮----
<template #title>
          <span v-if="selectionMode === 'file'">
            当前显示 {{ fileGroups.length }} 个文件，共 {{ total }} 条语料
          </span>
          <span v-else-if="selectionMode === 'row'">
            当前显示 {{ rowGroups.length }} 行，共 {{ total }} 条语料
          </span>
        </template>
⋮----
当前显示 {{ fileGroups.length }} 个文件，共 {{ total }} 条语料
⋮----
当前显示 {{ rowGroups.length }} 行，共 {{ total }} 条语料
⋮----
<!-- 已选择统计 -->
⋮----
已选择 {{ selectedIds.length }} 条语料
⋮----
{{ file }}: {{ count }}
⋮----
{{ type }}: {{ count }}
⋮----
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Search,
  FolderOpened,
  List,
  Select,
  CloseBold,
  Document,
  Picture
} from '@element-plus/icons-vue'
import { useCorpusStore } from '@/stores'
import type { Corpus } from '@/types'
import type { ElTable } from 'element-plus'

const corpusStore = useCorpusStore()

// 选择模式
type SelectionMode = 'sentence' | 'file' | 'row'
const selectionMode = ref<SelectionMode>('sentence')

// 状态
const searchFileName = ref('')
const selectedType = ref('')
const rowStart = ref<number>()
const rowEnd = ref<number>()
const showOnlyWithImages = ref(false)
const showOnlyWithoutImages = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const selectedIds = ref<string[]>([])
const tableRef = ref<InstanceType<typeof ElTable>>()

// 计算属性
const loading = computed(() => corpusStore.loading)
const corpusList = computed(() => corpusStore.corpusList)
const total = computed(() => corpusStore.total)

// 文件分组（增强版，包含图片统计）
const fileGroups = computed(() => {
  const groups = new Map<string, { count: number; imageCount: number }>()
  corpusList.value.forEach(corpus => {
    const existing = groups.get(corpus.source_file) || { count: 0, imageCount: 0 }
    groups.set(corpus.source_file, {
      count: existing.count + 1,
      imageCount: existing.imageCount + (corpus.images?.length || 0)
    })
  })
  return Array.from(groups.entries()).map(([name, stats]) => ({ 
    name, 
    count: stats.count,
    imageCount: stats.imageCount
  }))
})

// 行分组（增强版，包含字段预览和图片统计）
const rowGroups = computed(() => {
  const groups = new Map<string, { count: number; imageCount: number; fields: Corpus[] }>()
  corpusList.value.forEach(corpus => {
    // 使用特殊分隔符避免文件名中的 - 干扰
    const key = `${corpus.source_file}|||${corpus.source_row}`
    const existing = groups.get(key) || { count: 0, imageCount: 0, fields: [] }
    groups.set(key, {
      count: existing.count + 1,
      imageCount: existing.imageCount + (corpus.images?.length || 0),
      fields: [...existing.fields, corpus]
    })
  })
  return Array.from(groups.entries()).map(([key, stats]) => {
    const [file, row] = key.split('|||')
    return { 
      file, 
      row: parseInt(row), 
      count: stats.count,
      imageCount: stats.imageCount,
      fields: stats.fields
    }
  })
})

// 全局统计：基于所有已选择的ID（不仅仅是当前页）
// 需要从后端获取完整的语料信息来统计
const allSelectedCorpus = ref<Corpus[]>([])

// 按文件统计选择（基于全局）
const selectedByFile = computed(() => {
  const stats: Record<string, number> = {}
  
  // 统计当前页的
  corpusList.value.forEach(corpus => {
    if (selectedIds.value.includes(corpus.text_id)) {
      stats[corpus.source_file] = (stats[corpus.source_file] || 0) + 1
    }
  })
  
  // 统计已缓存的其他页的
  allSelectedCorpus.value.forEach(corpus => {
    if (selectedIds.value.includes(corpus.text_id) && 
        !corpusList.value.find(c => c.text_id === corpus.text_id)) {
      stats[corpus.source_file] = (stats[corpus.source_file] || 0) + 1
    }
  })
  
  return stats
})

// 按分类统计选择（基于全局）
const selectedByType = computed(() => {
  const stats: Record<string, number> = {}
  
  // 统计当前页的
  corpusList.value.forEach(corpus => {
    if (selectedIds.value.includes(corpus.text_id)) {
      stats[corpus.text_type] = (stats[corpus.text_type] || 0) + 1
    }
  })
  
  // 统计已缓存的其他页的
  allSelectedCorpus.value.forEach(corpus => {
    if (selectedIds.value.includes(corpus.text_id) && 
        !corpusList.value.find(c => c.text_id === corpus.text_id)) {
      stats[corpus.text_type] = (stats[corpus.text_type] || 0) + 1
    }
  })
  
  return stats
})

// 方法
const fetchList = async () => {
  // 在文件/行选择模式下，使用更大的页面大小以获取更多数据
  const effectivePageSize = (selectionMode.value === 'file' || selectionMode.value === 'row') 
    ? 1000  // 使用后端允许的最大值（已提高到1000）
    : pageSize.value

  await corpusStore.fetchList({
    page: currentPage.value,
    page_size: effectivePageSize,
    source_file: searchFileName.value || undefined,
    source_field: selectedType.value || undefined,
    has_images: showOnlyWithImages.value ? true : (showOnlyWithoutImages.value ? false : undefined)
  })
}

const handleModeChange = () => {
  // 切换模式时重置筛选条件（保留"是否包含图片"）
  searchFileName.value = ''
  selectedType.value = ''
  rowStart.value = undefined
  rowEnd.value = undefined
  currentPage.value = 1
  
  // 切换到文件/行模式时，加载更多数据
  fetchList()
}

const handleImageFilterChange = (which: 'with' | 'without') => {
  // 两个图片筛选互斥
  if (which === 'with' && showOnlyWithImages.value) {
    showOnlyWithoutImages.value = false
  } else if (which === 'without' && showOnlyWithoutImages.value) {
    showOnlyWithImages.value = false
  }
  // 切换图片筛选时重置选择状态（清除上次选择的语料）
  handleClearSelection()
  currentPage.value = 1
  fetchList()
}

const handleFilterChange = () => {
  // 文件名搜索或字段分类筛选的变更需要重置选择，避免保留其他页数据的历史选择
  handleClearSelection()
  currentPage.value = 1
  fetchList()
}

const handlePageChange = () => {
  fetchList()
}

const handleSelectionChange = (selection: Corpus[]) => {
  // 更新选中的ID列表（仅在句子级选择模式）
  const currentPageIds = corpusList.value.map(c => c.text_id)
  // 移除当前页的所有ID
  selectedIds.value = selectedIds.value.filter(id => !currentPageIds.includes(id))
  // 添加新选中的ID
  selectedIds.value.push(...selection.map(c => c.text_id))
  
  // 缓存选中的语料信息（用于统计）
  updateSelectedCorpusCache(selection)
}

const handleSelectAll = () => {
  if (!tableRef.value) return
  tableRef.value.toggleAllSelection()
}

const handleClearSelection = () => {
  selectedIds.value = []
  allSelectedCorpus.value = []
  if (tableRef.value) {
    tableRef.value.clearSelection()
  }
}

const isFileSelected = (fileName: string) => {
  const fileCorpus = corpusList.value.filter(c => c.source_file === fileName)
  if (fileCorpus.length === 0) return false
  return fileCorpus.every(c => selectedIds.value.includes(c.text_id))
}

const handleSelectFile = (fileName: string) => {
  const fileCorpus = corpusList.value.filter(c => c.source_file === fileName)
  const fileTextIds = fileCorpus.map(c => c.text_id)
  
  if (isFileSelected(fileName)) {
    // 取消选择
    selectedIds.value = selectedIds.value.filter(id => !fileTextIds.includes(id))
    // 从缓存中移除
    allSelectedCorpus.value = allSelectedCorpus.value.filter(c => !fileTextIds.includes(c.text_id))
  } else {
    // 选择
    selectedIds.value = [...new Set([...selectedIds.value, ...fileTextIds])]
    // 添加到缓存
    updateSelectedCorpusCache(fileCorpus)
  }
}

const isRowSelected = (fileName: string, row: number) => {
  const rowCorpus = corpusList.value.filter(
    c => c.source_file === fileName && c.source_row === row
  )
  if (rowCorpus.length === 0) return false
  return rowCorpus.every(c => selectedIds.value.includes(c.text_id))
}

const handleSelectRow = (fileName: string, row: number) => {
  const rowCorpus = corpusList.value.filter(
    c => c.source_file === fileName && c.source_row === row
  )
  const rowTextIds = rowCorpus.map(c => c.text_id)
  
  if (isRowSelected(fileName, row)) {
    // 取消选择
    selectedIds.value = selectedIds.value.filter(id => !rowTextIds.includes(id))
    // 从缓存中移除
    allSelectedCorpus.value = allSelectedCorpus.value.filter(c => !rowTextIds.includes(c.text_id))
  } else {
    // 选择
    selectedIds.value = [...new Set([...selectedIds.value, ...rowTextIds])]
    // 添加到缓存
    updateSelectedCorpusCache(rowCorpus)
  }
}

// 更新选中语料的缓存
const updateSelectedCorpusCache = (newSelection: Corpus[]) => {
  newSelection.forEach(corpus => {
    // 如果不在缓存中，添加进去
    if (!allSelectedCorpus.value.find(c => c.text_id === corpus.text_id)) {
      allSelectedCorpus.value.push(corpus)
    }
  })
  
  // 清理缓存：移除未选中的
  allSelectedCorpus.value = allSelectedCorpus.value.filter(c => 
    selectedIds.value.includes(c.text_id)
  )
}

const updateTableSelection = () => {
  if (!tableRef.value || selectionMode.value !== 'sentence') return
  
  corpusList.value.forEach(corpus => {
    const isSelected = selectedIds.value.includes(corpus.text_id)
    tableRef.value!.toggleRowSelection(corpus, isSelected)
  })
}

// 监听语料列表变化，更新表格选择状态
watch(corpusList, () => {
  updateTableSelection()
}, { immediate: true })

// 生命周期
onMounted(() => {
  fetchList()
})

// 暴露方法供父组件调用
defineExpose({
  getSelectedIds: () => selectedIds.value,
  getSelectedCorpus: () => {
    // 返回选中的完整 Corpus 对象
    // 从当前页和缓存中获取
    const selected: Corpus[] = []
    
    // 从当前页获取
    corpusList.value.forEach(corpus => {
      if (selectedIds.value.includes(corpus.text_id)) {
        selected.push(corpus)
      }
    })
    
    // 从缓存获取（其他页的）
    allSelectedCorpus.value.forEach(corpus => {
      if (selectedIds.value.includes(corpus.text_id) && 
          !selected.find(c => c.text_id === corpus.text_id)) {
        selected.push(corpus)
      }
    })
    
    return selected
  },
  clearSelection: handleClearSelection
})
</script>
⋮----
<style scoped lang="scss">
.corpus-selector {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .mode-selector {
    display: flex;
    align-items: center;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 8px;
    gap: 16px;
  }

  .filter-toolbar {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    padding: 12px;
    background: #fff;
    border: 1px solid #ebeef5;
    border-radius: 8px;
  }

  .content-area {
    min-height: 400px;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    background: #fff;

    .corpus-table {
      .no-image {
        color: #c0c4cc;
      }
    }

    .file-selector,
    .row-selector {
      padding: 16px;

      .file-list,
      .row-list {
        display: flex;
        flex-direction: column;
        gap: 12px;
        max-height: 500px;
        overflow-y: auto;
      }

      .file-item,
      .row-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px;
        background: #f5f7fa;
        border: 2px solid transparent;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;

        &:hover {
          background: #ecf5ff;
          border-color: #b3d8ff;
        }

        &.selected {
          background: #ecf5ff;
          border-color: #409eff;
        }

        .file-icon {
          font-size: 24px;
          color: #409eff;
        }

        .file-info,
        .row-info {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 8px;

          .file-name,
          .row-title {
            font-size: 14px;
            font-weight: 600;
            color: #303133;
          }

          .file-stats,
          .row-stats {
            display: flex;
            gap: 8px;
          }

          .row-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
          }

          .row-preview {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
          }
        }
      }
    }
  }

  .pagination {
    display: flex;
    justify-content: center;
    padding: 16px;
    background: #fff;
    border: 1px solid #ebeef5;
    border-radius: 8px;
  }

  .mode-info {
    padding: 16px;
    background: #fff;
    border: 1px solid #ebeef5;
    border-radius: 8px;
  }

  .selection-summary {
    padding: 16px;
    background: #f0f9ff;
    border: 1px solid #b3d8ff;
    border-radius: 8px;

    .summary-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 16px;
      font-weight: 600;
      color: #409eff;
      margin-bottom: 12px;
    }

    .summary-details {
      display: flex;
      flex-direction: column;
      gap: 8px;

      .detail-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        flex-wrap: wrap;

        .label {
          color: #606266;
          font-weight: 500;
          min-width: 60px;
        }
      }
    }
  }
}
</style>
````

## File: frontend/src/components/dataset/DatasetCard.vue
````vue
<template>
  <el-card class="dataset-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="dataset-name">
          <el-icon class="dataset-icon"><Folder /></el-icon>
          <span class="name-text">{{ dataset.name }}</span>
          <el-tag :type="statusTagType" size="small" class="status-tag">
            {{ statusText }}
          </el-tag>
        </div>
        <el-dropdown trigger="click" @command="handleCommand">
          <el-icon class="more-icon"><MoreFilled /></el-icon>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="view" :icon="View">
                查看详情
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="batchAnnotate" 
                :icon="MagicStick"
              >
                批量标注
              </el-dropdown-item>
              <!-- Task 47: 分配管理（仅管理员可见） -->
              <el-dropdown-item 
                v-if="isAdmin" 
                command="assign" 
                :icon="Setting"
              >
                分配管理
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="edit" 
                :icon="Edit"
              >
                编辑
              </el-dropdown-item>
              <el-dropdown-item 
                command="export" 
                :icon="Download"
                :disabled="datasetStatus === 'empty'"
              >
                导出
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="delete" 
                :icon="Delete" 
                divided
              >
                删除
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </template>

    <div class="card-content">
      <!-- 描述 -->
      <div v-if="dataset.description" class="description">
        {{ dataset.description }}
      </div>
      <div v-else class="description empty">
        暂无描述
      </div>

      <!-- 统计信息 -->
      <div class="statistics">
        <div class="stat-item">
          <div class="stat-label">总任务数</div>
          <div class="stat-value">{{ statistics.total_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">已标注</div>
          <div class="stat-value completed">{{ statistics.completed_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">已复核</div>
          <div class="stat-value reviewed">{{ statistics.reviewed_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">待处理</div>
          <div class="stat-value pending">{{ statistics.pending_tasks }}</div>
        </div>
      </div>

      <!-- 进度条 -->
      <div class="progress-section">
        <div class="progress-label">
          <span>完成进度</span>
          <span class="progress-percent">{{ completionRate }}%</span>
        </div>
        <el-progress
          :percentage="completionRate"
          :color="progressColor"
          :show-text="false"
        />
      </div>

      <!-- 元信息 -->
      <div class="meta-info">
        <span class="meta-item">
          <el-icon><Clock /></el-icon>
          {{ formatDate(dataset.created_at) }}
        </span>
      </div>
    </div>

    <template #footer>
      <div class="card-footer">
        <el-button size="small" @click="handleView">
          查看详情
        </el-button>
        <el-button 
          v-if="!isViewer" 
          size="small" 
          type="primary" 
          @click="handleStartAnnotation"
        >
          开始标注
        </el-button>
        <el-tooltip
          v-else
          :disabled="datasetStatus !== 'empty'"
          content="数据集为空,无法导出"
          placement="top"
        >
          <span>
            <el-button 
              size="small" 
              type="primary" 
              :disabled="datasetStatus === 'empty'"
              @click="handleCommand('export')"
            >
              导出数据
            </el-button>
          </span>
        </el-tooltip>
      </div>
    </template>
  </el-card>
</template>
⋮----
<template #header>
      <div class="card-header">
        <div class="dataset-name">
          <el-icon class="dataset-icon"><Folder /></el-icon>
          <span class="name-text">{{ dataset.name }}</span>
          <el-tag :type="statusTagType" size="small" class="status-tag">
            {{ statusText }}
          </el-tag>
        </div>
        <el-dropdown trigger="click" @command="handleCommand">
          <el-icon class="more-icon"><MoreFilled /></el-icon>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="view" :icon="View">
                查看详情
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="batchAnnotate" 
                :icon="MagicStick"
              >
                批量标注
              </el-dropdown-item>
              <!-- Task 47: 分配管理（仅管理员可见） -->
              <el-dropdown-item 
                v-if="isAdmin" 
                command="assign" 
                :icon="Setting"
              >
                分配管理
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="edit" 
                :icon="Edit"
              >
                编辑
              </el-dropdown-item>
              <el-dropdown-item 
                command="export" 
                :icon="Download"
                :disabled="datasetStatus === 'empty'"
              >
                导出
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="delete" 
                :icon="Delete" 
                divided
              >
                删除
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </template>
⋮----
<span class="name-text">{{ dataset.name }}</span>
⋮----
{{ statusText }}
⋮----
<template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="view" :icon="View">
                查看详情
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="batchAnnotate" 
                :icon="MagicStick"
              >
                批量标注
              </el-dropdown-item>
              <!-- Task 47: 分配管理（仅管理员可见） -->
              <el-dropdown-item 
                v-if="isAdmin" 
                command="assign" 
                :icon="Setting"
              >
                分配管理
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="edit" 
                :icon="Edit"
              >
                编辑
              </el-dropdown-item>
              <el-dropdown-item 
                command="export" 
                :icon="Download"
                :disabled="datasetStatus === 'empty'"
              >
                导出
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="delete" 
                :icon="Delete" 
                divided
              >
                删除
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
⋮----
<!-- Task 47: 分配管理（仅管理员可见） -->
⋮----
<!-- 描述 -->
⋮----
{{ dataset.description }}
⋮----
<!-- 统计信息 -->
⋮----
<div class="stat-value">{{ statistics.total_tasks }}</div>
⋮----
<div class="stat-value completed">{{ statistics.completed_tasks }}</div>
⋮----
<div class="stat-value reviewed">{{ statistics.reviewed_tasks }}</div>
⋮----
<div class="stat-value pending">{{ statistics.pending_tasks }}</div>
⋮----
<!-- 进度条 -->
⋮----
<span class="progress-percent">{{ completionRate }}%</span>
⋮----
<!-- 元信息 -->
⋮----
{{ formatDate(dataset.created_at) }}
⋮----
<template #footer>
      <div class="card-footer">
        <el-button size="small" @click="handleView">
          查看详情
        </el-button>
        <el-button 
          v-if="!isViewer" 
          size="small" 
          type="primary" 
          @click="handleStartAnnotation"
        >
          开始标注
        </el-button>
        <el-tooltip
          v-else
          :disabled="datasetStatus !== 'empty'"
          content="数据集为空,无法导出"
          placement="top"
        >
          <span>
            <el-button 
              size="small" 
              type="primary" 
              :disabled="datasetStatus === 'empty'"
              @click="handleCommand('export')"
            >
              导出数据
            </el-button>
          </span>
        </el-tooltip>
      </div>
    </template>
⋮----
<script setup lang="ts">
import { computed } from 'vue'
import {
  Folder,
  MoreFilled,
  View,
  Edit,
  Download,
  Delete,
  Clock,
  MagicStick,
  Setting
} from '@element-plus/icons-vue'
import type { Dataset, DatasetStatistics, DatasetStatus } from '@/types'
import { formatDateRelative } from '@/utils/datetime'

interface Props {
  dataset: Dataset
  isViewer?: boolean
  isAdmin?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isViewer: false,
  isAdmin: false
})

const emit = defineEmits<{
  view: [dataset: Dataset]
  edit: [dataset: Dataset]
  delete: [dataset: Dataset]
  export: [dataset: Dataset]
  batchAnnotate: [dataset: Dataset]
  assign: [dataset: Dataset]
}>()

// 计算属性
const statistics = computed<DatasetStatistics>(() => {
  return props.dataset.statistics || {
    total_tasks: 0,
    completed_tasks: 0,
    reviewed_tasks: 0,
    pending_tasks: 0
  }
})

const completionRate = computed(() => {
  const total = statistics.value.total_tasks
  if (total === 0) return 0
  return Math.round((statistics.value.completed_tasks / total) * 100)
})

const progressColor = computed(() => {
  const rate = completionRate.value
  if (rate === 100) return '#67c23a'
  if (rate >= 50) return '#409eff'
  return '#e6a23c'
})

const datasetStatus = computed<DatasetStatus>(() => {
  const total = statistics.value.total_tasks
  const completed = statistics.value.completed_tasks
  
  if (total === 0) return 'empty'
  if (completed < total) return 'in_progress'
  return 'completed'
})

const statusText = computed(() => {
  switch (datasetStatus.value) {
    case 'empty':
      return '空'
    case 'in_progress':
      return '进行中'
    case 'completed':
      return '已完成'
    default:
      return ''
  }
})

const statusTagType = computed(() => {
  switch (datasetStatus.value) {
    case 'empty':
      return 'info'
    case 'in_progress':
      return 'warning'
    case 'completed':
      return 'success'
    default:
      return 'info'
  }
})

// 方法
const formatDate = (dateString: string) => formatDateRelative(dateString)

const handleCommand = (command: string) => {
  switch (command) {
    case 'view':
      emit('view', props.dataset)
      break
    case 'batchAnnotate':
      emit('batchAnnotate', props.dataset)
      break
    case 'assign':
      emit('assign', props.dataset)
      break
    case 'edit':
      emit('edit', props.dataset)
      break
    case 'export':
      emit('export', props.dataset)
      break
    case 'delete':
      emit('delete', props.dataset)
      break
  }
}

const handleView = () => {
  emit('view', props.dataset)
}

const handleStartAnnotation = () => {
  // 跳转到数据集详情页面，查看任务列表
  emit('view', props.dataset)
}
</script>
⋮----
<style scoped lang="scss">
.dataset-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .dataset-name {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1;
      min-width: 0;

      .dataset-icon {
        font-size: 20px;
        color: #409eff;
        flex-shrink: 0;
      }

      .name-text {
        font-size: 16px;
        font-weight: 600;
        color: #303133;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .status-tag {
        flex-shrink: 0;
        margin-left: auto;
      }
    }

    .more-icon {
      font-size: 20px;
      color: #909399;
      cursor: pointer;
      flex-shrink: 0;

      &:hover {
        color: #409eff;
      }
    }
  }

  .card-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 16px;

    .description {
      font-size: 14px;
      line-height: 1.6;
      color: #606266;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;

      &.empty {
        color: #c0c4cc;
        font-style: italic;
      }
    }

    .statistics {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;

      .stat-item {
        text-align: center;

        .stat-label {
          font-size: 12px;
          color: #909399;
          margin-bottom: 4px;
        }

        .stat-value {
          font-size: 20px;
          font-weight: 600;
          color: #303133;

          &.completed {
            color: #67c23a;
          }

          &.reviewed {
            color: #409eff;
          }

          &.pending {
            color: #e6a23c;
          }
        }
      }
    }

    .progress-section {
      .progress-label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        font-size: 13px;
        color: #606266;

        .progress-percent {
          font-weight: 600;
          color: #409eff;
        }
      }
    }

    .meta-info {
      display: flex;
      gap: 16px;
      font-size: 13px;
      color: #909399;

      .meta-item {
        display: flex;
        align-items: center;
        gap: 4px;

        .el-icon {
          font-size: 14px;
        }
      }
    }
  }

  .card-footer {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
  }
}
</style>
````

## File: frontend/src/components/dataset/DatasetCreateDialog.vue
````vue
<template>
  <el-dialog
    v-model="dialogVisible"
    title="创建数据集"
    width="90%"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="数据集名称" prop="name">
        <el-input
          v-model="formData.name"
          placeholder="请输入数据集名称"
          maxlength="100"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="数据集描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入数据集描述（可选）"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="选择语料" required>
        <div class="corpus-selector-wrapper">
          <CorpusSelector ref="corpusSelectorRef" />
        </div>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button
          type="primary"
          :loading="loading"
          @click="handleSubmit"
        >
          创建数据集
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>
⋮----
<template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button
          type="primary"
          :loading="loading"
          @click="handleSubmit"
        >
          创建数据集
        </el-button>
      </div>
    </template>
⋮----
<script setup lang="ts">
import { ref, computed, watch, h } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useDatasetStore, useAuthStore } from '@/stores'
import CorpusSelector from './CorpusSelector.vue'

interface Props {
  modelValue: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

const datasetStore = useDatasetStore()
const authStore = useAuthStore()

// 状态
const formRef = ref<FormInstance>()
const corpusSelectorRef = ref<InstanceType<typeof CorpusSelector>>()
const loading = ref(false)

const formData = ref({
  name: '',
  description: ''
  // 移除 corpus_ids，因为它不是表单字段，而是从 CorpusSelector 获取的
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入数据集名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ]
}

// 计算属性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 方法
const handleClose = () => {
  formRef.value?.resetFields()
  corpusSelectorRef.value?.clearSelection()
  dialogVisible.value = false
}

const handleSubmit = async () => {
  try {
    // 验证表单
    await formRef.value?.validate()

    // 获取选中的语料完整信息
    const selectedCorpus = corpusSelectorRef.value?.getSelectedCorpus() || []
    
    if (selectedCorpus.length === 0) {
      ElMessage.warning('请至少选择一条语料')
      return
    }

    // 提取数据库ID
    const corpusIds = selectedCorpus
      .map(corpus => corpus.id)
      .filter((id): id is number => id !== undefined)

    if (corpusIds.length === 0) {
      ElMessage.error('无法获取语料ID，请重试')
      return
    }

    if (corpusIds.length !== selectedCorpus.length) {
      ElMessage.warning(`部分语料缺少ID信息，将创建 ${corpusIds.length} 个任务`)
    }

    // 确认创建（VNode格式，支持换行）
    const confirmMessageVNode = h('div', [
      h('div', '即将创建数据集：'),
      h('div', [
        h('div', [`- 名称：${formData.value.name}`]),
        h('div', [`- 选中语料：${corpusIds.length} 条`]),
        h('div', [`- 将创建 ${corpusIds.length} 个标注任务`]),
      ]),
      h('div', { style: 'margin-top: 8px;' }, '确认创建吗？')
    ])
    await ElMessageBox.confirm(confirmMessageVNode, '确认创建', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    })

    loading.value = true

    // 调用API创建数据集
    await datasetStore.create({
      name: formData.value.name,
      description: formData.value.description,
      corpus_ids: corpusIds,  // 使用数据库ID
      created_by: authStore.user?.id || 1
    })

    ElMessage.success('数据集创建成功')
    emit('success')
    handleClose()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('创建数据集失败:', error)
      ElMessage.error(error.message || '创建失败')
    }
  } finally {
    loading.value = false
  }
}

// 监听对话框打开，重置表单
watch(dialogVisible, (newVal) => {
  if (newVal) {
    formData.value = {
      name: '',
      description: ''
    }
  }
})
</script>
⋮----
<style scoped lang="scss">
.corpus-selector-wrapper {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 16px;
  background: #fafafa;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
````

## File: frontend/src/components/dataset/DatasetEditDialog.vue
````vue
<template>
  <el-dialog
    v-model="dialogVisible"
    title="编辑数据集"
    width="500px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="数据集名称" prop="name">
        <el-input
          v-model="formData.name"
          placeholder="请输入数据集名称"
          maxlength="100"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="数据集描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入数据集描述（可选）"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button
          type="primary"
          :loading="loading"
          @click="handleSubmit"
        >
          保存
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>
⋮----
<template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button
          type="primary"
          :loading="loading"
          @click="handleSubmit"
        >
          保存
        </el-button>
      </div>
    </template>
⋮----
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useDatasetStore } from '@/stores'
import type { Dataset } from '@/api/dataset'

interface Props {
  modelValue: boolean
  dataset?: Dataset
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

const datasetStore = useDatasetStore()

// 状态
const formRef = ref<FormInstance>()
const loading = ref(false)

const formData = ref({
  name: '',
  description: ''
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入数据集名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ]
}

// 计算属性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 监听对话框打开，填充数据
watch(dialogVisible, (newVal) => {
  if (newVal && props.dataset) {
    formData.value = {
      name: props.dataset.name || '',
      description: props.dataset.description || ''
    }
  }
})

// 方法
const handleClose = () => {
  formRef.value?.resetFields()
  dialogVisible.value = false
}

const handleSubmit = async () => {
  try {
    // 验证表单
    await formRef.value?.validate()

    if (!props.dataset) {
      ElMessage.error('数据集信息缺失')
      return
    }

    loading.value = true

    // 调用API更新数据集
    await datasetStore.update(props.dataset.dataset_id, {
      name: formData.value.name,
      description: formData.value.description
    })

    ElMessage.success('数据集更新成功')
    emit('success')
    handleClose()
  } catch (error: any) {
    console.error('更新数据集失败:', error)
    ElMessage.error(error.message || '更新失败')
  } finally {
    loading.value = false
  }
}
</script>
⋮----
<style scoped lang="scss">
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
````

## File: frontend/src/components/label/DefinitionReview.vue
````vue
<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEntityType ? '审核实体类型定义' : '审核关系类型定义'"
    width="800px"
  >
    <el-form :model="formData" label-width="120px">
      <el-form-item label="类型名称">
        <el-input :value="typeName" disabled />
      </el-form-item>
      
      <el-form-item label="定义">
        <el-input
          v-model="formData.definition"
          type="textarea"
          :rows="4"
          placeholder="请输入或修改定义"
        />
      </el-form-item>

      <el-form-item label="方向规则" v-if="!isEntityType">
        <el-input
          v-model="formData.direction_rule"
          type="textarea"
          :rows="2"
          placeholder="请输入关系方向规则"
        />
      </el-form-item>

      <el-form-item label="示例">
        <el-tag
          v-for="(example, index) in formData.examples"
          :key="index"
          closable
          @close="removeExample(index)"
          style="margin-right: 8px; margin-bottom: 8px;"
        >
          {{ example }}
        </el-tag>
        <el-input
          v-model="newExample"
          placeholder="输入示例后按回车添加"
          @keyup.enter="addExample"
          style="width: 200px; margin-top: 8px;"
        />
      </el-form-item>

      <el-form-item label="消歧说明">
        <el-input
          v-model="formData.disambiguation"
          type="textarea"
          :rows="3"
          placeholder="请输入消歧说明"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleReject">驳回</el-button>
      <el-button type="primary" @click="handleApprove">批准</el-button>
    </template>
  </el-dialog>
</template>
⋮----
{{ example }}
⋮----
<template #footer>
      <el-button @click="handleReject">驳回</el-button>
      <el-button type="primary" @click="handleApprove">批准</el-button>
    </template>
⋮----
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import type { EntityType, RelationType } from '@/api/label'

interface Props {
  visible: boolean
  entityType?: EntityType | null
  relationType?: RelationType | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
  'success': []
}>()

const labelStore = useLabelStore()
const newExample = ref('')

const formData = ref({
  definition: '',
  direction_rule: '',
  examples: [] as string[],
  disambiguation: ''
})

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const isEntityType = computed(() => !!props.entityType)

const typeName = computed(() => {
  if (props.entityType) {
    return `${props.entityType.type_name_zh} (${props.entityType.type_name})`
  }
  if (props.relationType) {
    return `${props.relationType.type_name_zh} (${props.relationType.type_name})`
  }
  return ''
})

watch(() => props.visible, (visible) => {
  if (visible) {
    if (props.entityType) {
      formData.value = {
        definition: props.entityType.definition || '',
        direction_rule: '',
        examples: props.entityType.examples || [],
        disambiguation: props.entityType.disambiguation || ''
      }
    } else if (props.relationType) {
      formData.value = {
        definition: props.relationType.definition || '',
        direction_rule: props.relationType.direction_rule || '',
        examples: props.relationType.examples || [],
        disambiguation: props.relationType.disambiguation || ''
      }
    }
  }
})

const addExample = () => {
  if (newExample.value.trim()) {
    formData.value.examples.push(newExample.value.trim())
    newExample.value = ''
  }
}

const removeExample = (index: number) => {
  formData.value.examples.splice(index, 1)
}

const handleApprove = async () => {
  try {
    if (props.entityType) {
      await labelStore.reviewEntityType(props.entityType.id, {
        approved: true,
        definition: formData.value.definition,
        examples: formData.value.examples,
        disambiguation: formData.value.disambiguation
      })
    } else if (props.relationType) {
      await labelStore.reviewRelationType(props.relationType.id, {
        approved: true,
        definition: formData.value.definition,
        direction_rule: formData.value.direction_rule,
        examples: formData.value.examples,
        disambiguation: formData.value.disambiguation
      })
    }
    emit('success')
    dialogVisible.value = false
  } catch (error) {
    ElMessage.error('审核失败')
  }
}

const handleReject = async () => {
  try {
    if (props.entityType) {
      await labelStore.reviewEntityType(props.entityType.id, {
        approved: false
      })
    } else if (props.relationType) {
      await labelStore.reviewRelationType(props.relationType.id, {
        approved: false
      })
    }
    ElMessage.success('已驳回')
    emit('success')
    dialogVisible.value = false
  } catch (error) {
    ElMessage.error('操作失败')
  }
}
</script>
````

## File: frontend/src/components/label/EntityTypeConfig.vue
````vue
<template>
  <div class="entity-type-config">
    <div class="toolbar">
      <el-button type="primary" @click="handleCreate">新建实体类型</el-button>
      <el-space>
        <el-checkbox v-model="showInactive">显示已停用</el-checkbox>
        <el-checkbox v-model="showUnreviewed">显示未审核</el-checkbox>
      </el-space>
    </div>

    <el-table :data="filteredEntityTypes" v-loading="labelStore.loading">
      <el-table-column prop="type_name" label="类型名称" width="150" />
      <el-table-column prop="type_name_zh" label="中文名称" width="150" />
      <el-table-column label="颜色" width="100">
        <template #default="{ row }">
          <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
            {{ row.type_name_zh }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="支持边界框" width="100">
        <template #default="{ row }">
          <el-tag :type="row.supports_bbox ? 'success' : 'info'" size="small">
            {{ row.supports_bbox ? '是' : '否' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="审核状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_reviewed ? 'success' : 'warning'" size="small">
            {{ row.is_reviewed ? '已审核' : '待审核' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
            {{ row.is_active ? '启用' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" @click="handleGenerateDefinition(row)">生成定义</el-button>
          <el-button size="small" @click="handleReview(row)" v-if="!row.is_reviewed">审核</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑实体类型' : '新建实体类型'"
      width="600px"
    >
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="类型名称" prop="type_name">
          <el-input v-model="formData.type_name" placeholder="英文名称，如 Product" />
        </el-form-item>
        <el-form-item label="中文名称" prop="type_name_zh">
          <el-input v-model="formData.type_name_zh" placeholder="中文名称，如 产品" />
        </el-form-item>
        <el-form-item label="颜色" prop="color">
          <el-color-picker v-model="formData.color" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="支持边界框">
          <el-switch v-model="formData.supports_bbox" />
        </el-form-item>
        <el-form-item label="启用状态" v-if="isEdit">
          <el-switch v-model="formData.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 审核对话框 -->
    <DefinitionReview
      v-model:visible="reviewDialogVisible"
      :entity-type="currentEntityType"
      @success="handleReviewSuccess"
    />
  </div>
</template>
⋮----
<template #default="{ row }">
          <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
            {{ row.type_name_zh }}
          </el-tag>
        </template>
⋮----
{{ row.type_name_zh }}
⋮----
<template #default="{ row }">
          <el-tag :type="row.supports_bbox ? 'success' : 'info'" size="small">
            {{ row.supports_bbox ? '是' : '否' }}
          </el-tag>
        </template>
⋮----
{{ row.supports_bbox ? '是' : '否' }}
⋮----
<template #default="{ row }">
          <el-tag :type="row.is_reviewed ? 'success' : 'warning'" size="small">
            {{ row.is_reviewed ? '已审核' : '待审核' }}
          </el-tag>
        </template>
⋮----
{{ row.is_reviewed ? '已审核' : '待审核' }}
⋮----
<template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
            {{ row.is_active ? '启用' : '停用' }}
          </el-tag>
        </template>
⋮----
{{ row.is_active ? '启用' : '停用' }}
⋮----
<template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" @click="handleGenerateDefinition(row)">生成定义</el-button>
          <el-button size="small" @click="handleReview(row)" v-if="!row.is_reviewed">审核</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
⋮----
<!-- 创建/编辑对话框 -->
⋮----
<template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
⋮----
<!-- 审核对话框 -->
⋮----
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import type { EntityType } from '@/api/label'
import DefinitionReview from './DefinitionReview.vue'

const labelStore = useLabelStore()
const showInactive = ref(false)
const showUnreviewed = ref(true)  // 默认显示未审核的标签（包括默认配置）
const dialogVisible = ref(false)
const reviewDialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const currentEntityType = ref<EntityType | null>(null)

const formData = ref({
  type_name: '',
  type_name_zh: '',
  color: '#409EFF',
  description: '',
  supports_bbox: false,
  is_active: true
})

const rules: FormRules = {
  type_name: [{ required: true, message: '请输入类型名称', trigger: 'blur' }],
  type_name_zh: [{ required: true, message: '请输入中文名称', trigger: 'blur' }],
  color: [{ required: true, message: '请选择颜色', trigger: 'change' }]
}

const filteredEntityTypes = computed(() => {
  return labelStore.entityTypes.filter(et => {
    if (!showInactive.value && !et.is_active) return false
    if (!showUnreviewed.value && !et.is_reviewed) return false
    return true
  })
})

const handleCreate = () => {
  isEdit.value = false
  formData.value = {
    type_name: '',
    type_name_zh: '',
    color: '#409EFF',
    description: '',
    supports_bbox: false,
    is_active: true
  }
  dialogVisible.value = true
}

const handleEdit = (row: EntityType) => {
  isEdit.value = true
  formData.value = {
    type_name: row.type_name,
    type_name_zh: row.type_name_zh,
    color: row.color,
    description: row.description || '',
    supports_bbox: row.supports_bbox,
    is_active: row.is_active
  }
  currentEntityType.value = row
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      if (isEdit.value && currentEntityType.value) {
        await labelStore.updateEntityType(currentEntityType.value.id, formData.value)
        ElMessage.success('更新成功')
      } else {
        await labelStore.createEntityType(formData.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    }
  })
}

const handleGenerateDefinition = async (row: EntityType) => {
  try {
    await ElMessageBox.confirm('确定要使用LLM生成该实体类型的定义吗？', '提示', {
      type: 'warning'
    })
    await labelStore.generateEntityDefinition(row.id)
    ElMessage.success('定义生成成功，请审核')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('生成失败')
    }
  }
}

const handleReview = (row: EntityType) => {
  currentEntityType.value = row
  reviewDialogVisible.value = true
}

const handleReviewSuccess = () => {
  ElMessage.success('审核成功')
  labelStore.fetchEntityTypes()
}

const handleDelete = async (row: EntityType) => {
  try {
    await ElMessageBox.confirm('确定要删除该实体类型吗？', '警告', {
      type: 'warning'
    })
    await labelStore.deleteEntityType(row.id)
    ElMessage.success('删除成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  labelStore.fetchEntityTypes({ include_inactive: true, include_unreviewed: true })
})
</script>
⋮----
<style scoped>
.entity-type-config {
  padding: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
````

## File: frontend/src/components/label/LabelImportExport.vue
````vue
<template>
  <el-dialog
    v-model="dialogVisible"
    :title="mode === 'import' ? '导入标签配置' : '导出标签配置'"
    width="600px"
  >
    <div v-if="mode === 'import'">
      <el-upload
        drag
        :auto-upload="false"
        :on-change="handleFileChange"
        :limit="1"
        accept=".json"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            只能上传JSON格式的配置文件
          </div>
        </template>
      </el-upload>

      <el-alert
        v-if="previewData"
        title="预览"
        type="info"
        :closable="false"
        style="margin-top: 20px;"
      >
        <div>实体类型: {{ previewData.entity_types?.length || 0 }} 个</div>
        <div>关系类型: {{ previewData.relation_types?.length || 0 }} 个</div>
      </el-alert>
    </div>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button
        v-if="mode === 'import'"
        type="primary"
        @click="handleImport"
        :disabled="!previewData"
        :loading="loading"
      >
        导入
      </el-button>
    </template>
  </el-dialog>
</template>
⋮----
<template #tip>
          <div class="el-upload__tip">
            只能上传JSON格式的配置文件
          </div>
        </template>
⋮----
<div>实体类型: {{ previewData.entity_types?.length || 0 }} 个</div>
<div>关系类型: {{ previewData.relation_types?.length || 0 }} 个</div>
⋮----
<template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button
        v-if="mode === 'import'"
        type="primary"
        @click="handleImport"
        :disabled="!previewData"
        :loading="loading"
      >
        导入
      </el-button>
    </template>
⋮----
<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { useLabelStore } from '@/stores/label'
import type { UploadFile } from 'element-plus'

interface Props {
  visible: boolean
  mode: 'import' | 'export'
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
  'success': []
}>()

const labelStore = useLabelStore()
const loading = ref(false)
const previewData = ref<any>(null)

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const handleFileChange = (file: UploadFile) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const content = e.target?.result as string
      previewData.value = JSON.parse(content)
    } catch (error) {
      ElMessage.error('文件格式错误')
      previewData.value = null
    }
  }
  reader.readAsText(file.raw!)
}

const handleImport = async () => {
  if (!previewData.value) return
  
  loading.value = true
  try {
    await labelStore.importLabels(previewData.value)
    emit('success')
    dialogVisible.value = false
    previewData.value = null
  } catch (error) {
    ElMessage.error('导入失败')
  } finally {
    loading.value = false
  }
}
</script>
⋮----
<style scoped>
.el-icon--upload {
  font-size: 67px;
  color: #8c939d;
  margin: 40px 0 16px;
  line-height: 50px;
}
</style>
````

## File: frontend/src/components/label/PromptPreview.vue
````vue
<template>
  <el-dialog
    v-model="dialogVisible"
    title="Agent Prompt 预览"
    width="900px"
  >
    <div class="prompt-preview">
      <el-radio-group v-model="promptType" @change="handleTypeChange">
        <el-radio-button value="entity">实体抽取</el-radio-button>
        <el-radio-button value="relation">关系抽取</el-radio-button>
        <el-radio-button value="image">图片标注</el-radio-button>
      </el-radio-group>

      <div class="prompt-content" v-loading="loading">
        <pre v-if="promptContent">{{ promptContent }}</pre>
        <el-empty v-else description="暂无内容" />
      </div>

      <div class="prompt-actions">
        <el-button @click="handleCopy">复制</el-button>
        <el-button type="primary" @click="handleRefresh">刷新</el-button>
      </div>
    </div>
  </el-dialog>
</template>
⋮----
<pre v-if="promptContent">{{ promptContent }}</pre>
⋮----
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '@/stores/label'

interface Props {
  visible: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const labelStore = useLabelStore()
const promptType = ref<'entity' | 'relation' | 'image'>('entity')
const promptContent = ref('')
const loading = ref(false)

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const loadPrompt = async () => {
  loading.value = true
  try {
    promptContent.value = await labelStore.previewPrompt(promptType.value)
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleTypeChange = () => {
  loadPrompt()
}

const handleRefresh = () => {
  loadPrompt()
}

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(promptContent.value)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

watch(() => props.visible, (visible) => {
  if (visible) {
    loadPrompt()
  }
})
</script>
⋮----
<style scoped>
.prompt-preview {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.prompt-content {
  min-height: 400px;
  max-height: 600px;
  overflow-y: auto;
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 16px;
}

.prompt-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
````

## File: frontend/src/components/label/RelationTypeConfig.vue
````vue
<template>
  <div class="relation-type-config">
    <div class="toolbar">
      <el-button type="primary" @click="handleCreate">新建关系类型</el-button>
      <el-space>
        <el-checkbox v-model="showInactive">显示已停用</el-checkbox>
        <el-checkbox v-model="showUnreviewed">显示未审核</el-checkbox>
      </el-space>
    </div>

    <el-table :data="filteredRelationTypes" v-loading="labelStore.loading">
      <el-table-column prop="type_name" label="类型名称" width="150" />
      <el-table-column prop="type_name_zh" label="中文名称" width="150" />
      <el-table-column label="颜色" width="100">
        <template #default="{ row }">
          <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
            {{ row.type_name_zh }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="审核状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_reviewed ? 'success' : 'warning'" size="small">
            {{ row.is_reviewed ? '已审核' : '待审核' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
            {{ row.is_active ? '启用' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" @click="handleGenerateDefinition(row)">生成定义</el-button>
          <el-button size="small" @click="handleReview(row)" v-if="!row.is_reviewed">审核</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑关系类型' : '新建关系类型'"
      width="600px"
    >
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="类型名称" prop="type_name">
          <el-input v-model="formData.type_name" placeholder="英文名称，如 has_defect" />
        </el-form-item>
        <el-form-item label="中文名称" prop="type_name_zh">
          <el-input v-model="formData.type_name_zh" placeholder="中文名称，如 存在缺陷" />
        </el-form-item>
        <el-form-item label="颜色" prop="color">
          <el-color-picker v-model="formData.color" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="启用状态" v-if="isEdit">
          <el-switch v-model="formData.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 审核对话框 -->
    <DefinitionReview
      v-model:visible="reviewDialogVisible"
      :relation-type="currentRelationType"
      @success="handleReviewSuccess"
    />
  </div>
</template>
⋮----
<template #default="{ row }">
          <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
            {{ row.type_name_zh }}
          </el-tag>
        </template>
⋮----
{{ row.type_name_zh }}
⋮----
<template #default="{ row }">
          <el-tag :type="row.is_reviewed ? 'success' : 'warning'" size="small">
            {{ row.is_reviewed ? '已审核' : '待审核' }}
          </el-tag>
        </template>
⋮----
{{ row.is_reviewed ? '已审核' : '待审核' }}
⋮----
<template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
            {{ row.is_active ? '启用' : '停用' }}
          </el-tag>
        </template>
⋮----
{{ row.is_active ? '启用' : '停用' }}
⋮----
<template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" @click="handleGenerateDefinition(row)">生成定义</el-button>
          <el-button size="small" @click="handleReview(row)" v-if="!row.is_reviewed">审核</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
⋮----
<!-- 创建/编辑对话框 -->
⋮----
<template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
⋮----
<!-- 审核对话框 -->
⋮----
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import type { RelationType } from '@/api/label'
import DefinitionReview from './DefinitionReview.vue'

const labelStore = useLabelStore()
const showInactive = ref(false)
const showUnreviewed = ref(true)  // 默认显示未审核的标签（包括默认配置）
const dialogVisible = ref(false)
const reviewDialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const currentRelationType = ref<RelationType | null>(null)

const formData = ref({
  type_name: '',
  type_name_zh: '',
  color: '#67C23A',
  description: '',
  is_active: true
})

const rules: FormRules = {
  type_name: [{ required: true, message: '请输入类型名称', trigger: 'blur' }],
  type_name_zh: [{ required: true, message: '请输入中文名称', trigger: 'blur' }],
  color: [{ required: true, message: '请选择颜色', trigger: 'change' }]
}

const filteredRelationTypes = computed(() => {
  return labelStore.relationTypes.filter(rt => {
    if (!showInactive.value && !rt.is_active) return false
    if (!showUnreviewed.value && !rt.is_reviewed) return false
    return true
  })
})

const handleCreate = () => {
  isEdit.value = false
  formData.value = {
    type_name: '',
    type_name_zh: '',
    color: '#67C23A',
    description: '',
    is_active: true
  }
  dialogVisible.value = true
}

const handleEdit = (row: RelationType) => {
  isEdit.value = true
  formData.value = {
    type_name: row.type_name,
    type_name_zh: row.type_name_zh,
    color: row.color,
    description: row.description || '',
    is_active: row.is_active
  }
  currentRelationType.value = row
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      if (isEdit.value && currentRelationType.value) {
        await labelStore.updateRelationType(currentRelationType.value.id, formData.value)
        ElMessage.success('更新成功')
      } else {
        await labelStore.createRelationType(formData.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    }
  })
}

const handleGenerateDefinition = async (row: RelationType) => {
  try {
    await ElMessageBox.confirm('确定要使用LLM生成该关系类型的定义吗？', '提示', {
      type: 'warning'
    })
    await labelStore.generateRelationDefinition(row.id)
    ElMessage.success('定义生成成功，请审核')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('生成失败')
    }
  }
}

const handleReview = (row: RelationType) => {
  currentRelationType.value = row
  reviewDialogVisible.value = true
}

const handleReviewSuccess = () => {
  ElMessage.success('审核成功')
  labelStore.fetchRelationTypes()
}

const handleDelete = async (row: RelationType) => {
  try {
    await ElMessageBox.confirm('确定要删除该关系类型吗？', '警告', {
      type: 'warning'
    })
    await labelStore.deleteRelationType(row.id)
    ElMessage.success('删除成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  labelStore.fetchRelationTypes({ include_inactive: true, include_unreviewed: true })
})
</script>
⋮----
<style scoped>
.relation-type-config {
  padding: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
````

## File: frontend/src/components/label/VersionCompare.vue
````vue
<template>
  <el-dialog
    v-model="dialogVisible"
    title="版本比较"
    width="1200px"
  >
    <div v-if="version1 && version2" class="version-compare">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="版本1">{{ version1.version_name }}</el-descriptions-item>
        <el-descriptions-item label="版本2">{{ version2.version_name }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ version1.created_at }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ version2.created_at }}</el-descriptions-item>
      </el-descriptions>

      <div v-if="compareResult" class="compare-result">
        <el-divider>实体类型变更</el-divider>
        
        <el-collapse v-model="activeNames">
          <el-collapse-item title="新增实体类型" name="added-entities" v-if="compareResult.added_entities.length > 0">
            <el-table :data="compareResult.added_entities">
              <el-table-column prop="type_name" label="类型名称" width="150" />
              <el-table-column prop="type_name_zh" label="中文名称" width="150" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
            </el-table>
          </el-collapse-item>

          <el-collapse-item title="删除实体类型" name="removed-entities" v-if="compareResult.removed_entities.length > 0">
            <el-table :data="compareResult.removed_entities">
              <el-table-column prop="type_name" label="类型名称" width="150" />
              <el-table-column prop="type_name_zh" label="中文名称" width="150" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
            </el-table>
          </el-collapse-item>

          <el-collapse-item title="修改实体类型" name="modified-entities" v-if="compareResult.modified_entities.length > 0">
            <el-table :data="compareResult.modified_entities">
              <el-table-column prop="old.type_name" label="类型名称" width="150" />
              <el-table-column label="变更内容">
                <template #default="{ row }">
                  <div class="diff-content">
                    <div v-if="row.old.type_name_zh !== row.new.type_name_zh">
                      <span class="diff-label">中文名称:</span>
                      <span class="diff-old">{{ row.old.type_name_zh }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.type_name_zh }}</span>
                    </div>
                    <div v-if="row.old.color !== row.new.color">
                      <span class="diff-label">颜色:</span>
                      <el-tag :color="row.old.color" :style="{ backgroundColor: row.old.color, color: '#fff' }">旧</el-tag>
                      <span class="diff-arrow">→</span>
                      <el-tag :color="row.new.color" :style="{ backgroundColor: row.new.color, color: '#fff' }">新</el-tag>
                    </div>
                    <div v-if="row.old.description !== row.new.description">
                      <span class="diff-label">描述:</span>
                      <span class="diff-old">{{ row.old.description }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.description }}</span>
                    </div>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-collapse-item>
        </el-collapse>

        <el-divider>关系类型变更</el-divider>
        
        <el-collapse v-model="activeNames">
          <el-collapse-item title="新增关系类型" name="added-relations" v-if="compareResult.added_relations.length > 0">
            <el-table :data="compareResult.added_relations">
              <el-table-column prop="type_name" label="类型名称" width="150" />
              <el-table-column prop="type_name_zh" label="中文名称" width="150" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
            </el-table>
          </el-collapse-item>

          <el-collapse-item title="删除关系类型" name="removed-relations" v-if="compareResult.removed_relations.length > 0">
            <el-table :data="compareResult.removed_relations">
              <el-table-column prop="type_name" label="类型名称" width="150" />
              <el-table-column prop="type_name_zh" label="中文名称" width="150" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
            </el-table>
          </el-collapse-item>

          <el-collapse-item title="修改关系类型" name="modified-relations" v-if="compareResult.modified_relations.length > 0">
            <el-table :data="compareResult.modified_relations">
              <el-table-column prop="old.type_name" label="类型名称" width="150" />
              <el-table-column label="变更内容">
                <template #default="{ row }">
                  <div class="diff-content">
                    <div v-if="row.old.type_name_zh !== row.new.type_name_zh">
                      <span class="diff-label">中文名称:</span>
                      <span class="diff-old">{{ row.old.type_name_zh }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.type_name_zh }}</span>
                    </div>
                    <div v-if="row.old.color !== row.new.color">
                      <span class="diff-label">颜色:</span>
                      <el-tag :color="row.old.color" :style="{ backgroundColor: row.old.color, color: '#fff' }">旧</el-tag>
                      <span class="diff-arrow">→</span>
                      <el-tag :color="row.new.color" :style="{ backgroundColor: row.new.color, color: '#fff' }">新</el-tag>
                    </div>
                    <div v-if="row.old.description !== row.new.description">
                      <span class="diff-label">描述:</span>
                      <span class="diff-old">{{ row.old.description }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.description }}</span>
                    </div>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-collapse-item>
        </el-collapse>
      </div>

      <el-empty v-else description="暂无差异" />
    </div>
  </el-dialog>
</template>
⋮----
<el-descriptions-item label="版本1">{{ version1.version_name }}</el-descriptions-item>
<el-descriptions-item label="版本2">{{ version2.version_name }}</el-descriptions-item>
<el-descriptions-item label="创建时间">{{ version1.created_at }}</el-descriptions-item>
<el-descriptions-item label="创建时间">{{ version2.created_at }}</el-descriptions-item>
⋮----
<template #default="{ row }">
                  <div class="diff-content">
                    <div v-if="row.old.type_name_zh !== row.new.type_name_zh">
                      <span class="diff-label">中文名称:</span>
                      <span class="diff-old">{{ row.old.type_name_zh }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.type_name_zh }}</span>
                    </div>
                    <div v-if="row.old.color !== row.new.color">
                      <span class="diff-label">颜色:</span>
                      <el-tag :color="row.old.color" :style="{ backgroundColor: row.old.color, color: '#fff' }">旧</el-tag>
                      <span class="diff-arrow">→</span>
                      <el-tag :color="row.new.color" :style="{ backgroundColor: row.new.color, color: '#fff' }">新</el-tag>
                    </div>
                    <div v-if="row.old.description !== row.new.description">
                      <span class="diff-label">描述:</span>
                      <span class="diff-old">{{ row.old.description }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.description }}</span>
                    </div>
                  </div>
                </template>
⋮----
<span class="diff-old">{{ row.old.type_name_zh }}</span>
⋮----
<span class="diff-new">{{ row.new.type_name_zh }}</span>
⋮----
<span class="diff-old">{{ row.old.description }}</span>
⋮----
<span class="diff-new">{{ row.new.description }}</span>
⋮----
<template #default="{ row }">
                  <div class="diff-content">
                    <div v-if="row.old.type_name_zh !== row.new.type_name_zh">
                      <span class="diff-label">中文名称:</span>
                      <span class="diff-old">{{ row.old.type_name_zh }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.type_name_zh }}</span>
                    </div>
                    <div v-if="row.old.color !== row.new.color">
                      <span class="diff-label">颜色:</span>
                      <el-tag :color="row.old.color" :style="{ backgroundColor: row.old.color, color: '#fff' }">旧</el-tag>
                      <span class="diff-arrow">→</span>
                      <el-tag :color="row.new.color" :style="{ backgroundColor: row.new.color, color: '#fff' }">新</el-tag>
                    </div>
                    <div v-if="row.old.description !== row.new.description">
                      <span class="diff-label">描述:</span>
                      <span class="diff-old">{{ row.old.description }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.description }}</span>
                    </div>
                  </div>
                </template>
⋮----
<span class="diff-old">{{ row.old.type_name_zh }}</span>
⋮----
<span class="diff-new">{{ row.new.type_name_zh }}</span>
⋮----
<span class="diff-old">{{ row.old.description }}</span>
⋮----
<span class="diff-new">{{ row.new.description }}</span>
⋮----
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import type { LabelSchemaVersion } from '@/api/label'

interface Props {
  visible: boolean
  version1?: LabelSchemaVersion
  version2?: LabelSchemaVersion
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const labelStore = useLabelStore()
const activeNames = ref(['added-entities', 'removed-entities', 'modified-entities', 'added-relations', 'removed-relations', 'modified-relations'])
const compareResult = ref<any>(null)

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

watch(() => props.visible, async (visible) => {
  if (visible && props.version1 && props.version2) {
    try {
      compareResult.value = await labelStore.compareVersions(
        props.version1.version_id,
        props.version2.version_id
      )
    } catch (error) {
      ElMessage.error('比较失败')
    }
  }
})
</script>
⋮----
<style scoped>
.version-compare {
  padding: 20px 0;
}

.compare-result {
  margin-top: 20px;
}

.diff-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.diff-label {
  font-weight: 500;
  margin-right: 8px;
}

.diff-old {
  color: #f56c6c;
  text-decoration: line-through;
}

.diff-new {
  color: #67c23a;
  font-weight: 500;
}

.diff-arrow {
  margin: 0 8px;
  color: #909399;
}
</style>
````

## File: frontend/src/components/label/VersionManager.vue
````vue
<template>
  <div class="version-manager">
    <div class="toolbar">
      <el-button type="primary" @click="handleCreateSnapshot">创建版本快照</el-button>
      <el-button @click="handleCompare" :disabled="selectedVersions.length !== 2">
        比较版本
      </el-button>
    </div>

    <el-table
      :data="labelStore.versions"
      v-loading="labelStore.loading"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" :selectable="row => !row.is_active" />
      <el-table-column prop="version_name" label="版本名称" width="200">
        <template #default="{ row }">
          {{ row.version_name }}
          <el-tag v-if="isDefaultVersion(row)" type="warning" size="small" style="margin-left: 8px;">
            默认
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="version_id" label="版本ID" width="150" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="实体类型数" width="120">
        <template #default="{ row }">
          {{ row.entity_types?.length || 0 }}
        </template>
      </el-table-column>
      <el-table-column label="关系类型数" width="120">
        <template #default="{ row }">
          {{ row.relation_types?.length || 0 }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
            {{ row.is_active ? '当前版本' : '历史版本' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button
            size="small"
            @click="handleViewDetail(row)"
          >
            查看详情
          </el-button>
          <el-button
            size="small"
            type="primary"
            @click="handleActivate(row)"
            v-if="!row.is_active"
          >
            激活
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建快照对话框 -->
    <VersionSnapshotDialog
      v-model:visible="snapshotDialogVisible"
      @success="handleSnapshotSuccess"
    />

    <!-- 版本比较对话框 -->
    <VersionCompare
      v-model:visible="compareDialogVisible"
      :version1="selectedVersions[0]"
      :version2="selectedVersions[1]"
    />

    <!-- 版本详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="版本详情"
      width="900px"
    >
      <div v-if="currentVersion">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="版本名称">
            {{ currentVersion.version_name }}
            <el-tag v-if="isDefaultVersion(currentVersion)" type="warning" size="small" style="margin-left: 8px;">
              默认版本（只读）
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="版本ID">{{ currentVersion.version_id }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ currentVersion.description }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentVersion.created_at }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentVersion.is_active ? 'success' : 'info'">
              {{ currentVersion.is_active ? '当前版本' : '历史版本' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider>实体类型 ({{ currentVersion.entity_types?.length || 0 }})</el-divider>
        <el-table :data="currentVersion.entity_types" max-height="300">
          <el-table-column prop="type_name" label="类型名称" width="150" />
          <el-table-column prop="type_name_zh" label="中文名称" width="150" />
          <el-table-column label="颜色" width="100">
            <template #default="{ row }">
              <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
                {{ row.type_name_zh }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" show-overflow-tooltip />
        </el-table>

        <el-divider>关系类型 ({{ currentVersion.relation_types?.length || 0 }})</el-divider>
        <el-table :data="currentVersion.relation_types" max-height="300">
          <el-table-column prop="type_name" label="类型名称" width="150" />
          <el-table-column prop="type_name_zh" label="中文名称" width="150" />
          <el-table-column label="颜色" width="100">
            <template #default="{ row }">
              <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
                {{ row.type_name_zh }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" show-overflow-tooltip />
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>
⋮----
<template #default="{ row }">
          {{ row.version_name }}
          <el-tag v-if="isDefaultVersion(row)" type="warning" size="small" style="margin-left: 8px;">
            默认
          </el-tag>
        </template>
⋮----
{{ row.version_name }}
⋮----
<template #default="{ row }">
          {{ row.entity_types?.length || 0 }}
        </template>
⋮----
{{ row.entity_types?.length || 0 }}
⋮----
<template #default="{ row }">
          {{ row.relation_types?.length || 0 }}
        </template>
⋮----
{{ row.relation_types?.length || 0 }}
⋮----
<template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
            {{ row.is_active ? '当前版本' : '历史版本' }}
          </el-tag>
        </template>
⋮----
{{ row.is_active ? '当前版本' : '历史版本' }}
⋮----
<template #default="{ row }">
          <el-button
            size="small"
            @click="handleViewDetail(row)"
          >
            查看详情
          </el-button>
          <el-button
            size="small"
            type="primary"
            @click="handleActivate(row)"
            v-if="!row.is_active"
          >
            激活
          </el-button>
        </template>
⋮----
<!-- 创建快照对话框 -->
⋮----
<!-- 版本比较对话框 -->
⋮----
<!-- 版本详情对话框 -->
⋮----
{{ currentVersion.version_name }}
⋮----
<el-descriptions-item label="版本ID">{{ currentVersion.version_id }}</el-descriptions-item>
<el-descriptions-item label="描述" :span="2">{{ currentVersion.description }}</el-descriptions-item>
<el-descriptions-item label="创建时间">{{ currentVersion.created_at }}</el-descriptions-item>
⋮----
{{ currentVersion.is_active ? '当前版本' : '历史版本' }}
⋮----
<el-divider>实体类型 ({{ currentVersion.entity_types?.length || 0 }})</el-divider>
⋮----
<template #default="{ row }">
              <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
                {{ row.type_name_zh }}
              </el-tag>
            </template>
⋮----
{{ row.type_name_zh }}
⋮----
<el-divider>关系类型 ({{ currentVersion.relation_types?.length || 0 }})</el-divider>
⋮----
<template #default="{ row }">
              <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
                {{ row.type_name_zh }}
              </el-tag>
            </template>
⋮----
{{ row.type_name_zh }}
⋮----
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import type { LabelSchemaVersion } from '@/api/label'
import VersionSnapshotDialog from './VersionSnapshotDialog.vue'
import VersionCompare from './VersionCompare.vue'

const labelStore = useLabelStore()
const snapshotDialogVisible = ref(false)
const compareDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const selectedVersions = ref<LabelSchemaVersion[]>([])
const currentVersion = ref<LabelSchemaVersion | null>(null)

// 判断是否为默认版本
const isDefaultVersion = (version: LabelSchemaVersion) => {
  return version.version_id === 'DEFAULT_V1.0'
}

const handleCreateSnapshot = () => {
  snapshotDialogVisible.value = true
}

const handleSnapshotSuccess = () => {
  ElMessage.success('版本快照创建成功')
  labelStore.fetchVersions()
}

const handleSelectionChange = (selection: LabelSchemaVersion[]) => {
  selectedVersions.value = selection
}

const handleCompare = () => {
  if (selectedVersions.value.length === 2) {
    compareDialogVisible.value = true
  }
}

const handleViewDetail = (row: LabelSchemaVersion) => {
  currentVersion.value = row
  detailDialogVisible.value = true
}

const handleActivate = async (row: LabelSchemaVersion) => {
  try {
    const message = isDefaultVersion(row)
      ? `确定要切换回默认配置吗？这将恢复系统默认的16种实体类型和1种关系类型。`
      : `确定要激活版本 "${row.version_name}" 吗？这将替换当前的标签体系配置。`
    
    await ElMessageBox.confirm(
      message,
      '警告',
      { type: 'warning' }
    )
    await labelStore.activateVersion(row.version_id)
    ElMessage.success('版本激活成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('激活失败')
    }
  }
}

onMounted(() => {
  labelStore.fetchVersions()
})
</script>
⋮----
<style scoped>
.version-manager {
  padding: 20px;
}

.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
</style>
````

## File: frontend/src/components/label/VersionSnapshotDialog.vue
````vue
<template>
  <el-dialog
    v-model="dialogVisible"
    title="创建版本快照"
    width="600px"
  >
    <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
      <el-form-item label="版本名称" prop="version_name">
        <el-input v-model="formData.version_name" placeholder="如: v1.0.0" />
      </el-form-item>
      <el-form-item label="版本描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请描述此版本的主要变更"
        />
      </el-form-item>
      <el-alert
        title="提示"
        type="info"
        :closable="false"
        style="margin-bottom: 20px;"
      >
        创建快照将保存当前所有实体类型和关系类型的配置，包括定义、示例等信息。
      </el-alert>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="loading">创建</el-button>
    </template>
  </el-dialog>
</template>
⋮----
<template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="loading">创建</el-button>
    </template>
⋮----
<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import { useUserStore } from '@/stores/user'

interface Props {
  visible: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
  'success': []
}>()

const labelStore = useLabelStore()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const formData = ref({
  version_name: '',
  description: ''
})

const rules: FormRules = {
  version_name: [{ required: true, message: '请输入版本名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入版本描述', trigger: 'blur' }]
}

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      await labelStore.createSnapshot({
        version_name: formData.value.version_name,
        description: formData.value.description,
        created_by: userStore.currentUser?.id || 1
      })
      emit('success')
      dialogVisible.value = false
      formData.value = {
        version_name: '',
        description: ''
      }
    } catch (error) {
      ElMessage.error('创建失败')
    } finally {
      loading.value = false
    }
  })
}
</script>
````

## File: frontend/src/composables/useRelationCreation.ts
````typescript
/**
 * 关系创建Composable
 * 提供关系创建的交互逻辑（点击两个实体创建关系）
 */
⋮----
import { ref } from 'vue'
⋮----
export interface RelationCreationState {
  isActive: boolean
  sourceEntityId: number | null
  targetEntityId: number | null
  step: 'idle' | 'selecting-source' | 'selecting-target'
}
⋮----
export function useRelationCreation()
⋮----
/**
   * 开始创建关系
   */
const startCreation = () =>
⋮----
/**
   * 选择实体
   * @param entityId 实体ID
   * @returns 是否完成选择（选择了两个实体）
   */
const selectEntity = (entityId: number): boolean =>
⋮----
// 选择源实体
⋮----
// 选择目标实体
⋮----
// 不能选择同一个实体
⋮----
return true // 完成选择
⋮----
/**
   * 取消创建
   */
const cancelCreation = () =>
⋮----
/**
   * 重置状态（创建完成后）
   */
const reset = () =>
⋮----
/**
   * 获取当前选择的实体ID
   */
const getSelectedEntities = () =>
⋮----
/**
   * 判断实体是否被选中
   */
const isEntitySelected = (entityId: number): 'source' | 'target' | null =>
⋮----
/**
   * 获取提示信息
   */
const getHintMessage = (): string =>
````

## File: frontend/src/composables/useTextSelection.ts
````typescript
/**
 * 文本选择Composable
 * 提供增强的文本选择功能，包括偏移量计算和验证
 */
⋮----
export interface TextSelection {
  start: number
  end: number
  text: string
}
⋮----
export function useTextSelection()
⋮----
/**
   * 获取当前文本选择
   * @param container 文本容器元素
   * @returns 选择的文本范围和内容
   */
const getSelection = (container: HTMLElement | undefined): TextSelection | null =>
⋮----
// 确保选择在容器内
⋮----
// 计算偏移量
⋮----
// 允许 start === end 的情况（光标位置），但检查选择的文本
⋮----
/**
   * 计算节点在容器中的偏移量
   * @param container 容器元素
   * @param node 目标节点
   * @param offset 节点内偏移量
   * @returns 在容器中的绝对偏移量
   */
const getOffsetInContainer = (
    container: HTMLElement,
    node: Node,
    offset: number
): number =>
⋮----
// 如果是span元素，检查data-offset属性
⋮----
/**
   * 验证偏移量是否有效
   * @param text 原始文本
   * @param start 起始偏移量
   * @param end 结束偏移量
   * @returns 是否有效
   */
const validateOffset = (text: string, start: number, end: number): boolean =>
⋮----
/**
   * 修正偏移量（如果文本略有变化）
   * @param text 原始文本
   * @param entityText 实体文本
   * @param start 起始偏移量
   * @param end 结束偏移量
   * @returns 修正后的偏移量，如果无法修正则返回null
   */
const correctOffset = (
    text: string,
    entityText: string,
    start: number,
    end: number
):
⋮----
// 首先验证原始偏移量
⋮----
// 尝试在附近查找匹配
const searchRange = 50 // 搜索范围
⋮----
// 无法修正
⋮----
/**
   * 计算两个文本范围是否重叠
   * @param range1 范围1
   * @param range2 范围2
   * @returns 是否重叠
   */
const hasOverlap = (
    range1: { start: number; end: number },
    range2: { start: number; end: number }
): boolean =>
⋮----
/**
   * 高亮显示文本范围
   * @param container 容器元素
   * @param start 起始偏移量
   * @param end 结束偏移量
   */
const highlightRange = (container: HTMLElement, start: number, end: number) =>
⋮----
/**
   * 清除所有高亮
   * @param container 容器元素
   */
const clearHighlight = (container: HTMLElement) =>
````

## File: frontend/src/constants/taskStatus.ts
````typescript
/**
 * 任务状态常量和工具函数
 * 统一管理任务状态的显示和颜色
 */
⋮----
// 任务状态枚举
export enum TaskStatus {
  PENDING = 'pending',           // 待处理
  PROCESSING = 'processing',     // 处理中
  COMPLETED = 'completed',       // 已完成
  UNDER_REVIEW = 'under_review', // 待复核
  APPROVED = 'approved',         // 已批准
  REJECTED = 'rejected',         // 已驳回
  FAILED = 'failed'              // 失败
}
⋮----
PENDING = 'pending',           // 待处理
PROCESSING = 'processing',     // 处理中
COMPLETED = 'completed',       // 已完成
UNDER_REVIEW = 'under_review', // 待复核
APPROVED = 'approved',         // 已批准
REJECTED = 'rejected',         // 已驳回
FAILED = 'failed'              // 失败
⋮----
// 状态显示文本映射
⋮----
// 状态标签类型映射（Element Plus Tag 类型）
⋮----
// 状态选项（用于下拉框）
⋮----
/**
 * 获取状态显示文本
 * @param status 状态值
 * @returns 显示文本
 */
export function getStatusText(status: string): string
⋮----
/**
 * 获取状态标签类型
 * @param status 状态值
 * @returns Element Plus Tag 类型
 */
export function getStatusType(status: string): string
⋮----
/**
 * 检查状态是否为最终状态（不可再编辑）
 * @param status 状态值
 * @returns 是否为最终状态
 */
export function isFinalStatus(status: string): boolean
⋮----
/**
 * 检查状态是否可以提交复核
 * @param status 状态值
 * @returns 是否可以提交复核
 */
export function canSubmitForReview(status: string): boolean
⋮----
/**
 * 检查状态是否可以编辑
 * @param status 状态值
 * @returns 是否可以编辑
 */
export function canEdit(status: string): boolean
````

## File: frontend/src/layouts/MainLayout.vue
````vue
<template>
  <el-container class="main-layout">
    <el-header class="header">
      <div class="header-left">
        <router-link to="/" class="title-link">
          <h1 class="title">{{ appTitle }}</h1>
          <span class="subtitle">本系统重点面向KF、QMS和品质失效案例及视频数据的多模态标注工作。</span>
        </router-link>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon>
            <span>{{ authStore.user?.username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-container>
      <el-aside width="240px" class="aside">
        <el-menu
          :default-active="activeMenu"
          router
          class="menu"
        >
          <el-sub-menu index="/source-management">
            <template #title>
              <el-icon><FolderOpened /></el-icon>
              <span>数据源管理</span>
            </template>
            <el-menu-item index="/document/import">表格数据导入</el-menu-item>
            <el-menu-item index="/document/data-list">数据列表</el-menu-item>
            <el-menu-item index="/document/statistics">数据分析</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/annotation-management">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>实体关系标注</span>
            </template>
            <el-menu-item
              v-if="authStore.user?.role !== 'viewer'"
              index="/corpus"
            >
              标注原始语料管理
            </el-menu-item>
            <el-menu-item
              v-if="['admin', 'viewer'].includes(authStore.user?.role)"
              index="/datasets"
            >
              数据集管理
            </el-menu-item>
            <el-menu-item
              v-if="authStore.user?.role !== 'viewer'"
              index="/labels"
            >
              实体关系标签配置
            </el-menu-item>
            <el-menu-item
              v-if="authStore.user?.role !== 'viewer'"
              index="/annotations"
            >
              实体关系标注任务
            </el-menu-item>
            <el-menu-item
              v-if="['admin', 'annotator'].includes(authStore.user?.role)"
              index="/review"
            >
              标注复核管理
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/multimodal-convert">
            <template #title>
              <el-icon><Share /></el-icon>
              <span>多模态格式转换</span>
            </template>
            <el-menu-item index="/multimodal/export">多模态语料导出</el-menu-item>
          </el-sub-menu>

          <el-menu-item
            v-if="authStore.user?.role === 'admin'"
            index="/users"
          >
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>
⋮----
<h1 class="title">{{ appTitle }}</h1>
⋮----
<span>{{ authStore.user?.username }}</span>
⋮----
<template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
⋮----
<template #title>
              <el-icon><FolderOpened /></el-icon>
              <span>数据源管理</span>
            </template>
⋮----
<template #title>
              <el-icon><Document /></el-icon>
              <span>实体关系标注</span>
            </template>
⋮----
<template #title>
              <el-icon><Share /></el-icon>
              <span>多模态格式转换</span>
            </template>
⋮----
<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  User,
  Document,
  FolderOpened,
  Share
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const appTitle = import.meta.env.VITE_APP_TITLE || '面向离散型电子信息制造业的多模态语料库构建平台'

const activeMenu = computed(() => route.path)

const handleCommand = (command: string) => {
  if (command === 'logout') {
    authStore.logout()
    router.push('/login')
  }
}
</script>
⋮----
<style scoped>
.main-layout {
  height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #409eff;
  color: white;
  padding: 0 20px;
}

.header-left .title {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.header-left .subtitle {
  font-size: 11px;
  font-weight: normal;
  margin-left: 12px;
  opacity: 0.85;
}

.title-link {
  text-decoration: none;
  color: inherit;
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e4e7ed;
}

.menu {
  border-right: none;
  height: 100%;
}

.main {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>
````

## File: frontend/src/main.ts
````typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
⋮----
import App from './App.vue'
import router from './router'
````

## File: frontend/src/router/index.ts
````typescript
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
⋮----
// 登录页面
⋮----
// 主布局
⋮----
// 首页/Dashboard
⋮----
// 语料管理（浏览员不可访问）
⋮----
// 数据集管理（所有角色可访问）
⋮----
// Task 47: 我的数据集（必须在 :id 之前！）
⋮----
// Task 47: 数据集分配管理
⋮----
// 标签配置（浏览员不可访问）
⋮----
// 标注任务（浏览员不可访问）
⋮----
// 复核管理（管理员和标注员可访问）
⋮----
// 用户管理（管理员）
⋮----
// 文档管理
⋮----
// 多模态格式转换
⋮----
// 404页面
⋮----
// 路由守卫
⋮----
// 检查是否需要认证
⋮----
// 未登录，跳转到登录页
⋮----
// 检查是否需要管理员权限
⋮----
// 权限不足
⋮----
// 检查是否需要特定角色
⋮----
// 角色不匹配
⋮----
// 已登录用户访问登录页，跳转到首页
````

## File: frontend/src/stores/annotation.ts
````typescript
/**
 * 标注任务Store
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { annotationApi } from '@/api'
import type { AnnotationTask, TextEntity, BatchJobProgress } from '@/types'
⋮----
// State
⋮----
// Getters
⋮----
// Actions - 任务管理
const fetchTask = async (taskId: string) =>
⋮----
const updateTask = async (taskId: string, data: {
    status?: string
    assigned_to?: number
}) =>
⋮----
// Actions - 批量标注
const startBatchAnnotation = async (data: {
    dataset_id: string
    annotation_type: 'automatic' | 'manual'
    assigned_to: number
}) =>
⋮----
// 初始化批量任务状态
⋮----
const fetchBatchStatus = async (jobId: string) =>
⋮----
const pollBatchStatus = (jobId: string, interval = 2000): NodeJS.Timeout =>
⋮----
// Actions - 实体管理
const addEntity = async (taskId: string, data: {
    token: string
    label: string
    start_offset: number
    end_offset: number
}) =>
⋮----
const updateEntity = async (taskId: string, entityId: number, data: {
    token?: string
    label?: string
    start_offset?: number
    end_offset?: number
}) =>
⋮----
const deleteEntity = async (taskId: string, entityId: number) =>
⋮----
// 同时删除相关的关系
⋮----
// Actions - 关系管理
const addRelation = async (taskId: string, data: {
    from_entity_id: number
    to_entity_id: number
    relation_type: string
}) =>
⋮----
const updateRelation = async (taskId: string, relationId: number, data: {
    from_entity_id?: number
    to_entity_id?: number
    relation_type?: string
}) =>
⋮----
const deleteRelation = async (taskId: string, relationId: number) =>
⋮----
const reset = () =>
⋮----
// State
⋮----
// Getters
⋮----
// Actions - 任务管理
⋮----
// Actions - 批量标注
⋮----
// Actions - 实体管理
⋮----
// Actions - 关系管理
⋮----
// 工具方法
````

## File: frontend/src/stores/auth.ts
````typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginRequest } from '@/types'
import { authApi } from '@/api/auth'
⋮----
// State
⋮----
// Getters
⋮----
// Actions
const login = async (username: string, password: string) =>
⋮----
// 保存到localStorage
⋮----
const logout = () =>
⋮----
// 清除localStorage
⋮----
const loadUserFromStorage = () =>
⋮----
const getAuthHeader = () =>
⋮----
// 初始化时加载用户信息
````

## File: frontend/src/stores/corpus.ts
````typescript
/**
 * 语料管理Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { corpusApi } from '@/api'
import type { Corpus, PaginatedResponse } from '@/types'
⋮----
// State
⋮----
// Actions
const fetchList = async (params?: {
    page?: number
    page_size?: number
    source_file?: string
    source_field?: string  // 修改为 source_field 以匹配后端
    has_images?: boolean
}) =>
⋮----
source_field?: string  // 修改为 source_field 以匹配后端
⋮----
const fetchDetail = async (id: number) =>
⋮----
const upload = async (file: File) =>
⋮----
// 上传成功后刷新列表
⋮----
const deleteCorpus = async (textId: string) =>
⋮----
// 删除成功后从列表中移除
⋮----
const reset = () =>
````

## File: frontend/src/stores/dataset.ts
````typescript
/**
 * 数据集管理Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { datasetApi } from '@/api'
import type { Dataset } from '@/types'
⋮----
// State
⋮----
// Actions
const fetchList = async (params?: {
    page?: number
    page_size?: number
    created_by?: number
}) =>
⋮----
// 后端返回格式: { success, message, data: { items, total } }
⋮----
const fetchDetail = async (id: string | number) =>
⋮----
// 后端返回格式: { success, message, data: {...} }
⋮----
const create = async (data: {
    name: string
    description?: string
    corpus_ids: number[]
    created_by: number
    label_schema_version_id?: number
}) =>
⋮----
// 创建成功后刷新列表
⋮----
const update = async (id: number, data: {
    name?: string
    description?: string
    label_schema_version_id?: number
}) =>
⋮----
// 更新列表中的数据
⋮----
const deleteDataset = async (datasetId: string) =>
⋮----
// 删除成功后从列表中移除
⋮----
const exportDataset = async (datasetId: string, params?: {
    output_path?: string
    status_filter?: string[]
}) =>
⋮----
const fetchDatasetTasks = async (
    datasetId: string,
    params?: {
      page?: number
      page_size?: number
      status?: string
    }
) =>
⋮----
const addTasksToDataset = async (datasetId: string, corpusIds: number[]) =>
⋮----
const removeTaskFromDataset = async (datasetId: string, taskId: string) =>
⋮----
const reset = () =>
````

## File: frontend/src/stores/document.ts
````typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { documentApi } from '@/api/document'
import type { TransferProgress } from '@/api/document'
import type { BatchExportParams, ProcessorInfo, ProcessedFile, StatisticsData } from '@/types'
⋮----
type TransferPhase = 'idle' | 'uploading' | 'processing' | 'downloading' | 'success' | 'exception'
⋮----
interface TransferState {
  percentage: number
  loaded: number
  total: number | null
  phase: TransferPhase
  message: string
}
⋮----
const createTransferState = (): TransferState => (
⋮----
const resetTransferState = (target: typeof excelUploadProgress) =>
⋮----
const updateTransferState = (
    target: typeof excelUploadProgress,
    progress: TransferProgress,
    phase: TransferPhase,
    message: string
) =>
⋮----
const fetchProcessors = async () =>
⋮----
const fetchProcessedFiles = async () =>
⋮----
const setCurrentProcessor = async (name: string) =>
⋮----
const handleUploadProgress = (target: typeof excelUploadProgress, progress: TransferProgress) =>
⋮----
const finalizeTransferSuccess = (target: typeof excelUploadProgress, message: string) =>
⋮----
const finalizeTransferError = (target: typeof excelUploadProgress, message: string) =>
⋮----
const uploadExcel = async (file: File) =>
⋮----
const uploadImagesZip = async (file: File, dataSource: string) =>
⋮----
const importJsonData = async (dataSource: string) =>
⋮----
const getStatistics = async (): Promise<StatisticsData | null> =>
⋮----
const exportEntityText = async (dataSources?: string[]) =>
⋮----
const exportClipAlignment = async (dataSources?: string[]) =>
⋮----
const exportQaAlignment = async (dataSources?: string[]) =>
⋮----
const batchExport = async (params: BatchExportParams) =>
⋮----
const resetExcelUploadProgress = () =>
⋮----
const resetImageUploadProgress = () =>
⋮----
const resetExportProgress = () =>
⋮----
const reset = () =>
````

## File: frontend/src/stores/index.ts
````typescript
/**
 * Store统一导出
 */
````

## File: frontend/src/stores/label.ts
````typescript
/**
 * 标签管理Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { labelApi, type EntityType, type RelationType, type LabelSchemaVersion } from '@/api/label'
⋮----
// State
⋮----
// Actions
const fetchEntityTypes = async (params?: {
    include_inactive?: boolean
    include_unreviewed?: boolean
}) =>
⋮----
const createEntityType = async (data: {
    type_name: string
    type_name_zh: string
    color: string
    description?: string
    supports_bbox?: boolean
}) =>
⋮----
// 刷新列表
⋮----
const updateEntityType = async (id: number, data: {
    type_name?: string
    type_name_zh?: string
    color?: string
    description?: string
    supports_bbox?: boolean
    is_active?: boolean
}) =>
⋮----
// 更新列表中的数据
⋮----
const deleteEntityType = async (id: number) =>
⋮----
// 从列表中移除
⋮----
const generateEntityDefinition = async (id: number) =>
⋮----
// 刷新列表
⋮----
const reviewEntityType = async (id: number, data: {
    approved: boolean
    definition?: string
    examples?: string[]
    disambiguation?: string
}) =>
⋮----
// 更新列表中的数据
⋮----
const fetchRelationTypes = async (params?: {
    include_inactive?: boolean
    include_unreviewed?: boolean
}) =>
⋮----
const createRelationType = async (data: {
    type_name: string
    type_name_zh: string
    color: string
    description?: string
}) =>
⋮----
// 刷新列表
⋮----
const updateRelationType = async (id: number, data: {
    type_name?: string
    type_name_zh?: string
    color?: string
    description?: string
    is_active?: boolean
}) =>
⋮----
// 更新列表中的数据
⋮----
const deleteRelationType = async (id: number) =>
⋮----
// 从列表中移除
⋮----
const generateRelationDefinition = async (id: number) =>
⋮----
// 刷新列表
⋮----
const reviewRelationType = async (id: number, data: {
    approved: boolean
    definition?: string
    direction_rule?: string
    examples?: string[]
    disambiguation?: string
}) =>
⋮----
// 更新列表中的数据
⋮----
const importLabels = async (data: {
    entity_types: Partial<EntityType>[]
    relation_types: Partial<RelationType>[]
}) =>
⋮----
// 刷新列表
⋮----
const exportLabels = async () =>
⋮----
const previewPrompt = async (promptType?: 'entity' | 'relation' | 'image') =>
⋮----
const fetchVersions = async () =>
⋮----
// 找到当前激活的版本
⋮----
const createSnapshot = async (data: {
    version_name: string
    description: string
    created_by: number
}) =>
⋮----
// 刷新版本列表
⋮----
const activateVersion = async (versionId: string) =>
⋮----
// 刷新版本列表和标签列表
⋮----
const compareVersions = async (version1: string, version2: string) =>
⋮----
const reset = () =>
````

## File: frontend/src/stores/review.ts
````typescript
/**
 * 复核管理Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { reviewApi } from '@/api'
import type { ReviewTask, ReviewStatistics } from '@/types'
⋮----
// State
⋮----
// Actions
const fetchList = async (params?: {
    page?: number
    page_size?: number
    status?: string
    reviewer_id?: number
}) =>
⋮----
const fetchDetail = async (reviewId: string) =>
⋮----
const submit = async (taskId: string) =>
⋮----
const approve = async (reviewId: string, data?: {
    comment?: string
}) =>
⋮----
// 更新列表中的状态
⋮----
const reject = async (reviewId: string, data: {
    comment: string
    suggestions?: string
}) =>
⋮----
// 更新列表中的状态
⋮----
const fetchStatistics = async (datasetId: number) =>
⋮----
const fetchSummary = async (datasetId: number) =>
⋮----
const reset = () =>
````

## File: frontend/src/stores/user.ts
````typescript
/**
 * 用户Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
⋮----
export interface User {
  id: number
  username: string
  role: 'admin' | 'annotator' | 'viewer'
  created_at: string
}
⋮----
const setCurrentUser = (user: User | null) =>
````

## File: frontend/src/types/assignment.ts
````typescript
/**
 * 数据集分配相关类型定义
 * Task 47: 数据集级别任务分配功能
 */
⋮----
/**
 * 分配模式
 */
export type AssignmentMode = 'full' | 'range'
⋮----
/**
 * 转移模式
 */
export type TransferMode = 'all' | 'remaining' | 'completed'
⋮----
/**
 * 分配角色
 */
export type AssignmentRole = 'annotator' | 'reviewer'
⋮----
/**
 * 分配请求
 */
export interface AssignmentRequest {
  user_id: number
  role: AssignmentRole
  mode: AssignmentMode
  start_index?: number
  end_index?: number
}
⋮----
/**
 * 自动分配请求
 */
export interface AutoAssignmentRequest {
  user_ids: number[]
  role: AssignmentRole
}
⋮----
/**
 * 转移分配请求
 */
export interface TransferAssignmentRequest {
  old_user_id: number
  new_user_id: number
  role: AssignmentRole
  transfer_mode: TransferMode
  transfer_reason?: string
}
⋮----
/**
 * 分配信息
 */
export interface AssignmentInfo {
  assignment_id: number
  dataset_id: string
  user_id: number
  username: string
  role: string
  task_range: string | null
  task_count: number
  completed_count: number
⋮----
/**
 * 自动分配信息
 */
export interface AutoAssignmentInfo {
  user_id: number
  username: string
  task_range: string
  task_count: number
}
⋮----
/**
 * 我的数据集信息
 */
export interface MyDatasetInfo {
  dataset_id: string
  name: string
  description?: string
  my_role: string
  my_task_range: string | null
  my_task_count: number
  my_completed_count: number
  total_tasks: number
  assigned_at: string
}
⋮----
/**
 * 分配列表数据
 */
export interface AssignmentListData {
  dataset_id: string
  dataset_name: string
  total_tasks: number
  assignments: AssignmentInfo[]
  unassigned_count: number
  annotator_count: number
  reviewer_count: number
}
⋮----
/**
 * 我的数据集列表数据
 */
export interface MyDatasetsData {
  items: MyDatasetInfo[]
  total: number
  page: number
  page_size: number
}
⋮----
/**
 * 转移结果
 */
export interface TransferResult {
  old_assignment_id: number
  new_assignment_id: number
  old_user: {
    id: number
    username: string
  }
  new_user: {
    id: number
    username: string
  }
  transferred_tasks: number
  transfer_mode: string
  transferred_at: string
}
⋮----
/**
 * 取消分配检查结果
 */
export interface CancelCheckResult {
  can_cancel: boolean
  reason: string
  stats: {
    total_tasks: number
    completed_count: number
    in_review_count: number
    processing_count: number
    pending_count: number
  }
  action?: string
}
````

## File: frontend/src/types/index.ts
````typescript
// ==================== 用户相关 ====================
⋮----
export interface User {
  id: number
  username: string
  role: 'admin' | 'annotator' | 'reviewer' | 'viewer'
  created_at: string
}
⋮----
export interface LoginRequest {
  username: string
  password: string
}
⋮----
export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}
⋮----
// ==================== 语料相关 ====================
⋮----
export interface Corpus {
  id?: number  // 数据库ID（可选，因为API返回的是text_id）
  text_id: string
  text: string
  text_type: string  // 句子分类：问题描述、原因分析、采取措施等
  source_file: string
  source_row: number
  source_field: string
  has_images: boolean
  images?: Image[]
  created_at: string
}
⋮----
id?: number  // 数据库ID（可选，因为API返回的是text_id）
⋮----
text_type: string  // 句子分类：问题描述、原因分析、采取措施等
⋮----
export interface Image {
  id?: number  // 数据库ID（可选）
  image_id: string
  corpus_id?: number
  file_path: string
  original_name: string
  width: number
  height: number
}
⋮----
id?: number  // 数据库ID（可选）
⋮----
// ==================== 数据集相关 ====================
⋮----
export interface Dataset {
  id: number
  dataset_id: string
  name: string
  description: string
  label_schema_version_id?: number
  created_by: number
  created_at: string
  updated_at: string
  statistics?: DatasetStatistics
}
⋮----
export interface DatasetStatistics {
  total_tasks: number
  completed_tasks: number
  reviewed_tasks: number
  pending_tasks: number
}
⋮----
export type DatasetStatus = 'empty' | 'in_progress' | 'completed'
⋮----
// ==================== 标注任务相关 ====================
⋮----
export interface AnnotationTask {
  id: number
  task_id: string
  dataset_id: number
  corpus_id: number
  corpus: Corpus
  status: TaskStatus
  annotation_type: AnnotationType | null
  assigned_to: number
  current_version: number
  text_entities: TextEntity[]
  image_entities: ImageEntity[]
  relations: Relation[]
  created_at: string
  updated_at: string
}
⋮----
export interface TaskListItem {
  id: number
  task_id: string
  dataset_id: string
  dataset_name: string
  corpus_id: number
  corpus_text: string
  status: TaskStatus
  annotation_type: AnnotationType | null
  entity_count: number
  relation_count: number
  current_version: number
  created_at: string
  updated_at: string
}
⋮----
export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'reviewed'
export type AnnotationType = 'automatic' | 'manual'
⋮----
// ==================== 实体相关 ====================
⋮----
export interface TextEntity {
  id: number
  entity_id: string  // 任务内唯一ID (字符串格式: entity-xxx)
  task_id: number
  version: number
  token: string
  label: string
  start_offset: number
  end_offset: number
  confidence?: number
}
⋮----
entity_id: string  // 任务内唯一ID (字符串格式: entity-xxx)
⋮----
export interface ImageEntity {
  id: number
  entity_id: string
  image_id: number
  task_id: number
  version: number
  label: string
  annotation_type: 'whole_image' | 'region'
  bbox?: BoundingBox
  confidence?: number
}
⋮----
export interface BoundingBox {
  x: number
  y: number
  width: number
  height: number
}
⋮----
// ==================== 关系相关 ====================
⋮----
export interface Relation {
  id: number
  relation_id: string  // 任务内唯一ID (字符串格式: relation-xxx)
  task_id: number
  version: number
  from_entity_id: string  // 字符串格式的entity_id
  to_entity_id: string    // 字符串格式的entity_id
  relation_type: string
}
⋮----
relation_id: string  // 任务内唯一ID (字符串格式: relation-xxx)
⋮----
from_entity_id: string  // 字符串格式的entity_id
to_entity_id: string    // 字符串格式的entity_id
⋮----
// ==================== 标签配置相关 ====================
⋮----
export interface EntityType {
  id: number
  type_name: string
  type_name_zh: string
  color: string
  description?: string
  definition?: string  // LLM生成的标准定义
  examples?: string[]  // LLM生成的示例
  disambiguation?: string  // LLM生成的辨析
  is_active: boolean
  is_reviewed: boolean  // 是否已审核
  reviewed_by?: number
  reviewed_at?: string
}
⋮----
definition?: string  // LLM生成的标准定义
examples?: string[]  // LLM生成的示例
disambiguation?: string  // LLM生成的辨析
⋮----
is_reviewed: boolean  // 是否已审核
⋮----
export interface RelationType {
  id: number
  type_name: string
  type_name_zh: string
  color: string
  description?: string
  definition?: string  // LLM生成的标准定义
  direction_rule?: string  // LLM生成的方向规则
  examples?: string[]  // LLM生成的示例
  disambiguation?: string  // LLM生成的辨析
  is_active: boolean
  is_reviewed: boolean
  reviewed_by?: number
  reviewed_at?: string
}
⋮----
definition?: string  // LLM生成的标准定义
direction_rule?: string  // LLM生成的方向规则
examples?: string[]  // LLM生成的示例
disambiguation?: string  // LLM生成的辨析
⋮----
export interface LabelSchema {
  entity_types: EntityType[]
  relation_types: RelationType[]
}
⋮----
// 标签体系版本
export interface LabelSchemaVersion {
  id: number
  version_id: string
  version_name: string
  description: string
  is_active: boolean
  entity_types: EntityType[]
  relation_types: RelationType[]
  created_by: number
  created_at: string
}
⋮----
// ==================== 批量任务相关 ====================
⋮----
export interface BatchJob {
  id: number
  job_id: string
  dataset_id: number
  status: BatchJobStatus
  total_tasks: number
  completed_tasks: number
  failed_tasks: number
  started_at?: string
  completed_at?: string
  created_at: string
}
⋮----
export type BatchJobStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
⋮----
export interface BatchJobProgress {
  job_id: string
  status: BatchJobStatus
  progress: {
    total: number
    completed: number
    failed: number
  }
  started_at?: string
  completed_at?: string
}
⋮----
// ==================== 复核相关 ====================
⋮----
export interface ReviewTask {
  id: number
  review_id: string
  task_id: number
  task: AnnotationTask
  status: ReviewStatus
  reviewer_id?: number
  review_comment?: string
  reviewed_at?: string
  created_at: string
}
⋮----
export type ReviewStatus = 'pending' | 'approved' | 'rejected'
⋮----
export interface ReviewStatistics {
  total_reviews: number
  approved: number
  rejected: number
  pending: number
  approval_rate: number
  avg_review_time: number
}
⋮----
// ==================== 版本管理相关 ====================
⋮----
export interface Version {
  id: number
  history_id: string
  task_id: number
  version: number
  change_type: ChangeType
  change_description?: string
  changed_by: number
  snapshot_data: VersionSnapshot
  created_at: string
}
⋮----
export type ChangeType = 'create' | 'update' | 'delete'
⋮----
export interface VersionSnapshot {
  text_entities: TextEntity[]
  image_entities: ImageEntity[]
  relations: Relation[]
}
⋮----
export interface VersionDiff {
  added_entities: TextEntity[]
  removed_entities: TextEntity[]
  modified_entities: Array<{
    old: TextEntity
    new: TextEntity
  }>
  added_relations: Relation[]
  removed_relations: Relation[]
  modified_relations: Array<{
    old: Relation
    new: Relation
  }>
}
⋮----
// ==================== API响应相关 ====================
⋮----
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}
⋮----
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}
⋮----
export interface ErrorResponse {
  detail: string
}
⋮----
// ==================== 文档管理模块类型 ====================
⋮----
export interface ProcessorInfo {
  name: string
  display_name: string
}
⋮----
export interface ProcessedFile {
  filename: string
  data_source: string
  table_count: number
  processed_time: string
  output_dir: string
}
⋮----
export interface UploadResult {
  success: boolean
  is_duplicate: boolean
  message: string
  data_source?: string
  table_count?: number
  image_count?: number
  corpus_count?: number
}
⋮----
export interface ImportResult {
  success: boolean
  message: string
  total_records: number
  inserted_records: number
  skipped_records: number
}
⋮----
export interface ExportResult {
  success: boolean
  data: any[]
  count: number
}
⋮----
export type ExportFormat = 'entity_text' | 'clip_alignment' | 'qa_alignment'
⋮----
export interface BatchExportParams {
  data_sources?: string[]
  formats: ExportFormat[]
  include_images?: boolean
}
⋮----
export interface StatisticsData {
  total_events: number
  defect_distribution: { name: string; count: number }[]
  customer_ranking: { name: string; count: number }[]
  four_m_distribution?: { element: string; count: number }[]
  workshop_distribution?: { name: string; count: number }[]
  line_distribution?: { name: string; count: number }[]
  inspection_node_distribution?: { name: string; count: number }[]
  status_distribution?: { status: string; count: number }[]
}
````

## File: frontend/src/utils/datetime.ts
````typescript
/**
 * 日期时间工具函数
 *
 * 背景：后端使用 datetime.utcnow() 存储 UTC 时间，但序列化时通过
 * .isoformat() 输出的字符串不带时区后缀（如 "2026-03-04T05:52:59"）。
 * 浏览器解析无时区后缀的字符串时，会将其当作本地时间而非 UTC，导致
 * 在 UTC+8 环境下时间显示比实际早 8 小时。
 *
 * 解决方案：解析前统一追加 "Z"，告知浏览器这是 UTC 时间，浏览器会
 * 自动转换为本地时间显示。
 */
⋮----
import { format, formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'
⋮----
/**
 * 将后端返回的 UTC 时间字符串解析为 Date 对象（自动补 Z 后缀）
 */
export function parseUTCDate(dateString: string): Date
⋮----
// 若已有时区信息（Z 或 +XX:XX），直接解析；否则追加 Z 表示 UTC
⋮----
/**
 * 格式化为 "yyyy-MM-dd HH:mm:ss" 本地时间字符串
 */
export function formatDateTime(dateString: string | null | undefined): string
⋮----
/**
 * 格式化为 "yyyy-MM-dd HH:mm" 本地时间字符串
 */
export function formatDateTimeShort(dateString: string | null | undefined): string
⋮----
/**
 * 格式化为相对时间（如 "3 分钟前"）
 */
export function formatDateRelative(dateString: string | null | undefined): string
````

## File: frontend/src/views/annotation/AnnotationEditor.vue
````vue
<template>
  <div class="annotation-editor-page">
    <div class="page-header">
      <h2>文本标注编辑器</h2>
      <div class="actions">
        <el-button @click="handleSave">保存</el-button>
        <el-button type="primary" @click="handleSubmit">提交复核</el-button>
      </div>
    </div>

    <div class="editor-container">
      <TextAnnotationEditor
        :text="sampleText"
        :entities="entities"
        :relations="relations"
        :entity-types="entityTypes"
        :relation-types="relationTypes"
        @add-entity="handleAddEntity"
        @update-entity="handleUpdateEntity"
        @delete-entity="handleDeleteEntity"
        @add-relation="handleAddRelation"
        @delete-relation="handleDeleteRelation"
      />
    </div>
  </div>
</template>
⋮----
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import TextAnnotationEditor from '@/components/annotation/TextAnnotationEditor.vue'
import { useLabelStore } from '@/stores/label'
import type { EntityType, RelationType } from '@/api/label'

interface Entity {
  id?: number
  text: string
  start_offset: number
  end_offset: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Relation {
  id?: number
  source_entity_id: number
  target_entity_id: number
  relation_type_id: number
  relation_type_name: string
}

const labelStore = useLabelStore()

// 示例文本
const sampleText = ref(`某客户反馈产品型号ABC-123在使用过程中出现了屏幕闪烁的问题。经检查发现，该批次产品在2024年1月15日生产，使用的是供应商XYZ提供的显示屏。

初步分析认为，问题可能是由于焊接工艺参数设置不当导致的。具体表现为焊接温度过高（实际温度350℃，标准温度应为320℃），导致显示屏排线接触不良。

处置措施：
1. 立即停止使用该批次产品
2. 对所有同批次产品进行全面检查
3. 调整焊接设备温度参数
4. 对操作人员进行再培训

改进措施：
1. 建立更严格的工艺参数监控机制
2. 增加产品出厂前的质量检测项目
3. 与供应商XYZ协商改进显示屏质量`)

const entities = ref<Entity[]>([])
const relations = ref<Relation[]>([])
const entityTypes = ref<EntityType[]>([])
const relationTypes = ref<RelationType[]>([])
let nextEntityId = 1
let nextRelationId = 1

// 加载标签配置
onMounted(async () => {
  try {
    await labelStore.fetchEntityTypes({ include_inactive: false })
    await labelStore.fetchRelationTypes({ include_inactive: false })
    entityTypes.value = labelStore.entityTypes
    relationTypes.value = labelStore.relationTypes
  } catch (error) {
    ElMessage.error('加载标签配置失败')
  }
})

const handleAddEntity = (entity: Omit<Entity, 'id'>) => {
  const newEntity: Entity = {
    ...entity,
    id: nextEntityId++
  }
  entities.value.push(newEntity)
  ElMessage.success('实体添加成功')
}

const handleUpdateEntity = (id: number, updates: Partial<Entity>) => {
  const index = entities.value.findIndex(e => e.id === id)
  if (index !== -1) {
    entities.value[index] = { ...entities.value[index], ...updates }
    ElMessage.success('实体更新成功')
  }
}

const handleDeleteEntity = (id: number) => {
  entities.value = entities.value.filter(e => e.id !== id)
  // 同时删除相关的关系
  relations.value = relations.value.filter(
    r => r.source_entity_id !== id && r.target_entity_id !== id
  )
  ElMessage.success('实体删除成功')
}

const handleAddRelation = (relation: Omit<Relation, 'id'>) => {
  const newRelation: Relation = {
    ...relation,
    id: nextRelationId++
  }
  relations.value.push(newRelation)
  ElMessage.success('关系添加成功')
}

const handleDeleteRelation = (id: number) => {
  relations.value = relations.value.filter(r => r.id !== id)
  ElMessage.success('关系删除成功')
}

const handleSave = () => {
  ElMessage.success('保存成功')
  console.log('Entities:', entities.value)
  console.log('Relations:', relations.value)
}

const handleSubmit = () => {
  ElMessage.success('提交复核成功')
}
</script>
⋮----
<style scoped>
.annotation-editor-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 10px;
}

.editor-container {
  flex: 1;
  overflow: hidden;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
}
</style>
````

## File: frontend/src/views/annotation/AnnotationList.vue
````vue
<template>
  <div class="annotation-list-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="title-section">
            <span class="title">标注任务列表</span>
            <span v-if="currentDatasetName" class="dataset-badge">
              <el-tag type="primary" size="large">{{ currentDatasetName }}</el-tag>
            </span>
          </div>
          <el-breadcrumb v-if="currentDatasetName" separator="/">
            <el-breadcrumb-item :to="{ name: 'my-datasets' }">我的数据集</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentDatasetName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
      </template>

      <!-- 筛选区域 -->
      <div class="filter-section">
        <el-form :inline="true" :model="filters">
          <el-form-item label="数据集">
            <el-select
              v-model="filters.dataset_id"
              placeholder="全部数据集"
              clearable
              style="width: 200px"
              @change="handleFilterChange"
            >
              <el-option
                v-for="dataset in datasets"
                :key="dataset.dataset_id"
                :label="dataset.name"
                :value="dataset.dataset_id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="状态">
            <el-select
              v-model="filters.status"
              placeholder="全部状态"
              clearable
              style="width: 150px"
              @change="handleFilterChange"
            >
              <el-option
                v-for="option in STATUS_OPTIONS"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="loadTasks">查询</el-button>
            <el-button @click="clearFilters">清除筛选</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 任务列表表格 -->
      <el-table
        v-loading="loading"
        :data="tasks"
        style="width: 100%"
        @row-click="handleRowClick"
      >
        <el-table-column prop="task_id" label="任务ID" width="180" />

        <el-table-column prop="dataset_name" label="数据集" width="150" show-overflow-tooltip />

        <el-table-column prop="corpus_text" label="语料预览" min-width="300" show-overflow-tooltip />

        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="标注信息" width="120">
          <template #default="{ row }">
            <div class="annotation-info">
              <span>实体: {{ row.entity_count }}</span>
              <span>关系: {{ row.relation_count }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click.stop="goToAnnotation(row.task_id)"
            >
              编辑
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态 -->
      <el-empty
        v-if="!loading && tasks.length === 0"
        description="暂无分配的任务"
      />

      <!-- 分页 -->
      <div v-if="tasks.length > 0" class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handlePageSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>
⋮----
<template #header>
        <div class="card-header">
          <div class="title-section">
            <span class="title">标注任务列表</span>
            <span v-if="currentDatasetName" class="dataset-badge">
              <el-tag type="primary" size="large">{{ currentDatasetName }}</el-tag>
            </span>
          </div>
          <el-breadcrumb v-if="currentDatasetName" separator="/">
            <el-breadcrumb-item :to="{ name: 'my-datasets' }">我的数据集</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentDatasetName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
      </template>
⋮----
<el-tag type="primary" size="large">{{ currentDatasetName }}</el-tag>
⋮----
<el-breadcrumb-item>{{ currentDatasetName }}</el-breadcrumb-item>
⋮----
<!-- 筛选区域 -->
⋮----
<!-- 任务列表表格 -->
⋮----
<template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
⋮----
{{ getStatusText(row.status) }}
⋮----
<template #default="{ row }">
            <div class="annotation-info">
              <span>实体: {{ row.entity_count }}</span>
              <span>关系: {{ row.relation_count }}</span>
            </div>
          </template>
⋮----
<span>实体: {{ row.entity_count }}</span>
<span>关系: {{ row.relation_count }}</span>
⋮----
<template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
⋮----
{{ formatDate(row.created_at) }}
⋮----
<template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click.stop="goToAnnotation(row.task_id)"
            >
              编辑
            </el-button>
          </template>
⋮----
<!-- 空状态 -->
⋮----
<!-- 分页 -->
⋮----
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { annotationApi } from '@/api/annotation'
import { datasetApi } from '@/api/dataset'
import type { TaskListItem, Dataset } from '@/types'
import { getStatusText, getStatusType, STATUS_OPTIONS } from '@/constants/taskStatus'

const router = useRouter()
const route = useRoute()

// 状态
const loading = ref(false)
const tasks = ref<TaskListItem[]>([])
const datasets = ref<Dataset[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const currentDatasetName = ref('')

// 筛选条件
const filters = ref({
  dataset_id: '',
  status: ''
})

// 加载数据集列表（用于筛选）
const loadDatasets = async () => {
  // 从任务列表中提取唯一的数据集
  // 这样可以避免额外的API调用和权限问题
  const uniqueDatasets = new Map<string, string>()
  
  tasks.value.forEach(task => {
    if (task.dataset_id && task.dataset_name) {
      uniqueDatasets.set(task.dataset_id, task.dataset_name)
    }
  })
  
  datasets.value = Array.from(uniqueDatasets.entries()).map(([dataset_id, name]) => ({
    dataset_id,
    name
  }))
}

// 加载任务列表
const loadTasks = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    if (filters.value.dataset_id) {
      params.dataset_id = filters.value.dataset_id
    }
    if (filters.value.status) {
      params.status = filters.value.status
    }

    const response = await annotationApi.getTaskList(params)

    if (response.success) {
      tasks.value = response.data.items
      total.value = response.data.total
      
      // 从任务列表中提取数据集信息用于筛选
      loadDatasets()
    }
  } catch (error: any) {
    console.error('加载任务列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载任务列表失败')
  } finally {
    loading.value = false
  }
}

// 筛选变化处理
const handleFilterChange = () => {
  currentPage.value = 1
  loadTasks()
}

// 清除筛选
const clearFilters = () => {
  filters.value.dataset_id = ''
  filters.value.status = ''
  currentDatasetName.value = ''
  currentPage.value = 1
  
  // 清除URL参数
  router.replace({ query: {} })
  
  loadTasks()
}

// 分页变化处理
const handlePageChange = (page: number) => {
  currentPage.value = page
  loadTasks()
}

const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadTasks()
}

// 行点击处理
const handleRowClick = (row: TaskListItem) => {
  goToAnnotation(row.task_id)
}

// 跳转到标注编辑器
const goToAnnotation = (taskId: string) => {
  router.push({ name: 'annotation-editor', params: { taskId } })
}

// 格式化日期
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 更新当前数据集名称
const updateCurrentDatasetName = () => {
  if (filters.value.dataset_id) {
    const dataset = datasets.value.find(d => d.dataset_id === filters.value.dataset_id)
    currentDatasetName.value = dataset?.name || ''
  } else {
    currentDatasetName.value = ''
  }
}

// 监听路由参数变化（从"我的数据集"跳转过来时）
watch(
  () => route.query.dataset_id,
  (datasetId) => {
    if (datasetId) {
      filters.value.dataset_id = datasetId as string
      loadTasks()
    }
  },
  { immediate: true }
)

// 监听数据集列表变化，更新当前数据集名称
watch(
  () => datasets.value,
  () => {
    updateCurrentDatasetName()
  },
  { deep: true }
)

onMounted(() => {
  // 只加载任务，数据集列表会从任务中提取
  if (!route.query.dataset_id) {
    loadTasks()
  }
})
</script>
⋮----
<style scoped lang="scss">
.annotation-list-container {
  padding: 20px;

  .card-header {
    display: flex;
    flex-direction: column;
    gap: 12px;

    .title-section {
      display: flex;
      align-items: center;
      gap: 12px;

      .title {
        font-size: 18px;
        font-weight: 600;
      }

      .dataset-badge {
        display: flex;
        align-items: center;
      }
    }
  }

  .filter-section {
    margin-bottom: 20px;
  }

  .annotation-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 12px;
    color: #606266;
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  :deep(.el-table__row) {
    cursor: pointer;

    &:hover {
      background-color: #f5f7fa;
    }
  }
}
</style>
````

## File: frontend/src/views/annotation/AnnotationPage.vue
````vue
<template>
  <div class="annotation-page">
    <!-- 加载状态 -->
    <el-loading v-if="loading" fullscreen text="加载任务数据中..." />
    
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <el-divider direction="vertical" />
        <h2>标注任务 #{{ taskId }}</h2>
        <el-tag :type="getStatusType(taskStatus)" size="small">
          {{ getStatusText(taskStatus) }}
        </el-tag>
      </div>

      <div class="header-right">
        <el-button-group>
          <el-button 
            @click="handleSave" 
            :loading="saving"
            :disabled="taskStatus === 'under_review' || taskStatus === 'approved'"
          >
            <el-icon><DocumentCopy /></el-icon>
            保存
          </el-button>
          <el-button 
            v-if="taskStatus !== 'under_review' && taskStatus !== 'approved'"
            type="primary" 
            @click="handleSubmitReview"
          >
            <el-icon><Check /></el-icon>
            提交复核
          </el-button>
          <el-button 
            v-else
            type="success" 
            @click="goToReview"
          >
            <el-icon><View /></el-icon>
            查看复核
          </el-button>
        </el-button-group>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="page-content">
      <div class="content-wrapper">
        <!-- 驳回提示 -->
        <el-alert
          v-if="taskStatus === 'rejected'"
          title="任务已被驳回"
          type="warning"
          description="该任务已被复核人员驳回，请根据驳回意见修改后重新保存并提交复核。"
          show-icon
          :closable="false"
          class="rejection-alert"
        />
        
        <!-- 只读提示 -->
        <el-alert
          v-if="isReadonly"
          title="只读模式"
          type="info"
          :description="getReadonlyMessage()"
          show-icon
          :closable="false"
          class="readonly-alert"
        />
        
        <!-- 左侧：标注编辑器 -->
        <div class="editor-section">
          <el-tabs v-model="activeTab" class="editor-tabs">
            <!-- 文本标注 -->
            <el-tab-pane label="文本标注" name="text">
              <TextAnnotationEditor
                v-if="corpusText"
                :text="corpusText"
                :entities="textEntities"
                :relations="relations"
                :entity-types="entityTypes"
                :relation-types="relationTypes"
                :readonly="isReadonly"
                @add-entity="handleAddTextEntity"
                @update-entity="handleUpdateTextEntity"
                @delete-entity="handleDeleteTextEntity"
                @add-relation="handleAddRelation"
                @delete-relation="handleDeleteRelation"
              />
              <el-empty v-else description="无文本内容" />
            </el-tab-pane>

            <!-- 图片标注 -->
            <el-tab-pane
              v-for="image in images"
              :key="image.id"
              :label="`图片 ${image.id}`"
              :name="`image-${image.id}`"
            >
              <ImageAnnotationEditor
                :image-url="image.url"
                :whole-image-entities="getImageEntities(image.id)"
                :bboxes="getImageBBoxes(image.id)"
                :entity-types="entityTypes"
                :readonly="isReadonly"
                @add-whole-image-entity="(entity) => handleAddWholeImageEntity(image.id, entity)"
                @delete-whole-image-entity="(id) => handleDeleteWholeImageEntity(image.id, id)"
                @add-bbox="(bbox) => handleAddBBox(image.id, bbox)"
                @update-bbox="(id, bbox) => handleUpdateBBox(image.id, id, bbox)"
                @delete-bbox="(id) => handleDeleteBBox(image.id, id)"
              />
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <!-- 右侧：信息面板 -->
      <div class="info-panel">
        <!-- 驳回历史 -->
        <el-card v-if="rejectionHistory.length > 0" class="info-card rejection-history-card">
          <template #header>
            <div class="card-header">
              <span>驳回历史</span>
              <el-tag type="warning" size="small">{{ rejectionHistory.length }} 次</el-tag>
            </div>
          </template>
          <el-scrollbar max-height="300px">
            <el-timeline>
              <el-timeline-item
                v-for="(rejection, index) in rejectionHistory"
                :key="index"
                :timestamp="formatDateTime(rejection.reviewed_at)"
                placement="top"
                type="warning"
              >
                <el-card>
                  <div class="rejection-item">
                    <div class="rejection-header">
                      <span class="rejection-round">第 {{ rejectionHistory.length - index }} 次驳回</span>
                      <span class="rejection-reviewer">复核人: {{ rejection.reviewer_id ? `用户${rejection.reviewer_id}` : '未知' }}</span>
                    </div>
                    <div class="rejection-comment">
                      {{ rejection.review_comment || '无驳回意见' }}
                    </div>
                  </div>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-scrollbar>
        </el-card>
        
        <!-- 任务信息 -->
        <el-card class="info-card">
          <template #header>
            <span>任务信息</span>
          </template>
          <div class="info-item">
            <span class="label">任务ID:</span>
            <span class="value">{{ taskId }}</span>
          </div>
          <div class="info-item">
            <span class="label">数据集ID:</span>
            <span class="value">{{ datasetId || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="label">语料ID:</span>
            <span class="value">{{ corpusId || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="label">状态:</span>
            <span class="value">{{ getStatusText(taskStatus) }}</span>
          </div>
          <div class="info-item">
            <span class="label">创建时间:</span>
            <span class="value">{{ formatDateTime(createdAt) }}</span>
          </div>
          <div class="info-item">
            <span class="label">更新时间:</span>
            <span class="value">{{ formatDateTime(updatedAt) }}</span>
          </div>
        </el-card>

        <!-- 统计信息 -->
        <el-card class="info-card">
          <template #header>
            <span>标注统计</span>
          </template>
          <div class="stat-item">
            <span class="stat-label">文本实体:</span>
            <span class="stat-value">{{ textEntities.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">关系:</span>
            <span class="stat-value">{{ relations.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">图片实体:</span>
            <span class="stat-value">{{ imageEntities.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">边界框:</span>
            <span class="stat-value">{{ bboxes.length }}</span>
          </div>
        </el-card>

        <!-- 版本历史 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>版本历史</span>
              <el-button text size="small" @click="refreshVersions">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
          <el-scrollbar max-height="300px">
            <div class="version-list">
              <div
                v-for="version in versions"
                :key="version.id"
                class="version-item"
                :class="{ current: version.is_current }"
              >
                <div class="version-info">
                  <span class="version-number">v{{ version.version_number }}</span>
                  <span class="version-time">{{ formatTime(version.created_at) }}</span>
                </div>
                <el-button
                  v-if="!version.is_current"
                  text
                  size="small"
                  @click="handleRollback(version.id)"
                >
                  回滚
                </el-button>
              </div>
            </div>
          </el-scrollbar>
        </el-card>

        <!-- 快捷键说明 -->
        <el-card class="info-card">
          <template #header>
            <span>快捷键</span>
          </template>
          <div class="shortcut-list">
            <div class="shortcut-item">
              <kbd>Ctrl + S</kbd>
              <span>保存</span>
            </div>
            <div class="shortcut-item">
              <kbd>Ctrl + Enter</kbd>
              <span>提交复核</span>
            </div>
            <div class="shortcut-item">
              <kbd>Esc</kbd>
              <span>取消操作</span>
            </div>
          </div>
          <el-divider />
          <div class="annotation-guide">
            <h4>标注操作</h4>
            <div class="guide-item">
              <strong>实体标注：</strong>
              <p>鼠标拖动选择文本，在弹出菜单中选择实体类型</p>
            </div>
            <div class="guide-item">
              <strong>关系标注：</strong>
              <p>按住 <kbd>Ctrl</kbd> 键，依次点击源实体和目标实体，然后选择关系类型</p>
            </div>
            <div class="guide-item">
              <strong>删除标注：</strong>
              <p>在右侧列表中点击删除按钮</p>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>
⋮----
<!-- 加载状态 -->
⋮----
<!-- 页面头部 -->
⋮----
<h2>标注任务 #{{ taskId }}</h2>
⋮----
{{ getStatusText(taskStatus) }}
⋮----
<!-- 内容区域 -->
⋮----
<!-- 驳回提示 -->
⋮----
<!-- 只读提示 -->
⋮----
<!-- 左侧：标注编辑器 -->
⋮----
<!-- 文本标注 -->
⋮----
<!-- 图片标注 -->
⋮----
<!-- 右侧：信息面板 -->
⋮----
<!-- 驳回历史 -->
⋮----
<template #header>
            <div class="card-header">
              <span>驳回历史</span>
              <el-tag type="warning" size="small">{{ rejectionHistory.length }} 次</el-tag>
            </div>
          </template>
⋮----
<el-tag type="warning" size="small">{{ rejectionHistory.length }} 次</el-tag>
⋮----
<span class="rejection-round">第 {{ rejectionHistory.length - index }} 次驳回</span>
<span class="rejection-reviewer">复核人: {{ rejection.reviewer_id ? `用户${rejection.reviewer_id}` : '未知' }}</span>
⋮----
{{ rejection.review_comment || '无驳回意见' }}
⋮----
<!-- 任务信息 -->
⋮----
<template #header>
            <span>任务信息</span>
          </template>
⋮----
<span class="value">{{ taskId }}</span>
⋮----
<span class="value">{{ datasetId || '-' }}</span>
⋮----
<span class="value">{{ corpusId || '-' }}</span>
⋮----
<span class="value">{{ getStatusText(taskStatus) }}</span>
⋮----
<span class="value">{{ formatDateTime(createdAt) }}</span>
⋮----
<span class="value">{{ formatDateTime(updatedAt) }}</span>
⋮----
<!-- 统计信息 -->
⋮----
<template #header>
            <span>标注统计</span>
          </template>
⋮----
<span class="stat-value">{{ textEntities.length }}</span>
⋮----
<span class="stat-value">{{ relations.length }}</span>
⋮----
<span class="stat-value">{{ imageEntities.length }}</span>
⋮----
<span class="stat-value">{{ bboxes.length }}</span>
⋮----
<!-- 版本历史 -->
⋮----
<template #header>
            <div class="card-header">
              <span>版本历史</span>
              <el-button text size="small" @click="refreshVersions">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
⋮----
<span class="version-number">v{{ version.version_number }}</span>
<span class="version-time">{{ formatTime(version.created_at) }}</span>
⋮----
<!-- 快捷键说明 -->
⋮----
<template #header>
            <span>快捷键</span>
          </template>
⋮----
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  DocumentCopy,
  Check,
  Refresh,
  View
} from '@element-plus/icons-vue'
import TextAnnotationEditor from '@/components/annotation/TextAnnotationEditor.vue'
import ImageAnnotationEditor from '@/components/annotation/ImageAnnotationEditor.vue'
import { useLabelStore } from '@/stores/label'
import type { EntityType, RelationType } from '@/api/label'
import { annotationApi } from '@/api/annotation'
import { reviewApi } from '@/api/review'

// 路由
const route = useRoute()
const router = useRouter()
const taskId = computed(() => route.params.taskId as string)

// Store
const labelStore = useLabelStore()

// 状态
const activeTab = ref('text')
const saving = ref(false)
const loading = ref(true)
const taskStatus = ref<'pending' | 'annotating' | 'reviewing' | 'approved' | 'rejected'>('pending')

// 只读模式：当任务处于复核中或已通过状态时，不允许编辑
// 注意：rejected（已驳回）状态应该允许编辑，以便标注员修改后重新提交
const isReadonly = computed(() => {
  return ['under_review', 'approved'].includes(taskStatus.value)
})

// 获取只读提示信息
const getReadonlyMessage = () => {
  const messages: Record<string, string> = {
    under_review: '该任务正在复核中，暂时无法编辑。如需修改，请等待复核结果。',
    approved: '该任务已通过复核，不可再编辑。'
  }
  return messages[taskStatus.value] || '该任务当前不可编辑。'
}

// 任务信息
const datasetName = ref('')
const datasetId = ref('')
const corpusId = ref('')
const annotatorName = ref('当前用户')
const createdAt = ref('')
const updatedAt = ref('')

// 语料文本
const corpusText = ref('')

// 图片列表
const images = ref<Array<{ id: number; url: string }>>([])

// 标注数据
const textEntities = ref<any[]>([])
const relations = ref<any[]>([])
const imageEntities = ref<Map<number, any[]>>(new Map())
const bboxes = ref<Map<number, any[]>>(new Map())

// 标签配置
const entityTypes = ref<EntityType[]>([])
const relationTypes = ref<RelationType[]>([])

// 版本历史
const versions = ref<any[]>([])

// 驳回历史
const rejectionHistory = ref<any[]>([])

// 加载任务数据
const loadTaskData = async () => {
  try {
    loading.value = true
    
    // 调用后端API获取任务详情（使用封装的API服务，包含认证头）
    const result = await annotationApi.getAnnotationTask(taskId.value)
    
    if (!result.success) {
      throw new Error(result.message || '获取任务详情失败')
    }
    
    const data = result.data
    
    // 设置任务信息
    datasetId.value = data.dataset_id || ''
    corpusId.value = data.corpus?.text_id || ''
    taskStatus.value = data.status || 'pending'
    createdAt.value = data.created_at || ''
    updatedAt.value = data.updated_at || ''
    
    // 设置语料文本
    corpusText.value = data.corpus?.text || ''
    
    // 设置实体数据 - 需要从 entityTypes 中匹配颜色和类型名称
    textEntities.value = data.entities?.map((e: any) => {
      // 尝试匹配中文名或英文名
      const entityType = entityTypes.value.find(et => 
        et.type_name === e.label || et.type_name_zh === e.label
      )
      return {
        id: e.id,
        entity_id: e.entity_id,
        text: e.token,
        entity_type_name: e.label,
        entity_type_id: entityType?.id,
        start_offset: e.start_offset,
        end_offset: e.end_offset,
        confidence: e.confidence,
        color: entityType?.color || '#cccccc' // 默认颜色
      }
    }) || []
    
    // 设置关系数据 - 需要从 relationTypes 中匹配类型名称
    relations.value = data.relations?.map((r: any) => {
      // 尝试匹配中文名或英文名
      const relationType = relationTypes.value.find(rt => 
        rt.type_name === r.relation_type || rt.type_name_zh === r.relation_type
      )
      return {
        id: r.id,
        relation_id: r.relation_id,
        source_entity_id: r.from_entity_id,
        target_entity_id: r.to_entity_id,
        relation_type_name: r.relation_type,
        relation_type_id: relationType?.id
      }
    }) || []
    
    // TODO: 加载图片数据
    // 目前图片数据为空，后续需要实现
    images.value = []
    
    // 加载驳回历史
    await loadRejectionHistory()
    
    console.log('任务数据加载成功:', {
      taskId: taskId.value,
      taskStatus: taskStatus.value,
      isReadonly: isReadonly.value,
      corpusText: corpusText.value,
      entities: textEntities.value.length,
      relations: relations.value.length,
      entityTypes: entityTypes.value.length,
      relationTypes: relationTypes.value.length,
      rejections: rejectionHistory.value.length
    })
  } catch (error: any) {
    console.error('加载任务数据失败:', error)
    ElMessage.error(error.message || '加载任务数据失败')
  } finally {
    loading.value = false
  }
}

// 加载驳回历史
const loadRejectionHistory = async () => {
  try {
    // 查询该任务的所有复核记录
    const response = await reviewApi.list({ 
      skip: 0, 
      limit: 100 
    })
    
    const reviews = Array.isArray(response) ? response : (response.data || [])
    
    // 筛选出该任务的所有驳回记录，按时间倒序排列
    rejectionHistory.value = reviews
      .filter((r: any) => r.task_id === taskId.value && r.status === 'rejected')
      .sort((a: any, b: any) => {
        const timeA = new Date(a.reviewed_at || a.created_at).getTime()
        const timeB = new Date(b.reviewed_at || b.created_at).getTime()
        return timeB - timeA // 最新的在前
      })
    
    console.log('[AnnotationPage] 驳回历史加载完成:', rejectionHistory.value.length, '条记录')
  } catch (error) {
    console.error('加载驳回历史失败:', error)
    // 不显示错误提示，因为这不是关键功能
  }
}

// 加载数据
onMounted(async () => {
  try {
    // 加载标签配置
    await labelStore.fetchEntityTypes({ include_inactive: false })
    await labelStore.fetchRelationTypes({ include_inactive: false })
    entityTypes.value = labelStore.entityTypes
    relationTypes.value = labelStore.relationTypes
    
    console.log('[AnnotationPage] Loaded entityTypes:', entityTypes.value)
    console.log('[AnnotationPage] Loaded relationTypes:', relationTypes.value)

    // 加载任务数据
    await loadTaskData()

    // 初始化图片实体和边界框
    images.value.forEach(image => {
      imageEntities.value.set(image.id, [])
      bboxes.value.set(image.id, [])
    })

    // 注册快捷键
    document.addEventListener('keydown', handleKeyDown)
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})

// 快捷键处理
const handleKeyDown = (e: KeyboardEvent) => {
  // Ctrl + S: 保存
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault()
    handleSave()
  }
  // Ctrl + Enter: 提交复核
  if (e.ctrlKey && e.key === 'Enter') {
    e.preventDefault()
    handleSubmitReview()
  }
  // Esc: 取消操作
  if (e.key === 'Escape') {
    // TODO: 取消当前操作
  }
}

// 文本实体操作
const handleAddTextEntity = async (entity: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API添加实体
    const response = await annotationApi.addTextEntity(taskId.value, {
      token: entity.text,
      label: entity.entity_type_name,
      start_offset: entity.start_offset,
      end_offset: entity.end_offset
    })
    
    // 添加到本地数组，使用后端返回的ID
    textEntities.value.push({
      ...entity,
      id: response.data.id,
      entity_id: response.data.entity_id
    })
  } catch (error) {
    console.error('添加实体失败:', error)
    ElMessage.error('添加实体失败')
  }
}

const handleUpdateTextEntity = async (id: number, updates: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API更新实体
    await annotationApi.updateTextEntity(taskId.value, id, {
      token: updates.text,
      label: updates.entity_type_name,
      start_offset: updates.start_offset,
      end_offset: updates.end_offset
    })
    
    // 更新本地数组
    const index = textEntities.value.findIndex(e => e.id === id)
    if (index !== -1) {
      textEntities.value[index] = { ...textEntities.value[index], ...updates }
    }
  } catch (error) {
    console.error('更新实体失败:', error)
    ElMessage.error('更新实体失败')
  }
}

const handleDeleteTextEntity = async (id: number) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API删除实体（后端会自动删除相关关系）
    await annotationApi.deleteTextEntity(taskId.value, id)
    
    // 删除本地相关关系
    relations.value = relations.value.filter(
      r => r.source_entity_id !== id && r.target_entity_id !== id
    )
    // 删除本地实体
    textEntities.value = textEntities.value.filter(e => e.id !== id)
    
    console.log('[AnnotationPage] Entity deleted, remaining entities:', textEntities.value.length)
  } catch (error) {
    console.error('删除实体失败:', error)
    ElMessage.error('删除实体失败')
  }
}

// 关系操作
const handleAddRelation = async (relation: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API添加关系
    const response = await annotationApi.addRelation(taskId.value, {
      from_entity_id: relation.source_entity_id,
      to_entity_id: relation.target_entity_id,
      relation_type: relation.relation_type_name
    })
    
    // 添加到本地数组，使用后端返回的ID
    relations.value.push({
      ...relation,
      id: response.data.id,
      relation_id: response.data.relation_id
    })
  } catch (error) {
    console.error('添加关系失败:', error)
    ElMessage.error('添加关系失败')
  }
}

const handleDeleteRelation = async (id: number) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API删除关系
    await annotationApi.deleteRelation(taskId.value, id)
    
    // 删除本地关系
    relations.value = relations.value.filter(r => r.id !== id)
  } catch (error) {
    console.error('删除关系失败:', error)
    ElMessage.error('删除关系失败')
  }
}

// 图片实体操作
const getImageEntities = (imageId: number) => {
  return imageEntities.value.get(imageId) || []
}

const handleAddWholeImageEntity = (imageId: number, entity: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const entities = imageEntities.value.get(imageId) || []
  entities.push({ ...entity, id: Date.now() })
  imageEntities.value.set(imageId, entities)
}

const handleDeleteWholeImageEntity = (imageId: number, entityId: number) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const entities = imageEntities.value.get(imageId) || []
  imageEntities.value.set(imageId, entities.filter(e => e.id !== entityId))
}

// 边界框操作
const getImageBBoxes = (imageId: number) => {
  return bboxes.value.get(imageId) || []
}

const handleAddBBox = (imageId: number, bbox: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const boxes = bboxes.value.get(imageId) || []
  boxes.push({ ...bbox, id: Date.now() })
  bboxes.value.set(imageId, boxes)
}

const handleUpdateBBox = (imageId: number, bboxId: number, updates: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const boxes = bboxes.value.get(imageId) || []
  const index = boxes.findIndex(b => b.id === bboxId)
  if (index !== -1) {
    boxes[index] = { ...boxes[index], ...updates }
    bboxes.value.set(imageId, boxes)
  }
}

const handleDeleteBBox = (imageId: number, bboxId: number) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const boxes = bboxes.value.get(imageId) || []
  bboxes.value.set(imageId, boxes.filter(b => b.id !== bboxId))
}

// 保存
const handleSave = async () => {
  if (!taskId.value) return
  
  saving.value = true
  try {
    // 标注数据已经通过增删改操作实时保存到后端
    // 这里更新任务状态为"已完成"，以便后续提交复核
    await annotationApi.updateAnnotationTask(
      taskId.value, 
      { status: 'completed' }
    )
    
    taskStatus.value = 'completed'
    ElMessage.success('保存成功')
    updatedAt.value = new Date().toISOString()
    
    // 重新加载任务数据以获取最新版本号
    await loadTaskData()
  } catch (error: any) {
    console.error('保存失败:', error)
    ElMessage.error(error.message || '保存失败')
  } finally {
    saving.value = false
  }
}

// 提交复核
const handleSubmitReview = async () => {
  if (!taskId.value) return
  
  try {
    // 检查任务状态，如果不是completed，提示用户先保存
    if (taskStatus.value !== 'completed') {
      await ElMessageBox.confirm(
        '请先保存标注结果，然后再提交复核。',
        '提示',
        { 
          type: 'warning',
          confirmButtonText: '保存并提交',
          cancelButtonText: '取消'
        }
      )
      
      // 先保存
      await handleSave()
    }
    
    // 确认提交
    await ElMessageBox.confirm(
      '确定要提交复核吗？提交后将无法继续编辑。',
      '提示',
      { type: 'warning' }
    )

    // 调用API提交复核
    console.log('[AnnotationPage] 开始提交复核, taskId:', taskId.value)
    const response = await reviewApi.submit(taskId.value)
    
    console.log('[AnnotationPage] 提交复核响应:', response)
    
    if (response.data || response.review_id) {
      taskStatus.value = 'under_review'
      ElMessage.success('提交复核成功')
      
      // 重新加载任务数据
      await loadTaskData()
      
      // 可选：跳转到复核列表
      // router.push({ name: 'review' })
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('提交复核失败:', error)
      console.error('错误详情:', error.response?.data)
      ElMessage.error(error.response?.data?.detail || error.message || '提交复核失败')
    }
  }
}

// 版本回滚
const handleRollback = async (versionId: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要回滚到此版本吗？当前未保存的修改将丢失。',
      '警告',
      { type: 'warning' }
    )

    // TODO: 调用API回滚版本
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('回滚成功')
    // 重新加载数据
  } catch (error) {
    // 用户取消
  }
}

// 刷新版本列表
const refreshVersions = () => {
  // TODO: 调用API刷新版本列表
  ElMessage.success('刷新成功')
}

// 返回
const goBack = () => {
  router.back()
}

// 跳转到复核页面
const goToReview = async () => {
  try {
    console.log('[AnnotationPage] 查找复核任务, taskId:', taskId.value)
    
    // 查询该任务的复核记录
    const response = await reviewApi.list({ 
      skip: 0, 
      limit: 100 
    })
    
    console.log('[AnnotationPage] 复核列表API响应:', response)
    
    // 后端直接返回数组，不是 { data: [...] } 格式
    const reviews = Array.isArray(response) ? response : (response.data || [])
    console.log('[AnnotationPage] 复核任务列表:', reviews)
    console.log('[AnnotationPage] 当前taskId:', taskId.value)
    
    const review = reviews.find((r: any) => {
      console.log('[AnnotationPage] 比较:', r.task_id, '===', taskId.value, '?', r.task_id === taskId.value)
      return r.task_id === taskId.value
    })
    
    if (review) {
      console.log('[AnnotationPage] 找到复核任务:', review)
      router.push({ name: 'review-detail', params: { reviewId: review.review_id } })
    } else {
      console.warn('[AnnotationPage] 未找到对应的复核任务')
      ElMessage.warning('未找到对应的复核任务')
      router.push({ name: 'review' })
    }
  } catch (error) {
    console.error('跳转失败:', error)
    router.push({ name: 'review' })
  }
}

// 状态相关
const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    pending: 'info',
    in_progress: 'warning',
    annotating: 'warning',
    reviewing: 'primary',
    approved: 'success',
    rejected: 'danger',
    completed: 'success'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '待标注',
    in_progress: '标注中',
    annotating: '标注中',
    under_review: '复核中',
    reviewing: '复核中',
    approved: '已通过',
    rejected: '已驳回',
    completed: '已完成'
  }
  return textMap[status] || '未知'
}

const formatTime = (time: string) => {
  return time.split(' ')[1] // 只显示时间部分
}

const formatDateTime = (dateTime: string) => {
  if (!dateTime) return '-'
  try {
    const date = new Date(dateTime)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch {
    return dateTime
  }
}
</script>
⋮----
<style scoped>
.annotation-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #dcdfe6;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.page-content {
  flex: 1;
  display: flex;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
}

.readonly-alert {
  flex-shrink: 0;
}

.editor-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.editor-tabs {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.editor-tabs :deep(.el-tabs__content) {
  flex: 1;
  overflow: hidden;
}

.editor-tabs :deep(.el-tab-pane) {
  height: 100%;
}

.info-panel {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
}

.info-card {
  flex-shrink: 0;
}

.rejection-history-card {
  border-color: #e6a23c;
}

.rejection-item {
  padding: 8px 0;
}

.rejection-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
}

.rejection-round {
  font-weight: 600;
  color: #e6a23c;
}

.rejection-reviewer {
  color: #909399;
}

.rejection-comment {
  padding: 12px;
  background: #fdf6ec;
  border-left: 3px solid #e6a23c;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
  white-space: pre-wrap;
  word-break: break-word;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-item,
.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child,
.stat-item:last-child {
  border-bottom: none;
}

.label,
.stat-label {
  color: #909399;
  font-size: 14px;
}

.value,
.stat-value {
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

.version-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.version-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  transition: all 0.2s;
}

.version-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.version-item.current {
  border-color: #67c23a;
  background-color: #f0f9ff;
}

.version-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.version-number {
  font-weight: 500;
  color: #303133;
}

.version-time {
  font-size: 12px;
  color: #909399;
}

.shortcut-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.shortcut-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.shortcut-item kbd {
  padding: 4px 8px;
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
}

.annotation-guide {
  margin-top: 8px;
}

.annotation-guide h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.guide-item {
  margin-bottom: 16px;
}

.guide-item:last-child {
  margin-bottom: 0;
}

.guide-item strong {
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
  color: #606266;
}

.guide-item p {
  margin: 0;
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
}

.guide-item kbd {
  padding: 2px 6px;
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  font-size: 11px;
  font-family: monospace;
}
</style>
````

## File: frontend/src/views/annotation/ImageAnnotationDemo.vue
````vue
<template>
  <div class="image-annotation-demo">
    <div class="page-header">
      <h2>图片标注编辑器</h2>
      <div class="actions">
        <el-button @click="handleSave">保存</el-button>
        <el-button type="primary" @click="handleSubmit">提交复核</el-button>
      </div>
    </div>

    <div class="editor-container">
      <ImageAnnotationEditor
        :image-url="sampleImageUrl"
        :whole-image-entities="wholeImageEntities"
        :bboxes="bboxes"
        :entity-types="entityTypes"
        @add-whole-image-entity="handleAddWholeImageEntity"
        @delete-whole-image-entity="handleDeleteWholeImageEntity"
        @add-bbox="handleAddBBox"
        @update-bbox="handleUpdateBBox"
        @delete-bbox="handleDeleteBBox"
      />
    </div>
  </div>
</template>
⋮----
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import ImageAnnotationEditor from '@/components/annotation/ImageAnnotationEditor.vue'
import { useLabelStore } from '@/stores/label'
import type { EntityType } from '@/api/label'

interface ImageEntity {
  id?: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface BoundingBox {
  id?: number
  x: number
  y: number
  width: number
  height: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

const labelStore = useLabelStore()

// 示例图片URL（可以替换为实际图片）
const sampleImageUrl = ref('https://via.placeholder.com/800x600/e3f2fd/2196f3?text=Sample+Image')

const wholeImageEntities = ref<ImageEntity[]>([])
const bboxes = ref<BoundingBox[]>([])
const entityTypes = ref<EntityType[]>([])
let nextWholeImageEntityId = 1
let nextBBoxId = 1

// 加载标签配置
onMounted(async () => {
  try {
    await labelStore.fetchEntityTypes({ include_inactive: false })
    entityTypes.value = labelStore.entityTypes
  } catch (error) {
    ElMessage.error('加载标签配置失败')
  }
})

const handleAddWholeImageEntity = (entity: Omit<ImageEntity, 'id'>) => {
  const newEntity: ImageEntity = {
    ...entity,
    id: nextWholeImageEntityId++
  }
  wholeImageEntities.value.push(newEntity)
}

const handleDeleteWholeImageEntity = (id: number) => {
  wholeImageEntities.value = wholeImageEntities.value.filter(e => e.id !== id)
}

const handleAddBBox = (bbox: Omit<BoundingBox, 'id'>) => {
  const newBBox: BoundingBox = {
    ...bbox,
    id: nextBBoxId++
  }
  bboxes.value.push(newBBox)
}

const handleUpdateBBox = (id: number, updates: Partial<BoundingBox>) => {
  const index = bboxes.value.findIndex(b => b.id === id)
  if (index !== -1) {
    bboxes.value[index] = { ...bboxes.value[index], ...updates }
  }
}

const handleDeleteBBox = (id: number) => {
  bboxes.value = bboxes.value.filter(b => b.id !== id)
}

const handleSave = () => {
  ElMessage.success('保存成功')
  console.log('Whole Image Entities:', wholeImageEntities.value)
  console.log('Bounding Boxes:', bboxes.value)
}

const handleSubmit = () => {
  ElMessage.success('提交复核成功')
}
</script>
⋮----
<style scoped>
.image-annotation-demo {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 10px;
}

.editor-container {
  flex: 1;
  overflow: hidden;
}
</style>
````

## File: frontend/src/views/corpus/CorpusManagement.vue
````vue
<template>
  <div class="corpus-management">
    <div class="page-header">
      <div class="header-left">
        <h2>语料管理</h2>
        <p class="page-desc">查看和管理已导入的语料记录</p>
      </div>
      <div class="header-right">
        <el-radio-group v-model="viewMode" size="default">
          <el-radio-button value="list">列表视图</el-radio-button>
          <el-radio-button value="grouped">分组视图</el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <el-card class="upload-redirect-card" shadow="never">
      <el-alert
        type="info"
        :closable="false"
        show-icon
      >
        <template #title>
          如需上传新的品质失效案例Excel，请前往
          <el-button type="primary" link @click="router.push('/document/import')">
            文档导入
          </el-button>
          页面
        </template>
      </el-alert>
    </el-card>

    <el-card class="preview-card">
      <template #header>
        <div class="card-header">
          <span>{{ viewMode === 'grouped' ? '语料分组（按Excel行）' : '语料列表' }}</span>
          <el-button
            type="primary"
            :icon="Refresh"
            @click="handleRefresh"
          >
            刷新
          </el-button>
        </div>
      </template>
      
      <!-- 列表视图 -->
      <CorpusPreview v-if="viewMode === 'list'" ref="corpusPreviewRef" />
      
      <!-- 分组视图 -->
      <CorpusGroupedView v-else ref="corpusGroupedRef" />
    </el-card>
  </div>
</template>
⋮----
<template #title>
          如需上传新的品质失效案例Excel，请前往
          <el-button type="primary" link @click="router.push('/document/import')">
            文档导入
          </el-button>
          页面
        </template>
⋮----
<template #header>
        <div class="card-header">
          <span>{{ viewMode === 'grouped' ? '语料分组（按Excel行）' : '语料列表' }}</span>
          <el-button
            type="primary"
            :icon="Refresh"
            @click="handleRefresh"
          >
            刷新
          </el-button>
        </div>
      </template>
⋮----
<span>{{ viewMode === 'grouped' ? '语料分组（按Excel行）' : '语料列表' }}</span>
⋮----
<!-- 列表视图 -->
⋮----
<!-- 分组视图 -->
⋮----
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Refresh } from '@element-plus/icons-vue'
import CorpusPreview from '@/components/corpus/CorpusPreview.vue'
import CorpusGroupedView from '@/components/corpus/CorpusGroupedView.vue'

const router = useRouter()

const corpusPreviewRef = ref()
const corpusGroupedRef = ref()
const viewMode = ref<'list' | 'grouped'>('grouped')  // 默认使用分组视图

const handleRefresh = () => {
  if (viewMode.value === 'list' && corpusPreviewRef.value) {
    corpusPreviewRef.value.refresh()
  } else if (viewMode.value === 'grouped' && corpusGroupedRef.value) {
    corpusGroupedRef.value.refresh()
  }
}
</script>
⋮----
<style scoped lang="scss">
.corpus-management {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;

    .header-left {
      h2 {
        margin: 0 0 8px;
        font-size: 24px;
        color: #303133;
      }

      .page-desc {
        margin: 0;
        font-size: 14px;
        color: #909399;
      }
    }

    .header-right {
      display: flex;
      align-items: center;
    }
  }

  .upload-redirect-card {
    margin-bottom: 20px;
  }

  .preview-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }
  }
}
</style>
````

## File: frontend/src/views/dataset/DatasetAssignment.vue
````vue
<template>
  <div class="dataset-assignment-container">
    <el-page-header @back="goBack" :content="`数据集分配管理 - ${datasetName}`" />

    <el-card class="assignment-card">
      <template #header>
        <div class="card-header">
          <span>{{ isPlanning ? '分配规划（未提交）' : '分配情况' }}</span>
          <div class="actions">
            <template v-if="!isPlanning">
              <el-button type="primary" @click="enterPlanningMode">
                <el-icon><Edit /></el-icon>
                开始规划
              </el-button>
              <el-button 
                type="warning" 
                @click="handleClearAssignments"
                :disabled="assignments.length === 0"
              >
                <el-icon><Delete /></el-icon>
                清空分配
              </el-button>
              <el-button @click="loadAssignments">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </template>
            <template v-else>
              <el-button type="success" @click="showAutoAssignDialog">
                <el-icon><MagicStick /></el-icon>
                自动分配
              </el-button>
              <el-button @click="clearPlanning">
                <el-icon><Delete /></el-icon>
                清空规划
              </el-button>
              <el-button @click="cancelPlanning">
                取消
              </el-button>
              <el-button 
                type="primary" 
                @click="submitPlanning"
                :loading="submitting"
              >
                <el-icon><Check /></el-icon>
                确认提交
              </el-button>
            </template>
          </div>
        </div>
      </template>

      <!-- 统计信息 -->
      <div class="stats">
        <el-statistic title="总任务数" :value="stats.total_tasks" />
        <el-statistic title="已分配" :value="stats.total_tasks - stats.unassigned_count" />
        <el-statistic title="未分配" :value="stats.unassigned_count" />
        <el-statistic title="标注员" :value="stats.annotator_count" />
        <el-statistic title="复核员" :value="stats.reviewer_count" />
      </div>

      <!-- 规划模式提示 -->
      <el-alert
        v-if="isPlanning"
        title="规划模式"
        type="info"
        :closable="false"
        style="margin-top: 20px"
      >
        <template #default>
          <div>
            <p>当前处于规划模式，所有更改不会立即生效。</p>
            <p>您可以：</p>
            <ul style="margin: 8px 0; padding-left: 20px;">
              <li>使用"自动分配"快速生成分配方案</li>
              <li>使用 +1/+10/-1/-10 按钮调整每个用户的任务数量</li>
              <li>删除不需要的分配</li>
              <li>点击"确认提交"保存所有更改</li>
            </ul>
            <div v-if="plans.length > 0" style="margin-top: 8px;">
              <div v-if="detectConflicts().length > 0" style="color: #f56c6c;">
                ❌ 检测到 {{ detectConflicts().length }} 个任务冲突，无法提交
              </div>
              <div v-else>
                <div v-if="plans.some(p => p.role === 'annotator')">
                  <span v-if="getUnassignedTasks('annotator').length > 0" style="color: #e6a23c;">
                    ⚠️ 标注员：还有 {{ getUnassignedTasks('annotator').length }} 个任务未分配
                  </span>
                  <span v-else style="color: #67c23a;">
                    ✓ 标注员：所有任务已分配
                  </span>
                </div>
                <div v-if="plans.some(p => p.role === 'reviewer')">
                  <span v-if="getUnassignedTasks('reviewer').length > 0" style="color: #e6a23c;">
                    ⚠️ 复核员：还有 {{ getUnassignedTasks('reviewer').length }} 个任务未分配
                  </span>
                  <span v-else style="color: #67c23a;">
                    ✓ 复核员：所有任务已分配
                  </span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </el-alert>

      <!-- 无任务提示 -->
      <el-alert
        v-if="stats.total_tasks === 0"
        title="该数据集还没有任务"
        type="warning"
        description="请先创建数据集并添加任务后再进行分配。数据集需要包含标注任务才能分配给标注员或复核员。"
        :closable="false"
        style="margin-top: 20px"
      />

      <!-- 任务覆盖可视化 -->
      <div v-if="stats.total_tasks > 0 && assignments.length > 0" class="task-coverage">
        <div class="coverage-title">任务分配可视化</div>
        
        <!-- 标注员可视化 -->
        <div v-if="annotatorAssignments.length > 0" class="coverage-section">
          <div class="coverage-section-title">
            <el-tag type="success" size="small">标注员</el-tag>
            <span class="coverage-count">{{ stats.annotator_count }} 人</span>
          </div>
          <div class="coverage-container">
            <div class="coverage-bar">
              <div 
                v-for="assignment in annotatorAssignments" 
                :key="assignment.assignment_id"
                :style="getCoverageStyle(assignment)"
                :class="['coverage-segment', 'role-annotator']"
                :title="`${assignment.username} (${assignment.task_range})`"
              >
                <span class="coverage-label">{{ assignment.username }}</span>
              </div>
            </div>
            <div class="coverage-legend">
              <span class="legend-start">任务 1</span>
              <span class="legend-end">任务 {{ stats.total_tasks }}</span>
            </div>
          </div>
        </div>

        <!-- 复核员可视化 -->
        <div v-if="reviewerAssignments.length > 0" class="coverage-section">
          <div class="coverage-section-title">
            <el-tag type="warning" size="small">复核员</el-tag>
            <span class="coverage-count">{{ stats.reviewer_count }} 人</span>
          </div>
          <div class="coverage-container">
            <div class="coverage-bar">
              <div 
                v-for="assignment in reviewerAssignments" 
                :key="assignment.assignment_id"
                :style="getCoverageStyle(assignment)"
                :class="['coverage-segment', 'role-reviewer']"
                :title="`${assignment.username} (${assignment.task_range})`"
              >
                <span class="coverage-label">{{ assignment.username }}</span>
              </div>
            </div>
            <div class="coverage-legend">
              <span class="legend-start">任务 1</span>
              <span class="legend-end">任务 {{ stats.total_tasks }}</span>
            </div>
          </div>
        </div>

        <!-- 统计信息 -->
        <div class="coverage-stats">
          <el-tag type="success">标注员: {{ stats.annotator_count }}</el-tag>
          <el-tag type="warning">复核员: {{ stats.reviewer_count }}</el-tag>
          <el-tag v-if="stats.unassigned_count > 0" type="info">
            未分配: {{ stats.unassigned_count }}
          </el-tag>
          <el-tag v-else type="success">
            <el-icon><Check /></el-icon> 全部已分配
          </el-tag>
        </div>
      </div>

      <!-- 分配列表 -->
      <el-table
        v-loading="loading"
        :data="displayAssignments"
        style="width: 100%; margin-top: 20px"
      >
        <el-table-column prop="username" label="用户" width="150">
          <template #default="{ row }">
            {{ row.username }}
            <el-tag v-if="row.isNew" type="success" size="small" style="margin-left: 8px;">新增</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.role === 'annotator'" type="success">标注员</el-tag>
            <el-tag v-else type="warning">复核员</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="task_range" label="任务范围" width="150" />
        <el-table-column prop="task_count" label="任务数" width="100" />

        <el-table-column v-if="!isPlanning" label="进度" width="200">
          <template #default="{ row }">
            <div class="progress-info">
              <el-progress
                :percentage="getProgress(row)"
                :color="getProgressColor(row)"
              />
              <span class="progress-text">
                已完成: {{ row.completed_count }} | 复核中: {{ row.in_review_count }}
              </span>
            </div>
          </template>
        </el-table-column>

        <el-table-column v-if="!isPlanning" prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.is_active" type="success">活跃</el-tag>
            <el-tag v-else type="info">已转移</el-tag>
          </template>
        </el-table-column>

        <el-table-column v-if="!isPlanning" label="转移信息" min-width="200">
          <template #default="{ row }">
            <div v-if="!row.is_active && row.transferred_to">
              <div>转移给: {{ row.transferred_to_username }}</div>
              <div class="text-secondary">{{ row.transfer_reason }}</div>
            </div>
            <span v-else>-</span>
          </template>
        </el-table-column>

        <el-table-column v-if="!isPlanning" prop="assigned_at" label="分配时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.assigned_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <template v-if="isPlanning">
              <el-button-group v-if="row.task_range !== '全部'">
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, -10)"
                >
                  -10
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, -1)"
                >
                  -1
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, 1)"
                >
                  +1
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, 10)"
                >
                  +10
                </el-button>
              </el-button-group>
              <el-button
                type="danger"
                size="small"
                @click="deletePlanItem(row.assignment_id)"
                style="margin-left: 8px;"
              >
                删除
              </el-button>
            </template>
            <template v-else>
              <el-button
                v-if="row.is_active"
                type="warning"
                size="small"
                @click="showTransferDialog(row)"
              >
                转移
              </el-button>
              <el-button
                v-if="row.is_active"
                type="danger"
                size="small"
                @click="handleCancel(row)"
              >
                取消
              </el-button>
            </template>
          </template>
        </el-table-column>

        <template #empty>
          <el-empty :description="isPlanning ? '暂无规划，点击上方按钮开始规划' : '暂无分配记录，点击【开始规划】按钮开始分配'" />
        </template>
      </el-table>
    </el-card>

    <!-- 分配对话框 -->
    <el-dialog
      v-model="assignDialogVisible"
      title="分配数据集"
      width="500px"
    >
      <el-form :model="assignForm" label-width="100px">
        <el-form-item label="角色">
          <el-radio-group v-model="assignForm.role">
            <el-radio value="annotator">标注员</el-radio>
            <el-radio value="reviewer">复核员</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="用户">
          <el-select v-model="assignForm.user_id" placeholder="请选择用户" filterable>
            <el-option
              v-for="user in availableUsers"
              :key="user.id"
              :label="`${user.username} (${getRoleLabel(user.role)})`"
              :value="user.id"
            />
          </el-select>
          <div v-if="availableUsers.length === 0" style="color: #909399; font-size: 12px; margin-top: 4px;">
            所有用户都已分配为{{ assignForm.role === 'annotator' ? '标注员' : '复核员' }}
          </div>
        </el-form-item>

        <el-form-item label="分配模式">
          <el-radio-group v-model="assignForm.mode">
            <el-radio value="full">整体分配</el-radio>
            <el-radio value="range">范围分配</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="assignForm.mode === 'range'" label="起始索引">
          <el-input-number v-model="assignForm.start_index" :min="1" :max="stats.total_tasks" />
        </el-form-item>

        <el-form-item v-if="assignForm.mode === 'range'" label="结束索引">
          <el-input-number v-model="assignForm.end_index" :min="1" :max="stats.total_tasks" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="assignDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAssign" :loading="submitting" :disabled="availableUsers.length === 0">确定</el-button>
      </template>
    </el-dialog>

    <!-- 自动分配对话框 -->
    <el-dialog
      v-model="autoAssignDialogVisible"
      title="自动分配"
      width="500px"
    >
      <el-form :model="autoAssignForm" label-width="100px">
        <el-form-item label="角色">
          <el-radio-group v-model="autoAssignForm.role">
            <el-radio value="annotator">标注员</el-radio>
            <el-radio value="reviewer">复核员</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="选择用户">
          <el-select
            v-model="autoAssignForm.user_ids"
            multiple
            placeholder="请选择用户"
            filterable
          >
            <el-option
              v-for="user in availableUsers"
              :key="user.id"
              :label="`${user.username} (${getRoleLabel(user.role)})`"
              :value="user.id"
            />
          </el-select>
          <div v-if="availableUsers.length === 0" style="color: #909399; font-size: 12px; margin-top: 4px;">
            所有用户都已分配为{{ autoAssignForm.role === 'annotator' ? '标注员' : '复核员' }}
          </div>
        </el-form-item>

        <el-alert
          title="自动分配将平均分配任务给选中的用户"
          type="info"
          :closable="false"
          style="margin-top: 10px"
        />
      </el-form>

      <template #footer>
        <el-button @click="autoAssignDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAutoAssign" :loading="submitting" :disabled="availableUsers.length === 0">确定</el-button>
      </template>
    </el-dialog>

    <!-- 转移对话框 -->
    <el-dialog
      v-model="transferDialogVisible"
      title="转移分配"
      width="500px"
    >
      <el-form :model="transferForm" label-width="100px">
        <el-form-item label="原用户">
          <el-input :value="currentAssignment?.username" disabled />
        </el-form-item>

        <el-form-item label="新用户">
          <el-select v-model="transferForm.new_user_id" placeholder="请选择用户" filterable>
            <el-option
              v-for="user in availableUsers"
              :key="user.id"
              :label="`${user.username} (${getRoleLabel(user.role)})`"
              :value="user.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="转移原因">
          <el-input
            v-model="transferForm.transfer_reason"
            type="textarea"
            :rows="3"
            placeholder="请输入转移原因"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="transferDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleTransfer" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>
⋮----
<template #header>
        <div class="card-header">
          <span>{{ isPlanning ? '分配规划（未提交）' : '分配情况' }}</span>
          <div class="actions">
            <template v-if="!isPlanning">
              <el-button type="primary" @click="enterPlanningMode">
                <el-icon><Edit /></el-icon>
                开始规划
              </el-button>
              <el-button 
                type="warning" 
                @click="handleClearAssignments"
                :disabled="assignments.length === 0"
              >
                <el-icon><Delete /></el-icon>
                清空分配
              </el-button>
              <el-button @click="loadAssignments">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </template>
            <template v-else>
              <el-button type="success" @click="showAutoAssignDialog">
                <el-icon><MagicStick /></el-icon>
                自动分配
              </el-button>
              <el-button @click="clearPlanning">
                <el-icon><Delete /></el-icon>
                清空规划
              </el-button>
              <el-button @click="cancelPlanning">
                取消
              </el-button>
              <el-button 
                type="primary" 
                @click="submitPlanning"
                :loading="submitting"
              >
                <el-icon><Check /></el-icon>
                确认提交
              </el-button>
            </template>
          </div>
        </div>
      </template>
⋮----
<span>{{ isPlanning ? '分配规划（未提交）' : '分配情况' }}</span>
⋮----
<template v-if="!isPlanning">
              <el-button type="primary" @click="enterPlanningMode">
                <el-icon><Edit /></el-icon>
                开始规划
              </el-button>
              <el-button 
                type="warning" 
                @click="handleClearAssignments"
                :disabled="assignments.length === 0"
              >
                <el-icon><Delete /></el-icon>
                清空分配
              </el-button>
              <el-button @click="loadAssignments">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </template>
<template v-else>
              <el-button type="success" @click="showAutoAssignDialog">
                <el-icon><MagicStick /></el-icon>
                自动分配
              </el-button>
              <el-button @click="clearPlanning">
                <el-icon><Delete /></el-icon>
                清空规划
              </el-button>
              <el-button @click="cancelPlanning">
                取消
              </el-button>
              <el-button 
                type="primary" 
                @click="submitPlanning"
                :loading="submitting"
              >
                <el-icon><Check /></el-icon>
                确认提交
              </el-button>
            </template>
⋮----
<!-- 统计信息 -->
⋮----
<!-- 规划模式提示 -->
⋮----
<template #default>
          <div>
            <p>当前处于规划模式，所有更改不会立即生效。</p>
            <p>您可以：</p>
            <ul style="margin: 8px 0; padding-left: 20px;">
              <li>使用"自动分配"快速生成分配方案</li>
              <li>使用 +1/+10/-1/-10 按钮调整每个用户的任务数量</li>
              <li>删除不需要的分配</li>
              <li>点击"确认提交"保存所有更改</li>
            </ul>
            <div v-if="plans.length > 0" style="margin-top: 8px;">
              <div v-if="detectConflicts().length > 0" style="color: #f56c6c;">
                ❌ 检测到 {{ detectConflicts().length }} 个任务冲突，无法提交
              </div>
              <div v-else>
                <div v-if="plans.some(p => p.role === 'annotator')">
                  <span v-if="getUnassignedTasks('annotator').length > 0" style="color: #e6a23c;">
                    ⚠️ 标注员：还有 {{ getUnassignedTasks('annotator').length }} 个任务未分配
                  </span>
                  <span v-else style="color: #67c23a;">
                    ✓ 标注员：所有任务已分配
                  </span>
                </div>
                <div v-if="plans.some(p => p.role === 'reviewer')">
                  <span v-if="getUnassignedTasks('reviewer').length > 0" style="color: #e6a23c;">
                    ⚠️ 复核员：还有 {{ getUnassignedTasks('reviewer').length }} 个任务未分配
                  </span>
                  <span v-else style="color: #67c23a;">
                    ✓ 复核员：所有任务已分配
                  </span>
                </div>
              </div>
            </div>
          </div>
        </template>
⋮----
❌ 检测到 {{ detectConflicts().length }} 个任务冲突，无法提交
⋮----
⚠️ 标注员：还有 {{ getUnassignedTasks('annotator').length }} 个任务未分配
⋮----
⚠️ 复核员：还有 {{ getUnassignedTasks('reviewer').length }} 个任务未分配
⋮----
<!-- 无任务提示 -->
⋮----
<!-- 任务覆盖可视化 -->
⋮----
<!-- 标注员可视化 -->
⋮----
<span class="coverage-count">{{ stats.annotator_count }} 人</span>
⋮----
<span class="coverage-label">{{ assignment.username }}</span>
⋮----
<span class="legend-end">任务 {{ stats.total_tasks }}</span>
⋮----
<!-- 复核员可视化 -->
⋮----
<span class="coverage-count">{{ stats.reviewer_count }} 人</span>
⋮----
<span class="coverage-label">{{ assignment.username }}</span>
⋮----
<span class="legend-end">任务 {{ stats.total_tasks }}</span>
⋮----
<!-- 统计信息 -->
⋮----
<el-tag type="success">标注员: {{ stats.annotator_count }}</el-tag>
<el-tag type="warning">复核员: {{ stats.reviewer_count }}</el-tag>
⋮----
未分配: {{ stats.unassigned_count }}
⋮----
<!-- 分配列表 -->
⋮----
<template #default="{ row }">
            {{ row.username }}
            <el-tag v-if="row.isNew" type="success" size="small" style="margin-left: 8px;">新增</el-tag>
          </template>
⋮----
{{ row.username }}
⋮----
<template #default="{ row }">
            <el-tag v-if="row.role === 'annotator'" type="success">标注员</el-tag>
            <el-tag v-else type="warning">复核员</el-tag>
          </template>
⋮----
<template #default="{ row }">
            <div class="progress-info">
              <el-progress
                :percentage="getProgress(row)"
                :color="getProgressColor(row)"
              />
              <span class="progress-text">
                已完成: {{ row.completed_count }} | 复核中: {{ row.in_review_count }}
              </span>
            </div>
          </template>
⋮----
已完成: {{ row.completed_count }} | 复核中: {{ row.in_review_count }}
⋮----
<template #default="{ row }">
            <el-tag v-if="row.is_active" type="success">活跃</el-tag>
            <el-tag v-else type="info">已转移</el-tag>
          </template>
⋮----
<template #default="{ row }">
            <div v-if="!row.is_active && row.transferred_to">
              <div>转移给: {{ row.transferred_to_username }}</div>
              <div class="text-secondary">{{ row.transfer_reason }}</div>
            </div>
            <span v-else>-</span>
          </template>
⋮----
<div>转移给: {{ row.transferred_to_username }}</div>
<div class="text-secondary">{{ row.transfer_reason }}</div>
⋮----
<template #default="{ row }">
            {{ formatDate(row.assigned_at) }}
          </template>
⋮----
{{ formatDate(row.assigned_at) }}
⋮----
<template #default="{ row }">
            <template v-if="isPlanning">
              <el-button-group v-if="row.task_range !== '全部'">
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, -10)"
                >
                  -10
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, -1)"
                >
                  -1
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, 1)"
                >
                  +1
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, 10)"
                >
                  +10
                </el-button>
              </el-button-group>
              <el-button
                type="danger"
                size="small"
                @click="deletePlanItem(row.assignment_id)"
                style="margin-left: 8px;"
              >
                删除
              </el-button>
            </template>
            <template v-else>
              <el-button
                v-if="row.is_active"
                type="warning"
                size="small"
                @click="showTransferDialog(row)"
              >
                转移
              </el-button>
              <el-button
                v-if="row.is_active"
                type="danger"
                size="small"
                @click="handleCancel(row)"
              >
                取消
              </el-button>
            </template>
          </template>
⋮----
<template v-if="isPlanning">
              <el-button-group v-if="row.task_range !== '全部'">
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, -10)"
                >
                  -10
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, -1)"
                >
                  -1
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, 1)"
                >
                  +1
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, 10)"
                >
                  +10
                </el-button>
              </el-button-group>
              <el-button
                type="danger"
                size="small"
                @click="deletePlanItem(row.assignment_id)"
                style="margin-left: 8px;"
              >
                删除
              </el-button>
            </template>
<template v-else>
              <el-button
                v-if="row.is_active"
                type="warning"
                size="small"
                @click="showTransferDialog(row)"
              >
                转移
              </el-button>
              <el-button
                v-if="row.is_active"
                type="danger"
                size="small"
                @click="handleCancel(row)"
              >
                取消
              </el-button>
            </template>
⋮----
<template #empty>
          <el-empty :description="isPlanning ? '暂无规划，点击上方按钮开始规划' : '暂无分配记录，点击【开始规划】按钮开始分配'" />
        </template>
⋮----
<!-- 分配对话框 -->
⋮----
所有用户都已分配为{{ assignForm.role === 'annotator' ? '标注员' : '复核员' }}
⋮----
<template #footer>
        <el-button @click="assignDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAssign" :loading="submitting" :disabled="availableUsers.length === 0">确定</el-button>
      </template>
⋮----
<!-- 自动分配对话框 -->
⋮----
所有用户都已分配为{{ autoAssignForm.role === 'annotator' ? '标注员' : '复核员' }}
⋮----
<template #footer>
        <el-button @click="autoAssignDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAutoAssign" :loading="submitting" :disabled="availableUsers.length === 0">确定</el-button>
      </template>
⋮----
<!-- 转移对话框 -->
⋮----
<template #footer>
        <el-button @click="transferDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleTransfer" :loading="submitting">确定</el-button>
      </template>
⋮----
<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { h } from 'vue'
import { Plus, MagicStick, Refresh, Delete, Check, Edit } from '@element-plus/icons-vue'
import { datasetApi } from '@/api/dataset'
import { userApi } from '@/api/user'
import type { AssignmentInfo } from '@/types/assignment'
import type { User } from '@/types'

const route = useRoute()
const router = useRouter()

// 数据集ID
const datasetId = computed(() => route.params.id as string)

// 状态
const loading = ref(false)
const submitting = ref(false)
const datasetName = ref('')
const assignments = ref<AssignmentInfo[]>([])
const stats = ref({
  total_tasks: 0,
  unassigned_count: 0,
  annotator_count: 0,
  reviewer_count: 0
})

// 规划模式状态
interface AssignmentPlan {
  id: string
  user_id: number
  username: string
  role: 'annotator' | 'reviewer'
  mode: 'full' | 'range'
  start_index?: number
  end_index?: number
  task_count: number
  isNew: boolean
}

const isPlanning = ref(false)
const plans = ref<AssignmentPlan[]>([])
const originalAssignments = ref<AssignmentInfo[]>([])

// 对话框
const assignDialogVisible = ref(false)
const autoAssignDialogVisible = ref(false)
const transferDialogVisible = ref(false)

// 表单
const assignForm = ref({
  user_id: null as number | null,
  role: 'annotator' as 'annotator' | 'reviewer',
  mode: 'full' as 'full' | 'range',
  start_index: 1,
  end_index: 1
})

const autoAssignForm = ref({
  user_ids: [] as number[],
  role: 'annotator' as 'annotator' | 'reviewer'
})

const transferForm = ref({
  new_user_id: null as number | null,
  transfer_reason: ''
})

const currentAssignment = ref<AssignmentInfo | null>(null)

// 可用用户列表
const availableUsers = ref<User[]>([])
// 所有用户列表（用于过滤）
const allUsers = ref<User[]>([])

// 活跃分配列表
const activeAssignments = computed(() => {
  if (isPlanning.value) {
    return plans.value.filter(p => !p.isNew || p.user_id)
  }
  return assignments.value.filter(a => a.is_active)
})

// 标注员分配列表
const annotatorAssignments = computed(() => {
  return activeAssignments.value.filter(a => a.role === 'annotator')
})

// 复核员分配列表
const reviewerAssignments = computed(() => {
  return activeAssignments.value.filter(a => a.role === 'reviewer')
})

// 显示的分配列表（规划模式显示plans，否则显示assignments）
const displayAssignments = computed(() => {
  if (isPlanning.value) {
    return plans.value.map(plan => ({
      assignment_id: plan.id,
      user_id: plan.user_id,
      username: plan.username,
      role: plan.role,
      task_range: plan.mode === 'full' ? '全部' : `${plan.start_index}-${plan.end_index}`,
      task_count: plan.task_count,
      completed_count: 0,
      in_review_count: 0,
      is_active: true,
      transferred_to: null,
      transferred_to_username: null,
      transferred_at: null,
      transfer_reason: null,
      assigned_by: null,
      assigned_at: new Date().toISOString(),
      isPlanning: true,
      isNew: plan.isNew
    }))
  }
  return assignments.value
})

// 已分配的用户ID集合（按角色区分）
const assignedUserIds = computed(() => {
  const annotators = new Set<number>()
  const reviewers = new Set<number>()
  
  assignments.value.forEach(assignment => {
    if (assignment.is_active) {
      if (assignment.role === 'annotator') {
        annotators.add(assignment.user_id)
      } else if (assignment.role === 'reviewer') {
        reviewers.add(assignment.user_id)
      }
    }
  })
  
  return { annotators, reviewers }
})

// 根据当前选择的角色过滤可用用户
const getAvailableUsersForRole = (role: 'annotator' | 'reviewer') => {
  const assigned = role === 'annotator' 
    ? assignedUserIds.value.annotators 
    : assignedUserIds.value.reviewers
  
  // 只显示标注员（annotator），并且排除已分配的用户
  return allUsers.value.filter(
    user => user.role === 'annotator' && !assigned.has(user.id)
  )
}

// 加载分配情况
const loadAssignments = async () => {
  loading.value = true
  try {
    const response = await datasetApi.getAssignments(datasetId.value)
    
    if (response.success) {
      const data = response.data
      assignments.value = data.assignments
      stats.value = {
        total_tasks: data.total_tasks,
        unassigned_count: data.unassigned_count,
        annotator_count: data.annotator_count,
        reviewer_count: data.reviewer_count
      }
      datasetName.value = data.dataset_name
    }
  } catch (error: any) {
    console.error('加载分配情况失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载分配情况失败')
  } finally {
    loading.value = false
  }
}

// 加载用户列表
const loadUsers = async () => {
  try {
    const users = await userApi.list()
    allUsers.value = Array.isArray(users) ? users : []
    availableUsers.value = allUsers.value.filter(
      (user: User) => user.role === 'annotator'
    )
    
    if (availableUsers.value.length === 0) {
      ElMessage.warning('没有可用的标注员，请先创建用户')
    }
  } catch (error: any) {
    console.error('加载用户列表失败', error)
    ElMessage.error(error.response?.data?.detail || '加载用户列表失败')
  }
}

// 显示分配对话框
const showAssignDialog = () => {
  // 检查数据集是否有任务
  if (stats.value.total_tasks === 0) {
    ElMessage.warning('该数据集没有任务，无法分配。请先添加任务到数据集。')
    return
  }
  
  assignForm.value = {
    user_id: null,
    role: 'annotator',
    mode: 'full',
    start_index: 1,
    end_index: stats.value.total_tasks
  }
  // 更新可用用户列表（过滤已分配的用户）
  availableUsers.value = getAvailableUsersForRole('annotator')
  assignDialogVisible.value = true
}

// 显示自动分配对话框
const showAutoAssignDialog = () => {
  // 检查数据集是否有任务
  if (stats.value.total_tasks === 0) {
    ElMessage.warning('该数据集没有任务，无法分配。请先添加任务到数据集。')
    return
  }
  
  // 如果不在规划模式，先进入规划模式
  if (!isPlanning.value) {
    enterPlanningMode()
  }
  
  autoAssignForm.value = {
    user_ids: [],
    role: 'annotator'
  }
  // 更新可用用户列表（过滤已分配的用户）
  availableUsers.value = getAvailableUsersForRole('annotator')
  autoAssignDialogVisible.value = true
}

// 显示转移对话框
const showTransferDialog = (assignment: AssignmentInfo) => {
  currentAssignment.value = assignment
  transferForm.value = {
    new_user_id: null,
    transfer_reason: ''
  }
  // 更新可用用户列表（过滤已分配的用户，但不包括当前用户）
  const assigned = assignment.role === 'annotator' 
    ? assignedUserIds.value.annotators 
    : assignedUserIds.value.reviewers
  
  availableUsers.value = allUsers.value.filter(
    user => user.role === 'annotator' && 
            (user.id === assignment.user_id || !assigned.has(user.id))
  )
  transferDialogVisible.value = true
}

// 处理分配
const handleAssign = async () => {
  if (!assignForm.value.user_id) {
    ElMessage.warning('请选择用户')
    return
  }

  // 检查数据集是否有任务
  if (stats.value.total_tasks === 0) {
    ElMessage.warning('该数据集没有任务，无法分配')
    return
  }

  // 在规划模式下，添加到规划列表
  if (isPlanning.value) {
    const user = allUsers.value.find(u => u.id === assignForm.value.user_id)
    if (!user) {
      ElMessage.error('用户不存在')
      return
    }
    
    const taskCount = assignForm.value.mode === 'full' 
      ? stats.value.total_tasks
      : (assignForm.value.end_index! - assignForm.value.start_index! + 1)
    
    addPlanItem({
      user_id: assignForm.value.user_id,
      username: user.username,
      role: assignForm.value.role,
      mode: assignForm.value.mode,
      start_index: assignForm.value.mode === 'range' ? assignForm.value.start_index : undefined,
      end_index: assignForm.value.mode === 'range' ? assignForm.value.end_index : undefined,
      task_count: taskCount
    })
    
    ElMessage.success('已添加到规划')
    assignDialogVisible.value = false
    return
  }

  // 非规划模式（旧逻辑）
  // 检查是否重复分配
  const existingAssignment = assignments.value.find(
    a => a.user_id === assignForm.value.user_id && 
         a.role === assignForm.value.role && 
         a.is_active
  )
  
  if (existingAssignment) {
    ElMessage.warning(`该用户已被分配为${assignForm.value.role === 'annotator' ? '标注员' : '复核员'}`)
    return
  }

  // 范围模式验证
  if (assignForm.value.mode === 'range') {
    if (!assignForm.value.start_index || !assignForm.value.end_index) {
      ElMessage.warning('请输入任务范围')
      return
    }
    if (assignForm.value.start_index < 1 || assignForm.value.end_index < assignForm.value.start_index) {
      ElMessage.warning('任务范围无效')
      return
    }
    if (assignForm.value.end_index > stats.value.total_tasks) {
      ElMessage.warning(`结束索引不能超过总任务数 ${stats.value.total_tasks}`)
      return
    }
  }

  submitting.value = true
  try {
    // 构建请求数据
    const requestData: any = {
      user_id: assignForm.value.user_id,
      role: assignForm.value.role,
      mode: assignForm.value.mode
    }
    
    // 只在范围模式下发送索引
    if (assignForm.value.mode === 'range') {
      requestData.start_index = assignForm.value.start_index
      requestData.end_index = assignForm.value.end_index
    }
    
    await datasetApi.assign(datasetId.value, requestData)
    ElMessage.success('分配成功')
    assignDialogVisible.value = false
    await loadAssignments()
  } catch (error: any) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') {
      ElMessage.error(detail)
    } else if (detail?.message) {
      ElMessage.error(detail.message)
    } else {
      ElMessage.error('分配失败')
    }
  } finally {
    submitting.value = false
  }
}

// 处理自动分配
const handleAutoAssign = async () => {
  if (autoAssignForm.value.user_ids.length === 0) {
    ElMessage.warning('请至少选择一个用户')
    return
  }

  // 在规划模式下，直接生成方案
  if (isPlanning.value) {
    await autoAssignInPlanning(autoAssignForm.value.user_ids, autoAssignForm.value.role)
    autoAssignDialogVisible.value = false
    return
  }

  // 非规划模式（旧逻辑，保留兼容）
  const existingCount = assignments.value.filter(
    a => a.is_active && a.role === autoAssignForm.value.role
  ).length

  const confirmMessageVNode = h('div', [
    h('div', '即将自动分配任务：'),
    h('div', [
      h('div', `- 选中用户：${autoAssignForm.value.user_ids.length} 个`),
      h('div', `- 角色：${autoAssignForm.value.role === 'annotator' ? '标注员' : '复核员'}`),
      h('div', `- 总任务数：${stats.value.total_tasks}`),
      h('div', `- 每人约：${Math.ceil(stats.value.total_tasks / autoAssignForm.value.user_ids.length)} 个任务`)
    ]),
    existingCount > 0 ? h('div', { style: 'color: #e6a23c; margin: 8px 0 0 0;' }, [
      `⚠️ 当前已有 ${existingCount} 个${autoAssignForm.value.role === 'annotator' ? '标注员' : '复核员'}分配，自动分配可能会与现有分配冲突。建议先清空现有分配。`
    ]) : null,
    h('div', { style: 'margin-top: 8px;' }, '确认自动分配吗？')
  ])
  try {
    await ElMessageBox.confirm(confirmMessageVNode, '确认自动分配', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info',
      distinguishCancelAndClose: true
    })

    submitting.value = true
    await datasetApi.autoAssign(datasetId.value, autoAssignForm.value as any)
    ElMessage.success('自动分配成功')
    autoAssignDialogVisible.value = false
    await loadAssignments()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('自动分配失败:', error)
      ElMessage.error(error.response?.data?.detail || '自动分配失败')
    }
  } finally {
    submitting.value = false
  }
}

// 处理转移
const handleTransfer = async () => {
  if (!transferForm.value.new_user_id) {
    ElMessage.warning('请选择新用户')
    return
  }

  if (!currentAssignment.value) return

  submitting.value = true
  try {
    await datasetApi.transferAssignment(datasetId.value, {
      old_user_id: currentAssignment.value.user_id,
      new_user_id: transferForm.value.new_user_id,
      role: currentAssignment.value.role as any,
      transfer_mode: 'all',
      transfer_reason: transferForm.value.transfer_reason
    })
    ElMessage.success('转移成功')
    transferDialogVisible.value = false
    loadAssignments()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '转移失败')
  } finally {
    submitting.value = false
  }
}

// 处理取消
const handleCancel = async (assignment: AssignmentInfo) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消用户 ${assignment.username} 的分配吗？`,
      '确认取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await datasetApi.cancelAssignment(
      datasetId.value,
      assignment.user_id,
      assignment.role
    )
    ElMessage.success('取消成功')
    loadAssignments()
  } catch (error: any) {
    if (error !== 'cancel') {
      const detail = error.response?.data?.detail
      if (typeof detail === 'object' && detail.action === 'transfer') {
        ElMessage.warning('该分配有已完成任务，请使用转移功能')
      } else {
        ElMessage.error(detail || '取消失败')
      }
    }
  }
}

// 批量清空分配
const handleClearAssignments = async () => {
  try {
    const activeCount = assignments.value.filter(a => a.is_active).length
    
    if (activeCount === 0) {
      ElMessage.info('没有需要清空的分配')
      return
    }
    
    await ElMessageBox.confirm(
      `确定要清空所有分配吗？这将取消 ${activeCount} 个活跃分配。`,
      '确认清空',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        distinguishCancelAndClose: true
      }
    )

    const result = await datasetApi.clearAssignments(datasetId.value)
    ElMessage.success(result.message || '清空成功')
    await loadAssignments()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清空分配失败:', error)
      ElMessage.error(error.response?.data?.detail || error.message || '清空失败')
    }
  }
}

// 计算进度
const getProgress = (row: AssignmentInfo) => {
  if (row.task_count === 0) return 0
  return Math.round((row.completed_count / row.task_count) * 100)
}

// 获取进度条颜色
const getProgressColor = (row: AssignmentInfo) => {
  const progress = getProgress(row)
  if (progress === 100) return '#67c23a'
  if (progress >= 50) return '#409eff'
  return '#e6a23c'
}

// 格式化日期
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 获取角色标签
const getRoleLabel = (role: string) => {
  const labels: Record<string, string> = {
    admin: '管理员',
    annotator: '标注员',
    reviewer: '复核员',
    viewer: '浏览员'
  }
  return labels[role] || role
}

// 获取任务覆盖样式
const getCoverageStyle = (assignment: any) => {
  if (!assignment.task_range || assignment.task_range === '全部') {
    return {
      left: '0%',
      width: '100%'
    }
  }
  
  // 解析范围 "1-50"
  const match = assignment.task_range.match(/(\d+)-(\d+)/)
  if (match) {
    const start = parseInt(match[1])
    const end = parseInt(match[2])
    const total = stats.value.total_tasks
    
    if (total === 0) {
      return { left: '0%', width: '0%' }
    }
    
    const leftPercent = ((start - 1) / total) * 100
    const widthPercent = ((end - start + 1) / total) * 100
    
    return {
      left: `${leftPercent}%`,
      width: `${widthPercent}%`
    }
  }
  
  return { left: '0%', width: '0%' }
}

// 格式化任务范围（将离散的任务号合并为范围）
const formatTaskRanges = (tasks: number[]) => {
  if (tasks.length === 0) return ''
  if (tasks.length > 20) return `任务 ${tasks[0]}-${tasks[tasks.length - 1]} 等`
  
  const sorted = [...tasks].sort((a, b) => a - b)
  const ranges: string[] = []
  let start = sorted[0]
  let end = sorted[0]
  
  for (let i = 1; i < sorted.length; i++) {
    if (sorted[i] === end + 1) {
      end = sorted[i]
    } else {
      ranges.push(start === end ? `${start}` : `${start}-${end}`)
      start = sorted[i]
      end = sorted[i]
    }
  }
  ranges.push(start === end ? `${start}` : `${start}-${end}`)
  
  return ranges.join(', ')
}

// 返回
const goBack = () => {
  router.back()
}

// ============================================================================
// 规划模式功能
// ============================================================================

// 进入规划模式
const enterPlanningMode = () => {
  isPlanning.value = true
  originalAssignments.value = [...assignments.value]
  
  // 将现有分配转换为规划
  plans.value = assignments.value
    .filter(a => a.is_active)
    .map(a => convertAssignmentToPlan(a))
}

// 退出规划模式
const exitPlanningMode = () => {
  isPlanning.value = false
  plans.value = []
  originalAssignments.value = []
}

// 取消规划
const cancelPlanning = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要取消规划吗？所有未提交的更改将丢失。',
      '确认取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    exitPlanningMode()
    ElMessage.info('已取消规划')
  } catch {
    // 用户取消
  }
}

// 转换分配为规划
const convertAssignmentToPlan = (assignment: AssignmentInfo): AssignmentPlan => {
  const isFullMode = assignment.task_range === '全部'
  let start_index, end_index
  
  if (!isFullMode) {
    const match = assignment.task_range.match(/(\d+)-(\d+)/)
    if (match) {
      start_index = parseInt(match[1])
      end_index = parseInt(match[2])
    }
  }
  
  return {
    id: `existing-${assignment.assignment_id}`,
    user_id: assignment.user_id,
    username: assignment.username,
    role: assignment.role as 'annotator' | 'reviewer',
    mode: isFullMode ? 'full' : 'range',
    start_index,
    end_index,
    task_count: assignment.task_count,
    isNew: false
  }
}

// 生成临时ID
const generateTempId = () => {
  return `temp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

// 自动分配（规划模式）
const autoAssignInPlanning = async (userIds: number[], role: 'annotator' | 'reviewer') => {
  const taskCount = stats.value.total_tasks
  const perUser = Math.ceil(taskCount / userIds.length)
  
  const newPlans: AssignmentPlan[] = []
  
  for (let i = 0; i < userIds.length; i++) {
    const userId = userIds[i]
    const user = allUsers.value.find(u => u.id === userId)
    if (!user) continue
    
    const start = i * perUser + 1
    const end = Math.min((i + 1) * perUser, taskCount)
    
    newPlans.push({
      id: generateTempId(),
      user_id: userId,
      username: user.username,
      role,
      mode: 'range',
      start_index: start,
      end_index: end,
      task_count: end - start + 1,
      isNew: true
    })
  }
  
  // 移除同角色的旧分配，保留其他角色的分配
  plans.value = plans.value.filter(p => p.role !== role)
  
  // 追加新分配
  plans.value.push(...newPlans)
  
  ElMessage.success(`已生成 ${newPlans.length} 个${role === 'annotator' ? '标注员' : '复核员'}分配方案`)
}

// 调整分配任务数（智能调整）
const adjustPlanTasks = (planId: string, delta: number) => {
  const planIndex = plans.value.findIndex(p => p.id === planId)
  if (planIndex === -1) return
  
  const plan = plans.value[planIndex]
  const totalTasks = stats.value.total_tasks
  
  // 如果是整体分配，不能调整
  if (plan.mode === 'full') {
    ElMessage.warning('整体分配不支持调整，请删除后重新添加范围分配')
    return
  }
  
  if (!plan.start_index || !plan.end_index) return
  
  // 计算新的结束索引
  let newEndIndex = plan.end_index + delta
  
  // 边界检查
  if (newEndIndex < plan.start_index) {
    ElMessage.warning('任务数不能小于1')
    return
  }
  
  if (newEndIndex > totalTasks) {
    newEndIndex = totalTasks
  }
  
  // 更新当前计划
  plan.end_index = newEndIndex
  plan.task_count = newEndIndex - plan.start_index + 1
  
  // 智能调整后续计划
  if (planIndex < plans.value.length - 1) {
    const nextPlan = plans.value[planIndex + 1]
    if (nextPlan.mode === 'range' && nextPlan.start_index && nextPlan.end_index) {
      // 调整下一个计划的起始索引
      const newNextStart = newEndIndex + 1
      
      if (newNextStart <= totalTasks) {
        nextPlan.start_index = newNextStart
        nextPlan.task_count = nextPlan.end_index - nextPlan.start_index + 1
        
        // 如果下一个计划的任务数变为0或负数，删除它
        if (nextPlan.task_count <= 0) {
          plans.value.splice(planIndex + 1, 1)
          ElMessage.info(`已自动删除 ${nextPlan.username} 的分配（任务数为0）`)
        }
      }
    }
  }
  
  ElMessage.success('已调整任务分配')
}

// 添加单个分配到规划（改为手动指定范围）
const addPlanItem = (item: Omit<AssignmentPlan, 'id' | 'isNew'>) => {
  plans.value.push({
    ...item,
    id: generateTempId(),
    isNew: true
  })
}

// 删除规划项
const deletePlanItem = (planId: string) => {
  const index = plans.value.findIndex(p => p.id === planId)
  if (index !== -1) {
    plans.value.splice(index, 1)
  }
}

// 清空规划
const clearPlanning = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有规划吗？',
      '确认清空',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    plans.value = []
    ElMessage.success('已清空规划')
  } catch {
    // 用户取消
  }
}

// 检测冲突（严格模式，按角色分别检测）
const detectConflicts = () => {
  const conflicts: string[] = []
  
  // 按角色分组
  const annotatorPlans = plans.value.filter(p => p.role === 'annotator')
  const reviewerPlans = plans.value.filter(p => p.role === 'reviewer')
  
  // 检测标注员冲突
  const annotatorConflicts = detectRoleConflicts(annotatorPlans, '标注员')
  conflicts.push(...annotatorConflicts)
  
  // 检测复核员冲突
  const reviewerConflicts = detectRoleConflicts(reviewerPlans, '复核员')
  conflicts.push(...reviewerConflicts)
  
  return conflicts
}

// 检测单个角色的冲突
const detectRoleConflicts = (rolePlans: AssignmentPlan[], roleName: string) => {
  const conflicts: string[] = []
  const taskMap = new Map<number, string[]>()
  
  rolePlans.forEach(plan => {
    if (plan.mode === 'full') {
      for (let i = 1; i <= stats.value.total_tasks; i++) {
        if (!taskMap.has(i)) {
          taskMap.set(i, [])
        }
        taskMap.get(i)!.push(plan.username)
      }
    } else if (plan.start_index && plan.end_index) {
      for (let i = plan.start_index; i <= plan.end_index; i++) {
        if (!taskMap.has(i)) {
          taskMap.set(i, [])
        }
        taskMap.get(i)!.push(plan.username)
      }
    }
  })
  
  // 查找冲突
  taskMap.forEach((users, taskIndex) => {
    if (users.length > 1) {
      conflicts.push(`任务 ${taskIndex} 被多个${roleName}重复分配: ${users.join(', ')}`)
    }
  })
  
  return conflicts
}

// 检查是否有未分配的任务（按角色）
const getUnassignedTasks = (role?: 'annotator' | 'reviewer') => {
  const assignedTasks = new Set<number>()
  
  // 只统计指定角色的分配（如果提供了role参数）
  const filteredPlans = role 
    ? plans.value.filter(p => p.role === role)
    : plans.value
  
  filteredPlans.forEach(plan => {
    if (plan.mode === 'full') {
      for (let i = 1; i <= stats.value.total_tasks; i++) {
        assignedTasks.add(i)
      }
    } else if (plan.start_index && plan.end_index) {
      for (let i = plan.start_index; i <= plan.end_index; i++) {
        assignedTasks.add(i)
      }
    }
  })
  
  const unassigned: number[] = []
  for (let i = 1; i <= stats.value.total_tasks; i++) {
    if (!assignedTasks.has(i)) {
      unassigned.push(i)
    }
  }
  
  return unassigned
}

// 提交规划
const submitPlanning = async () => {
  // 允许提交空规划（用于清空所有分配）
  if (plans.value.length === 0) {
    try {
      await ElMessageBox.confirm(
        '当前规划为空，提交后将清空所有现有分配。\n\n确认提交吗？',
        '确认清空',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
    } catch {
      return
    }
    
    // 直接调用清空API
    submitting.value = true
    try {
      await datasetApi.clearAssignments(datasetId.value)
      ElMessage.success('已清空所有分配')
      exitPlanningMode()
      await loadAssignments()
    } catch (error: any) {
      console.error('清空失败:', error)
      const detail = error.response?.data?.detail
      
      // 检查是否是有进度的分配错误
      if (detail && typeof detail === 'object' && detail.assignments_with_progress) {
        const progressList = detail.assignments_with_progress
          .slice(0, 3)
          .map((item: any) => `${item.username}(${item.role}): 已完成${item.completed}个, 复核中${item.in_review}个`)
          .join('\n')
        
        let message = `无法清空分配，以下用户已有标注进度：\n\n${progressList}`
        
        if (detail.assignments_with_progress.length > 3) {
          message += `\n...还有 ${detail.assignments_with_progress.length - 3} 个用户`
        }
        
        message += '\n\n请使用转移功能将任务转移给其他用户。'
        
        ElMessageBox.alert(message, '无法清空分配', {
          confirmButtonText: '知道了',
          type: 'warning'
        })
      } else {
        ElMessage.error(detail?.message || detail || error.message || '清空失败')
      }
    } finally {
      submitting.value = false
    }
    return
  }
  
  // 检测冲突（严格阻止）
  const conflicts = detectConflicts()
  if (conflicts.length > 0) {
    ElMessage.error(`存在任务冲突，无法提交！\n${conflicts.slice(0, 3).join('\n')}${conflicts.length > 3 ? `\n...还有 ${conflicts.length - 3} 个冲突` : ''}`)
    return
  }
  
  // 检查未分配的任务（按角色分别检查）
  const annotatorPlans = plans.value.filter(p => p.role === 'annotator')
  const reviewerPlans = plans.value.filter(p => p.role === 'reviewer')
  
  const warnings: string[] = []
  
  if (annotatorPlans.length > 0) {
    const unassignedAnnotator = getUnassignedTasks('annotator')
    if (unassignedAnnotator.length > 0) {
      const ranges = formatTaskRanges(unassignedAnnotator)
      warnings.push(`标注员：${unassignedAnnotator.length} 个任务未分配 (${ranges})`)
    }
  }
  
  if (reviewerPlans.length > 0) {
    const unassignedReviewer = getUnassignedTasks('reviewer')
    if (unassignedReviewer.length > 0) {
      const ranges = formatTaskRanges(unassignedReviewer)
      warnings.push(`复核员：${unassignedReviewer.length} 个任务未分配 (${ranges})`)
    }
  }
  
  if (warnings.length > 0) {
    try {
      await ElMessageBox.confirm(
        `存在未分配任务：\n\n${warnings.join('\n')}\n\n是否仍要提交？`,
        '存在未分配任务',
        {
          confirmButtonText: '仍要提交',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
    } catch {
      return
    }
  }
  
  // 确认提交
  try {
    await ElMessageBox.confirm(
      `即将提交 ${plans.value.length} 个分配，这将清空现有分配并创建新的分配。\n\n确认提交吗？`,
      '确认提交',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
  } catch {
    return
  }
  
  submitting.value = true
  try {
    // 构建请求数据
    const requestData = {
      assignments: plans.value.map(plan => ({
        user_id: plan.user_id,
        role: plan.role,
        mode: plan.mode,
        start_index: plan.start_index,
        end_index: plan.end_index
      })),
      clear_existing: true,
      role_filter: undefined  // 不使用角色筛选，允许同时提交标注员和复核员
    }
    
    await datasetApi.batchAssign(datasetId.value, requestData)
    ElMessage.success('分配提交成功')
    
    // 退出规划模式并刷新
    exitPlanningMode()
    await loadAssignments()
  } catch (error: any) {
    console.error('提交规划失败:', error)
    const detail = error.response?.data?.detail
    
    // 检查是否是有进度的分配错误
    if (detail && typeof detail === 'object' && detail.assignments_with_progress) {
      const progressList = detail.assignments_with_progress
        .slice(0, 3)
        .map((item: any) => `${item.username}(${item.role}): 已完成${item.completed}个, 复核中${item.in_review}个`)
        .join('\n')
      
      let message = `无法提交分配，以下用户已有标注进度：\n\n${progressList}`
      
      if (detail.assignments_with_progress.length > 3) {
        message += `\n...还有 ${detail.assignments_with_progress.length - 3} 个用户`
      }
      
      message += '\n\n请使用转移功能将任务转移给其他用户，或取消这些用户的分配后再重新规划。'
      
      ElMessageBox.alert(message, '无法提交分配', {
        confirmButtonText: '知道了',
        type: 'warning'
      })
    } else {
      ElMessage.error(detail?.message || detail || error.message || '提交失败')
    }
  } finally {
    submitting.value = false
  }
}

// 监听角色变化，更新可用用户列表
watch(() => assignForm.value.role, (newRole) => {
  availableUsers.value = getAvailableUsersForRole(newRole)
  // 如果当前选择的用户已被分配，清空选择
  if (assignForm.value.user_id && !availableUsers.value.find(u => u.id === assignForm.value.user_id)) {
    assignForm.value.user_id = null
  }
})

watch(() => autoAssignForm.value.role, (newRole) => {
  availableUsers.value = getAvailableUsersForRole(newRole)
  // 过滤掉已分配的用户
  autoAssignForm.value.user_ids = autoAssignForm.value.user_ids.filter(
    id => availableUsers.value.find(u => u.id === id)
  )
})

onMounted(() => {
  loadAssignments()
  loadUsers()
})
</script>
⋮----
<style scoped lang="scss">
.dataset-assignment-container {
  padding: 20px;

  .assignment-card {
    margin-top: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .actions {
        display: flex;
        gap: 10px;
      }
    }

    .stats {
      display: flex;
      gap: 40px;
      padding: 20px;
      background: #f5f7fa;
      border-radius: 4px;
    }

    .task-coverage {
      margin-top: 20px;
      padding: 20px;
      background: #fafafa;
      border-radius: 4px;
      border: 1px solid #e4e7ed;

      .coverage-title {
        font-size: 14px;
        font-weight: 500;
        color: #303133;
        margin-bottom: 16px;
      }

      .coverage-section {
        margin-bottom: 20px;

        &:last-of-type {
          margin-bottom: 12px;
        }

        .coverage-section-title {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 8px;
          font-size: 13px;
          color: #606266;

          .coverage-count {
            font-weight: 500;
          }
        }
      }

      .coverage-container {
        margin-bottom: 8px;
      }

      .coverage-bar {
        position: relative;
        height: 40px;
        background: #e4e7ed;
        border-radius: 4px;
        overflow: hidden;
      }

      .coverage-segment {
        position: absolute;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 12px;
        font-weight: 500;
        transition: all 0.3s;
        cursor: pointer;

        &.role-annotator {
          background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
        }

        &.role-reviewer {
          background: linear-gradient(135deg, #e6a23c 0%, #f0b95c 100%);
        }

        &:hover {
          opacity: 0.8;
          transform: translateY(-2px);
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }

        .coverage-label {
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          padding: 0 8px;
        }
      }

      .coverage-legend {
        display: flex;
        justify-content: space-between;
        margin-top: 8px;
        font-size: 12px;
        color: #909399;
      }

      .coverage-stats {
        display: flex;
        gap: 12px;
        align-items: center;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #e4e7ed;
      }
    }

    .progress-info {
      display: flex;
      flex-direction: column;
      gap: 4px;

      .progress-text {
        font-size: 12px;
        color: #606266;
      }
    }

    .text-secondary {
      font-size: 12px;
      color: #909399;
      margin-top: 4px;
    }
  }
}
</style>
````

## File: frontend/src/views/dataset/DatasetDetail.vue
````vue
<template>
  <div class="dataset-detail">
    <div v-loading="loading" class="detail-container">
      <el-page-header @back="handleBack">
        <template #content>
          <div class="page-header-content">
            <span class="page-title">{{ dataset?.name || '数据集详情' }}</span>
            <!-- Task 47: 添加分配管理按钮（仅管理员可见） -->
            <el-button
              v-if="authStore.user?.role === 'admin'"
              type="primary"
              @click="goToAssignment"
            >
              <el-icon><Setting /></el-icon>
              分配管理
            </el-button>
          </div>
        </template>
      </el-page-header>

      <div v-if="dataset" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="数据集名称">
            {{ dataset.name }}
          </el-descriptions-item>
          <el-descriptions-item label="数据集ID">
            {{ dataset.dataset_id }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ dataset.description || '暂无描述' }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ dataset.created_at }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">
            {{ dataset.updated_at }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="statistics-section">
          <h3>统计信息</h3>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-statistic title="总任务数" :value="dataset.statistics?.total_tasks || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="已完成" :value="dataset.statistics?.completed_tasks || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="已复核" :value="dataset.statistics?.reviewed_tasks || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="待处理" :value="dataset.statistics?.pending_tasks || 0" />
            </el-col>
          </el-row>
        </div>

        <!-- 标注任务列表 -->
        <div class="tasks-section">
          <div class="section-header">
            <h3>标注任务列表</h3>
            <div class="header-actions">
              <el-button
                v-if="authStore.user?.role !== 'viewer' && selectedTasks.length > 0"
                type="success"
                size="small"
                @click="handleBatchAnnotateSelected"
              >
                批量标注选中 ({{ selectedTasks.length }})
              </el-button>
              <el-button
                v-if="authStore.user?.role !== 'viewer'"
                type="primary"
                size="small"
                @click="handleBatchAnnotateAll"
              >
                批量标注全部
              </el-button>
              <!-- 添加语料按钮（仅管理员） -->
              <el-button
                v-if="authStore.user?.role === 'admin'"
                type="success"
                size="small"
                :icon="Plus"
                @click="openAddCorpusDialog"
              >
                添加语料
              </el-button>
            </div>
          </div>

          <el-table
            v-loading="tasksLoading"
            :data="taskList"
            stripe
            style="width: 100%"
            @selection-change="handleSelectionChange"
          >
            <el-table-column
              v-if="authStore.user?.role !== 'viewer'"
              type="selection"
              width="55"
              :selectable="isTaskSelectable"
            />
            <el-table-column prop="task_id" label="任务ID" width="180" />
            <el-table-column label="语料文本" min-width="300">
              <template #default="{ row }">
                <div class="text-preview">
                  {{ row.corpus_text || '暂无文本' }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="标注类型" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.annotation_type === 'automatic'" type="info">
                  自动
                </el-tag>
                <el-tag v-else-if="row.annotation_type === 'manual'" type="success">
                  手动
                </el-tag>
                <el-tag v-else type="warning">待标注</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="实体数" width="80">
              <template #default="{ row }">
                {{ row.entity_count || 0 }}
              </template>
            </el-table-column>
            <el-table-column label="关系数" width="80">
              <template #default="{ row }">
                {{ row.relation_count || 0 }}
              </template>
            </el-table-column>
            <el-table-column label="更新时间" width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.updated_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button
                  v-if="authStore.user?.role !== 'viewer'"
                  type="primary"
                  size="small"
                  @click="handleAnnotate(row)"
                >
                  {{ row.status === 'pending' ? '开始标注' : '继续标注' }}
                </el-button>
                <el-button
                  v-else
                  type="info"
                  size="small"
                  @click="handleAnnotate(row)"
                >
                  查看
                </el-button>
                <!-- 删除任务按钮（仅管理员） -->
                <el-button
                  v-if="authStore.user?.role === 'admin'"
                  type="danger"
                  size="small"
                  :icon="Delete"
                  @click="handleDeleteTask(row)"
                />
              </template>
            </el-table-column>
          </el-table>

          <div v-if="taskTotal > 0" class="pagination">
            <el-pagination
              v-model:current-page="taskPage"
              v-model:page-size="taskPageSize"
              :total="taskTotal"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="fetchTasks"
              @current-change="fetchTasks"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 添加语料对话框 -->
    <el-dialog
      v-model="addCorpusDialogVisible"
      title="添加语料到数据集"
      width="80%"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <CorpusSelector ref="corpusSelectorRef" />
      <template #footer>
        <el-button @click="addCorpusDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="addTasksLoading" @click="confirmAddCorpus">
          确认添加
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>
⋮----
<template #content>
          <div class="page-header-content">
            <span class="page-title">{{ dataset?.name || '数据集详情' }}</span>
            <!-- Task 47: 添加分配管理按钮（仅管理员可见） -->
            <el-button
              v-if="authStore.user?.role === 'admin'"
              type="primary"
              @click="goToAssignment"
            >
              <el-icon><Setting /></el-icon>
              分配管理
            </el-button>
          </div>
        </template>
⋮----
<span class="page-title">{{ dataset?.name || '数据集详情' }}</span>
<!-- Task 47: 添加分配管理按钮（仅管理员可见） -->
⋮----
{{ dataset.name }}
⋮----
{{ dataset.dataset_id }}
⋮----
{{ dataset.description || '暂无描述' }}
⋮----
{{ dataset.created_at }}
⋮----
{{ dataset.updated_at }}
⋮----
<!-- 标注任务列表 -->
⋮----
批量标注选中 ({{ selectedTasks.length }})
⋮----
<!-- 添加语料按钮（仅管理员） -->
⋮----
<template #default="{ row }">
                <div class="text-preview">
                  {{ row.corpus_text || '暂无文本' }}
                </div>
              </template>
⋮----
{{ row.corpus_text || '暂无文本' }}
⋮----
<template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
⋮----
{{ getStatusText(row.status) }}
⋮----
<template #default="{ row }">
                <el-tag v-if="row.annotation_type === 'automatic'" type="info">
                  自动
                </el-tag>
                <el-tag v-else-if="row.annotation_type === 'manual'" type="success">
                  手动
                </el-tag>
                <el-tag v-else type="warning">待标注</el-tag>
              </template>
⋮----
<template #default="{ row }">
                {{ row.entity_count || 0 }}
              </template>
⋮----
{{ row.entity_count || 0 }}
⋮----
<template #default="{ row }">
                {{ row.relation_count || 0 }}
              </template>
⋮----
{{ row.relation_count || 0 }}
⋮----
<template #default="{ row }">
                {{ formatDateTime(row.updated_at) }}
              </template>
⋮----
{{ formatDateTime(row.updated_at) }}
⋮----
<template #default="{ row }">
                <el-button
                  v-if="authStore.user?.role !== 'viewer'"
                  type="primary"
                  size="small"
                  @click="handleAnnotate(row)"
                >
                  {{ row.status === 'pending' ? '开始标注' : '继续标注' }}
                </el-button>
                <el-button
                  v-else
                  type="info"
                  size="small"
                  @click="handleAnnotate(row)"
                >
                  查看
                </el-button>
                <!-- 删除任务按钮（仅管理员） -->
                <el-button
                  v-if="authStore.user?.role === 'admin'"
                  type="danger"
                  size="small"
                  :icon="Delete"
                  @click="handleDeleteTask(row)"
                />
              </template>
⋮----
{{ row.status === 'pending' ? '开始标注' : '继续标注' }}
⋮----
<!-- 删除任务按钮（仅管理员） -->
⋮----
<!-- 添加语料对话框 -->
⋮----
<template #footer>
        <el-button @click="addCorpusDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="addTasksLoading" @click="confirmAddCorpus">
          确认添加
        </el-button>
      </template>
⋮----
<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Setting, Plus, Delete } from '@element-plus/icons-vue'
import { useDatasetStore, useAuthStore } from '@/stores'
import CorpusSelector from '@/components/dataset/CorpusSelector.vue'
import type { Dataset } from '@/types'
import { formatDateTime } from '@/utils/datetime'
import { getStatusText, getStatusType } from '@/constants/taskStatus'
import { annotationApi } from '@/api/annotation'

interface AnnotationTask {
  id: number
  task_id: string
  corpus_text: string
  status: string
  annotation_type: string
  entity_count: number
  relation_count: number
  updated_at: string
}

const route = useRoute()
const router = useRouter()
const datasetStore = useDatasetStore()
const authStore = useAuthStore()

const loading = ref(false)
const tasksLoading = ref(false)
const dataset = ref<Dataset | null>(null)
const taskList = ref<AnnotationTask[]>([])
const taskPage = ref(1)
const taskPageSize = ref(20)
const taskTotal = ref(0)

// 添加语料对话框
const addCorpusDialogVisible = ref(false)
const addTasksLoading = ref(false)
const corpusSelectorRef = ref<InstanceType<typeof CorpusSelector> | null>(null)

const handleBack = () => {
  router.push({ name: 'datasets' })
}

// Task 47: 跳转到分配管理页面
const goToAssignment = () => {
  if (dataset.value) {
    router.push({
      name: 'dataset-assignment',
      params: { id: dataset.value.dataset_id }
    })
  }
}

const fetchDetail = async () => {
  const id = route.params.id as string
  if (!id) {
    handleBack()
    return
  }

  loading.value = true
  try {
    dataset.value = await datasetStore.fetchDetail(id)
    // 获取任务列表
    await fetchTasks()
  } catch (error: any) {
    console.error('获取数据集详情失败:', error)
    
    // 如果是404错误，说明后端API还未实现，使用模拟数据
    if (error.response?.status === 404) {
      ElMessage.warning('后端API未实现，使用模拟数据')
      // 使用模拟数据
      dataset.value = {
        id: 1,
        dataset_id: id,
        name: `数据集 ${id}`,
        description: '这是一个测试数据集（模拟数据）',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        statistics: {
          total_tasks: 0,
          completed_tasks: 0,
          reviewed_tasks: 0,
          pending_tasks: 0
        }
      } as any
    } else {
      ElMessage.error('获取数据集详情失败')
      handleBack()
    }
  } finally {
    loading.value = false
  }
}

const fetchTasks = async () => {
  if (!dataset.value) return

  tasksLoading.value = true
  try {
    // 调用API获取任务列表
    const response = await datasetStore.fetchDatasetTasks(
      dataset.value.dataset_id,
      {
        page: taskPage.value,
        page_size: taskPageSize.value
      }
    )
    
    const newItems = response.items || []

    // 保留本地仍在 processing 的任务，避免后台查询暂时拿不到导致列表瞬移
    const processingCache = new Map(
      taskList.value
        .filter(t => t.status === 'processing')
        .map(t => [t.task_id, t])
    )
    const merged = newItems.map(item => processingCache.get(item.task_id) || item)

    taskList.value = merged
    taskTotal.value = response.total || merged.length
  } catch (error: any) {
    console.error('获取任务列表失败:', error)
    
    // 如果是404，说明后端API未实现，暂时不显示错误
    if (error.response?.status === 404) {
      console.warn('任务列表API未实现，显示空列表')
      taskList.value = []
      taskTotal.value = 0
    } else {
      ElMessage.error('获取任务列表失败')
    }
  } finally {
    tasksLoading.value = false
  }
}

const handleAnnotate = (task: AnnotationTask) => {
  // 跳转到标注页面
  router.push({
    name: 'annotation-editor',
    params: { taskId: task.task_id }
  })
}

// 刷新统计数据（详情接口现在内嵌 statistics）
const refreshDetail = async () => {
  if (!dataset.value) return
  try {
    dataset.value = await datasetStore.fetchDetail(dataset.value.dataset_id)
  } catch {
    // ignore
  }
}

// 打开"添加语料"对话框
const openAddCorpusDialog = () => {
  addCorpusDialogVisible.value = true
}

// 确认添加语料
const confirmAddCorpus = async () => {
  if (!dataset.value || !corpusSelectorRef.value) return

  const selectedIds: string[] = corpusSelectorRef.value.getSelectedIds()
  if (selectedIds.length === 0) {
    ElMessage.warning('请先选择要添加的语料')
    return
  }

  // CorpusSelector 返回 text_id (string)，但后端需要 corpus.id (integer)
  // 通过 getSelectedCorpus() 获取含 id 字段的完整 Corpus 对象
  const selectedCorpus = corpusSelectorRef.value.getSelectedCorpus()
  const corpusIds: number[] = selectedCorpus
    .map((c: any) => c.id)
    .filter((id: number | undefined): id is number => id !== undefined)

  if (corpusIds.length === 0) {
    ElMessage.error('无法获取语料数据库ID，请重试')
    return
  }
  if (corpusIds.length !== selectedCorpus.length) {
    ElMessage.warning(`部分语料缺少ID信息，将添加 ${corpusIds.length} 条`)
  }

  addTasksLoading.value = true
  try {
    const result = await datasetStore.addTasksToDataset(dataset.value.dataset_id, corpusIds)
    ElMessage.success(`添加成功：新增 ${result.added} 条，跳过重复 ${result.skipped} 条`)
    addCorpusDialogVisible.value = false
    // 刷新任务列表和统计
    await Promise.all([fetchTasks(), refreshDetail()])
  } catch (error: any) {
    ElMessage.error(error.message || '添加语料失败')
  } finally {
    addTasksLoading.value = false
  }
}

// 删除单个任务
const handleDeleteTask = async (task: AnnotationTask) => {
  if (!dataset.value) return

  try {
    const confirmMessageVNode = h('div', [
      h('div', `确定要删除任务 ${task.task_id} 吗？`),
      h('div', { style: 'margin-top: 8px; color: #f56c6c;' }, '此操作将同时删除其下的所有标注数据且不可恢复。')
    ])
    await ElMessageBox.confirm(
      confirmMessageVNode,
      '删除确认',
      {
        type: 'warning',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        confirmButtonClass: 'el-button--danger'
      }
    )
  } catch {
    return // 用户取消
  }

  try {
    await datasetStore.removeTaskFromDataset(dataset.value.dataset_id, task.task_id)
    ElMessage.success('任务删除成功')
    // 刷新列表和统计
    await Promise.all([fetchTasks(), refreshDetail()])
  } catch (error: any) {
    ElMessage.error(error.message || '删除任务失败')
  }
}

const selectedTasks = ref<AnnotationTask[]>([])

// 处理任务选择变化
const handleSelectionChange = (selection: AnnotationTask[]) => {
  selectedTasks.value = selection
}

// 判断任务是否可选择（只有pending状态的任务可以批量标注）
const isTaskSelectable = (row: AnnotationTask) => {
  return row.status === 'pending'
}

// 批量标注选中的任务
const handleBatchAnnotateSelected = async () => {
  if (selectedTasks.value.length === 0) {
    ElMessage.warning('请先选择要标注的任务')
    return
  }
  
  try {
    const taskIds = selectedTasks.value.map(t => t.task_id)
    await triggerBatchAnnotation(taskIds)
  } catch (error: any) {
    console.error('批量标注失败:', error)
    ElMessage.error(error.message || '批量标注失败')
  }
}

// 批量标注全部pending任务
const handleBatchAnnotateAll = async () => {
  const pendingTasks = taskList.value.filter(t => t.status === 'pending')
  
  if (pendingTasks.length === 0) {
    ElMessage.warning('没有待标注的任务')
    return
  }
  
  try {
    await triggerBatchAnnotation()
  } catch (error: any) {
    console.error('批量标注失败:', error)
    ElMessage.error(error.message || '批量标注失败')
  }
}

// 触发批量标注
const triggerBatchAnnotation = async (taskIds?: string[]) => {
  if (!dataset.value) {
    ElMessage.error('数据集信息未加载')
    return
  }
  
  try {
    const response = await annotationApi.triggerBatchAnnotation({
      dataset_id: dataset.value.dataset_id,
      task_ids: taskIds
    })

    if (response.success) {
      const jobId = response.data.job_id
      const totalTasks = response.data.total_tasks

      ElMessage.success(`批量标注任务已创建，共 ${totalTasks} 个任务`)

      // 清除选择
      selectedTasks.value = []

      // 前端先将目标任务标记为处理中，保持当前位置
      const targetIds = taskIds && taskIds.length > 0
        ? new Set(taskIds)
        : new Set(taskList.value.filter(t => t.status === 'pending').map(t => t.task_id))

      taskList.value = taskList.value.map(t => {
        if (targetIds.has(t.task_id)) {
          return { ...t, status: 'processing', annotation_type: t.annotation_type || 'automatic' }
        }
        return t
      })

      // 略延时再拉取最新结果，避免立刻翻页丢失位置
      setTimeout(() => {
        fetchTasks()
      }, 5000)
    }
  } catch (error: any) {
    throw error
  }
}

const handleBatchAnnotate = () => {
  // 保留旧方法以兼容
  handleBatchAnnotateAll()
}

// formatDateTime 已从 @/utils/datetime 导入

onMounted(() => {
  fetchDetail()
})
</script>
⋮----
<style scoped lang="scss">
.dataset-detail {
  padding: 20px;

  .detail-container {
    min-height: 400px;
  }

  .page-title {
    font-size: 20px;
    font-weight: 600;
  }

  .page-header-content {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .detail-content {
    margin-top: 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .statistics-section,
  .tasks-section {
    h3 {
      margin: 0 0 16px;
      font-size: 16px;
      font-weight: 600;
      color: #303133;
    }
  }

  .tasks-section {
    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      h3 {
        margin: 0;
      }

      .header-actions {
        display: flex;
        gap: 8px;
      }
    }

    .text-preview {
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      color: #606266;
    }

    .pagination {
      margin-top: 16px;
      display: flex;
      justify-content: center;
    }
  }
}
</style>
````

## File: frontend/src/views/dataset/DatasetManagement.vue
````vue
<template>
  <div class="dataset-management">
    <div class="page-header">
      <div class="header-left">
        <h2>数据集管理</h2>
        <p class="page-desc">
          {{ authStore.user?.role === 'viewer' ? '查看和导出数据集' : '从语料中选择记录创建数据集，用于标注任务' }}
        </p>
      </div>
      <div class="header-right">
        <el-select
          v-model="statusFilter"
          placeholder="筛选状态"
          clearable
          style="width: 150px; margin-right: 12px"
          @change="handleFilterChange"
        >
          <el-option label="全部" value="" />
          <el-option label="进行中" value="in_progress" />
          <el-option label="已完成" value="completed" />
        </el-select>
        <el-button
          v-if="authStore.user?.role !== 'viewer'"
          type="primary"
          :icon="Plus"
          @click="handleCreate"
        >
          创建数据集
        </el-button>
      </div>
    </div>

    <!-- 数据集列表 -->
    <div v-loading="loading" class="dataset-list">
      <el-empty
        v-if="!loading && datasetList.length === 0"
        :description="authStore.user?.role === 'viewer' ? '暂无数据集' : '暂无数据集'"
      >
        <el-button 
          v-if="authStore.user?.role !== 'viewer'" 
          type="primary" 
          @click="handleCreate"
        >
          创建第一个数据集
        </el-button>
      </el-empty>

      <div v-else class="dataset-grid">
        <DatasetCard
          v-for="dataset in datasetList"
          :key="dataset.id"
          :dataset="dataset"
          :is-viewer="authStore.user?.role === 'viewer'"
          :is-admin="authStore.user?.role === 'admin'"
          @view="handleView"
          @batch-annotate="handleBatchAnnotate"
          @assign="handleAssign"
          @edit="handleEdit"
          @delete="handleDelete"
          @export="handleExport"
        />
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[12, 24, 48]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 创建数据集对话框 -->
    <DatasetCreateDialog
      v-model="createDialogVisible"
      @success="handleCreateSuccess"
    />

    <!-- 编辑数据集对话框 -->
    <DatasetEditDialog
      v-model="editDialogVisible"
      :dataset="selectedDataset"
      @success="handleEditSuccess"
    />

    <!-- 批量标注对话框 -->
    <BatchAnnotationDialog
      v-model="batchAnnotationDialogVisible"
      :dataset="selectedDataset"
      @success="handleBatchAnnotationSuccess"
    />
  </div>
</template>
⋮----
{{ authStore.user?.role === 'viewer' ? '查看和导出数据集' : '从语料中选择记录创建数据集，用于标注任务' }}
⋮----
<!-- 数据集列表 -->
⋮----
<!-- 分页 -->
⋮----
<!-- 创建数据集对话框 -->
⋮----
<!-- 编辑数据集对话框 -->
⋮----
<!-- 批量标注对话框 -->
⋮----
<script setup lang="ts">
import axios from 'axios'
import { ref, computed, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useDatasetStore, useAuthStore } from '@/stores'
import DatasetCard from '@/components/dataset/DatasetCard.vue'
import DatasetCreateDialog from '@/components/dataset/DatasetCreateDialog.vue'
import DatasetEditDialog from '@/components/dataset/DatasetEditDialog.vue'
import BatchAnnotationDialog from '@/components/dataset/BatchAnnotationDialog.vue'
import type { Dataset, DatasetStatus } from '@/types'
import { buildApiUrl } from '@/utils/backendUrl'

const router = useRouter()
const datasetStore = useDatasetStore()
const authStore = useAuthStore()

// 状态
const createDialogVisible = ref(false)
const editDialogVisible = ref(false)
const batchAnnotationDialogVisible = ref(false)
const selectedDataset = ref<Dataset | null>(null)
const currentPage = ref(1)
const pageSize = ref(12)
const statusFilter = ref<DatasetStatus | ''>('')

// 检查用户角色，标注员和复核员应该使用"我的数据集"页面
const checkUserRole = () => {
  const userRole = authStore.user?.role
  if (userRole === 'annotator' || userRole === 'reviewer') {
    ElMessage.info('标注员和复核员请使用"我的数据集"查看分配给您的任务')
    router.replace({ name: 'my-datasets' })
  }
}

// 计算属性
const loading = computed(() => datasetStore.loading)
const allDatasets = computed(() => datasetStore.datasetList)
const total = computed(() => datasetStore.total)

// 根据状态筛选数据集
const datasetList = computed(() => {
  if (!statusFilter.value) {
    return allDatasets.value
  }
  
  return allDatasets.value.filter(dataset => {
    const stats = dataset.statistics
    if (!stats) return false
    
    const total = stats.total_tasks
    const completed = stats.completed_tasks
    
    if (statusFilter.value === 'in_progress') {
      return total > 0 && completed < total
    } else if (statusFilter.value === 'completed') {
      return total > 0 && completed === total
    }
    
    return true
  })
})

// 方法
const fetchList = async () => {
  // 浏览员应该看到所有数据集，不按创建人过滤
  const params: any = {
    page: currentPage.value,
    page_size: pageSize.value
  }
  
  // 只有非浏览员才按创建人过滤（可选）
  // 实际上，所有角色都应该能看到所有数据集
  // if (authStore.user?.role !== 'viewer') {
  //   params.created_by = authStore.user?.id
  // }
  
  await datasetStore.fetchList(params)
}

const handlePageChange = () => {
  fetchList()
}

const handleFilterChange = () => {
  // 筛选是前端实现,不需要重新请求
  // 如果需要后端筛选,可以在这里调用 fetchList()
}

const handleCreate = () => {
  createDialogVisible.value = true
}

const handleCreateSuccess = () => {
  ElMessage.success('数据集创建成功')
  fetchList()
}

const handleView = (dataset: Dataset) => {
  router.push({ name: 'dataset-detail', params: { id: dataset.dataset_id } })
}

const handleAssign = (dataset: Dataset) => {
  router.push({ name: 'dataset-assignment', params: { id: dataset.dataset_id } })
}

const handleBatchAnnotate = (dataset: Dataset) => {
  selectedDataset.value = dataset
  batchAnnotationDialogVisible.value = true
}

const handleBatchAnnotationSuccess = () => {
  ElMessage.success('批量标注完成')
  fetchList()
}

const handleEdit = (dataset: Dataset) => {
  selectedDataset.value = dataset
  editDialogVisible.value = true
}

const handleEditSuccess = () => {
  ElMessage.success('数据集更新成功')
  fetchList()
}

const handleDelete = async (dataset: Dataset) => {
  try {
    const confirmMessageVNode = h('div', [
      h('div', `确定要删除数据集 "${dataset.name}" 吗？`),
      h('div', { style: 'margin-top: 8px; color: #f56c6c;' }, '此操作将同时删除所有关联的标注任务，且不可恢复。')
    ])
    await ElMessageBox.confirm(
      confirmMessageVNode,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await datasetStore.deleteDataset(dataset.dataset_id)
    ElMessage.success('删除成功')
    
    // 如果当前页没有数据了，返回上一页
    if (datasetList.value.length === 0 && currentPage.value > 1) {
      currentPage.value--
    }
    
    fetchList()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

const handleExport = async (dataset: Dataset) => {
  try {
    const fallbackFilename = `${dataset.dataset_id}_${Date.now()}.jsonl`
    const requestedOutputPath = `data/exports/${fallbackFilename}`

    // 直接POST导出接口，获取blob
    const url = buildApiUrl(`/datasets/${dataset.dataset_id}/export`)

    const token = localStorage.getItem('token') || sessionStorage.getItem('token')
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const response = await axios.post(
      url,
      {
        output_path: requestedOutputPath,
        status_filter: ["completed", "reviewed"]
      },
      {
        headers,
        responseType: 'blob',
        validateStatus: status => status === 200
      }
    )

    // 尝试从响应头获取文件名
    let filename = fallbackFilename
    const disposition = response.headers['content-disposition']
    if (disposition) {
      const match = disposition.match(/filename="?([^";]+)"?/)
      if (match) filename = decodeURIComponent(match[1])
    }

    // 创建下载链接
    const blob = response.data
    const blobUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = blobUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(blobUrl)

    ElMessage.success('导出成功，已开始下载')
  } catch (error: any) {
    ElMessage.error(error?.message || '导出失败')
  }
}

// 生命周期
onMounted(() => {
  // 检查用户角色
  checkUserRole()
  
  // 如果不是标注员/复核员，加载数据集列表
  const userRole = authStore.user?.role
  if (userRole !== 'annotator' && userRole !== 'reviewer') {
    fetchList()
  }
})
</script>
⋮----
<style scoped lang="scss">
.dataset-management {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;

    .header-left {
      h2 {
        margin: 0 0 8px;
        font-size: 24px;
        color: #303133;
      }

      .page-desc {
        margin: 0;
        font-size: 14px;
        color: #909399;
      }
    }

    .header-right {
      display: flex;
      align-items: center;
    }
  }

  .dataset-list {
    min-height: 400px;

    .dataset-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 20px;
    }
  }

  .pagination {
    margin-top: 24px;
    display: flex;
    justify-content: center;
  }
}
</style>
````

## File: frontend/src/views/dataset/MyDatasets.vue
````vue
<template>
  <div class="my-datasets-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="title">我的数据集</span>
          <el-radio-group v-model="roleFilter" size="small" @change="loadMyDatasets">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="annotator">标注任务</el-radio-button>
            <el-radio-button label="reviewer">复核任务</el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="datasets"
        style="width: 100%"
      >
        <el-table-column prop="name" label="数据集名称" min-width="200">
          <template #default="{ row }">
            <el-link type="primary" @click="goToDetail(row.dataset_id)">
              {{ row.name }}
            </el-link>
          </template>
        </el-table-column>

        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />

        <el-table-column prop="my_role" label="我的角色" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.my_role === 'annotator'" type="success">标注员</el-tag>
            <el-tag v-else-if="row.my_role === 'reviewer'" type="warning">复核员</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="my_task_range" label="任务范围" width="120" />

        <el-table-column label="进度" width="200">
          <template #default="{ row }">
            <div class="progress-info">
              <el-progress
                :percentage="getProgress(row)"
                :color="getProgressColor(row)"
              />
              <span class="progress-text">
                {{ row.my_completed_count }} / {{ row.my_task_count }}
              </span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="total_tasks" label="总任务数" width="100" />

        <el-table-column prop="assigned_at" label="分配时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.assigned_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.my_role === 'annotator'"
              type="primary"
              size="small"
              @click="goToAnnotation(row.dataset_id)"
            >
              开始标注
            </el-button>
            <el-button
              v-else-if="row.my_role === 'reviewer'"
              type="warning"
              size="small"
              @click="goToReview(row.dataset_id)"
            >
              开始复核
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadMyDatasets"
          @current-change="loadMyDatasets"
        />
      </div>
    </el-card>
  </div>
</template>
⋮----
<template #header>
        <div class="card-header">
          <span class="title">我的数据集</span>
          <el-radio-group v-model="roleFilter" size="small" @change="loadMyDatasets">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="annotator">标注任务</el-radio-button>
            <el-radio-button label="reviewer">复核任务</el-radio-button>
          </el-radio-group>
        </div>
      </template>
⋮----
<template #default="{ row }">
            <el-link type="primary" @click="goToDetail(row.dataset_id)">
              {{ row.name }}
            </el-link>
          </template>
⋮----
{{ row.name }}
⋮----
<template #default="{ row }">
            <el-tag v-if="row.my_role === 'annotator'" type="success">标注员</el-tag>
            <el-tag v-else-if="row.my_role === 'reviewer'" type="warning">复核员</el-tag>
          </template>
⋮----
<template #default="{ row }">
            <div class="progress-info">
              <el-progress
                :percentage="getProgress(row)"
                :color="getProgressColor(row)"
              />
              <span class="progress-text">
                {{ row.my_completed_count }} / {{ row.my_task_count }}
              </span>
            </div>
          </template>
⋮----
{{ row.my_completed_count }} / {{ row.my_task_count }}
⋮----
<template #default="{ row }">
            {{ formatDate(row.assigned_at) }}
          </template>
⋮----
{{ formatDate(row.assigned_at) }}
⋮----
<template #default="{ row }">
            <el-button
              v-if="row.my_role === 'annotator'"
              type="primary"
              size="small"
              @click="goToAnnotation(row.dataset_id)"
            >
              开始标注
            </el-button>
            <el-button
              v-else-if="row.my_role === 'reviewer'"
              type="warning"
              size="small"
              @click="goToReview(row.dataset_id)"
            >
              开始复核
            </el-button>
          </template>
⋮----
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { datasetApi } from '@/api/dataset'
import type { MyDatasetInfo } from '@/types/assignment'

const router = useRouter()

// 状态
const loading = ref(false)
const datasets = ref<MyDatasetInfo[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const roleFilter = ref('')

// 加载我的数据集
const loadMyDatasets = async () => {
  loading.value = true
  try {
    console.log('开始加载我的数据集...')
    const response = await datasetApi.getMyDatasets({
      role: roleFilter.value || undefined,
      page: currentPage.value,
      page_size: pageSize.value
    })

    console.log('API响应:', response)
    console.log('response.success:', response.success)
    console.log('response.data:', response.data)
    console.log('response.data.items:', response.data?.items)

    if (response.success) {
      datasets.value = response.data.items
      total.value = response.data.total
      console.log('✓ 设置datasets:', datasets.value)
      console.log('✓ 设置total:', total.value)
    } else {
      console.error('API返回success=false')
    }
  } catch (error: any) {
    console.error('加载失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载数据集失败')
  } finally {
    loading.value = false
  }
}

// 计算进度百分比
const getProgress = (row: MyDatasetInfo) => {
  if (row.my_task_count === 0) return 0
  return Math.round((row.my_completed_count / row.my_task_count) * 100)
}

// 获取进度条颜色
const getProgressColor = (row: MyDatasetInfo) => {
  const progress = getProgress(row)
  if (progress === 100) return '#67c23a'
  if (progress >= 50) return '#409eff'
  return '#e6a23c'
}

// 格式化日期
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 跳转到数据集详情
const goToDetail = (datasetId: string) => {
  router.push({ name: 'dataset-detail', params: { id: datasetId } })
}

// 跳转到标注页面
const goToAnnotation = (datasetId: string) => {
  router.push({ name: 'annotations', query: { dataset_id: datasetId } })
}

// 跳转到复核页面
const goToReview = (datasetId: string) => {
  router.push({ name: 'review', query: { dataset_id: datasetId } })
}

onMounted(() => {
  loadMyDatasets()
})
</script>
⋮----
<style scoped lang="scss">
.my-datasets-container {
  padding: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .title {
      font-size: 18px;
      font-weight: 600;
    }
  }

  .progress-info {
    display: flex;
    flex-direction: column;
    gap: 4px;

    .progress-text {
      font-size: 12px;
      color: #606266;
      text-align: center;
    }
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
````

## File: frontend/src/views/document/DataList.vue
````vue
<template>
  <div class="data-list">
    <div class="page-header">
      <div class="header-left">
        <h2>数据列表</h2>
        <p class="page-desc">查看已导入的 KF/QMS/品质案例数据记录</p>
      </div>
    </div>

    <el-card class="processor-card" shadow="never">
      <el-radio-group v-model="currentProcessor">
        <el-radio-button
          v-for="p in processorTabs"
          :key="p.name"
          :value="p.name"
        >
          {{ p.display_name }}
        </el-radio-button>
      </el-radio-group>
    </el-card>

    <el-card class="table-card">
      <el-table
        :data="listData"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column :label="'\u56fe\u7247'" min-width="180">
          <template #default="{ row }">
            <div v-if="getRowImageUrls(row).length" class="image-cell">
              <el-image
                v-for="(img, idx) in getRowImageUrls(row).slice(0, 3)"
                :key="`${row.id}-${idx}`"
                :src="toAbsoluteImageUrl(img)"
                :preview-src-list="getRowImageUrls(row).map((u) => toAbsoluteImageUrl(u))"
                preview-teleported
                fit="cover"
                class="thumb"
              >
                <template #error>
                  <div class="thumb-error">{{ '\u9884\u89c8\u5f02\u5e38' }}</div>
                </template>
              </el-image>
              <span
                v-if="getRowImageUrls(row).length > 3"
                class="image-more"
              >
                +{{ getRowImageUrls(row).length - 3 }}
              </span>
              <span
                v-if="getRowMissingImageCount(row) > 0"
                class="image-missing"
              >
                {{ '\u7f3a\u5931' }}{{ getRowMissingImageCount(row) }}{{ '\u5f20' }}
              </span>
            </div>
            <span
              v-else-if="getRowMissingImageCount(row) > 0"
              class="no-image warning"
            >
              {{ '\u672a\u4e0a\u4f20\u56fe\u7247' }}
            </span>
            <span v-else class="no-image">{{ '\u65e0\u56fe\u7247' }}</span>
          </template>
        </el-table-column>

        <el-table-column
          v-for="col in tableColumns"
          :key="col"
          :prop="col"
          :label="getColumnLabel(col)"
          show-overflow-tooltip
          min-width="140"
        />
      </el-table>

      <el-empty
        v-if="!loading && listData.length === 0"
        description="暂无数据"
      />

      <div class="table-footer">
        <div class="total-hint" v-if="totalCount > 0">
          共 {{ totalCount }} 条记录
        </div>

        <el-pagination
          v-if="totalCount > 0"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalCount"
          :page-size="pageSize"
          :current-page="currentPage"
          :page-sizes="pageSizeOptions"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>
⋮----
{{ p.display_name }}
⋮----
<template #default="{ row }">
            <div v-if="getRowImageUrls(row).length" class="image-cell">
              <el-image
                v-for="(img, idx) in getRowImageUrls(row).slice(0, 3)"
                :key="`${row.id}-${idx}`"
                :src="toAbsoluteImageUrl(img)"
                :preview-src-list="getRowImageUrls(row).map((u) => toAbsoluteImageUrl(u))"
                preview-teleported
                fit="cover"
                class="thumb"
              >
                <template #error>
                  <div class="thumb-error">{{ '\u9884\u89c8\u5f02\u5e38' }}</div>
                </template>
              </el-image>
              <span
                v-if="getRowImageUrls(row).length > 3"
                class="image-more"
              >
                +{{ getRowImageUrls(row).length - 3 }}
              </span>
              <span
                v-if="getRowMissingImageCount(row) > 0"
                class="image-missing"
              >
                {{ '\u7f3a\u5931' }}{{ getRowMissingImageCount(row) }}{{ '\u5f20' }}
              </span>
            </div>
            <span
              v-else-if="getRowMissingImageCount(row) > 0"
              class="no-image warning"
            >
              {{ '\u672a\u4e0a\u4f20\u56fe\u7247' }}
            </span>
            <span v-else class="no-image">{{ '\u65e0\u56fe\u7247' }}</span>
          </template>
⋮----
<template #error>
                  <div class="thumb-error">{{ '\u9884\u89c8\u5f02\u5e38' }}</div>
                </template>
⋮----
<div class="thumb-error">{{ '\u9884\u89c8\u5f02\u5e38' }}</div>
⋮----
+{{ getRowImageUrls(row).length - 3 }}
⋮----
{{ '\u7f3a\u5931' }}{{ getRowMissingImageCount(row) }}{{ '\u5f20' }}
⋮----
{{ '\u672a\u4e0a\u4f20\u56fe\u7247' }}
⋮----
<span v-else class="no-image">{{ '\u65e0\u56fe\u7247' }}</span>
⋮----
共 {{ totalCount }} 条记录
⋮----
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useDocumentStore } from '@/stores/document'
import { documentApi } from '@/api/document'
import { buildBackendUrl } from '@/utils/backendUrl'

const store = useDocumentStore()

const defaultProcessors = [
  { name: 'kf', display_name: 'KF快反' },
  { name: 'qms', display_name: 'QMS质量' },
  { name: 'failure_case', display_name: '品质案例' }
]

const PROCESSOR_COLUMN_LABELS: Record<string, Record<string, string>> = {
  kf: {
    id: '快反编号',
    occurrence_time: '发生时间',
    problem_analysis: '问题原因及分析',
    short_term_measure: '短期改善措施',
    long_term_measure: '长期改善措施',
    classification: '所属分类',
    data_source: '数据源'
  },
  qms: {
    id: '制令单号',
    entry_time: '录入时间',
    model: '型号',
    barcode: '条码',
    position: '位号',
    status: '状态',
    data_source: '数据源'
  },
  failure_case: {
    id: '记录ID',
    source_file: '源文件',
    source_row: '源行号',
    问题分类: '问题分类',
    '客户/发生工程/供应商': '客户/发生工程/供应商',
    质量问题: '质量问题',
    问题描述: '问题描述',
    问题处理: '问题处理',
    原因分析: '原因分析',
    采取措施: '采取措施',
    闂鍒嗙被: '问题分类',
    '瀹㈡埛/鍙戠敓宸ョ▼/渚涘簲鍟?': '客户/发生工程/供应商',
    璐ㄩ噺闂: '质量问题',
    闂鎻忚堪: '问题描述',
    闂澶勭悊: '问题处理',
    鍘熷洜鍒嗘瀽: '原因分析',
    閲囧彇鎺柦: '采取措施',
    data_source: '数据源'
  }
}

const processorTabs = computed(() => {
  return store.processors.length > 0 ? store.processors : defaultProcessors
})

const currentProcessor = computed({
  get: () => store.currentProcessor,
  set: (val) => store.setCurrentProcessor(val)
})

const listData = ref<any[]>([])
const totalCount = ref(0)
const loading = ref(false)

const currentPage = ref(1)
const pageSize = ref(50)
const pageSizeOptions = [20, 50, 100, 200]

const processorFieldMapping = ref<Record<string, string>>({})
const hiddenColumns = new Set([
  'image_paths',
  'image_preview_urls',
  'image_count',
  'image_available_count',
  'image_missing_count'
])

const tableColumns = computed(() => {
  if (listData.value.length === 0) return []
  return Object.keys(listData.value[0]).filter((key) => !hiddenColumns.has(key))
})

function getColumnLabel(column: string) {
  const staticMap = PROCESSOR_COLUMN_LABELS[currentProcessor.value] || {}
  if (staticMap[column]) return staticMap[column]

  if (processorFieldMapping.value[column]) {
    return processorFieldMapping.value[column]
  }

  if (column === 'id' && processorFieldMapping.value.event_id) {
    return processorFieldMapping.value.event_id
  }

  return column
}

function toAbsoluteImageUrl(path: string) {
  if (!path) return ''
  return buildBackendUrl(path)
}

function getRowImageUrls(row: any): string[] {
  if (Array.isArray(row?.image_preview_urls)) {
    return row.image_preview_urls
  }
  if (typeof row?.image_preview_urls === 'string' && row.image_preview_urls.trim()) {
    return [row.image_preview_urls.trim()]
  }
  return []
}

function getRowMissingImageCount(row: any): number {
  if (typeof row?.image_missing_count === 'number' && row.image_missing_count > 0) {
    return row.image_missing_count
  }
  const total = typeof row?.image_count === 'number' ? row.image_count : 0
  const available = getRowImageUrls(row).length
  const missing = total - available
  return missing > 0 ? missing : 0
}

async function loadFieldMapping() {
  try {
    const res = await documentApi.getFieldMapping(store.currentProcessor)
    processorFieldMapping.value = res.field_mapping || {}
  } catch {
    processorFieldMapping.value = {}
  }
}

async function loadList() {
  loading.value = true
  try {
    const res = await documentApi.getDataList(store.currentProcessor, {
      page: currentPage.value,
      page_size: pageSize.value
    })
    listData.value = res.data
    totalCount.value = res.total_count ?? res.count
  } catch (e: any) {
    listData.value = []
    totalCount.value = 0
    ElMessage.error(e?.response?.data?.detail || '加载数据列表失败')
  } finally {
    loading.value = false
  }
}

function handlePageChange(page: number) {
  currentPage.value = page
  loadList()
}

function handleSizeChange(size: number) {
  pageSize.value = size
  currentPage.value = 1
  loadList()
}

onMounted(async () => {
  if (store.processors.length === 0) {
    await store.fetchProcessors()
  }
  await loadFieldMapping()
  await loadList()
})

watch(
  () => store.currentProcessor,
  async () => {
    currentPage.value = 1
    await loadFieldMapping()
    await loadList()
  }
)
</script>
⋮----
<style scoped lang="scss">
.data-list {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;

    .header-left {
      h2 {
        margin: 0 0 8px;
        font-size: 24px;
        color: #303133;
      }

      .page-desc {
        margin: 0;
        font-size: 14px;
        color: #909399;
      }
    }
  }

  .processor-card,
  .table-card {
    margin-bottom: 20px;
  }

  .table-footer {
    margin-top: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .total-hint {
    font-size: 14px;
    color: #909399;
    white-space: nowrap;
  }

  .image-cell {
    display: flex;
    align-items: center;
    gap: 6px;
    min-height: 48px;

    .thumb {
      width: 42px;
      height: 42px;
      border-radius: 4px;
      border: 1px solid #ebeef5;
      overflow: hidden;
      flex-shrink: 0;
    }

    .thumb-error {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
      font-size: 12px;
      color: #909399;
      background: #f5f7fa;
    }

    .image-more {
      font-size: 12px;
      color: #909399;
      white-space: nowrap;
    }

    .image-missing {
      font-size: 12px;
      color: #e6a23c;
      white-space: nowrap;
    }
  }

  .no-image {
    color: #c0c4cc;
    font-size: 13px;

    &.warning {
      color: #e6a23c;
    }
  }
}
</style>
````

## File: frontend/src/views/document/DataStatistics.vue
````vue
<template>
  <div class="data-statistics">
    <div class="page-header">
      <div class="header-left">
        <h2>数据分析</h2>
        <p class="page-desc">KF/QMS/品质案例数据统计与分布概览</p>
      </div>
    </div>

    <el-card class="processor-card" shadow="never">
      <el-radio-group v-model="currentProcessor">
        <el-radio-button
          v-for="p in processorTabs"
          :key="p.name"
          :value="p.name"
        >
          {{ p.display_name }}
        </el-radio-button>
      </el-radio-group>
    </el-card>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <el-statistic title="总事件数" :value="stats?.total_events ?? 0" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <el-statistic title="缺陷类型数" :value="stats?.defect_distribution?.length ?? 0" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <el-statistic title="客户数" :value="stats?.customer_ranking?.length ?? 0" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <el-statistic title="4M分布项" :value="stats?.four_m_distribution?.length ?? 0" />
        </el-card>
      </el-col>
    </el-row>

    <el-card class="distribution-card">
      <template #header>
        <div class="card-header">
          <span>缺陷分布</span>
          <el-button type="default" :icon="Refresh" @click="loadStats">刷新</el-button>
        </div>
      </template>

      <div class="distribution-content">
        <div class="chart-panel">
          <SimplePieChart :data="stats?.defect_distribution ?? []" />
        </div>
        <div class="table-panel">
          <el-table
            :data="stats?.defect_distribution ?? []"
            v-loading="loading"
            stripe
            style="width: 100%"
          >
            <el-table-column prop="name" label="缺陷名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="count" label="数量" width="120" align="center" sortable />
          </el-table>

          <el-empty
            v-if="!loading && (!stats?.defect_distribution || stats.defect_distribution.length === 0)"
            description="暂无数据"
          />
        </div>
      </div>
    </el-card>

    <el-card class="distribution-card" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>客户排名</span>
        </div>
      </template>

      <div class="distribution-content">
        <div class="chart-panel">
          <SimplePieChart :data="stats?.customer_ranking ?? []" />
        </div>
        <div class="table-panel">
          <el-table
            :data="stats?.customer_ranking ?? []"
            v-loading="loading"
            stripe
            style="width: 100%"
          >
            <el-table-column type="index" label="排名" width="70" align="center" />
            <el-table-column prop="name" label="客户名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="count" label="事件数" width="120" align="center" sortable />
          </el-table>

          <el-empty
            v-if="!loading && (!stats?.customer_ranking || stats.customer_ranking.length === 0)"
            description="暂无数据"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>
⋮----
{{ p.display_name }}
⋮----
<template #header>
        <div class="card-header">
          <span>缺陷分布</span>
          <el-button type="default" :icon="Refresh" @click="loadStats">刷新</el-button>
        </div>
      </template>
⋮----
<template #header>
        <div class="card-header">
          <span>客户排名</span>
        </div>
      </template>
⋮----
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { useDocumentStore } from '@/stores/document'
import type { StatisticsData } from '@/types'
import SimplePieChart from '@/components/charts/SimplePieChart.vue'

const store = useDocumentStore()

const defaultProcessors = [
  { name: 'kf', display_name: 'KF快反' },
  { name: 'qms', display_name: 'QMS质量' },
  { name: 'failure_case', display_name: '品质案例' }
]

const processorTabs = computed(() => {
  return store.processors.length > 0 ? store.processors : defaultProcessors
})

const currentProcessor = computed({
  get: () => store.currentProcessor,
  set: (val) => store.setCurrentProcessor(val)
})

const stats = ref<StatisticsData | null>(null)
const loading = ref(false)

async function loadStats() {
  loading.value = true
  try {
    stats.value = await store.getStatistics()
  } catch (e: any) {
    stats.value = null
    ElMessage.error(e?.response?.data?.detail || '加载统计数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (store.processors.length === 0) {
    await store.fetchProcessors()
  }
  await loadStats()
})

watch(
  () => store.currentProcessor,
  () => {
    loadStats()
  }
)
</script>
⋮----
<style scoped lang="scss">
.data-statistics {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;

    .header-left {
      h2 {
        margin: 0 0 8px;
        font-size: 24px;
        color: #303133;
      }

      .page-desc {
        margin: 0;
        font-size: 14px;
        color: #909399;
      }
    }
  }

  .processor-card {
    margin-bottom: 20px;
  }

  .stats-row {
    margin-bottom: 20px;
  }

  .stat-card {
    text-align: center;
  }

  .distribution-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }

    .distribution-content {
      display: flex;
      gap: 20px;
      align-items: flex-start;
    }

    .chart-panel {
      width: 380px;
      flex-shrink: 0;
    }

    .table-panel {
      flex: 1;
      min-width: 0;
    }
  }

  @media (max-width: 1200px) {
    .distribution-card {
      .distribution-content {
        flex-direction: column;
      }

      .chart-panel {
        width: 100%;
      }
    }
  }
}
</style>
````

## File: frontend/src/views/document/DocumentImport.vue
````vue
<template>
  <div class="document-import">
    <div class="page-header">
      <div class="header-left">
        <h2>文档导入</h2>
        <p class="page-desc">上传 Excel 文件并导入 KF、QMS、品质失效案例数据。</p>
      </div>
    </div>

    <el-card class="processor-card" shadow="never">
      <el-radio-group v-model="currentProcessor" @change="handleProcessorChange">
        <el-radio-button
          v-for="processor in processorTabs"
          :key="processor.name"
          :value="processor.name"
        >
          {{ processor.display_name }}
        </el-radio-button>
      </el-radio-group>
    </el-card>

    <el-card class="format-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>{{ currentFormatTip.title }}</span>
        </div>
      </template>

      <el-alert
        type="info"
        :closable="false"
        :description="currentFormatTip.description"
      />

      <div class="format-fields">
        <div class="format-label">必填字段：</div>
        <el-tag
          v-for="field in currentFormatTip.requiredFields"
          :key="field"
          class="field-tag"
          effect="plain"
          type="primary"
        >
          {{ field }}
        </el-tag>
      </div>

      <div v-if="currentFormatTip.aliasTip" class="alias-tip">
        <el-text type="warning">{{ currentFormatTip.aliasTip }}</el-text>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="upload-card">
          <template #header>
            <div class="card-header">
              <span>上传 Excel 文件</span>
            </div>
          </template>

          <el-upload
            ref="uploadRef"
            class="excel-uploader"
            :auto-upload="false"
            :limit="1"
            accept=".xlsx,.xls"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
          >
            <el-button type="primary">选择 Excel 文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 `.xlsx`、`.xls` 格式</div>
            </template>
          </el-upload>

          <el-button
            type="success"
            class="upload-btn"
            :loading="store.isUploading"
            :disabled="!selectedFile"
            @click="handleUpload"
          >
            上传并处理
          </el-button>

          <div v-if="excelProgressVisible" class="transfer-progress">
            <el-progress
              :percentage="store.excelUploadProgress.percentage"
              :status="excelProgressStatus"
              :stroke-width="8"
              :show-text="false"
            />
            <p class="progress-text">{{ excelProgressText }}</p>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="files-card">
          <template #header>
            <div class="card-header">
              <span>已处理文件</span>
              <el-button
                type="default"
                :icon="Refresh"
                @click="handleRefreshFiles"
              >
                刷新
              </el-button>
            </div>
          </template>

          <el-table
            :data="store.processedFiles"
            v-loading="store.loading"
            stripe
            style="width: 100%"
          >
            <el-table-column prop="filename" label="文件名" min-width="160" show-overflow-tooltip />
            <el-table-column prop="data_source" label="数据源" width="120" show-overflow-tooltip />
            <el-table-column prop="table_count" label="表格数" width="80" align="center" />
            <el-table-column prop="processed_time" label="处理时间" width="160" show-overflow-tooltip />
            <el-table-column label="操作" width="90" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="danger"
                  size="small"
                  @click="handleDelete(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-empty
            v-if="!store.loading && store.processedFiles.length === 0"
            description="暂无已处理文件"
          />
        </el-card>
      </el-col>
    </el-row>

    <el-card v-if="currentProcessor === 'qms'" class="images-card">
      <template #header>
        <div class="card-header">
          <span>图片上传</span>
        </div>
      </template>

      <el-alert
        type="info"
        :closable="false"
        description="QMS Excel 中的图片按文件名外链引用，需要单独上传 ZIP 压缩包。数据源标识必须与 Excel 文件名规范化后的数据源完全一致，导出时才能正确匹配图片。"
        style="margin-bottom: 12px"
      />

      <el-space wrap>
        <el-input
          v-model="imageDataSource"
          placeholder="请输入数据源标识"
          style="width: 220px"
        />
        <el-upload
          ref="imageUploadRef"
          class="image-uploader"
          :auto-upload="false"
          :limit="1"
          accept=".zip"
          :on-change="handleImageFileChange"
          :on-remove="handleImageFileRemove"
        >
          <el-button>选择 ZIP 文件</el-button>
          <template #tip>
            <span class="el-upload__tip">上传图片压缩包（`.zip`）</span>
          </template>
        </el-upload>
        <el-button
          type="warning"
          :disabled="!selectedImageFile || !imageDataSource"
          :loading="store.isImageUploading"
          @click="handleImageUpload"
        >
          上传图片
        </el-button>
        <el-button
          :disabled="!imageDataSource"
          :icon="Refresh"
          @click="handleQueryImages"
        >
          查询图片
        </el-button>
      </el-space>

      <div v-if="imageProgressVisible" class="transfer-progress">
        <el-progress
          :percentage="store.imageUploadProgress.percentage"
          :status="imageProgressStatus"
          :stroke-width="8"
          :show-text="false"
        />
        <p class="progress-text">{{ imageProgressText }}</p>
      </div>

      <div v-if="imageUploadStatus" class="status-alert">
        <el-alert
          :type="imageUploadStatus.type"
          :title="imageUploadStatus.message"
          :closable="false"
          show-icon
        />
      </div>
    </el-card>
  </div>
</template>
⋮----
{{ processor.display_name }}
⋮----
<template #header>
        <div class="card-header">
          <span>{{ currentFormatTip.title }}</span>
        </div>
      </template>
⋮----
<span>{{ currentFormatTip.title }}</span>
⋮----
{{ field }}
⋮----
<el-text type="warning">{{ currentFormatTip.aliasTip }}</el-text>
⋮----
<template #header>
            <div class="card-header">
              <span>上传 Excel 文件</span>
            </div>
          </template>
⋮----
<template #tip>
              <div class="el-upload__tip">支持 `.xlsx`、`.xls` 格式</div>
            </template>
⋮----
<p class="progress-text">{{ excelProgressText }}</p>
⋮----
<template #header>
            <div class="card-header">
              <span>已处理文件</span>
              <el-button
                type="default"
                :icon="Refresh"
                @click="handleRefreshFiles"
              >
                刷新
              </el-button>
            </div>
          </template>
⋮----
<template #default="{ row }">
                <el-button
                  type="danger"
                  size="small"
                  @click="handleDelete(row)"
                >
                  删除
                </el-button>
              </template>
⋮----
<template #header>
        <div class="card-header">
          <span>图片上传</span>
        </div>
      </template>
⋮----
<template #tip>
            <span class="el-upload__tip">上传图片压缩包（`.zip`）</span>
          </template>
⋮----
<p class="progress-text">{{ imageProgressText }}</p>
⋮----
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { useDocumentStore } from '@/stores/document'
import { documentApi } from '@/api/document'
import type { UploadFile } from 'element-plus'

const store = useDocumentStore()
const router = useRouter()

const defaultProcessors = [
  { name: 'kf', display_name: 'KF快反' },
  { name: 'qms', display_name: 'QMS质量' },
  { name: 'failure_case', display_name: '品质案例' }
]

const processorTabs = computed(() => {
  return store.processors.length > 0 ? store.processors : defaultProcessors
})

const currentProcessor = computed({
  get: () => store.currentProcessor,
  set: (value: string) => store.setCurrentProcessor(value)
})

interface FormatTip {
  title: string
  description: string
  requiredFields: string[]
  aliasTip?: string
}

const formatTips: Record<string, FormatTip> = {
  kf: {
    title: 'KF 快反文件格式要求',
    description: '请上传快反问题记录 Excel，字段名需与系统要求一致。',
    requiredFields: [
      '快反编号',
      '发生时间',
      '问题原因及分析',
      '问题图片',
      '短期改善措施',
      '长期改善措施',
      '所属分类',
      '客户名称',
      '产品型号',
      '缺陷类型不良现象'
    ],
    aliasTip: '兼容常见旧字段别名，例如：短期措施 -> 短期改善措施，长期措施 -> 长期改善措施，问题描述 -> 问题原因及分析。'
  },
  qms: {
    title: 'QMS 不合格品文件格式要求',
    description: '请上传 QMS 不合格品 Excel，需包含完整的质量追溯字段。',
    requiredFields: [
      '制令单号',
      '录入时间',
      '客户名称',
      '型号',
      '条码',
      '位号',
      '车间',
      '产线',
      '岗位',
      '不良项目',
      '质检节点',
      '状态',
      '照片'
    ]
  },
  failure_case: {
    title: '品质失效案例文件格式要求',
    description: '请上传品质失效案例 Excel，系统会自动识别并规范化同义字段。',
    requiredFields: [
      '问题分类',
      '客户/发生工程/供应商',
      '质量问题',
      '问题描述',
      '问题处理',
      '原因分析',
      '采取措施'
    ],
    aliasTip: '第二列支持同义表头：问题来源、供应商、客户；上传后会统一为“客户/发生工程/供应商”。'
  }
}

const defaultFormatTip: FormatTip = {
  title: '文件格式要求',
  description: '请按当前处理器对应字段准备 Excel 后再上传。',
  requiredFields: []
}

const currentFormatTip = computed<FormatTip>(() => {
  return formatTips[currentProcessor.value] || defaultFormatTip
})

const uploadRef = ref()
const imageUploadRef = ref()
const selectedFile = ref<File | null>(null)
const selectedImageFile = ref<File | null>(null)
const imageDataSource = ref('')
const imageUploadStatus = ref<{ type: 'success' | 'warning' | 'info'; message: string } | null>(null)

const formatBytes = (bytes?: number | null) => {
  if (!bytes || bytes <= 0) {
    return '0 B'
  }

  const units = ['B', 'KB', 'MB', 'GB']
  let value = bytes
  let unitIndex = 0

  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024
    unitIndex += 1
  }

  return `${value.toFixed(value >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`
}

const resolveProgressStatus = (phase: string): 'success' | 'exception' | undefined => {
  if (phase === 'success') return 'success'
  if (phase === 'exception') return 'exception'
  return undefined
}

const buildUploadProgressText = (
  state: { loaded: number; total: number | null; percentage: number; phase: string; message: string },
  processingText: string
) => {
  if (state.phase === 'uploading') {
    if (state.total) {
      return `已上传 ${formatBytes(state.loaded)} / ${formatBytes(state.total)} (${state.percentage}%)`
    }

    return `已上传 ${formatBytes(state.loaded)}`
  }

  if (state.phase === 'processing') {
    return state.message || processingText
  }

  return state.message
}

const excelProgressVisible = computed(() => store.excelUploadProgress.phase !== 'idle')
const excelProgressStatus = computed(() => resolveProgressStatus(store.excelUploadProgress.phase))
const excelProgressText = computed(() => buildUploadProgressText(store.excelUploadProgress, '文件已上传，正在等待服务器处理...'))

const imageProgressVisible = computed(() => store.imageUploadProgress.phase !== 'idle')
const imageProgressStatus = computed(() => resolveProgressStatus(store.imageUploadProgress.phase))
const imageProgressText = computed(() => buildUploadProgressText(store.imageUploadProgress, '压缩包已上传，正在等待服务器处理...'))

const handleFileChange = (file: UploadFile) => {
  selectedFile.value = file.raw || null
  store.resetExcelUploadProgress()
}

const handleFileRemove = () => {
  selectedFile.value = null
  store.resetExcelUploadProgress()
}

const resetExcelSelection = () => {
  selectedFile.value = null
  uploadRef.value?.clearFiles?.()
}

const handleUpload = async () => {
  if (!selectedFile.value) return

  try {
    const result = await store.uploadExcel(selectedFile.value)
    resetExcelSelection()

    if (!result.success) {
      ElMessage.error(result.message || '上传失败')
      return
    }

    if (store.currentProcessor === 'failure_case' && result.corpus_count && result.corpus_count > 0) {
      ElMessage.success(`上传成功，已生成 ${result.corpus_count} 条语料记录`)

      try {
        await ElMessageBox.confirm(
          `已为品质失效案例生成 ${result.corpus_count} 条语料记录，是否现在前往语料管理页面查看？`,
          '语料已就绪',
          {
            confirmButtonText: '前往语料管理',
            cancelButtonText: '稍后再去',
            type: 'success'
          }
        )

        router.push({ name: 'corpus' })
      } catch {
        // 用户取消跳转
      }

      return
    }

    ElMessage.success(result.message || '上传成功')
  } catch (error: any) {
    ElMessage.error(error?.message || '上传失败')
  }
}

const handleProcessorChange = async (value: string) => {
  await store.setCurrentProcessor(value)
  store.resetExcelUploadProgress()
  store.resetImageUploadProgress()
  imageUploadStatus.value = null
}

const handleRefreshFiles = () => {
  store.fetchProcessedFiles()
}

const handleDelete = async (row: { data_source: string }) => {
  try {
    await ElMessageBox.confirm(
      `确认彻底删除数据源“${row.data_source}”吗？这会同时删除处理文件、图片目录以及数据库中的相关记录，操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const result = await documentApi.deleteProcessedFile(store.currentProcessor, row.data_source)

    if (result.success) {
      ElMessage.success(result.message || '删除成功')
      store.fetchProcessedFiles()
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error?.message || '删除失败')
    }
  }
}

const handleImageFileChange = (file: UploadFile) => {
  selectedImageFile.value = file.raw || null
  store.resetImageUploadProgress()
}

const handleImageFileRemove = () => {
  selectedImageFile.value = null
  store.resetImageUploadProgress()
}

const resetImageSelection = () => {
  selectedImageFile.value = null
  imageUploadRef.value?.clearFiles?.()
}

const handleImageUpload = async () => {
  if (!selectedImageFile.value || !imageDataSource.value) return

  imageUploadStatus.value = null

  try {
    const result = await store.uploadImagesZip(selectedImageFile.value, imageDataSource.value)

    if (result.success) {
      imageUploadStatus.value = {
        type: 'success',
        message: result.message || '图片上传成功'
      }
      resetImageSelection()
    } else {
      imageUploadStatus.value = {
        type: 'warning',
        message: result.message || '图片上传失败'
      }
    }
  } catch (error: any) {
    imageUploadStatus.value = {
      type: 'warning',
      message: error?.message || '图片上传失败'
    }
  }
}

const handleQueryImages = async () => {
  if (!imageDataSource.value) return

  try {
    const result = await documentApi.getImagesInfo(imageDataSource.value)

    if (result.count > 0) {
      imageUploadStatus.value = {
        type: 'success',
        message: `当前已有 ${result.count} 张图片`
      }
    } else {
      imageUploadStatus.value = {
        type: 'info',
        message: '当前目录下暂无图片'
      }
    }
  } catch {
    imageUploadStatus.value = {
      type: 'warning',
      message: '查询失败'
    }
  }
}

onMounted(() => {
  store.fetchProcessors()
  store.fetchProcessedFiles()
})
</script>
⋮----
<style scoped lang="scss">
.document-import {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;

    .header-left {
      h2 {
        margin: 0 0 8px;
        font-size: 24px;
        color: #303133;
      }

      .page-desc {
        margin: 0;
        font-size: 14px;
        color: #909399;
      }
    }
  }

  .processor-card {
    margin-bottom: 20px;
  }

  .format-card {
    margin-bottom: 20px;

    .format-fields {
      margin-top: 12px;
      display: flex;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 8px;

      .format-label {
        color: #606266;
        font-size: 14px;
        line-height: 28px;
      }

      .field-tag {
        margin: 0;
      }
    }

    .alias-tip {
      margin-top: 10px;
    }
  }

  .upload-card,
  .files-card,
  .images-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }
  }

  .excel-uploader {
    margin-bottom: 12px;
  }

  .upload-btn {
    width: 100%;
  }

  .image-uploader {
    display: inline-block;
  }

  .transfer-progress {
    margin-top: 14px;
    padding: 12px 14px;
    border-radius: 8px;
    background: #f5f7fa;

    .progress-text {
      margin: 10px 0 0;
      color: #606266;
      font-size: 13px;
      line-height: 1.5;
    }
  }

  .status-alert {
    margin-top: 12px;
  }
}
</style>
````

## File: frontend/src/views/Home.vue
````vue
<template>
  <div class="home-page">
    <el-card class="welcome-card">
      <template #header>
        <h2>欢迎使用面向离散型电子信息制造业的多模态语料库构建平台</h2>
      </template>
      
      <div class="user-info">
        <p>当前用户: <strong>{{ authStore.user?.username }}</strong></p>
        <p>角色: <el-tag :type="roleTagType">{{ roleText }}</el-tag></p>
      </div>
      
      <el-divider />
      
      <div class="quick-actions">
        <h3>快速访问</h3>
        <div class="action-grid">
          <!-- 管理员和标注员 -->
          <el-card v-if="canAccessCorpus" shadow="hover" class="action-card" @click="goTo('/corpus')">
            <el-icon class="action-icon"><Document /></el-icon>
            <div class="action-title">语料管理</div>
            <div class="action-desc">上传和管理语料数据</div>
          </el-card>
          
          <!-- 所有角色 -->
          <el-card shadow="hover" class="action-card" @click="goTo('/datasets')">
            <el-icon class="action-icon"><Folder /></el-icon>
            <div class="action-title">数据集管理</div>
            <div class="action-desc">{{ authStore.user?.role === 'viewer' ? '查看和导出数据集' : '创建和管理数据集' }}</div>
          </el-card>
          
          <!-- 管理员和标注员 -->
          <el-card v-if="canAccessLabels" shadow="hover" class="action-card" @click="goTo('/labels')">
            <el-icon class="action-icon"><PriceTag /></el-icon>
            <div class="action-title">标签配置</div>
            <div class="action-desc">配置实体和关系标签</div>
          </el-card>
          
          <!-- 管理员和标注员 -->
          <el-card v-if="canAccessAnnotations" shadow="hover" class="action-card" @click="goTo('/annotations')">
            <el-icon class="action-icon"><Edit /></el-icon>
            <div class="action-title">标注任务</div>
            <div class="action-desc">进行实体关系标注</div>
          </el-card>
          
          <!-- 管理员和标注员 -->
          <el-card v-if="canAccessReview" shadow="hover" class="action-card" @click="goTo('/review')">
            <el-icon class="action-icon"><Check /></el-icon>
            <div class="action-title">复核管理</div>
            <div class="action-desc">复核标注结果</div>
          </el-card>
          
          <!-- 仅管理员 -->
          <el-card v-if="isAdmin" shadow="hover" class="action-card" @click="goTo('/users')">
            <el-icon class="action-icon"><User /></el-icon>
            <div class="action-title">用户管理</div>
            <div class="action-desc">管理系统用户</div>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>
⋮----
<template #header>
        <h2>欢迎使用面向离散型电子信息制造业的多模态语料库构建平台</h2>
      </template>
⋮----
<p>当前用户: <strong>{{ authStore.user?.username }}</strong></p>
<p>角色: <el-tag :type="roleTagType">{{ roleText }}</el-tag></p>
⋮----
<!-- 管理员和标注员 -->
⋮----
<!-- 所有角色 -->
⋮----
<div class="action-desc">{{ authStore.user?.role === 'viewer' ? '查看和导出数据集' : '创建和管理数据集' }}</div>
⋮----
<!-- 管理员和标注员 -->
⋮----
<!-- 管理员和标注员 -->
⋮----
<!-- 管理员和标注员 -->
⋮----
<!-- 仅管理员 -->
⋮----
<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Document, Folder, PriceTag, Edit, Check, User } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const roleText = computed(() => {
  const roleMap: Record<string, string> = {
    admin: '管理员',
    annotator: '标注员',
    viewer: '浏览员'
  }
  return roleMap[authStore.user?.role || ''] || authStore.user?.role
})

const roleTagType = computed(() => {
  const typeMap: Record<string, any> = {
    admin: 'danger',
    annotator: 'success',
    viewer: 'info'
  }
  return typeMap[authStore.user?.role || ''] || 'info'
})

const isAdmin = computed(() => authStore.user?.role === 'admin')
const canAccessCorpus = computed(() => ['admin', 'annotator'].includes(authStore.user?.role || ''))
const canAccessLabels = computed(() => ['admin', 'annotator'].includes(authStore.user?.role || ''))
const canAccessAnnotations = computed(() => ['admin', 'annotator'].includes(authStore.user?.role || ''))
const canAccessReview = computed(() => ['admin', 'annotator'].includes(authStore.user?.role || ''))

const goTo = (path: string) => {
  router.push(path)
}
</script>
⋮----
<style scoped lang="scss">
.home-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;

  .welcome-card {
    h2 {
      margin: 0;
      color: #303133;
    }
  }

  .user-info {
    padding: 16px 0;
    
    p {
      margin: 8px 0;
      font-size: 14px;
      color: #606266;
      
      strong {
        color: #303133;
        font-size: 16px;
      }
    }
  }

  .quick-actions {
    h3 {
      margin: 0 0 20px;
      color: #303133;
      font-size: 18px;
    }

    .action-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 16px;

      .action-card {
        cursor: pointer;
        text-align: center;
        padding: 24px 16px;
        transition: all 0.3s;

        &:hover {
          transform: translateY(-4px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .action-icon {
          font-size: 48px;
          color: #409eff;
          margin-bottom: 12px;
        }

        .action-title {
          font-size: 16px;
          font-weight: 600;
          color: #303133;
          margin-bottom: 8px;
        }

        .action-desc {
          font-size: 13px;
          color: #909399;
          line-height: 1.5;
        }
      }
    }
  }
}
</style>
````

## File: frontend/src/views/label/LabelConfig.vue
````vue
<template>
  <div class="label-config">
    <h2>标签配置</h2>
    <p>任务32：标签配置页面实现（待开发）</p>
  </div>
</template>
⋮----
<script setup lang="ts">
// 任务32将实现此页面
</script>
⋮----
<style scoped>
.label-config {
  padding: 20px;
}
</style>
````

## File: frontend/src/views/label/LabelManagement.vue
````vue
<template>
  <div class="label-management">
    <el-page-header @back="$router.back()" title="返回">
      <template #content>
        <span class="page-title">标签体系管理</span>
      </template>
      <template #extra>
        <el-space>
          <el-button @click="handleImport">导入配置</el-button>
          <el-button @click="handleExport">导出配置</el-button>
          <el-button type="primary" @click="handlePromptPreview">Prompt预览</el-button>
        </el-space>
      </template>
    </el-page-header>

    <el-tabs v-model="activeTab" class="label-tabs">
      <el-tab-pane label="实体类型" name="entity">
        <EntityTypeConfig />
      </el-tab-pane>
      <el-tab-pane label="关系类型" name="relation">
        <RelationTypeConfig />
      </el-tab-pane>
      <el-tab-pane label="版本管理" name="version">
        <VersionManager />
      </el-tab-pane>
    </el-tabs>

    <!-- 导入对话框 -->
    <LabelImportExport
      v-model:visible="importDialogVisible"
      mode="import"
      @success="handleImportSuccess"
    />

    <!-- Prompt预览对话框 -->
    <PromptPreview
      v-model:visible="promptPreviewVisible"
    />
  </div>
</template>
⋮----
<template #content>
        <span class="page-title">标签体系管理</span>
      </template>
<template #extra>
        <el-space>
          <el-button @click="handleImport">导入配置</el-button>
          <el-button @click="handleExport">导出配置</el-button>
          <el-button type="primary" @click="handlePromptPreview">Prompt预览</el-button>
        </el-space>
      </template>
⋮----
<!-- 导入对话框 -->
⋮----
<!-- Prompt预览对话框 -->
⋮----
<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import EntityTypeConfig from '@/components/label/EntityTypeConfig.vue'
import RelationTypeConfig from '@/components/label/RelationTypeConfig.vue'
import VersionManager from '@/components/label/VersionManager.vue'
import LabelImportExport from '@/components/label/LabelImportExport.vue'
import PromptPreview from '@/components/label/PromptPreview.vue'

const labelStore = useLabelStore()
const activeTab = ref('entity')
const importDialogVisible = ref(false)
const promptPreviewVisible = ref(false)

const handleImport = () => {
  importDialogVisible.value = true
}

const handleExport = async () => {
  try {
    const data = await labelStore.exportLabels()
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `label-config-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handlePromptPreview = () => {
  promptPreviewVisible.value = true
}

const handleImportSuccess = () => {
  ElMessage.success('导入成功')
}
</script>
⋮----
<style scoped>
.label-management {
  padding: 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 500;
}

.label-tabs {
  margin-top: 20px;
}
</style>
````

## File: frontend/src/views/Login.vue
````vue
<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>面向离散型电子信息制造业的多模态语料库构建平台</h2>
          <p>Multimodal Corpus Construction Platform for Discrete Electronic Information Manufacturing Industry</p>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="loginForm"
        :rules="rules"
        label-width="80px"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            clearable
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            style="width: 100%"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <div class="tips">
        <p>测试账号：admin / admin123</p>
      </div>
    </el-card>
  </div>
</template>
⋮----
<template #header>
        <div class="card-header">
          <h2>面向离散型电子信息制造业的多模态语料库构建平台</h2>
          <p>Multimodal Corpus Construction Platform for Discrete Electronic Information Manufacturing Industry</p>
        </div>
      </template>
⋮----
<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await authStore.login(loginForm.username, loginForm.password)
      ElMessage.success('登录成功')

      const redirect = route.query.redirect as string
      router.push(redirect || '/')
    } catch (error: any) {
      ElMessage.error(error.message || '登录失败')
    } finally {
      loading.value = false
    }
  })
}
</script>
⋮----
<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
}

.card-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.tips {
  text-align: center;
  color: #909399;
  font-size: 12px;
  margin-top: 16px;
}

.tips p {
  margin: 4px 0;
}
</style>
````

## File: frontend/src/views/multimodal/MultimodalExport.vue
````vue
<template>
  <div class="multimodal-export">
    <div class="page-header">
      <h2>多模态格式转换</h2>
      <p class="page-desc">独立导出 KF、QMS、品质失效案例数据，支持实体文本、CLIP 对齐、QA 对齐三种格式。</p>
    </div>

    <el-card class="processor-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>选择数据类型</span>
        </div>
      </template>

      <el-radio-group v-model="currentProcessor" @change="handleProcessorChange">
        <el-radio-button
          v-for="processor in processorTabs"
          :key="processor.name"
          :value="processor.name"
        >
          {{ processor.display_name }}
        </el-radio-button>
      </el-radio-group>
    </el-card>

    <el-card class="sources-card">
      <template #header>
        <div class="card-header">
          <span>选择导出数据源</span>
          <el-space>
            <el-button @click="selectAllSources">全选</el-button>
            <el-button @click="clearSources">清空</el-button>
            <el-button type="primary" :icon="Refresh" @click="refreshSources">刷新</el-button>
          </el-space>
        </div>
      </template>

      <el-checkbox-group v-model="selectedDataSources" class="sources-group">
        <el-checkbox
          v-for="file in store.processedFiles"
          :key="file.data_source"
          :label="file.data_source"
          class="source-item"
        >
          <div class="source-title">{{ file.filename }}</div>
          <div class="source-meta">数据源：{{ file.data_source }} | 记录数：{{ file.table_count }}</div>
        </el-checkbox>
      </el-checkbox-group>

      <el-empty
        v-if="!store.loading && store.processedFiles.length === 0"
        description="当前处理器暂无可导出的已处理文件"
      />
    </el-card>

    <el-card class="formats-card">
      <template #header>
        <div class="card-header">
          <span>导出格式配置</span>
        </div>
      </template>

      <el-form label-width="110px">
        <el-form-item label="导出格式">
          <el-checkbox-group v-model="exportFormats">
            <el-checkbox label="entity_text">实体文本</el-checkbox>
            <el-checkbox label="clip_alignment">CLIP 对齐</el-checkbox>
            <el-checkbox label="qa_alignment">QA 对齐</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="包含图片">
          <el-switch v-model="includeImages" />
        </el-form-item>
      </el-form>

      <el-alert
        type="info"
        :closable="false"
        description="系统会按当前数据类型与所选数据源批量导出，并打包为 ZIP 下载。当前进度优先显示真实传输字节；服务器打包阶段会单独提示。"
      />

      <el-button
        type="primary"
        class="export-btn"
        :loading="store.isExporting"
        :disabled="exportFormats.length === 0 || selectedDataSources.length === 0"
        @click="handleBatchExport"
      >
        开始导出
      </el-button>

      <div v-if="exportProgressVisible" class="transfer-progress">
        <el-progress
          :percentage="store.exportProgress.percentage"
          :status="exportProgressStatus"
          :stroke-width="8"
          :show-text="false"
        />
        <p class="progress-text">{{ exportProgressText }}</p>
      </div>
    </el-card>
  </div>
</template>
⋮----
<template #header>
        <div class="card-header">
          <span>选择数据类型</span>
        </div>
      </template>
⋮----
{{ processor.display_name }}
⋮----
<template #header>
        <div class="card-header">
          <span>选择导出数据源</span>
          <el-space>
            <el-button @click="selectAllSources">全选</el-button>
            <el-button @click="clearSources">清空</el-button>
            <el-button type="primary" :icon="Refresh" @click="refreshSources">刷新</el-button>
          </el-space>
        </div>
      </template>
⋮----
<div class="source-title">{{ file.filename }}</div>
<div class="source-meta">数据源：{{ file.data_source }} | 记录数：{{ file.table_count }}</div>
⋮----
<template #header>
        <div class="card-header">
          <span>导出格式配置</span>
        </div>
      </template>
⋮----
<p class="progress-text">{{ exportProgressText }}</p>
⋮----
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { useDocumentStore } from '@/stores/document'
import type { ExportFormat } from '@/types'

const store = useDocumentStore()

const defaultProcessors = [
  { name: 'kf', display_name: 'KF快反' },
  { name: 'qms', display_name: 'QMS质量' },
  { name: 'failure_case', display_name: '品质案例' }
]

const processorTabs = computed(() => {
  return store.processors.length > 0 ? store.processors : defaultProcessors
})

const currentProcessor = computed({
  get: () => store.currentProcessor,
  set: (value: string) => store.setCurrentProcessor(value)
})

const selectedDataSources = ref<string[]>([])
const exportFormats = ref<ExportFormat[]>(['entity_text'])
const includeImages = ref(false)

const formatBytes = (bytes?: number | null) => {
  if (!bytes || bytes <= 0) {
    return '0 B'
  }

  const units = ['B', 'KB', 'MB', 'GB']
  let value = bytes
  let unitIndex = 0

  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024
    unitIndex += 1
  }

  return `${value.toFixed(value >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`
}

const resolveProgressStatus = (phase: string): 'success' | 'exception' | undefined => {
  if (phase === 'success') return 'success'
  if (phase === 'exception') return 'exception'
  return undefined
}

const exportProgressVisible = computed(() => store.exportProgress.phase !== 'idle')
const exportProgressStatus = computed(() => resolveProgressStatus(store.exportProgress.phase))
const exportProgressText = computed(() => {
  const state = store.exportProgress

  if (state.phase === 'processing') {
    return state.message || '正在打包导出文件...'
  }

  if (state.phase === 'downloading') {
    if (state.total) {
      return `已下载 ${formatBytes(state.loaded)} / ${formatBytes(state.total)} (${state.percentage}%)`
    }

    return `正在接收导出文件，已下载 ${formatBytes(state.loaded)}`
  }

  return state.message
})

const resetSelectedSources = () => {
  selectedDataSources.value = store.processedFiles.map(file => file.data_source)
}

const handleProcessorChange = async (value: string) => {
  await store.setCurrentProcessor(value)
  store.resetExportProgress()
  resetSelectedSources()
}

const refreshSources = async () => {
  await store.fetchProcessedFiles()
  resetSelectedSources()
}

const selectAllSources = () => {
  resetSelectedSources()
}

const clearSources = () => {
  selectedDataSources.value = []
}

const downloadBlob = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

const handleBatchExport = async () => {
  try {
    const blob = await store.batchExport({
      formats: exportFormats.value,
      data_sources: selectedDataSources.value,
      include_images: includeImages.value
    })

    downloadBlob(blob, `${store.currentProcessor}_corpus_${Date.now()}.zip`)
    ElMessage.success('导出成功')
  } catch (error: any) {
    ElMessage.error(error?.message || '导出失败')
  }
}

onMounted(async () => {
  await store.fetchProcessors()
  await store.fetchProcessedFiles()
  store.resetExportProgress()
  resetSelectedSources()
})
</script>
⋮----
<style scoped lang="scss">
.multimodal-export {
  padding: 20px;

  .page-header {
    margin-bottom: 20px;

    h2 {
      margin: 0 0 8px;
      font-size: 24px;
      color: #303133;
    }

    .page-desc {
      margin: 0;
      font-size: 14px;
      color: #909399;
    }
  }

  .processor-card,
  .sources-card,
  .formats-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }
  }

  .sources-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 8px;

    .source-item {
      margin-right: 0;
      padding: 8px 10px;
      border: 1px solid #ebeef5;
      border-radius: 6px;
      background: #fafafa;
    }

    .source-title {
      font-weight: 600;
      color: #303133;
    }

    .source-meta {
      margin-top: 4px;
      font-size: 12px;
      color: #909399;
    }
  }

  .export-btn {
    margin-top: 16px;
    width: 100%;
  }

  .transfer-progress {
    margin-top: 14px;
    padding: 12px 14px;
    border-radius: 8px;
    background: #f5f7fa;

    .progress-text {
      margin: 10px 0 0;
      color: #606266;
      font-size: 13px;
      line-height: 1.5;
    }
  }
}
</style>
````

## File: frontend/src/views/NotFound.vue
````vue
<template>
  <div class="not-found">
    <el-result
      icon="warning"
      title="404"
      sub-title="抱歉，您访问的页面不存在"
    >
      <template #extra>
        <el-button type="primary" @click="goHome">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>
⋮----
<template #extra>
        <el-button type="primary" @click="goHome">返回首页</el-button>
      </template>
⋮----
<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>
⋮----
<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}
</style>
````

## File: frontend/src/views/review/ReviewDetail.vue
````vue
<template>
  <div class="review-detail-page">
    <!-- 加载状态 -->
    <el-loading v-if="loading" fullscreen text="加载复核任务数据中..." />
    
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <el-divider direction="vertical" />
        <h2>复核任务 #{{ reviewId }}</h2>
        <el-tag :type="getStatusType(reviewStatus)" size="small">
          {{ getStatusText(reviewStatus) }}
        </el-tag>
      </div>

      <div class="header-right">
        <el-button-group v-if="reviewStatus === 'pending'">
          <el-button type="danger" @click="handleReject" :loading="submitting">
            <el-icon><Close /></el-icon>
            驳回
          </el-button>
          <el-button type="success" @click="handleApprove" :loading="submitting">
            <el-icon><Check /></el-icon>
            批准
          </el-button>
        </el-button-group>
        <el-tag v-else :type="getStatusType(reviewStatus)" size="large">
          {{ getStatusText(reviewStatus) }}
        </el-tag>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="page-content">
      <!-- 左侧：标注查看器 -->
      <div class="viewer-section">
        <el-tabs v-model="activeTab" class="viewer-tabs">
          <!-- 文本标注 -->
          <el-tab-pane label="文本标注" name="text">
            <TextAnnotationEditor
              v-if="corpusText"
              :text="corpusText"
              :entities="textEntities"
              :relations="relations"
              :entity-types="entityTypes"
              :relation-types="relationTypes"
              :readonly="reviewStatus !== 'pending'"
              @add-entity="handleAddTextEntity"
              @update-entity="handleUpdateTextEntity"
              @delete-entity="handleDeleteTextEntity"
              @add-relation="handleAddRelation"
              @delete-relation="handleDeleteRelation"
            />
            <el-empty v-else description="无文本内容" />
          </el-tab-pane>

          <!-- 图片标注 -->
          <el-tab-pane
            v-for="image in images"
            :key="image.id"
            :label="`图片 ${image.id}`"
            :name="`image-${image.id}`"
          >
            <ImageAnnotationEditor
              :image-url="image.url"
              :whole-image-entities="getImageEntities(image.id)"
              :bboxes="getImageBBoxes(image.id)"
              :entity-types="entityTypes"
              :readonly="reviewStatus !== 'pending'"
              @add-whole-image-entity="(entity) => handleAddWholeImageEntity(image.id, entity)"
              @delete-whole-image-entity="(id) => handleDeleteWholeImageEntity(image.id, id)"
              @add-bbox="(bbox) => handleAddBBox(image.id, bbox)"
              @update-bbox="(id, bbox) => handleUpdateBBox(image.id, id, bbox)"
              @delete-bbox="(id) => handleDeleteBBox(image.id, id)"
            />
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 右侧：复核信息面板 -->
      <div class="info-panel">
        <!-- 复核信息 -->
        <el-card class="info-card">
          <template #header>
            <span>复核信息</span>
          </template>
          <div class="info-item">
            <span class="label">复核ID:</span>
            <span class="value">{{ reviewId }}</span>
          </div>
          <div class="info-item">
            <span class="label">标注任务ID:</span>
            <span class="value">{{ taskId || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="label">状态:</span>
            <span class="value">{{ getStatusText(reviewStatus) }}</span>
          </div>
          <div class="info-item">
            <span class="label">复核人:</span>
            <span class="value">{{ reviewerId ? `用户${reviewerId}` : '未分配' }}</span>
          </div>
          <div class="info-item">
            <span class="label">创建时间:</span>
            <span class="value">{{ formatDateTime(createdAt) }}</span>
          </div>
          <div class="info-item">
            <span class="label">复核时间:</span>
            <span class="value">{{ formatDateTime(reviewedAt) }}</span>
          </div>
        </el-card>

        <!-- 复核意见 -->
        <el-card class="info-card">
          <template #header>
            <span>复核意见</span>
          </template>
          <el-input
            v-if="reviewStatus === 'pending'"
            v-model="reviewComment"
            type="textarea"
            :rows="6"
            placeholder="请输入复核意见（驳回时必填）"
          />
          <div v-else class="review-comment-display">
            {{ reviewComment || '无' }}
          </div>
        </el-card>

        <!-- 标注统计 -->
        <el-card class="info-card">
          <template #header>
            <span>标注统计</span>
          </template>
          <div class="stat-item">
            <span class="stat-label">文本实体:</span>
            <span class="stat-value">{{ textEntities.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">关系:</span>
            <span class="stat-value">{{ relations.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">图片实体:</span>
            <span class="stat-value">{{ imageEntities.size }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">边界框:</span>
            <span class="stat-value">{{ bboxes.size }}</span>
          </div>
        </el-card>

        <!-- 操作提示 -->
        <el-card v-if="reviewStatus === 'pending'" class="info-card">
          <template #header>
            <span>操作说明</span>
          </template>
          <div class="guide-item">
            <strong>复核流程：</strong>
            <p>1. 仔细检查文本和图片标注</p>
            <p>2. 如需修改，可直接编辑标注</p>
            <p>3. 填写复核意见（驳回时必填）</p>
            <p>4. 点击"批准"或"驳回"按钮</p>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 驳回确认对话框 -->
    <el-dialog
      v-model="showRejectDialog"
      title="驳回确认"
      width="500px"
    >
      <el-form :model="rejectForm" label-width="100px">
        <el-form-item label="驳回原因" required>
          <el-input
            v-model="rejectForm.comment"
            type="textarea"
            :rows="4"
            placeholder="请输入驳回原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRejectDialog = false">取消</el-button>
        <el-button
          type="danger"
          @click="confirmReject"
          :disabled="!rejectForm.comment"
          :loading="submitting"
        >
          确认驳回
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>
⋮----
<!-- 加载状态 -->
⋮----
<!-- 页面头部 -->
⋮----
<h2>复核任务 #{{ reviewId }}</h2>
⋮----
{{ getStatusText(reviewStatus) }}
⋮----
{{ getStatusText(reviewStatus) }}
⋮----
<!-- 内容区域 -->
⋮----
<!-- 左侧：标注查看器 -->
⋮----
<!-- 文本标注 -->
⋮----
<!-- 图片标注 -->
⋮----
<!-- 右侧：复核信息面板 -->
⋮----
<!-- 复核信息 -->
⋮----
<template #header>
            <span>复核信息</span>
          </template>
⋮----
<span class="value">{{ reviewId }}</span>
⋮----
<span class="value">{{ taskId || '-' }}</span>
⋮----
<span class="value">{{ getStatusText(reviewStatus) }}</span>
⋮----
<span class="value">{{ reviewerId ? `用户${reviewerId}` : '未分配' }}</span>
⋮----
<span class="value">{{ formatDateTime(createdAt) }}</span>
⋮----
<span class="value">{{ formatDateTime(reviewedAt) }}</span>
⋮----
<!-- 复核意见 -->
⋮----
<template #header>
            <span>复核意见</span>
          </template>
⋮----
{{ reviewComment || '无' }}
⋮----
<!-- 标注统计 -->
⋮----
<template #header>
            <span>标注统计</span>
          </template>
⋮----
<span class="stat-value">{{ textEntities.length }}</span>
⋮----
<span class="stat-value">{{ relations.length }}</span>
⋮----
<span class="stat-value">{{ imageEntities.size }}</span>
⋮----
<span class="stat-value">{{ bboxes.size }}</span>
⋮----
<!-- 操作提示 -->
⋮----
<template #header>
            <span>操作说明</span>
          </template>
⋮----
<!-- 驳回确认对话框 -->
⋮----
<template #footer>
        <el-button @click="showRejectDialog = false">取消</el-button>
        <el-button
          type="danger"
          @click="confirmReject"
          :disabled="!rejectForm.comment"
          :loading="submitting"
        >
          确认驳回
        </el-button>
      </template>
⋮----
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  Check,
  Close
} from '@element-plus/icons-vue'
import TextAnnotationEditor from '@/components/annotation/TextAnnotationEditor.vue'
import ImageAnnotationEditor from '@/components/annotation/ImageAnnotationEditor.vue'
import { useLabelStore } from '@/stores/label'
import type { EntityType, RelationType } from '@/api/label'
import { reviewApi } from '@/api/review'
import { annotationApi } from '@/api/annotation'
import { formatDateTime } from '@/utils/datetime'

// 路由
const route = useRoute()
const router = useRouter()
const reviewId = computed(() => route.params.reviewId as string)

// Store
const labelStore = useLabelStore()

// 状态
const activeTab = ref('text')
const loading = ref(true)
const submitting = ref(false)
const reviewStatus = ref<'pending' | 'approved' | 'rejected'>('pending')
const showRejectDialog = ref(false)

// 复核信息
const taskId = ref('')
const reviewerId = ref<number>()
const reviewComment = ref('')
const createdAt = ref('')
const reviewedAt = ref('')

// 语料文本
const corpusText = ref('')

// 图片列表
const images = ref<Array<{ id: number; url: string }>>([])

// 标注数据
const textEntities = ref<any[]>([])
const relations = ref<any[]>([])
const imageEntities = ref<Map<number, any[]>>(new Map())
const bboxes = ref<Map<number, any[]>>(new Map())

// 标签配置
const entityTypes = ref<EntityType[]>([])
const relationTypes = ref<RelationType[]>([])

// 驳回表单
const rejectForm = ref({
  comment: ''
})

// 加载复核任务数据
const loadReviewData = async () => {
  try {
    loading.value = true
    
    console.log('[ReviewDetail] 开始加载复核数据, reviewId:', reviewId.value)
    
    // 获取复核任务详情
    const reviewResponse = await reviewApi.get(reviewId.value)
    
    console.log('[ReviewDetail] 复核API响应:', reviewResponse)
    
    // 后端可能直接返回对象，也可能是 { data: {...} } 格式
    const review = reviewResponse.data || reviewResponse
    
    console.log('[ReviewDetail] 解析后的复核数据:', review)
    
    // 设置复核信息
    if (review && review.task) {
      taskId.value = review.task_id || review.task?.task_id || ''
      reviewStatus.value = review.status || 'pending'
      reviewerId.value = review.reviewer_id
      reviewComment.value = review.review_comment || ''
      createdAt.value = review.created_at || ''
      reviewedAt.value = review.reviewed_at || ''
      
      console.log('[ReviewDetail] 复核信息已设置:', {
        taskId: taskId.value,
        reviewStatus: reviewStatus.value,
        reviewerId: reviewerId.value
      })
      
      // 如果有task_id，加载标注数据
      if (taskId.value) {
        await loadAnnotationData(taskId.value)
      } else {
        console.warn('[ReviewDetail] 没有task_id，无法加载标注数据')
      }
    } else {
      console.warn('[ReviewDetail] review 数据为空或格式不正确:', review)
    }
  } catch (error: any) {
    console.error('加载复核任务失败:', error)
    ElMessage.error(error.message || '加载复核任务失败')
  } finally {
    loading.value = false
  }
}

// 加载标注数据
const loadAnnotationData = async (taskIdValue: string) => {
  try {
    console.log('[ReviewDetail] 开始加载标注数据, taskId:', taskIdValue)
    
    // 调用后端API获取任务详情（使用封装的API服务，包含认证头）
    const result = await annotationApi.getAnnotationTask(taskIdValue)
    
    console.log('[ReviewDetail] 标注API响应:', result)
    
    if (!result.success) {
      throw new Error(result.message || '获取标注数据失败')
    }
    
    const data = result.data
    
    // 设置语料文本
    corpusText.value = data.corpus?.text || ''
    
    console.log('[ReviewDetail] 语料文本长度:', corpusText.value.length)
    
    // 设置实体数据
    textEntities.value = data.entities?.map((e: any) => {
      const entityType = entityTypes.value.find(et => 
        et.type_name === e.label || et.type_name_zh === e.label
      )
      return {
        id: e.id,
        entity_id: e.entity_id,
        text: e.token,
        entity_type_name: e.label,
        entity_type_id: entityType?.id,
        start_offset: e.start_offset,
        end_offset: e.end_offset,
        confidence: e.confidence,
        color: entityType?.color || '#cccccc'
      }
    }) || []
    
    // 设置关系数据
    relations.value = data.relations?.map((r: any) => {
      const relationType = relationTypes.value.find(rt => 
        rt.type_name === r.relation_type || rt.type_name_zh === r.relation_type
      )
      return {
        id: r.id,
        relation_id: r.relation_id,
        source_entity_id: r.from_entity_id,
        target_entity_id: r.to_entity_id,
        relation_type_name: r.relation_type,
        relation_type_id: relationType?.id
      }
    }) || []
    
    console.log('[ReviewDetail] 标注数据加载完成:', {
      corpusText: corpusText.value.substring(0, 50) + '...',
      entities: textEntities.value.length,
      relations: relations.value.length
    })
    
    // TODO: 加载图片数据
    images.value = []
  } catch (error: any) {
    console.error('加载标注数据失败:', error)
    ElMessage.error(error.message || '加载标注数据失败')
  }
}

// 批准复核
const handleApprove = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要批准此标注任务吗？',
      '确认批准',
      { type: 'success' }
    )

    submitting.value = true
    
    await reviewApi.approve(reviewId.value, {
      comment: reviewComment.value
    })
    
    ElMessage.success('批准成功')
    reviewStatus.value = 'approved'
    reviewedAt.value = new Date().toISOString()
    
    // 延迟返回列表
    setTimeout(() => {
      router.push({ name: 'review' })
    }, 1500)
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('批准失败:', error)
      ElMessage.error(error.message || '批准失败')
    }
  } finally {
    submitting.value = false
  }
}

// 驳回复核
const handleReject = () => {
  rejectForm.value.comment = reviewComment.value
  showRejectDialog.value = true
}

const confirmReject = async () => {
  if (!rejectForm.value.comment) {
    ElMessage.warning('请填写驳回原因')
    return
  }

  try {
    submitting.value = true
    
    await reviewApi.reject(reviewId.value, {
      comment: rejectForm.value.comment
    })
    
    ElMessage.success('驳回成功')
    reviewStatus.value = 'rejected'
    reviewComment.value = rejectForm.value.comment
    reviewedAt.value = new Date().toISOString()
    showRejectDialog.value = false
    
    // 延迟返回列表
    setTimeout(() => {
      router.push({ name: 'review' })
    }, 1500)
  } catch (error: any) {
    console.error('驳回失败:', error)
    ElMessage.error(error.message || '驳回失败')
  } finally {
    submitting.value = false
  }
}

// 标注编辑操作（仅在pending状态下可用）
const handleAddTextEntity = async (entity: any) => {
  if (reviewStatus.value !== 'pending') return
  
  try {
    const response = await annotationApi.addTextEntity(taskId.value, {
      token: entity.text,
      label: entity.entity_type_name,
      start_offset: entity.start_offset,
      end_offset: entity.end_offset
    })
    
    textEntities.value.push({
      ...entity,
      id: response.data.id,
      entity_id: response.data.entity_id
    })
  } catch (error) {
    console.error('添加实体失败:', error)
    ElMessage.error('添加实体失败')
  }
}

const handleUpdateTextEntity = async (id: number, updates: any) => {
  if (reviewStatus.value !== 'pending') return
  
  try {
    await annotationApi.updateTextEntity(taskId.value, id, {
      token: updates.text,
      label: updates.entity_type_name,
      start_offset: updates.start_offset,
      end_offset: updates.end_offset
    })
    
    const index = textEntities.value.findIndex(e => e.id === id)
    if (index !== -1) {
      textEntities.value[index] = { ...textEntities.value[index], ...updates }
    }
  } catch (error) {
    console.error('更新实体失败:', error)
    ElMessage.error('更新实体失败')
  }
}

const handleDeleteTextEntity = async (id: number) => {
  if (reviewStatus.value !== 'pending') return
  
  try {
    await annotationApi.deleteTextEntity(taskId.value, id)
    
    relations.value = relations.value.filter(
      r => r.source_entity_id !== id && r.target_entity_id !== id
    )
    textEntities.value = textEntities.value.filter(e => e.id !== id)
  } catch (error) {
    console.error('删除实体失败:', error)
    ElMessage.error('删除实体失败')
  }
}

const handleAddRelation = async (relation: any) => {
  if (reviewStatus.value !== 'pending') return
  
  try {
    const response = await annotationApi.addRelation(taskId.value, {
      from_entity_id: relation.source_entity_id,
      to_entity_id: relation.target_entity_id,
      relation_type: relation.relation_type_name
    })
    
    relations.value.push({
      ...relation,
      id: response.data.id,
      relation_id: response.data.relation_id
    })
  } catch (error) {
    console.error('添加关系失败:', error)
    ElMessage.error('添加关系失败')
  }
}

const handleDeleteRelation = async (id: number) => {
  if (reviewStatus.value !== 'pending') return
  
  try {
    await annotationApi.deleteRelation(taskId.value, id)
    relations.value = relations.value.filter(r => r.id !== id)
  } catch (error) {
    console.error('删除关系失败:', error)
    ElMessage.error('删除关系失败')
  }
}

// 图片实体操作
const getImageEntities = (imageId: number) => {
  return imageEntities.value.get(imageId) || []
}

const handleAddWholeImageEntity = (imageId: number, entity: any) => {
  if (reviewStatus.value !== 'pending') return
  const entities = imageEntities.value.get(imageId) || []
  entities.push({ ...entity, id: Date.now() })
  imageEntities.value.set(imageId, entities)
}

const handleDeleteWholeImageEntity = (imageId: number, entityId: number) => {
  if (reviewStatus.value !== 'pending') return
  const entities = imageEntities.value.get(imageId) || []
  imageEntities.value.set(imageId, entities.filter(e => e.id !== entityId))
}

const getImageBBoxes = (imageId: number) => {
  return bboxes.value.get(imageId) || []
}

const handleAddBBox = (imageId: number, bbox: any) => {
  if (reviewStatus.value !== 'pending') return
  const boxes = bboxes.value.get(imageId) || []
  boxes.push({ ...bbox, id: Date.now() })
  bboxes.value.set(imageId, boxes)
}

const handleUpdateBBox = (imageId: number, bboxId: number, updates: any) => {
  if (reviewStatus.value !== 'pending') return
  const boxes = bboxes.value.get(imageId) || []
  const index = boxes.findIndex(b => b.id === bboxId)
  if (index !== -1) {
    boxes[index] = { ...boxes[index], ...updates }
    bboxes.value.set(imageId, boxes)
  }
}

const handleDeleteBBox = (imageId: number, bboxId: number) => {
  if (reviewStatus.value !== 'pending') return
  const boxes = bboxes.value.get(imageId) || []
  bboxes.value.set(imageId, boxes.filter(b => b.id !== bboxId))
}

// 返回
const goBack = () => {
  router.push({ name: 'review' })
}

// 状态相关
const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '待复核',
    approved: '已通过',
    rejected: '已驳回'
  }
  return textMap[status] || '未知'
}

// formatDateTime 已从 @/utils/datetime 导入

// 初始化
onMounted(async () => {
  try {
    // 加载标签配置
    await labelStore.fetchEntityTypes({ include_inactive: false })
    await labelStore.fetchRelationTypes({ include_inactive: false })
    entityTypes.value = labelStore.entityTypes
    relationTypes.value = labelStore.relationTypes

    // 加载复核数据
    await loadReviewData()
  } catch (error) {
    ElMessage.error('初始化失败')
  }
})
</script>
⋮----
<style scoped>
.review-detail-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #dcdfe6;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.page-content {
  flex: 1;
  display: flex;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
}

.viewer-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.viewer-tabs {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.viewer-tabs :deep(.el-tabs__content) {
  flex: 1;
  overflow: hidden;
}

.viewer-tabs :deep(.el-tab-pane) {
  height: 100%;
}

.info-panel {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
}

.info-card {
  flex-shrink: 0;
}

.info-item,
.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child,
.stat-item:last-child {
  border-bottom: none;
}

.label,
.stat-label {
  color: #909399;
  font-size: 14px;
}

.value,
.stat-value {
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

.review-comment-display {
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100px;
  white-space: pre-wrap;
}

.guide-item {
  margin-bottom: 16px;
}

.guide-item:last-child {
  margin-bottom: 0;
}

.guide-item strong {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  color: #606266;
}

.guide-item p {
  margin: 4px 0;
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
}
</style>
````

## File: frontend/src/views/review/ReviewList.vue
````vue
<template>
  <div class="review-list-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="title">复核任务列表</span>
        </div>
      </template>

      <!-- 筛选区域 -->
      <div class="filter-section">
        <el-form :inline="true" :model="filters">
          <el-form-item label="状态">
            <el-select
              v-model="filters.status"
              placeholder="全部状态"
              clearable
              style="width: 150px"
              @change="handleFilterChange"
            >
              <el-option label="待复核" value="pending" />
              <el-option label="已通过" value="approved" />
              <el-option label="已驳回" value="rejected" />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="loadReviewTasks">查询</el-button>
            <el-button @click="clearFilters">清除筛选</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 任务列表表格 -->
      <el-table
        v-loading="loading"
        :data="reviewTasks"
        style="width: 100%"
        @row-click="handleReview"
      >
        <el-table-column prop="review_id" label="复核ID" width="180" />
        <el-table-column prop="task_id" label="标注任务ID" width="180" />
        
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="复核人" width="120">
          <template #default="{ row }">
            {{ row.reviewer_id ? `用户${row.reviewer_id}` : '未分配' }}
          </template>
        </el-table-column>
        
        <el-table-column prop="review_comment" label="复核意见" show-overflow-tooltip />
        
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="复核时间" width="180">
          <template #default="{ row }">
            {{ row.reviewed_at ? formatDateTime(row.reviewed_at) : '-' }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click.stop="handleReview(row)"
            >
              {{ row.status === 'pending' ? '开始复核' : '查看详情' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态 -->
      <el-empty
        v-if="!loading && reviewTasks.length === 0"
        description="暂无复核任务"
      />

      <!-- 分页 -->
      <div v-if="reviewTasks.length > 0" class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handlePageSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>
⋮----
<template #header>
        <div class="card-header">
          <span class="title">复核任务列表</span>
        </div>
      </template>
⋮----
<!-- 筛选区域 -->
⋮----
<!-- 任务列表表格 -->
⋮----
<template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
⋮----
{{ getStatusText(row.status) }}
⋮----
<template #default="{ row }">
            {{ row.reviewer_id ? `用户${row.reviewer_id}` : '未分配' }}
          </template>
⋮----
{{ row.reviewer_id ? `用户${row.reviewer_id}` : '未分配' }}
⋮----
<template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
⋮----
{{ formatDateTime(row.created_at) }}
⋮----
<template #default="{ row }">
            {{ row.reviewed_at ? formatDateTime(row.reviewed_at) : '-' }}
          </template>
⋮----
{{ row.reviewed_at ? formatDateTime(row.reviewed_at) : '-' }}
⋮----
<template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click.stop="handleReview(row)"
            >
              {{ row.status === 'pending' ? '开始复核' : '查看详情' }}
            </el-button>
          </template>
⋮----
{{ row.status === 'pending' ? '开始复核' : '查看详情' }}
⋮----
<!-- 空状态 -->
⋮----
<!-- 分页 -->
⋮----
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { reviewApi } from '@/api/review'
import { formatDateTime } from '@/utils/datetime'

interface ReviewTask {
  review_id: string
  task_id: string
  status: 'pending' | 'approved' | 'rejected'
  reviewer_id?: number
  review_comment?: string
  reviewed_at?: string
  created_at: string
}

const router = useRouter()

// 状态
const loading = ref(false)
const reviewTasks = ref<ReviewTask[]>([])

// 筛选条件
const filters = ref({
  status: '',
  reviewer_id: undefined as number | undefined
})

// 分页
const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

// 加载复核任务列表
const loadReviewTasks = async () => {
  try {
    loading.value = true
    
    const response = await reviewApi.list({
      page: pagination.value.page,
      page_size: pagination.value.pageSize,
      status: filters.value.status || undefined,
      reviewer_id: filters.value.reviewer_id
    })
    
    // 处理响应数据
    if (Array.isArray(response)) {
      // 如果返回的是数组
      reviewTasks.value = response
      pagination.value.total = response.length
    } else if (response.data) {
      // 如果返回的是包含data的对象
      reviewTasks.value = response.data.items || response.data
      pagination.value.total = response.data.total || reviewTasks.value.length
    }
  } catch (error: any) {
    console.error('加载复核任务失败:', error)
    ElMessage.error(error.message || '加载复核任务失败')
  } finally {
    loading.value = false
  }
}

// 筛选变化
const handleFilterChange = () => {
  pagination.value.page = 1
  loadReviewTasks()
}

// 清除筛选
const clearFilters = () => {
  filters.value.status = ''
  filters.value.reviewer_id = undefined
  pagination.value.page = 1
  loadReviewTasks()
}

// 分页变化
const handlePageChange = (page: number) => {
  pagination.value.page = page
  loadReviewTasks()
}

const handlePageSizeChange = (pageSize: number) => {
  pagination.value.pageSize = pageSize
  pagination.value.page = 1
  loadReviewTasks()
}

// 开始复核
const handleReview = (task: ReviewTask) => {
  router.push({
    name: 'review-detail',
    params: { reviewId: task.review_id }
  })
}

// 状态相关
const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '待复核',
    approved: '已通过',
    rejected: '已驳回'
  }
  return textMap[status] || '未知'
}

// formatDateTime 已从 @/utils/datetime 导入

// 初始化
onMounted(() => {
  loadReviewTasks()
})
</script>
⋮----
<style scoped lang="scss">
.review-list-container {
  padding: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .title {
      font-size: 18px;
      font-weight: 600;
    }
  }

  .filter-section {
    margin-bottom: 20px;
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  :deep(.el-table__row) {
    cursor: pointer;

    &:hover {
      background-color: #f5f7fa;
    }
  }
}
</style>
````

## File: frontend/src/views/user/UserManagement.vue
````vue
<template>
  <div class="user-management">
    <!-- 页面标题和操作栏 -->
    <div class="header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        创建用户
      </el-button>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-select
        v-model="filterRole"
        placeholder="筛选角色"
        clearable
        style="width: 200px"
        @change="loadUsers"
      >
        <el-option label="管理员" value="admin" />
        <el-option label="标注员" value="annotator" />
        <el-option label="浏览员" value="viewer" />
      </el-select>

      <el-button @click="loadUsers" :loading="loading">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <!-- 用户列表 -->
    <el-table
      :data="users"
      v-loading="loading"
      stripe
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="200" />
      <el-table-column prop="role" label="角色" width="150">
        <template #default="{ row }">
          <el-tag :type="getRoleTagType(row.role)">
            {{ getRoleLabel(row.role) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="200">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="200">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="handleEdit(row)"
          >
            编辑
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(row)"
            :disabled="row.id === currentUser?.id"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadUsers"
        @current-change="loadUsers"
      />
    </div>

    <!-- 创建/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '创建用户' : '编辑用户'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="formData.username"
            placeholder="请输入用户名"
            :disabled="dialogMode === 'edit'"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
          <div v-if="dialogMode === 'edit'" class="form-tip">
            留空则不修改密码
          </div>
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="formData.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="标注员" value="annotator" />
            <el-option label="浏览员" value="viewer" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>
⋮----
<!-- 页面标题和操作栏 -->
⋮----
<!-- 筛选栏 -->
⋮----
<!-- 用户列表 -->
⋮----
<template #default="{ row }">
          <el-tag :type="getRoleTagType(row.role)">
            {{ getRoleLabel(row.role) }}
          </el-tag>
        </template>
⋮----
{{ getRoleLabel(row.role) }}
⋮----
<template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
⋮----
{{ formatDate(row.created_at) }}
⋮----
<template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="handleEdit(row)"
          >
            编辑
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(row)"
            :disabled="row.id === currentUser?.id"
          >
            删除
          </el-button>
        </template>
⋮----
<!-- 分页 -->
⋮----
<!-- 创建/编辑用户对话框 -->
⋮----
<template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
⋮----
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import { userApi } from '@/api/user'
import { formatDateTimeShort } from '@/utils/datetime'
import { useUserStore } from '@/stores/user'
import type { User } from '@/types'

// Store
const userStore = useUserStore()
const currentUser = computed(() => userStore.currentUser)

// 数据
const users = ref<User[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const filterRole = ref<string>('')

// 对话框
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const submitting = ref(false)
const formRef = ref<FormInstance>()

// 表单数据
const formData = ref({
  id: 0,
  username: '',
  password: '',
  role: 'annotator' as 'admin' | 'annotator' | 'viewer'
})

// 表单验证规则
const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    {
      validator: (rule, value, callback) => {
        if (dialogMode.value === 'create' && !value) {
          callback(new Error('请输入密码'))
        } else if (value && value.length < 6) {
          callback(new Error('密码长度至少 6 个字符'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

// 加载用户列表
const loadUsers = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const response = await userApi.list({
      role: filterRole.value || undefined,
      skip,
      limit: pageSize.value
    })

    // 后端返回的是数组
    if (Array.isArray(response)) {
      users.value = response
      // 注意：后端没有返回总数，这里使用数组长度
      // 如果返回的数据等于 pageSize，说明可能还有更多数据
      if (response.length === pageSize.value) {
        total.value = (currentPage.value) * pageSize.value + 1
      } else {
        total.value = (currentPage.value - 1) * pageSize.value + response.length
      }
    } else {
      users.value = []
      total.value = 0
    }
  } catch (error: any) {
    console.error('加载用户列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载用户列表失败')
  } finally {
    loading.value = false
  }
}

// 创建用户
const handleCreate = () => {
  dialogMode.value = 'create'
  formData.value = {
    id: 0,
    username: '',
    password: '',
    role: 'annotator'
  }
  dialogVisible.value = true
}

// 编辑用户
const handleEdit = (user: User) => {
  dialogMode.value = 'edit'
  formData.value = {
    id: user.id,
    username: user.username,
    password: '',
    role: user.role
  }
  dialogVisible.value = true
}

// 删除用户
const handleDelete = async (user: User) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${user.username}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await userApi.delete(user.id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除用户失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    if (dialogMode.value === 'create') {
      // 创建用户
      await userApi.create({
        username: formData.value.username,
        password: formData.value.password,
        role: formData.value.role
      })
      ElMessage.success('创建成功')
    } else {
        const confirmMessageVNode = h('div', [
          h('div', `确定要删除用户 "${user.username}" 吗？`),
          h('div', { style: 'margin-top: 8px; color: #f56c6c;' }, '此操作不可恢复。')
        ])
        await ElMessageBox.confirm(
          confirmMessageVNode,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
    }

    dialogVisible.value = false
    loadUsers()
  } catch (error: any) {
    console.error('提交失败:', error)
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

// 获取角色标签类型
const getRoleTagType = (role: string) => {
  const typeMap: Record<string, any> = {
    admin: 'danger',
    annotator: 'primary',
    reviewer: 'success'
  }
  return typeMap[role] || ''
}

// 获取角色标签文本
const getRoleLabel = (role: string) => {
  const labelMap: Record<string, string> = {
    admin: '管理员',
    annotator: '标注员',
    viewer: '浏览员'
  }
  return labelMap[role] || role
}

// 格式化日期
const formatDate = (dateString: string) => formatDateTimeShort(dateString)

// 初始化
onMounted(() => {
  loadUsers()
})
</script>
⋮----
<style scoped>
.user-management {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style>
````

## File: frontend/src/vite-env.d.ts
````typescript
/// <reference types="vite/client" />
⋮----
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_TITLE?: string
  readonly VITE_BACKEND_ORIGIN?: string
  readonly VITE_DEV_PROXY_TARGET?: string
}
⋮----
interface ImportMeta {
  readonly env: ImportMetaEnv
}
````

## File: frontend/vite.config.ts
````typescript
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
````

## File: init_index.sh
````bash
#!/bin/bash
# 初始化项目索引
# 不带参数运行：扫描文件结构，供配置 ignore 规则使用
# 带 --run 参数运行：正式生成索引并检查配置

echo "=== 初始化项目索引 ==="
echo "创建目录结构..."
mkdir -p PROJECT_INDEX/history

echo ""
echo "=== 项目文件结构扫描 ==="
echo "（供配置 repomix.config.json 的 ignore 规则使用）"
echo ""

find . \
  -not -path '*/.*' \
  -not -path '*/node_modules/*' \
  -not -path '*/htmlcov/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/venv/*' \
  -not -path '*/.venv/*' \
  -not -path '*/env/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  -not -path '*/target/*' \
  -not -path '*/vendor/*' \
  -not -path '*/logs/*' \
  -type f | sort

echo ""
echo "--- 文件类型统计 ---"
find . \
  -not -path '*/.*' \
  -not -path '*/node_modules/*' \
  -not -path '*/htmlcov/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/venv/*' \
  -not -path '*/.venv/*' \
  -not -path '*/env/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  -not -path '*/target/*' \
  -not -path '*/vendor/*' \
  -not -path '*/logs/*' \
  -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

echo ""
echo "--- 顶层目录结构 ---"
find . -maxdepth 2 \
  -not -path '*/.*' \
  -not -path '*/node_modules/*' \
  -not -path '*/htmlcov/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/venv/*' \
  -not -path '*/.venv/*' \
  | sort

echo ""
echo "=========================================="
echo "请根据以上文件清单配置 repomix.config.json"
echo "确认 ignore.customPatterns 覆盖了不需要的文件类型后"
echo "再继续运行: bash init_index.sh --run"
echo "=========================================="

if [ "$1" != "--run" ]; then
    exit 0
fi

if [ ! -f "repomix.config.json" ]; then
    echo "❌ 错误：repomix.config.json 不存在，请先创建配置文件"
    exit 1
fi

if ! grep -q "{datetime}" repomix.config.json; then
    echo "⚠️  警告：repomix.config.json 中未找到 {datetime} 占位符"
    echo "   filePath 应该类似: \"PROJECT_INDEX/history\\\\ProjectName_{datetime}.md\""
    echo ""
fi

echo ""
echo "=== 生成索引 ==="
ts=$(date +"%Y-%m-%d_%H-%M-%S")
sed -i "s/{datetime}/$ts/" repomix.config.json
npx repomix@latest --config repomix.config.json --compress
sed -i "s/$ts/{datetime}/" repomix.config.json

latest=$(ls -t PROJECT_INDEX/history/*.md 2>/dev/null | head -1)
if [ -z "$latest" ]; then
    echo "❌ 错误：未找到生成的索引文件"
    exit 1
fi

echo ""
echo "✅ 生成完成: $latest"
echo ""
echo "=== 配置检查 ==="
total_files=$(grep -c "^## File:" "$latest" 2>/dev/null; true)
echo "总文件数: $total_files"
echo ""
echo "文件类型分布:"
grep "^## File:" "$latest" | sed 's/.*\.//' | sort | uniq -c | sort -rn

echo ""
echo "=== 优化建议 ==="
should_ignore=""
md_count=$(grep "^## File:" "$latest" | grep -c "\.md$" 2>/dev/null; true)
[ "$md_count" -gt 0 ] && should_ignore="${should_ignore}\n  \"**/*.md\","
json_count=$(grep "^## File:" "$latest" | grep -c "\.json$" 2>/dev/null; true)
[ "$json_count" -gt 0 ] && should_ignore="${should_ignore}\n  \"**/*.json\","
log_count=$(grep "^## File:" "$latest" | grep -c "\.log$" 2>/dev/null; true)
[ "$log_count" -gt 0 ] && should_ignore="${should_ignore}\n  \"**/*.log\","
img_count=$(grep "^## File:" "$latest" | grep -cE "\.(png|jpg|jpeg|gif|svg|webp)$" 2>/dev/null; true)
[ "$img_count" -gt 0 ] && should_ignore="${should_ignore}\n  \"**/*.png\", \"**/*.jpg\", \"**/*.gif\","
data_count=$(grep "^## File:" "$latest" | grep -cE "\.(csv|xlsx|db|sqlite)$" 2>/dev/null; true)
[ "$data_count" -gt 0 ] && should_ignore="${should_ignore}\n  \"**/*.csv\", \"**/*.xlsx\", \"**/*.db\","

if [ -n "$should_ignore" ]; then
    echo "⚠️  建议在 ignore.customPatterns 中添加："
    echo -e "$should_ignore"
    echo "添加后运行: bash update_index.sh"
else
    echo "✅ 配置良好，未发现需要忽略的文件类型"
fi

echo ""
echo "=== 下一步 ==="
echo "1. 检查索引文件: less $latest"
echo "2. 创建架构文档: PROJECT_INDEX/architecture.md"
echo "3. 创建数据库文档: PROJECT_INDEX/database_schema.md（如有数据库）"
echo "4. 更新 CLAUDE.md 添加索引引用"
echo "5. 后续更新使用: bash update_index.sh"
````

## File: update_index.sh
````bash
#!/bin/bash
# 更新项目索引
echo "=== 更新项目索引 ==="
echo "运行 repomix..."

ts=$(date +"%Y-%m-%d_%H-%M-%S")
sed -i "s/{datetime}/$ts/" repomix.config.json
npx repomix@latest --config repomix.config.json --compress
sed -i "s/$ts/{datetime}/" repomix.config.json

echo ""
echo "✅ 索引已更新"
echo ""
echo "=== 检测变更 ==="

latest=$(ls -t PROJECT_INDEX/history/*.md 2>/dev/null | head -1)
previous=$(ls -t PROJECT_INDEX/history/*.md 2>/dev/null | head -2 | tail -1)

if [ -z "$previous" ]; then
    echo "这是首次生成索引，没有历史版本可比对"
    echo "最新索引: $latest"
elif [ "$latest" = "$previous" ]; then
    echo "只有一个历史版本，没有变更"
else
    echo "比对: $previous"
    echo "  vs: $latest"
    echo ""
    diff -u "$previous" "$latest" > PROJECT_INDEX/latest_changes.diff
    added=$(grep -c "^+[^+]" PROJECT_INDEX/latest_changes.diff 2>/dev/null; true)
    removed=$(grep -c "^-[^-]" PROJECT_INDEX/latest_changes.diff 2>/dev/null; true)
    echo "变更统计:"
    echo "  新增: $added 行"
    echo "  删除: $removed 行"
    echo ""
    echo "详细变更: PROJECT_INDEX/latest_changes.diff"
fi

echo ""
echo "提示："
echo "- 架构文档: PROJECT_INDEX/architecture.md（需手动维护）"
echo "- 数据库表结构: PROJECT_INDEX/database_schema.md（需手动维护）"
echo "- 代码签名索引: PROJECT_INDEX/history/（自动生成）"
````
