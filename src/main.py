from gui import CanParserGui

from can_log_parser import CanLogParser
from frame_parser import FrameParser

f = open("output.txt", "w")

def run_parser(filename: str, output_file: str = "output.txt"):
    """ Main parsing logic """
    with open(output_file, "w") as f:
        gen = CanLogParser.generator(filename, CanLogParser.parse_line_h407_logger)

        for frame  in gen:
            if frame.time_s is not None and frame.short_id is not None:

                if frame.short_id == 0x00FF07 and frame.channel == '1': # ACUSTATUS channel 1
                   frm = FrameParser.parse_acu_status(frame.channel, frame.payload)
                   f.write(f"Engine1 state: {frm['diesel_state_1_s']}")
                   f.write(';')
                   f.write(frame.time_s)
                   f.write(f"Colling: {frm['cooling_active_1']}")
                   f.write('\n')


                if frame.short_id == 0x00FF07 and frame.channel == '2': # ACUSTATUS channel 1
                   frm = FrameParser.parse_acu_status(frame.channel, frame.payload)
                   f.write(f"Engine2 state: {frm['diesel_state_2_s']}")
                   f.write(';')
                   f.write(frame.time_s)
                   f.write(f"Colling: {frm['cooling_active_2']}")
                   f.write('\n')

                if frame.short_id == 0x00FF0C and frame.channel == '1': # EMCUERROR channel 1
                    frm = FrameParser.parse_emcu_error(frame.channel, frame.payload)
                    f.write(f"Chrg 1: {frm['Elmot_Charge_Error_1']}")
                    f.write('\n')
                    f.write(f"Err 1: {frm['Elmot_Error_1']}")
                    f.write('\n')

                if frame.short_id == 0x00FF0C and frame.channel == '2': # EMCUERROR channel 2
                    frm = FrameParser.parse_emcu_error(frame.channel, frame.payload)
                    f.write(f"Chrg 2: {frm['Elmot_Charge_Error_2']}")
                    f.write('\n')
                    f.write(f"Err 2: {frm['Elmot_Error_2']}")
                    f.write('\n')

                if frame.short_id == 0x00FF06 and frame.channel == '1': # channel 1
                    frm = FrameParser.parse_tmc2emcu(frame.channel, frame.payload)
                    f.write(f"CH1 running {frm['elmot_running_1']}")
                    f.write('\n')
                    f.write(f"CH1 charging {frm['elmot_charging_running_1']}")
                    f.write('\n')

                if frame.short_id == 0x00FF06 and frame.channel == '2': # channel 2
                    frm = FrameParser.parse_tmc2emcu(frame.channel, frame.payload)
                    f.write(f"CH2 running {frm['elmot_running_2']}")
                    f.write('\n')
                    f.write(f"CH2 charging {frm['elmot_charging_running_2']}")
                    f.write('\n')

                if frame.short_id == 0x00FF08 and frame.channel == '1': # channel 1
                    frm = FrameParser.parse_emcu_status(frame.channel, frame.payload)
                    f.write(f"CH1 status {frm['EMCU_State_1']}")
                    f.write('\n')

                if frame.short_id == 0x00FF08 and frame.channel == '2': # channel 1
                    frm = FrameParser.parse_emcu_status(frame.channel, frame.payload)
                    f.write(f"CH2 status {frm['EMCU_State_2']}")
                    f.write('\n')

if __name__ == "__main__":
    # Gui
    app = CanParserGui()

    # Bind analyze_button to run parser
    def analyze_wrapper():
        if not app.filepath:
            from tkinter import messagebox
            messagebox.showwarning("Warning", "Choose file!")
            return
        run_parser(app.filepath)
        from tkinter import messagebox
        messagebox.showinfo("Done", f"See output.txt")

    app.analyze_button.config(command=analyze_wrapper)

    app.root.mainloop()