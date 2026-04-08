"""QMS（不合格品记录）处理器配置 - 所有 QMS 特有常量集中在此"""

# 源字段名 → 标准实体字段名
FIELD_MAPPING = {
    'event_id': '制令单号',
    'occurrence_time': '录入时间',
    'defect': '不良项目',
    'images': '照片',
    'customer': '客户名称',
    'product_model': '型号',
    'barcode': '条码',
    'position': '位号',
    'workshop': '车间',
    'production_line': '产线',
    'station': '岗位',
    'inspection_node': '质检节点',
    'status': '状态',
}

# QMS 无可选字段
DEFAULT_VALUES = {}

# QMS 列名固定，无需重映射
COLUMN_MAPPINGS = {}

# --- 导出配置 ---

# 实体标注字段 [(源字段名, 实体标签)]
ENTITY_FIELDS = [
    ('制令单号', 'EVENT_ID'),
    ('录入时间', 'DATE'),
    ('客户名称', 'CUSTOMER'),
    ('型号', 'PRODUCT_MODEL'),
    ('条码', 'BARCODE'),
    ('位号', 'POSITION'),
    ('车间', 'WORKSHOP'),
    ('产线', 'PRODUCTION_LINE'),
    ('岗位', 'STATION'),
    ('不良项目', 'DEFECT_TYPE'),
    ('质检节点', 'INSPECTION_NODE'),
    ('状态', 'STATUS'),
]

# 关系映射 [(源字段名, 关系类型)]
RELATION_MAPPINGS = [
    ('客户名称', 'hasCustomer'),
    ('型号', 'hasProduct'),
    ('不良项目', 'hasDefect'),
    ('车间', 'hasWorkshop'),
    ('产线', 'hasProductionLine'),
    ('岗位', 'hasStation'),
    ('质检节点', 'hasInspectionNode'),
    ('状态', 'hasStatus'),
    ('录入时间', 'occurredAt'),
]

# Q&A 查询模板
QA_QUERY = "这是什么不良现象？发生在哪个工位？如何处理？"

# CLIP 导出字段顺序
CLIP_FIELDS = [
    '制令单号', '录入时间', '客户名称', '型号',
    '条码', '位号', '车间', '产线',
    '岗位', '不良项目', '质检节点', '状态',
]

# --- 图谱可视化配置 ---

NODE_TYPES = {
    'DefectOrder': {'label': '不合格品记录', 'color': '#409eff'},
    'Customer': {'label': '客户', 'color': '#67c23a'},
    'ProductModel': {'label': '产品型号', 'color': '#e6a23c'},
    'Workshop': {'label': '车间', 'color': '#9b59b6'},
    'ProductionLine': {'label': '产线', 'color': '#1abc9c'},
    'Station': {'label': '岗位', 'color': '#e74c3c'},
    'DefectType': {'label': '不良项目', 'color': '#f56c6c'},
    'InspectionNode': {'label': '质检节点', 'color': '#909399'},
}

EDGE_LABELS = {
    'BELONGS_TO_CUSTOMER': '归属客户',
    'INVOLVES_PRODUCT': '涉及产品',
    'HAS_DEFECT': '不良项目',
    'IN_WORKSHOP': '所在车间',
    'ON_PRODUCTION_LINE': '所在产线',
    'AT_STATION': '所在岗位',
    'INSPECTED_AT': '质检节点',
}
