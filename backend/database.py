"""
数据库连接和会话管理
"""
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite需要
    echo=settings.DEBUG
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    用于FastAPI依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_migration_v005():
    """执行 v005 迁移：新增 KF/QMS 相关表"""
    migration_path = Path(__file__).parent / "migrations" / "v005_add_kf_qms_tables.sql"
    if not migration_path.exists():
        print("[v005] 迁移文件不存在，跳过")
        return
    sql = migration_path.read_text(encoding="utf-8")
    with engine.connect() as conn:
        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt and not stmt.startswith("--"):
                conn.execute(text(stmt))
        conn.commit()
    print("[v005] 迁移完成")


def init_db():
    """
    初始化数据库
    创建所有表并执行迁移
    """
    # 导入所有模型以确保它们被注册
    from models import db_models  # noqa

    Base.metadata.create_all(bind=engine)
    run_migration_v005()
    print("数据库初始化完成")


def drop_db():
    """
    删除所有表（仅用于开发/测试）
    """
    Base.metadata.drop_all(bind=engine)
    print("数据库已清空")
