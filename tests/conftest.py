import typing as t
from collections.abc import Generator
from typing import Any

import pandas as pd
import pytest
from _pytest.tmpdir import Path, TempPathFactory
from pandas import DataFrame


@pytest.fixture(
    params=[
        # валидный номер карты
        ("12345678901234567890", "** 7890"),
        # ещё один валидный номер карты
        ("00000000000000000000", "** 0000"),
        # пустое поле
        ("", "Your input is incorrect"),
        # неверный ввод (пробел впереди)
        (" 1234567890123456", "Your input is incorrect"),
        # короткий номер
        ("1234", "Your input is incorrect"),
        # неправильный формат ввода
        ("dddddddddddddddd", "Your input is incorrect"),
    ]
)
def data_fixture(request: Any) -> Any:
    return request.param


@pytest.fixture(
    params=[
        # Нормальные случаи
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-12-31T23:59:59.999999", "31.12.2025"),
        # Граничные случаи
        ("2024-01-01T00:00:00.000000", "01.01.2024"),  # начало года
        ("2024-12-31T23:59:59.999999", "31.12.2024"),  # конец года
        # Нестандартные форматы ввода
        ("2024-03-11", "11.03.2024"),  # короткий формат
        ("2024-03-11T", "11.03.2024"),  # неполная строка
        # Некорректные значения
        ("", "Error"),  # пустая строка
        ("abc-def-ghi", "Error"),  # неверный формат
        ("2024-13-01", "Error"),  # несуществующая дата
    ]
)
def date_input_output(request: Any) -> Any:
    return request.param


@pytest.fixture
def transactions_data() -> list[dict[str, int | str]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def sorting_data() -> list[dict[str, int | str]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


TransactionType = t.Dict[str, t.Any]
TransactionsListType = t.List[TransactionType]


@pytest.fixture
def sample_transactions() -> TransactionsListType:
    """Возвращает пример списка транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873498234,
            "state": "CANCELED",
            "date": "2020-07-15T10:30:00.000000",
            "operationAmount": {"amount": "1500.00", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Отмененная операция",
            "from": None,
            "to": None,
        },
        {
            "id": 567890123,
            "state": "EXECUTED",
            "date": "2021-01-01T00:00:00.000000",
            "operationAmount": {"amount": "5000.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Покупка товара",
            "from": "Счет 9876543210",
            "to": "Счет 0123456789",
        },
    ]


@pytest.fixture
def sample_transactions_for_description() -> list[dict[str, int | str]]:
    """Фикстура, возвращающая образец списка транзакций."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Перевод со счета на счет"},
        {"id": 4, "description": "Перевод с карты на карту"},
        {"id": 5, "description": "Перевод организации"},
    ]


@pytest.fixture
def valid_range() -> tuple[int, int]:
    """Предоставляет валидный диапазон номеров для тестов."""
    return (1, 5)


@pytest.fixture
def invalid_range() -> tuple[int, int]:
    """Предоставляет диапазон, превышающий лимит (некорректный)."""
    return (1, 10000000000000000)


@pytest.fixture(scope="session")
def example_operations_file(tmpdir_factory: TempPathFactory) -> str:
    temp_dir = tmpdir_factory.mktemp("data")
    filename = temp_dir / "operations.json"
    filename.write_text('[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]', encoding="utf-8")
    return str(filename)


@pytest.fixture
def empty_file(tmp_path: Path) -> Generator[str, Any, None]:
    file_path = tmp_path / "empty.json"
    file_path.touch()
    yield str(file_path)
    file_path.unlink(missing_ok=True)


@pytest.fixture
def invalid_json_file(tmp_path: Path) -> Generator[str, Any, None]:
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{this_is_not_valid_json}")
    yield str(file_path)
    file_path.unlink(missing_ok=True)


@pytest.fixture
def non_list_json_file(tmp_path: Path) -> Generator[str, Any, None]:
    file_path = tmp_path / "nonlist.json"
    file_path.write_text('{"key": "value"}')
    yield str(file_path)
    file_path.unlink(missing_ok=True)


# Для тестирования чтения данных из csv-файла (модуль - test_file_reader)
@pytest.fixture
def csv_content() -> str:
    return (
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;"
        "Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации\n"
        "3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;COP;"
        "Discover 3172601889670065;Discover 0720428384694643;Перевод с карты на карту\n"
    )


# Для тестирования чтения данных из csv-файла (модуль - test_file_reader)
@pytest.fixture
def excel_dataframe() -> DataFrame:
    return pd.DataFrame(
        [
            {
                "amount": 16210.0,
                "currency_code": "PEN",
                "currency_name": "Sol",
                "date": "2023-09-05T11:30:32Z",
                "description": "Перевод организации",
                "from": "Счет 58803664561298323391",
                "id": 650703.0,
                "state": "EXECUTED",
                "to": "Счет 39745660563456619397",
            },
            {
                "amount": 29740.0,
                "currency_code": "COP",
                "currency_name": "Peso",
                "date": "2020-12-06T23:00:58Z",
                "description": "Перевод с карты на карту",
                "from": "Discover 3172601889670065",
                "id": 3598919.0,
                "state": "EXECUTED",
                "to": "Discover 0720428384694643",
            },
        ]
    )


# Для тестирования функции process_bank_search
@pytest.fixture(scope="module")
def operations() -> list:
    """Фикстура с примерами банковских операций."""
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Оплата услуг",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
        {
            "id": 939719570,
            "state": "CANCELED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Пополнение счета",
            "from": None,
            "to": "Счет 48894435692658808621",
        },
    ]
