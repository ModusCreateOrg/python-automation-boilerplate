# pylint: disable=import-outside-toplevel
# pylint: disable=unused-variable
import base64
from io import BytesIO
from time import sleep

import cv2
import numpy as np
from PIL import Image
from selenium.webdriver import ActionChains


def add_custom_commands():
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

    @add_method(WebDriver)
    def shadow_find_element(self, css_selector):
        return self.execute_script('return document.shadowRoot.querySelector(arguments[0])', css_selector)

    @add_method(WebDriver)
    def shadow_cascade_find_element(self, *args):
        script = 'return document'
        for arg in args:
            script += '.querySelector("%s").shadowRoot' % arg
        script = script[:-11] + ';'
        return self.execute_script(script)

    @add_method(WebDriver)
    def shadow_find_elements(self, css_selector):
        return self.execute_script('return document.shadowRoot.querySelectorAll(arguments[0])', css_selector)

    @add_method(WebElement)
    def shadow_find_element(self, css_selector):
        return self.parent.execute_script('return arguments[0].shadowRoot.querySelector(arguments[1])', self, css_selector)

    @add_method(WebElement)
    def shadow_cascade_find_element(self, *args):
        script = 'return %s' % self
        for arg in args:
            script += '.shadowRoot.querySelector("%s")' % arg
        return self.parent.execute_script(script)

    @add_method(WebElement)
    def shadow_find_elements(self, css_selector):
        return self.parent.execute_script('return arguments[0].shadowRoot.querySelectorAll(arguments[1])', self, css_selector)

    @add_method(WebElement)
    def get_cropped_screenshot_as_base64(self, y_point=0):
        base_score = 0.94
        # Scroll element into view
        self.parent.execute_script("window.scrollBy(0,100000)")
        sleep(1)
        actions = ActionChains(self.parent)
        self.parent.execute_script("arguments[0].scrollIntoView(true);", self)
        sleep(1)

        image_base_64 = self.parent.get_screenshot_as_base64()

        # im = Image.open(screenshot_url)
        im = Image.open(BytesIO(base64.b64decode(image_base_64)))
        im = im.crop((0, y_point, im.width, (im.height * 0.75 - y_point)))

        return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

    # Does not work on mobile where location and size are not correctly calculated
    @add_method(WebElement)
    def get_screenshot_as_base64(self, threshold=0):
        location = self.location
        size = self.size

        if self.parent.desired_capabilities['browserName'] in ["Chrome", "chrome", "MicrosoftEdge", "microsoftedge"]:
            self.parent.execute_script("window.scrollBy(0,100000)")
            sleep(1)
            # Scroll element into view
            actions = ActionChains(self.parent)
            actions.move_to_element(self).perform()
            sleep(1)
            location = self.location_once_scrolled_into_view

        if self.parent.desired_capabilities['browserName'] in ["Safari", "safari"]:
            self.parent.execute_script("window.scrollBy(0,100000)")
            sleep(1)
            # Scroll element into view
            self.parent.execute_script("arguments[0].scrollIntoView(true);", self)
            sleep(1)
            location = self.location_once_scrolled_into_view

        x_point = location['x']
        width = location['x'] + size['width']

        # Is needed for iOS screenshot to remove browser header controls.
        # On iOS the screenshot includes browser header and footer controls
        y_point = location['y'] + threshold
        height = location['y'] + size['height'] - threshold

        image_base_64 = self.parent.get_screenshot_as_base64()
        # im = Image.open(screenshot_url)
        img = Image.open(BytesIO(base64.b64decode(image_base_64)))
        img = img.crop((int(x_point), int(y_point), int(width), int(height)))

        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def add_method(cls):
    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally

    return decorator
