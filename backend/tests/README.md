# 测试目录

本目录包含所有后端测试代码和测试产物。

## 📁 目录结构

```
tests/
├── unit/              # 单元测试 (52个测试) - 测试单个模块/服务
│   ├── test_user_service.py
│   ├── test_export_service.py
│   ├── test_review_service.py
│   ├── test_serialization_service.py
│   ├── test_reward_dataset.py
│   ├── test_dataset_service.py
│   ├── test_version_management.py
│   ├── test_batch_annotation.py
│   ├── test_excel_processing.py
│   ├── test_offset_correction.py
│   ├── test_db_models.py
│   ├── test_schemas.py
│   └── test_label_management.py
│
├── api/               # API测试 (66个测试) - 测试REST API端点
│   ├── test_users_api.py
│   ├── test_review_api.py
│   ├── test_annotations_api.py
│   ├── test_images_api.py
│   ├── test_labels_api.py
│   ├── test_versions_api.py
│   ├── test_api_corpus.py
│   └── test_api_dataset.py
│
├── agents/            # Agent测试 (7个测试) - 测试AI代理
│   ├── test_entity_extraction.py
│   ├── test_relation_extraction.py
│   └── test_image_annotation_agent.py
│
├── integration/       # 集成测试 - 测试多个组件协作
│   └── integration_test.py
│
├── manual/            # 手动测试脚本 - 用于快速验证API功能
│   ├── README.md
│   ├── test_annotation_task_api.py
│   ├── test_dataset_tasks_api.py
│   ├── test_labels_api.py
│   ├── test_versions_api.py
│   └── test_task_text.py
│
└── test_artifacts/    # 测试产物 (自动生成)
    ├── databases/     # 测试数据库文件 (*.db)
    └── reports/       # 测试报告 (test_report_*.txt)
```

## 🚀 运行测试

### 运行所有测试
```bash
# 从backend目录
python run_tests.py

# 或使用pytest直接运行
pytest
```

### 运行并保存报告
```bash
python run_tests.py --save
# 报告保存在: tests/test_artifacts/reports/
```

### 按类型运行测试
```bash
# 单元测试
pytest tests/unit/ -v

# API测试
pytest tests/api/ -v

# Agent测试
pytest tests/agents/ -v

# 集成测试
pytest tests/integration/ -v
```

### 运行特定测试文件
```bash
pytest tests/unit/test_user_service.py -v
pytest tests/api/test_users_api.py -v
```

### 运行特定测试
```bash
pytest tests/unit/test_user_service.py::test_create_user -v
```

### 手动测试脚本

手动测试脚本位于 `tests/manual/` 目录，用于快速验证API功能：

```bash
cd tests/manual

# 测试标注任务API
python test_annotation_task_api.py

# 测试数据集任务列表API
python test_dataset_tasks_api.py

# 测试标签API
python test_labels_api.py

# 测试版本管理API
python test_versions_api.py

# 测试任务文本内容
python test_task_text.py
```

**注意**: 
- 手动测试脚本需要后端服务运行（`python main.py`）
- 这些脚本用于开发调试，不是自动化测试
- 详细说明见 `tests/manual/README.md`

### Windows快捷方式
```bash
test.bat
```

## 📊 测试统计

- **总测试数**: 130
- **单元测试**: 52 (100% 通过) ✅
- **API测试**: 66 (78.8% 通过) ⚠️
- **Agent测试**: 7 (100% 通过) ✅
- **集成测试**: 待添加

详细状态查看: `../docs/testing/TEST_STATUS.md`

## 📝 测试文档

所有测试相关文档位于: `../docs/testing/`

- **TEST_STATUS.md** - 当前测试状态和结果
- **TEST_FIXES_APPLIED.md** - 测试修复记录
- **README_TESTS.md** - 完整测试说明
- **HOW_TO_RUN_TESTS.md** - 运行指南

## 🧹 清理测试产物

测试数据库和报告会自动保存在`test_artifacts/`目录。如需清理：

```bash
# Windows
del tests\test_artifacts\databases\*.db
del tests\test_artifacts\reports\*.txt

# Linux/Mac
rm tests/test_artifacts/databases/*.db
rm tests/test_artifacts/reports/*.txt
```

## 编写测试

### 单元测试示例
```python
import pytest
from services.user_service import UserService

@pytest.fixture
def user_service(db):
    return UserService(db)

def test_create_user(user_service):
    user = user_service.create_user(
        username="test",
        password="pass123",
        role="annotator"
    )
    assert user.username == "test"
```

### API测试示例
```python
from fastapi.testclient import TestClient

def test_login(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## 测试最佳实践

1. **测试独立性** - 每个测试应该独立运行
2. **使用Fixtures** - 复用测试设置代码
3. **清晰命名** - 测试名称应该描述测试内容
4. **单一职责** - 每个测试只测试一个功能
5. **数据清理** - 测试后清理数据

## ⚠️ 注意事项

1. 测试数据库文件(*.db)不应提交到git
2. 测试报告可以定期清理
3. 某些API测试可能因fixture问题失败，但不影响功能使用
4. 详细问题说明见 `../docs/testing/TEST_STATUS.md`
