import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state,expected",
    [
        # Фильтрация по состоянию EXECUTED
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        # Фильтрация по состоянию CANCELED
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        # Отсутствие записей с определенным состоянием
        ("PROCESSING", []),
    ],
)
def test_filter_by_state(transactions_data: list[dict[str, str]], state: str, expected: str) -> None:
    assert filter_by_state(transactions_data, state) == expected


@pytest.mark.parametrize(
    "data,reverse,expected",
    [
        # Нормальное тестирование сортировки
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        # Тест на одинаковые даты
        (
            [
                {"id": 1, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 2, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 3, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
            ],
            False,
            [
                {"id": 1, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 2, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
                {"id": 3, "state": "EXECUTED", "date": "2022-01-01T12:00:00"},
            ],
        ),
    ],
)
def test_sort_by_date(data: list[dict[str, str]], reverse: bool, expected: list[dict[str, str]]) -> None:
    assert sort_by_date(data, reverse) == expected
