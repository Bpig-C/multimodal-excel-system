
# 品质失效案例实体关系标注系统

《品质失效案例实体关系标注系统》是一款自动化实体关系标注工具，支持从品质失效案例Excel文件导入数据，通过LLM批量自动标注和人工编辑相结合的方式，生成高质量的实体关系标注数据集。

---

## ⚠️ 重要提示

**创建文档前必读**: [DOCUMENTATION_RULES.md](DOCUMENTATION_RULES.md)

**核心原则**:
- 能不创建就不创建
- 临时文档用完立即删除
- 优先更新现有文档

---

## 技术栈

### 后端
- FastAPI - Web框架
- LangChain v1.0 - Agent框架
- SQLAlchemy - ORM
- SQLite - 数据库
- Qwen-Max - LLM模型（通过DashScope API）

### 前端
- Vue 3 - 前端框架
- TypeScript - 类型安全
- Element Plus - UI组件库
- Pinia - 状态管理
- Vite - 构建工具

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- Conda（推荐）或 virtualenv

### 后端启动

#### 1. 创建并激活conda环境（推荐）

```bash
conda create -n agent python=3.10
conda activate agent
```

#### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 3. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=your_api_key_here
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

#### 4. 初始化数据库

```bash
python init_db.py
```

#### 5. 启动后端服务

```bash
cd backend
conda activate agent
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# python main.py
```

后端将在 http://localhost:8000 启动

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端将在 http://localhost:5173 启动

## 测试

### 运行所有测试

```bash
cd backend
python run_tests.py
```

### 运行指定测试

```bash
# 交互式选择
python run_tests.py

# 直接指定测试模块
python run_tests.py excel_processing
python run_tests.py entity_extraction
python run_tests.py dataset_service
python run_tests.py label_management
python run_tests.py batch_annotation
```

### 运行Task 12-16综合测试

```bash
cd backend
python test_tasks_12_to_16.py
```

### 可用的测试模块

**基础功能测试**:
- `db_models` - 数据库模型测试
- `schemas` - Pydantic模型测试
- `excel_processing` - Excel处理测试
- `offset_correction` - 偏移量修正测试
- `entity_extraction` - 实体抽取测试
- `relation_extraction` - 关系抽取测试
- `dataset_service` - 数据集服务测试

**新增功能测试 (Task 12-16)**:
- `label_management` - 标签管理服务测试 (Task 12)
- `labels_api` - 标签管理API测试 (Task 13)
- `batch_annotation` - 批量标注服务测试 (Task 14)
- `annotations_api` - 标注任务API测试 (Task 15)
- `images_api` - 图片标注API测试 (Task 16)

详细测试指南请查看: [backend/TESTING_GUIDE.md](backend/TESTING_GUIDE.md)

## 项目结构

```
.
├── backend/              # 后端代码
│   ├── models/          # 数据模型
│   │   ├── db_models.py      # SQLAlchemy数据库模型
│   │   └── schemas.py        # Pydantic请求/响应模型
│   ├── services/        # 业务逻辑
│   │   ├── excel_processing.py    # Excel处理服务
│   │   ├── offset_correction.py   # 偏移量修正服务
│   │   └── dataset_service.py     # 数据集管理服务
│   ├── agents/          # LangChain Agents
│   │   ├── entity_extraction.py        # 实体抽取Agent
│   │   ├── relation_extraction.py      # 关系抽取Agent
│   │   └── label_definition_generator.py  # 标签定义生成Agent
│   ├── api/             # API路由
│   │   ├── corpus.py    # 语料管理API
│   │   └── dataset.py   # 数据集管理API
│   ├── tests/           # 测试文件
│   ├── test_*.py        # 单元测试
│   ├── run_tests.py     # 测试运行脚本
│   ├── config.py        # 配置管理
│   ├── database.py      # 数据库连接
│   ├── init_db.py       # 数据库初始化
│   └── main.py          # 应用入口
├── frontend/            # 前端代码
│   └── src/
│       ├── views/       # 页面组件
│       ├── components/  # 通用组件
│       ├── stores/      # 状态管理
│       ├── api/         # API封装
│       └── types/       # 类型定义
├── data/                # 数据目录
│   ├── database/        # SQLite数据库
│   ├── uploads/         # 上传文件
│   ├── images/          # 提取的图片
│   └── exports/         # 导出数据
└── .kiro/specs/         # 设计文档
    └── entity-relation-annotation-tool/
        ├── requirements.md  # 需求文档
        ├── design.md        # 设计文档
        └── tasks.md         # 任务列表
```

## 功能特性

### 已完成功能 ✅

- ✅ 项目初始化和基础架构
- ✅ 数据库模型和ORM配置（14个表）
- ✅ Pydantic数据模型定义
- ✅ Excel文件处理和WPS图片提取
- ✅ 语料管理API（上传、查询、删除）
- ✅ 偏移量验证与自动修正
- ✅ LangChain实体抽取Agent（16种实体类型）
- ✅ LangChain关系抽取Agent（8种关系类型）
- ✅ 数据集管理服务（创建、查询、统计、导出）
- ✅ 数据集管理API（完整CRUD）
- ✅ 标签定义生成Agent（LLM自动生成标签定义）
- ✅ 标签体系管理服务（动态Prompt生成、版本管理）
- ✅ 标签管理API（20个端点）
- ✅ 批量标注服务（异步执行、进度跟踪）
- ✅ 标注任务API（12个端点）
- ✅ 图片标注API（整图和区域标注）

**总进度**: 16/46 核心任务完成 (35%)

### 计划功能 📋

- 📋 版本管理服务和API
- 📋 复核服务和API
- 📋 数据导出服务
- 📋 Reward数据集生成
- 📋 用户管理和认证
- 📋 前端界面开发

---

## 📚 文档索引

完整的项目文档已整理到 `docs/` 目录，按类别组织：

### 用户指南
- [快速开始](./docs/user-guides/getting-started.md) - 系统安装和首次使用
- [标签配置指南](./docs/user-guides/label-configuration.md) - 标签体系配置
- [数据库脚本使用](./docs/user-guides/database-scripts.md) - 数据库维护

### 开发文档
- [后端项目总览](./docs/development/backend/overview.md) - 后端架构和技术栈
- [API集成指南](./docs/development/backend/api-integration.md) - 前端对接API
- [前端项目总览](./docs/development/frontend/overview.md) - 前端架构和技术栈
- [前端实现日志](./docs/development/frontend/implementation-log.md) - 开发记录
- [测试指南](./docs/development/testing/test-guide.md) - 测试策略和方法

### 功能文档
- [标注工作流](./docs/features/annotation-workflow.md) - 完整的标注流程
- [批量标注](./docs/features/batch-annotation.md) - 自动批量标注功能
- [版本管理](./docs/features/version-management.md) - 标签体系版本控制

### 项目文档
- [项目状态](./docs/project/status.md) - 当前开发进度
- [变更日志](./docs/project/changelog.md) - 功能更新和问题修复
- [路线图](./docs/project/roadmap.md) - 未来开发计划

### 规格文档
- [任务列表](./.kiro/specs/entity-relation-annotation-tool/tasks.md) - 完整的任务清单
- [需求文档](./.kiro/specs/entity-relation-annotation-tool/requirements.md) - 系统需求
- [设计文档](./.kiro/specs/entity-relation-annotation-tool/design.md) - 系统设计

**查看完整文档索引**: [docs/README.md](./docs/README.md)

---

## API文档

启动后端服务后，访问以下地址查看交互式API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

详细的API文档请查看 [API总览](./backend/api/API_DOCUMENTATION.md)

---

1. **Conda环境**: 建议使用conda创建名为`agent`的环境，避免依赖冲突
2. **API密钥**: 需要配置有效的DashScope API密钥才能使用LLM功能
3. **测试数据**: 测试时会创建临时数据库，不会影响生产数据
4. **图片提取**: 支持WPS Excel内嵌图片提取（DISPIMG公式）

## 贡献指南

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## License

MIT
