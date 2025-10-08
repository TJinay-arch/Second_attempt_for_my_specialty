from src.external_api import convert_amount
from src.external_api import fetch_exchange_rates

if __name__ == "__main__":
    a = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
          "amount": "100",
          "currency": {
            "name": "USD",
            "code": "USD"
          }
        }
    }
    b = {
        "id": 596171168,
        "state": "EXECUTED",
        "date": "2018-07-11T02:26:18.671407",
        "operationAmount": {
          "amount": "100",
          "currency": {
            "name": "руб.",
            "code": "RUB"
          }
        }
    }
    c = {
        "id": 782295999,
        "state": "EXECUTED",
        "date": "2019-09-11T17:30:34.445824",
        "operationAmount": {
          "amount": "100",
          "currency": {
            "name": "EUR",
            "code": "EUR"
          }
        }
    }
    print(convert_amount(c))
    print(convert_amount(a))
    print(fetch_exchange_rates())