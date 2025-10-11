import pprint

from src.file_reader import file_reader_csv, file_reader_excel

if __name__ == "__main__":
    print("\nДанные из csv-файла\n")
    file = file_reader_csv("./data/transactions.csv")
    pprint.pprint(file[:2])
    print("\nДанные из excel-файла\n")
    file_excel = file_reader_excel("./data/transactions_excel.xlsx")
    pprint.pprint(file_excel[:2])
