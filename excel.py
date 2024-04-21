import pandas as pd
import openpyxl

from validations import only_digits, is_bank_account_valid


class BulkData:
    def __init__(self):
        self.input_df = pd.read_excel(r"data/input.xlsx")

    def make_list_for_browser(self):
        accounts_list = self.input_df["Numer konta"].to_list()
        accounts_list = [only_digits(account) for account in accounts_list if is_bank_account_valid(account)]
        return accounts_list

    def write_errors_to_df(self):
        pass


if __name__ == "__main__":
    bulk_data_obj = BulkData()
    print(bulk_data_obj.input_df)
    print(bulk_data_obj.make_list_for_browser())
