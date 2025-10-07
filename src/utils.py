import json
import os
from typing import Any


def load_transactions_from_file(file_path: Any) -> list:
    """
    Функция принимает путь до JSON-файла и возвращает список словарей с данными о транзакциях.
    Если файл не найден, пустой или содержит не список, возвращает пустой список.
    """
    if not os.path.exists(file_path):
        return []  # Если файл не существует, возвращаем пустой список

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            transactions = json.load(file)  # Используем json.load(), так как работаем с файлом
            if not isinstance(transactions, list):
                return []  # Если данные не являются списком, возвращаем пустой список
            return transactions
    except FileNotFoundError:
        return []  # Возврат пустого списка, если файл не найден
    except json.JSONDecodeError:
        return []  # Возврат пустого списка, если файл содержит некорректные JSON-данные
