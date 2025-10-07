from typing import Any
from unittest.mock import patch

import pytest
from _pytest.tmpdir import TempPathFactory

from src.external_api import convert_amount, fetch_exchange_rates
from src.utils import load_transactions_from_file


def test_load_transactions_file_not_found() -> None:
    fake_file_path = "/path/to/fake/file.json"
    result = load_transactions_from_file(fake_file_path)
    assert result == [], "Должен вернуть пустой список, если файл не найден"


def test_load_transactions(example_operations_file: TempPathFactory) -> None:
    transactions = load_transactions_from_file(example_operations_file)
    assert len(transactions) == 2
    assert transactions[0]["id"] == 1
    assert transactions[1]["amount"] == 200


@pytest.mark.parametrize(
    "file_fixture, description",
    [
        ("empty_file", "Файл пустой"),
        ("invalid_json_file", "Файл содержит некорректные JSON-данные"),
        ("non_list_json_file", "Файл содержит корректные данные, но не список"),
        (lambda: "/path/to/fake/file.json", "Файл не существует"),
    ],
)
def test_load_transactions_return_empty_list(request: Any, file_fixture: Any, description: str) -> None:
    """
    Параметризованный тест, проверяющий случаи возврата пустого списка.
    """
    if callable(file_fixture):
        file_path = file_fixture()
    else:
        file_path = request.getfixturevalue(file_fixture)

    result = load_transactions_from_file(file_path)
    assert result == [], f"{description}: Должен вернуть пустой список"


@pytest.mark.parametrize(
    "transaction, expected",
    [
        ({"operationAmount.amount": 100, "operationAmount.currency.code": "USD"}, 10000),
        ({"operationAmount.amount": 100, "operationAmount.currency.code": "EUR"}, 8333.33),
    ],
)
def test_convert_amount_with_valid_input(transaction: dict, expected: float) -> None:
    """
    Тест проверяет успешную конвертацию валюты при условии правильного API-ответа.
    """
    with patch("src.external_api.fetch_exchange_rates", return_value={"RUB": 100, "USD": 1, "EUR": 1.2}):
        result = convert_amount(transaction)
        assert round(result, 2) == expected, f"Сумма {result} не равна ожидаемой {expected}"


# Тест на ошибку API
def test_convert_amount_with_error_response() -> None:
    """
    Тест проверяет поведение функции при ошибочном ответе от API.
    """
    transaction = {"operationAmount.amount": 100, "operationAmount.currency.code": "USD"}
    with patch("src.external_api.fetch_exchange_rates", side_effect=RuntimeError("Ошибка при получении данных")):
        with pytest.raises(RuntimeError):
            convert_amount(transaction)


MOCK_RESPONSE_SUCCESS = {"rates": {"RUB": 100, "USD": 1, "EUR": 1.2}, "timestamp": 1638321600}


@patch("src.external_api.requests.get")
def test_fetch_exchange_rates_success(mock_get: Any) -> None:
    # Устанавливаем успешный ответ от API
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = MOCK_RESPONSE_SUCCESS

    # Выполняем функцию
    rates = fetch_exchange_rates()

    # Проверяем результат
    assert rates["RUB"] == 100
    assert rates["USD"] == 1
    assert rates["EUR"] == 1.2


@patch("src.external_api.requests.get")
def test_fetch_exchange_rates_failure(mock_get: Any) -> None:
    # Эмулируем ошибку API
    mock_get.return_value.status_code = 403
    mock_get.return_value.text = "<html>...</html>"

    # Пробуем вызвать функцию и ждем исключения
    with pytest.raises(RuntimeError) as excinfo:
        fetch_exchange_rates()

    # Проверяем сообщение исключения
    assert "Ошибка при получении данных: 403" in str(excinfo.value)
