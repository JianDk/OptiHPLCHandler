import unittest

from applications import (
    determine_if_isocratic_method,
    determine_last_high_flow_time,
    determine_max_compositon_value,
    determine_strong_eluent,
)


class TestEmpowerTools(unittest.TestCase):
    def test_determine_if_isocratic_method(self):
        # Create a sample gradient table
        gradient_table = [
            {
                "Time": "Initial",
                "Flow": "0.3",
                "CompositionA": "90.0",
                "CompositionB": "10",
                "Curve": "Initial",
            },
            {
                "Time": "10.0",
                "Flow": "0.3",
                "CompositionA": "90",
                "CompositionB": "10",
                "Curve": "6",
            },
            {
                "Time": "10.1",
                "Flow": "0.3",
                "CompositionA": "90",
                "CompositionB": "10",
                "Curve": "6",
            },
        ]
        # Assert the method is isocratic
        assert determine_if_isocratic_method(gradient_table) is True

        # Assess float correctly handled
        gradient_table = [
            {
                "Time": "Initial",
                "Flow": "0.3",
                "CompositionA": "90",
                "CompositionB": "10",
                "Curve": "Initial",
            },
            {
                "Time": "10.0",
                "Flow": "0.3",
                "CompositionA": "90",
                "CompositionB": "10",
                "Curve": "6",
            },
            {
                "Time": "10.1",
                "Flow": "0.3",
                "CompositionA": "90",
                "CompositionB": "10",
                "Curve": "6",
            },
        ]
        # Assert the method is isocratic
        assert determine_if_isocratic_method(gradient_table) is True

        # Create a sample gradient table
        gradient_table = [
            {
                "Time": "Initial",
                "Flow": "0.3",
                "CompositionA": "90",
                "CompositionB": "10",
                "Curve": "Initial",
            },
            {
                "Time": "10.0",
                "Flow": "0.3",
                "CompositionA": "80",
                "CompositionB": "20",
                "Curve": "6",
            },
            {
                "Time": "10.1",
                "Flow": "0.3",
                "CompositionA": "70",
                "CompositionB": "30",
                "Curve": "6",
            },
        ]
        # Assert the method is not isocratic
        assert determine_if_isocratic_method(gradient_table) is False


def test_determine_index_of_max_compositon_value(self):
    gradient_table = [
        {"CompositionA": "10.0", "CompositionB": "20.0"},
        {"CompositionA": "15.0", "CompositionB": "25.0"},
        {"CompositionA": "5.0", "CompositionB": "15.0"},
    ]
    composition = "CompositionB"
    assert determine_max_compositon_value(gradient_table, composition) == (
        1,
        "25.0",
    )

    composition = "CompositionA"
    assert determine_max_compositon_value(gradient_table, composition) == (
        1,
        "15.0",
    )

    gradient_table = [
        {"CompositionZ": "10.0", "CompositionB": "20.0"},
    ]
    try:
        determine_max_compositon_value(gradient_table, "CompositionZ")
    except ValueError as e:
        assert str(e) == "Invalid composition string."


def test_determine_strong_eluent(self):
    gradient_table = [
        {"CompositionA": "10.0", "CompositionB": "90.0"},
        {"CompositionA": "90.0", "CompositionB": "10.0"},
        {"CompositionA": "10.0", "CompositionB": "90.0"},
    ]
    assert determine_strong_eluent(gradient_table) == ("CompositionA", ["CompositionB"])

    gradient_table = [
        {"CompositionB": "10.0", "CompositionA": "90.0"},
        {"CompositionB": "90.0", "CompositionA": "10.0"},
        {"CompositionB": "10.0", "CompositionA": "90.0"},
    ]
    assert determine_strong_eluent(gradient_table) == ("CompositionB", ["CompositionA"])

    gradient_table = [
        {"CompositionA": "90.0", "CompositionB": "10.0"},
    ]
    try:
        determine_strong_eluent(gradient_table)
    except ValueError as e:
        assert str(e) == "Cannot determine strong eluent for isocratic method."


def test_determine_last_high_flow_time(self):
    gradient_table = [
        {"Time": 0, "Flow": 0.5},
        {"Time": 10, "Flow": 1},
        {"Time": 20, "Flow": 1},
        {"Time": 30, "Flow": 0.1},
    ]
    assert determine_last_high_flow_time(gradient_table) == 20
