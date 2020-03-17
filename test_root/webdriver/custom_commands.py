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
