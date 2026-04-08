# 测试文档目录

本目录包含所有与测试相关的文档。

## 📁 文档列表

### 核心文档

- **TEST_STATUS.md** - 当前测试状态和结果汇总
- **TEST_FIXES_APPLIED.md** - 测试修复记录和历史
- **README_TESTS.md** - 测试系统完整说明
- **HOW_TO_RUN_TESTS.md** - 测试运行指南

### 测试产物位置

- **测试报告**: `../tests/test_artifacts/reports/`
- **测试数据库**: `../tests/test_artifacts/databases/`
- **测试代码**: `../tests/`

## 🚀 快速开始

### 运行所有测试
```bash
# 在backend目录下
python run_tests.py
```

### 运行测试并保存报告
```bash
python run_tests.py --save
```

### 运行特定测试
```bash
pytest tests/unit/ -v          # 单元测试
pytest tests/api/ -v           # API测试
pytest tests/agents/ -v        # Agent测试
```

### Windows快捷方式
```bash
test.bat
```

## 📊 当前测试状态

查看 **TEST_STATUS.md** 获取最新的测试结果和状态。

## 🔧 测试结构

```
backend/
├── tests/                          # 测试代码
│   ├── unit/                       # 单元测试
│   ├── api/                        # API测试
│   ├── agents/                     # Agent测试
│   ├── integration/                # 集成测试
│   └── test_artifacts/             # 测试产物
│       ├── databases/              # 测试数据库文件
│       └── reports/                # 测试报告
├── docs/testing/                   # 测试文档（本目录）
├── scripts/                        # 测试工具脚本
├── run_tests.py                    # 主测试运行脚本
└── test.bat                        # Windows快捷脚本
```

## 📝 文档更新

测试文档会在每次重要测试运行后更新。查看各文档的"最后更新"时间戳。
