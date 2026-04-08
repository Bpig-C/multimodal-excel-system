"""
偏移量验证与修正服务
用于验证和修正LLM标注的实体偏移量
"""
from typing import Tuple, Optional, List, Dict
from dataclasses import dataclass
import re


@dataclass
class CorrectionLog:
    """修正日志"""
    entity_text: str
    original_start: int
    original_end: int
    corrected_start: Optional[int]
    corrected_end: Optional[int]
    correction_type: str  # 'exact_match', 'fuzzy_match', 'failed'
    message: str


class OffsetCorrectionService:
    """偏移量验证与修正服务"""
    
    def __init__(self):
        self.correction_logs: List[CorrectionLog] = []
    
    def validate_offset(
        self,
        text: str,
        entity_text: str,
        start_offset: int,
        end_offset: int
    ) -> bool:
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
        if start_offset < 0 or end_offset > len(text) or start_offset >= end_offset:
            return False
        
        # 检查偏移量对应的文本是否匹配
        extracted_text = text[start_offset:end_offset]
        
        # 精确匹配
        if extracted_text == entity_text:
            return True
        
        # 去除空格后匹配
        if extracted_text.strip() == entity_text.strip():
            return True
        
        return False
    
    def correct_offset(
        self,
        text: str,
        entity_text: str,
        start_offset: int,
        end_offset: int,
        max_search_distance: int = 50
    ) -> Tuple[Optional[int], Optional[int], CorrectionLog]:
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
        if self.validate_offset(text, entity_text, start_offset, end_offset):
            log = CorrectionLog(
                entity_text=entity_text,
                original_start=start_offset,
                original_end=end_offset,
                corrected_start=start_offset,
                corrected_end=end_offset,
                correction_type='exact_match',
                message='偏移量正确，无需修正'
            )
            self.correction_logs.append(log)
            return start_offset, end_offset, log
        
        # 尝试查找最近匹配
        corrected_start, corrected_end = self.find_closest_match(
            text, entity_text, start_offset, max_search_distance
        )
        
        if corrected_start is not None and corrected_end is not None:
            log = CorrectionLog(
                entity_text=entity_text,
                original_start=start_offset,
                original_end=end_offset,
                corrected_start=corrected_start,
                corrected_end=corrected_end,
                correction_type='fuzzy_match',
                message=f'偏移量已修正: ({start_offset}, {end_offset}) -> ({corrected_start}, {corrected_end})'
            )
            self.correction_logs.append(log)
            return corrected_start, corrected_end, log
        
        # 无法修正
        log = CorrectionLog(
            entity_text=entity_text,
            original_start=start_offset,
            original_end=end_offset,
            corrected_start=None,
            corrected_end=None,
            correction_type='failed',
            message=f'无法找到匹配的文本: "{entity_text}"'
        )
        self.correction_logs.append(log)
        return None, None, log

    def find_closest_match(
        self,
        text: str,
        entity_text: str,
        hint_offset: int,
        max_distance: int = 50
    ) -> Tuple[Optional[int], Optional[int]]:
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
        
        if entity_len == 0:
            return None, None
        
        # 定义搜索范围
        search_start = max(0, hint_offset - max_distance)
        search_end = min(len(text), hint_offset + max_distance + entity_len)
        
        # 策略1: 精确匹配
        start_pos = text.find(entity_clean, search_start, search_end)
        if start_pos != -1:
            return start_pos, start_pos + entity_len
        
        # 策略2: 去除所有空格后匹配
        entity_no_space = entity_clean.replace(' ', '')
        text_no_space = text[search_start:search_end].replace(' ', '')
        
        pos_in_no_space = text_no_space.find(entity_no_space)
        if pos_in_no_space != -1:
            # 需要映射回原始文本的位置
            original_pos = self._map_position_with_spaces(
                text[search_start:search_end],
                pos_in_no_space,
                len(entity_no_space)
            )
            if original_pos:
                start, end = original_pos
                return search_start + start, search_start + end
        
        # 策略3: 模糊匹配（忽略标点和空格）
        entity_normalized = self._normalize_text(entity_clean)
        
        # 在搜索范围内滑动窗口查找
        for i in range(search_start, search_end - entity_len + 1):
            window = text[i:i + entity_len]
            window_normalized = self._normalize_text(window)
            
            if window_normalized == entity_normalized:
                return i, i + entity_len
        
        # 策略4: 扩展窗口模糊匹配（允许长度差异）
        for window_len in range(entity_len - 5, entity_len + 10):
            if window_len <= 0:
                continue
            
            for i in range(search_start, search_end - window_len + 1):
                window = text[i:i + window_len]
                window_normalized = self._normalize_text(window)
                
                # 计算相似度
                if self._text_similarity(entity_normalized, window_normalized) > 0.8:
                    return i, i + window_len
        
        return None, None
    
    def _map_position_with_spaces(
        self,
        text: str,
        pos_no_space: int,
        length_no_space: int
    ) -> Optional[Tuple[int, int]]:
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
        
        for i, char in enumerate(text):
            if char != ' ':
                if char_count == pos_no_space:
                    start_pos = i
                char_count += 1
                
                if start_pos is not None and char_count == pos_no_space + length_no_space:
                    return start_pos, i + 1
        
        return None
    
    def _normalize_text(self, text: str) -> str:
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
        return text
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度（简单的字符匹配率）
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度 (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        # 使用最长公共子序列
        len1, len2 = len(text1), len(text2)
        
        # 简化版：计算字符匹配率
        matches = sum(1 for c1, c2 in zip(text1, text2) if c1 == c2)
        max_len = max(len1, len2)
        
        return matches / max_len if max_len > 0 else 0.0
    
    def get_correction_logs(self) -> List[CorrectionLog]:
        """
        获取所有修正日志
        
        Returns:
            修正日志列表
        """
        return self.correction_logs
    
    def clear_logs(self):
        """清空修正日志"""
        self.correction_logs = []
    
    def get_correction_stats(self) -> Dict[str, int]:
        """
        获取修正统计信息
        
        Returns:
            统计信息字典
        """
        stats = {
            'total': len(self.correction_logs),
            'exact_match': 0,
            'fuzzy_match': 0,
            'failed': 0
        }
        
        for log in self.correction_logs:
            if log.correction_type in stats:
                stats[log.correction_type] += 1
        
        return stats
