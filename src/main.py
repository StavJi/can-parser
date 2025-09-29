import os
from gui import CanParserGui
import requests
from pathlib import Path
import pandas as pd

from can_log_parser import CanLogParser
from frame_selector import FrameSelector

def run_parser(filename: str, selected_frames, output_file: str):
    """ Main parsing logic """
    with open(output_file, "w") as f:
        rows = []
        gen = CanLogParser.generator(filename, CanLogParser.parse_line_h407_logger)

        for frame  in gen:
            if not frame.time_s or not frame.short_id:
                continue

            ext = Path(output_file).suffix.lower()

            if ext == ".txt":
                line = FrameSelector.select(frame, selected_frames, True)
                if line:
                    f.write(line + "\n")
            elif ext == ".xlsx":

                dictionary = FrameSelector.select(frame, selected_frames, False)
                if dictionary:
                    rows.append(dictionary)

        if rows:
            df = pd.DataFrame(rows)
            df.to_excel(output_file, index=False)

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

        try:
            app.log("Analyzing, please wait...")
            selected_frames = [name for name, var in app.check_vars.items() if var.get()]

            ext = app.get_output_format()
            output_file_name = f"output.{ext}"
            run_parser(app.filepath, selected_frames, output_file_name)

            app.log(f"Parsing done! See {output_file_name}")
        except Exception as err:
            # Parsing error
            app.log(f"Parsing failed:\n{err}")

    app.analyze_button.config(command=analyze_wrapper)

    app.root.mainloop()