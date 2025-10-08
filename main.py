from src.external_api import fetch_exchange_rates
from src.utils import load_transactions_from_file

#print(fetch_exchange_rates())
print(load_transactions_from_file(r"C:\Users\ilya-\PycharmProjects\bank_module\data\operations.json"))