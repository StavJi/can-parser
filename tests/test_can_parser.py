import pytest
from unittest.mock import MagicMock

from frame_selector import FrameSelector
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

def test_parse_tmc_status3():
    payload = [5, 80, 0, 0, 0, 0, 0, 0]  # Test data
    result = FrameParser.parse_tmc_status3(payload)
    assert "PowerSource_Status_1" in result
    assert isinstance(result["PowerControl_State_1_s"], str)

def test_parse_acu_status():
    payload = [20, 85, 0, 0, 0, 10, 20, 0] # Test data
    result = FrameParser.parse_acu_status(1, payload)
    assert result["diesel_state_1"] == 1
    assert result["cooling_active_1"] == 1
    assert "low_pressure_1" in result
    assert "high_pressure_1" in result

# Dummy frame
class DummyFrame:
    def __init__(self, short_id, channel, payload, time_s="123.456"):
        self.short_id = short_id
        self.channel = channel
        self.payload = payload
        self.time_s = time_s


def test_parse_returns_text():
    def fake_parser(channel, payload):
        return {"diesel_state": 1, "cooling_active": 0}

    # Select first handler
    handler = FrameSelector.HANDLERS[0]
    handler.parser_method = fake_parser
    handler.short_id = 0x111

    frame = DummyFrame(short_id=0x111, channel=1, payload=[0x00])

    result = handler.parse(frame)

    assert isinstance(result, str)
    assert "Frame=" in result
    assert "diesel_state=1" in result

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