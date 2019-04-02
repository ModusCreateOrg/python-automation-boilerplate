from tests.pages.base_page import BasePage
from tests.pages.locators import WelcomeLocators


class WelcomePage(BasePage):
    def assert_welcome_page(self):
        self.wait_for_animation()
        self.find_element(*WelcomeLocators.page_modal)
        self.find_element(*WelcomeLocators.page_logo)
        self.find_element(*WelcomeLocators.page_title)

    def get_started(self):
        self.wait_for_animation()
        self.find_element(*WelcomeLocators.get_started_button).click()
