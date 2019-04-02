import pytest
from pytest_bdd import given
from pytest_bdd import scenarios


scenarios('features/calculator.feature',
          example_converters=dict(number_1=int, number_2=int, result=int))


@given('I have powered calculator on')
def power_on_calculator():
    pytest.globalDict['number'] = []
