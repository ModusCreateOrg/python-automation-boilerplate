# pylint: disable=import-outside-toplevel
# pylint: disable=unused-variable
def add_custom_commands():
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

    @add_method(WebDriver)
    def get_cropped_screenshot_as_file(self, screenshot_url, y_point=0):
        self.get_screenshot_as_file(screenshot_url)

        from PIL import Image
        im = Image.open(screenshot_url)
        im = im.crop((0, y_point, im.width, im.height - y_point))
        im.save(screenshot_url)

    # Does not work on mobile where location and size are not correctly calculated
    @add_method(WebElement)
    def get_screenshot_as_file(self, screenshot_url, threshold=0):
        location = self.location
        size = self.size
        x_point = location['x']
        width = location['x'] + size['width']

        # Is needed for iOS screenshot to remove browser header controls.
        # On iOS the screenshot includes browser header and footer controls
        y_point = location['y'] + threshold
        height = location['y'] + size['height'] - threshold
        self.parent.get_screenshot_as_file(screenshot_url)

        from PIL import Image
        im = Image.open(screenshot_url)
        im = im.crop((int(x_point), int(y_point), int(width), int(height)))
        im.save(screenshot_url)


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
