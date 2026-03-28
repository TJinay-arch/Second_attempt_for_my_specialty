import csv
from typing import Any

import pandas as pd


def file_reader_csv(file_path: Any) -> list:
    """Функция для чтения данных о финансовых транзакциях из csv-файла"""

    try:
        data_list = []

        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            for row in reader:
                data_list.append(row)

        return data_list

    except FileNotFoundError:
        print("File not found, try again")
        return []


def file_reader_excel(file_path: Any) -> list[Any]:
    """Функция для чтения данных о финансовых транзакциях из excel-файла"""

    try:
        excel_data = pd.read_excel(file_path).head()
        data_list = excel_data.to_dict(orient="records")
        return data_list
    except FileNotFoundError:
        print("File not found, try again")
        return []
