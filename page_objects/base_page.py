from selenium.webdriver.support import expected_conditions as ec

from webdriver.custom_wait import CustomWait


class BasePage:

    def __init__(self, selenium, base_url):
        self.base_url = base_url
        self.selenium = selenium
        self.wait = CustomWait(self.selenium)

    def open(self, **kwargs):
        self.selenium.get('%s/' % self.base_url)

    def is_loaded(self, **kwargs):
        self.wait.until(ec.url_matches('%s/' % self.base_url))
