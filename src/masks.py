import logging
import os

get_mask_logger = logging.getLogger("masks.py")
get_mask_logger.setLevel(logging.DEBUG)


log_directory = r"C:\Users\ilya-\PycharmProjects\bank_module\logs"
os.makedirs(log_directory, exist_ok=True)
log_filename = os.path.join(log_directory, "masks.log")
get_mask_handler = logging.FileHandler(log_filename, mode="w")


file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
get_mask_handler.setFormatter(file_formatter)

get_mask_logger.addHandler(get_mask_handler)


def get_mask_card_number(input_card: str) -> str:
    """Функция принимает на вход номер и возвращает её маску"""

    # Удаляем все пробелы из исходной строки
    card_number_replaced = input_card.replace(" ", "")

    # Преобразуем в список для дальнейшей обработки
    card_number = list(card_number_replaced)

    # Проверка корректности ввода номера карты
    for item in card_number:
        if item not in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            get_mask_logger.error("User's input is incorrect (str - 32)\n")
            return "Your input is incorrect"

    # Проверка граничных случаев и маскировка номера карты
    if len(card_number) == 16:
        for i in range(len(card_number)):
            if 6 <= i <= 11:
                card_number[i] = "*"

        # Формируем итоговую строку с пробелами между группами цифр
        masked_string = "".join(card_number[:4]) + " "
        masked_string += "".join(card_number[4:8]) + " "
        masked_string += "".join(card_number[8:12]) + " "
        masked_string += "".join(card_number[12:16])

        get_mask_logger.info(f"Function ends with the result {masked_string} \n")
        return masked_string
    else:
        get_mask_logger.error("User's input is incorrect (str - 50)\n")
        return "Your input is incorrect"


def get_mask_account(input_account: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""

    account_number = list(input_account)

    # Проверка корректности ввода номера счета
    for item in account_number:
        if item not in (" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            get_mask_logger.error("User's input is incorrect (str - 62)\n")
            return "Your input is incorrect"
    if len(account_number) != 20 or account_number[0] == " ":
        get_mask_logger.error("User's input is incorrect (str - 65)\n")
        return "Your input is incorrect"

    string_output = "** " + "".join(account_number[-4:])
    get_mask_logger.info(f"Function ends with the result {string_output} \n")
    return string_output
