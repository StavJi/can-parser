import os
from datetime import datetime

# short_tmc_commands_ids = {
#     0x00FF05: 'TMC2ACU',
#     0x00FF06: 'TMC2EMCU',
#     0x00FF07: 'ACUSTATUS',
#     0x00FF08: 'EMCUSTATUS',
#     0x00FF09: 'TMCSTATUS',
#     0x00FF0A: 'ACUERROR',
#     0x00FF0C: 'EMCUERROR',
#     0x00FF0D: 'ACUENGINESTATUS',
#     0x00FF0E: 'ACUENGINESTATUS2',
#     0x00FF0F: 'ACUSTATUS2',
#     0x00FF10: 'TMCSTATU2',
#     0x00FF14: 'TMCSTATU5'
# }
#
#
# acu_frames = [
#               0x00FF07, # ACUSTATUS
#               0x00FF0F, # ACUSTATUS2
#               0x00FF03, # ACUSTATUS3
#               0x00FF0D, # ACUENGINESTATUS
#               0x00FF0E, # ACUENGINESTATUS2
#               0x00FF21, # ACUENGINESTATUS3
#               0x00FF0A, # ACUERROR
#               0x00EBFF, # ACUERROR
#               0x00FF17, # ACUVERSION
#               0x00FF15  # ACUTICK
#              ]
#
# tmc_frames = [
#               0x00FF09, # TMCSTATUS
#               0x00FF10, # TMCSTATUS2
#               0x00FF11, # TMCSTATUS3
#               0x00FF12, # TMCSTATUS4
#               0x00FF14, # TMCSTATUS5
#               0x00FF05, # TMC2ACU
#               0x00FF06, # TMC2EMCU
#               0x00FF46  # SYSIDENT
#               ]
#
# emcu_frames = [
#               0x00FF08, # EMCUSTATUS
#               0x00FF0C, # EMCUERROR
#               0x00FF18  # EMCUVERSION
#               ]

# def is_tmc_frame(short_id):
#     return short_id in tmc_frames
#
# def is_acu_frame(short_id):
#     return short_id in acu_frames
#
# def is_emcu_frame(short_id):
#     return short_id in emcu_frames

def extract_escaped(payload):
    out=""
    esc_detected = False
    for i in range(int(len(payload) / 2)):
        if esc_detected:
            out += payload[i*2:i*2+2]
            esc_detected=False
            
        elif payload[i*2:i*2+2] == 'FE':
            esc_detected = True
        else:
            out += payload[i*2:i*2+2]
    return out


def parse_line_h407_logger(line):
    line=line.split()
    if len(line) == 0:
        #skip empty line
        return None, None, None, None, None
    
    if line[0]=='//' or line[0]=='#':
        #skip comment
        return None, None, None, None, None
    
    if line[0].upper() == 'RAS:':
        payload_len=int(line[1])
        s_payload = line[2] 

        payload=[]
        try:
            for i in range(payload_len):
                payload.append(int(s_payload[i*2:i*2+2],16))
            
        except ValueError as ex:
            raise ValueError(f"PAYLOAD (len={payload_len}):{s_payload}") from ex

        return None, None, None, None, payload
    
    if line[0].upper() == 'HMI:':
        channel = line[1]
        s_payload = extract_escaped(line[3])
        payload_len = int(len(s_payload)/2)

        payload = []
        try:
            for i in range(payload_len):
                payload.append(int(s_payload[i*2:i*2+2],16))
            
        except ValueError as ex:
            raise ValueError(f"PAYLOAD (len={payload_len}):{s_payload}") from ex

        return None, None, None, channel, payload
    
    time_s = line[0]
    
    try:
        frame_id = int(line[1], 16)
    except:
        print("EXCEPTION at time %s" % time_s)
        print(line)
        raise
        
    short_id = (frame_id >> 8) & 0xFFFF
    
    size = int(line[2])
    
    payload = []

    if size == 0:
        size = 8
        
    u64_payload = int(line[3][0:2*size], 16)
        
    for i in range(size):
        payload.insert(0, u64_payload & 0xFF)
        u64_payload = u64_payload >> 8

    try:
        channel = line[4].split('=')[1]
    except ValueError:
        channel='?'


    return time_s, frame_id, short_id, channel, payload

def parse_line_h407_logger_only_can(line):
    line=line.split()
    if len(line) == 0:
        #skip empty line
        return None, None, None, None, None
    
    if line[0] == '//' or line[0] == '#':
        #skip comment
        return None, None, None, None, None
    
    if line[0].upper( )== 'RAS:':
        return None, None, None, None, None
    
    if line[0].upper()=='HMI:':
        return None, None, None, None, None
    
    #pravdepodne poskozeny RAS (chybi hlavicka)
    if len(line[0]) > 200:
        return None, None, None, None, None
    
    
    time_s = line[0]
    
    try:
        frame_id = int(line[1], 16)
    except:
        print("EXCEPTION at time %s" % time_s)
        print(line)
        raise
        
    short_id = (frame_id >> 8) & 0xFFFF
    
    size = int(line[2])
    
    payload = []
    #payload is right padded!!!
    
    if size == 0:
        size = 8
        
    u64_payload = int(line[3][0:2*size], 16)
        
    for i in range(size):
        payload.insert(0,u64_payload & 0xFF)
        u64_payload = u64_payload >> 8

    try:
        channel = line[4].split('=')[1]
    except ValueError:
        channel = '?'


    return time_s, frame_id, short_id, channel, payload

def generator(src_filename, line_parser, with_debug_info = False):

    with open(src_filename,'r') as f: 
        for line in f: 
            if line[:1] == '#':
                continue
            if line[:10] == '#timestamp':
                continue
            if line[:4] == 'date':
                continue
            if line[:8] == 'base hex':
                continue
            if line.strip() == 'begin triggerblock':
                continue

            if line[:2] == '==':
                continue
            
            if line.strip() == '':
                continue

            if line.strip() == 'end triggerblock':
                break

            time_s, frame_id, short_id, channel, payload = line_parser(line)
            if with_debug_info:
                yield time_s, frame_id, short_id, channel, payload, line
            else:
                yield time_s, frame_id, short_id, channel, payload
                

def generator_x(src_filename, line_parser):

    with open(src_filename,'r') as f: 
        for line in f: 
            if line[:1] == '#':
                continue
            if line[:10] == '#timestamp':
                continue
            if line[:4] == 'date':
                continue
            if line[:8] == 'base hex':
                continue
            if line.strip() == 'begin triggerblock':
                continue

            if line[:2] == '==':
                continue
            
            if line.strip() == '':
                continue

            if line.strip() == 'end triggerblock':
                break

            time_s, frame_id, short_id, channel, payload = line_parser(line)
            yield time_s, frame_id, short_id, channel, payload, line


####################################
##  Correct time of can messages
####################################
def timestamp_begin_of_file(filename):
    with open(filename,'r') as f: 

        #searching the head of the log for #timestamp:
        i=0
        line=f.readline()
        while line != '':
           if line[:10] == '#timestamp':
               return datetime.fromtimestamp(float(line[11:])/1000.0)
           if i == 10:
               break
           i+=1

        #find last position in file
        position = f.seek(0,2)
        
        #seek 200 from bottom
        f.seek(position-200,0)
        line=f.readline()
        while line != '':
            #print(line)
            try:
                time_stamp = int(line[0:12])
            except ValueError:
                time_stamp = 0
                
            line=f.readline()

    mod_time= os.stat(filename).st_mtime
    return datetime.fromtimestamp(mod_time-time_stamp/1000,tz=None)

def get_timestamp_of_dt(filename, dt):
    start_dt_timestamp = timestamp_begin_of_file(filename).timestamp()
    return dt.timestamp() - start_dt_timestamp

def get_lines_of_file(filename):
    with open(filename,'r') as f: 

        lines_cnt = 0
        line=f.readline()

        while line != '':
            lines_cnt += 1
            line=f.readline()

    return lines_cnt


##########################################
## get day/month/year from first TMCSTATUS
##########################################

def get_date_time_from_tmc_status(filename):
    gen = generator(filename,parse_line_h407_logger)
    
    for i in gen:
        time_s, frame_id, short_id, channel, payload = i
        if short_id == 0x00FF09: # TMCSTATUS
            #2           Hours
            print("DATE: %d.%d TIME: %d:%d" %
                      (payload[3],
                        payload[4],
                        payload[1],
                        payload[2]))
            #3           Minutes
            #4           Day
            #5           Month
            #6-7         Year
            #print(payload)
            return datetime(payload[6]*256+payload[5],payload[4],payload[3],payload[1],payload[2])

    return None