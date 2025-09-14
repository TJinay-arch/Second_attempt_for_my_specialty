import pytest


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
def data_fixture(request):
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
def date_input_output(request):
    return request.param

@pytest.fixture
def transactions_data():
    return [
        {
            'id': 41428829,
            'state': 'EXECUTED',
            'date': '2019-07-03T18:35:29.512364'
        },
        {
            'id': 939719570,
            'state': 'EXECUTED',
            'date': '2018-06-30T02:08:58.425572'
        },
        {
            'id': 594226727,
            'state': 'CANCELED',
            'date': '2018-09-12T21:27:25.241689'
        },
        {
            'id': 615064591,
            'state': 'CANCELED',
            'date': '2018-10-14T08:21:33.419441'
        }
    ]

@pytest.fixture
def sorting_data():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]