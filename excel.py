import pandas as pd
import openpyxl

from validations import is_bank_account_valid, format_bank_account


class BulkData:
    def __init__(self):
        self.df = pd.read_excel(r"data/input.xlsx")

    def format_bank_accounts(self):
        self.df["Numer konta"] = self.df["Numer konta"].apply(
            lambda x: format_bank_account(x) if is_bank_account_valid(x) else x)

    def make_list_for_browser(self) -> list:
        accounts_list = self.df["Numer konta"].to_list()
        accounts_list = [account for account in accounts_list if is_bank_account_valid(account)]
        self.df["Rezultat"] = self.df["Numer konta"].apply(
            lambda x: "" if is_bank_account_valid(x) else "BŁĘDNY NUMER KONTA")
        return accounts_list

    def write_scraped_data_to_df(self, results: dict, bank_account: str):
        condition = self.df["Numer konta"] == bank_account
        print(condition)
        if results.get("error") and len(results.get("error")) > 1:
            self.df.loc[condition, "Rezultat"] = results["error"]
        else:
            self.df.loc[condition, "Rezultat"] = results["info"]
            self.df.loc[condition, "NIP"] = results["nip"]


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    bulk_data_obj = BulkData()
    bulk_data_obj.format_bank_accounts()
    print(bulk_data_obj.make_list_for_browser())
    print(bulk_data_obj.df)
