from time import sleep

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class CustomWebElement(WebElement):

    def click(self, i=29):
        try:
            sleep(2)
            super(CustomWebElement, self).click()
            sleep(1)
        except WebDriverException as error:
            if 'Other element would receive the click:' in error.msg and i != 0:
                if i == 29:
                    print('Retrying click. Failed due to: %s' % error.msg)
                self.click(i - 1)
            else:
                raise error

    def clear(self):
        """Clears the text if it's a text entry element."""
        text_length = self.get_attribute('value').__len__()
        text_length = text_length if text_length != 0 else self.text.__len__()
        if text_length != 0:
            # pylint: disable=unused-variable
            for i in range(text_length):
                self.send_keys(keys=Keys.ARROW_RIGHT)
                self.send_keys(keys=Keys.BACK_SPACE)

    def send_keys(self, i=29, length=0, keys=tuple):
        try:
            if isinstance(keys, tuple):
                super(CustomWebElement, self).send_keys(keys)
            elif keys in Keys.__dict__.values():
                super(CustomWebElement, self).send_keys(keys)
            else:
                expected_value = str(keys)
                super(CustomWebElement, self).send_keys(keys)
                if (length == 0 and expected_value != self.get_attribute('value')) or \
                    (length != 0 and expected_value[:length] != self.get_attribute('value')):
                    self.clear()
                    super(CustomWebElement, self).send_keys(keys)
        except WebDriverException as error:
            if 'Element is not currently visible and may not be manipulated' in error.msg:
                sleep(2)
            if i != 0:
                self.send_keys(i=i - 1, length=length, keys=keys)
            else:
                raise error
        except Exception as error:
            raise error
