"""
语料管理API测试
测试语料上传、查询、删除等功能
"""
import sys
from pathlib import Path

# 添加backend目录到Python路径
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import shutil

from main import app
from database import Base, get_db
from models.db_models import Corpus, Image
from config import settings

# 创建测试数据库 - 保存到test_artifacts目录
TEST_DATABASE_URL = "sqlite:///./tests/test_artifacts/databases/test_corpus_api.db"
engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # 使用静态连接池确保所有连接使用同一个数据库
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """覆盖数据库依赖"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    app.dependency_overrides[get_db] = override_get_db
    """模块级别的数据库设置"""
    # 确保先删除旧表
    Base.metadata.drop_all(bind=engine)
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    yield
    # 测试结束后清理
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def clean_database():
    """每个测试前清理数据"""
    db = TestingSessionLocal()
    try:
        # 清理数据但保留表结构
        db.query(Image).delete()
        db.query(Corpus).delete()
        db.commit()
    finally:
        db.close()
    yield


@pytest.fixture(scope="function")
def sample_corpus(clean_database):
    """创建示例语料 - 使用function scope确保每个测试都有新数据"""
    db = TestingSessionLocal()
    try:
        corpus = Corpus(
            text_id="test_corpus_001",
            text="这是一个测试语料",
            text_type="问题描述",
            source_file="test.xlsx",
            source_row=1,
            source_field="问题描述",
            has_images=False
        )
        db.add(corpus)
        db.commit()
        db.refresh(corpus)
        corpus_id = corpus.id
        text_id = corpus.text_id
    finally:
        db.close()
    
    # 返回数据后，数据已经在数据库中
    yield {"id": corpus_id, "text_id": text_id}


@pytest.fixture(scope="function")
def sample_corpus_with_images(clean_database):
    """创建带图片的示例语料 - 使用function scope确保每个测试都有新数据"""
    db = TestingSessionLocal()
    try:
        corpus = Corpus(
            text_id="test_corpus_002",
            text="这是一个带图片的测试语料",
            text_type="原因分析",
            source_file="test.xlsx",
            source_row=2,
            source_field="原因分析",
            has_images=True
        )
        db.add(corpus)
        db.commit()
        db.refresh(corpus)
        
        corpus_id = corpus.id
        text_id = corpus.text_id
        
        # 添加图片
        image = Image(
            image_id="test_image_001",
            corpus_id=corpus_id,
            file_path="imgs/test_image_001.png",
            original_name="test.png",
            width=800,
            height=600
        )
        db.add(image)
        db.commit()
    finally:
        db.close()
    
    # 返回数据后，数据已经在数据库中
    yield {"id": corpus_id, "text_id": text_id}


class TestCorpusAPI:
    """语料管理API测试类"""
    
    def test_get_corpus_list_empty(self, clean_database):
        """测试获取空语料列表"""
        response = client.get("/api/v1/corpus")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["items"]) == 0
    
    def test_get_corpus_list_with_data(self, sample_corpus):
        """测试获取语料列表"""
        response = client.get("/api/v1/corpus")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["text_id"] == "test_corpus_001"
        assert data["items"][0]["text"] == "这是一个测试语料"
        assert data["items"][0]["text_type"] == "问题描述"
    
    def test_get_corpus_list_pagination(self, clean_database):
        """测试分页功能"""
        db = TestingSessionLocal()
        try:
            # 创建多个语料
            for i in range(25):
                corpus = Corpus(
                    text_id=f"test_corpus_{i:03d}",
                    text=f"测试语料 {i}",
                    text_type="问题描述",
                    source_file="test.xlsx",
                    source_row=i,
                    source_field="问题描述",
                    has_images=False
                )
                db.add(corpus)
            db.commit()
        finally:
            db.close()
        
        # 测试第一页
        response = client.get("/api/v1/corpus?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 25
        assert len(data["items"]) == 10
        
        # 测试第二页
        response = client.get("/api/v1/corpus?page=2&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 25
        assert len(data["items"]) == 10
        
        # 测试第三页
        response = client.get("/api/v1/corpus?page=3&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 25
        assert len(data["items"]) == 5
    
    def test_get_corpus_list_filter_by_field(self, clean_database):
        """测试按字段筛选"""
        db = TestingSessionLocal()
        try:
            # 创建不同字段的语料
            corpus1 = Corpus(
                text_id="test_corpus_001",
                text="问题描述内容",
                text_type="问题描述",
                source_field="问题描述",
                has_images=False
            )
            corpus2 = Corpus(
                text_id="test_corpus_002",
                text="原因分析内容",
                text_type="原因分析",
                source_field="原因分析",
                has_images=False
            )
            db.add_all([corpus1, corpus2])
            db.commit()
        finally:
            db.close()
        
        # 筛选问题描述
        response = client.get("/api/v1/corpus?source_field=问题描述")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["source_field"] == "问题描述"
        
        # 筛选原因分析
        response = client.get("/api/v1/corpus?source_field=原因分析")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["source_field"] == "原因分析"
    
    def test_get_corpus_list_filter_by_images(self, sample_corpus, sample_corpus_with_images):
        """测试按是否包含图片筛选"""
        # 筛选包含图片的语料
        response = client.get("/api/v1/corpus?has_images=true")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["has_images"] is True
        
        # 筛选不包含图片的语料
        response = client.get("/api/v1/corpus?has_images=false")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["has_images"] is False
    
    def test_get_corpus_detail(self, sample_corpus):
        """测试获取语料详情"""
        response = client.get("/api/v1/corpus/test_corpus_001")
        assert response.status_code == 200
        data = response.json()
        assert data["text_id"] == "test_corpus_001"
        assert data["text"] == "这是一个测试语料"
        assert data["text_type"] == "问题描述"
        assert data["has_images"] is False
        assert len(data["images"]) == 0
    
    def test_get_corpus_detail_with_images(self, sample_corpus_with_images):
        """测试获取带图片的语料详情"""
        response = client.get("/api/v1/corpus/test_corpus_002")
        assert response.status_code == 200
        data = response.json()
        assert data["text_id"] == "test_corpus_002"
        assert data["has_images"] is True
        assert len(data["images"]) == 1
        assert data["images"][0]["image_id"] == "test_image_001"
        assert data["images"][0]["file_path"] == "imgs/test_image_001.png"
    
    def test_get_corpus_detail_not_found(self, clean_database):
        """测试获取不存在的语料"""
        response = client.get("/api/v1/corpus/nonexistent")
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
    
    def test_delete_corpus(self, sample_corpus):
        """测试删除语料"""
        response = client.delete("/api/v1/corpus/test_corpus_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "成功删除" in data["message"]
        
        # 验证语料已被删除
        response = client.get("/api/v1/corpus/test_corpus_001")
        assert response.status_code == 404
    
    def test_delete_corpus_with_images(self, sample_corpus_with_images):
        """测试删除带图片的语料（级联删除）"""
        # 先验证图片存在
        db = TestingSessionLocal()
        try:
            corpus_id = sample_corpus_with_images["id"]
            images_count = db.query(Image).filter(Image.corpus_id == corpus_id).count()
            assert images_count == 1
        finally:
            db.close()
        
        # 删除语料
        response = client.delete("/api/v1/corpus/test_corpus_002")
        assert response.status_code == 200
        
        # 验证图片记录也被删除
        db = TestingSessionLocal()
        try:
            images_count = db.query(Image).count()
            assert images_count == 0
        finally:
            db.close()
    
    def test_delete_corpus_not_found(self, clean_database):
        """测试删除不存在的语料"""
        response = client.delete("/api/v1/corpus/nonexistent")
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
    
    def test_get_corpus_images(self, sample_corpus_with_images):
        """测试获取语料关联图片"""
        response = client.get("/api/v1/corpus/test_corpus_002/images")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["image_id"] == "test_image_001"
        assert data[0]["file_path"] == "imgs/test_image_001.png"
        assert data[0]["width"] == 800
        assert data[0]["height"] == 600
    
    def test_get_corpus_images_empty(self, sample_corpus):
        """测试获取无图片语料的图片列表"""
        response = client.get("/api/v1/corpus/test_corpus_001/images")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    def test_get_corpus_images_not_found(self, clean_database):
        """测试获取不存在语料的图片"""
        response = client.get("/api/v1/corpus/nonexistent/images")
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]


# 清理测试数据库文件
def teardown_module(module):
    """清理测试数据库"""
    # 关闭所有连接
    engine.dispose()
    # 等待一下确保文件被释放
    import time
    time.sleep(0.5)
    # 删除测试数据库
    db_path = Path("./tests/test_artifacts/databases/test_corpus_api.db")
    if db_path.exists():
        try:
            db_path.unlink()
        except PermissionError:
            # 如果文件被占用，忽略错误
            pass
