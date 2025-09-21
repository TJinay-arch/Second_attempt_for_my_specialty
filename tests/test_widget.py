import pytest
from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account_or_card, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет ** 4305"),
        ("Счет 736541084301358", "Your input is incorrect"),
        ("", "Error"),
        ("Visa Platinum 1345", "Your input is incorrect"),
    ],
)
def test_mask_account_card(account_or_card: str, expected: str) -> None:
    assert mask_account_card(account_or_card) == expected


def test_get_date(date_input_output: tuple[str, str]) -> None:
    """
    Тестируем правильность преобразования даты с разными случаями.
    """
    input_string, expected_result = date_input_output

    result = get_date(input_string)
    assert result == expected_result, f"Неправильное преобразование даты {input_string}, ожидалось {expected_result}"
