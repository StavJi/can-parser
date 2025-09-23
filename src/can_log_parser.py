import os
from datetime import datetime

class CanFrame:
    """ One CAN frame """

    def __init__(self, time_s, frame_id, short_id, channel, payload, raw_line = None):
        self.time_s = time_s
        self.frame_id = frame_id
        self.short_id = short_id
        self.channel = channel
        self.payload = payload
        self.raw_line = raw_line

    def __repr__(self):
        return f"<CanFrame {self.time_s} id=0x{self.frame_id:X} short=0x{self.short_id:X} channel={self.channel} payload={self.payload}>"

class CanLogParser:
    """ Log parser supporting more formats """

    @staticmethod
    def extract_escaped(payload: str) -> str:
        out = ""
        esc_detected = False
        for i in range(int(len(payload) / 2)):
            if esc_detected:
                out += payload[i * 2:i * 2 + 2]
                esc_detected = False
            elif payload[i * 2:i * 2 + 2] == 'FE':
                esc_detected = True
            else:
                out += payload[i * 2:i * 2 + 2]
        return out

    @classmethod
    def parse_line_h407_logger(cls, line: str) -> CanFrame | None:
        line = line.split()
        if len(line) == 0 or line[0] in ('//', '#'):
            return None

        if line[0].upper() == 'RAS:':
            payload_len = int(line[1])
            s_payload = line[2]
            payload = [int(s_payload[i * 2:i * 2 + 2], 16) for i in range(payload_len)]
            return CanFrame(None, None, None, None, payload)

        if line[0].upper() == 'HMI:':
            channel = line[1]
            s_payload = cls.extract_escaped(line[3])
            payload_len = int(len(s_payload) / 2)
            payload = [int(s_payload[i * 2:i * 2 + 2], 16) for i in range(payload_len)]
            return CanFrame(None, None, None, channel, payload)

        time_s = line[0]
        frame_id = int(line[1], 16)
        short_id = (frame_id >> 8) & 0xFFFF
        size = int(line[2]) or 8

        u64_payload = int(line[3][0:2 * size], 16)
        payload = [(u64_payload >> (8 * i)) & 0xFF for i in reversed(range(size))]

        try:
            channel = line[4].split('=')[1]
        except ValueError:
            channel = '?'

        return CanFrame(time_s, frame_id, short_id, channel, payload)

    @classmethod
    def parse_line_h407_logger_only_can(cls, line: str) -> CanFrame | None:
        line = line.split()
        if len(line) == 0 or line[0] in ('//', '#'):
            return None
        if line[0].upper() in ('RAS:', 'HMI:'):
            return None
        if len(line[0]) > 200:
            return None

        time_s = line[0]
        frame_id = int(line[1], 16)
        short_id = (frame_id >> 8) & 0xFFFF
        size = int(line[2]) or 8

        u64_payload = int(line[3][0:2 * size], 16)
        payload = [(u64_payload >> (8 * i)) & 0xFF for i in reversed(range(size))]

        try:
            channel = line[4].split('=')[1]
        except ValueError:
            channel = '?'

        return CanFrame(time_s, frame_id, short_id, channel, payload)

    @staticmethod
    def generator(src_filename, line_parser, with_debug_info=False):
        with open(src_filename, 'r') as f:
            for line in f:
                if line.strip() in ('', 'begin triggerblock', 'end triggerblock'):
                    continue
                if line.startswith(('#', '==', 'date', 'base hex', '#timestamp')):
                    continue

                frame = line_parser(line)
                if frame is None:
                    continue

                if with_debug_info:
                    yield frame, line
                else:
                    yield frame

    ####################################
    ##  Correct time of can messages
    ####################################

    @staticmethod
    def timestamp_begin_of_file(filename: str) -> datetime:
        # searching the head of the log for #timestamp:
        with open(filename, 'r') as f:
            for i in range(10):
                line = f.readline()
                if line.startswith('#timestamp'):
                    return datetime.fromtimestamp(float(line[11:]) / 1000.0)

            # find last position in file
            position = f.seek(0, 2)
            # seek 200 from bottom
            f.seek(max(0, position - 200), 0)

            time_stamp = 0
            line = f.readline()
            while line != '':
                try:
                    time_stamp = int(line[0:12])
                except ValueError:
                    pass
                line = f.readline()

        mod_time = os.stat(filename).st_mtime
        return datetime.fromtimestamp(mod_time - time_stamp / 1000)

    @classmethod
    def get_timestamp_of_dt(cls, filename: str, dt: datetime) -> float:
        start_dt_timestamp = cls.timestamp_begin_of_file(filename).timestamp()
        return dt.timestamp() - start_dt_timestamp

    @staticmethod
    def get_lines_of_file(filename: str) -> int:
        with open(filename, 'r') as f:
            lines_cnt = 0
            line = f.readline()

            while line != '':
                lines_cnt += 1
                line = f.readline()

        return lines_cnt

    ##########################################
    ## get day/month/year from first TMCSTATUS
    ##########################################

    @classmethod
    def get_date_time_from_tmc_status(cls, filename: str) -> datetime | None:
        for frame in cls.generator(filename, cls.parse_line_h407_logger):
            if frame.short_id == 0x00FF09:  # TMCSTATUS
                # 3           Minutes
                # 4           Day
                # 5           Month
                # 6-7         Year

                return datetime(frame.payload[6] * 256 + frame.payload[5],
                                frame.payload[4], frame.payload[3],
                                frame.payload[1], frame.payload[2])
        return None