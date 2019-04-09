from pytest_bdd import given, parsers

from page_objects.home_page import HomePage
from utils.utils import get_file_path


@given(parsers.re('User navigates to "(?P<filename>(.*)+)" homepage'))
def navigate_to_homepage(selenium, base_url, variables, filename):
    is_mobile_web = True if 'platformName' in selenium.desired_capabilities \
                            and (selenium.desired_capabilities['platformName'].lower() == 'ios'
                                 or selenium.desired_capabilities['platformName'].lower() == 'android') \
        else False
    is_bs_mobile_web = True if 'device' in selenium.desired_capabilities else False
    if not is_mobile_web and not is_bs_mobile_web:
        selenium.maximize_window()
    base_url = 'file://%s' % get_file_path(filename)
    HomePage(selenium, base_url, variables['en']).open()
