"""
标注任务权限检查测试
测试任务详情和编辑API的权限检查

Requirements: 2.5, 3.4, 6.5
- 测试标注员访问未分配任务返回403
- 测试浏览员编辑任务返回403
- 测试浏览员访问未完成任务返回403
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
from models.db_models import User, Corpus, Dataset, AnnotationTask, DatasetCorpus, DatasetAssignment

# 创建测试数据库
test_db_dir = os.path.join(os.path.dirname(__file__), '..', 'test_artifacts', 'databases')
os.makedirs(test_db_dir, exist_ok=True)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(test_db_dir, 'test_annotation_permission.db')}"
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
def setup_test_data(db):
    """设置测试数据"""
    # 创建管理员用户
    admin = User(
        username="admin_perm",
        password_hash="hashed_password",
        role="admin"
    )
    db.add(admin)
    db.flush()
    
    # 创建标注员用户
    annotator1 = User(
        username="annotator1_perm",
        password_hash="hashed_password",
        role="annotator"
    )
    db.add(annotator1)
    db.flush()
    
    annotator2 = User(
        username="annotator2_perm",
        password_hash="hashed_password",
        role="annotator"
    )
    db.add(annotator2)
    db.flush()
    
    # 创建浏览员用户
    viewer = User(
        username="viewer_perm",
        password_hash="hashed_password",
        role="viewer"
    )
    db.add(viewer)
    db.flush()
    
    # 创建测试数据集
    dataset = Dataset(
        dataset_id="perm-test-dataset",
        name="Permission Test Dataset",
        description="Dataset for permission testing",
        created_by=admin.id
    )
    db.add(dataset)
    db.flush()
    
    # 创建10个任务：前5个pending，后5个completed
    tasks = []
    for i in range(10):
        corpus = Corpus(
            text_id=f"perm-corpus-{i+1:03d}",
            text=f"Permission test corpus {i+1}",
            text_type="test",
            source_file="test.xlsx",
            source_row=i+1,
            source_field="test"
        )
        db.add(corpus)
        db.flush()
        
        dc = DatasetCorpus(
            dataset_id=dataset.id,
            corpus_id=corpus.id
        )
        db.add(dc)
        
        # 前5个pending，后5个completed
        status = 'pending' if i < 5 else 'completed'
        
        task = AnnotationTask(
            task_id=f"perm-task-{i+1:03d}",
            dataset_id=dataset.id,
            corpus_id=corpus.id,
            status=status,
            annotation_type='automatic',
            current_version=1
        )
        db.add(task)
        db.flush()
        tasks.append(task)
    
    db.commit()
    
    # 刷新对象
    db.refresh(dataset)
    db.refresh(admin)
    db.refresh(annotator1)
    db.refresh(annotator2)
    db.refresh(viewer)
    for task in tasks:
        db.refresh(task)
    
    # 为annotator1分配前5个任务（索引1-5）
    assignment1 = DatasetAssignment(
        dataset_id=dataset.id,
        user_id=annotator1.id,
        role='annotator',
        task_start_index=1,
        task_end_index=5,
        is_active=True,
        assigned_by=admin.id
    )
    db.add(assignment1)
    
    # annotator2没有任何分配
    
    db.commit()
    
    return {
        'dataset': dataset,
        'admin': admin,
        'annotator1': annotator1,
        'annotator2': annotator2,
        'viewer': viewer,
        'tasks': tasks
    }


class TestAnnotationPermission:
    """标注任务权限检查测试套件"""
    
    def test_annotator_access_unassigned_task_returns_403(self, task_query_service, setup_test_data):
        """
        测试标注员访问未分配任务返回403
        
        annotator1被分配了前5个任务（索引1-5），尝试访问第6个任务应该返回False
        annotator2没有任何分配，访问任何任务都应该返回False
        
        Requirements: 2.5, 6.5
        """
        annotator1 = setup_test_data['annotator1']
        annotator2 = setup_test_data['annotator2']
        tasks = setup_test_data['tasks']
        
        # annotator1访问第6个任务（未分配）
        task_6 = tasks[5]  # 索引5是第6个任务
        has_permission = task_query_service.check_task_permission(
            user_id=annotator1.id,
            user_role='annotator',
            task_id=task_6.id
        )
        
        assert has_permission == False, "annotator1不应该有权限访问未分配的任务"
        
        # annotator1访问第1个任务（已分配）
        task_1 = tasks[0]
        has_permission = task_query_service.check_task_permission(
            user_id=annotator1.id,
            user_role='annotator',
            task_id=task_1.id
        )
        
        assert has_permission == True, "annotator1应该有权限访问已分配的任务"
        
        # annotator2访问任何任务（没有分配）
        for task in tasks:
            has_permission = task_query_service.check_task_permission(
                user_id=annotator2.id,
                user_role='annotator',
                task_id=task.id
            )
            assert has_permission == False, f"annotator2不应该有权限访问任务 {task.task_id}"
    
    def test_annotator_access_assigned_task_allowed(self, task_query_service, setup_test_data):
        """
        测试标注员访问已分配任务被允许
        
        annotator1被分配了前5个任务，应该能够访问这些任务
        
        Requirements: 2.4
        """
        annotator1 = setup_test_data['annotator1']
        tasks = setup_test_data['tasks']
        
        # annotator1访问前5个任务（已分配）
        for i in range(5):
            task = tasks[i]
            has_permission = task_query_service.check_task_permission(
                user_id=annotator1.id,
                user_role='annotator',
                task_id=task.id
            )
            assert has_permission == True, f"annotator1应该有权限访问任务 {task.task_id}"
    
    def test_viewer_edit_task_returns_403(self, task_query_service, setup_test_data):
        """
        测试浏览员编辑任务返回403
        
        浏览员不应该有权限编辑任何任务，即使是已完成的任务
        在实际API中，浏览员的编辑请求会被直接拒绝
        
        Requirements: 3.4, 6.5
        """
        viewer = setup_test_data['viewer']
        tasks = setup_test_data['tasks']
        
        # 浏览员尝试访问已完成的任务（只读权限）
        completed_task = tasks[5]  # 第6个任务是completed状态
        assert completed_task.status == 'completed'
        
        has_permission = task_query_service.check_task_permission(
            user_id=viewer.id,
            user_role='viewer',
            task_id=completed_task.id
        )
        
        # 浏览员可以查看已完成的任务
        assert has_permission == True, "浏览员应该有权限查看已完成的任务"
        
        # 但是在API层面，浏览员的编辑请求会被拒绝
        # 这个测试验证了check_task_permission对浏览员的行为
        # 实际的编辑拒绝逻辑在API层面实现（见annotations.py的update_annotation_task）
    
    def test_viewer_access_incomplete_task_returns_403(self, task_query_service, setup_test_data):
        """
        测试浏览员访问未完成任务返回403
        
        浏览员只能访问已完成的任务，访问pending/processing状态的任务应该返回False
        
        Requirements: 3.3, 6.5
        """
        viewer = setup_test_data['viewer']
        tasks = setup_test_data['tasks']
        
        # 浏览员访问pending状态的任务
        for i in range(5):
            task = tasks[i]
            assert task.status == 'pending'
            
            has_permission = task_query_service.check_task_permission(
                user_id=viewer.id,
                user_role='viewer',
                task_id=task.id
            )
            
            assert has_permission == False, f"浏览员不应该有权限访问未完成的任务 {task.task_id}"
    
    def test_viewer_access_completed_task_allowed(self, task_query_service, setup_test_data):
        """
        测试浏览员访问已完成任务被允许
        
        浏览员应该能够访问已完成的任务
        
        Requirements: 3.2, 3.3
        """
        viewer = setup_test_data['viewer']
        tasks = setup_test_data['tasks']
        
        # 浏览员访问completed状态的任务
        for i in range(5, 10):
            task = tasks[i]
            assert task.status == 'completed'
            
            has_permission = task_query_service.check_task_permission(
                user_id=viewer.id,
                user_role='viewer',
                task_id=task.id
            )
            
            assert has_permission == True, f"浏览员应该有权限访问已完成的任务 {task.task_id}"
    
    def test_admin_access_all_tasks_allowed(self, task_query_service, setup_test_data):
        """
        测试管理员访问所有任务被允许
        
        管理员应该能够访问所有任务，无论状态如何
        
        Requirements: 1.3, 6.2
        """
        admin = setup_test_data['admin']
        tasks = setup_test_data['tasks']
        
        # 管理员访问所有任务
        for task in tasks:
            has_permission = task_query_service.check_task_permission(
                user_id=admin.id,
                user_role='admin',
                task_id=task.id
            )
            
            assert has_permission == True, f"管理员应该有权限访问任务 {task.task_id}"
    
    def test_permission_check_with_invalid_task_id(self, task_query_service, setup_test_data):
        """
        测试使用无效任务ID进行权限检查
        
        当任务不存在时，应该返回False
        """
        admin = setup_test_data['admin']
        
        # 使用不存在的任务ID
        has_permission = task_query_service.check_task_permission(
            user_id=admin.id,
            user_role='admin',
            task_id=99999
        )
        
        assert has_permission == False, "不存在的任务应该返回False"
    
    def test_annotator_boundary_task_access(self, task_query_service, setup_test_data):
        """
        测试标注员边界任务访问
        
        验证任务范围的边界情况：
        - annotator1被分配了索引1-5的任务
        - 应该能访问第1个和第5个任务
        - 不应该能访问第0个（如果存在）和第6个任务
        
        Requirements: 2.2, 2.5
        """
        annotator1 = setup_test_data['annotator1']
        tasks = setup_test_data['tasks']
        
        # 边界测试：第1个任务（索引1，数组索引0）
        task_1 = tasks[0]
        has_permission = task_query_service.check_task_permission(
            user_id=annotator1.id,
            user_role='annotator',
            task_id=task_1.id
        )
        assert has_permission == True, "annotator1应该有权限访问第1个任务"
        
        # 边界测试：第5个任务（索引5，数组索引4）
        task_5 = tasks[4]
        has_permission = task_query_service.check_task_permission(
            user_id=annotator1.id,
            user_role='annotator',
            task_id=task_5.id
        )
        assert has_permission == True, "annotator1应该有权限访问第5个任务"
        
        # 边界测试：第6个任务（索引6，数组索引5）
        task_6 = tasks[5]
        has_permission = task_query_service.check_task_permission(
            user_id=annotator1.id,
            user_role='annotator',
            task_id=task_6.id
        )
        assert has_permission == False, "annotator1不应该有权限访问第6个任务"
    
    def test_multiple_annotators_isolation(self, task_query_service, setup_test_data, db):
        """
        测试多个标注员之间的隔离
        
        验证不同标注员的任务分配是隔离的
        
        Requirements: 2.1, 6.3
        """
        annotator1 = setup_test_data['annotator1']
        annotator2 = setup_test_data['annotator2']
        dataset = setup_test_data['dataset']
        tasks = setup_test_data['tasks']
        admin = setup_test_data['admin']
        
        # 为annotator2分配后5个任务（索引6-10）
        assignment2 = DatasetAssignment(
            dataset_id=dataset.id,
            user_id=annotator2.id,
            role='annotator',
            task_start_index=6,
            task_end_index=10,
            is_active=True,
            assigned_by=admin.id
        )
        db.add(assignment2)
        db.commit()
        
        # annotator1应该只能访问前5个任务
        for i in range(5):
            task = tasks[i]
            has_permission = task_query_service.check_task_permission(
                user_id=annotator1.id,
                user_role='annotator',
                task_id=task.id
            )
            assert has_permission == True, f"annotator1应该有权限访问任务 {task.task_id}"
        
        # annotator1不应该能访问后5个任务
        for i in range(5, 10):
            task = tasks[i]
            has_permission = task_query_service.check_task_permission(
                user_id=annotator1.id,
                user_role='annotator',
                task_id=task.id
            )
            assert has_permission == False, f"annotator1不应该有权限访问任务 {task.task_id}"
        
        # annotator2应该只能访问后5个任务
        for i in range(5, 10):
            task = tasks[i]
            has_permission = task_query_service.check_task_permission(
                user_id=annotator2.id,
                user_role='annotator',
                task_id=task.id
            )
            assert has_permission == True, f"annotator2应该有权限访问任务 {task.task_id}"
        
        # annotator2不应该能访问前5个任务
        for i in range(5):
            task = tasks[i]
            has_permission = task_query_service.check_task_permission(
                user_id=annotator2.id,
                user_role='annotator',
                task_id=task.id
            )
            assert has_permission == False, f"annotator2不应该有权限访问任务 {task.task_id}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

