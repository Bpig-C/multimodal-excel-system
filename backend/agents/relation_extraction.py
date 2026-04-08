"""
关系抽取Agent
基于已提取的实体识别它们之间的关系
"""
import json
import logging
import re
from typing import List, Optional, Set
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from config import settings
from agents.entity_extraction import ExtractedEntity
from models.db_models import RelationType
from services.dynamic_prompt_builder import DynamicPromptBuilder

logger = logging.getLogger(__name__)


# ============================================================================
# 输出模型定义
# ============================================================================

class ExtractedRelation(BaseModel):
    """提取的关系"""
    id: int = Field(..., description="关系ID，从0开始")
    from_id: int = Field(..., description="源实体ID")
    to_id: int = Field(..., description="目标实体ID")
    type: str = Field(..., description="关系类型")


class RelationExtractionOutput(BaseModel):
    """关系抽取输出"""
    text_id: str = Field(..., description="文本ID")
    relations: List[ExtractedRelation] = Field(default_factory=list, description="提取的关系列表")


# ============================================================================
# Prompt模板
# ============================================================================

RELATION_EXTRACTION_PROMPT = """你是一个专业的品质失效案例关系抽取专家。请基于给定的文本和已标注的实体，识别实体之间的关系。

## 关系类型定义（共8类）

1. **has_defect** (有缺陷): 产品/部件存在某种缺陷
   - 方向: Product/Material -> DefectPhenomenon/IssueType
   - 示例: "显示屏" has_defect "裂纹"

2. **caused_by** (由...引起): 问题由某原因导致
   - 方向: DefectPhenomenon/IssueType -> SpecificCause/CauseCategory
   - 示例: "划痕" caused_by "操作不当"

3. **occurs_in** (发生在): 问题发生在某工序/地点
   - 方向: DefectPhenomenon/IssueType -> Process/Location
   - 示例: "功能失效" occurs_in "测试工序"

4. **uses_equipment** (使用设备): 工序使用某设备
   - 方向: Process -> Equipment
   - 示例: "焊接" uses_equipment "焊接机"

5. **uses_material** (使用物料): 产品/工序使用某物料
   - 方向: Product/Process -> Material
   - 示例: "主板" uses_material "电子元件"

6. **performed_by** (由...执行): 工序由某人员执行
   - 方向: Process -> Personnel
   - 示例: "组装" performed_by "操作工"

7. **supplied_by** (由...供应): 物料/产品由某供应商提供
   - 方向: Material/Product -> Supplier
   - 示例: "钢材" supplied_by "XX供应商"

8. **resolved_by** (通过...解决): 问题通过某措施解决
   - 方向: DefectPhenomenon/IssueType -> Action
   - 示例: "裂纹" resolved_by "返工处理"

## 标注原则

1. **实体ID有效性**: 所有from_id和to_id必须存在于输入的实体列表中
2. **关系方向性**: 严格遵守关系的方向定义
3. **就近原则**: 优先标注距离较近的实体关系
4. **避免冗余**: 不标注间接或推断的关系
5. **类型准确**: 严格按照8种关系类型标注

## 输出格式

请严格按照JSON格式输出：
{
  "text_id": "文本ID",
  "relations": [
    {
      "id": 0,
      "from_id": 源实体ID,
      "to_id": 目标实体ID,
      "type": "关系类型"
    }
  ]
}

## 示例

输入:
文本ID: 001
文本: "产品外观有划痕，经检查发现是焊接工序中操作不当导致。"
实体列表:
[
  {"id": 0, "token": "产品", "label": "Product"},
  {"id": 1, "token": "划痕", "label": "DefectPhenomenon"},
  {"id": 2, "token": "焊接", "label": "Process"},
  {"id": 3, "token": "操作不当", "label": "SpecificCause"}
]

输出:
{
  "text_id": "001",
  "relations": [
    {"id": 0, "from_id": 0, "to_id": 1, "type": "has_defect"},
    {"id": 1, "from_id": 1, "to_id": 3, "type": "caused_by"},
    {"id": 2, "from_id": 1, "to_id": 2, "type": "occurs_in"}
  ]
}

现在请处理以下输入：
"""


# ============================================================================
# Agent类
# ============================================================================

class RelationExtractionAgent:
    """关系抽取Agent"""
    
    def __init__(self):
        """初始化Agent"""
        # 创建LLM
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            api_key=settings.DASHSCOPE_API_KEY,
            base_url=settings.DASHSCOPE_BASE_URL,
            timeout=settings.LLM_TIMEOUT_SECONDS,
            max_retries=settings.LLM_MAX_RETRIES
        )
    
    def extract_relations(
        self,
        text_id: str,
        text: str,
        entities: List[ExtractedEntity],
        relation_types: Optional[List[RelationType]] = None
    ) -> RelationExtractionOutput:
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
        if len(entities) < 2:
            return RelationExtractionOutput(text_id=text_id, relations=[])
        
        # 构建prompt（优先使用动态标签体系）
        if relation_types:
            entities_for_prompt = [
                {
                    'id': entity.id,
                    'token': entity.token,
                    'label': entity.label
                }
                for entity in entities
            ]
            prompt = DynamicPromptBuilder.build_relation_extraction_prompt(
                text_id=text_id,
                text=text,
                entities=entities_for_prompt,
                relation_types=relation_types
            )
        else:
            entities_str = "[\n"
            for entity in entities:
                entities_str += f'  {{"id": {entity.id}, "token": "{entity.token}", "label": "{entity.label}"}},\n'
            entities_str += "]"

            prompt = f"""{RELATION_EXTRACTION_PROMPT}

文本ID: {text_id}
文本: "{text}"
实体列表:
{entities_str}
"""
        
        # 直接调用LLM获取原始文本输出（兼容DashScope/Qwen）
        structured_llm = self.llm
        
        try:
            # 调用LLM
            raw_response = structured_llm.invoke(prompt)
            raw_text = raw_response.content if hasattr(raw_response, 'content') else str(raw_response)
            logger.debug(f"[关系抽取] text_id={text_id} 原始响应: {raw_text[:500]}")
            
            # 从响应中提取JSON
            json_text = self._extract_json(raw_text)
            data = json.loads(json_text)
            
            relations = [
                ExtractedRelation(
                    id=r.get('id', idx),
                    from_id=r['from_id'],
                    to_id=r['to_id'],
                    type=r['type']
                )
                for idx, r in enumerate(data.get('relations', []))
            ]
            logger.info(f"[关系抽取] text_id={text_id} LLM返回关系数={len(relations)}")
            
            # 验证实体ID有效性
            valid_entity_ids = {entity.id for entity in entities}
            validated_relations = []
            
            for relation in relations:
                if relation.from_id not in valid_entity_ids:
                    logger.warning(f"[关系抽取] 关系{relation.id}的from_id={relation.from_id}无效，已跳过")
                    continue
                if relation.to_id not in valid_entity_ids:
                    logger.warning(f"[关系抽取] 关系{relation.id}的to_id={relation.to_id}无效，已跳过")
                    continue
                if relation.from_id == relation.to_id:
                    logger.warning(f"[关系抽取] 关系{relation.id}的from_id和to_id相同，已跳过")
                    continue
                validated_relations.append(relation)
            
            # 重新编号关系ID
            for idx, relation in enumerate(validated_relations):
                relation.id = idx
            
            return RelationExtractionOutput(text_id=text_id, relations=validated_relations)
            
        except Exception as e:
            logger.error(f"[关系抽取] text_id={text_id} 失败: {e}", exc_info=True)
            return RelationExtractionOutput(text_id=text_id, relations=[])
    
    @staticmethod
    def _extract_json(text: str) -> str:
        """从LLM响应中提取JSON块。"""
        match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if match:
            return match.group(1).strip()
        match = re.search(r'(\{[\s\S]*\})', text)
        if match:
            return match.group(1).strip()
        return text.strip()


# ============================================================================
# 全局单例
# ============================================================================

_relation_agent: Optional[RelationExtractionAgent] = None


def get_relation_agent() -> RelationExtractionAgent:
    """获取关系抽取Agent实例（单例模式）"""
    global _relation_agent
    if _relation_agent is None:
        _relation_agent = RelationExtractionAgent()
    return _relation_agent
