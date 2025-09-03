from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(input_number: str) -> str:
    """Функция обрабатывает информацию как о счетах, так и номерах карт"""

    parts = input_number.split()
    if parts[0] == "Счет":
        name_part: str = "".join(parts[:-1])
        account_part: str = get_mask_account(parts[-1])
        return f"{name_part} {account_part}"
    else:
        name_of_a_card_part: str = "".join(parts[:-1])
        card_part: str = get_mask_card_number(parts[-1])
        return f"{name_of_a_card_part} {card_part}"


def get_date(input_string: str) -> str:
    """функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"("11.03.2024")"""

    parts_of_data = input_string.split("-")
    year_from_string = parts_of_data[-1]
    output_date = year_from_string[0:2] + "."
    output_date += "".join(parts_of_data[1]) + "."
    output_date += "".join(parts_of_data[0])

    return output_date
