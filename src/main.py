import os
from gui import CanParserGui

from can_log_parser import CanLogParser
from frame_parser import FrameParser

f = open("output.txt", "w")

def run_parser(filename: str, selected_frames, output_file: str = "output.txt"):
    """ Main parsing logic """
    with open(output_file, "w") as f:
        gen = CanLogParser.generator(filename, CanLogParser.parse_line_h407_logger)

        for frame  in gen:
            if frame.time_s is not None and frame.short_id is not None:

                if frame.short_id == 0x00FF07 and frame.channel == '1' and "ACUSTATUS_CH1" in selected_frames: # ACUSTATUS channel 1
                   frm = FrameParser.parse_acu_status(frame.channel, frame.payload)
                   f.write(f"Engine1 state: {frm['diesel_state_1_s']}")
                   f.write(';')
                   f.write(frame.time_s)
                   f.write(f"Colling: {frm['cooling_active_1']}")
                   f.write('\n')


                if frame.short_id == 0x00FF07 and frame.channel == '2' and "ACUSTATUS_CH2" in selected_frames: # ACUSTATUS channel 1
                   frm = FrameParser.parse_acu_status(frame.channel, frame.payload)
                   f.write(f"Engine2 state: {frm['diesel_state_2_s']}")
                   f.write(';')
                   f.write(frame.time_s)
                   f.write(f"Colling: {frm['cooling_active_2']}")
                   f.write('\n')

                if frame.short_id == 0x00FF0C and frame.channel == '1' and "EMCUSTATUS_CH1" in selected_frames: # EMCUERROR channel 1
                    frm = FrameParser.parse_emcu_error(frame.channel, frame.payload)
                    f.write(f"Chrg 1: {frm['Elmot_Charge_Error_1']}")
                    f.write('\n')
                    f.write(f"Err 1: {frm['Elmot_Error_1']}")
                    f.write('\n')

                if frame.short_id == 0x00FF0C and frame.channel == '2' and "EMCUSTATUS_CH2" in selected_frames: # EMCUERROR channel 2
                    frm = FrameParser.parse_emcu_error(frame.channel, frame.payload)
                    f.write(f"Chrg 2: {frm['Elmot_Charge_Error_2']}")
                    f.write('\n')
                    f.write(f"Err 2: {frm['Elmot_Error_2']}")
                    f.write('\n')

                if frame.short_id == 0x00FF06 and frame.channel == '1' and "TMC2EMCU_CH1" in selected_frames: # TMC2EMCU channel 1
                    frm = FrameParser.parse_tmc2emcu(frame.channel, frame.payload)
                    f.write(f"CH1 running {frm['elmot_running_1']}")
                    f.write('\n')
                    f.write(f"CH1 charging {frm['elmot_charging_running_1']}")
                    f.write('\n')

                if frame.short_id == 0x00FF06 and frame.channel == '2' and "TMC2EMCU_CH2" in selected_frames: # TMC2EMCU channel 2
                    frm = FrameParser.parse_tmc2emcu(frame.channel, frame.payload)
                    f.write(f"CH2 running {frm['elmot_running_2']}")
                    f.write('\n')
                    f.write(f"CH2 charging {frm['elmot_charging_running_2']}")
                    f.write('\n')

                if frame.short_id == 0x00FF08 and frame.channel == '1' and "EMCUSTATUS_CH1" in selected_frames: # channel 1
                    frm = FrameParser.parse_emcu_status(frame.channel, frame.payload)
                    f.write(f"CH1 status {frm['EMCU_State_1']}")
                    f.write('\n')

                if frame.short_id == 0x00FF08 and frame.channel == '2' and "EMCUSTATUS_CH2" in selected_frames: # channel 1
                    frm = FrameParser.parse_emcu_status(frame.channel, frame.payload)
                    f.write(f"CH2 status {frm['EMCU_State_2']}")
                    f.write('\n')

if __name__ == "__main__":
    # Gui
    app = CanParserGui()

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