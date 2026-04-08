"""
跨数据集任务列表API集成测试
测试 GET /api/v1/annotations 端点

Requirements: 1.1, 1.4, 1.5, 2.1, 2.6
- 测试管理员获取所有任务
- 测试标注员获取分配的任务
- 测试筛选功能
- 测试分页功能
- 测试排序功能
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
test_db_dir = os.path.join(os.path.dirname(__file__), '..', 'test_artifacts', 'databases')
os.makedirs(test_db_dir, exist_ok=True)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(test_db_dir, 'test_cross_dataset_api.db')}"
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
        username="admin_cross",
        password_hash="hashed_password",
        role="admin"
    )
    db.add(admin)
    db.flush()
    
    # 创建标注员用户
    annotator1 = User(
        username="annotator1_cross",
        password_hash="hashed_password",
        role="annotator"
    )
    db.add(annotator1)
    db.flush()
    
    annotator2 = User(
        username="annotator2_cross",
        password_hash="hashed_password",
        role="annotator"
    )
    db.add(annotator2)
    db.flush()
    
    # 创建浏览员用户
    viewer = User(
        username="viewer_cross",
        password_hash="hashed_password",
        role="viewer"
    )
    db.add(viewer)
    db.flush()
    
    # 创建两个测试数据集
    dataset1 = Dataset(
        dataset_id="cross-dataset-1",
        name="Cross Dataset Test 1",
        description="First dataset for cross-dataset testing",
        created_by=admin.id
    )
    db.add(dataset1)
    db.flush()
    
    dataset2 = Dataset(
        dataset_id="cross-dataset-2",
        name="Cross Dataset Test 2",
        description="Second dataset for cross-dataset testing",
        created_by=admin.id
    )
    db.add(dataset2)
    db.flush()
    
    # 为数据集1创建20个任务
    for i in range(20):
        corpus = Corpus(
            text_id=f"cross-corpus-1-{i+1:03d}",
            text=f"Cross dataset test corpus 1-{i+1}",
            text_type="test",
            source_file="test1.xlsx",
            source_row=i+1,
            source_field="test"
        )
        db.add(corpus)
        db.flush()
        
        dc = DatasetCorpus(
            dataset_id=dataset1.id,
            corpus_id=corpus.id
        )
        db.add(dc)
        
        # 前10个pending，后10个completed
        status = 'pending' if i < 10 else 'completed'
        
        task = AnnotationTask(
            task_id=f"cross-task-1-{i+1:03d}",
            dataset_id=dataset1.id,
            corpus_id=corpus.id,
            status=status,
            annotation_type='automatic',
            current_version=1
        )
        db.add(task)
    
    # 为数据集2创建15个任务
    for i in range(15):
        corpus = Corpus(
            text_id=f"cross-corpus-2-{i+1:03d}",
            text=f"Cross dataset test corpus 2-{i+1}",
            text_type="test",
            source_file="test2.xlsx",
            source_row=i+1,
            source_field="test"
        )
        db.add(corpus)
        db.flush()
        
        dc = DatasetCorpus(
            dataset_id=dataset2.id,
            corpus_id=corpus.id
        )
        db.add(dc)
        
        # 前5个pending，中间5个processing，后5个completed
        if i < 5:
            status = 'pending'
        elif i < 10:
            status = 'processing'
        else:
            status = 'completed'
        
        task = AnnotationTask(
            task_id=f"cross-task-2-{i+1:03d}",
            dataset_id=dataset2.id,
            corpus_id=corpus.id,
            status=status,
            annotation_type='automatic',
            current_version=1
        )
        db.add(task)
    
    db.commit()
    
    # 刷新对象
    db.refresh(dataset1)
    db.refresh(dataset2)
    db.refresh(admin)
    db.refresh(annotator1)
    db.refresh(annotator2)
    db.refresh(viewer)
    
    # 为annotator1分配dataset1的前10个任务（索引1-10）
    assignment1 = DatasetAssignment(
        dataset_id=dataset1.id,
        user_id=annotator1.id,
        role='annotator',
        task_start_index=1,
        task_end_index=10,
        is_active=True,
        assigned_by=admin.id
    )
    db.add(assignment1)
    
    # 为annotator2分配dataset2的所有任务（整体分配）
    assignment2 = DatasetAssignment(
        dataset_id=dataset2.id,
        user_id=annotator2.id,
        role='annotator',
        task_start_index=None,
        task_end_index=None,
        is_active=True,
        assigned_by=admin.id
    )
    db.add(assignment2)
    
    db.commit()
    
    return {
        'dataset1': dataset1,
        'dataset2': dataset2,
        'admin': admin,
        'annotator1': annotator1,
        'annotator2': annotator2,
        'viewer': viewer
    }


class TestCrossDatasetTasksAPI:
    """跨数据集任务列表API测试套件"""
    
    def test_admin_gets_all_tasks_across_datasets(self, task_query_service, setup_test_data):
        """
        测试管理员获取所有数据集的所有任务
        
        管理员应该能够看到所有数据集的所有任务（20 + 15 = 35个）
        
        Requirements: 1.1
        """
        admin = setup_test_data['admin']
        
        tasks, total = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            page=1,
            page_size=100
        )
        
        # 管理员应该看到所有35个任务
        assert total == 35
        assert len(tasks) == 35
        
        # 验证任务来自两个数据集
        dataset_ids = {task.dataset_id for task in tasks}
        assert len(dataset_ids) == 2
    
    def test_admin_filter_by_dataset(self, task_query_service, setup_test_data):
        """
        测试管理员按数据集筛选
        
        管理员应该能够筛选特定数据集的任务
        
        Requirements: 1.4
        """
        admin = setup_test_data['admin']
        dataset1 = setup_test_data['dataset1']
        dataset2 = setup_test_data['dataset2']
        
        # 筛选数据集1
        tasks1, total1 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset1.id,
            page_size=100
        )
        
        assert total1 == 20
        assert all(task.dataset_id == dataset1.id for task in tasks1)
        
        # 筛选数据集2
        tasks2, total2 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset2.id,
            page_size=100
        )
        
        assert total2 == 15
        assert all(task.dataset_id == dataset2.id for task in tasks2)
    
    def test_admin_filter_by_status(self, task_query_service, setup_test_data):
        """
        测试管理员按状态筛选
        
        验证管理员可以筛选特定状态的任务（跨数据集）
        
        Requirements: 1.4
        """
        admin = setup_test_data['admin']
        
        # 筛选pending状态（dataset1: 10个, dataset2: 5个 = 15个）
        tasks_pending, total_pending = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            status='pending',
            page_size=100
        )
        
        assert total_pending == 15
        assert all(task.status == 'pending' for task in tasks_pending)
        
        # 筛选completed状态（dataset1: 10个, dataset2: 5个 = 15个）
        tasks_completed, total_completed = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            status='completed',
            page_size=100
        )
        
        assert total_completed == 15
        assert all(task.status == 'completed' for task in tasks_completed)
        
        # 筛选processing状态（dataset2: 5个）
        tasks_processing, total_processing = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            status='processing',
            page_size=100
        )
        
        assert total_processing == 5
        assert all(task.status == 'processing' for task in tasks_processing)
    
    def test_admin_pagination(self, task_query_service, setup_test_data):
        """
        测试管理员分页功能
        
        验证分页正确工作，不同页返回不同的任务
        
        Requirements: 1.5
        """
        admin = setup_test_data['admin']
        
        # 第一页（20条）
        tasks_page1, total_page1 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            page=1,
            page_size=20
        )
        
        assert total_page1 == 35
        assert len(tasks_page1) == 20
        
        # 第二页（15条）
        tasks_page2, total_page2 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            page=2,
            page_size=20
        )
        
        assert total_page2 == 35
        assert len(tasks_page2) == 15
        
        # 验证两页任务不重复
        page1_ids = {task.id for task in tasks_page1}
        page2_ids = {task.id for task in tasks_page2}
        assert len(page1_ids & page2_ids) == 0
    
    def test_admin_sorting(self, task_query_service, setup_test_data):
        """
        测试管理员排序功能
        
        验证按不同字段排序正确工作
        
        Requirements: 1.4
        """
        admin = setup_test_data['admin']
        
        # 按创建时间降序（默认）
        tasks_desc, _ = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            sort_by='created_at',
            sort_order='desc',
            page_size=35
        )
        
        # 验证降序排列
        for i in range(len(tasks_desc) - 1):
            assert tasks_desc[i].created_at >= tasks_desc[i+1].created_at
        
        # 按创建时间升序
        tasks_asc, _ = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            sort_by='created_at',
            sort_order='asc',
            page_size=35
        )
        
        # 验证升序排列
        for i in range(len(tasks_asc) - 1):
            assert tasks_asc[i].created_at <= tasks_asc[i+1].created_at
    
    def test_annotator1_gets_assigned_tasks_only(self, task_query_service, setup_test_data):
        """
        测试标注员1只能获取分配的任务
        
        annotator1被分配了dataset1的前10个任务（索引1-10）
        
        Requirements: 2.1
        """
        annotator1 = setup_test_data['annotator1']
        dataset1 = setup_test_data['dataset1']
        
        tasks, total = task_query_service.get_user_tasks(
            user_id=annotator1.id,
            user_role='annotator',
            page_size=100
        )
        
        # 应该只看到10个任务
        assert total == 10
        assert len(tasks) == 10
        
        # 所有任务都应该来自dataset1
        assert all(task.dataset_id == dataset1.id for task in tasks)
    
    def test_annotator2_gets_all_assigned_dataset_tasks(self, task_query_service, setup_test_data):
        """
        测试标注员2获取整体分配的数据集任务
        
        annotator2被分配了dataset2的所有任务（整体分配）
        
        Requirements: 2.1
        """
        annotator2 = setup_test_data['annotator2']
        dataset2 = setup_test_data['dataset2']
        
        tasks, total = task_query_service.get_user_tasks(
            user_id=annotator2.id,
            user_role='annotator',
            page_size=100
        )
        
        # 应该看到dataset2的所有15个任务
        assert total == 15
        assert len(tasks) == 15
        
        # 所有任务都应该来自dataset2
        assert all(task.dataset_id == dataset2.id for task in tasks)
    
    def test_annotator_filter_by_dataset(self, task_query_service, setup_test_data):
        """
        测试标注员按数据集筛选
        
        标注员应该能够筛选自己被分配的数据集
        
        Requirements: 2.6
        """
        annotator1 = setup_test_data['annotator1']
        dataset1 = setup_test_data['dataset1']
        dataset2 = setup_test_data['dataset2']
        
        # 筛选dataset1（annotator1有权限）
        tasks1, total1 = task_query_service.get_user_tasks(
            user_id=annotator1.id,
            user_role='annotator',
            dataset_id=dataset1.id,
            page_size=100
        )
        
        assert total1 == 10
        assert all(task.dataset_id == dataset1.id for task in tasks1)
        
        # 筛选dataset2（annotator1无权限）
        tasks2, total2 = task_query_service.get_user_tasks(
            user_id=annotator1.id,
            user_role='annotator',
            dataset_id=dataset2.id,
            page_size=100
        )
        
        assert total2 == 0
        assert len(tasks2) == 0
    
    def test_annotator_filter_by_status(self, task_query_service, setup_test_data):
        """
        测试标注员按状态筛选
        
        标注员应该能够筛选自己任务的状态
        
        Requirements: 2.6
        """
        annotator1 = setup_test_data['annotator1']
        
        # annotator1的10个任务都是pending状态
        tasks_pending, total_pending = task_query_service.get_user_tasks(
            user_id=annotator1.id,
            user_role='annotator',
            status='pending',
            page_size=100
        )
        
        assert total_pending == 10
        assert all(task.status == 'pending' for task in tasks_pending)
        
        # 筛选completed状态（annotator1没有completed任务）
        tasks_completed, total_completed = task_query_service.get_user_tasks(
            user_id=annotator1.id,
            user_role='annotator',
            status='completed',
            page_size=100
        )
        
        assert total_completed == 0
    
    def test_annotator_pagination(self, task_query_service, setup_test_data):
        """
        测试标注员分页功能
        
        验证标注员的任务列表支持分页
        
        Requirements: 1.5, 2.1
        """
        annotator2 = setup_test_data['annotator2']
        
        # 第一页（10条）
        tasks_page1, total_page1 = task_query_service.get_user_tasks(
            user_id=annotator2.id,
            user_role='annotator',
            page=1,
            page_size=10
        )
        
        assert total_page1 == 15
        assert len(tasks_page1) == 10
        
        # 第二页（5条）
        tasks_page2, total_page2 = task_query_service.get_user_tasks(
            user_id=annotator2.id,
            user_role='annotator',
            page=2,
            page_size=10
        )
        
        assert total_page2 == 15
        assert len(tasks_page2) == 5
        
        # 验证不重复
        page1_ids = {task.id for task in tasks_page1}
        page2_ids = {task.id for task in tasks_page2}
        assert len(page1_ids & page2_ids) == 0
    
    def test_annotator_sorting(self, task_query_service, setup_test_data):
        """
        测试标注员排序功能
        
        验证标注员的任务列表支持排序
        
        Requirements: 2.6
        """
        annotator2 = setup_test_data['annotator2']
        
        # 按创建时间降序
        tasks_desc, _ = task_query_service.get_user_tasks(
            user_id=annotator2.id,
            user_role='annotator',
            sort_by='created_at',
            sort_order='desc',
            page_size=15
        )
        
        assert len(tasks_desc) == 15
        
        # 验证降序
        for i in range(len(tasks_desc) - 1):
            assert tasks_desc[i].created_at >= tasks_desc[i+1].created_at
    
    def test_combined_filters(self, task_query_service, setup_test_data):
        """
        测试组合筛选功能
        
        验证可以同时使用多个筛选条件
        
        Requirements: 1.4, 2.6
        """
        admin = setup_test_data['admin']
        dataset1 = setup_test_data['dataset1']
        
        # 组合筛选：dataset1 + pending状态
        tasks, total = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            dataset_id=dataset1.id,
            status='pending',
            page_size=100
        )
        
        assert total == 10
        assert all(task.dataset_id == dataset1.id for task in tasks)
        assert all(task.status == 'pending' for task in tasks)
    
    def test_pagination_with_filters(self, task_query_service, setup_test_data):
        """
        测试分页与筛选组合
        
        验证分页和筛选可以同时工作
        
        Requirements: 1.4, 1.5
        """
        admin = setup_test_data['admin']
        
        # 筛选pending状态，分页查询
        tasks_page1, total_page1 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            status='pending',
            page=1,
            page_size=10
        )
        
        assert total_page1 == 15
        assert len(tasks_page1) == 10
        assert all(task.status == 'pending' for task in tasks_page1)
        
        # 第二页
        tasks_page2, total_page2 = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            status='pending',
            page=2,
            page_size=10
        )
        
        assert total_page2 == 15
        assert len(tasks_page2) == 5
        assert all(task.status == 'pending' for task in tasks_page2)
    
    def test_empty_result_for_unassigned_annotator(self, task_query_service, setup_test_data, db):
        """
        测试未分配任务的标注员
        
        验证没有分配任务的标注员返回空列表
        
        Requirements: 2.1
        """
        # 创建一个新的未分配任务的标注员
        unassigned_annotator = User(
            username="unassigned_annotator",
            password_hash="hashed_password",
            role="annotator"
        )
        db.add(unassigned_annotator)
        db.commit()
        db.refresh(unassigned_annotator)
        
        tasks, total = task_query_service.get_user_tasks(
            user_id=unassigned_annotator.id,
            user_role='annotator',
            page_size=100
        )
        
        assert total == 0
        assert len(tasks) == 0
    
    def test_task_data_completeness(self, task_query_service, setup_test_data):
        """
        测试任务数据完整性
        
        验证返回的任务包含所有必要字段
        
        Requirements: 1.1
        """
        admin = setup_test_data['admin']
        
        tasks, total = task_query_service.get_user_tasks(
            user_id=admin.id,
            user_role='admin',
            page=1,
            page_size=5
        )
        
        assert len(tasks) == 5
        
        for task in tasks:
            # 验证必要字段存在
            assert hasattr(task, 'id')
            assert hasattr(task, 'task_id')
            assert hasattr(task, 'dataset_id')
            assert hasattr(task, 'corpus_id')
            assert hasattr(task, 'status')
            assert hasattr(task, 'annotation_type')
            assert hasattr(task, 'current_version')
            assert hasattr(task, 'created_at')
            assert hasattr(task, 'updated_at')
            
            # 验证字段值有效
            assert task.task_id is not None
            assert task.dataset_id is not None
            assert task.corpus_id is not None
            assert task.status in ['pending', 'processing', 'completed', 'failed']
            assert task.annotation_type in ['automatic', 'manual']
            assert task.current_version >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
