import json
import os
from typing import Any
import logging


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
        utils_logger.error("Os path isn't exists (str - 28)\n")
        return []  # Если файл не существует, возвращаем пустой список

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content.strip():  # Проверяем, не пустой ли файл
                return []

            transactions = json.loads(content)
            if not isinstance(transactions, list):
                utils_logger.error("Format of data isn't a list (str - 39) \n")
                return []  # Если данные не представляют собой список, возвращаем пустой список
            return transactions
    except FileNotFoundError:
        utils_logger.error("File not found (str - 43) \n")
        return []  # Возврат пустого списка, если файл не найден
    except json.JSONDecodeError:
        utils_logger.error("Format of data isn't json (str - 46) \n")
        return []  # Если файл содержит некорректные JSON-данные, возвращаем пустой список
