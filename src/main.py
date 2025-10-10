import os
import threading
from gui import CanParserGui
import requests
from pathlib import Path
import pandas as pd

from can_log_parser import CanLogParser
from frame_selector import FrameSelector

def run_parser(filename: str, selected_frames, output_file: str):
    """ Main parsing logic """
    with open(output_file, "w") as f:
        grouped_rows = { }
        gen = CanLogParser.generator(filename, CanLogParser.parse_line_h407_logger)

        for frame  in gen:
            if not frame.time_s or not frame.short_id:
                continue

            ext = Path(output_file).suffix.lower()

            if ext == ".txt":
                line = FrameSelector.select_text(frame, selected_frames)
                if line:
                    f.write(line + "\n")
            elif ext == ".xlsx":

                dictionary = FrameSelector.select_dictionary(frame, selected_frames)
                if dictionary:
                    frame_type = dictionary["Frame"] # Frame name without channel
                    if frame_type not in grouped_rows:
                        grouped_rows[frame_type] = []
                    grouped_rows[frame_type].append(dictionary)

        if grouped_rows:
            with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
                for frame_type, rows in grouped_rows.items():
                    df = pd.DataFrame(rows)
                    df.to_excel(writer, sheet_name=frame_type, index=False)

if __name__ == "__main__":
    # Gui
    app = CanParserGui()

    try:
        response = requests.get('https://zenquotes.io/api/random', timeout = 5)
        response.raise_for_status()

        try:
            json_data = response.json()[0] # From some reason API returns list with just one element

            author = json_data.get('a', 'Unknown')
            quote = json_data.get('q', 'Unknown')

            app.log(f"Quote:\n{quote}\n{author}")
        except (ValueError, TypeError):
            app.log(f"Unexpected API quote response")

    except requests.exceptions.RequestException as e:
        app.log(f"No quote today. Error code {e}.")

    # Bind analyze_button to run parser
    def analyze_wrapper():
        if not app.filepath:
            app.log("Choose some file to analyze!")
            return

        # Check path if exists
        if not os.path.isfile(app.filepath):
            app.log(f"File does not exist:\n{app.filepath}")
            return

        def worker():
            try:
                app.disable_all_widgets()
                app.log("Analyzing, please wait...")
                selected_frames = [name for name, var in app.check_vars.items() if var.get()]

                ext = app.get_output_format()
                output_file_name = f"output.{ext}"
                run_parser(app.filepath, selected_frames, output_file_name)

                app.log(f"Parsing done! See {output_file_name}")
            except Exception as err:
                # Parsing error
                app.log(f"Parsing failed:\n{err}")
            finally:
                app.enable_all_widgets()

        # Run parser in new thread
        threading.Thread(target=worker, daemon=True).start()

    app.analyze_button.config(command=analyze_wrapper)

    app.root.mainloop()