from collections.abc import Generator, Iterator, Mapping
from typing import Any


def filter_by_currency(transactions: list[dict], currency_code: str) -> Iterator[dict]:
    """Функция возвращает генератор, фильтрующий транзакции по валюте"""
    for transaction in transactions:
        # Проверяем наличие нужных полей и совпадение валюты
        if (transaction.get("operationAmount", {}).get("currency", {}).get("code")) == currency_code:
            yield transaction


def transaction_descriptions(transactions: list[Mapping]) -> Iterator[str]:
    """Генерирует описания транзакций по порядку"""
    for transaction in transactions:
        description = transaction.get("description", "")
        yield description


def card_number_generator(start: int, end: int) -> Generator[str, Any, None]:
    """
    Генератор номеров банковских карт в диапазоне от start до end включительно.
    Ограничено значением 9999 9999 9999 9999.
    """
    max_card_number = 9999_9999_9999_9999
    if not (0 <= start <= max_card_number and 0 <= end <= max_card_number):
        raise ValueError(f"Диапазон должен находиться в пределах от 0 до {max_card_number}.")

    current_value = start
    while current_value <= end:
        formatted_card_number = "{:016d}".format(current_value)
        yield "{} {} {} {}".format(
            formatted_card_number[:4],
            formatted_card_number[4:8],
            formatted_card_number[8:12],
            formatted_card_number[12:],
        )
        current_value += 1
