# Requirements Document

## Introduction

本文档定义了基于角色的任务列表权限控制功能的需求。该功能将创建新的标注任务列表页面（`/annotations`），作为管理员和标注员的工作台，提供跨数据集的任务视图。同时增强现有的数据集任务列表API（`GET /api/v1/datasets/{dataset_id}/tasks`），添加基于角色和分配的权限过滤。浏览员将通过数据集页面查看已完成的标注结果，而不使用任务列表页面。

## Glossary

- **System**: 实体关系标注系统（Entity-Relation Annotation System）
- **AnnotationTask**: 标注任务，包含待标注的语料和标注结果
- **DatasetAssignment**: 数据集分配记录，定义用户对数据集的访问权限和任务范围
- **Admin**: 管理员角色，拥有系统所有权限
- **Annotator**: 标注员角色，负责执行标注任务
- **Viewer**: 浏览员角色，通过数据集页面查看已完成的标注结果
- **TaskRange**: 任务范围，由起始索引和结束索引定义的任务子集
- **TaskList**: 任务列表，显示在 `/annotations` 页面的跨数据集任务集合
- **TaskFilter**: 任务过滤器，根据用户权限筛选任务的逻辑组件
- **WorkBench**: 工作台，标注员和管理员用于查看和处理任务的主要界面

## Requirements

### Requirement 1

**User Story:** 作为管理员，我希望在任务列表页面看到所有标注任务（跨数据集），以便我可以监控和管理整个系统的标注进度。

#### Acceptance Criteria

1. WHEN 管理员访问任务列表页面 THEN THE System SHALL 显示所有数据集的所有标注任务
2. WHEN 管理员查看任务列表 THEN THE System SHALL 显示每个任务的完整信息（任务ID、数据集名称、语料内容预览、状态、分配信息、创建时间）
3. WHEN 管理员点击任务 THEN THE System SHALL 允许管理员查看和编辑该任务的标注内容
4. WHEN 管理员在任务列表中筛选 THEN THE System SHALL 支持按数据集、状态、分配用户进行筛选
5. WHEN 任务列表包含超过20条记录 THEN THE System SHALL 支持分页显示

### Requirement 2

**User Story:** 作为标注员，我希望在任务列表页面只看到分配给我的任务（跨数据集），以便我可以专注于完成自己的工作。

#### Acceptance Criteria

1. WHEN 标注员访问任务列表页面 THEN THE System SHALL 只显示分配给该标注员的标注任务
2. WHEN 标注员查看任务列表 THEN THE System SHALL 根据数据集分配记录的任务范围过滤任务
3. WHEN 标注员的分配范围为任务1-50 THEN THE System SHALL 只显示该数据集的第1到第50个任务
4. WHEN 标注员点击任务 THEN THE System SHALL 允许标注员查看和编辑该任务的标注内容
5. WHEN 标注员尝试访问未分配给他的任务 THEN THE System SHALL 返回403权限错误
6. WHEN 标注员在任务列表中筛选 THEN THE System SHALL 支持按数据集、状态进行筛选

### Requirement 3

**User Story:** 作为浏览员，我希望通过数据集页面查看已完成的标注结果，以便我可以浏览和分析标注数据。

#### Acceptance Criteria

1. WHEN 浏览员访问数据集列表页面 THEN THE System SHALL 显示所有包含已完成任务的数据集
2. WHEN 浏览员点击数据集 THEN THE System SHALL 显示该数据集的任务列表（只包含已完成的任务）
3. WHEN 浏览员点击任务 THEN THE System SHALL 允许浏览员查看该任务的标注内容但不能编辑
4. WHEN 浏览员尝试编辑任务 THEN THE System SHALL 禁用所有编辑操作并显示只读提示
5. WHEN 浏览员访问任务列表页面（/annotations）THEN THE System SHALL 重定向到数据集列表页面

### Requirement 4

**User Story:** 作为系统，我需要提供高效的跨数据集任务查询API，以便前端可以快速加载和显示任务列表。

#### Acceptance Criteria

1. WHEN 前端请求任务列表 THEN THE System SHALL 根据当前用户的角色和权限返回相应的任务集合
2. WHEN API接收到任务列表请求 THEN THE System SHALL 在数据库层面进行权限过滤而不是在应用层
3. WHEN 查询标注员的任务 THEN THE System SHALL 使用数据集分配表的任务范围进行高效过滤
4. WHEN 任务列表包含超过100条记录 THEN THE System SHALL 支持分页查询
5. WHEN API返回任务列表 THEN THE System SHALL 包含任务总数、当前页码、每页数量等分页信息

### Requirement 5

**User Story:** 作为系统，我需要增强现有的数据集任务列表API，添加基于角色和分配的权限过滤。

#### Acceptance Criteria

1. WHEN 标注员请求数据集任务列表 THEN THE System SHALL 只返回分配给该标注员的任务
2. WHEN 浏览员请求数据集任务列表 THEN THE System SHALL 只返回状态为已完成的任务
3. WHEN 管理员请求数据集任务列表 THEN THE System SHALL 返回该数据集的所有任务
4. WHEN 标注员的分配范围为任务1-50 THEN THE System SHALL 按任务ID排序后返回第1到第50个任务
5. WHEN 用户请求未授权的数据集任务列表 THEN THE System SHALL 返回403权限错误

### Requirement 6

**User Story:** 作为开发者，我需要清晰的权限检查逻辑，以便系统可以正确地控制不同角色的访问权限。

#### Acceptance Criteria

1. WHEN 系统检查用户权限 THEN THE System SHALL 首先验证用户的角色（admin/annotator/viewer）
2. WHEN 用户角色为管理员 THEN THE System SHALL 授予所有任务的访问和编辑权限
3. WHEN 用户角色为标注员 THEN THE System SHALL 检查数据集分配表以确定任务访问权限
4. WHEN 用户角色为浏览员 THEN THE System SHALL 只授予已完成任务的只读权限
5. WHEN 权限检查失败 THEN THE System SHALL 返回明确的错误信息（403 Forbidden）

### Requirement 7

**User Story:** 作为用户，我希望任务列表页面提供清晰的视觉反馈，以便我可以快速了解任务状态和我的权限。

#### Acceptance Criteria

1. WHEN 用户查看任务列表 THEN THE System SHALL 使用不同的颜色或图标标识任务状态（待处理、进行中、已完成、失败）
2. WHEN 标注员查看任务 THEN THE System SHALL 高亮显示优先级高的任务
3. WHEN 浏览员查看任务 THEN THE System SHALL 显示只读标识
4. WHEN 任务列表为空 THEN THE System SHALL 显示友好的空状态提示（如"暂无分配的任务"）
5. WHEN 用户权限不足 THEN THE System SHALL 显示清晰的权限提示信息

### Requirement 8

**User Story:** 作为标注员，我希望从"我的数据集"页面点击"开始标注"后，能够直接进入该数据集的任务列表，以便快速开始工作。

#### Acceptance Criteria

1. WHEN 标注员在"我的数据集"页面点击"开始标注" THEN THE System SHALL 跳转到任务列表页面并自动筛选该数据集的任务
2. WHEN 任务列表页面接收到数据集ID参数 THEN THE System SHALL 自动应用数据集筛选条件
3. WHEN 标注员查看筛选后的任务列表 THEN THE System SHALL 只显示该数据集中分配给该标注员的任务
4. WHEN 标注员清除数据集筛选 THEN THE System SHALL 显示所有分配给该标注员的任务（跨数据集）
5. WHEN URL包含数据集ID参数 THEN THE System SHALL 在页面标题或面包屑中显示当前数据集名称

### Requirement 9

**User Story:** 作为系统，我需要确保任务范围的正确性，以便标注员只能看到和操作分配给他们的任务。

#### Acceptance Criteria

1. WHEN 系统计算任务范围 THEN THE System SHALL 使用数据集分配表中的 task_start_index 和 task_end_index
2. WHEN 任务范围为 NULL THEN THE System SHALL 解释为分配了该数据集的所有任务
3. WHEN 任务范围为 1-50 THEN THE System SHALL 按任务ID排序后取第1到第50个任务
4. WHEN 多个标注员分配了不同范围 THEN THE System SHALL 确保每个标注员只能看到自己的范围
5. WHEN 任务被删除或重新排序 THEN THE System SHALL 保持任务索引的一致性

### Requirement 10

**User Story:** 作为系统，我需要提供新的跨数据集任务列表API端点，以支持任务列表页面的功能。

#### Acceptance Criteria

1. WHEN 系统启动 THEN THE System SHALL 提供 GET /api/v1/tasks 端点用于查询跨数据集任务列表
2. WHEN API接收到请求 THEN THE System SHALL 支持按数据集ID、状态、分配用户进行筛选
3. WHEN API接收到请求 THEN THE System SHALL 支持按创建时间、更新时间、状态进行排序
4. WHEN API返回任务列表 THEN THE System SHALL 包含每个任务的数据集名称、语料文本预览、实体数、关系数
5. WHEN API接收到未认证的请求 THEN THE System SHALL 返回401未授权错误

### Requirement 11

**User Story:** 作为开发者，我需要确保API修改的向后兼容性，以便现有功能不受影响。

#### Acceptance Criteria

1. WHEN 修改 GET /api/v1/datasets/{dataset_id}/tasks API THEN THE System SHALL 保持响应数据结构不变
2. WHEN 数据集详情页面调用任务列表API THEN THE System SHALL 根据当前用户权限返回相应的任务
3. WHEN 管理员在数据集详情页查看任务 THEN THE System SHALL 显示该数据集的所有任务（与修改前行为一致）
4. WHEN 标注员在数据集详情页查看任务 THEN THE System SHALL 只显示分配给该标注员的任务
5. WHEN 浏览员在数据集详情页查看任务 THEN THE System SHALL 只显示已完成的任务
