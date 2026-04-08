"""
数据集任务列表API向后兼容性测试
测试增强后的 GET /api/v1/datasets/{dataset_id}/tasks API 的向后兼容性

Requirements: 11.1, 11.3
- 测试管理员行为与修改前一致
- 测试响应格式不变
- 测试分页和筛选功能正常
"""
import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from services.task_query_service import TaskQueryService
from services.dataset_assignment_service import DatasetAssignmentService
from models.db_models import User, Corpus, Dataset, AnnotationTask, DatasetCorpus, DatasetAssignment

# 创建测试数据库
import os
test_db_dir = os.path.join(os.path.dirname(__file__), '..', 'test_artifacts', 'databases')
os.makedirs(test_db_dir, exist_ok=True)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(test_db_dir, 'test_backward_compatibility.db')}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db():
    """创建测试数据库会话"""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def task_query_service(db):
    """创建任务查询服务实例"""
    return TaskQueryService(db)


@pytest.fixture(scope="module")
def assignment_service(db):
    """创建分配服务实例"""
    return DatasetAssignmentService(db)


@pytest.fixture(scope="module")
def setup_test_data(db, assignment_service):
    """设置测试数据"""
    # 创建管理员用户
    admin = User(
        username="admin_user",
        password_hash="hashed_password",
        role="admin"
    )
    db.add(admin)
    db.flush()
    
    # 创建标注员用户
    annotator = User(
        username="annotator_user",
        password_hash="hashed_password",
        role="annotator"
    )
    db.add(annotator)
    db.flush()
    
    # 创建浏览员用户
    viewer = User(
        username="viewer_user",
        password_hash="hashed_password",
        role="viewer"
    )
    db.add(viewer)
    db.flush()
    
    # 创建测试数据集
    dataset = Dataset(
        dataset_id="test-dataset-bc",
        name="Backward Compatibility Test Dataset",
        description="Dataset for backward compatibility testing",
        created_by=admin.id
    )
    db.add(dataset)
    db.flush()
    
    # 创建30个语料和任务（用于测试分页）
    for i in range(30):
        corpus = Corpus(
            text_id=f"bc-corpus-{i+1:03d}",
            text=f"Backward compatibility test corpus {i+1}",
            text_type="test",
            source_file="test.xlsx",
            source_row=i+1,
            source_field="test"
        )
        db.add(corpus)
        db.flush()
        
        # 关联语料到数据集
        dc = DatasetCorpus(
            dataset_id=dataset.id,
            corpus_id=corpus.id
        )
        db.add(dc)
        
        # 创建任务
        # 前10个任务状态为pending，中间10个为processing，后10个为completed
        if i < 10:
            status = 'pending'
        elif i < 20:
            status = 'processing'
        else:
            status = 'completed'
        
        task = AnnotationTask(
            task_id=f"bc-task-{i+1:03d}",
            dataset_id=dataset.id,
            corpus_id=corpus.id,
            status=status,
            annotation_type='automatic',
            current_version=1
        )
        db.add(task)
    
    db.commit()
    
    # 刷新对象以获取ID
    db.refresh(dataset)
    db.refresh(admin)
    db.refresh(annotator)
    db.refresh(viewer)
    
    # 返回测试数据
    return {
        'dataset': dataset,
        'admin': admin,
        'annotator': annotator,
        'viewer': viewer
    }


class TestBackwardCompatibility:
    """向后兼容性测试套件"""
    
    def test_admin_sees_all_tasks(self, task_query_service, setup_test_data):
        """
        测试管理员看到所有任务（与修改前行为一致）
        
        管理员应该能够看到数据集中的所有30个任务
        
        Requirements: 11.3
        """
        admin = setup_test_data['admin']
        dataset = setup_test_data['dataset']
        
        tasks, total = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            page=1,
            page_size=100
        )
        
        # 管理员应该看到所有30个任务
        assert total == 30
        assert len(tasks) == 30
    
    def test_pagination_works_correctly(self, task_query_service, setup_test_data):
        """
        测试分页功能正常工作
        
        验证：
        - 第一页返回正确数量的任务
        - 第二页返回正确数量的任务
        - 总数正确
        - 页码正确
        
        Requirements: 11.1, 11.3
        """
        admin = setup_test_data['admin']
        dataset = setup_test_data['dataset']
        
        # 请求第一页（每页20条）
        tasks_page1, total_page1 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            page=1,
            page_size=20
        )
        
        # 验证第一页
        assert total_page1 == 30
        assert len(tasks_page1) == 20
        
        # 请求第二页
        tasks_page2, total_page2 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            page=2,
            page_size=20
        )
        
        # 验证第二页
        assert total_page2 == 30
        assert len(tasks_page2) == 10  # 剩余10个任务
        
        # 验证两页的任务不重复
        page1_task_ids = {task.id for task in tasks_page1}
        page2_task_ids = {task.id for task in tasks_page2}
        assert len(page1_task_ids & page2_task_ids) == 0, "Pages should not have overlapping tasks"
    
    def test_status_filter_works(self, task_query_service, setup_test_data):
        """
        测试状态筛选功能正常工作
        
        验证：
        - 筛选pending状态返回10个任务
        - 筛选processing状态返回10个任务
        - 筛选completed状态返回10个任务
        - 所有返回的任务状态正确
        
        Requirements: 11.1, 11.3
        """
        admin = setup_test_data['admin']
        dataset = setup_test_data['dataset']
        
        # 测试pending筛选
        tasks_pending, total_pending = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            status='pending'
        )
        
        assert total_pending == 10
        assert all(task.status == "pending" for task in tasks_pending)
        
        # 测试processing筛选
        tasks_processing, total_processing = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            status='processing'
        )
        
        assert total_processing == 10
        assert all(task.status == "processing" for task in tasks_processing)
        
        # 测试completed筛选
        tasks_completed, total_completed = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            status='completed'
        )
        
        assert total_completed == 10
        assert all(task.status == "completed" for task in tasks_completed)
    
    def test_pagination_with_filter(self, task_query_service, setup_test_data):
        """
        测试分页和筛选组合使用
        
        验证分页和状态筛选可以同时工作
        
        Requirements: 11.1, 11.3
        """
        admin = setup_test_data['admin']
        dataset = setup_test_data['dataset']
        
        # 筛选pending状态，每页5条
        tasks_page1, total_page1 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            status='pending',
            page=1,
            page_size=5
        )
        
        assert total_page1 == 10
        assert len(tasks_page1) == 5
        assert all(task.status == "pending" for task in tasks_page1)
        
        # 第二页
        tasks_page2, total_page2 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            status='pending',
            page=2,
            page_size=5
        )
        
        assert total_page2 == 10
        assert len(tasks_page2) == 5
        assert all(task.status == "pending" for task in tasks_page2)
        
        # 验证两页不重复
        page1_ids = {task.id for task in tasks_page1}
        page2_ids = {task.id for task in tasks_page2}
        assert len(page1_ids & page2_ids) == 0
    
    def test_default_pagination_values(self, task_query_service, setup_test_data):
        """
        测试默认分页参数
        
        验证不传递分页参数时使用默认值（page=1, page_size=20）
        
        Requirements: 11.1
        """
        admin = setup_test_data['admin']
        dataset = setup_test_data['dataset']
        
        tasks, total = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id
        )
        
        # 验证使用默认分页参数（默认page_size=20）
        assert total == 30
        assert len(tasks) == 20  # 第一页20条
    
    def test_admin_behavior_consistency(self, task_query_service, setup_test_data):
        """
        测试管理员行为一致性
        
        验证管理员在增强前后的行为完全一致：
        - 可以看到所有任务
        - 可以使用所有筛选功能
        - 返回正确的任务数据
        
        Requirements: 11.3
        """
        admin = setup_test_data['admin']
        dataset = setup_test_data['dataset']
        
        # 测试1: 获取所有任务
        tasks_all, total_all = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            page_size=100
        )
        assert total_all == 30
        assert len(tasks_all) == 30
        
        # 测试2: 使用状态筛选
        tasks_filtered, total_filtered = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            status='completed'
        )
        assert total_filtered == 10
        
        # 测试3: 使用分页
        tasks_paged, total_paged = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            page=1,
            page_size=10
        )
        assert total_paged == 30
        assert len(tasks_paged) == 10
        
        # 测试4: 验证返回的任务对象包含必要字段
        for task in tasks_all[:5]:  # 检查前5个任务
            assert hasattr(task, 'id')
            assert hasattr(task, 'task_id')
            assert hasattr(task, 'corpus_id')
            assert hasattr(task, 'status')
            assert hasattr(task, 'annotation_type')
            assert hasattr(task, 'current_version')
            assert hasattr(task, 'created_at')
            assert hasattr(task, 'updated_at')
    
    def test_empty_result_handling(self, task_query_service, setup_test_data):
        """
        测试空结果的处理
        
        验证当筛选条件导致没有结果时，返回空列表和0总数
        
        Requirements: 11.1
        """
        admin = setup_test_data['admin']
        dataset = setup_test_data['dataset']
        
        # 使用不存在的状态筛选
        tasks, total = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            status='nonexistent'
        )
        
        assert total == 0
        assert tasks == []
    
    def test_sorting_consistency(self, task_query_service, setup_test_data):
        """
        测试排序一致性
        
        验证默认排序（按created_at降序）保持一致
        
        Requirements: 11.1, 11.3
        """
        admin = setup_test_data['admin']
        dataset = setup_test_data['dataset']
        
        # 获取任务列表（默认排序）
        tasks, total = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            page_size=30
        )
        
        assert len(tasks) == 30
        
        # 验证排序（默认按created_at降序）
        for i in range(len(tasks) - 1):
            assert tasks[i].created_at >= tasks[i+1].created_at
    
    def test_task_data_integrity(self, task_query_service, setup_test_data):
        """
        测试任务数据完整性
        
        验证返回的任务数据完整且正确
        
        Requirements: 11.1
        """
        admin = setup_test_data['admin']
        dataset = setup_test_data['dataset']
        
        tasks, total = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset.id,
            page=1,
            page_size=5
        )
        
        assert len(tasks) == 5
        
        for task in tasks:
            # 验证任务属于正确的数据集
            assert task.dataset_id == dataset.id
            
            # 验证任务ID格式正确
            assert task.task_id.startswith('bc-task-')
            
            # 验证状态是有效值
            assert task.status in ['pending', 'processing', 'completed', 'failed']
            
            # 验证标注类型
            assert task.annotation_type in ['automatic', 'manual']
            
            # 验证版本号
            assert task.current_version >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
