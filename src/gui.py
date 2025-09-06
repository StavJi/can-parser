import tkinter as tk
from tkinter import messagebox
import sv_ttk

class MyGui:
    def __init__(self):
        self.root = tk.Tk()

        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Close", command=self.on_closing)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close without question", command=exit)

        self.action_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.action_menu.add_command(label='Show Message', command=self.show_message)

        self.menu_bar.add_cascade(menu=self.file_menu, label="File")
        self.menu_bar.add_cascade(menu=self.action_menu, label="Action")

        self.root.config(menu=self.menu_bar)

        self.label = tk.Label(self.root, text = 'Hello World', font = ('Arial', 18))
        self.label.pack(padx = 10 , pady = 10)

        self.textbox = tk.Text(self.root, font = ('Arial', 16))
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx = 10 , pady = 10)

        self.check_state = tk.IntVar()

        self.check = tk.Checkbutton(self.root, text = "Show message", font = ('Arial', 16), variable = self.check_state)
        self.check.pack(padx = 10 , pady = 10)

        self.button = tk.Button(self.root, text = 'Msg', font = ('Arial', 18), command = self.show_message)
        self.button.pack(padx = 10 , pady = 10)

        self.clear_btn = tk.Button(self.root, text='Clear', font=('Arial', 18), command = self.clear)
        self.clear_btn.pack(padx = 10 , pady = 10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get('1.0', tk.END))
        else:
            messagebox.showinfo(title="Message", message=self.textbox.get('1.0', tk.END))

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.show_message()

    def on_closing(self):
        if messagebox.askyesno(title='Quit?', message='Do you really want to quit?'):
            self.root.destroy()

    def clear(self):
        self.textbox.delete('1.0', tk.END)

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