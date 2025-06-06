from datetime import datetime
from typing import Optional

import pandas as pd

from src.utils import load_transactions_from_excel


def generate_filtered_report(
    status: Optional[str] = None,
    currency: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> str:
    """
    Генерирует Excel-отчёт по отфильтрованным операциям.

    :param status: Статус операции (например, "OK").
    :param currency: Валюта операции (например, "RUB").
    :param start: Дата начала периода (в формате YYYY-MM-DD).
    :param end: Дата конца периода (в формате YYYY-MM-DD).
    :return: Путь до созданного Excel-файла.
    """
    transactions = load_transactions_from_excel("data/operations3.xlsx")

    start_dt = datetime.strptime(start, "%Y-%m-%d") if start else None
    end_dt = datetime.strptime(end, "%Y-%m-%d") if end else None

    filtered = []
    for t in transactions:
        operation_date = t.get("Дата операции")
        if not isinstance(operation_date, datetime):
            continue

        if (
            (not status or t.get("Статус") == status)
            and (not currency or t.get("Валюта операции") == currency)
            and (not start_dt or operation_date >= start_dt)
            and (not end_dt or operation_date <= end_dt)
        ):
            filtered.append(t)

    df = pd.DataFrame(filtered)
    output_file = "data/report.xlsx"
    df.to_excel(output_file, index=False)

    return output_file
