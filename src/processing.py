def filter_by_state(data: list[dict[str, str]], state: str ="EXECUTED") -> list[dict[str, str]]:
    """Функция фильтрует список словарей по ключу state"""

    filtered_data = []
    i = 0
    for dictionary in data:
        for key, value in data[i].items():
            if key == "state" and value == state:
                filtered_data.append(data[i])
        i += 1
    return filtered_data


def sort_by_date(date_list: list[dict[str, str]], param: bool = False) -> list[dict[str, str]]:
    """Функция сортирует список словарей по ключу date"""

    sorted_list = sorted(date_list, key=lambda x: x["date"], reverse=param)
    return sorted_list
