# 测试修复总结

## 已完成的修复

### 1. test_users_api.py ✅
**问题**: 数据库在每个测试后被完全清理（包括表结构），导致后续测试失败

**修复方案**:
- 将 `setup_database` 改为 `setup_module` (module scope)
  - 只在模块开始时创建表，结束时删除表
- 添加 `cleanup_data` (function scope, autouse=True)
  - 每个测试后只清理数据，保留表结构
- 所有fixtures改为 function scope
  - 确保每个测试独立创建所需数据

**关键改动**:
```python
@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """模块级别的数据库设置"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function", autouse=True)
def cleanup_data():
    """每个测试后清理数据，但不删除表结构"""
    yield
    db = TestingSessionLocal()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()
```

### 2. tests/test_api_corpus.py ✅
**问题**: `setup_database` fixture 的 `autouse=True` 在每个测试后删除表，导致 "no such table: corpus" 错误

**修复方案**:
- 将 `setup_database` 改为 `setup_database_class` (class scope)
  - 为 TestCorpusAPI 类设置，只在类开始和结束时操作表结构
- 添加 `clean_database` (function scope)
  - 每个测试前清理数据，但保留表结构
- 更新所有测试方法使用 `clean_database` 而不是 `setup_database`

**关键改动**:
```python
@pytest.fixture(scope="class", autouse=True)
def setup_database_class():
    """类级别的数据库设置"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def clean_database():
    """每个测试前清理数据"""
    db = TestingSessionLocal()
    try:
        db.query(Image).delete()
        db.query(Corpus).delete()
        db.commit()
    finally:
        db.close()
    yield
```

## 待修复的测试

### 3. test_review_api.py ⚠️
**当前状态**: 使用 module scope fixtures，数据在整个模块中共享

**潜在问题**: 
- 如果某个测试修改了共享数据，可能影响其他测试
- 测试顺序依赖可能导致不稳定

**建议修复** (如果测试仍然失败):
- 检查是否有测试修改了共享的 fixture 数据
- 考虑将修改数据的测试改为使用独立的 fixture
- 或者将所有 fixtures 改为 function scope

## 修复原则总结

### 数据库Fixture的最佳实践

1. **表结构管理** (module/class scope):
   ```python
   @pytest.fixture(scope="module", autouse=True)
   def setup_module():
       Base.metadata.create_all(bind=engine)
       yield
       Base.metadata.drop_all(bind=engine)
   ```

2. **数据清理** (function scope):
   ```python
   @pytest.fixture(scope="function", autouse=True)
   def cleanup_data():
       yield
       # 清理数据但保留表结构
       db.query(Model).delete()
       db.commit()
   ```

3. **测试数据** (function scope):
   ```python
   @pytest.fixture(scope="function")
   def test_data():
       # 创建测试所需的数据
       yield data
       # 不需要清理，autouse的cleanup会处理
   ```

### 关键点

- ✅ 表结构操作应该在 module/class 级别
- ✅ 数据清理应该在 function 级别
- ✅ 测试数据应该在 function 级别创建
- ✅ 使用 `yield` 而不是 `return` 在 fixtures 中
- ✅ 每个测试应该独立，不依赖其他测试的数据
- ❌ 避免在 function scope 中删除表结构
- ❌ 避免在 module scope 中创建会被修改的数据

## 预期结果

修复后，测试应该：
- 每个测试独立运行
- 测试顺序不影响结果
- 数据库状态在测试间正确隔离
- 所有测试都能通过

## 下一步

1. 运行测试验证修复: `pytest backend/test_users_api.py -v`
2. 运行测试验证修复: `pytest backend/tests/test_api_corpus.py -v`
3. 检查 test_review_api.py 是否需要修复
4. 运行完整测试套件: `pytest backend -v`
