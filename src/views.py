# src/views.py
from fastapi import APIRouter, HTTPException

from src.utils import load_transactions_from_excel

router = APIRouter()


@router.get("/operations")
def get_operations() -> list[dict]:
    transactions = load_transactions_from_excel("data/operations3.xlsx")
    if not transactions:
        raise HTTPException(status_code=404, detail="Нет данных о транзакциях")
    return transactions
