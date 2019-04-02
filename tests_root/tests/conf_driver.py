import time
import pytest
from appium import webdriver
from tests.utils import get_driver_params


def set_up():
    url = 'http://127.0.0.1:4723/wd/hub'
    # pylint: disable=no-member
    desired_capabilities = {
        'autoWebview': True,
        'autoGrantPermissions': True,
        'platformName': 'iOS',
        'platformVersion': '11.0',
        'deviceName': 'iPhone 8 Plus',
        'app': '/Users/sergiu/ModusCreate/Pfizer/QuittersCircle/platforms/ios/build/emulator/Quitter\'s Circle.app',
        # 'appPackage': 'com.pfizerinternational.qcrefresh',
        # 'appActivity': '.MainActivity',
        # 'platformName': 'Android',
        # 'platformVersion': '8.1',
        # 'deviceName': 'Pixel_XL_Android_8.1',
        # 'app': '/Users/sergiu/ModusCreate/Pfizer/QuittersCircle/platforms/android/build/outputs/apk/debug/android-debug.apk'
    }
    driver = webdriver.Remote(url, desired_capabilities)

    time.sleep(1)

    driver_params = get_driver_params()
    driver.implicitly_wait(driver_params['implicit_wait_time'])
    driver.timeout = driver_params['timeout']

    pytest.globalDict['driver'] = driver


def tear_down():
    # pylint: disable=no-member
    pytest.globalDict['driver'].quit()
