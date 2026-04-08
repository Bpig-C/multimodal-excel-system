"""Configuration module for the backend settings."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Backend directory (used to resolve relative paths)
BACKEND_DIR = Path(__file__).resolve().parent
# Project root (multimodal_excel_system/), one level above backend/
PROJECT_DIR = BACKEND_DIR.parent
# All data files live under PROJECT_DIR/data/
_DATA_DIR = PROJECT_DIR / "data"


def normalize_database_url(raw_value: str | None) -> str:
    """Normalize DATABASE_URL into a SQLAlchemy-compatible URL."""
    if not raw_value:
        raise RuntimeError(
            "DATABASE_URL is required. To avoid ambiguous local SQLite files, "
            "the backend no longer falls back to ./data/database/annotation.db."
        )

    value = raw_value.strip().strip('"').strip("'")

    # Already a full URL
    if "://" in value:
        return value

    # Support relative/absolute filesystem paths
    path = Path(value)
    if not path.is_absolute():
        path = (BACKEND_DIR / value).resolve()

    return f"sqlite:///{path.as_posix()}"


class Settings:
    """Application settings."""

    # Application
    APP_NAME: str = "面向离散型电子信息制造业的多模态语料库构建平台"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    # Database
    DATABASE_URL: str = normalize_database_url(os.getenv("DATABASE_URL"))

    # LLM
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    DASHSCOPE_BASE_URL: str = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    LLM_MODEL: str = "qwen-max"
    LLM_TEMPERATURE: float = 0.0
    LLM_TIMEOUT_SECONDS: int = int(os.getenv("LLM_TIMEOUT_SECONDS", "120"))
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "1"))

    # Storage — all paths are absolute, anchored to PROJECT_DIR/data/
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")  # 'local' or 'minio'
    UPLOAD_DIR: Path = _DATA_DIR / "uploads"
    IMAGE_DIR: Path = _DATA_DIR / "images"
    EXPORT_DIR: Path = _DATA_DIR / "exports"
    PROCESSED_DIR: Path = _DATA_DIR / "processed"
    DATABASE_DIR: Path = _DATA_DIR / "database"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB

    # MinIO (when STORAGE_TYPE='minio')
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "annotation-images")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    MINIO_PUBLIC_URL: str = os.getenv("MINIO_PUBLIC_URL", "")  # Optional public URL

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Batch tasks
    BATCH_SIZE: int = 10
    MAX_CONCURRENT_TASKS: int = 5


# Global settings instance
settings = Settings()

# Ensure required directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.IMAGE_DIR.mkdir(parents=True, exist_ok=True)
settings.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
settings.DATABASE_DIR.mkdir(parents=True, exist_ok=True)
