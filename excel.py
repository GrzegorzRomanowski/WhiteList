import os
import pandas as pd
from typing import List, Dict, Union

from validations import is_valid_bank_account, format_bank_account
from config import config_obj


# Constants from .env
BULK_DATA_PATH = config_obj.BULK_DATA_PATH


class BulkData:
    def __init__(self):
        self.df = pd.read_excel(rf"{BULK_DATA_PATH}/input.xlsx")

    def format_bank_accounts(self):
        """ Apply 'format_bank_account' function on all valid accounts in "Numer konta" column.
        :return:
        """
        self.df["Numer konta"] = self.df["Numer konta"].apply(
            lambda x: format_bank_account(x) if is_valid_bank_account(x) else x)

    def make_list_for_browser(self) -> List[str]:
        """ Make a list of valid accounts to iterate through it and fill "Rezultat" column.
        :return: list of account which can be checked on webpage
        """
        accounts_list = self.df["Numer konta"].to_list()
        accounts_list = [account for account in accounts_list if is_valid_bank_account(account)]
        self.df["Rezultat"] = self.df["Numer konta"].apply(
            lambda x: "" if is_valid_bank_account(x) else "BŁĘDNY NUMER KONTA")
        return accounts_list

    def write_scraped_data_to_df(self, results: Dict[str, Union[str, list]], bank_account: str):
        """ Write scraped data to DataFrame for specified bank account (for one row).
        :param results: dict with scrapped data by browser
        :param bank_account: specified bank account
        :return:
        """
        condition = self.df["Numer konta"] == bank_account
        if results.get("error") and len(results.get("error")) > 1:
            self.df.loc[condition, "Rezultat"] = results["error"]
        else:
            self.df.loc[condition, "Rezultat"] = results["info"]
            self.df.loc[condition, "NIP"] = results["nip"]

    def save_output_to_file(self):
        """ Saves data in an Excel file and adjust the column width to contained data.
        :return:
        """
        with pd.ExcelWriter(rf'{BULK_DATA_PATH}/output.xlsx', engine='openpyxl', mode='w') as writer:
            self.df.to_excel(writer, sheet_name="output", index=False)
            ws = writer.sheets["output"]
            for column in ws.columns:
                length = max(len(str(cell.value)) for cell in column)
                ws.column_dimensions[column[0].column_letter].width = length + 2

    @staticmethod
    def init_input_file(full_path: str):
        """ Init an input Excel file with only first header filled.
        :param full_path: full path to file as string
        :return:
        """
        header = {'A': ['Numer konta']}
        df = pd.DataFrame(header)
        df.to_excel(full_path, index=False, header=False, startrow=0, startcol=0, sheet_name="input")


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    bulk_data_obj = BulkData()
    bulk_data_obj.format_bank_accounts()
    print("List of bank accounts to be checked\n", bulk_data_obj.make_list_for_browser())
    print("\nDataFrame:\n", bulk_data_obj.df)
