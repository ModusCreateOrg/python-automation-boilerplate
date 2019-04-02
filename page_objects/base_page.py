from webdriver.custom_wait import CustomWait


class BasePage:

    def __init__(self, selenium, base_url):
        self.base_url = base_url
        self.selenium = selenium
        self.wait = CustomWait(self.selenium)

    def open(self, **kwargs):
        pass

    def is_loaded(self, **kwargs):
        pass
