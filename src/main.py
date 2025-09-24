import os
from gui import CanParserGui
import requests

from can_log_parser import CanLogParser
from frame_selector import FrameSelector

def run_parser(filename: str, selected_frames, output_file: str = "output.txt"):
    """ Main parsing logic """
    with open(output_file, "w") as f:
        gen = CanLogParser.generator(filename, CanLogParser.parse_line_h407_logger)

        for frame  in gen:
            if not frame.time_s or not frame.short_id:
                continue

            line = FrameSelector.select(frame, selected_frames)
            if line:
                f.write(line + "\n")

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
            run_parser(app.filepath, selected_frames)
            app.log("Parsing done! See output.txt")
        except Exception as e:
            # Parsing error
            app.log(f"Parsing failed:\n{e}")

    app.analyze_button.config(command=analyze_wrapper)

    app.root.mainloop()