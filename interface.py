import tkinter as tk
from tkinter import ttk


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("White List")
        # self.iconbitmap(r"logo.ico")
        self.geometry("300x200")

        # Styles
        self.ttk_style = ttk.Style()
        self.ttk_style.configure('Blue.TFrame', background='blue')
        self.ttk_style.configure('Green.TFrame', background='green')

        # Frames
        self.welcome_message = ttk.Label(self, text="Hello", background="Yellow", anchor="center")
        self.welcome_message.place(relx=0, relwidth=1, rely=0, relheight=0.2)
        self.frame1 = ttk.Frame(self, style='Blue.TFrame')
        self.frame1.place(relx=0, relwidth=1, rely=0.2, relheight=0.5)
        self.frame2 = ttk.Frame(self, style='Green.TFrame')
        self.frame2.place(relx=0, relwidth=1, rely=0.7, relheight=0.3)

        # Check buttons
        self.check_var_1 = tk.BooleanVar(value=True)
        self.check_1 = ttk.Checkbutton(self.frame1, text="Check 1", variable=self.check_var_1)
        self.check_1.pack(anchor='w')

        self.check_var_2 = tk.BooleanVar(value=False)
        self.check_2 = ttk.Checkbutton(self.frame1, text="Check 2", variable=self.check_var_2)
        self.check_2.pack(anchor='w')

        self.check_var_3 = tk.BooleanVar(value=True)
        self.check_3 = ttk.Checkbutton(self.frame1, text="Check 3", variable=self.check_var_3)
        self.check_3.pack(anchor='w')

        # Run button
        self.run_button = ttk.Button(self.frame2, text="RUN", command=self.get_check_buttons)
        self.run_button.pack()

        self.mainloop()

    def get_check_buttons(self):
        print(self.check_var_1.get(), self.check_var_2.get(), self.check_var_3.get())
        return self.check_var_1.get(), self.check_var_2.get(), self.check_var_3.get()


if __name__ == "__main__":
    # Shouldn't be launched directly - only for debugging purposes
    gui_obj = Interface()
    v1, v2, v3 = gui_obj.get_check_buttons()
    print(v1, v2, v3)
