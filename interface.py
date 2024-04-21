import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from typing import Literal

from browser import WhiteListBrowser, white_list_url
from excel import BulkData


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("White List")
        self.iconbitmap(r"tax.ico")
        self.geometry("600x750")

        # Saved values
        self.results: dict = dict()
        # Styles
        self.ttk_style = ttk.Style()
        self.ttk_style.configure('Blue.TFrame', background='blue')
        self.ttk_style.configure('Green.TFrame', background='green')

        # Main frames
        self.frame0 = ttk.Frame(self, style='Blue.TFrame')
        self.frame0.place(relx=0, relwidth=0.5, rely=0, relheight=0.2)
        self.frame1 = ttk.Frame(self, style='Blue.TFrame')
        self.frame1.place(relx=0, relwidth=1, rely=0.2, relheight=0.2)
        self.frame2 = ttk.Frame(self, style='Green.TFrame')
        self.frame2.place(relx=0, relwidth=1, rely=0.4, relheight=0.6)

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
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="  Pojedyncza weryfikacja     ")
        self.notebook.add(self.tab2, text="  Weryfikacja listy w Excelu     ")
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Tab1
        self.frame1_tab1 = ttk.Frame(self.tab1)
        self.frame1_tab1.place(relx=0, relwidth=0.3, rely=0, relheight=0.75)
        self.frame2_tab1 = ttk.Frame(self.tab1)
        self.frame2_tab1.place(relx=0.3, relwidth=0.4, rely=0, relheight=0.75)
        self.frame3_tab1 = ttk.Frame(self.tab1)
        self.frame3_tab1.place(relx=0.7, relwidth=0.3, rely=0, relheight=0.75)
        # Radio buttons
        self.validation_method_var = tk.IntVar(value=1)
        self.method_1 = ttk.Radiobutton(self.frame1_tab1, text="Numer konta", variable=self.validation_method_var, value=1)
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
        self.changed_date = ttk.Checkbutton(self.frame3_tab1, text="Inna data niż dzisiejsza?", variable=self.changed_date_var, command=self.entry_on_off)
        self.changed_date.pack()
        self.entry_date = ttk.Entry(self.frame3_tab1, state="disabled")
        self.entry_date.pack()
        self.select_date_button = ttk.Button(self.frame3_tab1, text="Wybierz datę", command=self.select_date, state="disabled")
        self.select_date_button.pack()
        # Run button
        self.run_button = ttk.Button(self.tab1, text="WYKONAJ", command=self.run_tab2)  #TODO:
        self.run_button.place(relx=0, relwidth=1, rely=0.75, relheight=0.25)

        # Tab2
        #TODO:

        # Results
        self.result_text = tk.Text(self.frame2, background="Silver", pady=10, padx=10)
        self.result_text.pack(anchor='center')

        self.mainloop()

    def entry_on_off(self):
        if self.changed_date_var.get():
            self.entry_date.config(state="normal")
            self.select_date_button.config(state="normal")
        else:
            self.entry_date.delete(0, "end")
            self.entry_date.config(state="disabled")
            self.select_date_button.config(state="disabled")

    def get_data_from_tab1(self):
        print(self.validation_method_var.get(), self.entry_number.get(), self.changed_date_var.get())
        return self.validation_method_var.get(), self.entry_number.get(), self.changed_date_var.get()

    def select_date(self):
        top = tk.Toplevel(self)
        top.iconbitmap(r"tax.ico")
        cal = Calendar(top, selectmode="day", date_pattern="dd-mm-yyyy")
        cal.pack(fill="both", expand=True)

        def set_date():
            self.entry_date.delete(0, "end")  # Wyczyść aktualną zawartość pola Entry
            self.entry_date.insert(0, cal.get_date())  # Wstaw wybraną datę do pola Entry
            top.destroy()  # Zamknij okno kalendarza po wyborze daty

        # Utwórz przycisk do zatwierdzania wybranej daty
        confirm_button = ttk.Button(top, text="Wybierz", command=set_date)
        confirm_button.pack(pady=5)

    def run_tab1(self):
        via, number, date = self.get_data_from_tab1()
        browser_obj = WhiteListBrowser(white_list_url)
        browser_obj.select_validation_method(int(via))
        browser_obj.input_number(number)
        browser_obj.submit_button()
        self.results = browser_obj.get_results()
        print(self.results)
        browser_obj.driver.quit()
        self.print_results()

    def run_tab2(self):
        browser_obj = WhiteListBrowser(white_list_url)
        browser_obj.select_validation_method(1)
        bulk_data_obj = BulkData()
        bulk_data_obj.format_bank_accounts()
        bank_accounts_list = bulk_data_obj.make_list_for_browser()
        for account in bank_accounts_list:
            browser_obj.input_number(account)
            browser_obj.submit_button()
            current_results = browser_obj.get_results()
            bulk_data_obj.write_scraped_data_to_df(results=current_results, bank_account=account)
            print(bulk_data_obj.df)

        browser_obj.driver.quit()
        print("FINAL DF\n")
        print(bulk_data_obj.df)

    def print_results(self):
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
    gui_obj = Interface()
