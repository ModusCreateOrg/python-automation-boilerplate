from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException


# pylint: disable=invalid-name
class is_webview_present:
    def __init__(self, driver):
        self.driver = driver

    def __call__(self, driver):
        print('Printing app contexts: ' + ' / '.join(self.driver.contexts))
        if self.driver.desired_capabilities['platformName'].lower() == 'ios':
            return any('WEBVIEW_' in context for context in self.driver.contexts)
        if self.driver.desired_capabilities['platformName'].lower() == 'android':
            return any('WEBVIEW_com.pfizer' in context for context in self.driver.contexts)
        return None


# pylint: disable=invalid-name
class is_ionic_loaded:
    def __init__(self, driver):
        self.driver = driver

    def __call__(self, driver):
        return self.driver.execute_script('return Ionic != undefined && Ionic.platform != undefined;')


# pylint: disable=invalid-name
class visibility_of_child_element_located:
    """ An expectation for checking that a child element, known to be present on the
    DOM of a page, is visible. Visibility means that the element is not only
    displayed but also has a height and width that is greater than 0.
    element is the WebElement
    returns the (same) WebElement once it is visible
    """

    def __init__(self, parent_element, locator):
        self.parent_element = parent_element
        self.locator = locator

    def __call__(self, driver):
        try:
            return _child_element_if_visible(self.parent_element.find_element(*self.locator))
        except StaleElementReferenceException:
            return False


# pylint: disable=invalid-name
class invisibility_of_child_element_located:
    """ An Expectation for checking that an element is either invisible or not
    present on the DOM.
    """

    def __init__(self, parent_element, locator):
        self.parent_element = parent_element
        self.locator = locator

    def __call__(self, driver):
        try:
            return _child_element_if_visible(self.parent_element.find_element(*self.locator), False)
        except (NoSuchElementException, StaleElementReferenceException):
            return True


# pylint: disable=invalid-name
class wait_for_the_attribute_value:
    def __init__(self, element, attribute, value):
        self.element = element
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = self.element.get_attribute(self.attribute)
            return element_attribute == self.value
        except (NoSuchElementException, StaleElementReferenceException):
            return False


# pylint: disable=invalid-name
class wait_for_condition:
    def __init__(self, condition):
        self.condition = condition

    def __call__(self, driver):
        return self.condition


def _child_element_if_visible(element, visibility=True):
    return element if element.is_displayed() == visibility else False
