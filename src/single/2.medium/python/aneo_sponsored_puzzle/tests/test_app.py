from unittest.mock import patch
import sys, os, io
import pytest

sys.path.insert(0, os.path.abspath('..'))
from app import *

test_cases_numbers = [str(x) for x in range(1, 11)]


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
