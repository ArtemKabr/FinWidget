import json
from datetime import datetime
from typing import Any, cast

import numpy as np
import pandas as pd

from src.utils_logger import logger


def load_transactions_from_excel(file_path: str) -> list[dict[str, Any]]:
    """
    Загружает транзакции из Excel-файла и возвращает список словарей.

    :param file_path: Путь до Excel-файла.
    :return: Список операций в виде словарей.
    """
    try:
        df = pd.read_excel(file_path, parse_dates=["Дата операции"])

        df = df.replace([np.nan, np.inf, -np.inf], None)

        logger.info(f"Загружено {len(df)} транзакций из файла: {file_path}")
        return cast(list[dict[str, Any]], df.to_dict(orient="records"))
    except Exception as e:
        logger.error(f"Ошибка при загрузке Excel-файла: {e}")
        raise RuntimeError(f"Ошибка при загрузке Excel-файла: {e}")


def get_greeting_from_time(dt: datetime) -> str:
    hour = dt.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_user_settings() -> dict[str, Any]:
    """
    Загружает пользовательские настройки из user_settings.json.
    """
    with open("user_settings.json", encoding="utf-8") as f:
        return cast(dict[str, Any], json.load(f))


def load_operations(file_path: str = "data/operations3.xlsx") -> pd.DataFrame:
    """
    Загружает операции из Excel-файла.
    """
    try:
        df = pd.read_excel(file_path)
        df = df.fillna("")  # избегаем NaN для JSON-ответов
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке Excel-файла: {e}")
        raise RuntimeError(f"Ошибка при загрузке Excel-файла: {e}")


def get_month_range(dt: datetime) -> tuple[datetime, datetime]:
    """
    Возвращает диапазон от начала месяца до указанной даты.

    :param dt: Дата
    :return: Кортеж (начало_месяца, дата)
    """
    start_of_month = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return start_of_month, dt


def get_currency_rates(currencies: list[str]) -> dict[str, float]:
    """
    Возвращает фиктивные курсы валют для указанных кодов валют.
    Для разработки и отладки, потом можно заменить на API-запрос.

    :param currencies: Список кодов валют (например, ["USD", "EUR"])
    :return: Словарь с курсами
    """
    return {currency: round(90 + i * 5.5, 2) for i, currency in enumerate(currencies)}


def get_stock_prices(stocks: list[str]) -> dict[str, float]:
    """
    Возвращает фиктивные цены акций для указанных тикеров.
    Для разработки и отладки, потом можно заменить на API-запрос.

    :param stocks: Список тикеров (например, ["AAPL", "TSLA"])
    :return: Словарь с ценами
    """
    return {stock: round(100 + i * 50.0, 2) for i, stock in enumerate(stocks)}
