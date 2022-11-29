from fastapi import FastAPI

from transport.handlers import items
from transport.handlers.items import tag_items

metadata_tags = [tag_items]


def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов для API"""

    app.include_router(
        items.router,
        prefix="",
        tags=[tag_items.name],
    )
