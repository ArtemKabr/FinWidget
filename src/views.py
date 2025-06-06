from collections import Counter
from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query

from src.reports import generate_filtered_report
from src.utils import (
    get_currency_rates,
    get_greeting_from_time,
    get_month_range,
    get_stock_prices,
    get_user_settings,
    load_operations,
    load_transactions_from_excel,
)

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
def create_report(
    status: Optional[str] = None,
    currency: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> dict:
    file_path = generate_filtered_report(status=status, currency=currency, start=start, end=end)
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


@router.get("/home")
def home(date: str = Query(..., description="Дата в формате YYYY-MM-DD HH:MM:SS")) -> dict[str, Any]:
    """
    🌅 Главная страница: приветствие, траты по картам, топ-5 трат, курсы валют и акции.
    """
    dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Загрузка настроек пользователя
    settings = get_user_settings()
    user_currencies = settings["user_currencies"]
    user_stocks = settings["user_stocks"]

    # Загрузка и фильтрация операций
    df = load_operations()
    start_date, end_date = get_month_range(dt)
    df_period = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= dt)]

    # Приветствие
    greeting = get_greeting_from_time(dt)

    # Данные по картам
    cards = []
    for card, group in df_period.groupby("Номер карты"):
        spent = group["Сумма платежа"].sum()
        cashback = round(spent * 0.01, 2)
        cards.append(
            {
                "last_digits": str(card)[-4:],
                "total_spent": round(spent, 2),
                "cashback": cashback,
            }
        )

    # Топ-5 транзакций
    top_transactions = df_period.nlargest(5, "Сумма платежа")[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ]
    top_transactions = top_transactions.to_dict(orient="records")

    # Курсы валют и цены акций
    currency_rates = get_currency_rates(user_currencies)
    stock_prices = get_stock_prices(user_stocks)

    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": [
            {
                "date": t["Дата операции"].strftime("%d.%m.%Y"),
                "amount": round(t["Сумма платежа"], 2),
                "category": t["Категория"],
                "description": t["Описание"],
            }
            for t in top_transactions
        ],
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
