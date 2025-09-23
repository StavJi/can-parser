from frame_parser import FrameParser
import inspect

class BaseFrameHandler:
    """ Base frame parser handler """

    short_id: int = None   # CAN frame ID
    name: str = None       # Name in GUI (ACUSTATUS, EMCUSTATUS etc.), but with channel maybe it will cause problems
    parser_method = None   # Frame parser fuction which parse the frame

    @classmethod
    def parse(cls, frame):
        """ Parse frame and return output text """

        # Determine if channel is needed or not
        sig = inspect.signature(cls.parser_method)
        if len(sig.parameters) == 2:
            frm = cls.parser_method(frame.channel, frame.payload)
        else:
            frm = cls.parser_method(frame.payload)

        values = [f"{k}={v}" for k, v in frm.items()]
        return f"Timestamp={frame.time_s}; Frame={cls.name}; Channel={frame.channel}\n {', '.join(values)}"


class TmcStatusHandler(BaseFrameHandler):
    short_id = 0xFF09
    name = "TMCSTATUS"
    parser_method = FrameParser.parse_tmc_status


class TmcStatus2Handler(BaseFrameHandler):
    short_id = 0xFF10
    name = "TMCSTATUS2"
    parser_method = FrameParser.parse_tmc_status2

class TmcStatus3Handler(BaseFrameHandler):
    short_id = 0xFF11
    name = "TMCSTATUS3"
    parser_method = FrameParser.parse_tmc_status3

class TmcStatus4Handler(BaseFrameHandler):
    short_id = 0xFF12
    name = "TMCSTATUS4"
    parser_method = FrameParser.parse_tmc_status4

class TmcStatus5Handler(BaseFrameHandler):
    short_id = 0xFF14
    name = "TMCSTATUS5"
    parser_method = FrameParser.parse_tmc_status5

class Tmc2EmcuHandler(BaseFrameHandler):
    short_id = 0xFF06
    name = "TMC2EMCU"
    parser_method = FrameParser.parse_tmc2emcu

class Tmc2AcuHandler(BaseFrameHandler):
    short_id = 0xFF05
    name = "TMC2ACU"
    parser_method = FrameParser.parse_tmc2acu

class AcuStatusHandler(BaseFrameHandler):
    short_id = 0xFF07
    name = "ACUSTATUS"
    parser_method = FrameParser.parse_acu_status

class AcuStatus2Handler(BaseFrameHandler):
    short_id = 0xFF0F
    name = "ACUSTATUS2"
    parser_method = FrameParser.parse_acu_status2

class AcuStatus3Handler(BaseFrameHandler):
    short_id = 0xFF03
    name = "ACUSTATUS3"
    parser_method = FrameParser.parse_acu_status3

class AcuErrorHandler(BaseFrameHandler):
    short_id = 0xFF0A
    name = "ACUERROR"
    parser_method = FrameParser.parse_acu_error

class AcuDiagnostics2Handler(BaseFrameHandler):
    short_id = 0xFF24
    name = "ACUDIAGNOSTICS2"
    parser_method = FrameParser.parse_acu_diagnostics2

class EmcuStatusHandler(BaseFrameHandler):
    short_id = 0xFF08
    name = "EMCUSTATUS"
    parser_method = FrameParser.parse_emcu_status


class EmcuErrorHandler(BaseFrameHandler):
    short_id = 0xFF0C
    name = "EMCUERROR"
    parser_method = FrameParser.parse_emcu_error


class EngineStatusHandler(BaseFrameHandler):
    short_id = 0xFF0D
    name = "ENGINESTATUS"
    parser_method = FrameParser.parse_acu_engine_status


class EngineStatus2Handler(BaseFrameHandler):
    short_id = 0x00FF0E
    name = "ENGINESTATUS2"
    parser_method = FrameParser.parse_acu_engine_status2

class FrameSelector:
    HANDLERS = [
        TmcStatusHandler,
        TmcStatus2Handler,
        TmcStatus3Handler,
        TmcStatus4Handler,
        TmcStatus5Handler,
        Tmc2EmcuHandler,
        Tmc2AcuHandler,
        AcuStatusHandler,
        AcuStatus2Handler,
        AcuStatus3Handler,
        AcuErrorHandler,
        AcuDiagnostics2Handler,
        EmcuStatusHandler,
        EmcuErrorHandler,
        EngineStatusHandler,
        EngineStatus2Handler,
    ]

    @classmethod
    def select(cls, frame, selected_frames):
        for handler in cls.HANDLERS:
            if frame.short_id == handler.short_id:
                key = f"{handler.name}_CH{frame.channel}"
                if key in selected_frames:
                    return handler.parse(frame)
        return None