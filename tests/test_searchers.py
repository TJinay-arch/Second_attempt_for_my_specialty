import pytest

from src.searchers import process_bank_operations, process_bank_search


@pytest.mark.parametrize(
    "search_term, expected_result",
    [
        (
            "организации",
            [
                {
                    "id": 441945886,
                    "state": "EXECUTED",
                    "date": "2019-08-26T10:50:58.294041",
                    "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод организации",
                    "from": "Maestro 1596837868705199",
                    "to": "Счет 64686473678894779589",
                }
            ],
        ),
        (
            "услуг",
            [
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                    "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Оплата услуг",
                    "from": "MasterCard 7158300734726758",
                    "to": "Счет 35383033474447895560",
                }
            ],
        ),
        ("отсутствует", []),
    ],
)
def test_process_bank_search(operations: list, search_term: str, expected_result: list) -> None:
    assert process_bank_search(operations, search_term) == expected_result


@pytest.mark.parametrize(
    "categories, expected_result",
    [
        (["Перевод организации", "Оплата услуг"], {"Перевод организации": 1, "Оплата услуг": 1}),
        (
            ["Операция перевода", "Пополнение счета"],  # Один из запросов отсутствует
            {"Операция перевода": 0, "Пополнение счета": 1},
        ),
        (["Категория отсутствует"], {"Категория отсутствует": 0}),  # Полностью пустые категории
    ],
)
def test_process_bank_operations(operations, categories, expected_result):
    result = process_bank_operations(operations, categories)
    assert result == expected_result
