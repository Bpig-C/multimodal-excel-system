"""
数据导出服务测试脚本
测试数据导出的核心功能
"""
import sys
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base
from models.db_models import (
    User, Corpus, Image, Dataset, AnnotationTask, 
    TextEntity, ImageEntity, Relation
)
from services.export_service import ExportService


@pytest.fixture(scope="module")
def db():
    """创建测试数据库 fixture"""
    engine = create_engine('sqlite:///./tests/test_artifacts/databases/test_export_service.db', echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def service(db):
    """创建 ExportService fixture"""
    return ExportService(db)


@pytest.fixture(scope="module")
def dataset(db):
    """创建测试数据集 fixture"""
    # 创建用户
    user = User(
        username="test_user",
        password_hash="hash123",
        role="admin"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 创建语料
    corpus1 = Corpus(
        text_id="CORP_001",
        text="2022年02月21日，捷普产线反馈CB760-60038产品排线连锡10pcs。",
        text_type="问题描述",
        source_file="test.xlsx",
        source_row=1,
        source_field="问题描述",
        has_images=True
    )
    corpus2 = Corpus(
        text_id="CORP_002",
        text="客户反馈产品质量问题。",
        text_type="原因分析",
        source_file="test.xlsx",
        source_row=2,
        source_field="原因分析",
        has_images=False
    )
    db.add_all([corpus1, corpus2])
    db.commit()
    db.refresh(corpus1)
    db.refresh(corpus2)
    
    # 创建数据集
    dataset = Dataset(
        dataset_id="DS_001",
        name="测试数据集",
        description="用于测试导出功能",
        created_by=user.id
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    
    # 创建标注任务
    task1 = AnnotationTask(
        task_id="TASK_001",
        dataset_id=dataset.id,
        corpus_id=corpus1.id,
        status='completed',
        annotation_type='manual',
        assigned_to=user.id
    )
    task2 = AnnotationTask(
        task_id="TASK_002",
        dataset_id=dataset.id,
        corpus_id=corpus2.id,
        status='approved',
        annotation_type='manual',
        assigned_to=user.id
    )
    db.add_all([task1, task2])
    db.commit()
    db.refresh(task1)
    db.refresh(task2)
    
    # 添加实体到 task1
    entity1 = TextEntity(
        entity_id=0,
        task_id=task1.id,
        version=1,
        token="2022年02月21日",
        label="日期时间",
        start_offset=0,
        end_offset=12
    )
    entity2 = TextEntity(
        entity_id=1,
        task_id=task1.id,
        version=1,
        token="捷普",
        label="客户名称",
        start_offset=13,
        end_offset=15
    )
    db.add_all([entity1, entity2])
    db.commit()
    
    # 添加关系
    relation = Relation(
        relation_id=0,
        task_id=task1.id,
        version=1,
        from_entity_id=0,
        to_entity_id=1,
        relation_type="relates_to"
    )
    db.add(relation)
    db.commit()
    
    return dataset


def test_export_all_data(service, dataset):
    """测试导出所有数据"""
    result = service.export_dataset(dataset.id)
    
    assert 'total_count' in result
    assert 'all_data' in result
    assert result['total_count'] >= 0
    
    # 验证数据格式
    if result['all_data']:
        first_record = result['all_data'][0]
        assert 'text' in first_record
        assert 'text_type' in first_record
        assert 'entities' in first_record
        assert 'relations' in first_record
        assert 'images' in first_record


def test_export_with_status_filter(service, dataset):
    """测试按状态筛选导出"""
    # 只导出已批准的任务
    result = service.export_dataset(
        dataset.id,
        status_filter=['approved']
    )
    
    assert 'total_count' in result
    assert result['total_count'] >= 0


def test_export_with_text_type_filter(service, dataset):
    """测试按句子分类筛选导出"""
    # 只导出"问题描述"类型
    result = service.export_dataset(
        dataset.id,
        text_type_filter=['问题描述']
    )
    
    assert 'total_count' in result
    
    # 验证所有记录都是指定类型
    for record in result['all_data']:
        assert record['text_type'] == '问题描述'


def test_train_test_split(service, dataset):
    """测试训练集/测试集划分"""
    # 80%训练集，20%测试集
    result = service.export_dataset(
        dataset.id,
        train_test_split=0.8,
        random_seed=42
    )
    
    assert 'total_count' in result
    assert 'train_count' in result
    assert 'test_count' in result
    
    # 验证划分
    assert result['train_count'] + result['test_count'] == result['total_count']


def test_export_to_jsonl(service, dataset):
    """测试导出为JSONL文件"""
    # 导出数据
    result = service.export_dataset(dataset.id)
    
    # 写入文件
    output_path = "test_export.jsonl"
    service.export_to_jsonl(result['all_data'], output_path)
    
    # 验证文件
    assert os.path.exists(output_path)
    
    with open(output_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 验证每行都是有效的JSON
    for line in lines:
        json.loads(line)
    
    # 清理测试文件
    os.remove(output_path)


def test_export_statistics(service, dataset):
    """测试导出统计"""
    stats = service.get_export_statistics(dataset.id)
    
    assert 'total_tasks' in stats
    assert 'total_entities' in stats
    assert 'total_relations' in stats
    assert 'total_images' in stats
    assert 'average_entities_per_task' in stats
    assert 'average_relations_per_task' in stats
    assert 'text_type_distribution' in stats


def test_data_format(service, dataset):
    """测试导出数据格式"""
    result = service.export_dataset(dataset.id)
    
    if not result['all_data']:
        return  # 没有数据可验证
    
    record = result['all_data'][0]
    
    # 验证必需字段
    required_fields = ['text', 'text_type', 'entities', 'relations', 'images', 'image_relations']
    for field in required_fields:
        assert field in record, f"缺少必需字段: {field}"
    
    # 验证实体格式
    if record['entities']:
        entity = record['entities'][0]
        entity_fields = ['id', 'start_offset', 'end_offset', 'label']
        for field in entity_fields:
            assert field in entity, f"实体缺少字段: {field}"
    
    # 验证关系格式
    if record['relations']:
        relation = record['relations'][0]
        relation_fields = ['from_id', 'to_id', 'type']
        for field in relation_fields:
            assert field in relation, f"关系缺少字段: {field}"
    
    # 验证图片格式
    if record['images']:
        image = record['images'][0]
        image_fields = ['id', 'image_path', 'label', 'bbox']
        for field in image_fields:
            assert field in image, f"图片缺少字段: {field}"
