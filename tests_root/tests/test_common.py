import pytest
from pytest_bdd import when, parsers


@when(parsers.parse('I enter {number:d} into the calculator'))
def input_number(number):
    return pytest.globalDict['number'].append(number)


@when('I enter <number_1> into the calculator')
def input_number_first(number_1):
    input_number(number_1)


@when('I enter <number_2> into the calculator')
def input_number_second(number_2):
    input_number(number_2)


@when('I press add')
def sum_numbers():
    pytest.globalDict['sum'] = sum(pytest.globalDict['number'])
