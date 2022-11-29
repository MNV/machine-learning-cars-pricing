from pydantic import BaseModel, BaseSettings, Field


class Project(BaseModel):
    """
    Описание проекта.
    """

    #: название проекта
    title: str = "Предсказание стоимости автомобилей."
    #: описание проекта
    description: str = "Предсказание стоимости автомобилей с использованием методов машинного обучения."
    #: версия релиза
    release_version: str = Field(default="0.1.0")


class Settings(BaseSettings):
    """
    Настройки проекта.
    """

    #: режим отладки
    debug: bool = Field(default=False)
    #: описание проекта
    project: Project
    #: путь к файлу модели для предсказаний
    file_path_model: str = Field(default="/media/model.pickle")

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


# инициализация настроек приложения
settings = Settings()
