from webdriver.custom_wait import CustomWait


class BasePage:

    def __init__(self, selenium, base_url):
        self._base_url = base_url
        self._selenium = selenium
        self.wait = CustomWait(self._selenium)

    def __getitem__(self, key):
        return getattr(self, key)

    def open(self, **kwargs):
        pass

    def is_loaded(self, **kwargs):
        pass
