from time import sleep

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# This Base class is serving basic attributes for every single page inherited from Page class


class BasePage(object):
    def __init__(self, driver):
        self.base_url = None
        self.driver = driver

    def find_element(self, *locator):
        if locator.__len__() == 2:
            return self.driver.find_element(*locator)
        return self.driver.find_element(*(locator[1], locator[2] % locator[0]))

    def find_elements(self, *locator):
        if locator.__len__() == 2:
            return self.driver.find_elements(*locator)
        return self.driver.find_elements(*(locator[1], locator[2] % locator[0]))

    def wait_for_element_visible(self, *locator):
        wait = WebDriverWait(self.driver, 10)
        if locator.__len__() == 2:
            return wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
        return wait.until(EC.visibility_of_element_located((locator[1], locator[2] % locator[0])))

    def wait_for_element_not_visible(self, *locator):
        wait = WebDriverWait(self.driver, 10)
        if locator.__len__() == 2:
            return wait.until(EC.invisibility_of_element_located((locator[0], locator[1])))
        return wait.until(EC.invisibility_of_element_located((locator[1], locator[2] % locator[0])))

    def wait_for_animation(self):
        sleep(1)

    def open(self, url):
        url = self.base_url + url
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def scroll_to_element(self, *locator):
        element = self.find_element(*locator)
        scroll = ActionChains(self.driver).move_to_element(element)
        scroll.perform()

    def accept_alert(self):
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            print('System alert was not present. Android OS testing.')
            pass

    def dismiss_alert(self):
        try:
            self.driver.switch_to.alert.dismiss()
        except NoAlertPresentException:
            print('System alert was not present. Android OS testing.')
            pass
