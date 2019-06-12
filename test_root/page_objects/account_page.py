from assertpy import assert_that
from selenium.webdriver.common.by import By

from test_root.page_objects.base_page import BasePage
from test_root.page_objects.locators import AccountPageLocators


# pylint: disable=line-too-long
class AccountPage(BasePage):

    def __init__(self, selenium):
        super().__init__(selenium, '')

    @property
    def __back_button(self):
        return self.selenium.find_element(By.XPATH, AccountPageLocators().back_button)

    @property
    def __content_title(self):
        return self.selenium.find_element(By.XPATH, AccountPageLocators().content_title)

    @property
    def __check_button(self):
        return self.selenium.find_element(By.XPATH, AccountPageLocators().check_button % 'Check')

    @property
    def __title(self):
        return self.selenium.find_element(By.XPATH, AccountPageLocators().title)

    @property
    def __email_field_label(self):
        return self.selenium.find_element(By.XPATH, AccountPageLocators().email_field_label)

    @property
    def __email_field_input(self):
        return self.selenium.find_element(By.XPATH, AccountPageLocators().email_field_input)

    @property
    def __email_field_input_placeholder(self):
        return self.selenium.find_element(By.XPATH, AccountPageLocators().email_field_input_placeholder)

    def is_loaded(self):
        self.wait.until(self.__back_button.get_property('hidden') is False)
        self.wait.until(self.__title.get_property('hidden') is False)
        assert_that(self.__title.text).is_equal_to_ignoring_case('Check Account')
        self.wait.until(self.__content_title.get_property('hidden') is False)
        assert_that(self.__content_title.text).is_equal_to_ignoring_case('Enter any username or email and\nwe\'ll check if it\'s been hacked')
        self.wait.until(self.__check_button.get_property('hidden') is False)
        assert_that(self.__check_button.text).is_equal_to_ignoring_case('Check')
        self.wait.until(self.__email_field_label.get_property('hidden') is False)
        assert_that(self.__email_field_label.text).is_equal_to_ignoring_case('Your username or email')
        self.wait.until(self.__email_field_input.get_property('hidden') is False)
        assert_that(self.__email_field_input_placeholder.get_attribute('placeholder')).is_equal_to_ignoring_case('Username or email')

    def fill_email(self, email):
        self.__email_field_input.send_keys(email)

    def check_email(self):
        self.__check_button().click()
