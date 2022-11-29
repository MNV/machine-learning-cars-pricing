from fastapi import FastAPI

from routes import metadata_tags, setup_routes
from settings import settings

model = None


def build_app() -> FastAPI:
    """Создание приложения FastAPI."""

    app_params = {
        "debug": settings.debug,
        "openapi_tags": metadata_tags,
        "title": f'API системы "{settings.project.title}"',
        "description": settings.project.description,
        "version": settings.project.release_version,
    }
    app = FastAPI(**app_params)
    setup_routes(app)

    return app
