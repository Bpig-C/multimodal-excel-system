"""KF（快反问题记录）处理器配置 - 所有 KF 特有常量集中在此"""

# 源字段名 → 标准实体字段名
FIELD_MAPPING = {
    'event_id': '快反编号',
    'occurrence_time': '发生时间',
    'problem_analysis': '问题原因及分析',
    'images': '问题图片',
    'short_term_measure': '短期改善措施',
    'long_term_measure': '长期改善措施',
    'classification': '所属分类',
    'customer': '客户名称',
    'product_model': '产品型号',
    'product_category': '产品分类',
    'industry_category': '行业类别',
    'defect': '缺陷类型不良现象',
    'root_cause_category': '异常原因',
    'process_category': '过程分类',
    'four_m_element': '4M要素',
}

# 老版本 Excel 缺失字段默认值
DEFAULT_VALUES = {
    '4M要素': '未分类',
    '行业类别': '未分类',
    '产品分类': '未分类',
    '过程分类': '未分类',
    '异常原因': '未分类',
}

# Excel 列名重映射（旧/别名 → 标准名）
COLUMN_MAPPINGS = {
    "经验类别1": "4M要素",
    "经验类别2": "行业类别",
    "经验类别3": "产品分类",
    "经验类别4": "过程分类",
    "经验类别5": "异常原因",
    "缺陷类型": "缺陷类型不良现象",
    "流出原因": "异常原因",
    "短期措施": "短期改善措施",
    "长期措施": "长期改善措施",
    "问题描述": "问题原因及分析",
}

# --- 导出配置 ---

# 实体标注字段 [(源字段名, 实体标签)]
ENTITY_FIELDS = [
    ('快反编号', 'EVENT_ID'),
    ('发生时间', 'DATE'),
    ('4M要素', 'FOUR_M'),
    ('行业类别', 'INDUSTRY'),
    ('产品分类', 'PRODUCT_CATEGORY'),
    ('过程分类', 'PROCESS'),
    ('异常原因', 'ROOT_CAUSE'),
    ('客户名称', 'CUSTOMER'),
    ('产品型号', 'PRODUCT_MODEL'),
    ('缺陷类型不良现象', 'DEFECT_TYPE'),
    ('短期改善措施', 'SHORT_TERM_MEASURE'),
    ('长期改善措施', 'LONG_TERM_MEASURE'),
]

# 关系映射 [(源字段名, 关系类型)]
RELATION_MAPPINGS = [
    ('客户名称', 'hasCustomer'),
    ('产品型号', 'hasProduct'),
    ('缺陷类型不良现象', 'hasDefect'),
    ('异常原因', 'hasCause'),
    ('4M要素', 'involves4M'),
    ('发生时间', 'occurredAt'),
    ('行业类别', 'belongsToIndustry'),
    ('产品分类', 'hasProductCategory'),
    ('过程分类', 'hasProcessCategory'),
    ('短期改善措施', 'hasShortTermMeasure'),
    ('长期改善措施', 'hasLongTermMeasure'),
]

# Q&A 查询模板
QA_QUERY = "当前缺陷是什么？是什么原因导致的？如何解决？"

# CLIP 导出字段顺序
CLIP_FIELDS = [
    '快反编号', '发生时间', '问题原因及分析', '4M要素',
    '行业类别', '产品分类', '过程分类', '异常原因',
    '客户名称', '产品型号', '缺陷类型不良现象',
    '短期改善措施', '长期改善措施', '所属分类',
]

# --- 图谱可视化配置 ---

NODE_TYPES = {
    'QuickResponseEvent': {'label': '快反事件', 'color': '#409eff'},
    'Customer': {'label': '客户', 'color': '#67c23a'},
    'ProductModel': {'label': '产品型号', 'color': '#e6a23c'},
    'DefectType': {'label': '缺陷类型', 'color': '#f56c6c'},
    'RootCause': {'label': '异常原因', 'color': '#909399'},
    'FourMElement': {'label': '4M要素', 'color': '#b88230'},
}

EDGE_LABELS = {
    'BELONGS_TO_CUSTOMER': '归属客户',
    'INVOLVES_PRODUCT': '涉及产品',
    'HAS_DEFECT': '缺陷类型',
    'ATTRIBUTED_TO': '异常原因',
    'RELATED_TO_4M': '4M要素',
}
