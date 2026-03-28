import logging
from typing import Any


def log(filename: str = "console") -> Any:
    """Декоратор с параметром обеспечивающий логирование в файл или консоль"""

    def decorator(func: Any) -> Any:
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
            if filename == "console":
                try:
                    logging.basicConfig(
                        level=logging.INFO, filemode="w", format="%(asctime)s %(levelname)s %(message)s"
                    )
                    logging.info("Function starts")
                    result = func(*args, **kwargs)
                    message_1 = f"Function ends with the result {result}"
                    logging.info(message_1)
                    return result
                except Exception as e:
                    logging.exception(
                        f"Function works incorrect, the exception is {e}, input params {args} and {kwargs}"
                    )
            else:
                try:
                    logging.basicConfig(
                        level=logging.INFO,
                        filename=f"{filename}",
                        filemode="a",
                        format="%(asctime)s %(levelname)s %(message)s",
                    )
                    logging.info("Function starts")
                    result = func(*args, **kwargs)
                    message_2 = f"Function ends with the result {result} \n"
                    logging.info(message_2)
                    return result
                except Exception as e:
                    logging.exception(
                        f"Function works incorrect, the exception is {e}, input params {args} and {kwargs}"
                    )

        return wrapper

    return decorator
