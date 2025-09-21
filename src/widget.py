from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_number: str) -> str:
    """Функция обрабатывает информацию как о счетах, так и номерах карт"""
    if input_number == "":
        return "Error"

    parts = input_number.split()

    checking_part = parts[-1]

    if parts[0] == "Счет":
        if len(checking_part) != 20:
            return "Your input is incorrect"
        name_part: str = " ".join(parts[:-1])
        account_part: str = get_mask_account(parts[-1])
        return f"{name_part} {account_part}"
    else:
        if len(checking_part) != 16:
            return "Your input is incorrect"
        name_of_a_card_part: str = " ".join(parts[:-1])
        card_part: str = get_mask_card_number(parts[-1])
        return f"{name_of_a_card_part} {card_part}"


def get_date(input_string: str) -> str:
    """
    Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024").
    """
    if len(input_string.strip()) == 0 or "-" not in input_string:
        return "Error"

    # Разделяем строку по символу "-"
    parts = input_string.split("-")

    # Проверяем, чтобы было ровно три компонента (год, месяц, день)
    if len(parts) != 3:
        return "Error"

    try:
        year = int(parts[0].strip())
        month = int(parts[1].strip())
        day_part = parts[2].split("T")[0].strip()
        day = int(day_part)
    except ValueError:
        return "Error"

    # Простые проверки на существование даты
    if month > 12 or month <= 0:
        return "Error"
    elif day > 31 or day <= 0:
        return "Error"
    else:
        # Если всё хорошо, формируем выходную строку
        return f"{day:02d}.{month:02d}.{year}"
