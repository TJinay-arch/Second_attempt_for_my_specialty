def get_mask_card_number(input_card: str) -> None:
    """Функция принимает на вход номер и возвращает её маску"""

    # Преобразуем ввод в список символов карты
    card_number = list(input_card)

    # Перебираем индексы
    for i in range(len(card_number)):
        # Если позиция индекса находится между шестым и двенадцатым символом включительно,
        # замещаем её звездочкой (*).
        if 6 <= i <= 11:
            card_number[i] = "*"

    # Формируем итоговую маску с пробелами каждые четыре цифры
    masked_string = "".join(card_number[:4]) + " "
    masked_string += "".join(card_number[4:8]) + " "
    masked_string += "".join(card_number[8:12]) + " "
    masked_string += "".join(card_number[12:16])
    print(masked_string)


def get_mask_account(input_account: str) -> None:
    """Функция принимает на вход номер счета и возвращает его маску"""

    account_number = list(input_account)
    string_output = "".join(account_number[-5:-1])
    print("** " + string_output)
