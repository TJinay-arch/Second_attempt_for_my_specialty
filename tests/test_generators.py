import typing as t

import pytest
from mypy.build import Mapping

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)

TransactionType = t.Dict[str, t.Any]
TransactionsListType = t.List[TransactionType]


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", {939719570, 567890123}),  # Должны вернуть ID двух транзакций в долларах
        ("RUB", {142264268}),  # Одна транзакция в рублях
        ("EUR", {873498234}),  # Одна отменённая транзакция в евро
        ("GBP", set()),  # Нет транзакций в фунтах стерлингов
    ],
)
def test_filter_by_currency(sample_transactions: TransactionsListType, currency: str, expected_ids: set) -> None:
    """Тестирует фильтр по валюте"""
    filtered_transactions = list(filter_by_currency(sample_transactions, currency))
    actual_ids = {tx["id"] for tx in filtered_transactions}
    assert actual_ids == expected_ids, f"Транзакции для валюты '{currency}' некорректны."


TransactionsDescriptionListType = t.List[Mapping]


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ([{"id": 1, "description": "Операция 1"}], ["Операция 1"]),
        ([{"id": 2}, {"id": 3}], ["", ""]),  # Случаи, когда описания отсутствуют
        ([{"id": 4, "description": ""}], [""]),  # Пустой объект описания
        (
            [{"id": 5, "description": "Перечисление"}, {"id": 6, "description": "Оплата услуги"}],
            ["Перечисление", "Оплата услуги"],
        ),
    ],
)
def test_transaction_descriptions(
    input_data: TransactionsDescriptionListType,
    expected_output: list[str],
    sample_transactions_for_description: t.List[t.Dict[str, t.Any]],
) -> None:
    """Тестирование генератора описаний транзакций."""
    generator = transaction_descriptions(input_data)
    results = []
    try:
        while True:
            result = next(generator)
            results.append(result)
    except StopIteration:
        pass
    finally:
        assert (
            results == expected_output
        ), f"Последовательность описаний неверна: ожидалось {expected_output}, получено {results}"


@pytest.mark.parametrize(
    "start,end,expected_result",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (1000, 1001, ["0000 0000 0000 1000", "0000 0000 0000 1001"]),
    ],
)
def test_valid_ranges(valid_range: tuple[int, int], start: int, end: int, expected_result: list[str]) -> None:
    """Тестирование генерации карт с правильными диапазонами."""
    gen = card_number_generator(start, end)
    generated_numbers = list(gen)
    assert generated_numbers == expected_result, "Неверные номера карт!"


def test_invalid_range(invalid_range: tuple[int, int]) -> None:
    """Тестирование попытки превысить лимит (ожидается ошибка)."""
    with pytest.raises(ValueError):
        list(card_number_generator(*invalid_range))  # ожидает ошибку ValueError
