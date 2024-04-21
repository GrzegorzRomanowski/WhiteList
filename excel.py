import pandas as pd
import openpyxl

from validations import only_digits, is_bank_account_valid


class BulkData:
    def __init__(self):
        self.df = pd.read_excel(r"data/input.xlsx")

    def make_list_for_browser(self) -> list:
        accounts_list = self.df["Numer konta"].to_list()
        accounts_list = [only_digits(account) for account in accounts_list if is_bank_account_valid(account)]
        self.df["Rezultat"] = self.df["Numer konta"].apply(
            lambda x: "" if is_bank_account_valid(x) else "BŁĘDNY NUMER KONTA")
        return accounts_list

    def write_scraped_data_to_df(self, results: dict):
        pass


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    bulk_data_obj = BulkData()
    print(bulk_data_obj.make_list_for_browser())
    print(bulk_data_obj.df)
