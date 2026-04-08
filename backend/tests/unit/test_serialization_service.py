"""
序列化服务测试（简化版）
测试基本的序列化和反序列化功能
"""
import sys
from pathlib import Path
import pytest

# 添加backend目录到Python路径
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

from database import Base
from models.db_models import (
    AnnotationTask,
    TextEntity,
    ImageEntity,
    Relation,
    Dataset,
    Corpus,
    Image
)
from services.serialization_service import SerializationService


@pytest.fixture(scope="module")
def db():
    """创建测试数据库 fixture"""
    TEST_DATABASE_URL = "sqlite:///./tests/test_artifacts/databases/test_serialization.db"
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def service(db):
    """创建 SerializationService fixture"""
    return SerializationService(db)


@pytest.fixture(scope="function")
def test_data(db):
    """创建测试数据 fixture - 每个测试函数独立创建"""
    # 创建语料
    corpus = Corpus(
        text_id=f"TEXT_{id(db)}",  # 使用唯一ID避免冲突
        text="2022年02月21日，捷普产线反馈CB760-60038产品排线连锡10pcs。",
        text_type="问题描述",
        source_file="test.xlsx"
    )
    db.add(corpus)
    db.commit()
    db.refresh(corpus)
    
    # 创建图片记录
    image1 = Image(
        image_id=f"IMG_{id(db)}_1",
        corpus_id=corpus.id,
        file_path="/test/img1.png",
        original_name="img1.png"
    )
    image2 = Image(
        image_id=f"IMG_{id(db)}_2",
        corpus_id=corpus.id,
        file_path="/test/img2.png",
        original_name="img2.png"
    )
    db.add_all([image1, image2])
    db.commit()
    db.refresh(image1)
    db.refresh(image2)
    
    # 创建数据集
    dataset = Dataset(
        dataset_id=f"DS_{id(db)}",
        name="测试数据集",
        created_by=1
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    
    # 创建标注任务
    task = AnnotationTask(
        task_id=f"TASK_{id(db)}",
        dataset_id=dataset.id,
        corpus_id=corpus.id,
        status="completed"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # 创建文本实体
    entities = [
        TextEntity(
            task_id=task.id,
            entity_id=0,
            version=1,
            token="2022年02月21日",
            label="日期时间",
            start_offset=0,
            end_offset=12
        ),
        TextEntity(
            task_id=task.id,
            entity_id=1,
            version=1,
            token="捷普",
            label="客户名称",
            start_offset=13,
            end_offset=15
        ),
        TextEntity(
            task_id=task.id,
            entity_id=2,
            version=1,
            token="CB760-60038",
            label="产品型号",
            start_offset=19,
            end_offset=30
        )
    ]
    db.add_all(entities)
    db.commit()
    
    for entity in entities:
        db.refresh(entity)
    
    # 创建图片实体
    image_entity_whole = ImageEntity(
        task_id=task.id,
        entity_id=100,
        version=1,
        image_id=image1.id,
        label="缺陷图片",
        bbox_x=None,
        bbox_y=None,
        bbox_width=None,
        bbox_height=None
    )
    image_entity_region = ImageEntity(
        task_id=task.id,
        entity_id=101,
        version=1,
        image_id=image2.id,
        label="缺陷区域",
        bbox_x=10,
        bbox_y=20,
        bbox_width=100,
        bbox_height=80
    )
    db.add_all([image_entity_whole, image_entity_region])
    db.commit()
    db.refresh(image_entity_whole)
    db.refresh(image_entity_region)
    
    # 创建关系
    relation = Relation(
        task_id=task.id,
        relation_id=0,
        version=1,
        from_entity_id=entities[1].entity_id,
        to_entity_id=entities[2].entity_id,
        relation_type="relates_to"
    )
    db.add(relation)
    db.commit()
    db.refresh(relation)
    
    yield {
        'task': task,
        'entities': entities,
        'image_entities': [image_entity_whole, image_entity_region],
        'relations': [relation]
    }
    
    # 清理测试数据
    db.query(Relation).filter(Relation.task_id == task.id).delete()
    db.query(ImageEntity).filter(ImageEntity.task_id == task.id).delete()
    db.query(TextEntity).filter(TextEntity.task_id == task.id).delete()
    db.query(AnnotationTask).filter(AnnotationTask.id == task.id).delete()
    db.query(Image).filter(Image.corpus_id == corpus.id).delete()
    db.query(Dataset).filter(Dataset.id == dataset.id).delete()
    db.query(Corpus).filter(Corpus.id == corpus.id).delete()
    db.commit()


def test_serialize_text_entity(service, test_data):
    """测试1: 序列化文本实体"""
    entities = test_data['entities']
    
    # 序列化第一个实体
    entity = entities[0]
    serialized = service.serialize_text_entity(entity)
    
    # 验证字段
    assert "id" in serialized
    assert "start_offset" in serialized
    assert "end_offset" in serialized
    assert "label" in serialized
    assert serialized["label"] == "日期时间"


def test_serialize_image_entities(service, test_data):
    """测试2: 序列化图片实体（整图和区域）"""
    image_entities = test_data['image_entities']
    
    # 序列化整图实体
    whole_image = image_entities[0]
    serialized_whole = service.serialize_image_entity(whole_image)
    
    assert serialized_whole["bbox"] is None
    
    # 序列化区域实体
    region_image = image_entities[1]
    serialized_region = service.serialize_image_entity(region_image)
    
    assert serialized_region["bbox"] is not None
    assert "x" in serialized_region["bbox"]
    assert "y" in serialized_region["bbox"]
    assert "width" in serialized_region["bbox"]
    assert "height" in serialized_region["bbox"]


def test_serialize_relation(service, test_data):
    """测试3: 序列化关系"""
    relations = test_data['relations']
    
    # 序列化关系
    relation = relations[0]
    serialized = service.serialize_relation(relation)
    
    # 验证字段
    assert "from_id" in serialized
    assert "to_id" in serialized
    assert "type" in serialized
    assert serialized["type"] == "relates_to"


def test_serialize_complete_task(service, test_data):
    """测试4: 序列化完整标注任务"""
    task = test_data['task']
    
    # 序列化完整任务
    serialized = service.serialize_annotation_task(task, include_metadata=True)
    
    # 验证结构
    assert "text" in serialized
    assert "text_type" in serialized
    assert "entities" in serialized
    assert "images" in serialized
    assert "relations" in serialized
    assert "task_id" in serialized
    
    # 验证数据
    assert len(serialized['entities']) == 3
    assert len(serialized['images']) == 2
    assert len(serialized['relations']) == 1


def test_round_trip(service, test_data):
    """测试5: 往返一致性测试"""
    task = test_data['task']
    
    # 序列化
    serialized = service.serialize_annotation_task(task, include_metadata=False)
    
    # 反序列化
    deserialized = service.deserialize_annotation_task(
        serialized,
        task.id,
        create_entities=False
    )
    
    # 验证数据一致性
    assert len(deserialized["text_entities"]) == len(serialized["entities"])
    assert len(deserialized["image_entities"]) == len(serialized["images"])
    assert len(deserialized["relations"]) == len(serialized["relations"])


def test_validate_data():
    """测试6: 数据格式验证"""
    # 有效数据
    valid_data = {
        "text": "测试文本",
        "entities": [
            {"id": 1, "start_offset": 0, "end_offset": 4, "label": "测试"}
        ],
        "images": [
            {"id": 100, "image_path": "img.png", "label": "图片", "bbox": None}
        ],
        "relations": [
            {"from_id": 1, "to_id": 100, "type": "relates_to"}
        ]
    }
    
    result = SerializationService.validate_serialized_data(valid_data)
    assert result is True
    
    # 无效数据（缺少字段）
    invalid_data = {
        "text": "测试文本",
        "entities": []
        # 缺少relations字段
    }
    
    result = SerializationService.validate_serialized_data(invalid_data)
    assert result is False
