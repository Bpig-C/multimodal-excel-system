# 实现计划

## 任务列表

- [x] 1. 项目初始化和基础架构搭建




  - 创建项目目录结构
  - 配置后端FastAPI项目（requirements.txt、main.py、config.py）
  - 配置前端Vue3项目（package.json、vite.config.ts、tsconfig.json）
  - 配置环境变量加载（python-dotenv）
  - 初始化SQLite数据库连接
  - 配置CORS和基础中间件
  - _Requirements: 所有需求的基础_

- [x] 2. 数据库模型和ORM配置



  - 创建SQLAlchemy Base和数据库引擎配置
  - 实现14个数据库表模型（users、corpus、images、datasets等）
  - 创建数据库初始化脚本（建表、索引）
  - 实现数据库迁移工具
  - _Requirements: 所有需求的基础_

- [x] 3. Pydantic数据模型定义



  - 定义实体模型（Entity、ImageEntity、BoundingBox）
  - 定义关系模型（Relation）
  - 定义任务模型（AnnotationTask、TaskStatus、AnnotationType）
  - 定义数据集模型（Dataset、CorpusRecord）
  - 定义标签配置模型（EntityTypeConfig、RelationTypeConfig、LabelSchema）
  - 定义复核模型（ReviewTask、ReviewStatus）
  - 定义版本模型（Version、ChangeType、VersionDiff）
  - 定义API请求响应模型
  - _Requirements: 所有需求的基础_

- [x] 4. Excel处理服务实现
  - 实现Excel文件验证功能（格式、必需列）
  - 实现WPS内嵌图片提取功能（解析cellimages.xml和rels）
  - 实现图片文件导出功能
  - 实现DISPIMG公式转Markdown格式功能
  - 实现文本分句功能（按句号、换行符、序号分割）
  - 实现语料记录生成功能（含元数据和字段分类）
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

- [ ]* 4.1 编写Excel处理属性测试
  - **Property 1: Excel文件验证完整性**
  - **Validates: Requirements 1.1**

- [ ]* 4.2 编写图片提取属性测试
  - **Property 2: 图片ID映射一致性**
  - **Property 3: 图片文件导出完整性**
  - **Validates: Requirements 1.2, 1.3**

- [ ]* 4.3 编写文本处理属性测试
  - **Property 4: DISPIMG转换正确性**
  - **Property 5: 文本分句一致性**
  - **Validates: Requirements 1.4, 1.5**

- [ ]* 4.4 编写语料生成属性测试
  - **Property 6: 语料记录元数据完整性**
  - **Property 7: 处理统计准确性**
  - **Validates: Requirements 1.6, 1.7, 1.8**


- [x] 5. 语料管理API实现









  - 实现POST /api/v1/corpus/upload接口（上传Excel文件）
  - 实现GET /api/v1/corpus接口（获取语料列表，支持分页和筛选）
  - 实现GET /api/v1/corpus/{id}接口（获取语料详情）
  - 实现DELETE /api/v1/corpus/{id}接口（删除语料）
  - 实现GET /api/v1/corpus/{id}/images接口（获取语料关联图片）
  - _Requirements: 1.8, 1.9_

- [ ]* 5.1 编写语料管理单元测试
  - 测试文件上传流程
  - 测试语料查询和筛选
  - 测试语料删除
  - _Requirements: 1.8, 1.9_

- [x] 6. 偏移量验证与修正服务实现



  - 实现偏移量验证功能（validate_offset）
  - 实现偏移量修正功能（correct_offset）
  - 实现最近匹配查找功能（find_closest_match）
  - 实现修正日志记录功能
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ]* 6.1 编写偏移量处理属性测试
  - **Property 18: 实体偏移量验证正确性**
  - **Property 44: 偏移量修正准确性**
  - **Property 45: 最近匹配选择正确性**
  - **Property 46: 偏移量修正日志记录完整性**
  - **Property 47: 无法修正实体标记正确性**
  - **Validates: Requirements 10.1, 10.2, 10.3, 10.4, 10.5**

- [x] 7. LangChain Agent配置和实体抽取Agent实现



  - 配置LangChain v1.0和LangGraph环境
  - 配置Qwen-Max模型连接（使用DashScope API）
  - 实现实体抽取Prompt模板
  - 实现实体抽取Agent（使用create_agent和ToolStrategy）
  - 实现实体抽取结构化输出模型（AgentEntityExtractionOutput）
  - 集成偏移量验证和修正功能
  - _Requirements: 4.2, 4.4_

- [ ]* 7.1 编写实体抽取Agent单元测试
  - 使用Mock测试Agent调用流程
  - 测试结构化输出解析
  - 测试偏移量验证集成
  - _Requirements: 4.2, 4.4_

- [ ]* 7.2 编写实体抽取属性测试
  - **Property 16: LLM实体抽取输出格式正确性**
  - **Validates: Requirements 4.2**

- [x] 8. 关系抽取Agent实现





  - 实现关系抽取Prompt模板
  - 实现关系抽取Agent（使用create_agent和ToolStrategy）
  - 实现关系抽取结构化输出模型（AgentRelationExtractionOutput）
  - 实现关系实体ID有效性验证
  - _Requirements: 4.5_

- [ ]* 8.1 编写关系抽取Agent单元测试
  - 使用Mock测试Agent调用流程
  - 测试关系ID验证
  - _Requirements: 4.5_

- [ ]* 8.2 编写关系抽取属性测试
  - **Property 19: 关系实体ID有效性**
  - **Validates: Requirements 4.5**

- [x] 9. 多模态图片标注Agent实现（可选简化版）



  - 实现图片分类Prompt模板
  - 实现多模态Agent（调用Qwen-VL或简化为单一标签）
  - 实现图片实体输出模型
  - _Requirements: 4.3_

- [ ]* 9.1 编写图片标注属性测试
  - **Property 17: 多模态标注输出格式正确性**
  - **Validates: Requirements 4.3**


- [x] 10. 数据集管理服务实现



  - 实现数据集创建功能（create_dataset）
  - 实现数据集查询功能（get_dataset、list_datasets）
  - 实现数据集删除功能（delete_dataset，级联删除）
  - 实现数据集导出功能（export_dataset，生成JSONL）
  - _Requirements: 2.2, 2.3, 2.4, 2.5, 2.6_

- [ ]* 10.1 编写数据集管理属性测试
  - **Property 8: 数据集任务创建一致性**
  - **Property 9: 数据集统计准确性**
  - **Property 10: 级联删除完整性**
  - **Property 11: 数据集导出格式正确性**
  - **Validates: Requirements 2.3, 2.4, 2.5, 2.6**

- [x] 11. 数据集管理API实现
  - 实现POST /api/v1/datasets接口（创建数据集）
  - 实现GET /api/v1/datasets接口（获取数据集列表）
  - 实现GET /api/v1/datasets/{id}接口（获取数据集详情）
  - 实现PUT /api/v1/datasets/{id}接口（更新数据集）
  - 实现DELETE /api/v1/datasets/{id}接口（删除数据集）
  - 实现POST /api/v1/datasets/{id}/export接口（导出数据集）
  - _Requirements: 2.2, 2.3, 2.4, 2.5, 2.6_

- [ ]* 11.1 编写数据集API单元测试
  - 测试数据集CRUD操作
  - 测试导出功能
  - _Requirements: 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 12. 标签体系管理服务实现



  - 实现实体类型CRUD功能
  - 实现关系类型CRUD功能
  - 实现标签体系导入导出功能（JSON格式）
  - 实现标签修改兼容性验证功能
  - 实现预置标签初始化功能（品质失效案例领域本体）
  - 实现标签定义生成功能（调用LLM生成详细定义）
  - 实现标签定义审核功能（人工审核和确认）
  - 实现动态Prompt生成功能（基于数据库标签配置）
  - 实现标签配置缓存机制（提升性能）
  - 实现标签体系版本管理功能（版本快照、切换、比较）
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [ ]* 12.1 编写标签管理属性测试
  - **Property 12: 标签配置序列化往返一致性**
  - **Property 13: 标签修改影响范围准确性**
  - **Property 14: 标签配置合并正确性**



  - **Validates: Requirements 3.1, 3.2, 3.3, 3.5, 3.6**

- [x] 13. 标签管理API实现


  - 实现GET /api/v1/labels/entities接口（获取实体类型列表）
  - 实现POST /api/v1/labels/entities接口（创建实体类型）
  - 实现PUT /api/v1/labels/entities/{id}接口（更新实体类型）
  - 实现DELETE /api/v1/labels/entities/{id}接口（删除实体类型）
  - 实现POST /api/v1/labels/entities/{id}/generate-definition接口（生成实体类型定义）
  - 实现POST /api/v1/labels/entities/{id}/review接口（审核实体类型定义）
  - 实现GET /api/v1/labels/relations接口（获取关系类型列表）
  - 实现POST /api/v1/labels/relations接口（创建关系类型）
  - 实现PUT /api/v1/labels/relations/{id}接口（更新关系类型）
  - 实现DELETE /api/v1/labels/relations/{id}接口（删除关系类型）
  - 实现POST /api/v1/labels/relations/{id}/generate-definition接口（生成关系类型定义）
  - 实现POST /api/v1/labels/relations/{id}/review接口（审核关系类型定义）
  - 实现POST /api/v1/labels/import接口（导入标签配置）
  - 实现GET /api/v1/labels/export接口（导出标签配置）
  - 实现GET /api/v1/labels/prompt-preview接口（预览Agent Prompt）
  - 实现GET /api/v1/labels/versions接口（获取版本列表）
  - 实现POST /api/v1/labels/versions/snapshot接口（创建版本快照）
  - 实现GET /api/v1/labels/versions/{version_id}接口（获取版本详情）
  - 实现POST /api/v1/labels/versions/{version_id}/activate接口（激活版本）
  - 实现GET /api/v1/labels/versions/compare接口（比较版本差异）
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ]* 13.1 编写标签API单元测试
  - 测试标签CRUD操作
  - 测试导入导出功能
  - _Requirements: 3.1, 3.2, 3.5, 3.6_

- [x] 14. 批量标注服务实现



  - 实现批量任务创建功能（create_batch_job）
  - 实现批量标注执行功能（使用异步任务队列）
  - 实现批量任务进度跟踪功能
  - 实现批量任务状态更新功能
  - 实现单个任务失败处理和错误记录
  - _Requirements: 4.1, 4.6, 4.7, 4.8_

- [ ]* 14.1 编写批量标注属性测试
  - **Property 15: 批量标注任务创建完整性**
  - **Property 20: 批量标注进度计算准确性**
  - **Property 21: 批量标注状态更新正确性**
  - **Property 22: 标注失败错误记录完整性**
  - **Validates: Requirements 4.1, 4.6, 4.7, 4.8**


- [x] 15. 标注任务API实现



  - 实现POST /api/v1/annotations/batch接口（批量自动标注）
  - 实现GET /api/v1/annotations/{task_id}接口（获取标注任务详情）
  - 实现PUT /api/v1/annotations/{task_id}接口（更新标注任务）
  - 实现POST /api/v1/annotations/{task_id}/entities接口（添加文本实体）
  - 实现PUT /api/v1/annotations/{task_id}/entities/{id}接口（更新文本实体）
  - 实现DELETE /api/v1/annotations/{task_id}/entities/{id}接口（删除文本实体）
  - 实现POST /api/v1/annotations/{task_id}/relations接口（添加关系）
  - 实现PUT /api/v1/annotations/{task_id}/relations/{id}接口（更新关系）
  - 实现DELETE /api/v1/annotations/{task_id}/relations/{id}接口（删除关系）
  - _Requirements: 4.1, 4.2, 4.5, 5.2, 5.6_

- [ ]* 15.1 编写标注API单元测试
  - 测试批量标注触发
  - 测试实体CRUD操作
  - 测试关系CRUD操作
  - _Requirements: 4.1, 5.2, 5.6_

- [ ]* 15.2 编写实体关系操作属性测试
  - **Property 23: 文本选择偏移量计算正确性**
  - **Property 24: 关系创建有向性正确性**
  - **Validates: Requirements 5.2, 5.6**

- [x] 16. 图片标注API实现
  - 实现POST /api/v1/images/{image_id}/entities接口（添加图片实体）
  - 实现GET /api/v1/images/{image_id}/entities接口（获取图片实体列表）
  - 实现PUT /api/v1/images/{image_id}/entities/{id}接口（更新图片实体）
  - 实现DELETE /api/v1/images/{image_id}/entities/{id}接口（删除图片实体）
  - _Requirements: 5.4, 5.5, 12.3, 12.5, 12.6, 12.7_

- [ ]* 16.1 编写图片标注单元测试
  - 测试整图标注
  - 测试区域标注（边界框）
  - _Requirements: 5.4, 5.5_

- [ ]* 16.2 编写图片坐标变换属性测试
  - **Property 53: 图片坐标变换不变性**
  - **Validates: Requirements 12.8**

- [x] 17. 版本管理服务实现
  - 实现版本创建功能（create_version）
  - 实现版本历史查询功能（get_version_history）
  - 实现版本回滚功能（rollback_to_version）
  - 实现版本比较功能（compare_versions）
  - 实现版本快照存储（JSON格式）
  - _Requirements: 5.7, 5.8_

- [ ]* 17.1 编写版本管理属性测试
  - **Property 25: 版本历史递增性**
  - **Property 26: 版本回滚一致性**
  - **Validates: Requirements 5.7, 5.8**

- [x] 18. 版本管理API实现
  - 实现GET /api/v1/versions/{task_id}接口（获取版本历史）
  - 实现POST /api/v1/versions/{task_id}/rollback接口（回滚版本）
  - 实现GET /api/v1/versions/compare接口（比较版本差异）
  - _Requirements: 5.7, 5.8_

- [ ]* 18.1 编写版本API单元测试
  - 测试版本历史查询
  - 测试版本回滚
  - 测试版本比较
  - _Requirements: 5.7, 5.8_

- [x] 19. 复核服务实现
  - 实现复核任务创建功能（submit_for_review）
  - 实现复核任务查询功能（get_review_tasks）
  - 实现复核批准功能（approve_task）
  - 实现复核驳回功能（reject_task）
  - 实现复核修改差异记录功能
  - 实现质量统计计算功能
  - _Requirements: 6.1, 6.3, 6.4, 6.6, 6.7_

- [ ]* 19.1 编写复核服务属性测试
  - **Property 27: 复核任务创建正确性**
  - **Property 28: 复核批准状态更新正确性**
  - **Property 29: 复核驳回状态更新正确性**
  - **Property 30: 复核修改差异记录完整性**
  - **Property 31: 质量统计计算准确性**
  - **Validates: Requirements 6.1, 6.3, 6.4, 6.6, 6.7**


- [x] 20. 复核API实现
  - 实现POST /api/v1/review/submit/{task_id}接口（提交复核）
  - 实现GET /api/v1/review/tasks接口（获取复核任务列表）
  - 实现GET /api/v1/review/{review_id}接口（获取复核任务详情）
  - 实现POST /api/v1/review/{review_id}/approve接口（批准任务）
  - 实现POST /api/v1/review/{review_id}/reject接口（驳回任务）
  - 实现GET /api/v1/review/dataset/{dataset_id}/statistics接口（获取数据集质量统计）
  - 实现GET /api/v1/review/dataset/{dataset_id}/summary接口（获取数据集复核摘要）
  - _Requirements: 6.1, 6.3, 6.4_

- [ ]* 20.1 编写复核API单元测试
  - 测试复核提交
  - 测试复核批准和驳回
  - _Requirements: 6.1, 6.3, 6.4_

- [x] 21. 数据导出服务实现
  - 实现标注数据导出功能（按状态筛选）
  - 实现JSONL格式生成功能
  - 实现训练集/测试集划分功能
  - 实现按句子分类筛选导出功能
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 21.1 编写数据导出属性测试
  - **Property 32: 导出数据状态筛选正确性**
  - **Property 33: 导出数据格式完整性**
  - **Property 34: JSONL格式有效性**
  - **Property 35: 数据集划分比例准确性**
  - **Property 36: 句子分类筛选正确性**
  - **Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5**

- [x] 22. Reward数据集生成服务实现



  - 实现人工修正任务筛选功能
  - 实现标注差异计算功能
  - 实现Reward数据集JSONL生成功能
  - 实现修正频率统计功能
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ]* 22.1 编写Reward数据集属性测试
  - **Property 37: Reward数据集筛选正确性**
  - **Property 38: 标注差异计算准确性**
  - **Property 39: Reward数据格式完整性**
  - **Property 40: 修正频率统计准确性**
  - **Validates: Requirements 8.1, 8.2, 8.3, 8.4**

- [x] 23. 用户管理服务实现
  - 实现用户创建功能（密码加密）
  - 实现用户查询功能
  - 实现用户更新功能
  - 实现用户删除功能
  - 实现JWT Token生成和验证
  - 实现基于角色的权限检查
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 23.1 编写用户管理属性测试
  - **Property 41: 用户角色分配正确性**
  - **Property 42: 权限检查正确性**
  - **Property 43: 复核人员分配有效性**
  - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**

- [x] 24. 用户管理和认证API实现
  - 实现POST /api/v1/users接口（创建用户）
  - 实现GET /api/v1/users接口（获取用户列表）
  - 实现PUT /api/v1/users/{id}接口（更新用户）
  - 实现DELETE /api/v1/users/{id}接口（删除用户）
  - 实现POST /api/v1/auth/login接口（用户登录）
  - 实现POST /api/v1/auth/logout接口（用户登出）
  - 实现JWT认证中间件
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ]* 24.1 编写用户API单元测试
  - 测试用户CRUD操作
  - 测试登录登出
  - 测试JWT认证
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 25. 数据序列化服务实现




  - 实现文本实体序列化/反序列化
  - 实现整图实体序列化/反序列化
  - 实现区域实体序列化/反序列化
  - 实现关系序列化/反序列化
  - 实现标注任务完整序列化/反序列化
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7_

- [ ]* 25.1 编写序列化属性测试
  - **Property 48: 标注数据序列化往返一致性**
  - **Property 49: 文本实体序列化格式正确性**
  - **Property 50: 整图实体序列化格式正确性**
  - **Property 51: 区域实体序列化格式正确性**
  - **Property 52: 关系序列化格式正确性**
  - **Validates: Requirements 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7**


- [x] 26. 后端集成测试和错误处理完善



  - 编写API集成测试（端到端流程测试）
  - 实现统一错误处理中间件
  - 实现日志记录系统
  - 实现错误响应格式标准化
  - 测试并发场景和事务处理
  - _Requirements: 所有需求_

- [ ]* 26.1 编写后端集成测试
  - 测试完整的标注流程（上传→标注→复核→导出）
  - 测试错误场景和边界情况
  - _Requirements: 所有需求_

- [x] 27. 前端项目初始化和路由配置
  - 创建Vue3项目结构
  - 配置Vue Router（页面路由）
  - 配置Pinia状态管理
  - 配置Axios（API请求封装）
  - 配置Element Plus UI组件库
  - 配置TypeScript类型定义
  - _Requirements: 所有需求的基础_
  - _完成日期: 2025-01-24_
  - _状态: ✅ 已完成_

- [x] 28. 前端API服务层实现
  - 实现语料管理API封装
  - 实现数据集管理API封装
  - 实现标注任务API封装
  - 实现图片标注API封装
  - 实现标签管理API封装
  - 实现复核API封装
  - 实现用户管理API封装
  - 实现统一错误处理
  - _Requirements: 所有需求的基础_
  - _完成日期: 2025-01-24_
  - _状态: ✅ 已完成 (frontend/src/api/)_

- [x] 29. 前端状态管理实现
  - 实现语料管理Store（Pinia）
  - 实现数据集管理Store
  - 实现标注任务Store
  - 实现标签配置Store
  - 实现用户认证Store
  - _Requirements: 所有需求的基础_
  - _完成日期: 2025-01-24_
  - _状态: ✅ 已完成 (frontend/src/stores/)_

- [x] 30. Excel导入页面实现
  - 实现文件上传组件（FileUploader）
  - 实现处理进度显示组件（ProcessingProgress）
  - 实现语料预览列表组件（CorpusPreview）
  - 实现按字段分类筛选功能
  - 实现图片缩略图显示
  - _Requirements: 1.8, 1.9_
  - _完成日期: 2025-01-24_
  - _状态: ✅ 已完成 (CorpusManagement.vue)_

- [x] 31. 数据集管理页面实现



  - 实现数据集列表组件（DatasetList）
  - 实现数据集卡片组件（DatasetCard）
  - 实现创建数据集对话框（DatasetCreateDialog）
  - 实现语料选择器组件（CorpusSelector）
  - 实现数据集统计显示
  - _Requirements: 2.1, 2.2, 2.4_

- [x] 32. 标签配置页面实现
  - 实现实体类型配置组件（EntityTypeConfig）
  - 实现关系类型配置组件（RelationTypeConfig）
  - 实现标签定义生成组件（DefinitionGenerator）
  - 实现标签定义审核组件（DefinitionReview）
  - 实现标签导入导出组件（LabelImportExport）
  - 实现Agent Prompt预览组件（PromptPreview）
  - 实现标签体系版本管理组件（VersionManager）
  - 实现版本快照创建对话框（VersionSnapshotDialog）
  - 实现版本比较组件（VersionCompare）
  - 实现标签颜色选择器
  - 实现审核状态标识（待审核/已审核）
  - _Requirements: 3.1, 3.2, 3.5, 3.6_
  - _完成日期: 2025-01-24_
  - _状态: ✅ 已完成 (LabelManagement.vue, LabelConfig.vue)_

- [x] 33. 文本标注编辑器核心组件实现



  - 实现文本显示和选择功能（use-enhanced-text-selection）
  - 实现实体高亮显示组件（EntityHighlight）
  - 实现标签选择菜单组件（LabelSelector）
  - 实现实体列表面板（EntityList）
  - 实现关系列表面板（RelationList）
  - 实现偏移量计算和验证
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 34. 关系标注可视化组件实现



  - 实现SVG关系箭头层组件（RelationArrowLayer）
  - 实现关系创建交互（点击两个实体）
  - 实现关系编辑和删除功能
  - 实现箭头自动布局算法
  - _Requirements: 5.6_


- [x] 35. 图片标注编辑器组件实现


  - 实现图片查看器组件（ImageViewer）
  - 实现整图标注功能（点击图片选择标签）
  - 实现区域标注功能（拖拽绘制边界框）
  - 实现边界框编辑和删除功能
  - 实现图片缩放和平移功能
  - 实现坐标变换保持功能
  - _Requirements: 5.4, 5.5, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8_

- [x] 36. 标注编辑页面集成



  - 集成文本标注编辑器和图片标注编辑器
  - 实现标注模式切换（实体模式/关系模式）
  - 实现版本历史显示和回滚功能
  - 实现保存和提交复核功能
  - 实现快捷键支持
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_

- [x] 37. 批量标注功能实现
  - 实现批量标注触发按钮
  - 实现批量任务进度显示（实时更新）
  - 实现批量任务取消功能
  - 实现批量任务结果查看
  - _Requirements: 4.1, 4.6, 4.7_

- [x] 38. 复核页面实现



  - 实现复核任务列表组件（ReviewTaskList）
  - 实现标注结果查看器（只读模式）
  - 实现复核操作面板（批准/驳回/修改）
  - 实现复核意见输入
  - 实现LLM纠正建议功能
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [ ] 39. 数据导出功能实现 (暂时跳过)
  - 实现导出配置对话框（状态筛选、格式选择）
  - 实现训练集/测试集划分配置
  - 实现按句子分类筛选
  - 实现导出进度显示
  - 实现文件下载功能
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  - _状态: ⏸️ 暂时跳过_

- [ ] 40. Reward数据集生成功能实现 (暂时跳过)
  - 实现Reward数据集生成按钮
  - 实现修正统计显示
  - 实现Reward数据预览
  - 实现Reward数据导出
  - _Requirements: 8.1, 8.2, 8.3, 8.4_
  - _状态: ⏸️ 暂时跳过_

- [x] 41. 用户管理页面实现
  - 实现用户列表组件
  - 实现用户创建对话框
  - 实现用户编辑和删除功能
  - 实现角色分配功能
  - _Requirements: 9.1, 9.5_
  - _完成日期: 2025-01-23_
  - _完成报告: USER_MANAGEMENT_COMPLETE.md_

- [x] 42. 登录和认证功能实现
  - 实现登录页面
  - 实现JWT Token存储和管理
  - 实现路由守卫（权限检查）
  - 实现自动登出（Token过期）
  - _Requirements: 9.2, 9.3, 9.4_
  - _完成日期: 2025-01-24_
  - _状态: ✅ 已完成 (Login.vue, auth.ts, router guards)_

- [x] 43. 前端UI优化和响应式设计
  - 实现响应式布局（适配不同屏幕尺寸）
  - 实现加载状态和骨架屏
  - 实现错误提示和成功提示
  - 实现确认对话框（删除等危险操作）
  - 优化交互体验（防抖、节流）
  - _Requirements: 所有需求_
  - _完成日期: 2025-01-24_
  - _状态: ✅ 已完成 (包含43.1数据集状态指示器)_

- [x] 43.1 数据集状态指示器功能
  - **背景**: 所有用户(包括浏览员)都能看到所有数据集,需要添加状态指示器提升用户体验
  - **目标**: 让用户清楚了解数据集完成状态,防止对空数据集进行无效操作
  - **实施内容**:
    - 在数据集卡片上添加状态标签(空/进行中/已完成)
    - 对于空数据集,禁用导出按钮并显示提示
    - 添加状态筛选器(全部/进行中/已完成)
    - 保持当前"查看全部"行为,不隐藏未完成的数据集
  - **状态定义**:
    - 空: `total_tasks === 0`
    - 进行中: `total_tasks > 0 && completed_tasks < total_tasks`
    - 已完成: `total_tasks > 0 && completed_tasks === total_tasks`
  - **修改文件**:
    - `frontend/src/types/index.ts` - 添加 DatasetStatus 类型
    - `frontend/src/components/dataset/DatasetCard.vue` - 状态标签和导出控制
    - `frontend/src/views/dataset/DatasetManagement.vue` - 状态筛选器
  - **参考文档**:
    - 实施计划: `DATASET_STATUS_INDICATORS_PLAN.md`
    - 完成报告: `DATASET_STATUS_INDICATORS_COMPLETE.md`
  - _完成日期: 2025-01-24_
  - _Requirements: 用户体验优化_

- [ ]* 43.2 编写前端组件单元测试
  - 测试核心组件功能
  - 测试用户交互
  - _Requirements: 所有需求_
  - _状态: 延后到 Task 47 之后_

---

## 🔄 任务顺序调整说明

**原计划**: Task 44 (测试) → Task 45 (文档) → Task 46 (检查点) → Task 47 (架构优化)

**调整后**: Task 47 (架构优化) → Task 44 (测试) → Task 45 (文档) → Task 46 (检查点)

**调整原因**:
1. Task 47 数据集分配功能是实际使用的核心需求
2. 架构调整后再测试，避免重复工作
3. 在完整架构下测试更有价值

---

- [x] 47. 数据集级别任务分配功能（架构优化）✅ **已完成**
  - **优先级**：P0（核心功能，优先实施）
  - **背景**：当前系统任务是针对单条语料，实际使用中应按数据集组织和分配
  - **目标**：实现数据集级别的分配机制，不同角色有不同权限
  - **完成日期**: 2026-01-24
  - **完成文档**：
    - 功能完整文档：`docs/TASK47_FINAL.md`
    - 角色设计说明：`docs/TASK47_ROLE_CLARIFICATION.md`
    - API测试报告：`docs/TASK47_API_TEST_REPORT.md` (11/11 通过)
  - **实施内容**：
    - ✅ 新增 DatasetAssignment 表实现数据集分配
    - ✅ 实现三种分配模式（整体/范围/自动）
    - ✅ 实现分配管理（取消/转移）
    - ✅ 前端添加"我的数据集"页面
    - ✅ 前端添加"分配管理"页面
    - ✅ 实现权限控制和路由守卫
    - ✅ 后端API完整实现（6个端点）
    - ✅ 服务层完整实现（15个方法）
  - **测试结果**：
    - 后端API测试：11/11 全部通过（100%）
    - 数据库表已创建并有实际数据
    - 前端页面和路由已实现
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5（用户管理和权限）_

- [ ] 44. 系统集成测试和端到端测试（混合测试策略）
  - **测试策略**: 采用"手动测试 + 自动化测试"混合方案
  - **阶段1: 手动测试 + 测试清单**（Task 44.1）
    - 创建基于角色的测试清单
    - 手动验证关键用户流程
    - 记录测试结果和问题
  - **阶段2: Playwright E2E 自动化测试**（Task 44.2）
    - 搭建 Playwright 测试框架
    - 实现关键路径自动化测试
    - 配置多环境支持（开发/生产）
  - **阶段3: 性能和压力测试**（Task 44.3）
    - 大文件上传测试
    - 大数据集处理测试
    - 并发用户测试
  - _Requirements: 所有需求_
  - _参考文档: `docs/TESTING_STRATEGY.md`_

- [ ] 44.1 创建测试清单并执行手动测试
  - **目标**: 验证 Task 47 实施后的完整功能
  - **测试清单内容**:
    - 管理员流程测试（创建数据集、分配任务、查看统计）
    - 标注员流程测试（查看分配、标注任务、提交复核）
    - 浏览员流程测试（查看数据集、导出数据）
    - 复核员流程测试（复核任务、批准/驳回）
    - 权限控制测试（越权访问、角色切换）
    - 边界情况测试（空数据、大数据、并发操作）
    - 错误处理测试（网络错误、服务器错误、验证错误）
  - **输出**:
    - 测试清单文档（`docs/MANUAL_TEST_CHECKLIST.md`）
    - 测试结果报告（`docs/MANUAL_TEST_RESULTS.md`）
    - 发现的问题列表（`docs/ISSUES_FOUND.md`）
  - _预计时间: 2-3 天_
  - _Requirements: 所有需求_

- [ ] 44.2 搭建 Playwright E2E 测试框架
  - **目标**: 自动化关键用户流程测试
  - **实施内容**:
    - 安装和配置 Playwright
    - 配置多浏览器测试（Chrome, Firefox, Safari）
    - 配置环境变量支持（baseURL, 测试账号）
    - 实现 Page Object Model 模式
    - 编写关键路径测试用例:
      - 登录认证流程
      - 数据集创建和分配流程
      - 标注任务流程
      - 复核流程
      - 数据导出流程
    - 配置 CI/CD 集成（可选）
  - **技术要点**:
    - 使用相对路径而非绝对URL（支持不同部署环境）
    - 使用 data-testid 属性定位元素（提高稳定性）
    - 实现自动等待和重试机制
    - 配置截图和视频录制（失败时）
  - **输出**:
    - Playwright 配置文件（`playwright.config.ts`）
    - Page Object 类（`tests/pages/`）
    - 测试用例（`tests/e2e/`）
    - 测试文档（`docs/E2E_TESTING_GUIDE.md`）
  - _预计时间: 3-4 天_
  - _Requirements: 所有需求_

- [ ] 44.3 性能和压力测试
  - 大文件上传测试（>10MB Excel文件）
  - 大数据集处理测试（>1000条语料）
  - 并发用户测试（多用户同时操作）
  - 数据库性能测试（查询优化）
  - 前端渲染性能测试（大列表、复杂组件）
  - _预计时间: 2-3 天_
  - _Requirements: 所有需求_

- [ ] 45. 文档编写和部署准备
  - 编写README.md（项目介绍、安装、使用）
  - 编写API文档（Swagger/OpenAPI）
  - 编写用户手册（`docs/USER_MANUAL.md`）
  - 编写开发者文档（`docs/DEVELOPER_GUIDE.md`）
  - 编写部署文档（`docs/DEPLOYMENT_GUIDE.md`）
  - 准备Docker部署配置（`Dockerfile`, `docker-compose.yml`）
  - 准备生产环境配置（`.env.production`）
  - _预计时间: 3-4 天_
  - _Requirements: 所有需求_

- [ ] 46. 最终检查点 - 确保所有测试通过
  - 运行所有自动化测试
  - 执行最终手动回归测试
  - 检查文档完整性
  - 确认部署配置正确
  - 询问用户是否有问题
  - 准备发布清单
  - _预计时间: 1-2 天_
  - _Requirements: 所有需求_

---

## 未来优化任务

以下任务为系统增强功能，在完成核心功能和测试后根据需要实施：

- [ ] 48. 批量标注优化
  - **优先级**：P2
  - **目标**：提升LLM标注准确率和用户体验
  - **实施内容**：
    - 优化 Agent Prompt 模板
    - 添加批量标注进度实时显示
    - 实现批量标注任务暂停/恢复功能
    - 添加标注质量评估指标
  - _预计时间: 3-5 天_

- [ ] 49. 数据导出功能增强（Task 39 扩展）
  - **优先级**：P2
  - **目标**：支持更多导出格式和配置选项
  - **实施内容**：
    - 支持多种格式（JSON, CSV, Excel, JSONL）
    - 实现训练集/测试集自动划分
    - 实现按句子分类筛选导出
    - 添加导出模板自定义功能
  - _预计时间: 2-3 天_

- [ ] 50. Reward数据集生成功能（Task 40 扩展）
  - **优先级**：P3
  - **目标**：生成用于模型训练的Reward数据集
  - **实施内容**：
    - 实现人工修正任务筛选
    - 实现标注差异计算
    - 实现Reward数据集JSONL生成
    - 实现修正频率统计
  - _预计时间: 2-3 天_

- [ ] 51. 统计分析功能
  - **优先级**：P2
  - **目标**：提供数据洞察和质量监控
  - **实施内容**：
    - 标注质量统计（准确率、一致性）
    - 用户工作量统计（标注数量、时间）
    - 数据集完成度分析（进度、瓶颈）
    - 实体/关系分布统计
    - 可视化图表展示
  - _预计时间: 4-5 天_

- [ ] 52. UI/UX 增强
  - **优先级**：P3
  - **目标**：提升用户体验
  - **实施内容**：
    - 深色模式支持
    - 快捷键支持（标注、导航）
    - 批量操作（批量删除、批量分配）
    - 拖拽排序和组织
    - 自定义主题配置
  - _预计时间: 3-4 天_

- [ ] 53. 性能优化
  - **优先级**：P2
  - **目标**：提升系统性能和响应速度
  - **实施内容**：
    - 数据库查询优化（索引、缓存）
    - 前端虚拟滚动（大列表）
    - 图片懒加载和压缩
    - API 响应缓存
    - WebSocket 实时更新
  - _预计时间: 3-5 天_

- [ ] 54. 协作功能增强
  - **优先级**：P3
  - **目标**：提升多用户协作体验
  - **实施内容**：
    - 实时协作提示（谁在编辑）
    - 任务锁定机制（防止冲突）
    - 评论和讨论功能
    - 通知系统（任务分配、复核结果）
  - _预计时间: 4-6 天_

