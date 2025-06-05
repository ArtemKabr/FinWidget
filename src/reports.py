from typing import Optional

import pandas as pd

from src.utils import load_transactions_from_excel


def generate_filtered_report(status: Optional[str] = None, currency: Optional[str] = None) -> str:
    """
    Генерирует Excel-отчёт по отфильтрованным операциям.

    :param status: Статус операции (например, "OK").
    :param currency: Валюта операции (например, "RUB").
    :return: Имя созданного файла.
    """
    transactions = load_transactions_from_excel("data/operations3.xlsx")

    filtered = [
        t
        for t in transactions
        if (not status or t.get("Статус") == status) and (not currency or t.get("Валюта операции") == currency)
    ]

    df = pd.DataFrame(filtered)
    output_file = "data/report.xlsx"
    df.to_excel(output_file, index=False)

    return output_file
