# pylint: disable=import-outside-toplevel
from assertpy import assert_that
from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage
from page_objects.locators import ActionLocators, ContextLocators


class AccountPage(BasePage):

    def __init__(self, selenium, base_url):
        super().__init__(selenium, base_url)

        import pytest
        self._env = pytest.globalDict['env']

    @property
    def _back_button(self):
        return self._selenium.find_element(By.XPATH, ActionLocators.back_button)

    @property
    def _check_button(self):
        return self._selenium.find_element(By.XPATH, ActionLocators.check_button)

    @property
    def _page_title(self):
        return self._selenium.title

    @property
    def _title(self):
        return self._selenium.find_element(By.XPATH, ContextLocators.title)

    @property
    def _text_field(self):
        return self._selenium.find_element(By.XPATH, ActionLocators.text_field % 'email')

    @property
    def _text_field_label(self):
        return self._selenium.find_element(By.XPATH, ContextLocators.text_field_label)

    def validate_action_buttons(self):
        assert_that(self._back_button.get_property('hidden')).is_false()
        assert_that(self._check_button.get_property('hidden')).is_false()

    def validate_text_field(self):
        assert_that(self._text_field_label.get_property('hidden')).is_false()
        assert_that(self._text_field.get_property('hidden')).is_false()

    def is_loaded(self, **kwargs):
        self.wait.wait_for_element_visible(value='//ion-title', time_to_wait=20)
        assert_that(self._title.text).is_equal_to('Check Account')
