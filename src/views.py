from typing import Optional

from fastapi import APIRouter, HTTPException

from src.reports import generate_filtered_report
from src.utils import load_transactions_from_excel

router = APIRouter()


@router.get("/operations")
def get_operations(
    status: Optional[str] = None,
    currency: Optional[str] = None,
    category: Optional[str] = None,
) -> dict:
    transactions = load_transactions_from_excel("data/operations3.xlsx")
    if not transactions:
        raise HTTPException(status_code=404, detail="Нет данных о транзакциях")

    filtered = [
        t
        for t in transactions
        if (not status or t.get("Статус") == status)
        and (not currency or t.get("Валюта операции") == currency)
        and (not category or t.get("Категория") == category)
    ]

    return {"operations": filtered}


@router.get("/report")
def create_report(status: Optional[str] = None, currency: Optional[str] = None) -> dict:
    """
    📊 Генерация Excel-отчёта по фильтру.

    :param status: Фильтрация по статусу.
    :param currency: Фильтрация по валюте.
    :return: Сообщение об успешном создании отчёта.
    """
    file_path = generate_filtered_report(status=status, currency=currency)
    return {"message": f"Отчёт успешно сохранён в {file_path}"}
