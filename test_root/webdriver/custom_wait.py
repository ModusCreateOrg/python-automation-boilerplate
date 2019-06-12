from time import sleep

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webdriver import custom_expected_conditions as CEC


class CustomWait:

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element_present(self, by=By.XPATH, value=None, text=None):
        if text is not None:
            value = value % text
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located((by, value)))

    def wait_for_element_visible(self, by=By.XPATH, value=None, text=None, wait_time=20):
        if text is not None:
            value = value % text
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located((by, value)))

    def wait_for_element_not_visible(self, by=By.XPATH, value=None, text=None):
        if text is not None:
            value = value % text

        wait = WebDriverWait(self.driver, 5)
        self.driver.implicitly_wait(3)
        result = wait.until(EC.invisibility_of_element_located((by, value)))
        # pylint: disable=no-member
        self.driver.implicitly_wait(pytest.globalDict['implicit_wait_time'])
        return result

    def wait_for_element_clickable(self, by=By.XPATH, value=None, text=None):
        if text is not None:
            value = value % text
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.element_to_be_clickable((by, value)))

    def wait_for_child_element_visible(self, parent_element, by=By.XPATH, value=None, text=None):
        if text is not None:
            value = value % text
        wait = WebDriverWait(self.driver, 10)
        return wait.until(CEC.visibility_of_child_element_located(parent_element, (by, value)))

    def wait_for_child_element_not_visible(self, parent_element, by=By.XPATH, value=None, text=None):
        if text is not None:
            value = value % text

        wait = WebDriverWait(self.driver, 5)
        self.driver.implicitly_wait(5)
        result = wait.until(CEC.invisibility_of_child_element_located(parent_element, (by, value)))
        # pylint: disable=no-member
        self.driver.implicitly_wait(pytest.globalDict['implicit_wait_time'])
        return result

    def wait_for_the_attribute_value(self, element, attribute, value):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(CEC.wait_for_the_attribute_value(element, attribute, value))

    def until(self, condition, time=15):
        wait = WebDriverWait(self.driver, time)
        result = wait.until(CEC.wait_for_condition(condition))
        return result

    # pylint: disable=no-member
    @staticmethod
    def static_wait(period=1):
        sleep(period)
