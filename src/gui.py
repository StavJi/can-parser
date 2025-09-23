import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.font as tk_font
import configparser
from frame_selector import FrameSelector

def show_about():
    messagebox.showinfo("About","CAN Bus parser developed in 2025.\n"
                                             "Final project of the Python Developer course.")

class CanParserGui:
    def __init__(self):
        self.filepath = None  # File path selected by user
        self.config_path = "config/cfg.ini"

        config = configparser.ConfigParser()
        config.read(self.config_path)
        self.can_bus_channel_count = config['DEFAULT'].getint('CanBusChannels', fallback = 1)

        self.root = tk.Tk()
        self.root.geometry("700x800")
        self.root.title("CAN bus parser")

        btn_font = tk_font.Font(family="Arial", size=12, weight="bold")
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

        # Frame checkbox selector
        frame_selector = tk.LabelFrame(
            self.root,
            text="Select frames to parse",
            font=("Arial", 12, "bold")
        )
        frame_selector.pack(padx=10, pady=10, anchor="w")

        # Head of the frame
        for ch in range(1, self.can_bus_channel_count + 1):
            tk.Label(frame_selector, text=f"CH{ch}", font=("Arial", 10, "bold")).grid(row=0, column=ch, padx=5, pady=5)

        # Available frames to parse
        # Take available frames from frame_selector.py
        frames = [handler.name for handler in FrameSelector.HANDLERS]
        self.check_vars = {}

        for row, fr in enumerate(frames, start=1):
            # Create column with frame name
            tk.Label(frame_selector, text=fr).grid(row=row, column=0, sticky="w", padx=5, pady=2)

            for ch in range(1, self.can_bus_channel_count + 1):
                key = f"{fr}_CH{ch}"
                self.check_vars[key] = tk.BooleanVar(value=False)

                chk = tk.Checkbutton(frame_selector, variable=self.check_vars[key])
                chk.grid(row=row, column=ch, padx=5, pady=2)

        self.load_selection() # Load last selected frames from config

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

    def save_selection(self):
        """ Save selected CAN bus frames """
        #self.log("Saving selected CAN bus frames")

        config = configparser.ConfigParser()
        config.read(self.config_path)

        if "Frames" not in config:
            config["Frames"] = {}

        for key, var in self.check_vars.items():
            config["Frames"][key] = str(var.get())

        with open(self.config_path, "w") as f:
            config.write(f)

    def load_selection(self):
        """ Load last selected CAN bus frames from config """
        #self.log("Loading last selected CAN bus frames")

        config = configparser.ConfigParser()
        config.read(self.config_path)

        if "Frames" in config:
            for key, var in self.check_vars.items():
                if key in config["Frames"]:
                    var.set(config.getboolean("Frames", key))

    def log(self, message: str):
        """ Add log message to log """
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Scroll
        self.log_text.config(state="disabled")

    def on_closing(self):
        self.save_selection() # Save selected frames
        if messagebox.askyesno(title='Quit?', message='Do you really want to quit?'):
            self.root.destroy()

    def open_file(self):
        self.filepath = filedialog.askopenfilename( title="Choose file to analyze",
                                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filepath:
            self.log(f"Selected file: {self.filepath}")