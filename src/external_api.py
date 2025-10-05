import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "http://api.exchangeratesapi.io/v1/latest"


def fetch_exchange_rates() -> Any:
    """
    Получение текущих курсов валют.
    """
    params = {"access_key": API_KEY, "symbols": "RUB,EUR,USD", "format": 1}
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise RuntimeError(
            f"Ошибка при получении данных: {response.status_code}. Ответ сервера: {response.text[:100]}..."
        )
    rates = response.json().get("rates", {})
    return rates


def convert_amount(amount: Any, currency: Any) -> float:
    """
    Конвертация суммы в нужную валюту.
    """
    rates = fetch_exchange_rates()
    if currency.upper() in ["USD", "EUR"]:
        rub_rate = rates["RUB"]  # Курс рубля
        base_currency_rate = rates[currency.upper()]  # Текущий курс нужной валюты
        converted_amount = amount * (rub_rate / base_currency_rate)
        return float(converted_amount)
    elif currency.upper() == "RUB":
        return float(amount)
    else:
        raise ValueError(f"Валюта '{currency}' не поддерживается.")
