# 后端测试说明

## 📁 目录结构

```
backend/
├── tests/                      # 测试目录
│   ├── unit/                  # 单元测试
│   ├── api/                   # API测试
│   ├── agents/                # Agent测试
│   └── integration/           # 集成测试
├── docs/                       # 测试文档
├── scripts/                    # 测试脚本
├── pytest.ini                  # Pytest配置
├── run_tests.py               # 主测试脚本
├── test.bat                   # Windows快速测试
└── README_TESTS.md            # 本文档
```

## 🚀 快速开始

### Windows
```cmd
test.bat
```

### 所有平台
```bash
# 运行测试（实时输出到终端）
python run_tests.py

# 运行测试并保存报告到文件（实时显示输出）
python run_tests.py --save
# 输出会实时显示，同时保存到 test_report_YYYYMMDD_HHMMSS.txt

# 简洁模式
python run_tests.py --quiet
```

### 使用 pytest
```bash
# 运行所有测试
pytest

# 运行特定类型
pytest tests/unit/      # 单元测试
pytest tests/api/       # API测试
pytest tests/agents/    # Agent测试
pytest tests/integration/  # 集成测试
```

### 测试报告

运行 `python run_tests.py --save` 会生成带时间戳的测试报告文件：
- 文件名格式：`test_report_YYYYMMDD_HHMMSS.txt`
- 包含完整的测试输出和结果汇总

## 📊 测试类型

### 单元测试 (tests/unit/)
测试单个模块或服务的功能
- 服务层测试
- 数据模型测试
- 工具函数测试

### API测试 (tests/api/)
测试REST API端点
- 用户认证API
- 数据管理API
- 标注API

### Agent测试 (tests/agents/)
测试AI代理功能
- 实体抽取
- 关系抽取
- 图像标注

### 集成测试 (tests/integration/)
测试多个组件协作
- 端到端流程测试
- 系统集成测试

## 🔧 测试工具

### 快速测试汇总
```bash
python scripts/run_quick_test.py
```

### 生成测试报告
```bash
python scripts/generate_test_report.py
```

### 清理测试文件
```bash
python scripts/cleanup_test_files.py
```

### 测试数据库连接
```bash
python scripts/test_db_connection.py
```

## 📈 测试覆盖率

```bash
# 生成覆盖率报告
pytest --cov=. --cov-report=html --cov-report=term

# 查看HTML报告
# 打开 htmlcov/index.html
```

## 📝 编写测试

### Fixture最佳实践

```python
import pytest

# Module scope - 表结构管理
@pytest.fixture(scope="module", autouse=True)
def setup_module():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Function scope - 数据清理
@pytest.fixture(scope="function", autouse=True)
def cleanup_data():
    yield
    db.query(Model).delete()
    db.commit()

# Function scope - 测试数据
@pytest.fixture(scope="function")
def test_user(db):
    user = create_user(...)
    yield user
```

### 测试示例

```python
def test_create_user(db, user_service):
    """测试创建用户"""
    user = user_service.create_user(
        username="test",
        password="pass123",
        role="annotator"
    )
    assert user.username == "test"
    assert user.role == "annotator"
```

## 🎯 测试覆盖率目标

- **核心服务**: >90%
- **API端点**: >80%
- **工具函数**: >85%
- **总体**: >75%

## 📚 相关文档

- [测试目录说明](tests/README.md)
- [测试状态](TEST_STATUS.md)
- [整理完成报告](CLEANUP_DONE.md)
- [测试修复总结](docs/TEST_FIX_SUMMARY.md)
