import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def fetch_exchange_rates() -> Any:
    """
    Получение текущих курсов валют.
    """
    params = {"base": "RUB", "symbols": "USD,EUR", "apikey": API_KEY}
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise RuntimeError(
            f"Ошибка при получении данных: {response.status_code}. Ответ сервера: {response.text[:100]}..."
        )
    rates = response.json().get("rates", {})
    return rates


def convert_amount(transaction: Dict[str, Any]) -> float:
    """
    Конвертация суммы транзакции в нужную валюту.
    """
    amount = float(transaction.get("operationAmount", {}).get("amount", 0))
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", "").upper()

    rates = fetch_exchange_rates()
    if currency in ["USD", "EUR"]:
        base_currency_rate = rates[currency]
        converted_amount = float(amount / base_currency_rate)
        return round(converted_amount, 2)
    elif currency == "RUB":
        return amount
    else:
        raise ValueError(f"Валюта '{currency}' не поддерживается.")
