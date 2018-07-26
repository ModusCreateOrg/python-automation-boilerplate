
import time
import pytest
from appium import webdriver
from tests.utils import get_driver_params


def set_up():
    url = 'http://127.0.0.1:4723/wd/hub'
    desired_capabilities = {
        'autoWebview': True,
        'autoGrantPermissions': True,
        'platformName': 'iOS',
        'platformVersion': '11.2',
        'deviceName': 'iPhone 8 Plus',
        'app': 'test.ipa'
        }
    driver = webdriver.Remote(url, desired_capabilities)

    time.sleep(1)

    driver_params = get_driver_params()
    driver.implicitly_wait(driver_params['implicit_wait_time'])
    driver.timeout = driver_params['timeout']

    pytest.globalDict['driver'] = driver


def tear_down():
    pytest.globalDict['driver'].quit()

