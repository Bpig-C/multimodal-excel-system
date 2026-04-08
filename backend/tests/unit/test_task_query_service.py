"""
任务查询服务测试脚本
测试基于角色的任务查询和权限检查功能
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
from models.db_models import User, Dataset, Corpus, AnnotationTask, DatasetAssignment, DatasetCorpus


@pytest.fixture(scope="module")
def db():
    engine = create_engine('sqlite:///./tests/test_artifacts/databases/test_task_query_service.db', echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="module")
def service(db):
    return TaskQueryService(db)

@pytest.fixture(scope="module")
def assignment_service(db):
    return DatasetAssignmentService(db)

@pytest.fixture(scope="module")
def admin_user(db):
    user = User(username="admin", password_hash="hashed_password", role="admin")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="module")
def annotator_user(db):
    user = User(username="annotator1", password_hash="hashed_password", role="annotator")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="module")
def annotator_user2(db):
    user = User(username="annotator2", password_hash="hashed_password", role="annotator")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="module")
def viewer_user(db):
    user = User(username="viewer1", password_hash="hashed_password", role="viewer")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="module")
def dataset1(db, admin_user):
    dataset = Dataset(dataset_id="test-dataset-1", name="Test Dataset 1", description="Test", created_by=admin_user.id)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset

@pytest.fixture(scope="module")
def dataset2(db, admin_user):
    dataset = Dataset(dataset_id="test-dataset-2", name="Test Dataset 2", description="Test", created_by=admin_user.id)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset

@pytest.fixture(scope="module")
def corpus_items(db):
    corpus_list = []
    for i in range(10):
        corpus = Corpus(text_id=f"test-corpus-{i+1}", text=f"Test corpus {i+1}", text_type="test", source_file="test.xlsx", source_row=i+1, source_field="test")
        db.add(corpus)
        corpus_list.append(corpus)
    db.commit()
    for corpus in corpus_list:
        db.refresh(corpus)
    return corpus_list

@pytest.fixture(scope="module")
def tasks_dataset1(db, dataset1, corpus_items):
    tasks = []
    for i in range(10):
        dc = DatasetCorpus(dataset_id=dataset1.id, corpus_id=corpus_items[i].id)
        db.add(dc)
        task = AnnotationTask(task_id=f"task-ds1-{i+1}", dataset_id=dataset1.id, corpus_id=corpus_items[i].id, status='pending' if i < 5 else 'completed', annotation_type='automatic')
        db.add(task)
        tasks.append(task)
    db.commit()
    for task in tasks:
        db.refresh(task)
    return tasks

@pytest.fixture(scope="module")
def tasks_dataset2(db, dataset2, corpus_items):
    tasks = []
    for i in range(5):
        corpus = Corpus(text_id=f"test-corpus-ds2-{i+1}", text=f"Test corpus ds2 {i+1}", text_type="test", source_file="test2.xlsx", source_row=i+1, source_field="test")
        db.add(corpus)
        db.flush()
        dc = DatasetCorpus(dataset_id=dataset2.id, corpus_id=corpus.id)
        db.add(dc)
        task = AnnotationTask(task_id=f"task-ds2-{i+1}", dataset_id=dataset2.id, corpus_id=corpus.id, status='pending' if i < 3 else 'completed', annotation_type='automatic')
        db.add(task)
        tasks.append(task)
    db.commit()
    for task in tasks:
        db.refresh(task)
    return tasks

@pytest.fixture(scope="module")
def full_assignment(db, dataset1, annotator_user, admin_user, assignment_service):
    assignment = assignment_service.assign_full(dataset_id=dataset1.id, user_id=annotator_user.id, role='annotator', assigned_by=admin_user.id)
    return assignment

@pytest.fixture(scope="module")
def range_assignment(db, dataset2, annotator_user2, admin_user, assignment_service):
    assignment = assignment_service.assign_range(dataset_id=dataset2.id, user_id=annotator_user2.id, role='annotator', start_index=1, end_index=3, assigned_by=admin_user.id)
    return assignment


class TestTaskQueryService:
    def test_admin_gets_all_tasks(self, service, admin_user, tasks_dataset1, tasks_dataset2):
        tasks, total = service.get_user_tasks(user_id=admin_user.id, user_role='admin')
        assert total == 15
        assert len(tasks) == 15
    
    def test_admin_filter_by_dataset(self, service, admin_user, dataset1, tasks_dataset1):
        tasks, total = service.get_user_tasks(user_id=admin_user.id, user_role='admin', dataset_id=dataset1.id)
        assert total == 10
        assert all(task.dataset_id == dataset1.id for task in tasks)
    
    def test_admin_filter_by_status(self, service, admin_user, tasks_dataset1, tasks_dataset2):
        tasks, total = service.get_user_tasks(user_id=admin_user.id, user_role='admin', status='pending')
        assert total == 8
        assert all(task.status == 'pending' for task in tasks)
    
    def test_annotator_gets_assigned_tasks_full(self, service, annotator_user, dataset1, tasks_dataset1, full_assignment):
        tasks, total = service.get_user_tasks(user_id=annotator_user.id, user_role='annotator')
        assert total == 10
        assert all(task.dataset_id == dataset1.id for task in tasks)
    
    def test_annotator_gets_assigned_tasks_range(self, service, annotator_user2, dataset2, tasks_dataset2, range_assignment):
        tasks, total = service.get_user_tasks(user_id=annotator_user2.id, user_role='annotator')
        assert total == 3
        assert all(task.dataset_id == dataset2.id for task in tasks)
    
    def test_viewer_gets_completed_tasks_only(self, service, viewer_user, tasks_dataset1, tasks_dataset2):
        tasks, total = service.get_user_tasks(user_id=viewer_user.id, user_role='viewer')
        assert total == 7
        assert all(task.status == 'completed' for task in tasks)
    
    def test_check_task_permission_admin(self, service, admin_user, tasks_dataset1):
        for task in tasks_dataset1:
            assert service.check_task_permission(user_id=admin_user.id, user_role='admin', task_id=task.id) == True
    
    def test_check_task_permission_annotator_with_assignment(self, service, annotator_user, tasks_dataset1, full_assignment):
        for task in tasks_dataset1:
            assert service.check_task_permission(user_id=annotator_user.id, user_role='annotator', task_id=task.id) == True
    
    def test_check_task_permission_viewer_completed(self, service, viewer_user, tasks_dataset1):
        for task in tasks_dataset1[5:]:
            assert task.status == 'completed'
            assert service.check_task_permission(user_id=viewer_user.id, user_role='viewer', task_id=task.id) == True
    
    def test_check_task_permission_viewer_pending(self, service, viewer_user, tasks_dataset1):
        for task in tasks_dataset1[:5]:
            assert task.status == 'pending'
            assert service.check_task_permission(user_id=viewer_user.id, user_role='viewer', task_id=task.id) == False
