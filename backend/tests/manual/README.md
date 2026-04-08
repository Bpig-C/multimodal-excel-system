# 手动测试脚本

本目录包含用于手动测试API的Python脚本。这些脚本用于快速验证API功能，不是自动化测试的一部分。

## 使用方法

### 前提条件
1. 后端服务正在运行（`python main.py`）
2. 已安装requests库（`pip install requests`）

### 运行脚本

```bash
cd backend/tests/manual

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

## 脚本说明

### test_annotation_task_api.py
测试获取标注任务详情API
- 端点: `GET /api/v1/annotations/{task_id}`
- 验证任务信息返回

### test_dataset_tasks_api.py
测试获取数据集任务列表API
- 端点: `GET /api/v1/datasets/{dataset_id}/tasks`
- 验证分页和筛选功能

### test_labels_api.py
测试标签管理API
- 端点: `GET /api/v1/labels/entities`
- 端点: `GET /api/v1/labels/relations`
- 验证标签列表返回

### test_versions_api.py
测试版本管理API
- 端点: `GET /api/v1/labels/versions`
- 验证版本列表和详情

### test_task_text.py
测试不同任务的文本内容
- 验证语料文本正确加载
- 检查文本长度和内容

## 注意事项

1. **这些不是自动化测试**：它们需要手动运行并检查输出
2. **需要真实数据**：脚本中使用的ID需要存在于数据库中
3. **用于调试**：主要用于开发过程中快速验证API功能
4. **不计入测试覆盖率**：自动化测试在`tests/api/`目录中

## 自动化测试

如需运行自动化测试，请使用：
```bash
cd backend
python run_tests.py
```

或查看 [测试指南](../../../docs/development/testing/test-guide.md)
