from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    """
    Модель объекта для предсказания.
    """

    name: str
    year: int
    selling_price: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: Optional[str]
    engine: Optional[str]
    max_power: Optional[str]
    torque: Optional[str]
    seats: Optional[str]


class Items(BaseModel):
    """
    Список моделей объектов.
    """

    objects: list[Item]


class ItemPredictionResponse(BaseModel):
    """
    Модель для представления результата предсказания.
    """

    data: float
