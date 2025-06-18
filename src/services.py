import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.utils import logger

# Загрузка переменных окружения
load_dotenv()


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли (RUB) с использованием API CurrencyFreaks.

    :param transaction: Словарь операции:
                        {
                            "operationAmount": {
                                "amount": "100.00",
                                "currency": {"code": "USD"}
                            }
                        }
    :return: Сумма в рублях (float).
    """
    amount_str = transaction["operationAmount"]["amount"]
    currency_code = transaction["operationAmount"]["currency"]["code"]
    amount = float(amount_str)

    if currency_code == "RUB":
        return amount

    api_key = os.getenv("CURRENCY_API_KEY")
    if not api_key:
        raise RuntimeError("API ключ для конвертации валюты не найден")

    url = f"https://api.currencyfreaks.com/latest" f"?apikey={api_key}&symbols=RUB&base={currency_code}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        rate = float(data["rates"]["RUB"])
        return round(amount * rate, 2)

    except Exception as e:
        logger.error(f"💱 Ошибка при конвертации {currency_code} → RUB: {e}")
        raise RuntimeError(f"Ошибка при конвертации {currency_code} → RUB")
