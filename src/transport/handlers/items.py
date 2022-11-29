import codecs
from csv import DictReader

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTasks

from schemas.items import Item, ItemPredictionResponse
from schemas.routes import MetadataTag
from services.items import ItemsService

router = APIRouter()


tag_items = MetadataTag(
    name="items",
    description="Получение предсказаний для переданных объектов.",
)


@router.get(
    "/predict_item",
    summary="Получение предсказания для переданного объекта.",
    response_model=ItemPredictionResponse,
)
async def predict_item(
    item: Item,
    items_service: ItemsService = Depends(),
) -> ItemPredictionResponse:
    """
    Получение предсказания стоимости автомобиля по переданным данным.

    :param item: Данные объекта для получения предсказания.
    :param items_service: Сервис для работы с информацией об объектах для предсказаний.
    :return:
    """

    return ItemPredictionResponse(data=await items_service.predict(item))


@router.get(
    "/predict_items",
    summary="Получение предсказаний для объектов, переданных в CSV-файле.",
)
async def predict_items(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    items_service: ItemsService = Depends(),
) -> StreamingResponse:
    """
    Получение предсказаний стоимостей автомобилей по переданным данным в CSV-файле.

    :param background_tasks: Фоновые задачи для асинхронного выполнения.
    :param file: Файл с данными объектов для предсказаний.
    :param items_service: Сервис для работы с информацией об объектах для предсказаний.
    :return:
    """

    rows = DictReader(codecs.iterdecode(file.file, "utf-8"), delimiter=",")
    background_tasks.add_task(file.file.close)
    items = [Item.parse_obj(row) for row in rows]
    file_output = await items_service.predict_as_file(items)

    return StreamingResponse(
        file_output,
        headers={"Content-Disposition": "attachment; filename=predictions.csv"},
        media_type="text/csv",
    )
