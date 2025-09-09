import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.font as tkFont

class CanParserGui:
    def __init__(self):
        self.filepath = None # File path selected by user

        self.root = tk.Tk()
        self.root.geometry("300x110")
        self.root.title("CAN bus parser")

        btn_font = tkFont.Font(family="Arial", size=12, weight="bold")
        self.button_bg = "#55165E"  # Purple background
        self.button_fg = "white"    # White text

        # Button for file selection
        self.open_button = tk.Button(self.root, text="Open File", font=btn_font, bg=self.button_bg,
                                     fg=self.button_fg, width = 15, command=self.open_file)

        self.open_button.pack(padx = 10 , pady = 10)


        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Close", command=exit)

        self.action_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.action_menu.add_command(label='About', command=self.show_about)

        self.menu_bar.add_cascade(menu=self.file_menu, label="File")
        self.menu_bar.add_cascade(menu=self.action_menu, label="About")

        self.root.config(menu=self.menu_bar)

        # Button analyze
        self.analyze_button = tk.Button(self.root, text="Analyze", font=btn_font, bg=self.button_bg,
                                        fg=self.button_fg, width = 15, command=self.analyze_file)

        self.analyze_button.pack(padx = 10 , pady = 10)

        # self.textbox = tk.Text(self.root, font = ('Arial', 16))
        # self.textbox.bind("<KeyPress>", self.shortcut)
        # self.textbox.pack(padx = 10 , pady = 10)
        #
        # self.check_state = tk.IntVar()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    # def shortcut(self, event):
    #     if event.state == 12 and event.keysym == "Return":
    #         self.show_message()

    # def clear(self):
    #     self.textbox.delete('1.0', tk.END)

    def show_about(self):
        messagebox.showinfo("About","CAN Bus parser developed in 2025.\n"
                                                 "Final project of the Python Developer course.")

    def on_closing(self):
        if messagebox.askyesno(title='Quit?', message='Do you really want to quit?'):
            self.root.destroy()

    def open_file(self):
        self.filepath = filedialog.askopenfilename( title="Choose file to analyze",
                                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filepath:
            messagebox.showinfo("File Selected", f"File: {self.filepath}")

    def analyze_file(self):
        ...
        # if not self.filepath:
        #     messagebox.showwarning("Chyba", "Nejdřív vyber soubor.")
        #     return
        #
        # selection = self.listbox.curselection()
        # if not selection:
        #     messagebox.showwarning("Chyba", "Vyber jednu možnost z nabídky.")
        #     return
        #
        # option = self.options[selection[0]]
        #
        # try:
        #     with open(self.filepath, "r", encoding="utf-8") as f:
        #         content = f.read()
        # except Exception as e:
        #     messagebox.showerror("Chyba", f"Nepodařilo se načíst soubor:\n{e}")
        #     return
        #
        # if option == "Počet řádků":
        #     result = f"Soubor má {content.count(chr(10)) + 1} řádků."
        # elif option == "Počet slov":
        #     result = f"Soubor má {len(content.split())} slov."
        # elif option == "Počet znaků":
        #     result = f"Soubor má {len(content)} znaků."
        # else:
        #     result = "Neznámá možnost."
        #
        # self.result_label.config(text=result)


# def toggle_theme():
#     if sv_ttk.get_theme() == "dark":
#         print("Setting theme to light")
#         sv_ttk.use_light_theme()
#     elif sv_ttk.get_theme() == "light":
#         print("Setting theme to dark")
#         sv_ttk.use_dark_theme()
#     else:
#         print("Not Sun Valley theme")

# def gui():
#     root = tkinter.Tk()
#     root.geometry("1000x800")
#     root.title("CAN bus parser")
#
#     label = ttk.Label(root, text="Hello World!", font=('Arial', 18))
#     label.pack(padx = 20, pady = 20)
#
#     my_entry = ttk.Entry(root, font=('Arial', 16))
#     my_entry.pack(padx = 10, pady = 10)
#
#     button = ttk.Button(root, text='Clik me')
#     button.pack(padx=10, pady=10)
#
#     sv_ttk.use_dark_theme()
#
#     # button = ttk.Button(root, text="Toggle theme", command=sv_ttk.toggle_theme)
#     # button.pack()
#
#     root.mainloop()