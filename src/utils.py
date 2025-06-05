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
        df = pd.read_excel(file_path)

        df = df.replace([np.nan, np.inf, -np.inf], None)

        logger.info(f"Загружено {len(df)} транзакций из файла: {file_path}")
        return cast(list[dict[str, Any]], df.to_dict(orient="records"))
    except Exception as e:
        logger.error(f"Ошибка при загрузке Excel-файла: {e}")
        raise RuntimeError(f"Ошибка при загрузке Excel-файла: {e}")
