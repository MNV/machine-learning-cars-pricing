import io
import pickle
import re

import pandas as pd
from numpy import ndarray
from pandas import DataFrame

from schemas.items import Item
from settings import settings


class ItemsService:
    """
    Сервис для работы с информацией об объектах для предсказаний.
    """

    def __init__(self):
        """
        Инициализация сервиса.
        """

        self.model = pickle.load(open(settings.file_path_model, "rb"))

    async def _process_data(self, df: DataFrame, drop_first=False) -> ndarray:
        """
        Обработка данных для предсказания.

        :param df: Pandas DataFrame с данными.
        :param drop_first: Удалять ли первый столбец для One Hot Encoding?
        :return:
        """

        df["mileage"] = df["mileage"].str.extract(r"(\d+.\d+)").astype(float)
        df["engine"] = df["engine"].str.extract(r"(\d+.\d+)").astype("Int64")
        df["max_power"] = df["max_power"].str.extract(r"(\d+.\d+)").astype(float)

        # получение максимальных значений RPM
        rpm_values = (
            df["torque"]
            .str.extract(r"(\d+)\s*rpm|(\d{1}\d+)\s*\(", flags=re.IGNORECASE)
            .astype(float)
        )
        df["max_torque_rpm"] = rpm_values[0].fillna(rpm_values[1])
        df.drop(["name", "selling_price", "torque"], axis=1, inplace=True)
        df = df.fillna(df.median(numeric_only=True))
        # число лошадиных сил на литр объема двигателя
        df["power_per_engine"] = df["engine"] / df["max_power"]
        # получение квадрата года (т.к. существует квадратичная зависимость цены от года)
        df["year_squared"] = df["year"] ** 2

        df = pd.get_dummies(
            df,
            columns=df.dtypes[df.dtypes == "object"].index.values.tolist() + ["seats"],
            drop_first=drop_first,
        )

        df_templpate = pd.DataFrame()
        df_templpate["year"] = df.get("year", 0)
        df_templpate["km_driven"] = df.get("km_driven", 0)
        df_templpate["mileage"] = df.get("mileage", 0)
        df_templpate["engine"] = df.get("engine", 0)
        df_templpate["max_power"] = df.get("max_power", 0)
        df_templpate["max_torque_rpm"] = df.get("max_torque_rpm", 0)
        df_templpate["fuel_Diesel"] = df.get("fuel_Diesel", 0)
        df_templpate["fuel_LPG"] = df.get("fuel_LPG", 0)
        df_templpate["fuel_Petrol"] = df.get("fuel_Petrol", 0)
        df_templpate["seller_type_Individual"] = df.get("seller_type_Individual", 0)
        df_templpate["seller_type_Trustmark Dealer"] = df.get(
            "seller_type_Trustmark Dealer", 0
        )
        df_templpate["transmission_Manual"] = df.get("transmission_Manual", 0)
        df_templpate["owner_Fourth & Above Owner"] = df.get(
            "owner_Fourth & Above Owner", 0
        )
        df_templpate["owner_Second Owner"] = df.get("owner_Second Owner", 0)
        df_templpate["owner_Test Drive Car"] = df.get("owner_Test Drive Car", 0)
        df_templpate["owner_Third Owner"] = df.get("owner_Third Owner", 0)
        df_templpate["seats_14"] = df.get("seats_14", 0)
        df_templpate["seats_2"] = df.get("seats_2", 0)
        df_templpate["seats_4"] = df.get("seats_4", 0)
        df_templpate["seats_5"] = df.get("seats_5", 0)
        df_templpate["seats_6"] = df.get("seats_6", 0)
        df_templpate["seats_7"] = df.get("seats_7", 0)
        df_templpate["seats_8"] = df.get("seats_8", 0)
        df_templpate["seats_9"] = df.get("seats_9", 0)
        df_templpate["power_per_engine"] = df.get("power_per_engine", 0)
        df_templpate["year_squared"] = df.get("year_squared", 0)

        return self.model.predict(df_templpate)

    async def predict(self, item: Item) -> ndarray:
        """
        Предсказание стоимости автомобиля.

        :param item: Список объектов с данными об автомобилях.
        :return:
        """

        df = pd.DataFrame([item.dict()])
        return await self._process_data(df)

    async def predict_as_file(self, items: list[Item]) -> io.StringIO:
        """
        Предсказание стоимости автомобилей с выгрузкой в файл.

        :param items: Объекты с данными об автомобилях.
        :return:
        """

        df_source = pd.DataFrame([item.dict() for item in items])
        df = df_source.copy()

        # добавление атрибута с предсказанной стоимостью
        df_source["predicted_selling_price"] = await self._process_data(
            df, drop_first=True
        )

        # сохранение данных в буфер для представления в файле
        file_buffer = io.StringIO()
        df_source.to_csv(file_buffer)
        file_buffer.seek(0)

        return file_buffer
