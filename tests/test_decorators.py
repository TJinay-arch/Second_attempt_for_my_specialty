import logging
import os
import sys
import time

from _pytest.capture import CaptureFixture

from src.decorators import decorator_for_logging


# Тест вывода в консоль
# Тест вывода в консоль
def test_console_output(capsys: CaptureFixture[str]) -> None:
    """Тестирует вывод в консоль и сравнивает результат работы функции get_mask_account"""

    # Очистим кэшированные логгеры, иначе предыдущий вывод повлияет на новый
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Включаем ведение логов в stdout (это важно!)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # Декорируем функцию для вывода в консоль
    @decorator_for_logging()
    def get_mask_account(input_account: str) -> str:
        """Функция принимает на вход номер счета и возвращает его маску"""
        account_number = list(input_account)

        # Проверка корректности ввода номера счета
        for item in account_number:
            if item not in (" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                return "Your input is incorrect"
        if len(account_number) != 20 or account_number[0] == " ":
            return "Your input is incorrect"

        string_output = "** " + "".join(account_number[-4:])
        return string_output

    # Вызываем декорированную функцию
    result = get_mask_account("12345678901234567890")

    # Захватываем вывод
    captured = capsys.readouterr()

    # Проверяем вывод в stdout
    expected_message = "Function starts\n"
    assert expected_message in captured.out

    # Проверяем результат функции
    assert result == "** 7890"


# Тест вывода в файл
def test_file_output() -> None:
    """Тестирует запись логов в файл log.log и сравнивает результат работы функции"""

    file_log = r"C:\Users\ilya-\PycharmProjects\bank_module\log.log"

    if os.path.exists(file_log):
        os.remove(file_log)

    # Предотвращаем конфликты с предыдущей конфигурацией логирования
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    @decorator_for_logging(filename="log.log")
    def get_mask_account(input_account: str) -> str:
        """Функция принимает на вход номер счета и возвращает его маску"""
        account_number = list(input_account)

        # Проверка корректности ввода номера счета
        for item in account_number:
            if item not in (" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                return "Your input is incorrect"
        if len(account_number) != 20 or account_number[0] == " ":
            return "Your input is incorrect"

        string_output = "** " + "".join(account_number[-4:])
        return string_output

    # Явно переустанавливаем конфигурацию логирования для этого теста
    logging.basicConfig(
        level=logging.INFO, filename=file_log, filemode="a", format="%(asctime)s %(levelname)s %(message)s"
    )
    # Вызываем декорированную функцию
    result = get_mask_account("12345678901234567890")

    time.sleep(0.1)

    with open(file_log, "r") as file:
        content = file.read()

    # Проверяем наличие нужных сообщений в файле
    assert "Function starts" in content
    assert f"Function ends with the result {result} \n" in content

    assert result == "** 7890"
