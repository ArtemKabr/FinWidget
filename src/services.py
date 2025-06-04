import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.utils import logger  # если логгер подключен

load_dotenv()


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли (RUB) по курсу ЦБ или API.

    :param transaction: Словарь операции с полями:
                        {
                          "operationAmount": {
                            "amount": "100.00",
                            "currency": { "code": "USD" }
                          }
                        }
    :return: Сумма в рублях.
    """
    amount_str = transaction["operationAmount"]["amount"]
    currency_code = transaction["operationAmount"]["currency"]["code"]

    amount = float(amount_str)
    if currency_code == "RUB":
        return amount

    api_key = os.getenv("CURRENCY_API_KEY")
    if not api_key:
        raise RuntimeError("API ключ для конвертации валюты не найден")

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency_code}&symbols=RUB"
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        rate = data["rates"]["RUB"]
        return float(round(amount * rate, 2))

    except Exception as e:
        logger.error(f"Ошибка при конвертации {currency_code} → RUB: {e}")
        raise
