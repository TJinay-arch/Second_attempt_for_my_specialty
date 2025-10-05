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
            content = file.read()
            if not content.strip():  # Проверяем, не пустой ли файл
                return []

            transactions = json.loads(content)
            if not isinstance(transactions, list):
                return []  # Если данные не представляют собой список, возвращаем пустой список
            return transactions
    except json.JSONDecodeError:
        return []  # Если файл содержит некорректные JSON-данные, возвращаем пустой список
