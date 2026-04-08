# Backend Scripts

**最后更新**: 2026-01-24

本目录包含后端维护、测试和迁移脚本。

---

## 📁 目录结构

```
scripts/
├── testing/          # 测试相关脚本
├── migration/        # 数据库迁移脚本
└── maintenance/      # 维护和清理脚本
```

---

## 🧪 测试脚本 (testing/)

### prepare_test_users.py
**用途**: 创建测试用户账户

**创建的用户**:
- `admin` / `admin123` - 管理员
- `test_annotator1` / `test123` - 标注员1
- `test_annotator2` / `test123` - 标注员2

**使用**:
```bash
cd backend
python scripts/testing/prepare_test_users.py
```

### test_assignment_api.py
**用途**: 测试数据集分配API

**测试覆盖**:
- 整体分配
- 范围分配
- 自动分配
- 取消分配
- 转移分配
- 获取分配情况
- 获取我的数据集

**使用**:
```bash
cd backend
python scripts/testing/test_assignment_api.py
```

**测试结果**: 参见 `docs/TASK47_API_TEST_REPORT.md`

### verify_test_structure.py
**用途**: 验证测试文件结构

**使用**:
```bash
cd backend
python scripts/testing/verify_test_structure.py
```

---

## 🔄 迁移脚本 (migration/)

### migrate_dataset_assignment.py
**用途**: 执行数据集分配功能的数据库迁移

**操作**:
- 创建 `dataset_assignments` 表
- 创建8个索引
- 验证迁移结果

**使用**:
```bash
cd backend
python scripts/migration/migrate_dataset_assignment.py
```

**相关SQL**: `backend/migrations/add_dataset_assignment.sql`

### create_default_version.py
**用途**: 创建默认标签版本

**使用**:
```bash
cd backend
python scripts/migration/create_default_version.py
```

---

## 🛠️ 维护脚本 (maintenance/)

> 所有维护脚本现在都以 `.env` 中的 `DATABASE_URL` 为准，不再回退到 `backend/data/database/annotation.db`。
> `backend/tests/` 下的 `.db` 文件仅用于测试，不属于业务数据库。

### reset_db.py
**用途**: 重置数据库（删除所有数据）

**⚠️ 警告**: 此操作不可逆！

**使用**:
```bash
cd backend
python scripts/maintenance/reset_db.py
```

### clean_orphan_datasets.py
**用途**: 清理孤立的数据集记录

**使用**:
```bash
cd backend
python scripts/maintenance/clean_orphan_datasets.py
```

### force_clean_db.py
**用途**: 强制清理数据库

**⚠️ 警告**: 此操作不可逆！

**使用**:
```bash
cd backend
python scripts/maintenance/force_clean_db.py
```

---

## 📝 使用建议

### 开发环境
1. 使用 `reset_db.py` 重置数据库
2. 使用 `prepare_test_users.py` 创建测试用户
3. 使用 `test_assignment_api.py` 验证功能

### 生产环境
1. 使用 `migration/` 中的脚本进行数据库迁移
2. 定期使用 `clean_orphan_datasets.py` 清理数据
3. 不要使用 `reset_db.py` 或 `force_clean_db.py`

---

## 🔗 相关文档

- `docs/TASK47_FINAL.md` - 数据集分配功能文档
- `docs/TASK47_API_TEST_REPORT.md` - API测试报告
- `docs/TESTING_STRATEGY.md` - 测试策略
- `backend/DATABASE_SCRIPTS_GUIDE.md` - 数据库脚本指南

---

**维护人**: AI Assistant
