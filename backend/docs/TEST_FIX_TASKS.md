# 测试修复任务清单

## 当前状态
- **总测试数**: 130
- **通过**: 95 (73%)
- **失败**: 24
- **错误**: 11

## 待修复的测试文件

### 1. test_users_api.py (11 errors + 2 failures)
**问题**: 数据库fixture作用域问题，测试间数据被清理
**原因**: 
- `setup_database` fixture 在每个测试后清理数据库
- 后续测试依赖前面测试创建的用户数据
- `admin_user` fixture 使用 module scope，但数据库在 function scope 被清理

**解决方案**:
- [ ] 将所有fixtures改为function scope
- [ ] 每个测试独立创建所需数据
- [ ] 确保fixture正确使用yield

### 2. tests/test_api_corpus.py (14 failures)
**问题**: "no such table: corpus" 错误
**原因**:
- `setup_database` fixture 的 `autouse=True` 已设置
- 但某些测试方法没有正确触发fixture
- 可能是TestClient的数据库覆盖问题

**解决方案**:
- [ ] 检查 `override_get_db` 是否正确设置
- [ ] 确保所有测试方法都触发 `setup_database` fixture
- [ ] 验证数据库引擎和session的一致性

### 3. test_review_api.py (8 failures)
**问题**: 数据库操作失败
**原因**:
- 类似 test_users_api.py 的fixture作用域问题
- 测试间数据依赖问题

**解决方案**:
- [ ] 统一fixture作用域
- [ ] 确保每个测试独立创建数据
- [ ] 修复fixture的yield使用

## 修复优先级

1. **高优先级**: test_users_api.py (影响13个测试)
2. **高优先级**: tests/test_api_corpus.py (影响14个测试)
3. **中优先级**: test_review_api.py (影响8个测试)

## 修复策略

### 通用原则
1. 每个测试应该独立，不依赖其他测试的数据
2. 使用 function scope 的 fixtures 确保测试隔离
3. 正确使用 `yield` 而不是 `return` 在 fixtures 中
4. 确保数据库在每个测试前正确初始化

### 具体步骤
1. 修复 test_users_api.py 的 fixture 作用域
2. 修复 tests/test_api_corpus.py 的数据库初始化
3. 修复 test_review_api.py 的类似问题
4. 运行测试验证修复
5. 更新测试文档

## 进度跟踪
- [x] 分析测试失败原因
- [x] 修复 test_users_api.py - 改为module scope的setup + function scope的cleanup
- [x] 修复 tests/test_api_corpus.py - 改为class scope的setup + function scope的clean
- [ ] 修复 test_review_api.py
- [ ] 验证所有测试通过
- [ ] 更新测试文档
