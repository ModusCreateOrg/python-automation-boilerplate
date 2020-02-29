# pylint: disable=import-outside-toplevel
from assertpy import assert_that
from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage
from page_objects.locators import ActionLocators, ContextLocators
from utils.utils import compare_images


class HomePage(BasePage):

    def __init__(self, selenium, base_url):
        super().__init__(selenium, base_url)

        import pytest
        self._env = pytest.globalDict['env']
        self._page_url = ''

        extension = '.png'
        self._base_logo_screenshot_url = pytest.globalDict['base_screenshot_dir'] + '/homepage/base/logo' + extension
        self._actual_logo_screenshot_url = pytest.globalDict['actual_screenshot_dir'] + '/homepage/actual/logo' + extension
        self._diff_logo_screenshot_url = pytest.globalDict['diff_screenshot_dir'] + '/homepage/diff/logo' + extension
        self._base_account_button_screenshot_url = pytest.globalDict['base_screenshot_dir'] + '/homepage/base/account_button' + extension
        self._actual_account_button_screenshot_url = pytest.globalDict['actual_screenshot_dir'] + '/homepage/actual/account_button' + extension
        self._diff_account_button_screenshot_url = pytest.globalDict['diff_screenshot_dir'] + '/homepage/diff/account_button' + extension

    @property
    def _account_button(self):
        return self._selenium.find_element(By.XPATH, ActionLocators.button % 'Account logo')

    @property
    def _app_store_link(self):
        return self._selenium.find_element(By.XPATH, ActionLocators.link % 'beepios')

    @property
    def _google_play_link(self):
        return self._selenium.find_element(By.XPATH, ActionLocators.link % 'beepandroid')

    @property
    def _header(self):
        return self._selenium.find_element(By.XPATH, ContextLocators.title)

    @property
    def _how_does_it_work_link(self):
        return self._selenium.find_element(By.XPATH, '//span[.="How does it work?"]')

    @property
    def _logo(self):
        return self._selenium.find_element(By.XPATH, ContextLocators.image % 'Beep logo')

    @property
    def _title(self):
        return self._selenium.find_element(By.XPATH, ContextLocators.title)

    @property
    def _password_button(self):
        return self._selenium.find_element(By.XPATH, ActionLocators.button % 'Password logo')

    def click_button(self, element):
        self[element].click()

    def validate_element_is_visible(self, element):
        assert_that(self[element].get_property('hidden')).is_equal_to(False)

    def validate_account_button_default_visual(self):
        self._account_button.get_screenshot_as_file(self._actual_account_button_screenshot_url)
        score = compare_images(self._base_account_button_screenshot_url, self._actual_account_button_screenshot_url, self._diff_account_button_screenshot_url)
        assert_that(score, 'Actual _account_button screenshot is different from Base with %s. Diff saved here: %s'
                    % (score, self._diff_account_button_screenshot_url)).is_greater_than_or_equal_to(0.98)

    def validate_logo_default_visual(self):
        self._logo.get_screenshot_as_file(self._actual_logo_screenshot_url)
        score = compare_images(self._base_logo_screenshot_url, self._actual_logo_screenshot_url, self._diff_logo_screenshot_url)
        assert_that(score, 'Actual _logo screenshot is different from Base with %s. Diff saved here: %s'
                    % (score, self._diff_logo_screenshot_url)).is_greater_than_or_equal_to(0.98)

    def open(self, **kwargs):
        self._selenium.get('%s/%s' % (self._base_url, self._page_url))

    def is_loaded(self, **kwargs):
        self.wait.wait_for_element_visible(value=ContextLocators.image % 'Beep logo', time_to_wait=30)
        self.wait.wait_for_the_attribute_value(element=self._logo, attribute='class', value='ion-page hydrated', time_to_wait=30)
