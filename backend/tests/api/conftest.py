"""
API测试共享工具函数
不含 pytest fixture，供各测试文件直接 import 使用

使用方式（在测试文件顶部）：
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # backend/
    sys.path.insert(0, str(Path(__file__).parent))                # tests/api/
    from conftest import make_test_db, get_db_override, login, auth, create_user
"""
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 确保 backend/ 在 sys.path 中（conftest 由 pytest 自动加载时也需要）
_backend_dir = Path(__file__).parent.parent.parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))


# ============================================================================
# httpx 0.28+ 兼容补丁
# starlette 0.27.0 的 TestClient.__init__ 向 httpx.Client.__init__ 传递了
# `app=` 关键字参数，而 httpx 0.28 起已移除该参数，导致所有测试在 collect 阶段
# 抛出 TypeError。此补丁在 pytest 加载 conftest 时自动修复，无需修改 starlette。
# ============================================================================

def _patch_testclient_for_httpx28() -> None:
    import httpx
    ver = tuple(int(x) for x in httpx.__version__.split(".")[:2])
    if ver < (0, 28):
        return  # 旧版本不需要补丁

    import typing
    import contextlib
    import anyio
    from starlette import testclient as _stc
    from starlette.testclient import (
        ASGIApp, _is_asgi3, _WrapASGI2, _AsyncBackend, _TestClientTransport,
    )

    def _patched_init(
        self,
        app: ASGIApp,
        base_url: str = "http://testserver",
        raise_server_exceptions: bool = True,
        root_path: str = "",
        backend: str = "asyncio",
        backend_options: typing.Optional[typing.Dict[str, typing.Any]] = None,
        cookies: httpx._client.CookieTypes = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
    ) -> None:
        self.async_backend = _AsyncBackend(
            backend=backend, backend_options=backend_options or {}
        )
        if _is_asgi3(app):
            asgi_app = typing.cast("ASGI3App", app)
        else:
            asgi_app = _WrapASGI2(typing.cast("ASGI2App", app))
        self.app = asgi_app
        self.app_state: typing.Dict[str, typing.Any] = {}
        transport = _TestClientTransport(
            self.app,
            portal_factory=self._portal_factory,
            raise_server_exceptions=raise_server_exceptions,
            root_path=root_path,
            app_state=self.app_state,
        )
        if headers is None:
            headers = {}
        headers.setdefault("user-agent", "testclient")
        # 关键修复：移除 app=self.app，httpx 0.28+ 不再接受该参数
        httpx.Client.__init__(
            self,
            base_url=base_url,
            headers=headers,
            transport=transport,
            follow_redirects=True,
            cookies=cookies,
        )

    _stc.TestClient.__init__ = _patched_init


_patch_testclient_for_httpx28()


# ============================================================================
# DB 工厂
# ============================================================================

def make_test_db(db_name: str):
    """
    创建独立测试数据库。
    返回 (engine, SessionLocal)
    """
    url = f"sqlite:///./tests/test_artifacts/databases/{db_name}"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def get_db_override(SessionLocal):
    """
    生成 FastAPI get_db 的覆盖函数，绑定到指定的 SessionLocal。
    用法：app.dependency_overrides[get_db] = get_db_override(SessionLocal)
    """
    def override():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    return override


# ============================================================================
# 认证工具
# ============================================================================

def login(client, username: str, password: str) -> str:
    """登录并返回 access_token。断言失败时输出响应体供调试。"""
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password}
    )
    assert resp.status_code == 200, f"登录失败 ({username}): {resp.text}"
    return resp.json()["access_token"]


def auth(token: str) -> dict:
    """返回带有 Bearer token 的 Authorization 请求头。"""
    return {"Authorization": f"Bearer {token}"}


# ============================================================================
# 数据工厂
# ============================================================================

def create_user(SessionLocal, username: str, password: str, role: str) -> int:
    """使用 UserService 创建用户，返回用户 DB id。若用户已存在则直接返回其 ID。"""
    from models.db_models import User as UserModel
    from services.user_service import UserService
    db = SessionLocal()
    try:
        existing = db.query(UserModel).filter(UserModel.username == username).first()
        if existing:
            return existing.id
        svc = UserService(db)
        user = svc.create_user(username=username, password=password, role=role)
        db.commit()
        db.refresh(user)
        return user.id
    finally:
        db.close()


def create_corpus(SessionLocal, text_id: str, text: str = "品质失效测试语料内容",
                  source_file: str = "test.xlsx", source_row: int = 1,
                  source_field: str = "问题描述", text_type: str = "问题描述") -> int:
    """创建语料，返回语料 DB id。"""
    from models.db_models import Corpus
    db = SessionLocal()
    try:
        corpus = Corpus(
            text_id=text_id,
            text=text,
            text_type=text_type,
            source_file=source_file,
            source_row=source_row,
            source_field=source_field,
            has_images=False
        )
        db.add(corpus)
        db.commit()
        db.refresh(corpus)
        return corpus.id
    finally:
        db.close()


def create_dataset(SessionLocal, dataset_id: str, name: str, created_by: int,
                   description: str = "") -> int:
    """创建数据集，返回数据集 DB id。"""
    from models.db_models import Dataset
    db = SessionLocal()
    try:
        ds = Dataset(
            dataset_id=dataset_id,
            name=name,
            description=description,
            created_by=created_by
        )
        db.add(ds)
        db.commit()
        db.refresh(ds)
        return ds.id
    finally:
        db.close()


def create_task(SessionLocal, task_id: str, dataset_db_id: int, corpus_db_id: int,
                status: str = "pending") -> int:
    """创建标注任务（同时创建 DatasetCorpus 关联），返回任务 DB id。"""
    from models.db_models import AnnotationTask, DatasetCorpus
    db = SessionLocal()
    try:
        # 检查关联是否已存在
        existing = db.query(DatasetCorpus).filter(
            DatasetCorpus.dataset_id == dataset_db_id,
            DatasetCorpus.corpus_id == corpus_db_id
        ).first()
        if not existing:
            assoc = DatasetCorpus(dataset_id=dataset_db_id, corpus_id=corpus_db_id)
            db.add(assoc)

        task = AnnotationTask(
            task_id=task_id,
            dataset_id=dataset_db_id,
            corpus_id=corpus_db_id,
            status=status
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.id
    finally:
        db.close()


def create_image(SessionLocal, image_id: str, file_path: str = "test/img.png",
                 width: int = 800, height: int = 600) -> int:
    """创建图片记录，返回图片 DB id。"""
    from models.db_models import Image
    db = SessionLocal()
    try:
        img = Image(
            image_id=image_id,
            file_path=file_path,
            width=width,
            height=height
        )
        db.add(img)
        db.commit()
        db.refresh(img)
        return img.id
    finally:
        db.close()


# ============================================================================
# 清理工具
# ============================================================================

def truncate_all(SessionLocal):
    """清空所有核心表（用于测试后清理）。"""
    from models.db_models import (
        User, Corpus, Dataset, DatasetCorpus, AnnotationTask,
        TextEntity, Relation, ReviewTask, VersionHistory,
        DatasetAssignment, Image, ImageEntity, EntityType, RelationType
    )
    db = SessionLocal()
    try:
        for model in [
            VersionHistory, ReviewTask, Relation, TextEntity, ImageEntity,
            AnnotationTask, DatasetAssignment, DatasetCorpus,
            Dataset, Corpus, Image, EntityType, RelationType, User
        ]:
            db.query(model).delete()
        db.commit()
    finally:
        db.close()
