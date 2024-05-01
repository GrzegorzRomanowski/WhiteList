import pandas as pd

from validations import is_bank_account_valid, format_bank_account


class BulkData:
    def __init__(self):
        self.df = pd.read_excel(r"data/input.xlsx")

    def format_bank_accounts(self):
        """ Apply 'format_bank_account' function on all valid accounts in "Numer konta" column.
        :return:
        """
        self.df["Numer konta"] = self.df["Numer konta"].apply(
            lambda x: format_bank_account(x) if is_bank_account_valid(x) else x)

    def make_list_for_browser(self) -> list:
        """ Make a list of valid accounts to iterate through it and fill "Rezultat" column.
        :return: list of account which can be checked on webpage
        """
        accounts_list = self.df["Numer konta"].to_list()
        accounts_list = [account for account in accounts_list if is_bank_account_valid(account)]
        self.df["Rezultat"] = self.df["Numer konta"].apply(
            lambda x: "" if is_bank_account_valid(x) else "BŁĘDNY NUMER KONTA")
        return accounts_list

    def write_scraped_data_to_df(self, results: dict, bank_account: str):
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
        with pd.ExcelWriter(r'data/output.xlsx', engine='openpyxl', mode='w') as writer:
            self.df.to_excel(writer, sheet_name="output", index=False)
            ws = writer.sheets["output"]
            for column in ws.columns:
                length = max(len(str(cell.value)) for cell in column)
                ws.column_dimensions[column[0].column_letter].width = length + 2


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    bulk_data_obj = BulkData()
    bulk_data_obj.format_bank_accounts()
    print(bulk_data_obj.make_list_for_browser())
    print(bulk_data_obj.df)
