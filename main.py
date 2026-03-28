from src.file_reader import file_reader_csv, file_reader_excel
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.searchers import process_bank_search
from src.utils import load_transactions_from_file
from src.widget import get_date, mask_account_card


def main() -> None:
    """Функция сортирующая банковские операции по запросам пользователя"""

    print(
        """Привет! Добро пожаловать в программу работы с банковскими транзакциями. 
    Выберите необходимый пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла"""
    )
    users_answer = input()
    # Выбор пользователя
    try:
        if users_answer == "1":
            print("Для обработки выбран JSON-файл.")
            transactions = load_transactions_from_file("./data/operations.json")
            print(transactions)
        elif users_answer == "2":
            print("Для обработки выбран CSV-файл.")
            transactions = file_reader_csv("./data/transactions.csv")
        elif users_answer == "3":
            print("Для обработки выбран XLSX-файл.")
            transactions = file_reader_excel("./data/transactions_excel.xlsx")
        else:
            raise ValueError("Неверный выбор формата файла.")
    except Exception as e:
        print(f"Произошла ошибка: {e} Проверьте правильность ввода пути к файлу.")

    while True:
        status = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию.\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            )
            .strip()
            .upper()
        )
        valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
        if status not in valid_statuses:
            print(f"Статус операции '{status}' недоступен.")
        else:
            break

    transactions = filter_by_state(transactions, status)
    print(f"Операции отфильтрованы по статусу {status}")
    print(transactions)
    sorting_choice = input("Отсортировать операции по дате? Да/Нет ").strip().lower()
    if sorting_choice == "да":
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        ascending = True if order == "возрастанию" else False
        transactions = sort_by_date(transactions, ascending)
    print(transactions)
    ruble_filter = input("Выводить только рублевые транзакции? Да/Нет ").strip().lower()
    if ruble_filter == "да":
        transactions = list(filter_by_currency(transactions, "RUB"))
    print(transactions)
    description_filter = (
        input("Отфильтровать список транзакций по определённому слову в описании? Да/Нет ").strip().lower()
    )
    if description_filter == "да":
        description = input("Введите ключевое слово для фильтрации: ").strip().lower()
        transactions = process_bank_search(transactions, description)
    print(transactions)
    if len(list(transactions)) > 0:
        print("\nРаспечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(transactions)}\n")
        for elem in transactions:
            date = get_date(elem["date"])
            # Проверяем наличие полей 'from' и 'to'. Если их нет, ставим '--'.
            masked_data_from = mask_account_card(elem.get("from", "--"))
            masked_data_to = mask_account_card(elem.get("to", "--"))
            amount = elem["operationAmount"]["amount"]
            if elem["operationAmount"]["currency"]["code"] == "RUB":
                code = "руб."
            else:
                code = elem["operationAmount"]["currency"]["code"]
            if "Открытие" in elem["description"]:
                print(f"{date} {elem['description']}\n{masked_data_to}\nСумма: {amount} {code}\n")
            else:
                print(
                    f"{date} {elem['description']}\n{masked_data_from} -> {masked_data_to}\nСумма: {amount} {code}\n"
                )
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


if __name__ == "__main__":
    main()
