# 测试执行计划

## 📋 概述

本文档提供分批次的测试执行计划，帮助你系统地验证后端所有功能。每个批次都有明确的测试目标、执行命令和预期结果。

**测试环境要求**：
- Python 3.8+
- 已激活虚拟环境（推荐）
- 数据库已初始化：`python init_db.py`
- 环境变量已配置（`.env` 文件）

---

## 🎯 测试批次总览

| 批次 | 测试内容 | 预计时间 | 优先级 |
|------|---------|---------|--------|
| 批次1 | 快速冒烟测试 | 2-3分钟 | ⭐⭐⭐ |
| 批次2 | 核心API测试 | 5-8分钟 | ⭐⭐⭐ |
| 批次3 | 业务逻辑测试 | 8-10分钟 | ⭐⭐⭐ |
| 批次4 | 数据处理测试 | 5-7分钟 | ⭐⭐ |
| 批次5 | Agent测试 | 10-15分钟 | ⭐⭐ |
| 批次6 | 高级功能测试 | 8-10分钟 | ⭐⭐ |
| 批次7 | 完整集成测试 | 15-20分钟 | ⭐ |

---

## 📦 批次1：快速冒烟测试（必做）

**目标**：快速验证系统基本功能是否正常

**测试内容**：
- 数据库模型
- 基础Schema
- 集成测试

**执行命令**：
```bash
cd backend

# 方式1：单独运行
pytest test_db_models.py test_schemas.py -v

# 方式2：运行集成测试
python tests/integration_test.py
```

**预期结果**：
- ✅ 所有数据库模型字段完整
- ✅ Pydantic模型验证通过
- ✅ 集成测试流程完整

**失败处理**：
- 如果数据库模型测试失败 → 运行 `python init_db.py`
- 如果Schema测试失败 → 检查 `models/` 和 `schemas/` 目录

**测试记录**：
```
[ ] 测试已执行
[ ] 测试通过
[ ] 发现问题：_________________
```

---

## 📦 批次2：核心API测试（必做）

**目标**：验证核心API端点功能

**测试内容**：
- 用户管理API
- 标签管理API
- 图片管理API

**执行命令**：
```bash
cd backend

# 用户API测试
pytest test_users_api.py -v

# 标签API测试
pytest test_labels_api.py -v

# 图片API测试
pytest test_images_api.py -v
```

**预期结果**：
- ✅ 用户CRUD操作正常
- ✅ 标签管理20个端点可用
- ✅ 图片标注API正常

**API端点检查清单**：

**用户API**：
- [ ] POST /api/users - 创建用户
- [ ] GET /api/users - 获取用户列表
- [ ] GET /api/users/{id} - 获取用户详情
- [ ] PUT /api/users/{id} - 更新用户
- [ ] DELETE /api/users/{id} - 删除用户

**标签API**：
- [ ] GET /api/labels/entity-types - 获取实体类型
- [ ] POST /api/labels/entity-types - 创建实体类型
- [ ] GET /api/labels/relation-types - 获取关系类型
- [ ] POST /api/labels/relation-types - 创建关系类型

**图片API**：
- [ ] POST /api/images - 添加图片实体
- [ ] GET /api/images - 获取图片列表
- [ ] PUT /api/images/{id} - 更新图片
- [ ] DELETE /api/images/{id} - 删除图片

**测试记录**：
```
[ ] 测试已执行
[ ] 测试通过
[ ] 发现问题：_________________
```

---

## 📦 批次3：业务逻辑测试（必做）

**目标**：验证核心业务逻辑

**测试内容**：
- 标注任务管理
- 批量标注
- 版本管理
- 复核流程

**执行命令**：
```bash
cd backend

# 标注任务测试
pytest test_annotations_api.py -v

# 批量标注测试
pytest test_batch_annotation.py -v

# 版本管理测试
pytest test_version_management.py test_versions_api.py -v

# 复核流程测试
pytest test_review_service.py test_review_api.py -v
```

**预期结果**：
- ✅ 标注任务创建和管理正常
- ✅ 批量标注异步执行正常
- ✅ 版本快照和回滚功能正常
- ✅ 复核流程状态转换正常

**业务流程检查**：
- [ ] 创建标注任务
- [ ] 添加实体和关系
- [ ] 批量标注执行
- [ ] 创建版本快照
- [ ] 提交复核
- [ ] 批准/驳回标注

**测试记录**：
```
[ ] 测试已执行
[ ] 测试通过
[ ] 发现问题：_________________
```

---

## 📦 批次4：数据处理测试（推荐）

**目标**：验证数据处理和转换功能

**测试内容**：
- Excel处理
- 偏移量修正
- 数据集服务
- 导出服务
- 序列化服务

**执行命令**：
```bash
cd backend

# 数据处理测试
pytest test_excel_processing.py -v
pytest test_offset_correction.py -v
pytest test_dataset_service.py -v

# 导出和序列化测试
pytest test_export_service.py -v
pytest test_serialization_service.py -v
```

**预期结果**：
- ✅ Excel导入导出正常
- ✅ 偏移量自动修正功能正常
- ✅ 数据集管理正常
- ✅ JSONL导出格式正确
- ✅ 序列化往返一致性

**数据处理检查**：
- [ ] Excel文件解析
- [ ] 偏移量精确匹配
- [ ] 偏移量模糊匹配
- [ ] 数据集创建和查询
- [ ] 导出训练集/测试集
- [ ] 序列化反序列化

**测试记录**：
```
[ ] 测试已执行
[ ] 测试通过
[ ] 发现问题：_________________
```

---

## 📦 批次5：Agent测试（可选，需要API Key）

**目标**：验证AI Agent功能

**测试内容**：
- 实体抽取Agent
- 关系抽取Agent
- 图片标注Agent

**前置条件**：
- ✅ 配置 `DASHSCOPE_API_KEY` 环境变量
- ✅ 网络连接正常

**执行命令**：
```bash
cd backend

# 实体抽取测试
pytest test_entity_extraction.py -v

# 关系抽取测试
pytest test_relation_extraction.py -v

# 图片标注测试
pytest test_image_annotation_agent.py -v
```

**预期结果**：
- ✅ 实体抽取返回正确格式
- ✅ 关系抽取识别实体关系
- ✅ 图片标注生成描述

**注意事项**：
- Agent测试可能较慢（依赖外部API）
- 如果API Key未配置，测试会跳过
- 建议使用Mock进行快速测试

**测试记录**：
```
[ ] 测试已执行
[ ] 测试通过
[ ] 跳过（无API Key）
[ ] 发现问题：_________________
```

---

## 📦 批次6：高级功能测试（推荐）

**目标**：验证高级功能

**测试内容**：
- 标签管理服务
- 用户服务
- Reward数据集生成

**执行命令**：
```bash
cd backend

# 标签管理服务测试
pytest test_label_management.py -v

# 用户服务测试
pytest test_user_service.py -v

# Reward数据集测试
pytest test_reward_dataset.py -v
```

**预期结果**：
- ✅ 标签配置缓存正常
- ✅ 动态Prompt构建正常
- ✅ 用户权限管理正常
- ✅ Reward数据集生成正确

**功能检查**：
- [ ] 标签导入导出
- [ ] 标签版本管理
- [ ] 用户角色权限
- [ ] Reward数据筛选
- [ ] 标注差异计算

**测试记录**：
```
[ ] 测试已执行
[ ] 测试通过
[ ] 发现问题：_________________
```

---

## 📦 批次7：完整集成测试（可选）

**目标**：端到端验证完整业务流程

**测试内容**：
- 完整业务流程
- 所有模块集成

**执行命令**：
```bash
cd backend

# 方式1：运行集成测试
python tests/integration_test.py

# 方式2：运行所有测试
python tests/run_all_tests.py

# 方式3：使用pytest运行所有测试
pytest -v

# 方式4：带覆盖率报告
pytest --cov=. --cov-report=html --cov-report=term -v
```

**预期结果**：
- ✅ 所有测试通过
- ✅ 测试覆盖率 > 70%
- ✅ 无严重错误或警告

**完整流程检查**：
1. [ ] 用户注册和登录
2. [ ] 创建数据集和语料
3. [ ] 创建标注任务
4. [ ] 执行批量标注
5. [ ] 创建版本快照
6. [ ] 提交复核
7. [ ] 导出标注数据
8. [ ] 生成Reward数据集

**测试记录**：
```
[ ] 测试已执行
[ ] 测试通过
[ ] 测试覆盖率：_____%
[ ] 发现问题：_________________
```

---

## 🔧 测试工具和命令

### 统一测试运行器

```bash
cd backend
python run_tests.py
```

**菜单选项**：
1. db_models - 数据库模型测试
2. schemas - Pydantic模型测试
3. excel_processing - Excel处理测试
4. offset_correction - 偏移量修正测试
5. entity_extraction - 实体抽取测试
6. relation_extraction - 关系抽取测试
7. dataset_service - 数据集服务测试
8. label_management - 标签管理服务测试
9. labels_api - 标签管理API测试
10. batch_annotation - 批量标注服务测试
11. annotations_api - 标注任务API测试
12. images_api - 图片标注API测试
13. all - 运行所有测试

### Pytest常用命令

```bash
# 详细输出
pytest -v

# 显示print输出
pytest -s

# 运行特定测试
pytest test_file.py::test_function -v

# 运行匹配关键字的测试
pytest -k "user" -v

# 只运行失败的测试
pytest --lf -v

# 先运行失败的测试
pytest --ff -v

# 生成覆盖率报告
pytest --cov=. --cov-report=html -v

# 并行运行测试（需要安装pytest-xdist）
pytest -n auto -v
```

### 测试清理

```bash
cd backend
python tests/cleanup.py
```

---

## 📊 测试结果记录表

### 总体进度

| 批次 | 状态 | 通过率 | 执行时间 | 备注 |
|------|------|--------|---------|------|
| 批次1 | ⬜ | - | - | |
| 批次2 | ⬜ | - | - | |
| 批次3 | ⬜ | - | - | |
| 批次4 | ⬜ | - | - | |
| 批次5 | ⬜ | - | - | |
| 批次6 | ⬜ | - | - | |
| 批次7 | ⬜ | - | - | |

**状态说明**：
- ⬜ 未开始
- 🟡 进行中
- ✅ 已完成
- ❌ 失败

### 问题追踪

| 问题ID | 批次 | 测试文件 | 问题描述 | 状态 | 解决方案 |
|--------|------|---------|---------|------|---------|
| 1 | | | | ⬜ | |
| 2 | | | | ⬜ | |
| 3 | | | | ⬜ | |

---

## 🚨 常见问题和解决方案

### 问题1：模块导入失败

**错误信息**：`ModuleNotFoundError: No module named 'xxx'`

**解决方案**：
```bash
# 确保在backend目录下运行
cd backend

# 检查Python路径
python -c "import sys; print(sys.path)"

# 重新安装依赖
pip install -r requirements.txt
```

### 问题2：数据库锁定

**错误信息**：`database is locked`

**解决方案**：
```bash
# 停止所有使用数据库的进程
# 删除测试数据库
cd backend
python tests/cleanup.py
```

### 问题3：API Key错误

**错误信息**：`Invalid API Key`

**解决方案**：
```bash
# 检查.env文件
cat .env | grep DASHSCOPE_API_KEY

# 或跳过Agent测试
pytest -v -k "not agent"
```

### 问题4：测试超时

**错误信息**：`Test timeout`

**解决方案**：
```bash
# 增加超时时间
pytest --timeout=120 -v

# 或跳过慢速测试
pytest -v -m "not slow"
```

---

## 📈 测试最佳实践

1. **按顺序执行**：建议按批次1→2→3的顺序执行，确保基础功能正常
2. **记录结果**：每次测试后填写测试记录表
3. **问题追踪**：发现问题立即记录到问题追踪表
4. **定期清理**：测试前后运行清理脚本
5. **隔离测试**：每个批次使用独立的数据库

---

## 📚 相关文档

- [集成测试文档](./tests/README.md) - 集成测试详情
- [API文档](./api/API_DOCUMENTATION.md) - API接口文档
- [后端准备情况](./BACKEND_READINESS_REPORT.md) - 后端功能清单

---

## 📞 支持

如有测试相关问题：
1. 查看相关文档
2. 检查日志文件：`backend/logs/`
3. 提交Issue或联系开发团队

---

**最后更新**：2024-01-19

**版本**：v1.0.0
