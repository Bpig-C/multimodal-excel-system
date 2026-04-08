# 后端文档中心

欢迎来到实体关系标注系统后端文档中心！

## 📚 文档导航

### 🚀 快速开始

| 文档 | 说明 | 适用人群 |
|------|------|----------|
| [后端项目总览](./BACKEND_PROJECT_OVERVIEW.md) | 项目架构、技术栈、功能模块 | 所有开发者 |
| [前端对接指南](./FRONTEND_INTEGRATION_GUIDE.md) | API使用、认证流程、数据模型 | 前端开发者 |
| [API文档总览](../api/API_DOCUMENTATION.md) | 所有API端点汇总 | 前后端开发者 |

### 📖 API详细文档

| 模块 | 文档 | 端点数 |
|------|------|--------|
| 语料管理 | [README_CORPUS_API.md](../api/README_CORPUS_API.md) | 5 |
| 数据集管理 | [README_DATASET_API.md](../api/README_DATASET_API.md) | 7 |
| 标签管理 | [README_LABELS_API.md](../api/README_LABELS_API.md) | 20 |
| 图片标注 | [README_IMAGES_API.md](../api/README_IMAGES_API.md) | 4 |

### 🧪 测试文档

| 文档 | 说明 |
|------|------|
| [测试状态](./testing/TEST_STATUS.md) | 当前测试覆盖率和结果 |
| [测试说明](./testing/README_TESTS.md) | 完整测试系统说明 |
| [运行指南](./testing/HOW_TO_RUN_TESTS.md) | 如何运行测试 |
| [修复记录](./testing/TEST_FIXES_APPLIED.md) | 测试问题修复历史 |

### 🎨 设计文档

| 文档 | 说明 |
|------|------|
| [标签管理设计](../agents/LABEL_MANAGEMENT_DESIGN.md) | 标签体系设计 |
| [版本管理设计](../agents/LABEL_SCHEMA_VERSION_MANAGEMENT.md) | 版本控制设计 |
| [动态Prompt设计](../agents/README_DYNAMIC_PROMPT.md) | AI Prompt生成 |
| [图片标注设计](../agents/README_IMAGE_ANNOTATION.md) | 图片标注功能 |

---

## 🎯 按角色查看文档

### 前端开发者

**必读文档**:
1. [前端对接指南](./FRONTEND_INTEGRATION_GUIDE.md) ⭐
2. [API文档总览](../api/API_DOCUMENTATION.md)
3. [后端项目总览](./BACKEND_PROJECT_OVERVIEW.md)

**在线工具**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 后端开发者

**必读文档**:
1. [后端项目总览](./BACKEND_PROJECT_OVERVIEW.md) ⭐
2. [测试状态](./testing/TEST_STATUS.md)
3. [API文档总览](../api/API_DOCUMENTATION.md)

**代码位置**:
- API层: `backend/api/`
- 业务层: `backend/services/`
- 数据层: `backend/models/`
- AI层: `backend/agents/`

### 测试工程师

**必读文档**:
1. [测试状态](./testing/TEST_STATUS.md) ⭐
2. [测试说明](./testing/README_TESTS.md)
3. [运行指南](./testing/HOW_TO_RUN_TESTS.md)

**测试位置**:
- 单元测试: `backend/tests/unit/`
- API测试: `backend/tests/api/`
- Agent测试: `backend/tests/agents/`

### 项目经理

**必读文档**:
1. [后端项目总览](./BACKEND_PROJECT_OVERVIEW.md) ⭐
2. [测试状态](./testing/TEST_STATUS.md)

**关键指标**:
- API完成度: 100% (69/69)
- 测试通过率: 85.4% (111/130)
- 文档完整度: 100%

---

## 📊 项目状态

### 开发进度

| 模块 | 状态 | 测试 | 文档 |
|------|------|------|------|
| 用户管理 | ✅ | ✅ 100% | ✅ |
| 语料管理 | ✅ | ⚠️ 78.8% | ✅ |
| 数据集管理 | ✅ | ⚠️ 部分 | ✅ |
| 标签管理 | ✅ | ✅ 100% | ✅ |
| 标注任务 | ✅ | ✅ 100% | ✅ |
| 图片标注 | ✅ | ✅ 100% | ✅ |
| 版本管理 | ✅ | ✅ 100% | ✅ |
| 复核管理 | ✅ | ⚠️ 部分 | ✅ |
| AI Agent | ✅ | ✅ 100% | ✅ |

### 测试覆盖

- **总测试**: 130个
- **通过**: 111个 (85.4%)
- **失败**: 14个 (测试环境问题，不影响功能)
- **跳过**: 5个

---

## 🔗 快速链接

### 在线资源
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

### 代码仓库
- **API代码**: `backend/api/`
- **服务代码**: `backend/services/`
- **测试代码**: `backend/tests/`
- **文档**: `backend/docs/`

### 运行命令
```bash
# 启动服务
python main.py

# 运行测试
python run_tests.py

# 查看API文档
# 访问 http://localhost:8000/docs
```

---

## 📝 文档更新

所有文档都会定期更新。查看各文档底部的"最后更新"时间戳。

如有文档问题或建议，请提交Issue。

---

## 🆘 获取帮助

1. **查看文档**: 先查看相关文档
2. **查看Swagger**: 在线API文档有详细说明
3. **查看测试**: 测试代码是最好的使用示例
4. **提交Issue**: 如果还有问题，提交Issue

---

*文档中心最后更新: 2026-01-19*
