"""
实体抽取Agent
使用LangChain v1.0 + Qwen-Max进行自动化实体标注
"""
import json
import logging
import re
from typing import List, Optional
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from config import settings
from models.db_models import EntityType
from services.dynamic_prompt_builder import DynamicPromptBuilder
from services.offset_correction import OffsetCorrectionService

logger = logging.getLogger(__name__)


# ============================================================================
# 输出模型定义
# ============================================================================

class ExtractedEntity(BaseModel):
    """提取的实体"""
    id: int = Field(..., description="实体ID，从0开始")
    token: str = Field(..., description="实体文本")
    label: str = Field(..., description="实体类型标签")
    start_offset: int = Field(..., description="起始偏移量")
    end_offset: int = Field(..., description="结束偏移量")
    confidence: Optional[float] = Field(None, description="置信度(0-1)，可选")


class EntityExtractionOutput(BaseModel):
    """实体抽取输出"""
    text_id: str = Field(..., description="文本ID")
    entities: List[ExtractedEntity] = Field(default_factory=list, description="提取的实体列表")


# ============================================================================
# Prompt模板
# ============================================================================

ENTITY_EXTRACTION_PROMPT = """你是一个专业的品质失效案例实体抽取专家。请从给定的文本中精准抽取实体。

## 实体类型定义（共16类）

1. **产品** (Product): 具体的产品名称、型号、部件
   - 示例: "电机", "控制器", "显示屏", "XX型号主板"

2. **问题类型** (IssueType): 质量问题的分类
   - 示例: "外观缺陷", "功能失效", "性能不达标", "尺寸偏差"

3. **缺陷现象** (DefectPhenomenon): 具体的缺陷表现
   - 示例: "划痕", "裂纹", "变色", "无法启动", "噪音过大"

4. **原因分类** (CauseCategory): 问题原因的4M分类
   - 示例: "人员因素", "机器因素", "物料因素", "方法因素", "环境因素"

5. **具体原因** (SpecificCause): 详细的问题原因
   - 示例: "操作不当", "设备老化", "原材料不合格", "工艺参数错误"

6. **工序** (Process): 生产工序或过程
   - 示例: "焊接", "组装", "测试", "包装", "喷涂"

7. **设备** (Equipment): 生产设备或工具
   - 示例: "焊接机", "测试仪", "组装线", "检测设备"

8. **物料** (Material): 原材料或零部件
   - 示例: "钢材", "塑料", "电子元件", "螺丝"

9. **人员** (Personnel): 相关人员或岗位
   - 示例: "操作工", "质检员", "工程师", "班长"

10. **客户** (Customer): 客户名称或类型
    - 示例: "XX公司", "终端用户", "经销商"

11. **供应商** (Supplier): 供应商名称
    - 示例: "XX供应商", "原材料厂商"

12. **处理措施** (Action): 采取的纠正或预防措施
    - 示例: "返工", "报废", "加强检验", "调整参数", "培训"

13. **时间** (Time): 时间信息
    - 示例: "2022年", "3月", "第一季度"

14. **地点** (Location): 地理位置或工厂
    - 示例: "XX工厂", "生产线A", "仓库"

15. **数量** (Quantity): 数量信息
    - 示例: "100件", "5%", "3批次"

16. **标准** (Standard): 相关标准或规范
    - 示例: "GB/T标准", "ISO9001", "企业标准"

## 标注原则

1. **实体边界清晰**: 准确标注实体的起始和结束位置
2. **避免重叠**: 实体之间不应重叠，长词优先
3. **保留原文**: token字段必须与原文完全一致
4. **偏移量准确**: start_offset和end_offset必须准确对应原文位置（UTF-8字符索引）
5. **类型准确**: 严格按照16种实体类型标注

## 输出格式

请严格按照JSON格式输出：
{
  "text_id": "文本ID",
  "entities": [
    {
      "id": 0,
      "token": "实体文本",
      "label": "实体类型",
      "start_offset": 起始位置,
      "end_offset": 结束位置
    }
  ]
}

## 示例

输入文本[ID:001]: "产品外观有划痕，经检查发现是焊接工序中操作不当导致。"

输出:
{
  "text_id": "001",
  "entities": [
    {"id": 0, "token": "产品", "label": "Product", "start_offset": 0, "end_offset": 2},
    {"id": 1, "token": "划痕", "label": "DefectPhenomenon", "start_offset": 5, "end_offset": 7},
    {"id": 2, "token": "焊接", "label": "Process", "start_offset": 15, "end_offset": 17},
    {"id": 3, "token": "操作不当", "label": "SpecificCause", "start_offset": 20, "end_offset": 24}
  ]
}

现在请处理以下文本：
"""


# ============================================================================
# Agent类
# ============================================================================

class EntityExtractionAgent:
    """实体抽取Agent"""
    
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
        
        # 创建偏移量修正服务
        self.offset_service = OffsetCorrectionService()
    
    def extract_entities(
        self,
        text_id: str,
        text: str,
        entity_types: Optional[List[EntityType]] = None
    ) -> EntityExtractionOutput:
        """
        提取实体
        
        Args:
            text_id: 文本ID
            text: 原始文本
            
        Returns:
            EntityExtractionOutput
        """
        # 构建prompt（优先使用动态标签体系）
        if entity_types:
            prompt = DynamicPromptBuilder.build_entity_extraction_prompt(
                text_id=text_id,
                text=text,
                entity_types=entity_types
            )
        else:
            prompt = f"{ENTITY_EXTRACTION_PROMPT}\n文本ID: {text_id}\n文本内容: {text}"
        
        try:
            # 直接调用LLM获取原始文本输出（兼容DashScope/Qwen）
            raw_response = self.llm.invoke(prompt)
            raw_text = raw_response.content if hasattr(raw_response, 'content') else str(raw_response)
            logger.debug(f"[实体抽取] text_id={text_id} 原始响应: {raw_text[:500]}")
            
            # 从响应中提取JSON
            json_text = self._extract_json(raw_text)
            data = json.loads(json_text)
            
            entities = [
                ExtractedEntity(
                    id=e.get('id', idx),
                    token=e['token'],
                    label=e['label'],
                    start_offset=e['start_offset'],
                    end_offset=e['end_offset'],
                    confidence=e.get('confidence')
                )
                for idx, e in enumerate(data.get('entities', []))
            ]
            logger.info(f"[实体抽取] text_id={text_id} LLM返回实体数={len(entities)}")
            
            # 验证和修正偏移量
            corrected_entities = []
            for entity in entities:
                corrected_start, corrected_end, log = self.offset_service.correct_offset(
                    text=text,
                    entity_text=entity.token,
                    start_offset=entity.start_offset,
                    end_offset=entity.end_offset
                )
                if corrected_start is not None and corrected_end is not None:
                    entity.start_offset = corrected_start
                    entity.end_offset = corrected_end
                    corrected_entities.append(entity)
                else:
                    logger.warning(f"[实体抽取] 实体 '{entity.token}' 偏移量修正失败，已跳过")
            
            logger.info(f"[实体抽取] text_id={text_id} 偏移量修正后实体数={len(corrected_entities)}")
            return EntityExtractionOutput(text_id=text_id, entities=corrected_entities)
            
        except Exception as e:
            logger.error(f"[实体抽取] text_id={text_id} 失败: {e}", exc_info=True)
            return EntityExtractionOutput(text_id=text_id, entities=[])
    
    @staticmethod
    def _extract_json(text: str) -> str:
        """从LLM响应中提取JSON块。"""
        # 优先提取 ```json ... ``` 代码块
        match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if match:
            return match.group(1).strip()
        # 尝试直接找到第一个 { ... } 大块
        match = re.search(r'(\{[\s\S]*\})', text)
        if match:
            return match.group(1).strip()
        return text.strip()
    
    def get_correction_stats(self):
        """获取偏移量修正统计"""
        return self.offset_service.get_correction_stats()
    
    def clear_correction_logs(self):
        """清空修正日志"""
        self.offset_service.clear_logs()


# ============================================================================
# 全局单例
# ============================================================================

_entity_agent: Optional[EntityExtractionAgent] = None


def get_entity_agent() -> EntityExtractionAgent:
    """获取实体抽取Agent实例（单例模式）"""
    global _entity_agent
    if _entity_agent is None:
        _entity_agent = EntityExtractionAgent()
    return _entity_agent
