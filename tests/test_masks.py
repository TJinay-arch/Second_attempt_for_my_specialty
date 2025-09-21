import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("", "Your input is incorrect"),
        (" 1234567890123456", "1234 56** **** 3456"),
        ("1234", "Your input is incorrect"),
        ("dddddddddddddddd", "Your input is incorrect"),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


def test_get_mask_account(data_fixture: tuple[str, str]) -> None:
    account_number, expected = data_fixture
    assert get_mask_account(account_number) == expected
