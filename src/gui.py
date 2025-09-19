import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.font as tkFont


def show_about():
    messagebox.showinfo("About","CAN Bus parser developed in 2025.\n"
                                             "Final project of the Python Developer course.")

class CanParserGui:
    def __init__(self):
        self.filepath = None # File path selected by user

        self.root = tk.Tk()
        self.root.geometry("800x1200")
        self.root.title("CAN bus parser")

        btn_font = tkFont.Font(family="Arial", size=12, weight="bold")
        self.button_bg = "#55165E"  # Purple background
        self.button_fg = "white"    # White text

        # Button for file selection
        self.open_button = tk.Button(self.root, text="Open File", font=btn_font, bg=self.button_bg,
                                     fg=self.button_fg, width = 15, command=self.open_file)
        self.open_button.pack(padx = 10 , pady = 10, anchor="w")

        # Menu
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Close", command=exit)

        self.action_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.action_menu.add_command(label='About', command=show_about)

        self.menu_bar.add_cascade(menu=self.file_menu, label="File")
        self.menu_bar.add_cascade(menu=self.action_menu, label="About")

        self.root.config(menu=self.menu_bar)

        self.check_vars = {
            "TMCSTATUS_CH1": tk.BooleanVar(value=True),
            "TMCSTATUS_CH2": tk.BooleanVar(value=False),
            "TMCSTATUS2_CH1": tk.BooleanVar(value=False),
            "TMCSTATUS2_CH2": tk.BooleanVar(value=False),
            "TMCSTATUS3_CH1": tk.BooleanVar(value=False),
            "TMCSTATUS3_CH2": tk.BooleanVar(value=False),
            "TMCSTATUS4_CH1": tk.BooleanVar(value=False),
            "TMCSTATUS4_CH2": tk.BooleanVar(value=False),
            "TMCSTATUS5_CH1": tk.BooleanVar(value=False),
            "TMCSTATUS5_CH2": tk.BooleanVar(value=False),
            "TMC2ACU_CH1": tk.BooleanVar(value=False),
            "TMC2ACU_CH2": tk.BooleanVar(value=False),
            "TMC2EMCU_CH1": tk.BooleanVar(value=False),
            "TMC2EMCU_CH2": tk.BooleanVar(value=False),
            "ACUSTATUS_CH1": tk.BooleanVar(value=False),
            "ACUSTATUS_CH2": tk.BooleanVar(value=False),
            "ACUSTATUS2_CH1": tk.BooleanVar(value=False),
            "ACUSTATUS2_CH2": tk.BooleanVar(value=False),
            "ACUSTATUS3_CH1": tk.BooleanVar(value=False),
            "ACUSTATUS3_CH2": tk.BooleanVar(value=False),
            "ENGINESTATUS_CH1": tk.BooleanVar(value=False),
            "ENGINESTATUS_CH2": tk.BooleanVar(value=False),
            "ENGINESTATUS2_CH1": tk.BooleanVar(value=False),
            "ENGINESTATUS2_CH2": tk.BooleanVar(value=False),
            "ACUERROR_CH1": tk.BooleanVar(value=False),
            "ACUERROR_CH2": tk.BooleanVar(value=False),
            "EMCUSTATUS_CH1": tk.BooleanVar(value=False),
            "EMCUSTATUS_CH2": tk.BooleanVar(value=False),
            "EMCUERROR_CH1": tk.BooleanVar(value=False),
            "EMCUERROR_CH2": tk.BooleanVar(value=False),
            "ACUDIAGNOSTICS2_CH1": tk.BooleanVar(value=False),
            "ACUDIAGNOSTICS2_CH2": tk.BooleanVar(value=False),
        }

        checkbox_frame = tk.LabelFrame(self.root, text="Select frames to parse", font=btn_font)
        checkbox_frame.pack(padx=10, pady=5, anchor="w")

        for name, var in self.check_vars.items():
            tk.Checkbutton(checkbox_frame, text=name, variable=var).pack(anchor="w")

        # Button analyze
        self.analyze_button = tk.Button(self.root, text="Analyze", font=btn_font, bg=self.button_bg,
                                        fg=self.button_fg, width = 15)

        self.analyze_button.pack(padx = 10 , pady = 10, anchor="w")

        # Status box
        log_frame = tk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(log_frame, height=8, font=('Consolas', 10), state="disabled", bg="#f5f5f5")
        self.log_text.pack(fill="both", expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def log(self, message: str):
        """ Add log message to log """
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Scroll
        self.log_text.config(state="disabled")

    def on_closing(self):
        if messagebox.askyesno(title='Quit?', message='Do you really want to quit?'):
            self.root.destroy()

    def open_file(self):
        self.filepath = filedialog.askopenfilename( title="Choose file to analyze",
                                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filepath:
            self.log(f"Selected file: {self.filepath}")