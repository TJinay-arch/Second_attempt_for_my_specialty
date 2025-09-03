def get_mask_card_number(input_card: str) -> str:
    """Функция принимает на вход номер и возвращает её маску"""

    card_number = list(input_card)

    for i in range(len(card_number)):
        if 6 <= i <= 11:
            card_number[i] = "*"

    masked_string = "".join(card_number[:4]) + " "
    masked_string += "".join(card_number[4:8]) + " "
    masked_string += "".join(card_number[8:12]) + " "
    masked_string += "".join(card_number[12:16])

    return masked_string


def get_mask_account(input_account: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""

    account_number = list(input_account)
    string_output = "** " + "".join(account_number[-5:-1])

    return string_output
