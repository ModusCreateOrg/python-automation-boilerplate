# pylint: disable=import-outside-toplevel
from pytest_bdd import given

from page_objects.home_page import HomePage


@given("I load the Beep app")
def load_beep_app(selenium, base_url):
    import pytest
    if pytest.globalDict['env']['app'] is False:
        HomePage(selenium, base_url).open()
    if pytest.globalDict['env']['app'] is True:
        webview = selenium.contexts[1]
        selenium.switch_to.context(webview)
