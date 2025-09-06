import tkinter
from tkinter import ttk
import sv_ttk

def toggle_theme():
    if sv_ttk.get_theme() == "dark":
        print("Setting theme to light")
        sv_ttk.use_light_theme()
    elif sv_ttk.get_theme() == "light":
        print("Setting theme to dark")
        sv_ttk.use_dark_theme()
    else:
        print("Not Sun Valley theme")

def gui():
    root = tkinter.Tk()

    button = ttk.Button(root, text="Toggle theme", command=sv_ttk.toggle_theme)
    button.pack()

    root.mainloop()