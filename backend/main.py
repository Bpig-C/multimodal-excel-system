"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional
from config import settings
from database import init_db
from api.corpus import router as corpus_router
from api.corpus_grouped import router as corpus_grouped_router
from api.dataset import router as dataset_router
from api.dataset_assignment import router as dataset_assignment_router
from api.labels import router as labels_router
from api.annotations import router as annotations_router
from api.images import router as images_router
from api.versions import router as versions_router
from api.review import router as review_router
from api.users import router as users_router, auth_router
from api.document_import import router as document_import_router
from api.structured_export import router as structured_export_router
from api.config_api import router as config_router
from api.data_query import router as data_query_router
from services.storage_service import storage_service

# middlewares
from middleware.error_handler import error_handler_middleware
from middleware.logging_config import get_logger

logger = get_logger(__name__)

IMAGE_MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown logs."""
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} start")
    logger.info(f"Debug mode: {settings.DEBUG}")
    init_db()
    yield
    logger.info(f"{settings.APP_NAME} shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="《品质失效案例实体关系标注系统》API - 面向品质失效案例的实体关系标注服务",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Middlewares
app.middleware("http")(error_handler_middleware)

# Routers (order matters for grouped corpus)
app.include_router(corpus_grouped_router)
app.include_router(corpus_router)
app.include_router(document_import_router)
app.include_router(structured_export_router)
app.include_router(config_router)
app.include_router(data_query_router)
app.include_router(dataset_assignment_router)
app.include_router(dataset_router)
app.include_router(labels_router)
app.include_router(annotations_router)
app.include_router(images_router)
app.include_router(versions_router)
app.include_router(review_router)
app.include_router(users_router)
app.include_router(auth_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static or delegated file serving
if settings.STORAGE_TYPE == "local":
    settings.IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    settings.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    app.mount("/images", StaticFiles(directory=str(settings.IMAGE_DIR)), name="images")
    app.mount("/exports", StaticFiles(directory=str(settings.EXPORT_DIR)), name="exports")
    logger.info(f"Image storage: local filesystem ({settings.IMAGE_DIR})")
else:
    @app.get("/images/{file_path:path}")
    async def get_image(file_path: str):
        """Fetch image from object storage."""
        image_data = storage_service.get_image(file_path)
        if image_data is None:
            raise HTTPException(status_code=404, detail="Image not found")

        ext = file_path.split('.')[-1].lower()
        content_type_map = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp',
        }
        content_type = content_type_map.get(ext, 'image/png')
        return Response(content=image_data, media_type=content_type)

    logger.info(f"Image storage: MinIO ({settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET})")


def _safe_resolve_processed_image_path(
    processor_name: str,
    data_source: str,
    image_path: str,
) -> Optional[Path]:
    """Resolve processed image path and prevent path traversal."""
    if processor_name not in {"kf", "qms"}:
        return None

    base_dir = settings.PROCESSED_DIR.resolve()
    candidate = (base_dir / processor_name / data_source / image_path).resolve()
    try:
        candidate.relative_to(base_dir)
    except ValueError:
        return None
    return candidate


@app.get("/processed-images/{processor_name}/{data_source}/{image_path:path}")
async def get_processed_image(processor_name: str, data_source: str, image_path: str):
    """
    Serve KF/QMS processed image files.

    These images are stored under data/processed/{processor}/{data_source}/imgs/*
    and are separate from storage_service-managed /images files.
    """
    resolved = _safe_resolve_processed_image_path(processor_name, data_source, image_path)
    if resolved is None or not resolved.is_file():
        raise HTTPException(status_code=404, detail="Processed image not found")

    ext = resolved.suffix.lower()
    media_type = IMAGE_MEDIA_TYPES.get(ext)
    if not media_type:
        raise HTTPException(status_code=400, detail="Unsupported image format")

    return FileResponse(str(resolved), media_type=media_type)


@app.get("/")
async def root():
    """Root service metadata."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Catch-all exception handler returning JSON."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": "INTERNAL_ERROR",
            "error_message": str(exc),
            "timestamp": None,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
