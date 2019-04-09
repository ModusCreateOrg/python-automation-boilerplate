from assertpy import assert_that
from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage
from page_objects.locators import HomePageLocators


class HomePage(BasePage):

    def __init__(self, selenium, base_url, i18n):
        super().__init__(selenium, base_url)
        self.i18n = i18n
        self.page_url = ''

    @property
    def __page_text(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.page_text)

    def open(self):
        self.selenium.get('%s' % self.base_url)

    def inner_text_validation(self, text):
        assert_that(self.__page_text.get_property('innerText')).is_equal_to(text)

    def text_content_validation(self, text):
        assert_that(self.__page_text.get_property('textContent')).is_equal_to(text)
