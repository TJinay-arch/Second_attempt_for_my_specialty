import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Поиск транзакций по заданной строке с помощью регулярных выражений"""

    pattern = re.compile(search, re.IGNORECASE)

    filtered_data = [item for item in data if pattern.search(item["description"])]

    return filtered_data


def process_bank_operations(data: list[dict], categories: list[str]) -> dict:
    """Подсчитывает количество операций по каждому типу из указанного списка категорий"""

    filtered_descriptions = [op["description"] for op in data if op["description"] in categories]

    counts = Counter(filtered_descriptions)

    result = {cat: counts.get(cat, 0) for cat in categories}

    return result
