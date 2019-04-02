from assertpy import assert_that
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from page_objects.base_page import BasePage
from page_objects.locators import HomePageLocators


class HomePage(BasePage):

    def __init__(self, selenium, base_url, i18n):
        super().__init__(selenium, base_url)
        self.base_url = base_url
        self.i18n = i18n
        self.page_url = ''

    @property
    def __account_button(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.button % 'Account')

    @property
    def __app_logo(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.app_logo)

    @property
    def __app_store_link_android(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.app_store_link_android)

    @property
    def __app_store_link_ios(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.app_store_link_ios)

    @property
    def __app_title(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.app_title)

    @property
    def __dialog_close_button(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.dialog_close_button)

    @property
    def __dialog_done_button(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.dialog_done_button)

    @property
    def __dialog_paragraph(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.dialog_paragraph % self.i18n['homepage_dialog_resume'])

    @property
    def __how_it_works_link(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.footer_link)

    @property
    def __password_button(self):
        return self.selenium.find_element(By.XPATH, HomePageLocators.button % 'Password')

    def open(self):
        self.selenium.get('%s/%s' % (self.base_url, self.page_url))

    def is_loaded(self):
        self.wait.until(ec.url_matches('%s/%s' % (self.base_url, self.page_url)))
        self.wait.until(self.__account_button.get_property('hidden') is False)
        self.wait.until(self.__password_button.get_property('hidden') is False)

    def click_how_it_works(self):
        self.__how_it_works_link.click()

    def logo_visible(self):
        self.wait.until(self.__app_logo.get_property('hidden') is False)

    def title_visible(self):
        self.wait.until(self.__app_title.get_property('hidden') is False)
        assert_that(self.__app_title.get_property('innerText')).is_equal_to(self.i18n['app_title'])

    def store_links_visible(self):
        self.wait.until(self.__app_store_link_android.get_property('hidden') is False)
        self.wait.until(self.__app_store_link_ios.get_property('hidden') is False)
