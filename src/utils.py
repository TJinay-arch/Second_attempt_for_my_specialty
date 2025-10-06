import json
import logging
import os
from typing import Any

utils_logger = logging.getLogger("utils.py")
utils_logger.setLevel(logging.DEBUG)


log_directory = r"C:\Users\ilya-\PycharmProjects\bank_module\logs"
os.makedirs(log_directory, exist_ok=True)
log_filename = os.path.join(log_directory, "utils.log")
get_mask_handler = logging.FileHandler(log_filename, mode="w")


file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
get_mask_handler.setFormatter(file_formatter)

utils_logger.addHandler(get_mask_handler)


def load_transactions_from_file(file_path: Any) -> list:
    """
    Функция принимает путь до JSON-файла и возвращает список словарей с данными о транзакциях.
    Если файл не найден, пустой или содержит не список, возвращает пустой список.
    """
    if not os.path.exists(file_path):
        utils_logger.error("Os path isn't exists (str - 29)\n")
        return []  # Если файл не существует, возвращаем пустой список

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content.strip():  # Проверяем, не пустой ли файл
                return []

            transactions = json.loads(content)
            if not isinstance(transactions, list):
                utils_logger.error("Format of data isn't a list (str - 40) \n")
                return []  # Если данные не представляют собой список, возвращаем пустой список
            utils_logger.info(f"Function ends with the result {transactions} \n")
            return transactions
    except json.JSONDecodeError:
        utils_logger.error("Format of data isn't json (str - 44) \n")
        return []  # Если файл содержит некорректные JSON-данные, возвращаем пустой список
