import pandas as pd

DATABASE = "data/database_scheduler.xlsx"


def load_database():
    """
    Membaca seluruh sheet pada file Excel
    """

    data = {}

    excel = pd.ExcelFile(DATABASE)

    for sheet in excel.sheet_names:
        data[sheet] = pd.read_excel(DATABASE, sheet_name=sheet)

    return data


if __name__ == "__main__":

    database = load_database()

    print("===== SHEET YANG DITEMUKAN =====")

    for nama_sheet in database:
        print(nama_sheet)
