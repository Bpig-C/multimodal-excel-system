# 数据库表结构

> 最后更新：2026-04-02（代码模型核对一致）

## 核心标注模块

### users - 用户表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| username | VARCHAR(50) | 用户名，唯一 |
| password_hash | VARCHAR(255) | 密码哈希 |
| role | VARCHAR(20) | 角色：admin/annotator/reviewer/browser |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### corpus - 原始语料表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| text_id | VARCHAR(100) | 语料唯一ID |
| text | TEXT | 语料内容 |
| text_type | VARCHAR(100) | 句子分类 |
| source_file | VARCHAR(255) | 来源文件 |
| source_row | INTEGER | 来源行号 |
| source_field | VARCHAR(100) | 来源字段 |
| has_images | BOOLEAN | 是否有图片 |

### images - 图片表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| image_id | VARCHAR(100) | 图片唯一ID |
| corpus_id | INTEGER | 关联语料ID |
| file_path | VARCHAR(500) | 文件路径 |
| original_name | VARCHAR(255) | 原始文件名 |
| width | INTEGER | 图片宽度 |
| height | INTEGER | 图片高度 |

### datasets - 数据集表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| dataset_id | VARCHAR(100) | 数据集唯一ID |
| name | VARCHAR(255) | 数据集名称 |
| description | TEXT | 描述 |
| label_schema_version_id | INTEGER | 标签体系版本ID |
| created_by | INTEGER | 创建人ID |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### dataset_corpus - 数据集-语料关联表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| dataset_id | INTEGER | 数据集ID |
| corpus_id | INTEGER | 语料ID |
| created_at | DATETIME | 创建时间 |

**唯一约束**：dataset_id + corpus_id

### dataset_assignments - 数据集分配表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| dataset_id | INTEGER | 数据集ID |
| user_id | INTEGER | 用户ID |
| role | VARCHAR(20) | annotator/reviewer |
| task_start_index | INTEGER | 任务起始索引 |
| task_end_index | INTEGER | 任务结束索引 |
| is_active | BOOLEAN | 是否激活 |
| transferred_to | INTEGER | 转移给谁 |
| transferred_at | DATETIME | 转移时间 |
| assigned_by | INTEGER | 分配人ID |
| assigned_at | DATETIME | 分配时间 |

### annotation_tasks - 标注任务表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| task_id | VARCHAR(100) | 任务唯一ID |
| dataset_id | INTEGER | 数据集ID |
| corpus_id | INTEGER | 语料ID |
| status | VARCHAR(20) | pending/processing/completed/failed |
| annotation_type | VARCHAR(20) | automatic/manual |
| current_version | INTEGER | 当前版本号 |
| assigned_to | INTEGER | 指派人ID |
| error_message | TEXT | 错误信息 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### text_entities - 文本实体表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| entity_id | INTEGER | 实体在任务内的ID |
| task_id | INTEGER | 任务ID |
| version | INTEGER | 版本号 |
| token | TEXT | 实体文本 |
| label | VARCHAR(50) | 实体类型 |
| start_offset | INTEGER | 起始偏移 |
| end_offset | INTEGER | 结束偏移 |
| confidence | FLOAT | 置信度 |

### image_entities - 图片实体表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| entity_id | INTEGER | 实体在任务内的ID |
| task_id | INTEGER | 任务ID |
| image_id | INTEGER | 图片ID |
| version | INTEGER | 版本号 |
| label | VARCHAR(50) | 实体类型 |
| bbox_x | INTEGER | 边界框X |
| bbox_y | INTEGER | 边界框Y |
| bbox_width | INTEGER | 边界框宽度 |
| bbox_height | INTEGER | 边界框高度 |
| confidence | FLOAT | 置信度 |

### relations - 关系表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| relation_id | INTEGER | 关系在任务内的ID |
| task_id | INTEGER | 任务ID |
| version | INTEGER | 版本号 |
| from_entity_id | INTEGER | 起始实体ID |
| to_entity_id | INTEGER | 目标实体ID |
| relation_type | VARCHAR(50) | 关系类型 |
| created_at | DATETIME | 创建时间 |

### entity_types - 实体类型配置表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| type_name | VARCHAR(50) | 类型名（英文，唯一） |
| type_name_zh | VARCHAR(50) | 类型名（中文） |
| color | VARCHAR(20) | 颜色 |
| description | TEXT | 简短描述 |
| definition | TEXT | LLM生成的标准定义 |
| examples | TEXT | 示例（JSON） |
| disambiguation | TEXT | 类别辨析 |
| prompt_template | TEXT | Prompt模板 |
| supports_bbox | BOOLEAN | 是否支持边界框 |
| is_active | BOOLEAN | 是否启用 |
| is_reviewed | BOOLEAN | 是否已审核 |
| reviewed_by | INTEGER | 审核人ID |
| reviewed_at | DATETIME | 审核时间 |

### relation_types - 关系类型配置表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| type_name | VARCHAR(50) | 类型名（英文，唯一） |
| type_name_zh | VARCHAR(50) | 类型名（中文） |
| color | VARCHAR(20) | 颜色 |
| description | TEXT | 简短描述 |
| definition | TEXT | LLM生成的标准定义 |
| direction_rule | TEXT | 方向规则 |
| examples | TEXT | 示例（JSON） |
| disambiguation | TEXT | 类别辨析 |
| prompt_template | TEXT | Prompt模板 |
| is_active | BOOLEAN | 是否启用 |
| is_reviewed | BOOLEAN | 是否已审核 |

### review_tasks - 复核任务表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| review_id | VARCHAR(100) | 复核唯一ID |
| task_id | INTEGER | 关联标注任务ID |
| status | VARCHAR(20) | pending/approved/rejected |
| reviewer_id | INTEGER | 复核人ID |
| review_comment | TEXT | 复核意见 |
| reviewed_at | DATETIME | 复核时间 |
| created_at | DATETIME | 创建时间 |

### version_history - 版本历史表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| history_id | VARCHAR(100) | 历史唯一ID |
| task_id | INTEGER | 任务ID |
| version | INTEGER | 版本号 |
| change_type | VARCHAR(20) | create/update/delete |
| change_description | TEXT | 变更描述 |
| changed_by | INTEGER | 变更人ID |
| snapshot_data | TEXT | 完整快照（JSON） |
| created_at | DATETIME | 创建时间 |

### batch_jobs - 批量任务表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| job_id | VARCHAR(100) | 任务唯一ID |
| dataset_id | INTEGER | 数据集ID |
| status | VARCHAR(20) | pending/processing/completed/failed |
| total_tasks | INTEGER | 总任务数 |
| completed_tasks | INTEGER | 已完成任务数 |
| failed_tasks | INTEGER | 失败任务数 |
| progress | FLOAT | 进度 0.0-1.0 |
| error_message | TEXT | 错误信息 |
| created_by | INTEGER | 创建人ID |
| started_at | DATETIME | 开始时间 |
| completed_at | DATETIME | 完成时间 |
| created_at | DATETIME | 创建时间 |

### label_schema_versions - 标签体系版本表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| version_id | VARCHAR(100) | 版本唯一ID |
| version_name | VARCHAR(255) | 版本名称 |
| description | TEXT | 版本描述 |
| schema_data | TEXT | 完整标签配置快照（JSON） |
| is_active | BOOLEAN | 是否为当前活跃版本 |
| created_by | INTEGER | 创建人ID |
| created_at | DATETIME | 创建时间 |

## KF/QMS 处理器模块

### customers - 客户表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | VARCHAR(255) | 客户名称，唯一 |

### products - 产品型号表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| model | VARCHAR(255) | 型号，唯一 |
| product_category | VARCHAR(255) | 产品类别 |
| industry_category | VARCHAR(255) | 行业类别 |

### defects - 缺陷类型表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | VARCHAR(255) | 缺陷名称，唯一 |

### root_causes - 异常原因表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| category | VARCHAR(255) | 类别 |
| process_category | VARCHAR(255) | 过程类别 |

### four_m_elements - 4M要素表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| element | VARCHAR(255) | 要素名称，唯一 |

### quick_response_events - 快反事件表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(100) | 主键（非自增） |
| occurrence_time | DATETIME | 发生时间 |
| problem_analysis | TEXT | 问题分析 |
| short_term_measure | TEXT | 短期措施 |
| long_term_measure | TEXT | 长期措施 |
| images | TEXT | 图片路径 |
| data_source | VARCHAR(255) | 数据来源 |
| classification | VARCHAR(255) | 分类 |
| customer_id | INTEGER | 客户ID |
| product_id | INTEGER | 产品ID |
| defect_id | INTEGER | 缺陷ID |
| root_cause_id | INTEGER | 原因ID |
| four_m_id | INTEGER | 4M要素ID |

### qms_workshops - QMS车间表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | VARCHAR(255) | 车间名称，唯一 |

### qms_production_lines - QMS产线表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | VARCHAR(255) | 产线名称 |
| workshop_id | INTEGER | 车间ID |

**唯一约束**：name + workshop_id

### qms_stations - QMS岗位表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | VARCHAR(255) | 岗位名称，唯一 |

### qms_inspection_nodes - QMS质检节点表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | VARCHAR(255) | 节点名称，唯一 |

### qms_defect_orders - QMS不合格品记录表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| order_id | VARCHAR(100) | 制令单号（非唯一，同一制令单号可对应多条记录）|
| content_hash | VARCHAR(64) | 整行内容哈希，唯一约束，作为去重依据 |
| entry_time | VARCHAR(255) | 录入时间 |
| model | VARCHAR(255) | 型号 |
| barcode | VARCHAR(255) | 条码 |
| position | VARCHAR(255) | 位置 |
| photo_path | TEXT | 照片路径 |
| status | VARCHAR(255) | 状态 |
| data_source | VARCHAR(255) | 数据来源 |
| customer_id | INTEGER | 客户ID |
| workshop_id | INTEGER | 车间ID |
| line_id | INTEGER | 产线ID |
| station_id | INTEGER | 岗位ID |
| defect_id | INTEGER | 缺陷ID |
| inspection_node_id | INTEGER | 质检节点ID |
