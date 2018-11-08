from unittest.mock import patch
import sys, os, io
import pytest

sys.path.insert(0, os.path.abspath('..'))
from app import *

test_cases_numbers = list(range(1, 13))


@pytest.fixture()
def before():
    print("\r")


def get_input_output(input_file):
    with open("resources/testcases/{}.txt".format(input_file), 'r') as file:
        data = file.read()
    return data


# @pytest.mark.usefixtures("before")
@pytest.mark.parametrize("test_case_number", test_cases_numbers)
def test_eval(test_case_number):
    input = get_input_output("input{}".format(test_case_number)).split("\n")
    output = get_input_output("output{}".format(test_case_number))

    with patch('builtins.input', side_effect=input):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            my_main()
        assert fake_stdout.getvalue() == "{}\n".format(output)


def test_format_numerals():
    raw_numerals = [".oo.o...oo..ooo.oooo....o...oo..ooo.oooo....o...oo..ooo.oooo....o...oo..ooo.oooo",
                    "o..o................____________________________________________________________",
                    ".oo.....................................________________________________________",
                    "............................................................____________________"]
    expected_numerals = {0: '.oo.o..o.oo.....', 1: 'o...............', 2: 'oo..............', 3: 'ooo.............', 4: 'oooo............', 5: '....____........', 6: 'o...____........',
                         7: 'oo..____........', 8: 'ooo.____........', 9: 'oooo____........', 10: '....________....', 11: 'o...________....', 12: 'oo..________....', 13: 'ooo.________....',
                         14: 'oooo________....', 15: '....____________', 16: 'o...____________', 17: 'oo..____________', 18: 'ooo.____________', 19: 'oooo____________'}

    assert format_numerals(4, 4, raw_numerals) == expected_numerals


def test_decimal_to_base20():
    res = convert_decimal_to_base20(0)
    assert res == [0]

    res = convert_decimal_to_base20(20)
    assert res == [0, 1]

    res = convert_decimal_to_base20(25)
    assert res == [5, 1]


def test_get_digits_from_maya_number():
    number = "o...____........ooo............."
    expected_res = ["ooo.............", "o...____........"]

    assert get_digits_from_maya_number(4, 4, number) == expected_res


def test_maya_to_base_20():
    numerals = {0: '.oo.o..o.oo.....', 1: 'o...............', 2: 'oo..............', 3: 'ooo.............', 4: 'oooo............', 5: '....____........', 6: 'o...____........',
                7: 'oo..____........', 8: 'ooo.____........', 9: 'oooo____........', 10: '....________....', 11: 'o...________....', 12: 'oo..________....', 13: 'ooo.________....',
                14: 'oooo________....', 15: '....____________', 16: 'o...____________', 17: 'oo..____________', 18: 'ooo.____________', 19: 'oooo____________'}
    maya_number = ["ooo.............", "o...____........", "oooo____........", ".oo.o..o.oo....."]
    expected_base_20_number = [3, 6, 9, 0]

    assert maya_to_base_20(numerals, maya_number) == expected_base_20_number


def test_convert_base_20_to_decimal():
    base_20_number = [5, 1, 7]
    expected_res = 2825

    assert convert_base_20_to_decimal(base_20_number) == expected_res
