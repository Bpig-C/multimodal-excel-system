# 动态Prompt生成机制

## 概述

为了支持用户自定义标签体系，Agent的Prompt需要根据数据库中的标签配置动态生成。本文档说明动态Prompt生成的实现方案。

## 设计原则

1. **配置驱动**: 标签配置完全由数据库控制
2. **实时生效**: 修改数据库后，下次调用Agent即生效
3. **缓存优化**: 使用缓存减少数据库查询
4. **降级机制**: 如果数据库不可用，使用默认硬编码配置

## 架构设计

### 1. 标签配置缓存

```python
class LabelConfigCache:
    """标签配置缓存"""
    _entity_types_cache: Optional[List[EntityType]] = None
    _relation_types_cache: Optional[List[RelationType]] = None
    _cache_version: int = 0
    _cache_lock = threading.Lock()
    
    @classmethod
    def get_entity_types(cls, db_session) -> List[EntityType]:
        """获取实体类型配置（带缓存）"""
        with cls._cache_lock:
            current_version = cls._get_config_version(db_session)
            if current_version != cls._cache_version or cls._entity_types_cache is None:
                cls._entity_types_cache = db_session.query(EntityType)\
                    .filter(EntityType.is_active == True)\
                    .filter(EntityType.is_reviewed == True)\
                    .all()
                cls._cache_version = current_version
            return cls._entity_types_cache
    
    @classmethod
    def get_relation_types(cls, db_session) -> List[RelationType]:
        """获取关系类型配置（带缓存）"""
        with cls._cache_lock:
            current_version = cls._get_config_version(db_session)
            if current_version != cls._cache_version or cls._relation_types_cache is None:
                cls._relation_types_cache = db_session.query(RelationType)\
                    .filter(RelationType.is_active == True)\
                    .filter(RelationType.is_reviewed == True)\
                    .all()
                cls._cache_version = current_version
            return cls._relation_types_cache
    
    @classmethod
    def invalidate_cache(cls):
        """清空缓存（标签配置更新时调用）"""
        with cls._cache_lock:
            cls._entity_types_cache = None
            cls._relation_types_cache = None
            cls._cache_version += 1
    
    @classmethod
    def _get_config_version(cls, db_session) -> int:
        """获取配置版本号（基于最后更新时间）"""
        # 查询最新的updated_at时间戳作为版本号
        entity_max = db_session.query(func.max(EntityType.updated_at)).scalar()
        relation_max = db_session.query(func.max(RelationType.updated_at)).scalar()
        
        if entity_max and relation_max:
            return int(max(entity_max, relation_max).timestamp())
        return 0
```

### 2. 动态Prompt生成器

```python
class DynamicPromptBuilder:
    """动态Prompt构建器"""
    
    @staticmethod
    def build_entity_types_section(entity_types: List[EntityType]) -> str:
        """构建实体类型定义部分"""
        if not entity_types:
            return DEFAULT_ENTITY_TYPES_PROMPT
        
        sections = []
        for idx, et in enumerate(entity_types, 1):
            section = f"{idx}. **{et.type_name_zh}** ({et.type_name})"
            
            # 添加标准定义
            if et.definition:
                section += f"\n   - 定义: {et.definition}"
            elif et.description:
                section += f"\n   - 描述: {et.description}"
            
            # 添加示例
            if et.examples:
                examples = json.loads(et.examples) if isinstance(et.examples, str) else et.examples
                section += f"\n   - 示例: {', '.join(examples[:3])}"
            
            # 添加类别辨析
            if et.disambiguation:
                section += f"\n   - 辨析: {et.disambiguation}"
            
            sections.append(section)
        
        return "\n\n".join(sections)
    
    @staticmethod
    def build_relation_types_section(relation_types: List[RelationType]) -> str:
        """构建关系类型定义部分"""
        if not relation_types:
            return DEFAULT_RELATION_TYPES_PROMPT
        
        sections = []
        for idx, rt in enumerate(relation_types, 1):
            section = f"{idx}. **{rt.type_name_zh}** ({rt.type_name})"
            
            # 添加标准定义
            if rt.definition:
                section += f"\n   - 定义: {rt.definition}"
            elif rt.description:
                section += f"\n   - 描述: {rt.description}"
            
            # 添加方向规则
            if rt.direction_rule:
                section += f"\n   - 方向: {rt.direction_rule}"
            
            # 添加示例
            if rt.examples:
                examples = json.loads(rt.examples) if isinstance(rt.examples, str) else rt.examples
                section += f"\n   - 示例: {examples[0] if examples else ''}"
            
            # 添加类别辨析
            if rt.disambiguation:
                section += f"\n   - 辨析: {rt.disambiguation}"
            
            sections.append(section)
        
        return "\n\n".join(sections)
```

### 3. 更新Agent类

```python
class EntityExtractionAgent:
    """实体抽取Agent（支持动态Prompt）"""
    
    def __init__(self, db_session=None):
        """初始化Agent"""
        self.llm = ChatOpenAI(...)
        self.offset_service = OffsetCorrectionService()
        self.db_session = db_session
        self.prompt_builder = DynamicPromptBuilder()
    
    def extract_entities(self, text_id: str, text: str) -> EntityExtractionOutput:
        """提取实体（使用动态Prompt）"""
        # 获取实体类型配置
        if self.db_session:
            entity_types = LabelConfigCache.get_entity_types(self.db_session)
            entity_types_section = self.prompt_builder.build_entity_types_section(entity_types)
        else:
            # 降级：使用默认配置
            entity_types_section = DEFAULT_ENTITY_TYPES_PROMPT
        
        # 构建完整Prompt
        full_prompt = f"""你是一个专业的品质失效案例实体抽取专家。

## 实体类型定义

{entity_types_section}

## 标注原则

1. **实体边界清晰**: 准确标注实体的起始和结束位置
2. **避免重叠**: 实体之间不应重叠，长词优先
3. **保留原文**: token字段必须与原文完全一致
4. **偏移量准确**: start_offset和end_offset必须准确对应原文位置
5. **类型准确**: 严格按照上述实体类型标注

## 输出格式

请严格按照JSON格式输出...

文本ID: {text_id}
文本内容: {text}
"""
        
        # 调用LLM
        structured_llm = self.llm.with_structured_output(EntityExtractionOutput)
        result = structured_llm.invoke(full_prompt)
        
        # 验证和修正偏移量
        ...
        
        return result
```

## 使用流程

### 1. 标签配置更新流程

```
用户在前端修改标签配置
    ↓
调用API更新数据库
    ↓
API调用 LabelConfigCache.invalidate_cache()
    ↓
缓存失效，下次查询时重新加载
    ↓
Agent使用新配置生成Prompt
```

### 2. Agent调用流程

```
API接收标注请求
    ↓
创建数据库会话
    ↓
初始化Agent（传入db_session）
    ↓
Agent从缓存获取标签配置
    ↓
动态生成Prompt
    ↓
调用LLM进行标注
    ↓
返回结果
```

## 性能优化

### 1. 缓存策略

- **版本号机制**: 基于标签配置的最后更新时间生成版本号
- **线程安全**: 使用锁保护缓存读写
- **按需加载**: 只有在版本变化时才重新加载

### 2. 降级策略

- **默认配置**: 保留硬编码的默认配置
- **异常处理**: 数据库查询失败时使用默认配置
- **日志记录**: 记录降级事件便于排查

## 注意事项

1. **审核状态**: 只有已审核的标签才会用于Prompt生成
2. **活跃状态**: 只有活跃的标签才会被使用
3. **缓存失效**: 标签配置更新后必须调用 `invalidate_cache()`
4. **数据库会话**: Agent需要传入数据库会话才能使用动态配置
5. **向后兼容**: 如果不传入数据库会话，Agent使用默认硬编码配置

## 测试建议

1. **单元测试**: 测试Prompt生成逻辑
2. **集成测试**: 测试完整的配置更新→缓存失效→Prompt生成流程
3. **性能测试**: 测试缓存命中率和查询性能
4. **降级测试**: 测试数据库不可用时的降级行为
