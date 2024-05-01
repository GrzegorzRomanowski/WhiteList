import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from typing import Literal, Dict, Union

from browser import WhiteListBrowser
from excel import BulkData
from validations import is_valid_date
from config import config_obj


# Constants from .env
BULK_DATA_PATH = config_obj.BULK_DATA_PATH
WHITE_LIST_URL = config_obj.WHITE_LIST_URL


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("White List")
        self.iconbitmap(r"tax.ico")
        self.geometry("744x735")

        # Saved values
        self.results: Dict[str, Union[str, list]] = dict()
        # Styles
        self.ttk_style = ttk.Style()
        self.ttk_style.configure('Blue.TFrame', background='light blue')
        self.ttk_style.configure('Orange.TFrame', background='orange')

        # Main frames
        self.frame0 = ttk.Frame(self, style='Orange.TFrame')  # for photo
        self.frame0.place(relx=0, relwidth=0.33, rely=0, relheight=0.2)
        self.frame1 = ttk.Frame(self, style='Orange.TFrame')  # for tabs
        self.frame1.place(relx=0.33, relwidth=0.67, rely=0, relheight=0.2)
        self.frame2 = ttk.Frame(self, style='Blue.TFrame')  # for output
        self.frame2.place(relx=0, relwidth=1, rely=0.2, relheight=0.8)

        # Photo
        def resize_image(event):
            new_width = event.width
            new_height = event.height
            resize_factor = max(max(int(512/new_width)+1, 1), max(int(512/new_height)+1, 1))
            resized_photo = self.photo.subsample(resize_factor, resize_factor)
            self.photo_label.configure(image=resized_photo)
            self.photo_label.image = resized_photo

        self.photo = tk.PhotoImage(file="tax.png")
        self.photo_label = ttk.Label(self.frame0, background="Yellow", anchor="center", image=self.photo)
        self.photo_label.pack(fill="both", expand=True)
        self.photo_label.bind("<Configure>", resize_image)

        # Notebooks
        self.notebook = ttk.Notebook(self.frame1)
        self.tab1 = ttk.Frame(self.notebook)  # for single validation
        self.tab2 = ttk.Frame(self.notebook)  # for bulk validation
        self.notebook.add(self.tab1, text="  Pojedyncza weryfikacja     ")
        self.notebook.add(self.tab2, text="  Weryfikacja listy w Excelu     ")
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # region Tab1
        self.frame1_tab1 = ttk.Frame(self.tab1)  # for radio_buttons
        self.frame1_tab1.place(relx=0, relwidth=0.3, rely=0, relheight=0.75)
        self.frame2_tab1 = ttk.Frame(self.tab1)  # for input a number
        self.frame2_tab1.place(relx=0.3, relwidth=0.4, rely=0, relheight=0.75)
        self.frame3_tab1 = ttk.Frame(self.tab1)  # for date changing
        self.frame3_tab1.place(relx=0.7, relwidth=0.3, rely=0, relheight=0.75)
        # Radio buttons
        self.validation_method_var = tk.IntVar(value=1)
        self.method_1 = ttk.Radiobutton(self.frame1_tab1,
                                        text="Numer konta",
                                        variable=self.validation_method_var,
                                        value=1)
        self.method_1.pack(anchor='w')
        self.method_2 = ttk.Radiobutton(self.frame1_tab1, text="NIP", variable=self.validation_method_var, value=2)
        self.method_2.pack(anchor='w')
        self.method_3 = ttk.Radiobutton(self.frame1_tab1, text="REGON", variable=self.validation_method_var, value=3)
        self.method_3.pack(anchor='w')
        # Input number
        self.label_for_input = ttk.Label(self.frame2_tab1, text="Wpisz numer: ")
        self.label_for_input.pack(anchor="s", expand=True)
        self.entry_number = ttk.Entry(self.frame2_tab1)
        self.entry_number.pack(fill="x", expand=True)
        # Date
        self.changed_date_var = tk.BooleanVar(value=False)
        self.changed_date = ttk.Checkbutton(self.frame3_tab1,
                                            text="Inna data niż dzisiejsza?",
                                            variable=self.changed_date_var,
                                            command=self.entry_on_off)
        self.changed_date.pack()
        self.entry_date = ttk.Entry(self.frame3_tab1, state="disabled")
        self.entry_date.pack()
        self.select_date_button = ttk.Button(self.frame3_tab1,
                                             text="Wybierz datę",
                                             command=self.select_date,
                                             state="disabled")
        self.select_date_button.pack()
        # Run button 1
        self.run_button1 = ttk.Button(self.tab1, text="WYKONAJ", command=self.run_tab1)
        self.run_button1.place(relx=0, relwidth=1, rely=0.75, relheight=0.25)
        # endregion

        # region Tab2
        self.frame1_tab2 = ttk.Frame(self.tab2)  # for Excel buttons
        self.frame1_tab2.place(relx=0, relwidth=1, rely=0, relheight=0.5)
        self.frame2_tab2 = ttk.Frame(self.tab2)  # for progress bar
        self.frame2_tab2.place(relx=0, relwidth=1, rely=0.5, relheight=0.25)
        # Tab2 buttons
        self.button1_tab2 = ttk.Button(self.frame1_tab2,
                                       text="Edytuj dane wsadowe",
                                       command=lambda: Interface.open_excel_file(rf'{BULK_DATA_PATH}/input.xlsx'))
        self.button1_tab2.place(relx=0, relwidth=0.5, rely=0, relheight=1)
        self.button2_tab2 = ttk.Button(self.frame1_tab2,
                                       text="Otwórz dane wyjściowe",
                                       command=lambda: Interface.open_excel_file(rf'{BULK_DATA_PATH}/output.xlsx'))
        self.button2_tab2.place(relx=0.5, relwidth=0.5, rely=0, relheight=1)
        # Progress bar
        self.progress_bar = ttk.Progressbar(self.frame2_tab2, orient="horizontal", mode="determinate")
        self.progress_bar.pack(pady=2, padx=2, fill="x")
        # Run button 2
        self.run_button2 = ttk.Button(self.tab2, text="WYKONAJ", command=self.run_tab2)
        self.run_button2.place(relx=0, relwidth=1, rely=0.75, relheight=0.25)
        # endregion

        # Results
        self.result_text = tk.Text(self.frame2, background="Silver", pady=10, padx=10, height=35, width=89)
        self.result_text.pack(anchor='center')

        self.mainloop()

    def entry_on_off(self):
        """ Turn on/off an entry for data.
        :return:
        """
        if self.changed_date_var.get():
            self.entry_date.config(state="normal")
            self.select_date_button.config(state="normal")
        else:
            self.entry_date.delete(0, "end")
            self.entry_date.config(state="disabled")
            self.select_date_button.config(state="disabled")

    def get_data_from_tab1(self) -> (Literal[1, 2, 3], str, str):
        """ Get data from User from tab 1.
        :return: (validation method, number to validation, date)
        """
        different_date_bool = self.changed_date_var.get()
        different_date_str = self.entry_date.get() if different_date_bool else ""
        return self.validation_method_var.get(), self.entry_number.get(), different_date_str

    def select_date(self):
        """ Opens calendar window from tkinter.
        :return:
        """
        top = tk.Toplevel(self)
        top.iconbitmap(r"tax.ico")
        cal = Calendar(top, selectmode="day", date_pattern="dd-mm-yyyy")
        cal.pack(fill="both", expand=True)

        def set_date():
            """ Put a date from calendar to entry for date and destroy calendar window.
            :return:
            """
            self.entry_date.delete(0, "end")  # delete content of entry
            self.entry_date.insert(0, cal.get_date())  # insert new value
            top.destroy()  # close calendar

        # Confirm button
        confirm_button = ttk.Button(top, text="Wybierz", command=set_date)
        confirm_button.pack(pady=5)

    def run_tab1(self):
        """ Runs a browser for single validation.
        :return:
        """
        via, number, date = self.get_data_from_tab1()
        browser_obj = WhiteListBrowser(WHITE_LIST_URL)
        browser_obj.select_validation_method(int(via))
        browser_obj.input_number(number)
        date = is_valid_date(date)
        if date:
            browser_obj.type_date(date_str=date)
        browser_obj.submit_button()
        self.results = browser_obj.get_results()
        self.print_results()

    def run_tab2(self):
        """ Runs a browser for bulk validation.
        :return:
        """
        self.progress_bar["value"] = 0  # reset progress bar

        browser_obj = WhiteListBrowser(WHITE_LIST_URL)
        browser_obj.select_validation_method(1)
        bulk_data_obj = BulkData()
        bulk_data_obj.format_bank_accounts()
        bank_accounts_list = bulk_data_obj.make_list_for_browser()
        for i, account in enumerate(bank_accounts_list, start=1):
            browser_obj.input_number(account)
            browser_obj.submit_button()
            current_results = browser_obj.get_results()
            bulk_data_obj.write_scraped_data_to_df(results=current_results, bank_account=account)

            progress = (i / len(bank_accounts_list)) * 100
            self.progress_bar["value"] = progress
            self.update_idletasks()

        bulk_data_obj.save_output_to_file()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, bulk_data_obj.df.to_string(index=False,
                                                                   na_rep="----------",
                                                                   justify="center"))

    @staticmethod
    def open_excel_file(path: str):
        """ Opens a file in an active Excel application.
        :param path: Path to input or output file.
        :return:
        """
        full_path = os.path.abspath(path)
        os.system(f'start "EXCEL.EXE" "{full_path}"')

    def print_results(self):
        """ Unpack data from dictionary and print them into output field in User interface.
        :return:
        """
        if len(self.results["error"]) > 1:
            unpack_data = self.results["error"]
        else:
            bank_accounts = "\n".join(self.results['bank'])
            unpack_data = f"NIP: {self.results['nip']}\nREGON: {self.results['regon']}" \
                          f"\n\nKonta bankowe:\n{bank_accounts}"
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, unpack_data)


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes

    # Make a dir for bulk data
    if not os.path.exists(BULK_DATA_PATH):
        os.makedirs(BULK_DATA_PATH)
    if not os.path.exists(rf"{BULK_DATA_PATH}/input.xlsx"):
        BulkData.init_input_file(rf"{BULK_DATA_PATH}/input.xlsx")

    # Run interface
    gui_obj = Interface()
