"""
标签定义生成Agent
使用LLM自动生成实体类型和关系类型的详细定义
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from config import settings


# ============================================================================
# 输出模型定义
# ============================================================================

class EntityTypeDefinition(BaseModel):
    """实体类型定义"""
    type_name: str = Field(..., description="实体类型英文名")
    type_name_zh: str = Field(..., description="实体类型中文名")
    definition: str = Field(..., description="标准定义（详细说明该实体类型的含义和范围）")
    examples: List[str] = Field(..., description="示例列表（至少3个典型示例）")
    disambiguation: str = Field(..., description="类别辨析（与相似类型的区别）")


class RelationTypeDefinition(BaseModel):
    """关系类型定义"""
    type_name: str = Field(..., description="关系类型英文名")
    type_name_zh: str = Field(..., description="关系类型中文名")
    definition: str = Field(..., description="标准定义（详细说明该关系类型的含义）")
    direction_rule: str = Field(..., description="方向规则（说明from和to的实体类型约束）")
    examples: List[str] = Field(..., description="示例列表（格式：实体A --[关系]--> 实体B）")
    disambiguation: str = Field(..., description="类别辨析（与相似关系的区别）")


# ============================================================================
# Prompt模板
# ============================================================================

ENTITY_TYPE_DEFINITION_PROMPT = """你是一个专业的品质失效案例领域专家。请为给定的实体类型生成详细的标准定义。

## 任务说明

你需要为以下实体类型生成完整的定义信息：
- **实体类型**: {type_name_zh} ({type_name})
- **简短描述**: {description}

## 输出要求

请生成以下内容：

1. **标准定义** (definition):
   - 详细说明该实体类型的含义和范围
   - 明确该类型包含哪些内容，不包含哪些内容
   - 长度：100-200字

2. **示例列表** (examples):
   - 提供至少5个典型示例
   - 示例应覆盖不同的场景和表达方式
   - 每个示例应简洁明确

3. **类别辨析** (disambiguation):
   - 说明该类型与相似类型的区别
   - 帮助标注人员准确区分易混淆的类型
   - 长度：50-100字

## 领域背景

这是一个品质失效案例分析系统，主要处理制造业的质量问题记录。实体类型应该符合品质管理和失效分析的专业术语。

## 输出格式

请严格按照JSON格式输出：
{{
  "type_name": "{type_name}",
  "type_name_zh": "{type_name_zh}",
  "definition": "标准定义内容",
  "examples": ["示例1", "示例2", "示例3", "示例4", "示例5"],
  "disambiguation": "类别辨析内容"
}}
"""

RELATION_TYPE_DEFINITION_PROMPT = """你是一个专业的品质失效案例领域专家。请为给定的关系类型生成详细的标准定义。

## 任务说明

你需要为以下关系类型生成完整的定义信息：
- **关系类型**: {type_name_zh} ({type_name})
- **简短描述**: {description}

## 输出要求

请生成以下内容：

1. **标准定义** (definition):
   - 详细说明该关系类型的含义
   - 明确该关系表达什么样的语义联系
   - 长度：100-200字

2. **方向规则** (direction_rule):
   - 明确说明from实体和to实体的类型约束
   - 格式：from实体类型 -> to实体类型
   - 说明方向的语义含义

3. **示例列表** (examples):
   - 提供至少5个典型示例
   - 格式：实体A --[关系类型]--> 实体B
   - 示例应覆盖不同的场景

4. **类别辨析** (disambiguation):
   - 说明该关系与相似关系的区别
   - 帮助标注人员准确区分易混淆的关系
   - 长度：50-100字

## 领域背景

这是一个品质失效案例分析系统，关系类型应该符合因果分析、过程追溯等品质管理的专业逻辑。

## 输出格式

请严格按照JSON格式输出：
{{
  "type_name": "{type_name}",
  "type_name_zh": "{type_name_zh}",
  "definition": "标准定义内容",
  "direction_rule": "from实体类型 -> to实体类型的规则说明",
  "examples": ["示例1", "示例2", "示例3", "示例4", "示例5"],
  "disambiguation": "类别辨析内容"
}}
"""


# ============================================================================
# Agent类
# ============================================================================

class LabelDefinitionGenerator:
    """标签定义生成Agent"""
    
    def __init__(self):
        """初始化Agent"""
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=0.3,  # 稍高的温度以获得更丰富的内容
            api_key=settings.DASHSCOPE_API_KEY,
            base_url=settings.DASHSCOPE_BASE_URL
        )
    
    def generate_entity_type_definition(
        self,
        type_name: str,
        type_name_zh: str,
        description: str
    ) -> EntityTypeDefinition:
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
            type_name=type_name,
            type_name_zh=type_name_zh,
            description=description
        )
        
        # 使用结构化输出
        structured_llm = self.llm.with_structured_output(EntityTypeDefinition)
        
        try:
            result = structured_llm.invoke(prompt)
            return result
        except Exception as e:
            print(f"生成实体类型定义失败: {str(e)}")
            # 返回基础定义
            return EntityTypeDefinition(
                type_name=type_name,
                type_name_zh=type_name_zh,
                definition=description,
                examples=[],
                disambiguation=""
            )
    
    def generate_relation_type_definition(
        self,
        type_name: str,
        type_name_zh: str,
        description: str
    ) -> RelationTypeDefinition:
        """
        生成关系类型定义
        
        Args:
            type_name: 关系类型英文名
            type_name_zh: 关系类型中文名
            description: 简短描述
            
        Returns:
            RelationTypeDefinition
        """
        # 构建prompt
        prompt = RELATION_TYPE_DEFINITION_PROMPT.format(
            type_name=type_name,
            type_name_zh=type_name_zh,
            description=description
        )
        
        # 使用结构化输出
        structured_llm = self.llm.with_structured_output(RelationTypeDefinition)
        
        try:
            result = structured_llm.invoke(prompt)
            return result
        except Exception as e:
            print(f"生成关系类型定义失败: {str(e)}")
            # 返回基础定义
            return RelationTypeDefinition(
                type_name=type_name,
                type_name_zh=type_name_zh,
                definition=description,
                direction_rule="",
                examples=[],
                disambiguation=""
            )


# ============================================================================
# 全局单例
# ============================================================================

_label_generator: Optional[LabelDefinitionGenerator] = None


def get_label_generator() -> LabelDefinitionGenerator:
    """获取标签定义生成器实例（单例模式）"""
    global _label_generator
    if _label_generator is None:
        _label_generator = LabelDefinitionGenerator()
    return _label_generator
