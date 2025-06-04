# src/utils.py
from typing import Any

import pandas as pd

from src.utils_logger import logger


def load_transactions_from_excel(file_path: str) -> list[dict[str, Any]]:
    """
    Загружает транзакции из Excel-файла и возвращает список словарей.

    :param file_path: Путь до Excel-файла.
    :return: Список операций в виде словарей.
    """
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Загружено {len(df)} транзакций из файла: {file_path}")
        return list(df.to_dict(orient="records"))
    except Exception as e:
        logger.error(f"Ошибка при загрузке Excel-файла: {e}")
        raise RuntimeError(f"Ошибка при загрузке Excel-файла: {e}")
