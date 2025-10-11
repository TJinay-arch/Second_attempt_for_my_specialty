from unittest.mock import mock_open, patch

import pytest
from pandas.core.interchange.dataframe_protocol import DataFrame

from src.file_reader import file_reader_csv, file_reader_excel


@pytest.mark.parametrize(
    "input_file,expected_result",
    [
        (
            "test.csv",
            [
                {
                    "amount": "16210",
                    "currency_code": "PEN",
                    "currency_name": "Sol",
                    "date": "2023-09-05T11:30:32Z",
                    "description": "Перевод организации",
                    "from": "Счет 58803664561298323391",
                    "id": "650703",
                    "state": "EXECUTED",
                    "to": "Счет 39745660563456619397",
                },
                {
                    "amount": "29740",
                    "currency_code": "COP",
                    "currency_name": "Peso",
                    "date": "2020-12-06T23:00:58Z",
                    "description": "Перевод с карты на карту",
                    "from": "Discover 3172601889670065",
                    "id": "3598919",
                    "state": "EXECUTED",
                    "to": "Discover 0720428384694643",
                },
            ],
        ),
        ("nonexistent.csv", []),
    ],
)
def test_file_reader_csv(input_file: str, expected_result: list, csv_content: str) -> None:
    if input_file != "nonexistent.csv":
        m = mock_open(read_data=csv_content)
        with patch("builtins.open", m):
            result = file_reader_csv(input_file)
    else:
        with patch("builtins.open", side_effect=FileNotFoundError()):
            result = file_reader_csv(input_file)

    assert result == expected_result


@pytest.mark.parametrize(
    "input_file,expected_result",
    [
        (
            "test.xls",
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
            ],
        ),
        ("nonexistent.xls", []),
    ],
)
def test_file_reader_excel(input_file: str, expected_result: list, excel_dataframe: DataFrame) -> None:
    if input_file != "nonexistent.xls":
        with patch("pandas.read_excel", return_value=excel_dataframe):
            result = file_reader_excel(input_file)
    else:
        with patch("pandas.read_excel", side_effect=FileNotFoundError()):
            result = file_reader_excel(input_file)

    assert result == expected_result
