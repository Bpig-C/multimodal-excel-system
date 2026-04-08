# Implementation Plan

## Overview
本实施计划专注于增强现有系统，添加基于角色的任务列表权限控制。主要工作包括：
1. 增强现有的数据集任务列表API（`backend/api/dataset.py`）
2. 新增跨数据集任务列表API（`backend/api/annotations.py`）
3. 创建任务查询服务（复用现有的 `DatasetAssignmentService`）
4. 创建前端任务列表页面（`frontend/src/views/annotation/AnnotationList.vue`）

## Tasks

- [x] 1. 创建任务查询服务层





  - 创建 `backend/services/task_query_service.py`
  - 实现基于角色的任务查询逻辑
  - 复用 `DatasetAssignmentService` 的权限检查方法
  - _Requirements: 4.1, 4.2, 4.3, 6.1, 6.2, 6.3, 6.4_

- [x] 1.1 实现 TaskQueryService 核心方法


  - 实现 `get_user_tasks()` 方法（跨数据集查询）
  - 实现 `check_task_permission()` 方法（单任务权限检查）
  - 实现 `_build_task_query()` 私有方法（构建查询）
  - 实现 `_apply_permission_filter()` 私有方法（应用权限过滤）
  - _Requirements: 2.1, 2.2, 5.1, 5.2, 5.3_

- [x]* 1.2 编写 TaskQueryService 单元测试







  - 测试管理员获取所有任务
  - 测试标注员获取分配的任务
  - 测试任务范围过滤
  - 测试浏览员获取已完成任务
  - _Requirements: 1.1, 2.1, 3.2_

- [x] 2. 增强现有数据集任务列表API





  - 修改 `backend/api/dataset.py` 中的 `get_dataset_tasks()` 函数
  - 添加权限过滤逻辑（调用 TaskQueryService）
  - 保持响应格式不变（向后兼容）
  - _Requirements: 5.1, 5.2, 5.3, 11.1, 11.2, 11.3_

- [x] 2.1 添加权限过滤到 get_dataset_tasks


  - 获取当前用户信息
  - 根据用户角色调用 TaskQueryService
  - 管理员：返回所有任务
  - 标注员：返回分配的任务
  - 浏览员：返回已完成任务
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 2.2 编写向后兼容性测试






  - 测试管理员行为与修改前一致
  - 测试响应格式不变
  - 测试分页和筛选功能正常
  - _Requirements: 11.1, 11.3_

- [x] 3. 新增跨数据集任务列表API






  - 在 `backend/api/annotations.py` 添加 `GET /api/v1/annotations` 端点
  - 实现分页、筛选、排序功能
  - 集成 TaskQueryService
  - _Requirements: 4.1, 4.4, 4.5, 10.1, 10.2, 10.3_

- [x] 3.1 实现 GET /api/v1/annotations 端点


  - 定义请求参数（dataset_id, status, page, page_size, sort_by, sort_order）
  - 调用 TaskQueryService.get_user_tasks()
  - 构建响应数据（包含数据集名称、语料预览等）
  - 返回分页信息
  - _Requirements: 1.1, 1.2, 2.1, 4.1, 4.5_

- [x] 3.2 实现筛选和排序功能


  - 支持按 dataset_id 筛选
  - 支持按 status 筛选
  - 支持按 created_at, updated_at, status 排序
  - _Requirements: 1.4, 2.6, 8.2, 10.3_

- [x]* 3.3 编写 API 集成测试




  - 测试管理员获取所有任务
  - 测试标注员获取分配的任务
  - 测试筛选功能
  - 测试分页功能
  - 测试排序功能
  - _Requirements: 1.1, 1.4, 1.5, 2.1, 2.6_

- [x] 4. 增强任务详情和编辑API的权限检查






  - 修改 `backend/api/annotations.py` 中的 `get_annotation_task()` 函数
  - 修改 `backend/api/annotations.py` 中的 `update_annotation_task()` 函数
  - 添加权限检查逻辑
  - _Requirements: 2.4, 2.5, 3.3, 3.4, 6.5_

- [x] 4.1 添加权限检查到 get_annotation_task


  - 调用 TaskQueryService.check_task_permission()
  - 管理员：允许访问所有任务
  - 标注员：只允许访问分配的任务
  - 浏览员：只允许访问已完成任务
  - 权限不足返回403错误
  - _Requirements: 2.4, 2.5, 3.3, 6.5_

- [x] 4.2 添加权限检查到 update_annotation_task



  - 调用 TaskQueryService.check_task_permission()
  - 管理员：允许编辑所有任务
  - 标注员：只允许编辑分配的任务
  - 浏览员：禁止编辑（返回403）
  - _Requirements: 3.4, 6.5_

- [x] 4.3 编写权限检查测试







  - 测试标注员访问未分配任务返回403
  - 测试浏览员编辑任务返回403
  - 测试浏览员访问未完成任务返回403
  - _Requirements: 2.5, 3.4, 6.5_

- [x] 5. 创建前端任务列表页面





  - 实现 `frontend/src/views/annotation/AnnotationList.vue` 组件
  - 显示任务列表
  - 实现筛选UI
  - 实现分页UI
  - _Requirements: 1.1, 1.2, 1.4, 1.5, 2.1, 7.1, 7.2, 7.4_

- [x] 5.1 实现任务列表展示


  - 创建任务列表表格组件
  - 显示任务ID、数据集名称、语料预览、状态、创建时间
  - 使用不同颜色标识任务状态
  - 实现空状态提示
  - _Requirements: 1.2, 7.1, 7.4_

- [x] 5.2 实现筛选功能UI

  - 添加数据集筛选下拉框
  - 添加状态筛选下拉框
  - 实现筛选逻辑
  - 支持清除筛选
  - _Requirements: 1.4, 2.6, 8.2, 8.4_

- [x] 5.3 实现分页功能UI

  - 添加分页组件
  - 实现页码切换
  - 显示总数和当前页信息
  - _Requirements: 1.5, 4.4, 4.5_

- [x] 5.4 集成API调用


  - 创建 API 服务函数（`frontend/src/api/annotations.ts`）
  - 实现数据加载逻辑
  - 实现错误处理
  - 实现加载状态
  - _Requirements: 4.1, 6.5, 7.5_

- [x] 6. 实现导航集成
  - 修改"我的数据集"页面的"开始标注"按钮
  - 传递 dataset_id 参数到任务列表页面
  - 实现面包屑导航
  - _Requirements: 8.1, 8.2, 8.3, 8.5_

- [x] 6.1 修改"我的数据集"页面导航
  - 修改 `frontend/src/views/dataset/MyDatasets.vue`
  - 更新 `goToAnnotation()` 方法，传递 dataset_id 参数
  - _Requirements: 8.1_

- [x] 6.2 实现任务列表页面的数据集筛选
  - 从 URL 参数读取 dataset_id
  - 自动应用数据集筛选
  - 在页面标题显示数据集名称
  - _Requirements: 8.2, 8.3, 8.5_

- [x] 7. 添加数据库索引优化查询性能



  - 在 `annotation_tasks` 表添加复合索引
  - 创建数据库迁移脚本
  - _Requirements: 4.2, 4.3_

- [x] 7.1 创建数据库索引



  - 创建 `backend/migrations/add_task_query_indexes.sql`
  - 添加 `idx_annotation_tasks_dataset_status` 索引
  - 添加 `idx_annotation_tasks_created_at` 索引
  - _Requirements: 4.2_

- [ ] 8. 端到端测试和验证
  - 测试管理员工作流
  - 测试标注员工作流
  - 测试浏览员工作流
  - 验证向后兼容性
  - _Requirements: 所有需求_

- [x] 8.1 测试管理员工作流


  - 登录为管理员
  - 访问任务列表页面
  - 验证可以看到所有任务
  - 验证可以筛选和排序
  - 验证可以访问和编辑任何任务
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 8.2 测试标注员工作流
  - 登录为标注员
  - 从"我的数据集"点击"开始标注"
  - 验证只看到分配的任务
  - 验证任务范围过滤正确
  - 验证可以访问和编辑分配的任务
  - 验证无法访问未分配的任务（403错误）
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 8.1, 8.2, 8.3_

- [ ] 8.3 测试浏览员工作流
  - 登录为浏览员
  - 访问数据集页面
  - 验证只看到已完成的任务
  - 验证可以查看任务详情
  - 验证无法编辑任务（403错误）
  - 验证访问任务列表页面被重定向
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 8.4 验证向后兼容性
  - 测试管理员在数据集详情页的行为与修改前一致
  - 测试API响应格式不变
  - 测试现有功能不受影响
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 9. 文档更新
  - 更新API文档
  - 更新用户手册
  - 添加代码注释
  - _Requirements: 所有需求_

- [ ] 9.1 更新API文档
  - 文档化新的 `GET /api/v1/annotations` 端点
  - 文档化增强的 `GET /api/v1/datasets/{id}/tasks` 端点
  - 文档化权限规则
  - 文档化错误响应格式
  - _Requirements: 4.1, 5.1, 6.5_

- [ ] 9.2 更新用户手册
  - 添加任务列表页面使用说明
  - 添加权限说明
  - 添加常见问题解答
  - _Requirements: 所有需求_
