from can_log_parser import CanLogParser, CanFrame
from frame_selector import FrameSelector
from frame_parser import FrameParser
from datetime import datetime

################################################################################
# Tests for frame_parser.py
################################################################################

def test_gen_pwr_state_name():
    assert FrameParser.gen_pwr_state_name(0) == "Off::0"
    assert FrameParser.gen_pwr_state_name(1) == "Starting::1"
    assert FrameParser.gen_pwr_state_name(2) == "Stopping::2"
    assert FrameParser.gen_pwr_state_name(3) == "Run::3"
    assert FrameParser.gen_pwr_state_name(4) == "Error::4"
    assert FrameParser.gen_pwr_state_name(5) == "Deactivated::5"
    assert FrameParser.gen_pwr_state_name(6) == "StartingTimeoutError::6"

def test_gen_pwr_status_name():
    assert FrameParser.gen_pwr_status_name(0) == "NOT_AVAILABLE::0"
    assert FrameParser.gen_pwr_status_name(1) == "INERROR::1"
    assert FrameParser.gen_pwr_status_name(2) == "AVAILABLE::2"
    assert FrameParser.gen_pwr_status_name(3) == "LOWRPM::3"
    assert FrameParser.gen_pwr_status_name(4) == "HIGHRPM::4"
    assert FrameParser.gen_pwr_status_name(5) == "CAN_TIMEOUT::5"

def test_gen_diesel_state():
    assert FrameParser.gen_diesel_state(0) == "LOCKED::0"
    assert FrameParser.gen_diesel_state(1) == "STOPPED::1"
    assert FrameParser.gen_diesel_state(2) == "STARTING::2"
    assert FrameParser.gen_diesel_state(3) == "STOPPING::3"
    assert FrameParser.gen_diesel_state(4) == "LOWSPEED::4"
    assert FrameParser.gen_diesel_state(5) == "HIGHSPEED::5"
    assert FrameParser.gen_diesel_state(6) == "DPF::6"

def test_gen_load_states():
    assert FrameParser.gen_load_states(0) == "LoadOff::0"
    assert FrameParser.gen_load_states(1) == "Loading::1"
    assert FrameParser.gen_load_states(2) == "Unloading::2"
    assert FrameParser.gen_load_states(3) == "LoadOn::3"
    assert FrameParser.gen_load_states(4) == "UnexpectedUnloading::4"
    assert FrameParser.gen_load_states(5) == "LoadError::5"
    assert FrameParser.gen_load_states(6) == "LoadingTimeoutError::6"

def test_gen_dpf_state():
    assert FrameParser.gen_dpf_state(0) == "DPF_MOTOR_OFF::0"
    assert FrameParser.gen_dpf_state(1) == "DPF_NORMAL_OPERATION::1"
    assert FrameParser.gen_dpf_state(2) == "DPF_STANDSTILL_ONGOING::2"
    assert FrameParser.gen_dpf_state(3) == "DPF_STANDSTILL_REQUIRED::3"
    assert FrameParser.gen_dpf_state(4) == "DPF_STANDSTILL_REQUIRED_WARNING::4"
    assert FrameParser.gen_dpf_state(5) == "DPF_STANDSTILL_REQUIRED_SERVICE::5"
    assert FrameParser.gen_dpf_state(6) == "DPF_SERVICE_REQUIRED_FILTER_REMOVAL::6"
    assert FrameParser.gen_dpf_state(7) == "DPF_SERVICE_REQUIRED_OIL::7"
    assert FrameParser.gen_dpf_state(8) == "DPF_SERVICE_REQUIRED_FILTER_WASH::8"
    assert FrameParser.gen_dpf_state(9) == "DPF_STANDSTILL_ERROR::9"

def test_gen_tmc_request():
    assert FrameParser.gen_tmc_request(0) == "NONE::0"
    assert FrameParser.gen_tmc_request(1) == "DLOCK::1"
    assert FrameParser.gen_tmc_request(2) == "DUNLOCK::2"
    assert FrameParser.gen_tmc_request(3) == "DSTART::3"
    assert FrameParser.gen_tmc_request(4) == "DSTOP::4"
    assert FrameParser.gen_tmc_request(5) == "DCOOL::5"
    assert FrameParser.gen_tmc_request(6) == "DSPEED::6"
    assert FrameParser.gen_tmc_request(7) == "CHRSTART::7"
    assert FrameParser.gen_tmc_request(8) == "CHRSTOP::8"
    assert FrameParser.gen_tmc_request(9) == "COOLSTART::9"
    assert FrameParser.gen_tmc_request(10) == "COOLSTOP::10"
    assert FrameParser.gen_tmc_request(11) == "DPFSTART::11"

def test_parse_tmc_status():
    payload = [21, 12, 34, 1, 2, 23, 0, 0]  # Test data
    result = FrameParser.parse_tmc_status(payload)
    assert result["tmc_state"] == 5
    assert "DATE:" in result["tmc_dt"]
    assert result["dplus"] == 1

def test_parse_tmc_status2():
    # 'RTT_timestamp': payload[2] | (payload[3] << 8),  # 3-4 N/A Timestamp (sec)
    # 'TMC_ResetCounter': payload[4] | (payload[5] << 8),  # 5-6 N/A TMC Reset Counter (sec)
    # 'TMC_Watchog_Counter': payload[6] | (payload[7] << 8)}  # 7-8 N/A TMC Watchog Counter (sec)
    payload = [0, 0, 5, 8, 8, 5, 255, 165]  # Test data
    result = FrameParser.parse_tmc_status2(payload)
    assert result['RTT_timestamp'] == 2053
    assert result['TMC_ResetCounter'] == 1288
    assert result['TMC_Watchog_Counter'] == 42495

def test_parse_tmc_status3():
    payload = [37, 37, 37, 37, 0, 0, 0, 0]  # Test data
    result = FrameParser.parse_tmc_status3(payload)

    # for i in range(4):
    #     data[f'PowerSource_Status_{i + 1}'] = payload[i] & 0x07
    #     data[f'PowerSource_Status_{i + 1}_s'] = FrameParser.gen_pwr_status_name(payload[i] & 0x07)
    #     data[f'PowerControl_State_{i + 1}'] = (payload[i] >> 3) & 0x07
    #     data[f'PowerControl_State_{i + 1}_s'] = FrameParser.gen_pwr_state_name((payload[i] >> 3) & 0x07)
    #     data[f'PowerControl_IsError_{i + 1}'] = (payload[i] >> 6) & 0x01

    for i in range(4):
        assert result[f'PowerSource_Status_{i + 1}'] == 5
        assert result[f'PowerSource_Status_{i + 1}_s'] == "CAN_TIMEOUT::5"
        assert result[f'PowerControl_State_{i + 1}'] == 4
        assert result[f'PowerControl_State_{i + 1}_s'] == "Error::4"
        assert result[f'PowerControl_IsError_{i + 1}'] == 0

def test_parse_tmc_status4():

    #     data[f'Charger_State_{i + 1}'] = payload[i] & 0x07
    #     data[f'Charger_State_{i + 1}_s'] = FrameParser.gen_load_states(payload[i] & 0x07)
    #     data[f'Charger_IsError_{i + 1}'] = (payload[i] >> 6) & 0x01
    #     data[f'Charger_IsActivated_{i + 1}'] = (payload[i] >> 7) & 0x01
    #     data[f'Cooler_State_{i + 1}'] = payload[i + 4] & 0x07
    #     data[f'Cooler_State_{i + 1}_s'] = FrameParser.gen_load_states(payload[i + 4] & 0x07)
    #     data[f'Cooler_IsError_{i + 1}'] = (payload[i + 4] >> 6) & 0x01
    #     data[f'Cooler_IsActivated_{i + 1}'] = (payload[i + 4] >> 7) & 0x01

    payload = [90, 90, 90, 90, 90, 90, 90, 90]  # Test data
    result = FrameParser.parse_tmc_status4(payload)
    for i in range(4):
        assert result[f'Charger_State_{i + 1}'] == 2
        assert result[f'Charger_State_{i + 1}_s'] == "Unloading::2"
        assert result[f'Charger_IsError_{i + 1}'] == 1
        assert result[f'Charger_IsActivated_{i + 1}'] == 0
        assert result[f'Cooler_State_{i + 1}'] == 2
        assert result[f'Cooler_State_{i + 1}_s'] == "Unloading::2"
        assert result[f'Cooler_IsError_{i + 1}'] == 1
        assert result[f'Cooler_IsActivated_{i + 1}'] == 0

def test_parse_tmc_status5():
    # 'charg_req': payload[0] & 0x01,  # 1.1 Charging Required
    # 'cool_req': (payload[0] >> 1) & 0x01,  # 1.2 Cooling Required
    # 'boost_req': (payload[0] >> 2) & 0x01,  # 1.3 Boost Requested
    # 'read_chrg_state': (payload[0] >> 3) & 0x01,  # 1.4 Read Charging State
    # 'pwr_finished_flags': (payload[0] >> 4) & 0x0F,  # 1.5-1.8 PwrMng Finished Flags
    # 'run_1_id': payload[5] & 0x07,  # 6.1-3 UnitId
    # 'run_1_charging_assigned': (payload[5] >> 3) & 0x01,  # 6.4 charging_assigned
    # 'run_1_cooling_assigned': (payload[5] >> 4) & 0x01,  # 6.5 cooling_assigned
    # 'run_2_id': payload[6] & 0x07,  # 7.1-3 UnitId
    # 'run_2_charging_assigned': (payload[6] >> 3) & 0x01,  # 7.4 charging_assigned
    # 'run_2_cooling_assigned': (payload[6] >> 4) & 0x01,  # 7.5 cooling_assigned
    # 'run_3_id': payload[7] & 0x07,  # 7.1-3 UnitId
    # 'run_3_charging_assigned': (payload[7] >> 3) & 0x01,  # 7.4 charging_assigned
    # 'run_3_cooling_assigned': (payload[7] >> 4) & 0x01}  # 6-8.5 cooling_assigned

    payload = [165, 90, 165, 90, 165, 90, 165, 90]  # Test data
    result = FrameParser.parse_tmc_status5(payload)

    assert result['charg_req'] == 1
    assert result['cool_req'] == 0
    assert result['boost_req'] == 1
    assert result['read_chrg_state'] == 0
    assert result['pwr_finished_flags'] == 10
    assert result['run_1_id'] == 2
    assert result['run_1_charging_assigned'] == 1
    assert result['run_1_cooling_assigned'] == 1
    assert result['run_2_id'] == 5
    assert result['run_2_charging_assigned'] == 0
    assert result['run_2_cooling_assigned'] == 0
    assert result['run_3_id'] == 2
    assert result['run_3_charging_assigned'] == 1
    assert result['run_3_cooling_assigned'] == 1

def test_parse_tmc2acu():
    # 'tmc_req_{channel}_s': FrameParser.gen_tmc_request((payload[0] >> 0) & 0x0F),  # 1.1-1.4 N/A TMC Request
    # 'eng_running_{channel}': (payload[1] >> 0) & 0x01,  # 2.1 N/A Engine running cmd
    # 'charging_running_{channel}': (payload[1] >> 1) & 0x01,  # 2.2 N/A Charging running cmd
    # 'cooling_running_{channel}': (payload[1] >> 3) & 0x01,  # 2.4 N/A Cooling running cmd
    # 'dpf_running_{channel}': (payload[1] >> 4) & 0x01,  # 2.5 N/A DPF running cmd
    # 'relief_valve_{channel}': (payload[1] >> 7) & 0x01,  # 2.8 N/A Relief Valve cmd
    # 'eng_speed_{channel}': payload[4] | (payload[5] << 8)}  # 5-6 N/A Engine Speed

    payload = [5, 173, 0, 0, 128, 10, 0, 0]  # Test data
    channel = [1, 2]

    for ch in channel:
        result = FrameParser.parse_tmc2acu(ch, payload)
        assert result[f'tmc_req_{ch}_s'] == "DCOOL::5"
        assert result[f'eng_running_{ch}'] == 1
        assert result[f'charging_running_{ch}'] == 0
        assert result[f'cooling_running_{ch}'] == 1
        assert result[f'dpf_running_{ch}'] == 0
        assert result[f'relief_valve_{ch}'] == 1
        assert result[f'eng_speed_{ch}'] == 2688

def test_parse_tmc2emcu():
    # 'energy_source_select_{channel}': payload[1] & 0x03,  # 2.1-2.2 N/A Energy Source Select cmd
    # 'elmot_running_{channel}': (payload[1] >> 2) & 0x01,  # 2.3 N/A Elmot running cmd
    # 'elmot_charging_running_{channel}': (payload[1] >> 3) & 0x01,  # 2.4 N/A Elmot charging running cmd
    # 'aux_param_{channel}': payload[2]}  # 3 N/A AuxParam

    payload = [0, 6, 45, 0, 0, 0, 0, 0]  # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_tmc2emcu(ch, payload)
        assert result[f'energy_source_select_{ch}'] == 2
        assert result[f'elmot_running_{ch}'] == 1
        assert result[f'elmot_charging_running_{ch}'] == 0
        assert result[f'aux_param_{ch}'] == 45

def test_parse_acu_status():
    # 'diesel_state_{channel}': (payload[0] >> 4) & 0x0F,  # 1.5-1.8 Diesel State
    # 'diesel_state_{channel}_s': FrameParser.gen_diesel_state((payload[0] >> 4) & 0x0F),
    # 'dpf_state_{channel}_s': FrameParser.gen_dpf_state(payload[1] & 0x0F),
    # 'cooling_active_{channel}': (payload[1] >> 6) & 0x01,  # 2.7 Cooling Active
    # 'relief_valve_enable_{channel}': (payload[1] >> 7) & 0x01,  # 2.8 Relief Valve Enable
    # 'low_pressure_{channel}': (4.375 * (payload[5] / 10.0) - 18.3) / 10.0,
    # 'high_pressure_{channel}': (18.75 * (payload[6] / 10.0) - 75) / 10.0}

    payload = [20, 85, 0, 0, 0, 10, 20, 0] # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_acu_status(ch, payload)
        assert result[f'diesel_state_{ch}'] == 1
        assert result[f'diesel_state_{ch}_s'] == "STOPPED::1"
        assert result[f'dpf_state_{ch}_s'] == "DPF_STANDSTILL_REQUIRED_SERVICE::5"
        assert result[f'cooling_active_{ch}'] == 1
        assert result[f'relief_valve_enable_{ch}'] == 0
        assert f"low_pressure_{ch}" in result
        assert f"high_pressure_{ch}" in result

def test_parse_acu_status2():
    # data = {f'acu_supply_{channel}': payload[1] * 0.125}

    payload = [0, 80, 0, 0, 0, 0, 0, 0]  # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_acu_status2(ch, payload)
        assert result[f'acu_supply_{ch}'] == payload[1] * 0.125

def test_parse_acu_status3():
    # f'aftertreatment_diesel_particulate_filter_passive_regeneration_status_{channel}': payload[1] & 0x03,
    # f'aftertreatment_diesel_particulate_filter_active_regeneration_status_{channel}': (payload[1] >> 2) & 0x03,
    # f'dpf_active_regeneration_inhibited_status_{channel}': payload[2] & 0x03,
    # f'dpf_active_regeneration_inhibited_due_to_inhibit_switch_by_CAN_{channel}': (payload[2] >> 2) & 0x03,
    # f'dpf_active_regeneration_inhibited_due_to_parking_brake_{channel}': payload[4] & 0x03,
    # f'dpf_active_regeneration_inhibited_due_to_neutral_{channel}': (payload[3] >> 4) & 0x03,
    # f'dpf_active_regeneration_inhibited_system_fault_{channel}': (payload[4] >> 4) & 0x03,
    # f'dpf_active_regeneration_inhibited_system_timeout_{channel}': (payload[4] >> 6) & 0x03,
    # f'dpf_active_regeneration_inhibited_system_lockout_{channel}': (payload[5] >> 2) & 0x03,
    # f'dpf_active_regeneration_inhibited_engine_not_warmed_up_{channel}': (payload[5] >> 4) & 0x03,
    # f'exhaust_high_temperature_lamp_command_{channel}': (payload[6] >> 2) & 0x07,
    # f'dpf_active_regeneration_forced_status_{channel}': (payload[6] >> 5) & 0x07,
    # f'dpf_conditions_not_met_{channel}': (payload[7] >> 4) & 0x02}

    payload = [90, 165, 90, 165, 90, 165, 90, 165]  # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_acu_status3(ch, payload)
        assert result[f'aftertreatment_diesel_particulate_filter_passive_regeneration_status_{ch}'] == 1
        assert result[f'aftertreatment_diesel_particulate_filter_active_regeneration_status_{ch}'] == 1
        assert result[f'dpf_active_regeneration_inhibited_status_{ch}'] == 2
        assert result[f'dpf_active_regeneration_inhibited_due_to_inhibit_switch_by_CAN_{ch}'] == 2
        assert result[f'dpf_active_regeneration_inhibited_due_to_parking_brake_{ch}'] == 2
        assert result[f'dpf_active_regeneration_inhibited_due_to_neutral_{ch}'] == 2
        assert result[f'dpf_active_regeneration_inhibited_system_fault_{ch}'] == 1
        assert result[f'dpf_active_regeneration_inhibited_system_timeout_{ch}'] == 1
        assert result[f'dpf_active_regeneration_inhibited_system_lockout_{ch}'] == 1
        assert result[f'dpf_active_regeneration_inhibited_engine_not_warmed_up_{ch}'] == 2
        assert result[f'exhaust_high_temperature_lamp_command_{ch}'] == 6
        assert result[f'dpf_active_regeneration_forced_status_{ch}'] == 2
        assert result[f'dpf_conditions_not_met_{ch}'] == 2

def test_parse_acu_engine_status():
    # f'diesel_torque_{channel}': payload[0] - 125,
    # f'diesel_coolant_temp_{channel}': payload[2] - 40 # 3 Engine Coolant Temperature (1 deg C/bit, -40 deg C offset)
    # f'diesel_moto_hours_{channel}': payload[4] | (payload[5] << 8) | (payload[6] << 16) | (payload[7] << 24)}  # 5-8 Engine Total Hours of Operation

    payload = [175, 0, 120, 0, 1, 2, 3, 4]  # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_acu_engine_status(ch, payload)
        assert result[f'diesel_torque_{ch}'] == 50
        assert result[f'diesel_coolant_temp_{ch}'] == 80
        assert result[f'diesel_moto_hours_{ch}'] == 67305985

def test_parse_acu_engine_status2():
    # f'dpf_time_{channel}': payload[0],
    # f'soot_{channel}': payload[1],
    # f'ash_{channel}': payload[2],
    # f'current_diesel_rpm_{channel}': payload[3] | (payload[4] << 8)}  # 4-5 1 rpm /bit, Offset 0

    payload = [5, 80, 36, 10, 35, 0, 0, 0]  # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_acu_engine_status2(ch, payload)
        assert result[f'dpf_time_{ch}'] == 5
        assert result[f'soot_{ch}'] == 80
        assert result[f'ash_{ch}'] == 36
        assert result[f'current_diesel_rpm_{ch}'] == 8970

def test_parse_acu_error():
    # f'Acu_Error_{channel}' = payload[0] & 0x0F
    # f'Cooling_Error_{channel}' = (payload[0] >> 4) & 0x0F
    # f'Charging_Error_{channel}' = payload[1] & 0x0F
    # f'Intake_Servo_Error_{channel}' = (payload[1] >> 4) & 0x01
    # f'Outtake_Servo_Error_{channel}' = (payload[1] >> 5) & 0x01
    # f'Diesel_Trouble_Codes_Total_Num_{channel}' = payload[2]

    payload = [53, 23, 100, 0, 0, 0, 0, 0]  # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_acu_error(ch, payload)
        assert result[f'Acu_Error_{ch}'] == 5
        assert result[f'Cooling_Error_{ch}'] == 3
        assert result[f'Charging_Error_{ch}'] == 7
        assert result[f'Intake_Servo_Error_{ch}'] == 1
        assert result[f'Outtake_Servo_Error_{ch}'] == 0
        assert result[f'Diesel_Trouble_Codes_Total_Num_{ch}'] == 100

def test_parse_parse_emcu_status():
    # f'EMCU_State_{channel}': payload[0] & 0x0F,
    # f'Running_{channel}': (payload[0] >> 4) & 0x01,
    # f'Charging0_{channel}': (payload[0] >> 5) & 0x01,
    # f'Source_Available_{channel}': payload[1] & 0x03,
    # f'Charging1_{channel}': (payload[0] >> 7) & 0x01,
    # f'Source_Selected_{channel}': (payload[1] >> 2) & 0x03,
    # f'Emergency_Run_{channel}': (payload[1] >> 4) & 0x01,
    # f'Emergency_Elmot_Block_{channel}': (payload[1] >> 5) & 0x01,
    # f'On_Run_{channel}': (payload[1] >> 6) & 0x01,
    # f'Bypassed_{channel}': (payload[1] >> 7) & 0x01,
    # f'Ok_Softstarter_{channel}': (payload[2] >> 0) & 0x01,
    # f'Overload_Softstarter_{channel}': (payload[2] >> 1) & 0x01,
    # f'Manual_On_{channel}': (payload[2] >> 2) & 0x01,
    # f'Manual_Off_{channel}': (payload[2] >> 3) & 0x01,
    # f'Elmot_State_{channel}': (payload[2] >> 4) & 0x0F,
    # f'Door_{channel}': (payload[3] >> 0) & 0x01}

    payload = [165, 90, 165, 90, 165, 90, 165, 90]  # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_emcu_status(ch, payload)
        assert result[f'EMCU_State_{ch}'] == 5
        assert result[f'Running_{ch}'] == 0
        assert result[f'Charging0_{ch}'] == 1
        assert result[f'Source_Available_{ch}'] == 2
        assert result[f'Charging1_{ch}'] == 1
        assert result[f'Source_Selected_{ch}'] == 2
        assert result[f'Emergency_Run_{ch}'] == 1
        assert result[f'Emergency_Elmot_Block_{ch}'] == 0
        assert result[f'On_Run_{ch}'] == 1
        assert result[f'Bypassed_{ch}'] == 0
        assert result[f'Ok_Softstarter_{ch}'] == 1
        assert result[f'Overload_Softstarter_{ch}'] == 0
        assert result[f'Manual_On_{ch}'] == 1
        assert result[f'Manual_Off_{ch}'] == 0
        assert result[f'Elmot_State_{ch}'] == 10
        assert result[f'Door_{ch}'] == 0

def test_parse_parse_emcu_error():
    # f'Energy_Source_1_Error_{channel}': payload[0] & 0x0F,
    # f'Energy_Source_2_Error_{channel}': (payload[0] >> 4) & 0x0F,
    # f'Elmot_Charge_Error_{channel}': payload[1] & 0x0F,  # 2.1-2.4 charge error
    # f'Elmot_Error_{channel}': payload[2] & 0x0F}  # 3-4 Elmot error

    payload = [53, 15, 10, 0, 0, 0, 0, 0]  # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_emcu_error(ch, payload)
        assert result[f'Energy_Source_1_Error_{ch}'] == 5
        assert result[f'Energy_Source_2_Error_{ch}'] == 3
        assert result[f'Elmot_Charge_Error_{ch}'] == 15
        assert result[f'Elmot_Error_{ch}'] == 10

def test_parse_acu_diagnostics2():
    # f'SRV_ISOLATE_IN_{channel}': (payload[0] >> 0) & 0x01,
    # f'SRV_ISOLATE_FB_{channel}': (payload[0] >> 1) & 0x01,
    # f'MCU_SRV_SUP_ENA_{channel}': (payload[0] >> 2) & 0x01,
    # f'SRV_SUP_ENA_{channel}': (payload[0] >> 3) & 0x01,
    # f'MCU_OE1_{channel}': (payload[0] >> 4) & 0x01,
    # f'SRV_A_OPEN_DRIVE_{channel}': (payload[0] >> 5) & 0x01,
    # f'SRV_B_OPEN_DRIVE_{channel}': (payload[0] >> 6) & 0x01,
    # f'SRV_A_DIV_ENA_{channel}': (payload[0] >> 7) & 0x01,
    # f'SRV_B_DIV_ENA_{channel}': (payload[1] >> 0) & 0x01,
    # f'SRV_SUP_ADC_{channel}': payload[2] | (payload[3] << 8)}

    payload = [90, 165, 90, 165, 90, 165, 90, 165]  # Test data
    channel = [1, 2]
    for ch in channel:
        result = FrameParser.parse_acu_diagnostics2(ch, payload)
        assert result[f'SRV_ISOLATE_IN_{ch}'] == 0
        assert result[f'SRV_ISOLATE_FB_{ch}'] == 1
        assert result[f'MCU_SRV_SUP_ENA_{ch}'] == 0
        assert result[f'SRV_SUP_ENA_{ch}'] == 1
        assert result[f'MCU_OE1_{ch}'] == 1
        assert result[f'SRV_A_OPEN_DRIVE_{ch}'] == 0
        assert result[f'SRV_B_OPEN_DRIVE_{ch}'] == 1
        assert result[f'SRV_A_DIV_ENA_{ch}'] == 0
        assert result[f'SRV_B_DIV_ENA_{ch}'] == 1
        assert result[f'SRV_SUP_ADC_{ch}'] == 42330

################################################################################
# Tests for frame_selector.py
################################################################################
# Dummy frame
class DummyFrame:
    def __init__(self, short_id, channel, payload, time_ms="456"):
        self.short_id = short_id
        self.channel = channel
        self.payload = payload
        self.time_ms = time_ms

def test_parse_returns_text():
    def fake_parser(channel, payload):
        return {"diesel_state": 1, "cooling_active": 0}

    # Select first handler
    handler = FrameSelector.HANDLERS[0]
    handler.parser_method = fake_parser
    handler.short_id = 0x111

    frame = DummyFrame(short_id=0x111, channel=1, payload=[0x00])

    result = handler.parse(frame)

    assert result["cooling_active"] == 0
    assert result["diesel_state"] == 1

def test_short_ids_are_unique():
    """All handlers must have unique short_id."""
    short_ids = [handler.short_id for handler in FrameSelector.HANDLERS]
    # Comprehension set
    duplicates = {sid for sid in short_ids if short_ids.count(sid) > 1}
    assert not duplicates, f"Duplicate short_id(s) found: {duplicates}"

def test_names_are_unique():
    """All handlers must have unique name."""
    names = [handler.name for handler in FrameSelector.HANDLERS]
    duplicates = {n for n in names if names.count(n) > 1}
    assert not duplicates, f"Duplicate name(s) found: {duplicates}"

def test_all_handlers_have_short_id_and_name():
    """Each handler should define short_id and name."""
    for handler in FrameSelector.HANDLERS:
        assert handler.short_id is not None, f"{handler.__name__} has no short_id"
        assert handler.name is not None, f"{handler.__name__} has no name"
        assert isinstance(handler.short_id, int), f"{handler.__name__} short_id must be int"
        assert isinstance(handler.name, str), f"{handler.__name__} name must be str"

################################################################################
# Tests for can_log_parser.py
################################################################################
#TODO TBD

def test_extract_escaped_simple():
    # FE must be removed
    assert CanLogParser.extract_escaped("FE10A0") == "10A0"

def test_extract_escaped_no_escape():
    # input and output must be equal
    assert CanLogParser.extract_escaped("123321") == "123321"

def test_extract_escaped_multiple():
    # FE must be removed
    assert CanLogParser.extract_escaped("AAFE20FEFEEE") == "AA20FEEE"

def test_parse_line_ras():
    line = "RAS: 3 AABBCC"
    frame = CanLogParser.parse_line_h407_logger(line)
    assert isinstance(frame, CanFrame)
    assert frame.payload == [0xAA, 0xBB, 0xCC]

def test_parse_line_hmi():
    line = "HMI: 1 00 FEAA10"
    frame = CanLogParser.parse_line_h407_logger(line)
    assert frame.payload == [0xAA, 0x10]

def test_parse_line_can():
    line = "12345 18FF09AA 8 1122334455667788 CH=1"
    frame = CanLogParser.parse_line_h407_logger(line)
    assert frame.frame_id == 0x18FF09AA
    assert frame.short_id == 0xFF09
    assert frame.channel == "1"
    assert frame.payload == [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]

def test_timestamp_begin_of_file(tmp_path):
    test_file = tmp_path / "log.txt"
    test_file.write_text("#timestamp 1728000000\n")
    ts = CanLogParser.timestamp_begin_of_file(str(test_file))
    assert isinstance(ts, datetime)
    assert abs(ts.timestamp() - 1728000) < 10

def test_generator_parses_only_valid_lines(tmp_path):
    test_file = tmp_path / "log.txt"
    test_file.write_text("""
#timestamp 123456789
12345 18FF09AA 8 1122334455667788 CH=1
# comment
RAS: 3 AABBCC
""")
    frames = list(CanLogParser.generator(test_file, CanLogParser.parse_line_h407_logger))
    assert len(frames) == 2 # Two messages in frame
    assert all(isinstance(f, CanFrame) for f in frames)