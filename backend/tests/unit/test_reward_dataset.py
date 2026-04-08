"""
Reward数据集生成服务测试
测试LLM自动标注与人工修正差异的记录功能
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
    Dataset, AnnotationTask, TextEntity, Relation,
    Corpus, VersionHistory
)
from services.reward_dataset_service import RewardDatasetService


@pytest.fixture(scope="module")
def db():
    """创建测试数据库 fixture"""
    TEST_DATABASE_URL = "sqlite:///./tests/test_artifacts/databases/test_reward_dataset.db"
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
    """创建 RewardDatasetService fixture"""
    return RewardDatasetService(db)


@pytest.fixture(scope="function")
def test_data(db):
    """创建测试数据 fixture - 每个测试函数独立创建"""
    # 创建语料
    corpus = Corpus(
        text_id=f"TEXT_{id(db)}",
        text="2022年02月21日，捷普产线反馈CB760-60038产品排线连锡10pcs。",
        text_type="问题描述",
        source_file="test.xlsx"
    )
    db.add(corpus)
    db.commit()
    db.refresh(corpus)
    
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
        task_id="TASK_001",
        dataset_id=dataset.id,
        corpus_id=corpus.id,
        status="completed",
        annotation_type="manual",  # 已人工修正
        current_version=2  # 当前版本为2，表示有修正
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # 创建版本1（LLM自动标注）的实体
    llm_entities = [
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
            label="客户名称",  # LLM标注为"客户名称"
            start_offset=13,
            end_offset=15
        ),
        # LLM漏标了"产品型号"
    ]
    
    for entity in llm_entities:
        db.add(entity)
    
    # 创建版本1的关系（LLM没有标注关系）
    
    db.commit()
    
    # 创建版本1的快照
    version1_snapshot = {
        'version': 1,
        'task_info': {
            'task_id': task.task_id,
            'status': 'completed',
            'annotation_type': 'automatic'
        },
        'entities': [
            {
                'entity_id': 0,
                'token': '2022年02月21日',
                'label': '日期时间',
                'start_offset': 0,
                'end_offset': 12,
                'confidence': 0.95
            },
            {
                'entity_id': 1,
                'token': '捷普',
                'label': '客户名称',
                'start_offset': 13,
                'end_offset': 15,
                'confidence': 0.90
            }
        ],
        'image_entities': [],
        'relations': []
    }
    
    version1_history = VersionHistory(
        history_id="version-001",
        task_id=task.id,
        version=1,
        change_type='create',
        change_description='LLM自动标注',
        snapshot_data=json.dumps(version1_snapshot, ensure_ascii=False)
    )
    db.add(version1_history)
    db.commit()
    
    # 创建版本2（人工修正）的实体
    corrected_entities = [
        TextEntity(
            task_id=task.id,
            entity_id=0,
            version=2,
            token="2022年02月21日",
            label="日期时间",
            start_offset=0,
            end_offset=12
        ),
        TextEntity(
            task_id=task.id,
            entity_id=1,
            version=2,
            token="捷普",
            label="客户名称",  # 人工确认标签正确
            start_offset=13,
            end_offset=15
        ),
        TextEntity(
            task_id=task.id,
            entity_id=2,
            version=2,
            token="CB760-60038",
            label="产品型号",  # 人工新增
            start_offset=19,
            end_offset=30
        )
    ]
    
    for entity in corrected_entities:
        db.add(entity)
    
    # 创建版本2的关系（人工新增）
    relation = Relation(
        task_id=task.id,
        relation_id=0,
        version=2,
        from_entity_id=1,  # 捷普
        to_entity_id=2,    # CB760-60038
        relation_type="relates_to"
    )
    db.add(relation)
    
    db.commit()
    
    yield {'dataset': dataset, 'task': task}
    
    # Cleanup
    db.query(Relation).filter(Relation.task_id == task.id).delete()
    db.query(TextEntity).filter(TextEntity.task_id == task.id).delete()
    db.query(VersionHistory).filter(VersionHistory.task_id == task.id).delete()
    db.query(AnnotationTask).filter(AnnotationTask.id == task.id).delete()
    db.query(Dataset).filter(Dataset.id == dataset.id).delete()
    db.query(Corpus).filter(Corpus.id == corpus.id).delete()
    db.commit()


def test_filter_corrected_tasks(service, test_data):
    """测试1: 筛选存在人工修正的任务"""
    dataset = test_data['dataset']
    task = test_data['task']
    
    # 筛选修正任务
    corrected_tasks = service._filter_corrected_tasks(dataset.id)
    
    assert len(corrected_tasks) == 1
    assert corrected_tasks[0].task_id == task.task_id
    assert task.current_version == 2


def test_calculate_diff(service, test_data):
    """测试2: 计算标注差异"""
    task = test_data['task']
    
    # 获取原始和修正标注
    original = service._get_original_annotation(task)
    corrected = service._get_current_annotation(task)
    
    # 计算差异
    diff = service._calculate_diff(original, corrected)
    
    # 验证差异
    assert len(diff['entities']['added']) == 1  # 新增了"产品型号"
    assert len(diff['entities']['removed']) == 0
    assert len(diff['entities']['modified']) == 0
    assert len(diff['relations']['added']) == 1  # 新增了关系
    assert len(diff['relations']['removed']) == 0


def test_generate_reward_dataset(service, test_data):
    """测试3: 生成Reward数据集"""
    dataset = test_data['dataset']
    
    # 生成Reward数据集
    result = service.generate_reward_dataset(dataset.id)
    
    assert result['total_count'] == 1
    
    # 验证数据格式
    reward_data = result['reward_data']
    assert len(reward_data) == 1
    
    record = reward_data[0]
    assert 'task_id' in record
    assert 'text' in record
    assert 'original_annotation' in record
    assert 'corrected_annotation' in record
    assert 'diff' in record
    
    # 验证统计
    statistics = result['statistics']
    assert statistics['entity_added'] == 1
    assert statistics['relation_added'] == 1


def test_correction_frequency_report(service, test_data):
    """测试4: 修正频率报告"""
    dataset = test_data['dataset']
    
    # 获取修正频率报告
    report = service.get_correction_frequency_report(dataset.id)
    
    assert report['total_corrections'] == 2  # 1个实体 + 1个关系
    assert report['total_corrected_tasks'] == 1


def test_export_to_jsonl(service, test_data):
    """测试5: 导出JSONL文件"""
    import os
    dataset = test_data['dataset']
    
    # 生成并导出
    output_path = "test_reward_output.jsonl"
    result = service.generate_reward_dataset(dataset.id, output_path=output_path)
    
    # 验证文件
    assert os.path.exists(output_path)
    
    # 读取并验证内容
    with open(output_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    assert len(lines) == 1
    
    # 验证JSON格式
    record = json.loads(lines[0])
    assert 'original_annotation' in record
    assert 'corrected_annotation' in record
    assert 'diff' in record
    
    # 清理测试文件
    os.remove(output_path)
