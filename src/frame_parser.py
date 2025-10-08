import enum

# PowerControl_States
class PwrStatus(enum.Enum):
    NOT_AVAILABLE=0     # Power Resource is not installed
    INERROR = 1         # Power Resource is installed but in error
    AVAILABLE = 2       # Power Resource is installed and can be used
    LOWRPM = 3          # Power Resource is installed and running at low speed
    HIGHRPM = 4         # Power Resource is installed and running at high speed
    CAN_TIMEOUT = 5     #P ower Resource is installed and CAN communication stop working

class PwrState(enum.Enum):
    Off = 0
    Starting = 1
    Stopping = 2
    Run = 3
    Error = 4
    Deactivated = 5
    StartingTimeoutError=6

class DieselState(enum.Enum):
    LOCKED = 0
    STOPPED = 1
    STARTING = 2
    STOPPING = 3
    LOWSPEED = 4
    HIGHSPEED = 5
    DPF = 6

class LdStates(enum.Enum):
    LoadOff   = 0
    Loading   = 1
    Unloading = 2
    LoadOn    = 3
    UnexpectedUnloading = 4
    LoadError = 5
    LoadingTimeoutError = 6
    
class DpfState(enum.Enum):
    DPF_MOTOR_OFF = 0
    DPF_NORMAL_OPERATION = 1
    DPF_STANDSTILL_ONGOING = 2
    DPF_STANDSTILL_REQUIRED = 3
    DPF_STANDSTILL_REQUIRED_WARNING = 4
    DPF_STANDSTILL_REQUIRED_SERVICE = 5
    DPF_SERVICE_REQUIRED_FILTER_REMOVAL = 6
    DPF_SERVICE_REQUIRED_OIL = 7
    DPF_SERVICE_REQUIRED_FILTER_WASH = 8
    DPF_STANDSTILL_ERROR = 9
    
    
class TmcRequest(enum.Enum):
    NONE = 0
    DLOCK = 1
    DUNLOCK = 2
    DSTART = 3
    DSTOP = 4
    DCOOL = 5
    DSPEED = 6
    CHRSTART = 7
    CHRSTOP = 8
    COOLSTART = 9
    COOLSTOP = 10
    DPFSTART = 11


class FrameParser:
    """ Parser of CAN bus frames """

    @staticmethod
    def gen_pwr_state_name(value): return f'{PwrState(value).name}::{value}'

    @staticmethod
    def gen_pwr_status_name(value): return f'{PwrStatus(value).name}::{value}'

    @staticmethod
    def gen_diesel_state(value): return f'{DieselState(value).name}::{value}'

    @staticmethod
    def gen_load_states(value): return f'{LdStates(value).name}::{value}'

    @staticmethod
    def gen_dpf_state(value): return f'{DpfState(value).name}::{value}'

    @staticmethod
    def gen_tmc_request(value): return f'{TmcRequest(value).name}::{value}'

    @staticmethod
    def parse_tmc_status(payload):
        return {'tmc_state': payload[0] & 0x0F,
                'tmc_dt': f"DATE: {payload[3]:02}.{payload[4]:02}.{payload[5] + payload[6] * 256} TIME: {payload[1]:02}:{payload[2]:02}",
                'dplus': (payload[0] >> 4) & 0x01}

    @staticmethod
    def parse_tmc_status2(payload):
        return {'RTT_timestamp': payload[2] | (payload[3] << 8), # 3-4 N/A Timestamp (sec)
                'TMC_ResetCounter': payload[4] | (payload[5] << 8), # 5-6 N/A TMC Reset Counter (sec)
                'TMC_Watchog_Counter': payload[6] | (payload[7] << 8)} # 7-8 N/A TMC Watchog Counter (sec)

    @staticmethod
    def parse_tmc_status3(payload):
        data = {}
        for i in range(4):
            data[f'PowerSource_Status_{i + 1}'] = payload[i] & 0x07
            data[f'PowerSource_Status_{i + 1}_s'] = FrameParser.gen_pwr_status_name(payload[i] & 0x07)
            data[f'PowerControl_State_{i + 1}'] = (payload[i] >> 3) & 0x07
            data[f'PowerControl_State_{i + 1}_s'] = FrameParser.gen_pwr_state_name((payload[i] >> 3) & 0x07)
            data[f'PowerControl_IsError_{i + 1}'] = (payload[i] >> 6) & 0x01

        return data

    @staticmethod
    def parse_tmc_status4(payload):
        data = {}
        for i in range(4):
            data[f'Charger_State_{i + 1}'] = payload[i] & 0x07
            data[f'Charger_State_{i + 1}_s'] = FrameParser.gen_load_states(payload[i] & 0x07)
            data[f'Charger_IsError_{i + 1}'] = (payload[i] >> 6) & 0x01
            data[f'Charger_IsActivated_{i + 1}'] = (payload[i] >> 7) & 0x01
            data[f'Cooler_State_{i + 1}'] = payload[i + 4] & 0x07
            data[f'Cooler_State_{i + 1}_s'] = FrameParser.gen_load_states(payload[i + 4] & 0x07)
            data[f'Cooler_IsError_{i + 1}'] = (payload[i + 4] >> 6) & 0x01
            data[f'Cooler_IsActivated_{i + 1}'] = (payload[i + 4] >> 7) & 0x01

        return data


    @staticmethod
    def parse_tmc_status5(payload):
        data = {'charg_req': payload[0] & 0x01, # 1.1 Charging Required
                'cool_req': (payload[0] >> 1) & 0x01, # 1.2 Cooling Required
                'boost_req': (payload[0] >> 2) & 0x01, # 1.3 Boost Requested
                'read_chrg_state': (payload[0] >> 3) & 0x01, # 1.4 Read Charging State
                'pwr_finished_flags': (payload[0] >> 4) & 0x0F, # 1.5-1.8 PwrMng Finished Flags
                'run_1_id': payload[5] & 0x07, # 6.1-3 UnitId
                'run_1_charging_assigned': (payload[5] >> 3) & 0x01, # 6.4 charging_assigned
                'run_1_cooling_assigned': (payload[5] >> 4) & 0x01, # 6.5 cooling_assigned
                'run_2_id': payload[6] & 0x07, # 7.1-3 UnitId
                'run_2_charging_assigned': (payload[6] >> 3) & 0x01, # 7.4 charging_assigned
                'run_2_cooling_assigned': (payload[6] >> 4) & 0x01, # 7.5 cooling_assigned
                'run_3_id': payload[7] & 0x07, # 7.1-3 UnitId
                'run_3_charging_assigned': (payload[7] >> 3) & 0x01, # 7.4 charging_assigned
                'run_3_cooling_assigned': (payload[7] >> 4) & 0x01} # 6-8.5 cooling_assigned
        finished_flags = (payload[0] >> 4) & 0x0F
        for i in range(1, 9):
            data[f'pwr_finished_flag_STATE_{i}'] = (finished_flags == i)
        return data

    @staticmethod
    def parse_tmc2acu(channel, payload):
        data = {f'tmc_req_{channel}_s': FrameParser.gen_tmc_request((payload[0] >> 0) & 0x0F),  # 1.1-1.4 N/A TMC Request
                f'eng_running_{channel}': (payload[1] >> 0) & 0x01,  # 2.1 N/A Engine running cmd
                f'charging_running_{channel}': (payload[1] >> 1) & 0x01,  # 2.2 N/A Charging running cmd
                f'cooling_running_{channel}': (payload[1] >> 3) & 0x01,  # 2.4 N/A Cooling running cmd
                f'dpf_running_{channel}': (payload[1] >> 4) & 0x01,  # 2.5 N/A DPF running cmd
                f'relief_valve_{channel}': (payload[1] >> 7) & 0x01,  # 2.8 N/A Relief Valve cmd
                f'eng_speed_{channel}': payload[4] | (payload[5] << 8)}  # 5-6 N/A Engine Speed

        return data

    @staticmethod
    def parse_tmc2emcu(channel, payload):
        data = {f'energy_source_select_{channel}': payload[1] & 0x03,  # 2.1-2.2 N/A Energy Source Select cmd
                f'elmot_running_{channel}': (payload[1] >> 2) & 0x01,  # 2.3 N/A Elmot running cmd
                f'elmot_charging_running_{channel}': (payload[1] >> 3) & 0x01,  # 2.4 N/A Elmot charging running cmd
                f'aux_param_{channel}': payload[2]}  # 3 N/A AuxParam

        return data

    @staticmethod
    def parse_acu_status(channel, payload):
        data = {f'diesel_state_{channel}': (payload[0] >> 4) & 0x0F,  # 1.5-1.8 Diesel State
                f'diesel_state_{channel}_s': FrameParser.gen_diesel_state((payload[0] >> 4) & 0x0F),
                f'dpf_state_{channel}_s': FrameParser.gen_dpf_state(payload[1] & 0x0F),
                f'cooling_active_{channel}': (payload[1] >> 6) & 0x01,  # 2.7 Cooling Active
                f'relief_valve_enable_{channel}': (payload[1] >> 7) & 0x01,  # 2.8 Relief Valve Enable
                f'low_pressure_{channel}': (4.375 * (payload[5] / 10.0) - 18.3) / 10.0,
                f'high_pressure_{channel}': (18.75 * (payload[6] / 10.0) - 75) / 10.0}

        return data

    @staticmethod
    def parse_acu_status2(channel, payload):
        data = {f'acu_supply_{channel}': payload[1] * 0.125}

        return data

    @staticmethod
    def parse_acu_status3(channel, payload):
        data = {f'aftertreatment_diesel_particulate_filter_passive_regeneration_status_{channel}': payload[1] & 0x03,
                f'aftertreatment_diesel_particulate_filter_active_regeneration_status_{channel}': (payload[1] >> 2) & 0x03,
                f'dpf_active_regeneration_inhibited_status_{channel}': payload[2] & 0x03,
                f'dpf_active_regeneration_inhibited_due_to_inhibit_switch_by_CAN_{channel}': (payload[2] >> 2) & 0x03,
                f'dpf_active_regeneration_inhibited_due_to_neutral_{channel}': (payload[3] >> 4) & 0x03,
                f'dpf_active_regeneration_inhibited_due_to_parking_brake_{channel}': payload[4] & 0x03,
                f'dpf_active_regeneration_inhibited_system_fault_{channel}': (payload[4] >> 4) & 0x03,
                f'dpf_active_regeneration_inhibited_system_timeout_{channel}': (payload[4] >> 6) & 0x03,
                f'dpf_active_regeneration_inhibited_system_lockout_{channel}': (payload[5] >> 2) & 0x03,
                f'dpf_active_regeneration_inhibited_engine_not_warmed_up_{channel}': (payload[5] >> 4) & 0x03,
                f'exhaust_high_temperature_lamp_command_{channel}': (payload[6] >> 2) & 0x07,
                f'dpf_active_regeneration_forced_status_{channel}': (payload[6] >> 5) & 0x07,
                f'dpf_conditions_not_met_{channel}': (payload[7] >> 4) & 0x02}

        return data

    @staticmethod
    def parse_acu_engine_status(channel, payload):
        data = {f'diesel_torque_{channel}': payload[0] - 125,
                f'diesel_coolant_temp_{channel}': payload[2] - 40,
                # 3 Engine Coolant Temperature (1 deg C/bit, -40 deg C offset)
                f'diesel_moto_hours_{channel}': payload[4] | (payload[5] << 8) | (payload[6] << 16) | (payload[7] << 24)}  # 5-8 Engine Total Hours of Operation

        return data

    # Frame ID = 0xFF0E
    @staticmethod
    def parse_acu_engine_status2(channel, payload):
        data = {f'dpf_time_{channel}': payload[0],
                f'soot_{channel}': payload[1],
                f'ash_{channel}': payload[2],
                f'current_diesel_rpm_{channel}': payload[3] | (payload[4] << 8)}  # 4-5 1 rpm /bit, Offset 0

        return data

    @staticmethod
    def parse_acu_error(channel, payload, multiframe=False):
        data = {}

        # //1.1-1.4  Diesel Error
        # //1.5-1.8  Cooling Error
        # //2.1-2.4  Charging Error
        # //in multiframe TP.DT payload starts from byte 2
        if multiframe:
            data[f'Acu_Error_{channel}'] = payload[1] & 0x0F
            data[f'Cooling_Error_{channel}'] = (payload[1] >> 4) & 0x0F
            data[f'Charging_Error_{channel}'] = payload[2] & 0x0F
            data[f'Diesel_Trouble_Codes_Total_Num_{channel}'] = payload[3]
        else:
            data[f'Acu_Error_{channel}'] = payload[0] & 0x0F
            data[f'Cooling_Error_{channel}'] = (payload[0] >> 4) & 0x0F
            data[f'Charging_Error_{channel}'] = payload[1] & 0x0F
            data[f'Intake_Servo_Error_{channel}'] = (payload[1] >> 4) & 0x01
            data[f'Outtake_Servo_Error_{channel}'] = (payload[1] >> 5) & 0x01
            data[f'Diesel_Trouble_Codes_Total_Num_{channel}'] = payload[2]

        return data

    @staticmethod
    def parse_emcu_status(channel, payload):
        data = {f'EMCU_State_{channel}': payload[0] & 0x0F,
                f'Running_{channel}': (payload[0] >> 4) & 0x01,
                f'Charging0_{channel}': (payload[0] >> 5) & 0x01,
                f'Source_Available_{channel}': payload[1] & 0x03,
                f'Charging1_{channel}': (payload[0] >> 7) & 0x01,
                f'Source_Selected_{channel}': (payload[1] >> 2) & 0x03,
                f'Emergency_Run_{channel}': (payload[1] >> 4) & 0x01,
                f'Emergency_Elmot_Block_{channel}': (payload[1] >> 5) & 0x01,
                f'On_Run_{channel}': (payload[1] >> 6) & 0x01,
                f'Bypassed_{channel}': (payload[1] >> 7) & 0x01,
                f'Ok_Softstarter_{channel}': (payload[2] >> 0) & 0x01,
                f'Overload_Softstarter_{channel}': (payload[2] >> 1) & 0x01,
                f'Manual_On_{channel}': (payload[2] >> 2) & 0x01,
                f'Manual_Off_{channel}': (payload[2] >> 3) & 0x01,
                f'Elmot_State_{channel}': (payload[2] >> 4) & 0x0F,
                f'Door_{channel}': (payload[3] >> 0) & 0x01}

        return data

    @staticmethod
    def parse_emcu_error(channel, payload):
        data = {f'Energy_Source_1_Error_{channel}': payload[0] & 0x0F,
                f'Energy_Source_2_Error_{channel}': (payload[0] >> 4) & 0x0F,
                f'Elmot_Charge_Error_{channel}': payload[1] & 0x0F,  # 2.1-2.4 charge error
                f'Elmot_Error_{channel}': payload[2] & 0x0F}  # 3-4 Elmot error

        return data

    @staticmethod
    def parse_acu_diagnostics2(channel, payload):
        data = {f'SRV_ISOLATE_IN_{channel}': (payload[0] >> 0) & 0x01,
                f'SRV_ISOLATE_FB_{channel}': (payload[0] >> 1) & 0x01,
                f'MCU_SRV_SUP_ENA_{channel}': (payload[0] >> 2) & 0x01,
                f'SRV_SUP_ENA_{channel}': (payload[0] >> 3) & 0x01,
                f'MCU_OE1_{channel}': (payload[0] >> 4) & 0x01,
                f'SRV_A_OPEN_DRIVE_{channel}': (payload[0] >> 5) & 0x01,
                f'SRV_B_OPEN_DRIVE_{channel}': (payload[0] >> 6) & 0x01,
                f'SRV_A_DIV_ENA_{channel}': (payload[0] >> 7) & 0x01,
                f'SRV_B_DIV_ENA_{channel}': (payload[1] >> 0) & 0x01,
                f'SRV_SUP_ADC_{channel}': payload[2] | (payload[3] << 8)}

        return data