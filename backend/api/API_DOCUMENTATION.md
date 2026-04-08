# API 文档总览

本文档汇总了所有API端点的说明。详细的API文档请参考各个模块的README文件。

---

## 📚 API模块列表

### 1. 语料管理API
**文件**: `corpus.py`  
**文档**: [README_CORPUS_API.md](./README_CORPUS_API.md)  
**端点数**: 5个

**主要功能**:
- 上传Excel文件
- 获取语料列表（分页、筛选）
- 获取语料详情
- 删除语料
- 获取语料关联图片

---

### 2. 数据集管理API
**文件**: `dataset.py`  
**文档**: [README_DATASET_API.md](./README_DATASET_API.md)  
**端点数**: 7个

**主要功能**:
- 创建数据集
- 获取数据集列表
- 获取数据集详情
- 更新数据集
- 删除数据集
- 获取数据集统计
- 导出数据集

---

### 3. 标签管理API
**文件**: `labels.py`  
**文档**: [README_LABELS_API.md](./README_LABELS_API.md)  
**端点数**: 20个

**主要功能**:
- 实体类型CRUD（6个端点）
- 关系类型CRUD（6个端点）
- 标签导入导出（3个端点）
- 版本管理（5个端点）

---

### 4. 标注任务API
**文件**: `annotations.py`  
**端点数**: 12个

**主要功能**:
- 批量标注（3个端点）
- 任务管理（2个端点）
- 实体管理（3个端点）
- 关系管理（3个端点）

**核心端点**:

#### 批量标注
- `POST /api/v1/annotations/batch` - 触发批量自动标注
- `GET /api/v1/annotations/batch/{job_id}` - 获取批量任务状态
- `POST /api/v1/annotations/batch/{job_id}/cancel` - 取消批量任务

#### 任务管理
- `GET /api/v1/annotations/{task_id}` - 获取标注任务详情
- `PUT /api/v1/annotations/{task_id}` - 更新标注任务

#### 实体管理
- `POST /api/v1/annotations/{task_id}/entities` - 添加文本实体
- `PUT /api/v1/annotations/{task_id}/entities/{id}` - 更新文本实体
- `DELETE /api/v1/annotations/{task_id}/entities/{id}` - 删除文本实体

#### 关系管理
- `POST /api/v1/annotations/{task_id}/relations` - 添加关系
- `PUT /api/v1/annotations/{task_id}/relations/{id}` - 更新关系
- `DELETE /api/v1/annotations/{task_id}/relations/{id}` - 删除关系

---

### 5. 图片标注API
**文件**: `images.py`  
**文档**: [README_IMAGES_API.md](./README_IMAGES_API.md)  
**端点数**: 4个

**主要功能**:
- 添加图片实体（支持整图和区域标注）
- 获取图片实体列表
- 更新图片实体
- 删除图片实体

**核心端点**:
- `POST /api/v1/images/{image_id}/entities` - 添加图片实体
- `GET /api/v1/images/{image_id}/entities` - 获取图片实体列表
- `PUT /api/v1/images/{image_id}/entities/{id}` - 更新图片实体
- `DELETE /api/v1/images/{image_id}/entities/{id}` - 删除图片实体

---

### 6. 版本管理API
**文件**: `versions.py`  
**端点数**: 5个

**主要功能**:
- 获取版本历史
- 版本回滚
- 版本比较
- 版本详情查看
- 手动创建快照

**核心端点**:
- `GET /api/v1/versions/{task_id}` - 获取版本历史
- `POST /api/v1/versions/{task_id}/rollback` - 回滚版本
- `GET /api/v1/versions/compare` - 比较版本差异
- `GET /api/v1/versions/{task_id}/{version}` - 获取版本详情
- `POST /api/v1/versions/{task_id}/snapshot` - 手动创建快照

---

### 7. 复核管理API
**文件**: `review.py`  
**端点数**: 7个

**主要功能**:
- 提交复核
- 获取复核任务列表
- 获取复核任务详情
- 批准任务
- 驳回任务
- 数据集质量统计
- 数据集复核摘要

**核心端点**:
- `POST /api/v1/review/submit/{task_id}` - 提交复核
- `GET /api/v1/review/tasks` - 获取复核任务列表
- `GET /api/v1/review/{review_id}` - 获取复核任务详情
- `POST /api/v1/review/{review_id}/approve` - 批准任务
- `POST /api/v1/review/{review_id}/reject` - 驳回任务
- `GET /api/v1/review/dataset/{dataset_id}/statistics` - 获取数据集质量统计
- `GET /api/v1/review/dataset/{dataset_id}/summary` - 获取数据集复核摘要

---

### 8. 用户管理和认证API
**文件**: `users.py`  
**端点数**: 9个

**主要功能**:
- 用户登录登出
- 用户CRUD操作
- JWT认证
- 权限控制
- 用户统计

**核心端点**:

#### 认证端点
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/logout` - 用户登出
- `GET /api/v1/auth/me` - 获取当前用户信息

#### 用户管理端点（需要管理员权限）
- `POST /api/v1/users` - 创建用户
- `GET /api/v1/users` - 获取用户列表
- `GET /api/v1/users/{user_id}` - 获取用户详情
- `PUT /api/v1/users/{user_id}` - 更新用户信息
- `DELETE /api/v1/users/{user_id}` - 删除用户
- `GET /api/v1/users/statistics/summary` - 获取用户统计

**权限说明**:
- **admin**: 管理员，拥有所有权限
- **annotator**: 标注人员，可以进行标注和复核
- **reviewer**: 复核人员，可以进行复核

---

## 📊 API统计

| 模块 | 端点数 | 状态 |
|------|--------|------|
| 语料管理 | 5 | ✅ 已完成 |
| 数据集管理 | 7 | ✅ 已完成 |
| 标签管理 | 20 | ✅ 已完成 |
| 标注任务 | 12 | ✅ 已完成 |
| 图片标注 | 4 | ✅ 已完成 |
| 版本管理 | 5 | ✅ 已完成 |
| 复核管理 | 7 | ✅ 已完成 |
| 用户管理和认证 | 9 | ✅ 已完成 |
| **总计** | **69** | **已完成** |

---

## 🔗 快速链接

- [语料管理API详细文档](./README_CORPUS_API.md)
- [数据集管理API详细文档](./README_DATASET_API.md)
- [标签管理API详细文档](./README_LABELS_API.md)
- [图片标注API详细文档](./README_IMAGES_API.md)

---

## 🚀 使用示例

### 完整标注流程

```bash
# 0. 用户登录
POST /api/v1/auth/login

# 1. 上传Excel文件
POST /api/v1/corpus/upload

# 2. 创建数据集
POST /api/v1/datasets

# 3. 触发批量自动标注
POST /api/v1/annotations/batch

# 4. 查询批量任务进度
GET /api/v1/annotations/batch/{job_id}

# 5. 手动编辑标注（可选）
PUT /api/v1/annotations/{task_id}/entities/{id}
POST /api/v1/annotations/{task_id}/relations

# 6. 添加图片标注（可选）
POST /api/v1/images/{image_id}/entities

# 7. 提交复核
POST /api/v1/review/submit/{task_id}

# 8. 复核人员批准/驳回
POST /api/v1/review/{review_id}/approve
POST /api/v1/review/{review_id}/reject

# 9. 查看质量统计
GET /api/v1/review/dataset/{dataset_id}/statistics

# 10. 导出数据集
POST /api/v1/datasets/{id}/export
```

---

## 📝 通用响应格式

所有API端点遵循统一的响应格式:

### 成功响应
```json
{
  "success": true,
  "message": "操作描述",
  "data": { ... }
}
```

### 错误响应
```json
{
  "detail": "错误描述信息"
}
```

---

## 🔐 认证和授权

系统已实现JWT Token认证和基于角色的权限控制。

### 认证流程

1. **登录**: 使用用户名和密码调用 `POST /api/v1/auth/login`
2. **获取Token**: 登录成功后获得JWT访问令牌
3. **使用Token**: 在后续请求的Header中携带令牌
   ```
   Authorization: Bearer <your_token>
   ```
4. **登出**: 调用 `POST /api/v1/auth/logout`（前端删除token）

### 角色权限

| 角色 | 权限 |
|------|------|
| **admin** | 所有权限，包括用户管理、系统配置 |
| **annotator** | 标注和复核权限 |
| **reviewer** | 复核权限 |

### 权限控制

- 用户管理API（创建、更新、删除用户）需要**管理员权限**
- 其他API需要**登录认证**
- 未授权访问返回 `401 Unauthorized`
- 权限不足返回 `403 Forbidden`

---

## 📖 相关文档

- [测试指南](../TESTING_GUIDE.md)
- [项目README](../../README.md)
- [任务列表](../../.kiro/specs/entity-relation-annotation-tool/tasks.md)
- [项目进度](../../项目进度总结.md)

---

*最后更新: 2024-01-19*
