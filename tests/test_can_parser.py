import pytest
from unittest.mock import MagicMock

from frame_selector import FrameSelector, BaseFrameHandler
from frame_parser import FrameParser

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
    # return {'RTT_timestamp': payload[2] | (payload[3] << 8),  # 3-4 N/A Timestamp (sec)
    #         'TMC_ResetCounter': payload[4] | (payload[5] << 8),  # 5-6 N/A TMC Reset Counter (sec)
    #         'TMC_Watchog_Counter': payload[6] | (payload[7] << 8)}  # 7-8 N/A TMC Watchog Counter (sec)
    pass

def test_parse_tmc_status3():
    payload = [5, 80, 0, 0, 0, 0, 0, 0]  # Test data
    result = FrameParser.parse_tmc_status3(payload)
    # data = {}
    # for i in range(4):
    #     data[f'PowerSource_Status_{i + 1}'] = payload[i] & 0x07
    #     data[f'PowerSource_Status_{i + 1}_s'] = FrameParser.gen_pwr_status_name(payload[i] & 0x07)
    #     data[f'PowerControl_State_{i + 1}'] = (payload[i] >> 3) & 0x07
    #     data[f'PowerControl_State_{i + 1}_s'] = FrameParser.gen_pwr_state_name((payload[i] >> 3) & 0x07)
    #     data[f'PowerControl_IsError_{i + 1}'] = (payload[i] >> 6) & 0x01
    #
    # return data
    assert "PowerSource_Status_1" in result
    assert isinstance(result["PowerControl_State_1_s"], str)

def test_parse_tmc_status4():
    # data = {}
    # for i in range(4):
    #     data[f'Charger_State_{i + 1}'] = payload[i] & 0x07
    #     data[f'Charger_State_{i + 1}_s'] = FrameParser.gen_load_states(payload[i] & 0x07)
    #     data[f'Charger_IsError_{i + 1}'] = (payload[i] >> 6) & 0x01
    #     data[f'Charger_IsActivated_{i + 1}'] = (payload[i] >> 7) & 0x01
    #
    #     data[f'Cooler_State_{i + 1}'] = payload[i + 4] & 0x07
    #     data[f'Cooler_State_{i + 1}_s'] = FrameParser.gen_load_states(payload[i + 4] & 0x07)
    #     data[f'Cooler_IsError_{i + 1}'] = (payload[i + 4] >> 6) & 0x01
    #     data[f'Cooler_IsActivated_{i + 1}'] = (payload[i + 4] >> 7) & 0x01
    #
    # return data
    pass

def test_parse_tmc_status5():
    # data = {'charg_req': payload[0] & 0x01,  # 1.1 Charging Required
    #         'cool_req': (payload[0] >> 1) & 0x01,  # 1.2 Cooling Required
    #         'boost_req': (payload[0] >> 2) & 0x01,  # 1.3 Boost Requested
    #         'read_chrg_state': (payload[0] >> 3) & 0x01,  # 1.4 Read Charging State
    #         'pwr_finished_flags': (payload[0] >> 4) & 0x0F,  # 1.5-1.8 PwrMng Finished Flags
    #         'run_1_id': payload[5] & 0x07,  # 6.1-3 UnitId
    #         'run_1_charging_assigned': (payload[5] >> 3) & 0x01,  # 6.4 charging_assigned
    #         'run_1_cooling_assigned': (payload[5] >> 4) & 0x01,  # 6.5 cooling_assigned
    #         'run_2_id': payload[6] & 0x07,  # 7.1-3 UnitId
    #         'run_2_charging_assigned': (payload[6] >> 3) & 0x01,  # 7.4 charging_assigned
    #         'run_2_cooling_assigned': (payload[6] >> 4) & 0x01,  # 7.5 cooling_assigned
    #         'run_3_id': payload[7] & 0x07,  # 7.1-3 UnitId
    #         'run_3_charging_assigned': (payload[7] >> 3) & 0x01,  # 7.4 charging_assigned
    #         'run_3_cooling_assigned': (payload[7] >> 4) & 0x01}  # 6-8.5 cooling_assigned
    # finished_flags = (payload[0] >> 4) & 0x0F
    # for i in range(1, 9):
    #     data[f'pwr_finished_flag_STATE_{i}'] = (finished_flags == i)
    # return data
    pass

def test_parse_tmc2acu():
    # data = {f'tmc_req_{channel}_s': FrameParser.gen_tmc_request((payload[0] >> 0) & 0x0F),  # 1.1-1.4 N/A TMC Request
    #         f'eng_running_{channel}': (payload[1] >> 0) & 0x01,  # 2.1 N/A Engine running cmd
    #         f'charging_running_{channel}': (payload[1] >> 1) & 0x01,  # 2.2 N/A Charging running cmd
    #         f'cooling_running_{channel}': (payload[1] >> 3) & 0x01,  # 2.4 N/A Cooling running cmd
    #         f'dpf_running_{channel}': (payload[1] >> 4) & 0x01,  # 2.5 N/A DPF running cmd
    #         f'relief_valve_{channel}': (payload[1] >> 7) & 0x01,  # 2.8 N/A Relief Valve cmd
    #         f'eng_speed_{channel}': payload[4] | (payload[5] << 8)}  # 5-6 N/A Engine Speed
    #
    # return data
    pass

def test_parse_tmc2emcu():
    # data = {f'energy_source_select_{channel}': payload[1] & 0x03,  # 2.1-2.2 N/A Energy Source Select cmd
    #         f'elmot_running_{channel}': (payload[1] >> 2) & 0x01,  # 2.3 N/A Elmot running cmd
    #         f'elmot_charging_running_{channel}': (payload[1] >> 3) & 0x01,  # 2.4 N/A Elmot charging running cmd
    #         f'aux_param_{channel}': payload[2]}  # 3 N/A AuxParam
    #
    # return data
    pass

def test_parse_acu_status():
    # data = {f'diesel_state_{channel}': (payload[0] >> 4) & 0x0F,  # 1.5-1.8 Diesel State
    #         f'diesel_state_{channel}_s': FrameParser.gen_diesel_state((payload[0] >> 4) & 0x0F),
    #         f'dpf_state_{channel}_s': FrameParser.gen_dpf_state(payload[1] & 0x0F),
    #         f'cooling_active_{channel}': (payload[1] >> 6) & 0x01,  # 2.7 Cooling Active
    #         f'relief_valve_enable_{channel}': (payload[1] >> 7) & 0x01,  # 2.8 Relief Valve Enable
    #         f'low_pressure_{channel}': (4.375 * (payload[5] / 10.0) - 18.3) / 10.0,
    #         f'high_pressure_{channel}': (18.75 * (payload[6] / 10.0) - 75) / 10.0}
    #
    # return data
    payload = [20, 85, 0, 0, 0, 10, 20, 0] # Test data
    result = FrameParser.parse_acu_status(1, payload)
    assert result["diesel_state_1"] == 1
    assert result["cooling_active_1"] == 1
    assert "low_pressure_1" in result
    assert "high_pressure_1" in result

def test_parse_acu_status2():
    # data = {f'acu_supply_{channel}': payload[1] * 0.125}
    #
    # return data
    pass

def test_parse_acu_status3():
    # data = {f'aftertreatment_diesel_particulate_filter_passive_regeneration_status_{channel}': payload[1] & 0x03,
    #         f'aftertreatment_diesel_particulate_filter_active_regeneration_status_{channel}': (payload[1] >> 2) & 0x03,
    #         f'dpf_active_regeneration_inhibited_status_{channel}': payload[2] & 0x03,
    #         f'dpf_active_regeneration_inhibited_due_to_inhibit_switch_by_CAN_{channel}': (payload[2] >> 2) & 0x03,
    #         f'dpf_active_regeneration_inhibited_due_to_neutral_{channel}': (payload[3] >> 4) & 0x03,
    #         f'dpf_active_regeneration_inhibited_due_to_parking_brake_{channel}': payload[4] & 0x03,
    #         f'dpf_active_regeneration_inhibited_system_fault_{channel}': (payload[4] >> 4) & 0x03,
    #         f'dpf_active_regeneration_inhibited_system_timeout_{channel}': (payload[4] >> 6) & 0x03,
    #         f'dpf_active_regeneration_inhibited_system_lockout_{channel}': (payload[5] >> 2) & 0x03,
    #         f'dpf_active_regeneration_inhibited_engine_not_warmed_up_{channel}': (payload[5] >> 4) & 0x03,
    #         f'exhaust_high_temperature_lamp_command_{channel}': (payload[6] >> 2) & 0x07,
    #         f'dpf_active_regeneration_forced_status_{channel}': (payload[6] >> 5) & 0x07,
    #         f'dpf_conditions_not_met_{channel}': (payload[7] >> 4) & 0x02}
    #
    # return data
    pass

def test_parse_acu_engine_status():
    # data = {f'diesel_torque_{channel}': payload[0] - 125,
    #         f'diesel_coolant_temp_{channel}': payload[2] - 40,
    #         # 3 Engine Coolant Temperature (1 deg C/bit, -40 deg C offset)
    #         f'diesel_moto_hours_{channel}': payload[4] | (payload[5] << 8) | (payload[6] << 16) | (payload[7] << 24)}  # 5-8 Engine Total Hours of Operation
    #
    # return data
    pass

def test_parse_acu_engine_status2():
    # data = {f'dpf_time_{channel}': payload[0],
    #         f'soot_{channel}': payload[1],
    #         f'ash_{channel}': payload[2],
    #         f'current_diesel_rpm_{channel}': payload[3] | (payload[4] << 8)}  # 4-5 1 rpm /bit, Offset 0
    #
    # return data
    pass

def test_parse_acu_error():
    # data = {}
    #
    # data[f'Acu_Error_{channel}'] = payload[0] & 0x0F
    # data[f'Cooling_Error_{channel}'] = (payload[0] >> 4) & 0x0F
    # data[f'Charging_Error_{channel}'] = payload[1] & 0x0F
    # data[f'Intake_Servo_Error_{channel}'] = (payload[1] >> 4) & 0x01
    # data[f'Outtake_Servo_Error_{channel}'] = (payload[1] >> 5) & 0x01
    # data[f'Diesel_Trouble_Codes_Total_Num_{channel}'] = payload[2]
    #
    # return data
    pass

def test_parse_parse_emcu_status():
    # data = {f'EMCU_State_{channel}': payload[0] & 0x0F,
    #         f'Running_{channel}': (payload[0] >> 4) & 0x01,
    #         f'Charging0_{channel}': (payload[0] >> 5) & 0x01,
    #         f'Source_Available_{channel}': payload[1] & 0x03,
    #         f'Charging1_{channel}': (payload[0] >> 7) & 0x01,
    #         f'Source_Selected_{channel}': (payload[1] >> 2) & 0x03,
    #         f'Emergency_Run_{channel}': (payload[1] >> 4) & 0x01,
    #         f'Emergency_Elmot_Block_{channel}': (payload[1] >> 5) & 0x01,
    #         f'On_Run_{channel}': (payload[1] >> 6) & 0x01,
    #         f'Bypassed_{channel}': (payload[1] >> 7) & 0x01,
    #         f'Ok_Softstarter_{channel}': (payload[2] >> 0) & 0x01,
    #         f'Overload_Softstarter_{channel}': (payload[2] >> 1) & 0x01,
    #         f'Manual_On_{channel}': (payload[2] >> 2) & 0x01,
    #         f'Manual_Off_{channel}': (payload[2] >> 3) & 0x01,
    #         f'Elmot_State_{channel}': (payload[2] >> 4) & 0x0F,
    #         f'Door_{channel}': (payload[3] >> 0) & 0x01}
    #
    # return data
    pass

def test_parse_parse_emcu_error():
    # data = {f'Energy_Source_1_Error_{channel}': payload[0] & 0x0F,
    #         f'Energy_Source_2_Error_{channel}': (payload[0] >> 4) & 0x0F,
    #         f'Elmot_Charge_Error_{channel}': payload[1] & 0x0F,  # 2.1-2.4 charge error
    #         f'Elmot_Error_{channel}': payload[2] & 0x0F}  # 3-4 Elmot error
    #
    # return data
    pass

def test_parse_acu_diagnostics2():
    # data = {f'SRV_ISOLATE_IN_{channel}': (payload[0] >> 0) & 0x01,
    #         f'SRV_ISOLATE_FB_{channel}': (payload[0] >> 1) & 0x01,
    #         f'MCU_SRV_SUP_ENA_{channel}': (payload[0] >> 2) & 0x01,
    #         f'SRV_SUP_ENA_{channel}': (payload[0] >> 3) & 0x01,
    #         f'MCU_OE1_{channel}': (payload[0] >> 4) & 0x01,
    #         f'SRV_A_OPEN_DRIVE_{channel}': (payload[0] >> 5) & 0x01,
    #         f'SRV_B_OPEN_DRIVE_{channel}': (payload[0] >> 6) & 0x01,
    #         f'SRV_A_DIV_ENA_{channel}': (payload[0] >> 7) & 0x01,
    #         f'SRV_B_DIV_ENA_{channel}': (payload[1] >> 0) & 0x01,
    #         f'SRV_SUP_ADC_{channel}': payload[2] | (payload[3] << 8)}
    #
    # return data
    pass

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

################################################################################
# Tests for frame_selector.py
################################################################################
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


# def test_base_handler_parse_calls_parser():
#     """BaseFrameHandler.parse should call parser_method with payload."""
#     mock_parser = MagicMock(return_value={"ok": True})
#
#     class DummyHandler(BaseFrameHandler):
#         parser_method = staticmethod(mock_parser)
#
#     frame = DummyFrame(short_id=0x01, payload="abc", channel=0, time_ms="123456")
#     result = DummyHandler.parse(frame)
#
#     assert result == {"ok": True}
#     mock_parser.assert_called_once_with("abc")


# def test_select_dict_returns_expected(monkeypatch):
#     """Select_dictionary should return dictionary if frame matches and is selected."""
#     handler = FrameSelector.HANDLERS[0]
#     handler.short_id = 0xABCD
#     handler.parse = classmethod(lambda cls, frame: {"Speed": 100})
#
#     frame = DummyFrame(short_id=0x234, channel=1, time_ms="123", payload=[0x00])
#     result = handler.select(frame)
#     selected = [f"{handler.name}_CH1"]
#
#     result = FrameSelector.select_dictionary(frame, selected)
#
#     assert isinstance(result, dict)
#     assert result["Frame"] == handler.name
#     assert result["Channel"] == 1
#     assert result["Timestamp"] == 123
#     assert result["Speed"] == 100


# def test_select_dict_returns_none_if_not_selected():
#     """select_dict should return None if frame is not in selected_frames."""
#     handler = FrameSelector.HANDLERS[1]
#     handler.short_id = 0x2222
#     handler.parse = classmethod(lambda cls, frame: {"X": 1})
#
#     frame = DummyFrame(short_id=0x2222, channel=2)
#     selected = []  # not selected
#
#     result = FrameSelector.select_dict(frame, selected)
#     assert result is None
#
#
# def test_select_text_returns_string():
#     """select_text should return formatted string if key matches."""
#     handler = FrameSelector.HANDLERS[2]
#     handler.short_id = 0x3333
#     handler.parse = classmethod(lambda cls, frame: {"Temp": 42})
#
#     frame = DummyFrame(short_id=0x3333, channel=5, time_s=9.99)
#     selected = [f"{handler.name}_CH5"]
#
#     result = FrameSelector.select_text(frame, selected)
#
#     assert isinstance(result, str)
#     assert "Timestamp=9.99" in result
#     assert f"Frame={handler.name}" in result
#     assert "Channel=5" in result
#     assert "Temp=42" in result
#
#
# def test_select_text_returns_none_if_not_selected():
#     """select_text should return None if frame is not in selected_frames."""
#     handler = FrameSelector.HANDLERS[3]
#     handler.short_id = 0x4444
#     handler.parse = classmethod(lambda cls, frm: {"Val": 7})
#
#     frame = DummyFrame(short_id=0x4444, channel=7, time_s=11.0)
#     selected = []  # not selected
#
#     result = FrameSelector.select_text(frame, selected)
#     assert result is None

# from bank.bank_account import BankAccount
# from bank.currency import CurrencyConverter, CurrencyAPIClient
#
# from unittest.mock import MagicMock
#
# @pytest.fixture
# def converter_fixture():
#     mocked_client = MagicMock(spec=CurrencyAPIClient)
#     mocked_client.get_rate.return_value = 28
#     return CurrencyConverter(api_client=mocked_client)
#
# @pytest.fixture
# def bank_account_with_bonus(converter_fixture):
#     bank_account = BankAccount(name="your name",
#                                  currency="CZK",
#                                  currency_converter=converter_fixture,
#                                  bonus=100)
#     return bank_account
#
# @pytest.fixture
# def bank_account_without_bonus(converter_fixture):
#     bank_account = BankAccount(name="your name",
#                                  currency="CZK",
#                                  currency_converter=converter_fixture)
#     return bank_account
#
# def test_bonus_no_bonus_account(bank_account_without_bonus):
#     assert bank_account_without_bonus.get_balance() == 0
#
# def test_bonus_account(bank_account_with_bonus):
#     assert bank_account_with_bonus.get_balance() == 100
#
#
# def test_withdrawal_same_currency(bank_account_with_bonus):
#     bank_account_with_bonus.withdraw(10, "CZK")
#     assert bank_account_with_bonus.get_balance() == 90
#
#
# def test_withdrawal_different_currency(bank_account_with_bonus):
#     bank_account_with_bonus.withdraw(2, "EUR")
#     assert bank_account_with_bonus.get_balance() == 44