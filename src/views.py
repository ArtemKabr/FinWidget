from collections import Counter
from typing import Optional

from fastapi import APIRouter, HTTPException

from src.reports import generate_filtered_report
from src.utils import load_transactions_from_excel

router = APIRouter()


@router.get("/summary")
def get_summary() -> dict:
    """
    📊 Возвращает сводную статистику по транзакциям.
    """
    transactions = load_transactions_from_excel("data/operations3.xlsx")
    if not transactions:
        raise HTTPException(status_code=404, detail="Нет данных о транзакциях")

    total = len(transactions)
    status_counts = Counter(t.get("Статус") for t in transactions)

    return {"total_operations": total, "by_status": status_counts}


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


@router.get("/categories")
def get_categories() -> dict:
    """
    🔹 Возвращает список уникальных категорий из Excel-файла.
    """
    transactions = load_transactions_from_excel("data/operations3.xlsx")
    categories = sorted(set(t.get("Категория", "").strip() for t in transactions if t.get("Категория")))
    return {"categories": categories}


@router.get("/top-categories")
def get_top_categories(limit: int = 5) -> dict:
    """
    📊 Возвращает топ-N категорий по сумме операций.
    """
    transactions = load_transactions_from_excel("data/operations3.xlsx")
    if not transactions:
        raise HTTPException(status_code=404, detail="Нет данных")

    totals: dict[str, float] = {}
    for t in transactions:
        category = t.get("Категория")
        amount = t.get("operationAmount", {}).get("amount")
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            continue

        if category:
            totals[category] = totals.get(category, 0) + amount

    sorted_categories = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    result = [{"category": cat, "total": round(total, 2)} for cat, total in sorted_categories[:limit]]
    return {"top_categories": result}
