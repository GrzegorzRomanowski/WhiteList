import tkinter as tk
from tkinter import ttk

from browser import WhiteListBrowser


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("White List")
        self.iconbitmap(r"tax.ico")
        self.geometry("600x450")

        # Styles
        self.ttk_style = ttk.Style()
        self.ttk_style.configure('Blue.TFrame', background='blue')
        self.ttk_style.configure('Green.TFrame', background='green')

        # Frames
        self.frame0 = ttk.Frame(self, style='Blue.TFrame')
        self.frame0.place(relx=0, relwidth=0.5, rely=0, relheight=0.2)
        self.frame1 = ttk.Frame(self, style='Blue.TFrame')
        self.frame1.place(relx=0, relwidth=1, rely=0.2, relheight=0.5)
        self.frame2 = ttk.Frame(self, style='Green.TFrame')
        self.frame2.place(relx=0, relwidth=1, rely=0.7, relheight=0.3)

        # Photo
        def resize_image(event):
            new_width = event.width
            new_height = event.height
            resize_factor = max(max(int(512/new_width)+1, 1), max(int(512/new_height)+1, 1))
            resized_photo = photo.subsample(resize_factor, resize_factor)
            self.photo_label.configure(image=resized_photo)
            self.photo_label.image = resized_photo
        photo = tk.PhotoImage(file="tax.png")
        self.photo_label = ttk.Label(self.frame0, background="Yellow", anchor="center", image=photo)
        self.photo_label.pack(fill="both", expand=True)
        self.photo_label.bind("<Configure>", resize_image)

        # Notebooks
        self.notebook = ttk.Notebook(self.frame1)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text=" Pojedyncza weryfikacja   ")
        self.notebook.add(self.tab2, text=" Weryfikacja listy w Excelu   ")
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Radio buttons
        self.validation_method_var = tk.IntVar(value=1)
        self.method_1 = ttk.Radiobutton(self.tab1, text="Numer konta", variable=self.validation_method_var, value=1)
        self.method_1.pack(anchor='nw')
        self.method_2 = ttk.Radiobutton(self.tab1, text="NIP", variable=self.validation_method_var, value=2)
        self.method_2.pack(anchor='nw')
        self.method_3 = ttk.Radiobutton(self.tab1, text="REGON", variable=self.validation_method_var, value=3)
        self.method_3.pack(anchor='nw')

        self.changed_date_var = tk.BooleanVar(value=False)
        self.changed_date = ttk.Checkbutton(self.tab1, text="Inna data niż dzisiejsza?", variable=self.changed_date_var, command=self.entry_on_off)
        self.changed_date.pack(anchor='w')

        self.entry_date = ttk.Entry(self.tab1, state="disabled")
        self.entry_date.pack(anchor='w')

        self.check_var_3 = tk.BooleanVar(value=True)
        self.check_3 = ttk.Checkbutton(self.tab1, text="Check 3", variable=self.check_var_3)
        self.check_3.pack(anchor='sw')

        # Run button
        self.run_button = ttk.Button(self.tab1, text="RUN", command=self.get_check_buttons)
        self.run_button.pack()

        self.mainloop()

    def entry_on_off(self):
        if self.changed_date_var.get():
            self.entry_date.config(state="normal")
        else:
            self.entry_date.config(state="disabled")

    def get_check_buttons(self):
        print(self.validation_method_var.get(), self.changed_date_var.get(), self.check_var_3.get())
        return self.validation_method_var.get(), self.changed_date_var.get(), self.check_var_3.get()


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    gui_obj = Interface()
