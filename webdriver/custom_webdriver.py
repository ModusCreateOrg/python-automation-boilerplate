# This Base class is serving basic attributes for every single page inherited from Page class
from appium import webdriver
from selenium.common.exceptions import NoAlertPresentException, WebDriverException

from selenium.webdriver.support.wait import WebDriverWait

from webdriver.custom_expected_conditions import is_webview_present, is_ionic_loaded
from webdriver.custom_webelement import CustomWebElement


class WebDriverCustom(webdriver.Remote):
    _web_element_cls = CustomWebElement

    # pylint: disable=too-many-arguments
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=None, browser_profile=None,
                 proxy=None, keep_alive=False):
        webdriver.Remote.__init__(self, command_executor, desired_capabilities, browser_profile, proxy, keep_alive)
        self.is_tablet = False

    def create_web_element(self, element_id):
        """Creates a web element with the specified `element_id`."""
        return self._web_element_cls(self, element_id, w3c=self.w3c)

    def switch_to_webview_context(self):
        wait = WebDriverWait(self, 60)
        wait.until(is_webview_present(self), 'WEBVIEW context initialization failed')
        webview_context = None
        if self.desired_capabilities['platformName'].lower() == 'ios':
            webview_context = next(context for context in self.contexts if 'WEBVIEW_' in context)
        if self.desired_capabilities['platformName'].lower() == 'android':
            webview_context = next(context for context in self.contexts if 'WEBVIEW_com.pfizer' in context)
        # pylint: disable=no-member
        self.switch_to.context(webview_context)

    def set_platform(self):
        wait = WebDriverWait(self, 120)
        wait.until(is_ionic_loaded(self), 'Ionic not loaded')
        self.is_tablet = self.execute_script('return Ionic.platform.is("tablet")')

    # System Alert
    def accept_notification_alert(self):
        print('Accepting Notifications alert')
        try:
            # Fixme implicit wait fix needed here
            self.implicitly_wait(5)

            self.switch_to.alert.accept()

            from tests.utils import get_driver_params
            driver_params = get_driver_params()
            self.implicitly_wait(driver_params['implicit_wait_time'])

        except NoAlertPresentException:
            print('System alert was not present. Android OS testing.')
        except WebDriverException as error:
            print('Webdriver error: %s' % error.msg)

    # System Alert
    def dismiss_notification_alert(self):
        print('Dismissing Notifications alert')
        try:
            # Fixme implicit wait fix needed here
            self.implicitly_wait(5)

            self.switch_to.alert.dismiss()

            from tests.utils import get_driver_params
            driver_params = get_driver_params()
            self.implicitly_wait(driver_params['implicit_wait_time'])

        except NoAlertPresentException:
            print('System alert was not present. Android OS testing.')
        except WebDriverException as error:
            print('Webdriver error: %s' % error.msg)
