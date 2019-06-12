from assertpy import assert_that
from selenium.webdriver.common.by import By

from test_root.page_objects.base_page import BasePage


# pylint: disable=line-too-long
from test_root.page_objects.locators import HomePageLocators


class HomePage(BasePage):

    def __init__(self, selenium):
        super().__init__(selenium, '')

    @property
    def __header_logo(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators().header_logo)

    @property
    def __content_title(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators().content_title)

    @property
    def __account_button(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators().account_button)

    @property
    def __password_button(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators().password_button)

    @property
    def __footer_title(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators().footer_title)

    @property
    def __footer_link(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators().footer_link)

    @property
    def __app_store_btn_ios(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators().app_store_btn_ios)

    @property
    def __app_store_btn_android(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators().app_store_btn_android)

    def is_loaded(self):
        self.wait.until(self.__header_logo.get_property('hidden') is False)
        assert_that(self.__header_logo.get_attribute('src')).contains_ignoring_case('/img/Beep-Logo.e5d20974.svg')
        self.wait.until(self.__content_title.get_property('hidden') is False)
        assert_that(self.__content_title.text).is_equal_to_ignoring_case('Check if you\'ve\nbeen hacked')
        self.wait.until(self.__account_button.get_property('hidden') is False)
        assert_that(self.__account_button.text).is_equal_to_ignoring_case('Account')
        self.wait.until(self.__password_button.get_property('hidden') is False)
        assert_that(self.__password_button.text).is_equal_to_ignoring_case('Password')
        if 'device' not in self.selenium.capabilities:
            self.wait.until(self.__footer_title.get_property('hidden') is False)
            assert_that(self.__footer_title.text).is_equal_to_ignoring_case('How does it work?')
            self.wait.until(self.__footer_link.get_property('hidden') is False)
            self.wait.until(self.__app_store_btn_ios.get_property('hidden') is False)
            self.wait.until(self.__app_store_btn_android.get_property('hidden') is False)

    def go_to_account(self):
        self.__account_button.click()

    def go_to_password(self):
        self.__password_button.click()

    def go_to_how_it_works(self):
        self.__footer_link.click()
