import pytest
from pytest_bdd import given
from pytest_bdd import scenarios


scenarios('features/calculator.feature',
          example_converters=dict(number_1=int, number_2=int, result=int))


@given('I have powered calculator on')
def power_on_calculator(driver):
    print('PLATFORM NAME')
    if pytest.globalDict['driver']:
        print(pytest.globalDict['driver'].desired_capabilities['platformName'])
    else:
        print('NONE')
    print('PLATFORM NAME')
    if driver:
        print(driver.desired_capabilities['platformName'])
    else:
        print('NONE')
    pytest.globalDict['number'] = []
