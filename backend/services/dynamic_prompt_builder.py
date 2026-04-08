"""
动态Prompt构建器
根据数据库中的标签配置动态生成Agent的Prompt
"""
import json
from typing import List

from models.db_models import EntityType, RelationType


# 默认配置(降级使用)
DEFAULT_ENTITY_TYPES_PROMPT = """
1. **产品** (Product)
   - 描述: 具体的产品名称、型号、部件
   - 示例: 电机, 控制器, 显示屏

2. **缺陷现象** (DefectPhenomenon)
   - 描述: 具体的缺陷表现
   - 示例: 裂纹, 变形, 失效
"""

DEFAULT_RELATION_TYPES_PROMPT = """
1. **有缺陷** (has_defect)
   - 描述: 产品/部件存在某种缺陷
   - 方向: Product -> DefectPhenomenon
   - 示例: 显示屏 --[has_defect]--> 裂纹
"""


class DynamicPromptBuilder:
    """
    动态Prompt构建器
    
    根据数据库中的标签配置生成Agent的Prompt
    """
    
    @staticmethod
    def build_entity_types_section(entity_types: List[EntityType]) -> str:
        """
        构建实体类型定义部分
        
        Args:
            entity_types: 实体类型列表
            
        Returns:
            str: 实体类型定义的Prompt文本
        """
        if not entity_types:
            return DEFAULT_ENTITY_TYPES_PROMPT
        
        sections = []
        for idx, et in enumerate(entity_types, 1):
            # 标题行
            section = f"{idx}. **{et.type_name_zh}** ({et.type_name})"
            
            # 添加标准定义(优先使用LLM生成的定义)
            if et.definition:
                section += f"\n   - 定义: {et.definition}"
            elif et.description:
                section += f"\n   - 描述: {et.description}"
            
            # 添加示例
            if et.examples:
                try:
                    examples = json.loads(et.examples) if isinstance(et.examples, str) else et.examples
                    if examples:
                        # 最多显示5个示例
                        example_str = ', '.join(examples[:5])
                        section += f"\n   - 示例: {example_str}"
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # 添加类别辨析
            if et.disambiguation:
                section += f"\n   - 辨析: {et.disambiguation}"
            
            # 添加边界框支持说明
            if et.supports_bbox:
                section += f"\n   - 支持区域标注: 是"
            
            sections.append(section)
        
        return "\n\n".join(sections)
    
    @staticmethod
    def build_relation_types_section(relation_types: List[RelationType]) -> str:
        """
        构建关系类型定义部分
        
        Args:
            relation_types: 关系类型列表
            
        Returns:
            str: 关系类型定义的Prompt文本
        """
        if not relation_types:
            return DEFAULT_RELATION_TYPES_PROMPT
        
        sections = []
        for idx, rt in enumerate(relation_types, 1):
            # 标题行
            section = f"{idx}. **{rt.type_name_zh}** ({rt.type_name})"
            
            # 添加标准定义(优先使用LLM生成的定义)
            if rt.definition:
                section += f"\n   - 定义: {rt.definition}"
            elif rt.description:
                section += f"\n   - 描述: {rt.description}"
            
            # 添加方向规则
            if rt.direction_rule:
                section += f"\n   - 方向: {rt.direction_rule}"
            
            # 添加示例
            if rt.examples:
                try:
                    examples = json.loads(rt.examples) if isinstance(rt.examples, str) else rt.examples
                    if examples:
                        # 显示第一个示例
                        section += f"\n   - 示例: {examples[0]}"
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # 添加类别辨析
            if rt.disambiguation:
                section += f"\n   - 辨析: {rt.disambiguation}"
            
            sections.append(section)
        
        return "\n\n".join(sections)
    
    @staticmethod
    def build_entity_extraction_prompt(
        text_id: str,
        text: str,
        entity_types: List[EntityType]
    ) -> str:
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

        prompt = f"""你是一个专业的品质失效案例实体抽取专家。请从给定文本中精准抽取实体。

## 实体类型定义

{entity_types_section}

## 标注原则

1. **实体边界清晰**: 准确标注实体的起始和结束位置
2. **避免重叠**: 实体之间不应重叠,长词优先
3. **保留原文**: token字段必须与原文完全一致
4. **偏移量准确**: start_offset和end_offset必须准确对应原文位置
5. **类型准确**: 严格按照上述实体类型标注
6. **完整性**: 尽可能标注所有符合类型定义的实体
7. **辨析优先**: 遇到易混淆类别时，优先遵循各类型“辨析”说明
8. **最小充分**: 不要过度标注模糊短语，仅标注语义明确的实体

## 输出前自检

- 实体文本是否与原文逐字一致
- start_offset/end_offset 是否与实体文本严格对齐
- label 是否属于上方定义列表
- 是否存在重复或重叠实体

## 输出格式

请严格按照JSON格式输出（仅输出JSON，不要解释文本）:
- text_id: 文本ID
- entities: 实体列表,每个实体包含:
    - id: 实体ID（从0开始递增）
    - token: 实体文本(必须与原文完全一致)
    - label: 实体类型(必须是上述定义的类型之一)
    - start_offset: 起始位置(从0开始)
    - end_offset: 结束位置(不包含)

若无可抽取实体,请返回:
{{
    "text_id": "{text_id}",
    "entities": []
}}

## 待标注文本

文本ID: {text_id}
文本内容: {text}

请开始标注:"""

        return prompt
    
    @staticmethod
    def build_relation_extraction_prompt(
        text_id: str,
        text: str,
        entities: List[dict],
        relation_types: List[RelationType]
    ) -> str:
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

        entity_list_str = "\n".join([
            f"  - ID={e['id']}: {e['token']} ({e['label']})"
            for e in entities
        ])

        prompt = f"""你是一个专业的品质失效案例关系抽取专家。请基于文本与已标注实体识别关系。

## 关系类型定义

{relation_types_section}

## 标注原则

1. **方向准确**: 严格按照关系类型的方向规则标注
2. **实体有效**: from_id和to_id必须是已标注实体的ID
3. **关系合理**: 关系必须符合语义逻辑
4. **避免冗余**: 不要标注重复的关系
5. **类型准确**: 严格按照上述关系类型标注
6. **就近优先**: 优先标注文本中直接表达、距离较近的显式关系
7. **禁止臆断**: 不根据常识补全文本未表达的关系

## 输出前自检

- from_id/to_id 是否均存在于实体列表
- from_id 与 to_id 是否不同
- type 是否属于上方定义列表
- 是否存在重复关系

## 输出格式

请严格按照JSON格式输出（仅输出JSON，不要解释文本）:
- text_id: 文本ID
- relations: 关系列表,每个关系包含:
    - id: 关系ID（从0开始递增）
    - from_id: 源实体ID
    - to_id: 目标实体ID
    - type: 关系类型(必须是上述定义的类型之一)

若无可抽取关系,请返回:
{{
    "text_id": "{text_id}",
    "relations": []
}}

## 待标注文本

文本ID: {text_id}
文本内容: {text}

已标注实体:
{entity_list_str}

请开始标注关系:"""

        return prompt
    
    @staticmethod
    def build_prompt_preview(
        entity_types: List[EntityType],
        relation_types: List[RelationType]
    ) -> dict:
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
        
        # 统计审核状态
        entity_reviewed = sum(1 for et in entity_types if et.is_reviewed)
        entity_pending = len(entity_types) - entity_reviewed
        
        relation_reviewed = sum(1 for rt in relation_types if rt.is_reviewed)
        relation_pending = len(relation_types) - relation_reviewed
        
        return {
            'entity_types_section': entity_section,
            'relation_types_section': relation_section,
            'entity_count': len(entity_types),
            'entity_reviewed_count': entity_reviewed,
            'entity_pending_count': entity_pending,
            'relation_count': len(relation_types),
            'relation_reviewed_count': relation_reviewed,
            'relation_pending_count': relation_pending,
            'total_reviewed': entity_reviewed + relation_reviewed,
            'total_pending': entity_pending + relation_pending
        }
